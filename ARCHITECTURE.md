# ethereum-research-data — Architecture

Shareable corpus of Ethereum protocol research from public sources.
Scrapes Discourse forums, converts to searchable markdown, and maintains
the corpus for use with any search/indexing tool.

## Design principles

1. **Stdlib-only Python** — no pip dependencies. Anyone with Python 3.10+ can use it.
2. **Extensible sources** — adding a new Discourse forum is config, not code.
   Adding a non-Discourse source means adding one new scraper module.
3. **Separation of concerns** — scraping, converting, and indexing are
   independent steps. Each can be run alone.
4. **Enrichment is external** — the corpus is plain markdown. Enrichment
   (influence scores, graph links, thread classification) is a separate
   layer applied on top, not built in.
5. **Incremental by default** — re-running any step only processes new/changed data.

## Directory structure

```
ethereum-research-data/
├── README.md
├── ARCHITECTURE.md
├── sources.json                # Source registry (URLs, output paths, config)
│
├── scraper/
│   ├── __init__.py
│   ├── discourse.py            # Discourse forum scraper (generic)
│   └── cli.py                  # CLI entry point: python -m scraper
│
├── converter/
│   ├── __init__.py
│   ├── discourse_to_md.py      # Discourse JSON → markdown
│   └── cli.py                  # CLI entry point: python -m converter
│
├── scripts/
│   ├── refresh.sh              # Full pipeline: scrape all → convert all
│   ├── setup_qmd.sh            # Create QMD collections pointing at corpus/
│   └── curate_eips.py          # Copy all EIPs from an EIPs repo
│
├── erd_index/                  # Meilisearch indexing pipeline (uv-managed)
│   ├── embed_proxy.py          # Splitting embed proxy (Meilisearch → Ollama)
│
├── raw/                        # Scraped JSON (gitignored — regeneratable)
│   ├── ethresearch/
│   │   ├── index.json
│   │   ├── categories.json
│   │   ├── about.json
│   │   └── topics/             # {id}.json per topic
│   └── magicians/
│       ├── index.json
│       ├── categories.json
│       ├── about.json
│       └── topics/
│
├── corpus/                     # The deliverable — searchable markdown
│   ├── ethresearch/            # One .md per topic (managed by refresh.sh)
│   ├── magicians/              # One .md per topic (managed by refresh.sh)
│   ├── eips/             # All EIPs (managed by curate_eips.py)
│   └── <custom>/               # Drop-in directories (user-managed, never touched by refresh.sh)
│
└── .gitignore                  # raw/ ignored
```

## Corpus contract

Any subdirectory under `corpus/` that contains markdown files (`.md`) with
YAML frontmatter is a valid corpus source, regardless of how it was created.
This means:

- **Managed sources** (ethresearch, magicians) are populated by the
  scraper/converter pipeline via `refresh.sh`. These are listed in
  `sources.json` and their content is regeneratable from raw JSON.
- **Script-managed sources** (eips) are populated by dedicated scripts
  like `curate_eips.py`.
- **Drop-in sources** are any other subdirectory placed under `corpus/` by
  the user. `refresh.sh` never reads, writes, or deletes files in directories
  it does not own (i.e., directories not listed in `sources.json`).

`setup_qmd.sh` auto-discovers all subdirectories under `corpus/` and creates
a QMD collection for each one that contains `.md` files. No registration in
`sources.json` is needed for indexing — just place a directory of markdown
files in `corpus/` and run `scripts/setup_qmd.sh`.

The only requirement for drop-in content is that each `.md` file starts with
YAML frontmatter (`---` delimited). The frontmatter fields are not
prescribed — use whatever fields are appropriate for the content. Recommended
fields: `title`, `author`, `date`, `source`.

## sources.json

Defines all scraping targets. The scraper reads this to know what to fetch.

```json
{
  "sources": [
    {
      "name": "ethresearch",
      "type": "discourse",
      "url": "https://ethresear.ch",
      "raw_dir": "raw/ethresearch",
      "corpus_dir": "corpus/ethresearch"
    },
    {
      "name": "magicians",
      "type": "discourse",
      "url": "https://ethereum-magicians.org",
      "raw_dir": "raw/magicians",
      "corpus_dir": "corpus/magicians"
    }
  ]
}
```

To add a new Discourse forum: add an entry to sources.json. No code changes.

## Scraper (scraper/)

Generic Discourse scraper. Given a base URL:
1. Fetches /about.json → site stats
2. Fetches /categories.json → category tree
3. Paginates through categories + /latest → builds topic index
4. Fetches each topic's full content (with post pagination)

All output goes to the source's `raw_dir`. Incremental: skips already-fetched topics.

### CLI

```bash
# Scrape all sources defined in sources.json
python -m scraper

# Scrape a specific source
python -m scraper --source ethresearch

# Scrape a one-off URL (not in sources.json)
python -m scraper --url https://some-discourse.org --output raw/custom
```

## Converter (converter/)

Converts raw JSON topics to markdown. Given a source's raw_dir and corpus_dir:
1. Reads each {id}.json from raw_dir/topics/
2. Reads categories from raw_dir/categories.json
3. Renders markdown with YAML frontmatter + body + replies
4. Writes to corpus_dir/{id}-{slug}.md

### Markdown format

```markdown
---
source: ethresearch
topic_id: 12345
title: "Example Topic Title"
author: username
date: 2024-01-15
category: Proof-of-Stake
tags: [tag1, tag2]
url: https://ethresear.ch/t/example-topic/12345
views: 5000
likes: 42
posts_count: 15
---

# Example Topic Title

Body text of the first post...

## Replies

**username2** (2024-01-16):

Reply text...

---

**username3** (2024-01-17):

Another reply...
```

YAML frontmatter makes it easy for enrichment tools to add fields later
(e.g., `influence_score`, `research_thread`, `related`).

### CLI

```bash
# Convert all sources
python -m converter

# Convert a specific source
python -m converter --source ethresearch

# Convert with reply limit
python -m converter --max-replies 10
```

## Scripts

### refresh.sh

```bash
#!/bin/bash
# Full pipeline: scrape all sources, convert all, optionally update QMD
python -m scraper
python -m converter
echo "Corpus updated. Run 'scripts/setup_qmd.sh' to reindex."
```

### setup_qmd.sh

Auto-discovers all subdirectories under `corpus/` that contain `.md` files
and creates a QMD collection for each one. This includes both managed sources
(from sources.json) and drop-in directories. Idempotent: safe to re-run.

### curate_eips.py

Given a path to an EIPs repo, copies all EIPs to corpus/eips/.
Uses mtime checks to skip unchanged files and removes stale entries.
Reads YAML frontmatter to filter by status.

## Enrichment (external)

The corpus is designed to be enriched by external tools. The contract:
- Enrichment tools read corpus markdown files
- They may add YAML frontmatter fields (influence_score, research_thread, related, etc.)
- They may write enriched files in-place or to a separate directory
- The corpus converter never overwrites enrichment fields on re-conversion
  (it checks for existing frontmatter and preserves extra fields)

This means evolution-map's analyze.py (or any other tool) can add metadata
to the corpus without the corpus repo needing to know about it.
