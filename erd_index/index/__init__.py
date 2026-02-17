"""Meilisearch integration: client, schema, document builder, batch writer."""

from erd_index.index.document_builder import chunk_to_document, chunks_to_documents
from erd_index.index.meili_client import ensure_index, get_client, init_index
from erd_index.index.meili_schema import SCHEMA_VERSION, get_index_settings
from erd_index.index.writer import batch_upsert, delete_by_filter, delete_by_ids, get_index_stats

__all__ = [
    "SCHEMA_VERSION",
    "batch_upsert",
    "chunk_to_document",
    "chunks_to_documents",
    "delete_by_filter",
    "delete_by_ids",
    "ensure_index",
    "get_client",
    "get_index_settings",
    "get_index_stats",
    "init_index",
]
