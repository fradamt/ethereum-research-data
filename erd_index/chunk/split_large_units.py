"""Split oversized code units at AST statement boundaries."""

from __future__ import annotations

import logging

from erd_index.models import Chunk, ChunkKind, ParsedUnit
from erd_index.settings import ChunkSizing

__all__ = ["split_large_unit"]

log = logging.getLogger(__name__)

_OVERLAP_LINES = 8


def split_large_unit(unit: ParsedUnit, sizing: ChunkSizing) -> list[Chunk]:
    """Split a ``ParsedUnit`` that exceeds *sizing.hard_max_chars* into parts.

    Strategy:
    1. Parse the function body into top-level statements via simple line analysis.
    2. Greedily group statements until the next would exceed target_chars.
    3. Each part preserves the full signature and docstring as a header.
    4. Fallback: if splitting produces only 1 part, use line-window split with
       overlap.

    Returns a list of ``Chunk`` objects with ``part_index`` and ``part_count``.
    """
    header = _build_header(unit)
    body_lines = _extract_body_lines(unit.text, header)

    if not body_lines:
        # Degenerate case: the whole thing is effectively header.
        return [_make_chunk(unit, unit.text, 0, 1, unit.start_line, unit.end_line)]

    # Try statement-boundary splitting.
    parts = _split_at_statement_boundaries(body_lines, header, sizing)

    if len(parts) <= 1:
        # Fallback: line-window split.
        parts = _split_by_line_windows(body_lines, header, sizing)

    total = len(parts)
    chunks: list[Chunk] = []
    for i, (text, start_offset, end_offset) in enumerate(parts):
        start_line = unit.start_line + start_offset
        end_line = unit.start_line + end_offset
        chunks.append(_make_chunk(unit, text, i, total, start_line, end_line))

    return chunks


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_header(unit: ParsedUnit) -> str:
    """Build the preserved header: signature + docstring."""
    parts: list[str] = []
    if unit.signature:
        parts.append(unit.signature)
    if unit.docstring:
        # Re-wrap docstring with triple quotes for context.
        parts.append(f'    """{unit.docstring}"""')
    return "\n".join(parts)


def _extract_body_lines(full_text: str, header: str) -> list[str]:
    """Extract the body lines (everything after the header)."""
    lines = full_text.split("\n")
    header_line_count = len(header.split("\n"))
    # Skip past the signature/docstring area.  We use a simple heuristic:
    # find where the header ends in the original text.
    body_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Skip signature line(s), docstring, empty lines at the top.
        if i < header_line_count + 5:
            # Look for the end of docstring if present.
            if stripped.endswith('"""') and i > 0:
                body_start = i + 1
                break
            if stripped.endswith("'''") and i > 0:
                body_start = i + 1
                break
        if i >= header_line_count and stripped and not stripped.startswith(('"""', "'''", "#")):
            body_start = i
            break
    else:
        body_start = header_line_count

    return lines[body_start:]


def _is_statement_start(line: str, base_indent: int) -> bool:
    """Heuristic: a line starts a new statement if it's at the base indentation
    level (or less) and is not blank/comment-only."""
    if not line.strip():
        return False
    indent = len(line) - len(line.lstrip())
    return indent <= base_indent and not line.strip().startswith("#")


def _split_at_statement_boundaries(
    body_lines: list[str],
    header: str,
    sizing: ChunkSizing,
) -> list[tuple[str, int, int]]:
    """Split body at statement boundaries, returning (text, start_offset, end_offset) tuples."""
    if not body_lines:
        return []

    # Detect base indentation from the first non-blank line.
    base_indent = 0
    for line in body_lines:
        if line.strip():
            base_indent = len(line) - len(line.lstrip())
            break

    # Find statement boundary indices.
    boundaries = [0]
    for i, line in enumerate(body_lines):
        if i > 0 and _is_statement_start(line, base_indent):
            boundaries.append(i)

    if len(boundaries) <= 1:
        return []  # Can't split meaningfully; fall back.

    target = sizing.target_chars

    parts: list[tuple[str, int, int]] = []
    current_start = 0

    for bi in range(1, len(boundaries)):
        # Candidate: body_lines[current_start:boundaries[bi]]
        candidate = "\n".join(body_lines[current_start : boundaries[bi]])
        if len(header) + 1 + len(candidate) > target and current_start < boundaries[bi - 1]:
            # Flush what we have up to the previous boundary.
            part_text = header + "\n" + "\n".join(body_lines[current_start : boundaries[bi - 1]])
            end_idx = boundaries[bi - 1] - 1
            parts.append((part_text, current_start, end_idx))
            current_start = boundaries[bi - 1]

    # Flush remaining.
    if current_start < len(body_lines):
        part_text = header + "\n" + "\n".join(body_lines[current_start:])
        parts.append((part_text, current_start, len(body_lines) - 1))

    return parts


def _split_by_line_windows(
    body_lines: list[str],
    header: str,
    sizing: ChunkSizing,
) -> list[tuple[str, int, int]]:
    """Fallback: split by line windows with overlap."""
    header_len = len(header) + 1
    target = sizing.target_chars

    # Estimate lines per window.
    avg_line_len = max(1, sum(len(l) for l in body_lines) // max(1, len(body_lines)))
    lines_per_window = max(10, (target - header_len) // max(1, avg_line_len))

    parts: list[tuple[str, int, int]] = []
    start = 0
    while start < len(body_lines):
        end = min(start + lines_per_window, len(body_lines))
        window = body_lines[start:end]
        part_text = header + "\n" + "\n".join(window)
        parts.append((part_text, start, end - 1))
        if end >= len(body_lines):
            break
        start = end - _OVERLAP_LINES

    return parts


def _make_chunk(
    unit: ParsedUnit,
    text: str,
    part_index: int,
    part_count: int,
    start_line: int,
    end_line: int,
) -> Chunk:
    kind = ChunkKind.CODE_STRUCT if unit.symbol_kind in ("struct", "enum", "trait", "class") else ChunkKind.CODE_FUNCTION
    return Chunk(
        source_kind=unit.source_kind,
        chunk_kind=kind,
        source_name=unit.source_name,
        repository=unit.repository,
        language=unit.language,
        path=unit.path,
        title=unit.symbol_name,
        text=text,
        start_line=start_line,
        end_line=end_line,
        symbol_name=unit.symbol_name,
        symbol_kind=unit.symbol_kind,
        symbol_qualname=unit.symbol_qualname,
        signature=unit.signature,
        parent_symbol=unit.parent_symbol,
        module_path=unit.module_path,
        visibility=unit.visibility,
        imports=unit.imports,
        part_index=part_index,
        part_count=part_count,
    )
