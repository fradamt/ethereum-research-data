"""Parsers: frontmatter, markdown, tree-sitter (Python/Go/Rust)."""

from erd_index.parse.frontmatter import extract_frontmatter
from erd_index.parse.markdown_parser import parse_markdown

__all__ = ["extract_frontmatter", "parse_markdown"]
