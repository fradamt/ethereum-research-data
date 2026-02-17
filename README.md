# ethereum-research-data

Shareable corpus of Ethereum protocol research from public sources.
Scrapes Discourse forums (ethresear.ch, Ethereum Magicians, etc.),
converts to searchable markdown with YAML frontmatter, and maintains
the corpus for use with any search or indexing tool.

## Quick start

```bash
# Clone the repo
git clone https://github.com/your-org/ethereum-research-data
cd ethereum-research-data

# Scrape all configured sources and convert to markdown
scripts/refresh.sh

# Or scrape a single source
scripts/refresh.sh --source ethresearch

# (Optional) Copy all EIPs into the corpus
python3 scripts/curate_eips.py --eips-dir /path/to/EIPs/EIPS

# (Optional) Set up QMD for full-text + semantic search
scripts/setup_qmd.sh
```

Requires Python 3.10+ (stdlib only — no pip dependencies).

## Directory structure

```
sources.json           # Source registry (URLs, output paths)
scraper/               # Discourse forum scraper
converter/             # JSON -> markdown converter
scripts/               # Pipeline and utility scripts
raw/                   # Scraped JSON (gitignored, regeneratable)
corpus/                # The deliverable — searchable markdown
  ethresearch/         # One .md per ethresear.ch topic
  magicians/           # One .md per Ethereum Magicians topic
  eips/                # All EIPs (optional, from EIPs repo)
```

## Adding a new source

To add a new Discourse forum, add an entry to `sources.json`:

```json
{
  "name": "mysite",
  "type": "discourse",
  "url": "https://mysite.example.com",
  "raw_dir": "raw/mysite",
  "corpus_dir": "corpus/mysite"
}
```

Then run `scripts/refresh.sh`. No code changes needed.

## Custom sources

You can add any collection of markdown files to the corpus without going
through the scraper/converter pipeline. Just create a subdirectory under
`corpus/` and place `.md` files in it:

```bash
mkdir corpus/my-papers

# Each file should have YAML frontmatter
cat > corpus/my-papers/example.md << 'EOF'
---
title: "My Research Paper"
author: alice
date: 2025-06-15
source: custom
---

# My Research Paper

Content here...
EOF

# Reindex to make it searchable
scripts/setup_qmd.sh
```

Drop-in directories are never modified by `refresh.sh` — only directories
listed in `sources.json` are managed by the pipeline. The `setup_qmd.sh`
script auto-discovers all subdirectories under `corpus/` and creates a
QMD collection for each.

## Enrichment

The corpus is designed to be enriched by external tools. Enrichment
tools can read the markdown files and add YAML frontmatter fields
(influence scores, thread classification, related topics, etc.)
without modifying the core pipeline. The converter preserves any
extra frontmatter fields on re-conversion.

## Search with QMD

[QMD](https://github.com/tobi/qmd) provides keyword and semantic
search over the corpus. After installing QMD:

```bash
# Set up collections (auto-discovers corpus/ subdirectories, idempotent)
scripts/setup_qmd.sh

# Search
qmd search "proposer boost" --collection ethresearch
qmd vsearch "liveness under asynchrony"
```

## License

The scraped content belongs to its original authors under the
respective forum licenses. This tooling is provided as-is for
research purposes.
