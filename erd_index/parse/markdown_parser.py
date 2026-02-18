"""Parse markdown files into ParsedUnit objects.

Handles three corpus flavours:
- **forum** (ethresearch / magicians): heading-split + reply detection
- **eip**: heading-split with EIP metadata from frontmatter
- **generic**: plain heading-split
"""

from __future__ import annotations

import logging
import re
from typing import Any

from erd_index.models import Language, ParsedUnit, SourceKind
from erd_index.parse.frontmatter import extract_frontmatter

__all__ = ["parse_markdown"]

log = logging.getLogger(__name__)

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})", re.MULTILINE)
_REPLY_BOUNDARY_RE = re.compile(r"^---\s*$", re.MULTILINE)
_REPLY_HEADING_RE = re.compile(r"^\*\*(\S+)\*\*\s+\((\d{4}-\d{2}-\d{2})\):\s*$")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_markdown(
    text: str,
    *,
    path: str,
    source_name: str,
    repository: str = "",
) -> list[ParsedUnit]:
    """Parse a single markdown file into a list of :class:`ParsedUnit`.

    *source_name* determines the parsing flavour:
    - ``ethresearch`` / ``magicians`` → forum (replies are split)
    - ``eips`` → EIP (metadata extracted from frontmatter)
    - anything else → generic heading-split
    """
    fm, body = extract_frontmatter(text)
    source_kind = _source_kind_for(source_name)
    title = fm.get("title", "") or _extract_title(body)

    # Line offset: number of lines consumed by frontmatter + delimiters.
    # _line_number computes 1-based lines relative to body; add this offset
    # to get correct line numbers in the original file.
    fm_line_offset = text.count("\n", 0, len(text) - len(body))

    if source_kind == SourceKind.FORUM:
        units = _parse_forum(body, fm=fm, title=title, path=path,
                             source_name=source_name, repository=repository)
    elif source_kind == SourceKind.EIP:
        units = _parse_eip(body, fm=fm, title=title, path=path,
                           source_name=source_name, repository=repository)
    else:
        units = _parse_generic(body, fm=fm, title=title, path=path,
                               source_name=source_name, repository=repository,
                               source_kind=source_kind)

    if fm_line_offset > 0:
        for u in units:
            u.start_line += fm_line_offset
            u.end_line += fm_line_offset

    return units


# ---------------------------------------------------------------------------
# Source kind mapping
# ---------------------------------------------------------------------------


def _source_kind_for(source_name: str) -> SourceKind:
    if source_name in ("ethresearch", "magicians"):
        return SourceKind.FORUM
    if source_name == "eips":
        return SourceKind.EIP
    return SourceKind.GENERIC


def _extract_title(body: str) -> str:
    """Return the text of the first ``# `` heading, if any."""
    for m in _HEADING_RE.finditer(body):
        if len(m.group(1)) == 1:
            return m.group(2).strip()
    return ""


# ---------------------------------------------------------------------------
# Fenced-code-block awareness
# ---------------------------------------------------------------------------


def _fenced_ranges(text: str) -> list[tuple[int, int]]:
    """Return (start_offset, end_offset) pairs for fenced code blocks.

    Handles unclosed fences gracefully: an unclosed opener is skipped
    without consuming subsequent fence markers (so later blocks are
    still detected).
    """
    all_fences = list(_FENCE_RE.finditer(text))
    ranges: list[tuple[int, int]] = []
    i = 0
    while i < len(all_fences):
        m = all_fences[i]
        fence_char = m.group(1)[0]
        fence_len = len(m.group(1))
        start = m.start()
        # Find matching close fence.
        found = False
        for j in range(i + 1, len(all_fences)):
            m2 = all_fences[j]
            if m2.group(1)[0] == fence_char and len(m2.group(1)) >= fence_len:
                ranges.append((start, m2.end()))
                i = j + 1
                found = True
                break
        if not found:
            i += 1  # Unclosed fence — skip without consuming later markers
    return ranges


def _inside_fence(offset: int, fenced: list[tuple[int, int]]) -> bool:
    for s, e in fenced:
        if s <= offset < e:
            return True
    return False


# ---------------------------------------------------------------------------
# Line utilities
# ---------------------------------------------------------------------------


def _line_number(text: str, offset: int) -> int:
    """1-based line number for *offset* in *text*."""
    return text.count("\n", 0, offset) + 1


# ---------------------------------------------------------------------------
# Forum parser
# ---------------------------------------------------------------------------


def _parse_forum(
    body: str,
    *,
    fm: dict[str, Any],
    title: str,
    path: str,
    source_name: str,
    repository: str,
) -> list[ParsedUnit]:
    """Split a forum topic into the OP (heading-split) + per-reply units."""
    topic_id = fm.get("topic_id")
    author = str(fm.get("author", ""))
    category = str(fm.get("category", ""))

    # Locate ``## Replies`` section.
    replies_match = re.search(r"^##\s+Replies\s*$", body, re.MULTILINE)
    if replies_match:
        op_body = body[: replies_match.start()].rstrip()
        replies_body = body[replies_match.end():]
    else:
        op_body = body
        replies_body = ""

    units: list[ParsedUnit] = []

    # --- OP sections (heading-split) ---
    op_sections = _split_headings(op_body)
    for heading_path, section_text, start_off, end_off in op_sections:
        units.append(ParsedUnit(
            source_kind=SourceKind.FORUM,
            language=Language.MARKDOWN,
            source_name=source_name,
            repository=repository,
            path=path,
            title=title,
            text=section_text,
            start_line=_line_number(body, start_off),
            end_line=_line_number(body, end_off),
            heading_path=heading_path,
            topic_id=topic_id,
            post_number=1,
            author=author,
            category=category,
            frontmatter=fm,
        ))

    # --- Replies ---
    if replies_body:
        # Global offset of replies_body within *body*.
        replies_offset = len(body) - len(replies_body)
        reply_units = _split_replies(replies_body, offset=replies_offset)
        post_num = 2
        for r_author, r_text, r_start, r_end in reply_units:
            units.append(ParsedUnit(
                source_kind=SourceKind.FORUM,
                language=Language.MARKDOWN,
                source_name=source_name,
                repository=repository,
                path=path,
                title=title,
                text=r_text.strip(),
                start_line=_line_number(body, r_start),
                end_line=_line_number(body, r_end),
                heading_path=[title, "Replies"],
                topic_id=topic_id,
                post_number=post_num,
                author=r_author,
                category=category,
                frontmatter=fm,
            ))
            post_num += 1

    return units


def _split_replies(
    text: str, *, offset: int = 0,
) -> list[tuple[str, str, int, int]]:
    """Split reply text at ``---`` boundaries.

    Returns list of (author, text, abs_start, abs_end).
    """
    fenced = _fenced_ranges(text)
    # Find ``---`` separators that are NOT inside fenced blocks.
    separators: list[int] = []
    for m in _REPLY_BOUNDARY_RE.finditer(text):
        if not _inside_fence(m.start(), fenced):
            separators.append(m.start())

    if not separators:
        # No separators — treat as single reply.
        author = _reply_author(text)
        return [(author, text.strip(), offset, offset + len(text))]

    chunks: list[tuple[str, str, int, int]] = []

    # Content before the first ``---`` (first reply with no preceding separator).
    pre = text[: separators[0]].strip()
    if pre:
        author = _reply_author(pre)
        chunks.append((author, pre, offset, offset + separators[0]))

    for i, sep in enumerate(separators):
        start = sep
        end = separators[i + 1] if i + 1 < len(separators) else len(text)
        chunk = text[start:end]
        # Strip leading ``---\n``.
        inner = re.sub(r"^---\s*\n?", "", chunk)
        if inner.strip():
            author = _reply_author(inner)
            # Advance start past the --- separator so start_line points
            # to actual reply content, not the separator itself.
            content_start = start + (len(chunk) - len(inner))
            chunks.append((author, inner.strip(), offset + content_start, offset + end))

    return chunks


def _reply_author(text: str) -> str:
    """Extract author from the first line matching ``**Name** (date):``."""
    first_line = text.lstrip().split("\n", 1)[0]
    m = _REPLY_HEADING_RE.match(first_line)
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# EIP parser
# ---------------------------------------------------------------------------


def _parse_eip(
    body: str,
    *,
    fm: dict[str, Any],
    title: str,
    path: str,
    source_name: str,
    repository: str,
) -> list[ParsedUnit]:
    eip_num = _int_or_none(fm.get("eip"))
    eip_status = str(fm.get("status", ""))
    eip_type = str(fm.get("type", ""))
    eip_category = str(fm.get("category", ""))
    requires_eips = _parse_int_list(fm.get("requires"))
    supersedes_eips = _parse_int_list(fm.get("superseded-by"))
    replaces_eips = _parse_int_list(fm.get("replaces"))

    sections = _split_headings(body)
    units: list[ParsedUnit] = []
    for heading_path, section_text, start_off, end_off in sections:
        units.append(ParsedUnit(
            source_kind=SourceKind.EIP,
            language=Language.MARKDOWN,
            source_name=source_name,
            repository=repository,
            path=path,
            title=title,
            text=section_text,
            start_line=_line_number(body, start_off),
            end_line=_line_number(body, end_off),
            heading_path=heading_path,
            frontmatter=fm,
        ))

    # Attach EIP metadata to every unit via model fields that Chunk can copy.
    # ParsedUnit doesn't have eip_* fields — we stash them in frontmatter
    # and let the chunker propagate.  Actually, ParsedUnit *does* have
    # topic_id/post_number/author/category for forum — but for EIPs we use
    # frontmatter.  The chunker will read these.
    for u in units:
        u.frontmatter = {
            **fm,
            "_eip": eip_num,
            "_eip_status": eip_status,
            "_eip_type": eip_type,
            "_eip_category": eip_category,
            "_requires_eips": requires_eips,
            "_supersedes_eips": supersedes_eips,
            "_replaces_eips": replaces_eips,
        }

    return units


# ---------------------------------------------------------------------------
# Generic parser
# ---------------------------------------------------------------------------


def _parse_generic(
    body: str,
    *,
    fm: dict[str, Any],
    title: str,
    path: str,
    source_name: str,
    repository: str,
    source_kind: SourceKind,
) -> list[ParsedUnit]:
    sections = _split_headings(body)
    return [
        ParsedUnit(
            source_kind=source_kind,
            language=Language.MARKDOWN,
            source_name=source_name,
            repository=repository,
            path=path,
            title=title,
            text=section_text,
            start_line=_line_number(body, start_off),
            end_line=_line_number(body, end_off),
            heading_path=heading_path,
            frontmatter=fm,
        )
        for heading_path, section_text, start_off, end_off in sections
    ]


# ---------------------------------------------------------------------------
# Heading splitter (shared)
# ---------------------------------------------------------------------------


def _split_headings(
    text: str,
) -> list[tuple[list[str], str, int, int]]:
    """Split *text* at ``##`` and ``###`` headings.

    Returns list of (heading_path, section_text, start_offset, end_offset).
    Content before the first heading (or if there are no headings) is returned
    with an empty heading_path.  Code fences are respected.
    """
    fenced = _fenced_ranges(text)

    # Collect heading positions (## and ###).
    headings: list[tuple[int, int, str]] = []  # (offset, level, title)
    for m in _HEADING_RE.finditer(text):
        level = len(m.group(1))
        if level < 2 or level > 3:
            continue
        if _inside_fence(m.start(), fenced):
            continue
        headings.append((m.start(), level, m.group(2).strip()))

    if not headings:
        return [([], text, 0, len(text))] if text.strip() else []

    sections: list[tuple[list[str], str, int, int]] = []

    # Content before first heading.
    if headings[0][0] > 0:
        pre = text[: headings[0][0]]
        if pre.strip():
            sections.append(([], pre, 0, headings[0][0]))

    # Build heading path stack.
    path_stack: list[tuple[int, str]] = []  # (level, title)

    for i, (off, level, htitle) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
        section_text = text[off:end]

        # Maintain path stack: pop anything at same or deeper level.
        while path_stack and path_stack[-1][0] >= level:
            path_stack.pop()
        path_stack.append((level, htitle))
        heading_path = [t for _, t in path_stack]

        if section_text.strip():
            sections.append((heading_path, section_text, off, end))

    return sections


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _int_or_none(val: Any) -> int | None:
    if val is None:
        return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _parse_int_list(val: Any) -> list[int]:
    """Parse a frontmatter field that may be an int, a comma-separated string,
    or a list into ``list[int]``."""
    if val is None:
        return []
    if isinstance(val, int):
        return [val]
    if isinstance(val, list):
        out = []
        for v in val:
            try:
                out.append(int(v))
            except (TypeError, ValueError):
                log.debug("Skipping non-integer value %r in int list", v)
        return out
    if isinstance(val, str):
        out = []
        for part in val.replace(",", " ").split():
            try:
                out.append(int(part))
            except ValueError:
                log.debug("Skipping non-integer value %r in int list", part)
        return out
    return []
