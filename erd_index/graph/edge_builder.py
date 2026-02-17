"""Build graph edges from Chunk objects.

Produces edge dicts for the three edge types that can be derived from a single
chunk's metadata:

- **EIP dependency edges** — from ``requires_eips``, ``supersedes_eips``,
  ``replaces_eips`` frontmatter fields.
- **Cross-reference edges** — from ``mentions_eips`` (regex-extracted EIP
  references in the chunk text).
- **Code dependency edges** — from the dependency extractor output (list of
  ``(from_node_id, to_symbol, relation)`` tuples).

Spec-code links are built separately during the linking phase and are not
handled here.
"""

from __future__ import annotations

from typing import Any

from erd_index.models import Chunk

__all__ = ["build_edges_from_chunk"]


def _build_eip_deps(chunk: Chunk) -> list[dict[str, Any]]:
    """Build EIP dependency edge dicts from frontmatter fields."""
    if chunk.eip is None:
        return []

    edges: list[dict[str, Any]] = []

    for to_eip in chunk.requires_eips:
        edges.append({
            "from_eip": chunk.eip,
            "to_eip": to_eip,
            "relation": "requires",
            "source_node_id": chunk.node_id,
            "confidence": 1.0,
            "evidence_text": None,
            "extractor": "frontmatter",
        })

    for to_eip in chunk.supersedes_eips:
        edges.append({
            "from_eip": chunk.eip,
            "to_eip": to_eip,
            "relation": "supersedes",
            "source_node_id": chunk.node_id,
            "confidence": 1.0,
            "evidence_text": None,
            "extractor": "frontmatter",
        })

    for to_eip in chunk.replaces_eips:
        edges.append({
            "from_eip": chunk.eip,
            "to_eip": to_eip,
            "relation": "replaces",
            "source_node_id": chunk.node_id,
            "confidence": 1.0,
            "evidence_text": None,
            "extractor": "frontmatter",
        })

    return edges


def _build_cross_refs(chunk: Chunk) -> list[dict[str, Any]]:
    """Build cross-reference edges from mentions_eips.

    Each mentioned EIP gets a ``mentions_eip`` edge from this chunk's node
    to the canonical EIP node (``eip:<number>``).
    """
    edges: list[dict[str, Any]] = []

    for eip_num in chunk.mentions_eips:
        # Skip self-references for EIP chunks
        if chunk.eip is not None and eip_num == chunk.eip:
            continue

        edges.append({
            "from_node_id": chunk.node_id,
            "to_node_id": f"eip:{eip_num}",
            "relation": "mentions_eip",
            "span_start": None,
            "span_end": None,
            "anchor_text": f"EIP-{eip_num}",
            "confidence": 1.0,
            "extractor": "eip_refs",
        })

    return edges


def _build_code_deps(
    chunk: Chunk,
    dependencies: list[tuple[str, str, str]],
) -> list[dict[str, Any]]:
    """Build code dependency edges from dependency extractor output.

    Each dependency is a tuple of ``(from_node_id, to_symbol, relation)`` where:
    - ``from_node_id`` matches the chunk's node_id
    - ``to_symbol`` is a qualified symbol name that may or may not resolve to a
      known node_id.  If it contains ``:`` it's treated as a resolved node_id;
      otherwise it's stored as ``to_external_symbol``.
    - ``relation`` is one of: ``calls``, ``uses_type``, ``imports``,
      ``implements_trait``
    """
    edges: list[dict[str, Any]] = []

    for from_nid, to_symbol, relation in dependencies:
        # Heuristic: a resolved node_id uses single colons (e.g., "go-ethereum:core/vm:Run").
        # Rust paths use "::" (e.g., "std::collections::HashMap") — those are external.
        is_resolved = ":" in to_symbol and "::" not in to_symbol
        if is_resolved:
            edges.append({
                "from_code_node_id": from_nid,
                "to_code_node_id": to_symbol,
                "to_external_symbol": None,
                "relation": relation,
                "confidence": 0.7,
                "extractor": "tree_sitter",
                "evidence_text": None,
            })
        else:
            edges.append({
                "from_code_node_id": from_nid,
                "to_code_node_id": None,
                "to_external_symbol": to_symbol,
                "relation": relation,
                "confidence": 0.7,
                "extractor": "tree_sitter",
                "evidence_text": None,
            })

    return edges


def build_edges_from_chunk(
    chunk: Chunk,
    dependencies: list[tuple[str, str, str]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Build all edge dicts derivable from a single chunk.

    Parameters
    ----------
    chunk:
        The source chunk.
    dependencies:
        Optional list of ``(from_node_id, to_symbol, relation)`` tuples
        produced by the dependency extractor for code chunks.

    Returns
    -------
    dict with keys ``eip_deps``, ``cross_refs``, ``code_deps``, each a list
    of edge dicts ready for the corresponding ``store.upsert_*`` function.
    """
    return {
        "eip_deps": _build_eip_deps(chunk),
        "cross_refs": _build_cross_refs(chunk),
        "code_deps": _build_code_deps(chunk, dependencies or []),
    }
