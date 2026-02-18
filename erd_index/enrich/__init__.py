"""Enrichment: EIP refs, forum metadata, code metadata, dependency extraction, spec-code linking."""

from __future__ import annotations

from erd_index.enrich.code_metadata import enrich_code_chunk
from erd_index.enrich.dependency_extractor import extract_dependencies
from erd_index.enrich.eip_refs import extract_eip_refs
from erd_index.enrich.forum_metadata import enrich_forum_chunk
from erd_index.enrich.spec_code_linker import find_spec_code_links

__all__ = [
    "enrich_code_chunk",
    "enrich_forum_chunk",
    "extract_dependencies",
    "extract_eip_refs",
    "find_spec_code_links",
]
