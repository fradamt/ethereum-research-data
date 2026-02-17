"""Parse Python source files using tree-sitter and extract code units."""

from __future__ import annotations

import logging

from erd_index.models import Language, ParsedUnit, SourceKind
from erd_index.parse.treesitter_runtime import parse_source

__all__ = ["parse_python_file"]

log = logging.getLogger(__name__)

# Node types we extract as top-level units.
_UNIT_TYPES = {"function_definition", "decorated_definition", "class_definition"}
_IMPORT_TYPES = {"import_statement", "import_from_statement"}


def parse_python_file(
    source: str,
    *,
    path: str,
    repository: str = "",
    source_name: str = "",
) -> list[ParsedUnit]:
    """Parse a Python file and return a list of ``ParsedUnit`` objects.

    Extracts functions, decorated definitions, classes, and file-level imports.
    """
    tree = parse_source(source, "python")
    root = tree.root_node
    source_bytes = source.encode("utf-8")

    # Collect file-level imports.
    imports = _extract_imports(root, source_bytes)

    # Derive module path from file path (foo/bar/baz.py -> foo.bar.baz).
    module_path = _path_to_module(path)

    units: list[ParsedUnit] = []

    for child in root.children:
        if child.type in _UNIT_TYPES:
            unit = _process_node(
                child,
                source_bytes=source_bytes,
                path=path,
                repository=repository,
                source_name=source_name,
                imports=imports,
                module_path=module_path,
                parent_symbol="",
            )
            if unit:
                units.append(unit)

            # If it's a class, also extract its methods.
            cls_node = child
            if child.type == "decorated_definition":
                cls_node = _unwrap_decorated(child)
            if cls_node is not None and cls_node.type == "class_definition":
                class_name = _node_name(cls_node)
                body = cls_node.child_by_field_name("body")
                if body:
                    for member in body.children:
                        if member.type in _UNIT_TYPES:
                            mu = _process_node(
                                member,
                                source_bytes=source_bytes,
                                path=path,
                                repository=repository,
                                source_name=source_name,
                                imports=imports,
                                module_path=module_path,
                                parent_symbol=class_name,
                            )
                            if mu:
                                units.append(mu)

    return units


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_imports(root, source_bytes: bytes) -> list[str]:
    imports: list[str] = []
    for child in root.children:
        if child.type in _IMPORT_TYPES:
            imports.append(child.text.decode("utf-8"))
    return imports


def _path_to_module(path: str) -> str:
    """Convert ``foo/bar/baz.py`` to ``foo.bar.baz``."""
    mod = path.replace("/", ".").replace("\\", ".")
    for suffix in (".py", ".__init__"):
        if mod.endswith(suffix):
            mod = mod[: -len(suffix)]
    return mod


def _unwrap_decorated(node):
    """Given a ``decorated_definition``, return the inner definition node."""
    for child in node.children:
        if child.type in ("function_definition", "class_definition"):
            return child
    return None


def _node_name(node) -> str:
    """Extract the ``name`` field from a definition node."""
    name_node = node.child_by_field_name("name")
    if name_node:
        return name_node.text.decode("utf-8")
    return ""


def _extract_signature(node, source_bytes: bytes) -> str:
    """Build a signature string for a function or class definition.

    For decorated definitions, includes the decorator lines.
    """
    lines: list[str] = []

    # Decorators (if the node is a decorated_definition).
    if node.type == "decorated_definition":
        for child in node.children:
            if child.type == "decorator":
                lines.append(child.text.decode("utf-8"))
        inner = _unwrap_decorated(node)
        if inner is None:
            return node.text.decode("utf-8").split("\n", 1)[0]
        node = inner

    # First line of the definition (e.g. ``def foo(a, b) -> int:``).
    text = node.text.decode("utf-8")
    first_line = text.split("\n", 1)[0]
    lines.append(first_line)
    return "\n".join(lines)


def _extract_docstring(node) -> str:
    """Extract the docstring from a function/class body (first expression_statement
    containing a string node)."""
    inner = node
    if node.type == "decorated_definition":
        inner = _unwrap_decorated(node) or node

    body = inner.child_by_field_name("body")
    if body is None:
        return ""
    for child in body.children:
        if child.type == "expression_statement":
            for sub in child.children:
                if sub.type == "string":
                    raw = sub.text.decode("utf-8")
                    # Strip triple-quote delimiters.
                    for delim in ('"""', "'''"):
                        if raw.startswith(delim) and raw.endswith(delim):
                            return raw[3:-3].strip()
                    return raw.strip("\"'").strip()
            break  # Only check the first statement.
        # Skip comments/pass but stop at anything non-trivial.
        if child.type not in ("comment", "pass_statement"):
            break
    return ""


def _symbol_kind(node) -> str:
    inner = node
    if node.type == "decorated_definition":
        inner = _unwrap_decorated(node) or node
    if inner.type == "class_definition":
        return "class"
    if inner.type == "function_definition":
        return "function"
    return inner.type


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
) -> ParsedUnit | None:
    inner = node
    if node.type == "decorated_definition":
        inner = _unwrap_decorated(node) or node

    name = _node_name(inner)
    if not name:
        return None

    kind = _symbol_kind(node)
    qualname = f"{module_path}.{parent_symbol}.{name}" if parent_symbol else f"{module_path}.{name}"

    text = node.text.decode("utf-8")
    start_line = node.start_point[0] + 1  # 1-based
    end_line = node.end_point[0] + 1

    return ParsedUnit(
        source_kind=SourceKind.CODE,
        language=Language.PYTHON,
        source_name=source_name,
        repository=repository,
        path=path,
        text=text,
        start_line=start_line,
        end_line=end_line,
        symbol_name=name,
        symbol_kind="method" if parent_symbol and kind == "function" else kind,
        symbol_qualname=qualname,
        signature=_extract_signature(node, source_bytes),
        parent_symbol=parent_symbol,
        module_path=module_path,
        imports=imports,
        docstring=_extract_docstring(node),
    )
