# ethereum-research-data

Shareable corpus of Ethereum protocol research with full-text search.

## What's included

- **Corpus pipeline** (`scraper/`, `converter/`) -- scrapes Discourse forums
  (ethresear.ch, Ethereum Magicians), converts to markdown with YAML
  frontmatter. Stdlib-only Python, no dependencies.
- **Search infrastructure** (`erd_index/`) -- parses, chunks, and indexes the
  corpus (plus code repositories) into Meilisearch. Supports keyword search,
  faceted filtering, and optional hybrid search via Ollama embeddings.

## Prerequisites

| Component | Required for | Install |
|-----------|-------------|---------|
| Python 3.10+ | everything | -- |
| [uv](https://docs.astral.sh/uv/) | search infrastructure | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/installation) | search infrastructure | see link |
| [Ollama](https://ollama.com) + `nomic-embed-text` | hybrid search (optional) | `ollama pull nomic-embed-text` |

## Quick start -- corpus only

No dependencies beyond Python stdlib:

```bash
# Scrape all configured Discourse forums and convert to markdown
python -m scraper && python -m converter

# Or use the convenience script (equivalent)
scripts/refresh.sh

# Optionally copy EIPs into the corpus
python3 scripts/curate_eips.py --eips-dir /path/to/EIPs/EIPS
```

## Quick start -- full search

```bash
# Install Python dependencies
uv sync

# Start Meilisearch (separate terminal)
meilisearch --master-key=changeme
export MEILI_MASTER_KEY=changeme

# Build the corpus
scripts/refresh.sh

# Index into Meilisearch
./scripts/index_meili.sh
```

On subsequent runs, `index_meili.sh` performs an incremental sync -- only
changed files are reprocessed.

## Configuration

All indexer settings live in `config/indexer.toml`. Key sections:

- **`[meilisearch]`** -- URL, index name, batch size
- **`[paths]`** -- corpus directory, data/state databases
- **`[chunk_sizing]`** -- target and max character counts per chunk
- **`[[code_repos]]`** -- code repositories to index (Go, Python, Rust).
  Paths are relative to the project root; adjust to match your local checkout
  locations. Repos that don't exist on disk are silently skipped.
- **`[[corpus_sources]]`** -- markdown corpus directories to index

Environment variables: set `MEILI_MASTER_KEY` to match the key Meilisearch
was started with.

## Search examples

```bash
# Keyword search
curl 'http://localhost:7700/indexes/eth_chunks_current/search' \
  -H "Authorization: Bearer changeme" \
  -d '{"q": "proposer boost", "limit": 5}'

# Filter by source kind
curl 'http://localhost:7700/indexes/eth_chunks_current/search' \
  -H "Authorization: Bearer changeme" \
  -d '{"q": "EIP-4844 blob gas", "filter": "source_kind = ethresearch", "limit": 5}'

# Search code only
curl 'http://localhost:7700/indexes/eth_chunks_current/search' \
  -H "Authorization: Bearer changeme" \
  -d '{"q": "process_attestation", "filter": "doc_type = code", "limit": 5}'
```

## Development

```bash
uv sync --group dev

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy erd_index/
```

## Scheduling updates

To keep the corpus fresh automatically, add a cron job (or launchd plist on
macOS). Examples:

```bash
# Weekly corpus refresh — scrape forums and convert to markdown (Sunday 3am)
0 3 * * 0  cd /path/to/ethereum-research-data && scripts/refresh.sh >> /tmp/erd-refresh.log 2>&1

# Daily incremental Meilisearch sync (4am)
0 4 * * *  cd /path/to/ethereum-research-data && ./scripts/index_meili.sh >> /tmp/erd-index.log 2>&1

# Monthly full reindex (1st of month, 5am)
0 5 1 * *  cd /path/to/ethereum-research-data && uv run erd-index sync --no-incremental >> /tmp/erd-full.log 2>&1
```

Adjust paths and schedules to taste. The scraper and indexer are both
incremental, so frequent runs are inexpensive.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the corpus pipeline design and
[REVIEW.md](REVIEW.md) for a detailed walkthrough of the `erd_index`
indexing pipeline (data model, chunking strategy, graph sidecar, incremental
state management).

## License

The scraped content belongs to its original authors under the respective
forum licenses. This tooling is provided as-is for research purposes.
