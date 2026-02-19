"""Map file extensions to language strings."""

from __future__ import annotations

from pathlib import Path

__all__ = ["detect_language"]

_EXTENSION_MAP: dict[str, str] = {
    ".md": "markdown",
    ".py": "python",
    ".go": "go",
    ".rs": "rust",
    ".pdf": "pdf",
}


def detect_language(path: str | Path) -> str | None:
    """Return the language string for *path* based on its extension, or None."""
    suffix = Path(path).suffix.lower()
    return _EXTENSION_MAP.get(suffix)
