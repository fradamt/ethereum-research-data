"""Parse PDF files into ParsedUnit objects using PyMuPDF.

Extraction strategy (priority order):
1. TOC/bookmarks -- use PDF outline as section boundaries
2. Font-size heuristics -- detect headings by relative font size
3. Page-by-page fallback -- one unit per page
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from pathlib import Path

import pymupdf

from erd_index.models import Language, ParsedUnit, SourceKind

__all__ = ["parse_pdf_file"]

log = logging.getLogger(__name__)


def parse_pdf_file(
    path: Path,
    *,
    source_name: str,
    repository: str = "",
) -> list[ParsedUnit]:
    """Parse a PDF into a list of :class:`ParsedUnit`.

    *path* is the absolute path to the PDF on disk.
    """
    doc = pymupdf.open(str(path))
    try:
        title = doc.metadata.get("title", "") or ""
        toc = doc.get_toc()

        # Fallback title: largest text on page 1, then filename
        if not title:
            title = _extract_title_fallback(doc, toc) or path.stem

        if toc:
            units = _parse_with_toc(doc, toc, title=title)
        else:
            units = _parse_with_font_heuristics(doc, title=title)
            if not units:
                units = _parse_page_by_page(doc, title=title)

        # Fill in shared fields
        for u in units:
            u.source_name = source_name
            u.repository = repository
            u.path = str(path)
            if not u.title and title:
                u.title = title

        # Drop units with empty text
        units = [u for u in units if u.text.strip()]

        return units
    finally:
        doc.close()


# ---------------------------------------------------------------------------
# Title extraction fallback
# ---------------------------------------------------------------------------


_ARXIV_RE = re.compile(r"^arXiv:\d+\.\d+")


def _extract_title_fallback(doc: pymupdf.Document, toc: list[list]) -> str:
    """Extract title from the first page when PDF metadata has no title.

    Strategy: find the largest text on page 1 that isn't a header artifact
    (like arXiv IDs). Research papers typically have the title in the
    largest font on the first page.
    """
    if not doc:
        return ""
    page = doc[0]
    blocks = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_WHITESPACE)["blocks"]

    # Collect all lines with their font sizes
    candidates: list[tuple[float, str]] = []
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            parts: list[str] = []
            line_max_size = 0.0
            for span in line["spans"]:
                text = span["text"].strip()
                if text:
                    parts.append(text)
                    line_max_size = max(line_max_size, span["size"])
            line_text = " ".join(parts)
            if line_text and not _ARXIV_RE.match(line_text):
                candidates.append((line_max_size, line_text))

    if not candidates:
        return ""

    # Return the largest non-artifact text
    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


# ---------------------------------------------------------------------------
# Strategy 1: TOC-based extraction
# ---------------------------------------------------------------------------


def _parse_with_toc(
    doc: pymupdf.Document,
    toc: list[list],
    *,
    title: str,
) -> list[ParsedUnit]:
    """Extract sections using the PDF table of contents (bookmarks).

    Each TOC entry maps to a (level, title, page_number). We extract text
    from each section's page range.
    """
    units: list[ParsedUnit] = []
    total_pages = len(doc)

    for i, entry in enumerate(toc):
        start_page = entry[2]
        # TOC pages are 1-based in the list but pymupdf uses 0-based
        start_page_idx = max(0, start_page - 1)

        # End page: next TOC entry's page (exclusive), or last page
        if i + 1 < len(toc):
            end_page_idx = max(0, toc[i + 1][2] - 1)
        else:
            end_page_idx = total_pages - 1

        text = _extract_text_range(doc, start_page_idx, end_page_idx)
        if not text.strip():
            continue

        # Build heading_path from TOC nesting
        heading_path = _build_heading_path(toc, i)

        units.append(ParsedUnit(
            source_kind=SourceKind.GENERIC,
            language=Language.MARKDOWN,
            source_name="",  # filled in by caller
            path="",  # filled in by caller
            title=title,
            text=text,
            start_line=start_page_idx + 1,  # use page numbers as "lines"
            end_line=end_page_idx + 1,
            heading_path=heading_path,
        ))

    return units


def _extract_text_range(
    doc: pymupdf.Document,
    start_page: int,
    end_page: int,
) -> str:
    """Extract text for a TOC section across its page range.

    When multiple sections share a page, we extract the full page text for
    simplicity. Minor overlap between sections sharing a page boundary is
    acceptable -- the chunker handles deduplication via content hashing.
    """
    parts: list[str] = []
    for page_idx in range(start_page, end_page + 1):
        if page_idx < len(doc):
            page_text = doc[page_idx].get_text("text").strip()
            if page_text:
                parts.append(page_text)
    return "\n\n".join(parts)


def _build_heading_path(toc: list[list], idx: int) -> list[str]:
    """Build the heading path (ancestors + current) from TOC entries."""
    current_level = toc[idx][0]
    current_title = toc[idx][1]
    path: list[str] = [current_title]

    # Walk backwards to find ancestors
    for j in range(idx - 1, -1, -1):
        ancestor_level = toc[j][0]
        if ancestor_level < current_level:
            path.insert(0, toc[j][1])
            current_level = ancestor_level
            if current_level <= 1:
                break

    return path


# ---------------------------------------------------------------------------
# Strategy 2: Font-size heuristics
# ---------------------------------------------------------------------------


def _parse_with_font_heuristics(
    doc: pymupdf.Document,
    *,
    title: str,
) -> list[ParsedUnit]:
    """Detect headings by font size relative to the most common (body) size."""
    # First pass: determine body font size (most frequent)
    size_counts: Counter[float] = Counter()
    for page in doc:
        blocks = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        size_counts[round(span["size"], 1)] += len(text)

    if not size_counts:
        return []

    body_size = size_counts.most_common(1)[0][0]
    heading_threshold = body_size * 1.15  # 15% larger = heading

    # Second pass: segment by headings
    sections: list[tuple[str, str, int]] = []  # (heading, text, page_idx)
    current_heading = ""
    current_text_parts: list[str] = []
    current_page = 0

    for page_idx, page in enumerate(doc):
        blocks = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            block_text_parts: list[str] = []
            block_max_size = 0.0
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        block_text_parts.append(text)
                        block_max_size = max(block_max_size, span["size"])

            block_text = " ".join(block_text_parts)
            if not block_text:
                continue

            if block_max_size >= heading_threshold and len(block_text) < 200:
                # This block is a heading
                if current_heading or current_text_parts:
                    sections.append((
                        current_heading,
                        "\n\n".join(current_text_parts),
                        current_page,
                    ))
                current_heading = block_text
                current_text_parts = []
                current_page = page_idx
            else:
                current_text_parts.append(block_text)
                if not current_heading:
                    current_page = page_idx

    # Flush last section
    if current_heading or current_text_parts:
        sections.append((
            current_heading,
            "\n\n".join(current_text_parts),
            current_page,
        ))

    if not sections:
        return []

    units: list[ParsedUnit] = []
    for heading, text, page_idx in sections:
        if not text.strip():
            continue
        heading_path = [heading] if heading else []
        units.append(ParsedUnit(
            source_kind=SourceKind.GENERIC,
            language=Language.MARKDOWN,
            source_name="",
            path="",
            title=title,
            text=text,
            start_line=page_idx + 1,
            end_line=page_idx + 1,
            heading_path=heading_path,
        ))

    return units


# ---------------------------------------------------------------------------
# Strategy 3: Page-by-page fallback
# ---------------------------------------------------------------------------


def _parse_page_by_page(
    doc: pymupdf.Document,
    *,
    title: str,
) -> list[ParsedUnit]:
    """Last resort: one ParsedUnit per page."""
    units: list[ParsedUnit] = []
    for page_idx, page in enumerate(doc):
        text = page.get_text("text").strip()
        if not text:
            continue
        units.append(ParsedUnit(
            source_kind=SourceKind.GENERIC,
            language=Language.MARKDOWN,
            source_name="",
            path="",
            title=title,
            text=text,
            start_line=page_idx + 1,
            end_line=page_idx + 1,
            heading_path=[f"Page {page_idx + 1}"],
        ))
    return units
