"""Convert Chunk objects into Meilisearch document dicts."""

from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from erd_index.models import Chunk

__all__ = ["chunk_to_document", "chunks_to_documents", "sanitize_chunk_id", "sanitize_text"]

# Matches C0 control characters except tab (0x09), newline (0x0A), and
# carriage return (0x0D).  These cause Meilisearch's JSON parser to reject
# the entire payload with "control character (\u0000-\u001F) found".
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def sanitize_text(text: str) -> str:
    """Strip C0 control characters that Meilisearch rejects.

    Preserves tab, newline, and carriage return (the useful whitespace
    characters).  All other U+0000-U+001F characters are removed.
    """
    return _CONTROL_CHARS_RE.sub("", text)


def sanitize_chunk_id(chunk_id: str) -> str:
    """Sanitize a chunk_id for use as a Meilisearch document ID.

    Meilisearch IDs allow only alphanumeric characters, hyphens, and
    underscores.
    """
    return chunk_id.replace(":", "-").replace("/", "_").replace(".", "_")


def chunk_to_document(chunk: Chunk, schema_version: int) -> dict:
    """Convert a single Chunk into a Meilisearch document dict.

    The document ``id`` is the chunk's ``chunk_id``.  None/empty fields are
    omitted so Meilisearch stores a compact document.
    """
    safe_id = sanitize_chunk_id(chunk.chunk_id)
    doc: dict = {
        "id": safe_id,
        "doc_id": chunk.doc_id,
        "node_id": chunk.node_id,
        "schema_version": schema_version,
        "source_kind": chunk.source_kind.value,
        "chunk_kind": chunk.chunk_kind.value,
        "language": chunk.language.value,
        "text": sanitize_text(chunk.text),
        "start_line": chunk.start_line,
        "end_line": chunk.end_line,
        "content_hash": chunk.content_hash,
        "dedupe_key": chunk.dedupe_key,
        "indexed_at_ts": int(time.time()),
    }

    # --- Optional core fields (omit if empty/falsy) -----------------------
    _set_if(doc, "source_name", chunk.source_name)
    _set_if(doc, "repository", chunk.repository)
    _set_if(doc, "path", chunk.path)
    _set_if(doc, "url", chunk.url)
    _set_if(doc, "title", chunk.title)
    _set_if(doc, "summary", chunk.summary)
    _set_if(doc, "source_date", chunk.source_date)
    if chunk.source_date_ts:
        doc["source_date_ts"] = chunk.source_date_ts

    # Lists — omit if empty
    _set_if_list(doc, "heading_path", chunk.heading_path)
    _set_if_list(doc, "tags", chunk.tags)
    _set_if_list(doc, "mentions_eips", chunk.mentions_eips)

    # --- Forum fields ------------------------------------------------------
    if chunk.topic_id is not None:
        doc["topic_id"] = chunk.topic_id
    if chunk.post_number is not None:
        doc["post_number"] = chunk.post_number
    _set_if(doc, "author", chunk.author)
    _set_if(doc, "category", chunk.category)
    _set_if(doc, "research_thread", chunk.research_thread)
    if chunk.views:
        doc["views"] = chunk.views
    if chunk.likes:
        doc["likes"] = chunk.likes
    if chunk.posts_count:
        doc["posts_count"] = chunk.posts_count
    if chunk.influence_score:
        doc["influence_score"] = chunk.influence_score

    # --- EIP fields --------------------------------------------------------
    if chunk.eip is not None:
        doc["eip"] = chunk.eip
    _set_if(doc, "eip_status", chunk.eip_status)
    _set_if(doc, "eip_type", chunk.eip_type)
    _set_if(doc, "eip_category", chunk.eip_category)
    _set_if_list(doc, "requires_eips", chunk.requires_eips)
    _set_if_list(doc, "supersedes_eips", chunk.supersedes_eips)
    _set_if_list(doc, "replaces_eips", chunk.replaces_eips)

    # --- Code fields -------------------------------------------------------
    _set_if(doc, "symbol_name", chunk.symbol_name)
    _set_if(doc, "symbol_kind", chunk.symbol_kind)
    _set_if(doc, "symbol_qualname", chunk.symbol_qualname)
    _set_if(doc, "signature", chunk.signature)
    _set_if(doc, "parent_symbol", chunk.parent_symbol)
    _set_if(doc, "module_path", chunk.module_path)
    _set_if(doc, "visibility", chunk.visibility)
    _set_if_list(doc, "imports", chunk.imports)
    _set_if_list(doc, "used_imports", chunk.used_imports)
    _set_if_list(doc, "calls", chunk.calls)
    _set_if_list(doc, "member_symbols", chunk.member_symbols)

    # symbol_id: used as a filterable field in the schema — derived from
    # node_id for code chunks that have a symbol_name.
    if chunk.symbol_name:
        doc["symbol_id"] = chunk.node_id

    # --- Split metadata ----------------------------------------------------
    if chunk.part_index is not None:
        doc["part_index"] = chunk.part_index
    if chunk.part_count is not None:
        doc["part_count"] = chunk.part_count

    return doc


def chunks_to_documents(chunks: list[Chunk], schema_version: int) -> list[dict]:
    """Convert a list of Chunks into Meilisearch document dicts."""
    return [chunk_to_document(c, schema_version) for c in chunks]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _set_if(doc: dict, key: str, value: str) -> None:
    """Set *key* in *doc* only if *value* is non-empty."""
    if value:
        doc[key] = value


def _set_if_list(doc: dict, key: str, value: list) -> None:
    """Set *key* in *doc* only if *value* is non-empty."""
    if value:
        doc[key] = value
