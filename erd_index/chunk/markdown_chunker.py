"""Chunk ParsedUnits from the markdown parser into Chunk objects.

Strategies:
- **Small sections** (< target_chars/3) that share a parent heading are merged.
- **Large sections** (> hard_max_chars) are split at paragraph boundaries.
- **Normal sections** pass through as-is.
"""

from __future__ import annotations

import logging
from datetime import date, datetime

from erd_index.models import Chunk, ChunkKind, ParsedUnit, SourceKind
from erd_index.settings import ChunkSizing

log = logging.getLogger(__name__)

__all__ = ["chunk_parsed_units"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def chunk_parsed_units(
    units: list[ParsedUnit],
    sizing: ChunkSizing,
) -> list[Chunk]:
    """Convert a list of :class:`ParsedUnit` into :class:`Chunk` objects.

    Small consecutive units sharing a parent heading are merged.  Oversized
    units are split at paragraph boundaries.
    """
    if not units:
        return []

    merged = _merge_small(units, sizing)
    chunks: list[Chunk] = []
    for unit in merged:
        if len(unit.text) <= sizing.hard_max_chars:
            chunks.append(_unit_to_chunk(unit))
        else:
            chunks.extend(_split_large(unit, sizing))
    return chunks


# ---------------------------------------------------------------------------
# Merge small consecutive sections
# ---------------------------------------------------------------------------


def _parent_heading(path: list[str]) -> str:
    """Return the parent heading (all but last element), joined."""
    if len(path) <= 1:
        return ""
    return " > ".join(path[:-1])


def _merge_small(
    units: list[ParsedUnit],
    sizing: ChunkSizing,
) -> list[ParsedUnit]:
    threshold = sizing.target_chars // 3
    merged: list[ParsedUnit] = []
    buf: list[ParsedUnit] = []

    def flush() -> None:
        if not buf:
            return
        if len(buf) == 1:
            merged.append(buf[0])
        else:
            combined_text = "\n\n".join(u.text for u in buf)
            # Use the first unit as template, widen line range.
            base = buf[0].model_copy()
            base.text = combined_text
            base.end_line = buf[-1].end_line
            # Heading path: keep the parent only.
            if buf[0].heading_path:
                base.heading_path = list(buf[0].heading_path[:-1]) or list(buf[0].heading_path)
            merged.append(base)
        buf.clear()

    for unit in units:
        # Never merge forum replies — each has distinct author/post metadata.
        is_reply = (
            unit.source_kind == SourceKind.FORUM
            and unit.post_number is not None
            and unit.post_number > 1
        )
        if len(unit.text) >= threshold or is_reply:
            flush()
            merged.append(unit)
            continue

        # Can we append to the buffer?
        if buf:
            same_parent = _parent_heading(unit.heading_path) == _parent_heading(buf[0].heading_path)
            combined_len = sum(len(u.text) for u in buf) + len(unit.text) + 2 * len(buf)
            if same_parent and combined_len <= sizing.target_chars:
                buf.append(unit)
                continue
            else:
                flush()

        buf.append(unit)

    flush()
    return merged


# ---------------------------------------------------------------------------
# Split oversized units at paragraph boundaries
# ---------------------------------------------------------------------------


def _split_large(
    unit: ParsedUnit,
    sizing: ChunkSizing,
) -> list[Chunk]:
    paragraphs = unit.text.split("\n\n")
    parts: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        addition = len(para) + (2 if current else 0)
        if current and current_len + addition > sizing.target_chars:
            parts.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += addition

    if current:
        parts.append("\n\n".join(current))

    # If a single paragraph exceeds hard_max, just keep it (don't split mid-word).
    total = len(parts)
    chunks: list[Chunk] = []

    # Estimate lines per part proportionally.
    total_lines = unit.end_line - unit.start_line + 1
    total_chars = len(unit.text) or 1

    if total_lines <= 1:
        # Single-line unit: can't distribute lines, assign all parts
        # to the same line range.
        for i, part_text in enumerate(parts):
            chunk = _unit_to_chunk(unit)
            chunk.text = part_text
            chunk.start_line = unit.start_line
            chunk.end_line = unit.end_line
            if total > 1:
                chunk.part_index = i
                chunk.part_count = total
            chunks.append(chunk)
    else:
        line_offset = unit.start_line
        for i, part_text in enumerate(parts):
            part_lines = max(1, int(total_lines * len(part_text) / total_chars))
            start_line = min(line_offset, unit.end_line)
            end_line = min(line_offset + part_lines - 1, unit.end_line)
            line_offset = end_line + 1

            chunk = _unit_to_chunk(unit)
            chunk.text = part_text
            chunk.start_line = start_line
            chunk.end_line = end_line
            if total > 1:
                chunk.part_index = i
                chunk.part_count = total
            chunks.append(chunk)

    return chunks


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------


def _chunk_kind_for(unit: ParsedUnit) -> ChunkKind:
    if unit.source_kind == SourceKind.EIP:
        return ChunkKind.EIP_SECTION
    if unit.source_kind == SourceKind.FORUM and unit.post_number and unit.post_number > 1:
        return ChunkKind.MD_REPLY
    return ChunkKind.MD_HEADING


def _unit_to_chunk(unit: ParsedUnit) -> Chunk:
    fm = unit.frontmatter
    return Chunk(
        source_kind=unit.source_kind,
        chunk_kind=_chunk_kind_for(unit),
        source_name=unit.source_name,
        repository=unit.repository,
        language=unit.language,
        path=unit.path,
        title=unit.title,
        text=unit.text,
        start_line=unit.start_line,
        end_line=unit.end_line,
        heading_path=unit.heading_path,
        # Forum fields
        topic_id=unit.topic_id,
        post_number=unit.post_number,
        author=unit.author,
        category=unit.category,
        research_thread=fm.get("research_thread", ""),
        views=_int_or(fm.get("views", 0)),
        likes=_int_or(fm.get("likes", 0)),
        posts_count=_int_or(fm.get("posts_count", 0)),
        influence_score=_float_or(fm.get("influence_score", 0.0)),
        # EIP fields (stashed in frontmatter by parser)
        eip=fm.get("_eip"),
        eip_status=fm.get("_eip_status", ""),
        eip_type=fm.get("_eip_type", ""),
        eip_category=fm.get("_eip_category", ""),
        requires_eips=fm.get("_requires_eips", []),
        supersedes_eips=fm.get("_supersedes_eips", []),
        replaces_eips=fm.get("_replaces_eips", []),
        # Date
        source_date=str(fm.get("date", "")),
        source_date_ts=_date_to_ts(fm.get("date")),
        url=str(fm.get("url", "")),
    )


def _int_or(val: object, default: int = 0) -> int:
    """Coerce *val* to int, returning *default* on failure."""
    if isinstance(val, int):
        return val
    if isinstance(val, (str, float)):
        try:
            return int(val)
        except (ValueError, OverflowError):
            return default
    return default


def _float_or(val: object, default: float = 0.0) -> float:
    """Coerce *val* to float, returning *default* on failure."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            return default
    return default


def _date_to_ts(val: object) -> int:
    """Convert a frontmatter date value to a Unix timestamp, or 0."""
    if isinstance(val, datetime):
        return int(val.timestamp())
    if isinstance(val, date):
        return int(datetime(val.year, val.month, val.day).timestamp())
    if isinstance(val, str) and val:
        s = val.replace("Z", "+00:00") if val.endswith("Z") else val
        try:
            return int(datetime.fromisoformat(s).timestamp())
        except ValueError:
            log.debug("Unparseable date: %r", val)
            return 0
    return 0
