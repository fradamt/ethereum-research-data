# PDF Ingestion Design

**Date**: 2026-02-19
**Status**: Approved

## Goal

Add PDF ingestion to the indexer pipeline so PDFs in corpus source directories
(e.g., `vault/papers/`) are automatically discovered, parsed, chunked, and
indexed during `sync` — same as markdown files.

## Constraints

- PDFs are text-based research papers (no OCR needed)
- Reuse existing chunker and document builder — no schema changes
- PDFs become `source_kind=GENERIC` documents, same as vault markdown

## Library Choice

**PyMuPDF (`pymupdf`)** — best structured text extraction for research papers.
Provides font-size heuristics, bookmark/TOC extraction, and fast C backend.

## Architecture

### 1. Discovery

`erd_index/discover/language_detector.py`: add `".pdf": "pdf"` to
`_EXTENSION_MAP`.

Corpus source `include` patterns updated to also match `*.pdf` where desired
(e.g., vault source).

### 2. Parser

New file: `erd_index/parse/pdf_parser.py`

```python
def parse_pdf_file(
    path: Path,
    *,
    source_name: str,
    repository: str = "",
) -> list[ParsedUnit]:
```

Section extraction strategy (in priority order):
1. **TOC/bookmarks** — many research papers have PDF outlines. Use these as
   section boundaries.
2. **Font-size heuristics** — detect headings by font size/weight relative to
   body text. Group consecutive body text under the nearest heading.
3. **Page-by-page fallback** — if no structure detected, emit one ParsedUnit
   per page.

Each section becomes a `ParsedUnit` with:
- `source_kind = GENERIC`
- `language = Language.MARKDOWN` (text is plain, chunker handles it)
- `heading_path` from detected headings
- `title` from PDF metadata or first heading
- `start_line` / `end_line` mapped to page numbers

### 3. Pipeline

New function in `erd_index/pipeline.py`:

```python
def ingest_pdf(settings: Settings, *, dry_run: bool = False) -> IngestStats:
```

Modeled after `ingest_markdown()`:
- Filters `walk_sources()` for `language == "pdf"`
- Calls `parse_pdf_file()` per file
- Feeds results into `chunk_parsed_units()` (existing markdown chunker)
- Enriches with `extract_eip_refs()` where applicable
- Builds documents via `chunk_to_document()` and upserts to Meilisearch

Called from `sync()` alongside existing `ingest_markdown()` and
`ingest_code()`.

### 4. Config

Update `config/indexer.toml` vault source:

```toml
[[corpus_sources]]
name = "vault"
path = "/Users/francesco/Library/Mobile Documents/..."
include = ["**/*.md", "**/*.pdf"]
```

### What doesn't change

- `models.py` — `ParsedUnit`, `Chunk`, `SourceKind`, `ChunkKind` all reused
- `chunk/` — markdown chunker works on any `list[ParsedUnit]`
- `index/document_builder.py` — `chunk_to_document()` handles GENERIC
- Meilisearch schema — no new fields
- Search CLI — PDFs searchable immediately via existing filters

## Dependencies

Add to `pyproject.toml`:

```toml
"pymupdf>=1.25,<2.0"
```
