"""Convert parsed code units into search-ready chunks."""

from __future__ import annotations

import logging

from erd_index.chunk.group_small_units import group_small_units, is_small
from erd_index.chunk.split_large_units import split_large_unit
from erd_index.models import Chunk, ChunkKind, ParsedUnit
from erd_index.settings import ChunkSizing

__all__ = ["chunk_code_units"]

log = logging.getLogger(__name__)


def chunk_code_units(
    units: list[ParsedUnit],
    sizing: ChunkSizing | None = None,
    *,
    preserve_individuals: bool = False,
) -> list[Chunk]:
    """Partition *units* into ``Chunk`` objects using the sizing policy.

    1. Small functions (below thresholds) are grouped into ``code_group`` chunks.
    2. Normal functions become one ``code_function`` (or ``code_struct``) chunk each.
    3. Large functions (above hard_max_chars) are split at statement boundaries.

    If *preserve_individuals* is True, small functions that were grouped also
    appear as individual chunks (for graph-node resolution).  These individual
    chunks are returned alongside the group chunks.
    """
    if sizing is None:
        sizing = ChunkSizing()

    small: list[ParsedUnit] = []
    normal: list[ParsedUnit] = []
    large: list[ParsedUnit] = []

    for unit in units:
        text_len = len(unit.text)
        if text_len > sizing.hard_max_chars:
            large.append(unit)
        elif is_small(unit, sizing):
            small.append(unit)
        else:
            normal.append(unit)

    chunks: list[Chunk] = []

    # 1. Group small functions.
    if small:
        chunks.extend(group_small_units(small, sizing))
        if preserve_individuals:
            for unit in small:
                chunks.append(_unit_to_chunk(unit))

    # 2. Normal-sized units: one chunk each.
    for unit in normal:
        chunks.append(_unit_to_chunk(unit))

    # 3. Large units: split.
    for unit in large:
        chunks.extend(split_large_unit(unit, sizing))

    # Sort by source position for stable output.
    chunks.sort(key=lambda c: (c.path, c.start_line))
    return chunks


def _unit_to_chunk(unit: ParsedUnit) -> Chunk:
    """Convert a single normal-sized ``ParsedUnit`` to a ``Chunk``."""
    kind = _chunk_kind(unit)
    return Chunk(
        source_kind=unit.source_kind,
        chunk_kind=kind,
        source_name=unit.source_name,
        repository=unit.repository,
        language=unit.language,
        path=unit.path,
        title=unit.symbol_name,
        text=unit.text,
        start_line=unit.start_line,
        end_line=unit.end_line,
        symbol_name=unit.symbol_name,
        symbol_kind=unit.symbol_kind,
        symbol_qualname=unit.symbol_qualname,
        signature=unit.signature,
        parent_symbol=unit.parent_symbol,
        module_path=unit.module_path,
        visibility=unit.visibility,
        imports=unit.imports,
    )


def _chunk_kind(unit: ParsedUnit) -> ChunkKind:
    if unit.symbol_kind in ("struct", "enum", "trait", "class", "interface", "impl"):
        return ChunkKind.CODE_STRUCT
    return ChunkKind.CODE_FUNCTION
