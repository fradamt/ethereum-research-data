"""Extract import-to-usage dependency edges from code chunks.

Parses import statements for Python, Go, and Rust, then checks whether
imported names are actually used in the chunk text. Returns typed
(from_symbol, to_symbol, relation) tuples suitable for the graph
``code_dependency_edge`` table.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from erd_index.models import Chunk

__all__ = ["extract_dependencies"]

# ---------------------------------------------------------------------------
# Python imports
# ---------------------------------------------------------------------------

# from foo.bar import baz, qux
_PY_FROM_IMPORT = re.compile(
    r"^\s*from\s+([\w.]+)\s+import\s+(.+)", re.MULTILINE
)
# import foo.bar, baz
_PY_IMPORT = re.compile(
    r"^\s*import\s+(.+)", re.MULTILINE
)


def _parse_python_imports(text: str) -> list[tuple[str, str]]:
    """Return (module_path, imported_name) pairs for Python imports."""
    pairs: list[tuple[str, str]] = []

    # Collapse multi-line parenthesized imports to single lines so the
    # single-line regex can match them.  e.g.:
    #   from foo import (
    #       Bar,  # comment
    #       Baz,
    #   )
    # becomes: from foo import (Bar, Baz,)
    # Strip inline comments per-line BEFORE collapsing to avoid comments
    # from one line bleeding into names from subsequent lines.
    def _collapse_import(m: re.Match) -> str:  # type: ignore[type-arg]
        prefix = m.group(1)
        body = m.group(2)
        # Strip inline comments from each line before joining
        lines = [line.split("#")[0].rstrip() for line in body.split("\n")]
        return prefix + "(" + " ".join(lines) + ")"

    text = re.sub(
        r"(from\s+[\w.]+\s+import\s*)\(\s*\n(.*?)\)",
        _collapse_import,
        text,
        flags=re.DOTALL,
    )

    for m in _PY_FROM_IMPORT.finditer(text):
        module = m.group(1)
        names_part = m.group(2)
        # Handle parenthesized imports on single line
        names_part = names_part.strip().strip("()")
        for name in names_part.split(","):
            # Strip inline comments per-name (important for collapsed
            # multi-line imports like "bar, # comment baz,")
            name = name.split("#")[0].strip()
            if not name:
                continue
            # Handle "as" aliases: "bar as b" -> imported_name is "b"
            if " as " in name:
                _orig, alias = name.split(" as ", 1)
                pairs.append((f"{module}.{_orig.strip()}", alias.strip()))
            else:
                pairs.append((f"{module}.{name}", name))

    for m in _PY_IMPORT.finditer(text):
        names_part = m.group(1).split("#")[0]
        for name in names_part.split(","):
            name = name.strip()
            if not name or name.startswith("from"):
                continue
            if " as " in name:
                full, alias = name.split(" as ", 1)
                pairs.append((full.strip(), alias.strip()))
            else:
                # "import foo.bar" -> local name is "foo"
                local = name.split(".")[0]
                pairs.append((name, local))

    return pairs


# ---------------------------------------------------------------------------
# Go imports
# ---------------------------------------------------------------------------

# Matches individual import specs inside import(...) or standalone import "..."
_GO_IMPORT = re.compile(
    r'(?:(\w+)\s+)?"([^"]+)"'
)


def _parse_go_imports(text: str) -> list[tuple[str, str]]:
    """Return (import_path, local_name) pairs for Go imports."""
    pairs: list[tuple[str, str]] = []
    for m in _GO_IMPORT.finditer(text):
        alias = m.group(1)
        path = m.group(2)
        # Local name is the alias if given, otherwise last path segment
        local = alias if alias else path.rsplit("/", 1)[-1]
        if local == "_" or local == ".":
            continue
        pairs.append((path, local))
    return pairs


# ---------------------------------------------------------------------------
# Rust imports
# ---------------------------------------------------------------------------

# use foo::bar::Baz;  or  use foo::bar::{Baz, Qux};
_RUST_USE = re.compile(
    r"^\s*use\s+([\w:]+)(?:::\{([^}]+)\})?\s*;", re.MULTILINE
)


def _parse_rust_imports(text: str) -> list[tuple[str, str]]:
    """Return (full_path, local_name) pairs for Rust use declarations."""
    pairs: list[tuple[str, str]] = []
    for m in _RUST_USE.finditer(text):
        base = m.group(1)
        braced = m.group(2)
        if braced:
            for item in braced.split(","):
                item = item.strip()
                if not item:
                    continue
                if " as " in item:
                    orig, alias = item.split(" as ", 1)
                    pairs.append((f"{base}::{orig.strip()}", alias.strip()))
                else:
                    pairs.append((f"{base}::{item}", item.rsplit("::", 1)[-1]))
        else:
            # use foo::bar::Baz -> local name is "Baz"
            local = base.rsplit("::", 1)[-1]
            pairs.append((base, local))
    return pairs


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_dependencies(chunk: Chunk) -> list[tuple[str, str, str]]:
    """Extract dependency edges from a code chunk.

    Returns a list of ``(from_symbol, to_symbol, relation)`` tuples where:
    - *from_symbol* is the chunk's qualified name (or path:symbol_name fallback)
    - *to_symbol* is the full import path of the used dependency
    - *relation* is one of ``"imports"``, ``"calls"``, ``"uses_type"``

    Only imports that are actually referenced in the chunk body are returned.
    """
    lang = chunk.language.value if hasattr(chunk.language, "value") else str(chunk.language)

    # Use the chunk's imports list for parsing.  For Go, falling back to
    # chunk.text is unsafe because the Go import regex matches any double-
    # quoted string (including string literals in function bodies).
    if chunk.imports:
        import_text = "\n".join(chunk.imports)
    elif lang == "go":
        # Go: don't fall back to chunk.text — string literals create false
        # matches.  Return no deps if imports weren't captured.
        return []
    else:
        import_text = chunk.text

    if lang == "python":
        import_pairs = _parse_python_imports(import_text)
    elif lang == "go":
        import_pairs = _parse_go_imports(import_text)
    elif lang == "rust":
        import_pairs = _parse_rust_imports(import_text)
    else:
        return []

    from_sym = chunk.symbol_qualname or f"{chunk.path}:{chunk.symbol_name or 'module'}"

    edges: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    body = chunk.text

    for full_path, local_name in import_pairs:
        if not local_name or not re.search(rf"\b{re.escape(local_name)}\b", body):
            continue
        edge_key = (from_sym, full_path)
        if edge_key in seen:
            continue
        seen.add(edge_key)

        # Heuristic: if local_name is Title-cased, likely a type; otherwise an import
        relation = "uses_type" if local_name[0].isupper() else "imports"
        edges.append((from_sym, full_path, relation))

    return edges
