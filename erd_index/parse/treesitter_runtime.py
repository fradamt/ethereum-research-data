"""Shared tree-sitter initialization and parsing utilities."""

from __future__ import annotations

import logging
from functools import lru_cache

from tree_sitter import Language, Parser, Tree

__all__ = ["get_language", "parse_source"]

log = logging.getLogger(__name__)


@lru_cache(maxsize=8)
def get_language(lang: str) -> Language:
    """Return a cached ``tree_sitter.Language`` for *lang*.

    Supported values: ``"python"``, ``"go"``, ``"rust"``.
    """
    if lang == "python":
        import tree_sitter_python as tsp

        return Language(tsp.language())
    if lang == "go":
        import tree_sitter_go as tsg

        return Language(tsg.language())
    if lang == "rust":
        import tree_sitter_rust as tsr

        return Language(tsr.language())
    raise ValueError(f"Unsupported language: {lang!r}")


def parse_source(source: str | bytes, lang: str) -> Tree:
    """Parse *source* with the tree-sitter grammar for *lang*.

    Returns a ``tree_sitter.Tree`` whose ``root_node`` you can walk.
    """
    language = get_language(lang)
    parser = Parser(language)
    if isinstance(source, str):
        source = source.encode("utf-8")
    return parser.parse(source)
