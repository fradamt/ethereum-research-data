"""Compute derived code metadata for code chunks.

Enriches symbol_qualname, used_imports, calls, and visibility based on
language conventions.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from erd_index.models import Chunk

__all__ = ["enrich_code_chunk"]

# Matches a function/method call: identifier (possibly dotted) followed by `(`.
# Excludes common control-flow keywords.
_CALL_RE = re.compile(r"\b([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*\(")
_CONTROL_KEYWORDS = frozenset({
    "if", "else", "elif", "for", "while", "with", "return", "raise", "yield",
    "assert", "del", "print", "except", "finally", "try", "catch", "switch",
    "case", "match", "range", "len", "type", "isinstance", "issubclass",
    "super", "self", "cls",
    # Go
    "func", "go", "defer", "select", "make", "new", "append", "cap",
    "copy", "delete", "close", "panic", "recover",
    # Rust
    "fn", "let", "mut", "loop", "unsafe", "async", "await", "move",
    "impl", "trait", "where", "macro_rules",
})


def _build_qualname(chunk: Chunk) -> str:
    """Build a qualified name: module_path.ParentSymbol.symbol_name."""
    parts: list[str] = []
    if chunk.module_path:
        parts.append(chunk.module_path)
    if chunk.parent_symbol:
        parts.append(chunk.parent_symbol)
    if chunk.symbol_name:
        parts.append(chunk.symbol_name)
    return ".".join(parts) if parts else ""


def _filter_used_imports(imports: list[str], text: str) -> list[str]:
    """Return imports whose imported name appears in *text*."""
    used: list[str] = []
    for imp in imports:
        # Extract the final imported name: "from foo import bar" -> "bar",
        # "import foo.bar" -> "bar", or just the import string itself.
        name = imp.rsplit(".", 1)[-1].rsplit(" ", 1)[-1].strip()
        if not name:
            continue
        # Check for word-boundary usage in text
        if re.search(rf"\b{re.escape(name)}\b", text):
            used.append(imp)
    return used


def _extract_calls(text: str) -> list[str]:
    """Heuristically extract called function names from code text."""
    seen: set[str] = set()
    calls: list[str] = []
    for m in _CALL_RE.finditer(text):
        name = m.group(1)
        # Take the last segment for dedup check but keep full dotted name
        base = name.rsplit(".", 1)[-1]
        if base in _CONTROL_KEYWORDS:
            continue
        if name not in seen:
            seen.add(name)
            calls.append(name)
    return sorted(calls)


def _infer_visibility(chunk: Chunk) -> str:
    """Infer visibility from language conventions."""
    lang = chunk.language.value if hasattr(chunk.language, "value") else str(chunk.language)
    name = chunk.symbol_name

    if lang == "python":
        if name.startswith("__") and name.endswith("__"):
            return "public"  # dunder magic methods (__init__, __str__, etc.)
        if name.startswith("_"):
            return "private"
        return "public"

    if lang == "go":
        if name and name[0].isupper():
            return "public"
        return "private"

    if lang == "rust":
        # Check for `pub` keyword in the signature line
        sig = chunk.signature
        if sig and re.match(r"\s*pub\b", sig):
            return "public"
        return "private"

    return ""


def enrich_code_chunk(chunk: Chunk) -> Chunk:
    """Populate derived code metadata fields on *chunk*.

    Mutates and returns *chunk* for chaining convenience.
    """
    # Build qualified name if not already set
    if not chunk.symbol_qualname:
        chunk.symbol_qualname = _build_qualname(chunk)

    # Filter imports to those actually used in this chunk
    if chunk.imports and not chunk.used_imports:
        chunk.used_imports = _filter_used_imports(chunk.imports, chunk.text)

    # Extract function calls
    if not chunk.calls:
        chunk.calls = _extract_calls(chunk.text)

    # Infer visibility
    if not chunk.visibility and chunk.symbol_name:
        chunk.visibility = _infer_visibility(chunk)

    return chunk
