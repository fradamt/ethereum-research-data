"""Parse Rust source files using tree-sitter and extract code units."""

from __future__ import annotations

import logging

from erd_index.models import Language, ParsedUnit, SourceKind
from erd_index.parse.treesitter_runtime import parse_source

__all__ = ["parse_rust_file"]

log = logging.getLogger(__name__)

_TOP_LEVEL_UNITS = {
    "function_item",
    "struct_item",
    "enum_item",
    "trait_item",
    "impl_item",
}


def parse_rust_file(
    source: str,
    *,
    path: str,
    repository: str = "",
    source_name: str = "",
) -> list[ParsedUnit]:
    """Parse a Rust file and return a list of ``ParsedUnit`` objects.

    Extracts functions, structs, enums, traits, impl blocks, and their members.
    Also extracts ``use`` declarations and doc comments.
    """
    tree = parse_source(source, "rust")
    root = tree.root_node
    source_bytes = source.encode("utf-8")

    imports = _extract_imports(root, source_bytes)
    module_path = _path_to_module(path)

    units: list[ParsedUnit] = []
    children = list(root.children)

    for i, child in enumerate(children):
        if child.type not in _TOP_LEVEL_UNITS:
            continue

        if child.type == "impl_item":
            _process_impl(
                child,
                units=units,
                source_bytes=source_bytes,
                path=path,
                repository=repository,
                source_name=source_name,
                imports=imports,
                module_path=module_path,
                preceding=children[:i],
            )
        else:
            unit = _process_node(
                child,
                source_bytes=source_bytes,
                path=path,
                repository=repository,
                source_name=source_name,
                imports=imports,
                module_path=module_path,
                parent_symbol="",
                preceding=children[:i],
            )
            if unit:
                units.append(unit)

            # For trait_item, also extract member functions.
            if child.type == "trait_item":
                trait_name = _node_name(child)
                _extract_members(
                    child,
                    units=units,
                    source_bytes=source_bytes,
                    path=path,
                    repository=repository,
                    source_name=source_name,
                    imports=imports,
                    module_path=module_path,
                    parent_symbol=trait_name,
                )

    return units


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_imports(root, source_bytes: bytes) -> list[str]:
    imports: list[str] = []
    for child in root.children:
        if child.type == "use_declaration":
            imports.append(child.text.decode("utf-8"))
    return imports


def _path_to_module(path: str) -> str:
    """Convert ``src/foo/bar.rs`` to ``foo::bar``."""
    mod = path.replace("/", "::").replace("\\", "::")
    # Strip common prefixes.
    for prefix in ("src::", "lib::"):
        if mod.startswith(prefix):
            mod = mod[len(prefix) :]
    for suffix in (".rs",):
        if mod.endswith(suffix):
            mod = mod[: -len(suffix)]
    if mod.endswith("::mod"):
        mod = mod[: -len("::mod")]
    if mod.endswith("::lib"):
        mod = mod[: -len("::lib")]
    return mod


def _node_name(node) -> str:
    name_node = node.child_by_field_name("name")
    if name_node:
        return name_node.text.decode("utf-8")
    # For impl_item, extract the type name.
    if node.type == "impl_item":
        return _impl_target(node)
    return ""


def _impl_target(node) -> str:
    """Extract the target type of an impl block (e.g. ``MyStruct`` from ``impl MyStruct``)."""
    type_node = node.child_by_field_name("type")
    if type_node:
        return type_node.text.decode("utf-8")
    # Fallback: look for type_identifier child.
    for child in node.children:
        if child.type == "type_identifier":
            return child.text.decode("utf-8")
        if child.type == "generic_type":
            ident = child.child_by_field_name("type")
            if ident:
                return ident.text.decode("utf-8")
    return ""


def _get_doc_comment(preceding: list, target_start_row: int) -> str:
    """Collect ``///`` and ``//!`` doc comment lines immediately before the target."""
    doc_lines: list[str] = []
    for node in reversed(preceding):
        if node.type in ("line_comment", "block_comment"):
            text = node.text.decode("utf-8")
            if node.end_point[0] < target_start_row - 1 - len(doc_lines):
                break
            if text.startswith("///") or text.startswith("//!"):
                cleaned = text.lstrip("/!").strip()
                doc_lines.insert(0, cleaned)
            else:
                break
        else:
            break
    return "\n".join(doc_lines)


def _symbol_kind(node) -> str:
    kind_map = {
        "function_item": "function",
        "function_signature_item": "function",
        "struct_item": "struct",
        "enum_item": "enum",
        "trait_item": "trait",
        "impl_item": "impl",
    }
    return kind_map.get(node.type, node.type)


def _visibility_from_node(node) -> str:
    """Check for a ``visibility_modifier`` child (``pub``, ``pub(crate)``, etc.)."""
    for child in node.children:
        if child.type == "visibility_modifier":
            text = child.text.decode("utf-8")
            if "crate" in text:
                return "pub(crate)"
            if "super" in text:
                return "pub(super)"
            return "public"
    return "private"


def _signature(node, source_bytes: bytes) -> str:
    """Extract the signature (everything before the body block)."""
    text = node.text.decode("utf-8")
    # Find the opening brace.
    brace_depth = 0
    for i, ch in enumerate(text):
        if ch == "{":
            return text[:i].rstrip()
        if ch == ";":
            return text[:i].rstrip()
    return text.split("\n", 1)[0]


def _process_node(
    node,
    *,
    source_bytes: bytes,
    path: str,
    repository: str,
    source_name: str,
    imports: list[str],
    module_path: str,
    parent_symbol: str,
    preceding: list,
) -> ParsedUnit | None:
    name = _node_name(node)
    if not name:
        return None

    kind = _symbol_kind(node)
    if parent_symbol and kind == "function":
        kind = "method"

    qualname = f"{module_path}::{parent_symbol}::{name}" if parent_symbol else f"{module_path}::{name}"
    doc = _get_doc_comment(preceding, node.start_point[0])

    text = node.text.decode("utf-8")
    start_line = node.start_point[0] + 1
    end_line = node.end_point[0] + 1

    return ParsedUnit(
        source_kind=SourceKind.CODE,
        language=Language.RUST,
        source_name=source_name,
        repository=repository,
        path=path,
        text=text,
        start_line=start_line,
        end_line=end_line,
        symbol_name=name,
        symbol_kind=kind,
        symbol_qualname=qualname,
        signature=_signature(node, source_bytes),
        parent_symbol=parent_symbol,
        module_path=module_path,
        visibility=_visibility_from_node(node),
        imports=imports,
        docstring=doc,
    )


def _process_impl(
    impl_node,
    *,
    units: list[ParsedUnit],
    source_bytes: bytes,
    path: str,
    repository: str,
    source_name: str,
    imports: list[str],
    module_path: str,
    preceding: list,
) -> None:
    """Process an ``impl`` block: emit the impl itself and each member function."""
    impl_target = _impl_target(impl_node)

    # Emit the impl block itself (without the body, just the header is useful
    # for search; we include the full text for splitting later).
    impl_unit = _process_node(
        impl_node,
        source_bytes=source_bytes,
        path=path,
        repository=repository,
        source_name=source_name,
        imports=imports,
        module_path=module_path,
        parent_symbol="",
        preceding=preceding,
    )
    if impl_unit:
        units.append(impl_unit)

    # Extract member functions from the impl body.
    _extract_members(
        impl_node,
        units=units,
        source_bytes=source_bytes,
        path=path,
        repository=repository,
        source_name=source_name,
        imports=imports,
        module_path=module_path,
        parent_symbol=impl_target,
    )


def _extract_members(
    container_node,
    *,
    units: list[ParsedUnit],
    source_bytes: bytes,
    path: str,
    repository: str,
    source_name: str,
    imports: list[str],
    module_path: str,
    parent_symbol: str,
) -> None:
    """Extract function_item children from a trait or impl block body."""
    body = container_node.child_by_field_name("body")
    if body is None:
        # Try declaration_list for traits.
        for child in container_node.children:
            if child.type == "declaration_list":
                body = child
                break
    if body is None:
        return

    body_children = list(body.children)
    for j, member in enumerate(body_children):
        if member.type in ("function_item", "function_signature_item"):
            unit = _process_node(
                member,
                source_bytes=source_bytes,
                path=path,
                repository=repository,
                source_name=source_name,
                imports=imports,
                module_path=module_path,
                parent_symbol=parent_symbol,
                preceding=body_children[:j],
            )
            if unit:
                units.append(unit)
