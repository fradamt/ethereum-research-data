"""Tests for erd_index.parse.pdf_parser."""

from __future__ import annotations

from pathlib import Path

import pymupdf
import pytest

from erd_index.models import Language, SourceKind
from erd_index.parse.pdf_parser import parse_pdf_file


@pytest.fixture
def pdf_with_toc(tmp_path: Path) -> Path:
    """Create a small PDF with TOC bookmarks and two sections."""
    doc = pymupdf.open()

    # Page 1: title + intro
    page1 = doc.new_page()
    page1.insert_text((72, 80), "My Research Paper", fontsize=18)
    page1.insert_text((72, 120), "1 Introduction", fontsize=14)
    page1.insert_text(
        (72, 150),
        "This paper studies something interesting about distributed systems.",
        fontsize=10,
    )

    # Page 2: methods
    page2 = doc.new_page()
    page2.insert_text((72, 80), "2 Methods", fontsize=14)
    page2.insert_text(
        (72, 110),
        "We use formal verification to prove our results.",
        fontsize=10,
    )

    # Add TOC
    toc = [
        [1, "Introduction", 1],
        [1, "Methods", 2],
    ]
    doc.set_toc(toc)

    out = tmp_path / "paper_with_toc.pdf"
    doc.save(str(out))
    doc.close()
    return out


@pytest.fixture
def pdf_no_toc(tmp_path: Path) -> Path:
    """Create a PDF without TOC but with detectable heading font sizes."""
    doc = pymupdf.open()

    page = doc.new_page()
    page.insert_text((72, 80), "Abstract", fontsize=14)
    page.insert_text(
        (72, 120),
        "This is the abstract text for a paper about consensus protocols.",
        fontsize=10,
    )
    page.insert_text((72, 200), "Background", fontsize=14)
    page.insert_text(
        (72, 240),
        "Consensus protocols ensure agreement among distributed nodes.",
        fontsize=10,
    )

    out = tmp_path / "paper_no_toc.pdf"
    doc.save(str(out))
    doc.close()
    return out


@pytest.fixture
def pdf_flat(tmp_path: Path) -> Path:
    """Create a PDF with uniform font size (no headings detectable)."""
    doc = pymupdf.open()

    page = doc.new_page()
    page.insert_text((72, 80), "All text is the same size here.", fontsize=10)
    page.insert_text((72, 110), "No headings to detect at all.", fontsize=10)

    out = tmp_path / "flat.pdf"
    doc.save(str(out))
    doc.close()
    return out


class TestParsePdfWithToc:
    def test_returns_parsed_units(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault")
        assert len(units) >= 2

    def test_source_kind_is_generic(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault")
        for u in units:
            assert u.source_kind == SourceKind.GENERIC

    def test_language_is_markdown(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault")
        for u in units:
            assert u.language == Language.MARKDOWN

    def test_heading_path_populated(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault")
        headings = [u.heading_path for u in units if u.heading_path]
        assert len(headings) >= 2

    def test_title_extracted(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault")
        assert any("Introduction" in str(u.heading_path) for u in units)

    def test_text_not_empty(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault")
        for u in units:
            assert u.text.strip()

    def test_path_is_relative(self, pdf_with_toc: Path):
        units = parse_pdf_file(
            pdf_with_toc, source_name="vault",
        )
        for u in units:
            assert u.path == str(pdf_with_toc)


class TestParsePdfNoToc:
    def test_falls_back_to_font_heuristics(self, pdf_no_toc: Path):
        units = parse_pdf_file(pdf_no_toc, source_name="vault")
        assert len(units) >= 2
        headings = [u.heading_path for u in units if u.heading_path]
        assert len(headings) >= 1


class TestParsePdfFlat:
    def test_falls_back_to_page_split(self, pdf_flat: Path):
        units = parse_pdf_file(pdf_flat, source_name="vault")
        assert len(units) >= 1
        for u in units:
            assert u.text.strip()


class TestParsePdfEdgeCases:
    def test_empty_pdf(self, tmp_path: Path):
        doc = pymupdf.open()
        doc.new_page()  # blank page
        out = tmp_path / "empty.pdf"
        doc.save(str(out))
        doc.close()
        units = parse_pdf_file(out, source_name="vault")
        assert units == []

    def test_source_name_propagated(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="my-papers")
        for u in units:
            assert u.source_name == "my-papers"

    def test_repository_propagated(self, pdf_with_toc: Path):
        units = parse_pdf_file(pdf_with_toc, source_name="vault", repository="test-repo")
        for u in units:
            assert u.repository == "test-repo"
