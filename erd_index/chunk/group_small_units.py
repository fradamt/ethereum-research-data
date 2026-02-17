"""Group contiguous small functions into ``code_group`` chunks."""

from __future__ import annotations

import logging

from erd_index.models import Chunk, ChunkKind, ParsedUnit
from erd_index.settings import ChunkSizing

__all__ = ["group_small_units"]

log = logging.getLogger(__name__)


def is_small(unit: ParsedUnit, sizing: ChunkSizing) -> bool:
    """Return True if *unit* qualifies as a small function for grouping."""
    line_count = unit.end_line - unit.start_line + 1
    return (
        line_count <= sizing.small_fn_max_lines
        and len(unit.text) <= sizing.small_fn_max_chars
    )


def group_small_units(
    units: list[ParsedUnit],
    sizing: ChunkSizing,
) -> list[Chunk]:
    """Group contiguous small ``ParsedUnit`` objects sharing the same parent scope.

    Returns ``code_group`` chunks.  Each group contains up to
    ``sizing.small_group_max_members`` members and targets
    ``sizing.small_group_target_chars`` total characters.
    """
    if not units:
        return []

    chunks: list[Chunk] = []
    current_group: list[ParsedUnit] = []
    current_chars = 0
    current_parent = units[0].parent_symbol

    for unit in units:
        # Break group if parent scope changes.
        same_parent = unit.parent_symbol == current_parent

        would_exceed_chars = current_chars + len(unit.text) > sizing.small_group_target_chars
        would_exceed_members = len(current_group) >= sizing.small_group_max_members

        if current_group and (not same_parent or would_exceed_chars or would_exceed_members):
            chunks.append(_flush_group(current_group))
            current_group = []
            current_chars = 0

        current_parent = unit.parent_symbol
        current_group.append(unit)
        current_chars += len(unit.text)

    if current_group:
        chunks.append(_flush_group(current_group))

    return chunks


def _flush_group(members: list[ParsedUnit]) -> Chunk:
    """Create a ``code_group`` chunk from a list of small units."""
    first = members[0]

    # Combine texts with blank line separators.
    combined_text = "\n\n".join(m.text for m in members)
    member_symbols = [m.symbol_name for m in members]

    start_line = min(m.start_line for m in members)
    end_line = max(m.end_line for m in members)

    # Use the first member's metadata for shared fields.
    return Chunk(
        source_kind=first.source_kind,
        chunk_kind=ChunkKind.CODE_GROUP,
        source_name=first.source_name,
        repository=first.repository,
        language=first.language,
        path=first.path,
        title=", ".join(member_symbols),
        text=combined_text,
        start_line=start_line,
        end_line=end_line,
        symbol_name=member_symbols[0] if len(member_symbols) == 1 else "",
        symbol_kind="group",
        parent_symbol=first.parent_symbol,
        module_path=first.module_path,
        visibility=first.visibility,
        imports=first.imports,
        member_symbols=member_symbols,
    )
