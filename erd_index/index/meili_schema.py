"""Meilisearch index settings and schema version.

Defines the searchable, filterable, and sortable attributes matching
SEARCH-ARCHITECTURE.md section 1.3.
"""

from __future__ import annotations

__all__ = ["SCHEMA_VERSION", "get_index_settings"]

# Bump when the index schema changes (fields added/removed/retyped).
# Used by ensure_index() to detect when settings need re-applying.
SCHEMA_VERSION = 2


def get_index_settings() -> dict:
    """Return Meilisearch index settings matching SEARCH-ARCHITECTURE.md 1.3."""
    return {
        "searchableAttributes": [
            "title",
            "symbol_name",
            "symbol_qualname",
            "signature",
            "heading_path",
            "text",
            "summary",
            "tags",
            "category",
            "author",
            "module_path",
            "path",
        ],
        "filterableAttributes": [
            "schema_version",
            "source_kind",
            "chunk_kind",
            "source_name",
            "repository",
            "language",
            "doc_id",
            "node_id",
            "path",
            "topic_id",
            "post_number",
            "author",
            "category",
            "research_thread",
            "tags",
            "mentions_eips",
            "eip",
            "eip_status",
            "eip_type",
            "eip_category",
            "requires_eips",
            "supersedes_eips",
            "replaces_eips",
            "symbol_id",
            "symbol_name",
            "symbol_kind",
            "symbol_qualname",
            "parent_symbol",
            "module_path",
            "visibility",
            "imports",
            "used_imports",
            "content_hash",
            "dedupe_key",
            "text_length",
        ],
        "sortableAttributes": [
            "source_date_ts",
            "indexed_at_ts",
            "influence_score",
            "views",
            "likes",
            "eip",
            "start_line",
        ],
        "distinctAttribute": "dedupe_key",
    }
