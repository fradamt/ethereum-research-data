"""File discovery and language detection."""

from erd_index.discover.file_walker import DiscoveredFile, walk_sources
from erd_index.discover.language_detector import detect_language

__all__ = ["DiscoveredFile", "detect_language", "walk_sources"]
