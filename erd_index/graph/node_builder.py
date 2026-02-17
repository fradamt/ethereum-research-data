"""Build graph node dicts from Chunk objects.

Maps each Chunk to a dict suitable for ``store.upsert_node()``.
The node_id comes from ``Chunk.node_id`` (a computed field).
"""

from __future__ import annotations

import json
from typing import Any

from erd_index.models import Chunk, ChunkKind, SourceKind

__all__ = ["chunk_to_node"]

# Mapping from (source_kind, chunk_kind) to node_type.
# Forum posts need further refinement based on post_number.
_CODE_KIND_MAP: dict[str, str] = {
    "function": "code_function",
    "method": "code_function",
    "struct": "code_struct",
    "enum": "code_enum",
    "trait": "code_trait",
    "impl": "code_impl",
    "class": "code_class",
}


def _resolve_node_type(chunk: Chunk) -> str:
    """Determine the graph node_type from chunk fields."""
    if chunk.source_kind == SourceKind.FORUM:
        # post_number 0 or 1 means it's the topic opener; >1 is a reply post
        if chunk.post_number is not None and chunk.post_number > 1:
            return "forum_post"
        return "forum_topic"

    if chunk.source_kind == SourceKind.EIP:
        if chunk.chunk_kind == ChunkKind.EIP_SECTION:
            # Top-level EIP node has no heading_path or the heading_path is the title
            if not chunk.heading_path:
                return "eip"
            return "eip_section"
        return "eip"

    # Code chunks
    if chunk.chunk_kind in (ChunkKind.CODE_FUNCTION, ChunkKind.CODE_GROUP):
        return _CODE_KIND_MAP.get(chunk.symbol_kind, "code_function")

    if chunk.chunk_kind == ChunkKind.CODE_STRUCT:
        return _CODE_KIND_MAP.get(chunk.symbol_kind, "code_struct")

    # Fallback for anything else
    return "code_function"


def _build_section_anchor(chunk: Chunk) -> str | None:
    """Build a section anchor from heading_path (last heading, kebab-cased)."""
    if not chunk.heading_path:
        return None
    return chunk.heading_path[-1].lower().replace(" ", "-")


def _build_metadata(chunk: Chunk) -> str:
    """Build JSON metadata for extra fields not in the node schema."""
    meta: dict[str, Any] = {}
    if chunk.tags:
        meta["tags"] = chunk.tags
    if chunk.category:
        meta["category"] = chunk.category
    if chunk.author:
        meta["author"] = chunk.author
    if chunk.research_thread:
        meta["research_thread"] = chunk.research_thread
    if chunk.influence_score:
        meta["influence_score"] = chunk.influence_score
    if chunk.signature:
        meta["signature"] = chunk.signature
    if chunk.parent_symbol:
        meta["parent_symbol"] = chunk.parent_symbol
    if chunk.module_path:
        meta["module_path"] = chunk.module_path
    if chunk.visibility:
        meta["visibility"] = chunk.visibility
    if chunk.member_symbols:
        meta["member_symbols"] = chunk.member_symbols
    return json.dumps(meta) if meta else "{}"


def chunk_to_node(chunk: Chunk) -> dict[str, Any]:
    """Convert a Chunk to a node dict for ``store.upsert_node()``.

    Returns a dict with all fields expected by the ``node`` table.
    """
    return {
        "node_id": chunk.node_id,
        "node_type": _resolve_node_type(chunk),
        "source_name": chunk.source_name,
        "repository": chunk.repository or None,
        "language": chunk.language.value,
        "file_path": chunk.path,
        "chunk_id": chunk.chunk_id,
        "title": chunk.title or None,
        "url": chunk.url or None,
        "eip": chunk.eip,
        "section_anchor": _build_section_anchor(chunk),
        "symbol_name": chunk.symbol_name or None,
        "symbol_kind": chunk.symbol_kind or None,
        "start_line": chunk.start_line,
        "end_line": chunk.end_line,
        "content_hash": chunk.content_hash,
        "metadata_json": _build_metadata(chunk),
    }
