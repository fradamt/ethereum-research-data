"""Parse Go source files using tree-sitter and extract code units."""

from __future__ import annotations

import logging

from erd_index.models import Language, ParsedUnit, SourceKind
from erd_index.parse.treesitter_runtime import parse_source

__all__ = ["parse_go_file"]

log = logging.getLogger(__name__)

_FUNC_TYPES = {"function_declaration", "method_declaration"}


def parse_go_file(
    source: str,
    *,
    path: str,
    repository: str = "",
    source_name: str = "",
) -> list[ParsedUnit]:
    """Parse a Go file and return a list of ``ParsedUnit`` objects.

    Extracts functions, methods, struct type declarations, package clause,
    imports, and doc comments.
    """
    tree = parse_source(source, "go")
    root = tree.root_node
    source_bytes = source.encode("utf-8")

    pkg_name = _extract_package(root)
    imports = _extract_imports(root, source_bytes)

    units: list[ParsedUnit] = []

    children = list(root.children)
    for i, child in enumerate(children):
        if child.type in _FUNC_TYPES:
            unit = _process_func(
                child,
                source_bytes=source_bytes,
                path=path,
                repository=repository,
                source_name=source_name,
                imports=imports,
                pkg_name=pkg_name,
                preceding=children[:i],
            )
            if unit:
                units.append(unit)

        elif child.type == "type_declaration":
            for spec in child.children:
                if spec.type == "type_spec":
                    unit = _process_type_spec(
                        spec,
                        decl_node=child,
                        source_bytes=source_bytes,
                        path=path,
                        repository=repository,
                        source_name=source_name,
                        imports=imports,
                        pkg_name=pkg_name,
                        preceding=children[:i],
                    )
                    if unit:
                        units.append(unit)

    return units


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_package(root) -> str:
    for child in root.children:
        if child.type == "package_clause":
            for sub in child.children:
                if sub.type == "package_identifier":
                    return sub.text.decode("utf-8")
    return ""


def _extract_imports(root, source_bytes: bytes) -> list[str]:
    imports: list[str] = []
    for child in root.children:
        if child.type == "import_declaration":
            imports.append(child.text.decode("utf-8"))
    return imports


def _get_doc_comment(preceding: list, target_start_row: int, source_bytes: bytes) -> str:
    """Collect contiguous ``//`` comment lines immediately before *target_start_row*."""
    comment_lines: list[str] = []
    # Walk backwards from the end of preceding siblings.
    for node in reversed(preceding):
        if node.type == "comment" and node.end_point[0] >= target_start_row - 1 - len(comment_lines):
            text = node.text.decode("utf-8")
            if text.startswith("//"):
                comment_lines.insert(0, text.lstrip("/ ").strip())
            else:
                break
        else:
            break
    return "\n".join(comment_lines)


def _func_signature(node, source_bytes: bytes) -> str:
    """Extract the first line (signature) of a function/method declaration."""
    text = node.text.decode("utf-8")
    # Take up to the opening brace.
    for i, ch in enumerate(text):
        if ch == "{":
            return text[:i].rstrip()
    return text.split("\n", 1)[0]


def _receiver_type(node) -> str:
    """For a method_declaration, extract the receiver type name."""
    params = node.child_by_field_name("receiver")
    if params is None:
        return ""
    # Walk into parameter_list -> parameter_declaration -> type
    for child in params.children:
        if child.type == "parameter_declaration":
            type_node = child.child_by_field_name("type")
            if type_node:
                # Handle pointer receivers: *Type
                text = type_node.text.decode("utf-8")
                return text.lstrip("*")
    return ""


def _node_name(node) -> str:
    name_node = node.child_by_field_name("name")
    if name_node:
        return name_node.text.decode("utf-8")
    return ""


def _visibility(name: str) -> str:
    if name and name[0].isupper():
        return "public"
    return "private"


def _process_func(
    node,
    *,
    source_bytes: bytes,
    path: str,
    repository: str,
    source_name: str,
    imports: list[str],
    pkg_name: str,
    preceding: list,
) -> ParsedUnit | None:
    name = _node_name(node)
    if not name:
        return None

    receiver = _receiver_type(node) if node.type == "method_declaration" else ""
    kind = "method" if receiver else "function"
    qualname = f"{pkg_name}.{receiver}.{name}" if receiver else f"{pkg_name}.{name}"
    doc = _get_doc_comment(preceding, node.start_point[0], source_bytes)

    text = node.text.decode("utf-8")
    start_line = node.start_point[0] + 1
    end_line = node.end_point[0] + 1

    return ParsedUnit(
        source_kind=SourceKind.CODE,
        language=Language.GO,
        source_name=source_name,
        repository=repository,
        path=path,
        text=text,
        start_line=start_line,
        end_line=end_line,
        symbol_name=name,
        symbol_kind=kind,
        symbol_qualname=qualname,
        signature=_func_signature(node, source_bytes),
        parent_symbol=receiver,
        module_path=pkg_name,
        visibility=_visibility(name),
        imports=imports,
        docstring=doc,
    )


def _process_type_spec(
    spec_node,
    *,
    decl_node,
    source_bytes: bytes,
    path: str,
    repository: str,
    source_name: str,
    imports: list[str],
    pkg_name: str,
    preceding: list,
) -> ParsedUnit | None:
    name = _node_name(spec_node)
    if not name:
        return None

    # Determine if this is a struct, interface, or other type.
    type_node = spec_node.child_by_field_name("type")
    kind = "struct"
    if type_node:
        if type_node.type == "interface_type":
            kind = "interface"
        elif type_node.type != "struct_type":
            kind = "type_alias"

    qualname = f"{pkg_name}.{name}"
    doc = _get_doc_comment(preceding, decl_node.start_point[0], source_bytes)

    # Use the full type_declaration text (includes ``type Name struct { ... }``).
    text = decl_node.text.decode("utf-8")
    start_line = decl_node.start_point[0] + 1
    end_line = decl_node.end_point[0] + 1

    # Signature: first line of the type declaration.
    sig = text.split("\n", 1)[0]

    return ParsedUnit(
        source_kind=SourceKind.CODE,
        language=Language.GO,
        source_name=source_name,
        repository=repository,
        path=path,
        text=text,
        start_line=start_line,
        end_line=end_line,
        symbol_name=name,
        symbol_kind=kind,
        symbol_qualname=qualname,
        signature=sig,
        parent_symbol="",
        module_path=pkg_name,
        visibility=_visibility(name),
        imports=imports,
        docstring=doc,
    )
