"""Extract YAML frontmatter from markdown files."""

from __future__ import annotations

import logging
from typing import Any

import yaml

__all__ = ["extract_frontmatter"]

log = logging.getLogger(__name__)


def extract_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter delimited by ``---`` from *text*.

    Returns (frontmatter_dict, body) where *body* is the remaining text after
    the closing ``---``.  If no frontmatter is present, returns ({}, text).
    Malformed YAML logs a warning and returns ({}, body).
    """
    if not text.startswith("---"):
        return {}, text

    # Find the closing delimiter (must be on its own line).
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    yaml_block = text[3:end].strip()
    body = text[end + 4:]  # skip past the closing "---\n"
    if body.startswith("\n"):
        body = body[1:]

    try:
        fm = yaml.safe_load(yaml_block)
    except yaml.YAMLError as exc:
        log.warning("Malformed YAML frontmatter: %s", exc)
        return {}, body

    if not isinstance(fm, dict):
        return {}, body

    return fm, body
