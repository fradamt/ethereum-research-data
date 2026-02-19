"""Tests for PDF pipeline integration."""

from __future__ import annotations

from pathlib import Path

import pymupdf
import pytest

from erd_index.discover.file_walker import walk_sources
from erd_index.settings import CorpusSource, Settings


@pytest.fixture
def pdf_corpus(tmp_settings: Settings) -> Settings:
    """Create a corpus directory with a PDF and a markdown file."""
    corpus = Path(tmp_settings.corpus_dir) / "papers"
    corpus.mkdir(parents=True)

    # Create a small PDF
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 80), "Test Paper Title", fontsize=14)
    page.insert_text((72, 120), "Body text of the test paper.", fontsize=10)
    toc = [[1, "Test Paper Title", 1]]
    doc.set_toc(toc)
    doc.save(str(corpus / "test.pdf"))
    doc.close()

    # Create a markdown file too
    (corpus / "note.md").write_text("# A Note\n\nSome text.")

    # Add corpus source with both PDF and markdown includes
    tmp_settings.corpus_sources.append(
        CorpusSource(
            name="papers",
            path=str(corpus),
            include=["**/*.md", "**/*.pdf"],
        )
    )
    return tmp_settings


class TestPdfDiscovery:
    def test_discovers_pdf_files(self, pdf_corpus: Settings):
        files = list(walk_sources(pdf_corpus))
        languages = {f.language for f in files}
        assert "pdf" in languages
        assert "markdown" in languages

    def test_pdf_file_count(self, pdf_corpus: Settings):
        files = list(walk_sources(pdf_corpus))
        pdf_files = [f for f in files if f.language == "pdf"]
        assert len(pdf_files) == 1

    def test_pdf_relative_path(self, pdf_corpus: Settings):
        files = list(walk_sources(pdf_corpus))
        pdf_files = [f for f in files if f.language == "pdf"]
        assert pdf_files[0].relative_path == "test.pdf"

    def test_pdf_source_name(self, pdf_corpus: Settings):
        files = list(walk_sources(pdf_corpus))
        pdf_files = [f for f in files if f.language == "pdf"]
        assert pdf_files[0].source_name == "papers"

    def test_pdf_has_no_repository(self, pdf_corpus: Settings):
        files = list(walk_sources(pdf_corpus))
        pdf_files = [f for f in files if f.language == "pdf"]
        assert pdf_files[0].repository == ""
