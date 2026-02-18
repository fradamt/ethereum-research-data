# ethereum-research-data

Shareable corpus of Ethereum protocol research with full-text search.

The repo ships with **~6,500 forum posts** from ethresear.ch and Ethereum
Magicians, already converted to searchable markdown. You can index them
immediately or refresh with the latest posts first.

## What's included

- **Forum corpus** (`corpus/ethresearch/`, `corpus/magicians/`) -- ~6,500
  markdown files from ethresear.ch and Ethereum Magicians, with YAML
  frontmatter (title, author, date, views, likes, tags, replies).
- **Corpus pipeline** (`scraper/`, `converter/`) -- scrapes Discourse forums
  incrementally, converts to markdown. Stdlib-only Python, no dependencies.
- **Search infrastructure** (`erd_index/`) -- parses, chunks, and indexes the
  corpus (plus optional code repositories and EIPs) into Meilisearch.
  Supports keyword search, faceted filtering, and optional hybrid search
  via Ollama embeddings.

## Prerequisites

| Component | Required for | Install |
|-----------|-------------|---------|
| Python 3.10+ | everything | -- |
| [uv](https://docs.astral.sh/uv/) | search infrastructure | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/installation) | search infrastructure | see below |
| [Ollama](https://ollama.com) + `nomic-embed-text` | hybrid search (optional) | `ollama pull nomic-embed-text` |

### Installing Meilisearch

Pick **one** of these options:

```bash
# Option A: Binary (macOS)
brew install meilisearch

# Option B: Binary (Linux / macOS without Homebrew)
curl -L https://install.meilisearch.com | sh
# moves ./meilisearch to your PATH, e.g.:
sudo mv ./meilisearch /usr/local/bin/

# Option C: Docker
docker run -d --name meilisearch \
  -p 7700:7700 \
  -e MEILI_MASTER_KEY=changeme \
  -v $(pwd)/data/meili:/meili_data \
  getmeili/meilisearch:latest
```

## Quick start

The corpus is included in the repo, so you can index immediately:

```bash
# Install Python dependencies
uv sync

# Start Meilisearch (skip if using Docker — it's already running)
meilisearch --master-key=changeme &

# Set the master key (must match what Meilisearch was started with)
export MEILI_MASTER_KEY=changeme

# Index the corpus into Meilisearch
./scripts/index_meili.sh
```

This takes a few minutes to parse, chunk, and index ~6,500 forum posts.
After it finishes, search is available via the Meilisearch API at
`http://localhost:7700`.

### Updating the corpus

To scrape new posts from the forums (incremental -- only fetches new topics):

```bash
scripts/refresh.sh        # scrape + convert
./scripts/index_meili.sh  # re-index
```

### Adding EIPs

To include EIPs in the search index, clone the
[EIPs repo](https://github.com/ethereum/EIPs) as a sibling directory
and adjust `config/indexer.toml`:

```toml
[[corpus_sources]]
name = "eips"
path = "../EIPs/EIPS"
include = ["eip-*.md"]
```

### Adding code repositories

To index Ethereum client source code (Go, Rust, Python), clone the repos
as sibling directories. The default `config/indexer.toml` expects:

```
../go-ethereum/     # Go execution client
../lighthouse/      # Rust consensus client
../execution-specs/ # Python execution specs
../consensus-specs/ # Python consensus specs
```

Repos that don't exist on disk are silently skipped -- you only index
what you have.

## Configuration

All indexer settings live in `config/indexer.toml`:

- **`[meilisearch]`** -- URL, index name, batch size
- **`[paths]`** -- corpus directory, data/state databases
- **`[chunk_sizing]`** -- target and max character counts per chunk
- **`[[code_repos]]`** -- code repositories to index. Paths are relative
  to the project root. Adjust to match your local layout.
- **`[[corpus_sources]]`** -- markdown corpus directories. Drop-in
  directories under `corpus/` are also auto-discovered during sync.

Environment: set `MEILI_MASTER_KEY` to match the key Meilisearch was
started with.

## Search examples

```bash
# Keyword search
curl -X POST 'http://localhost:7700/indexes/eth_chunks_v1/search' \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "proposer boost", "limit": 5}'

# Filter by source
curl -X POST 'http://localhost:7700/indexes/eth_chunks_v1/search' \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "blob gas", "filter": "source_name = '\''ethresearch'\''", "limit": 5}'

# Search code (if code repos are indexed)
curl -X POST 'http://localhost:7700/indexes/eth_chunks_v1/search' \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "process_attestation", "filter": "source_kind = '\''code'\''", "limit": 5}'
```

## Development

```bash
uv sync --group dev

# Run tests (400 tests, ~0.7s)
uv run pytest

# Lint
uv run ruff check erd_index/ tests/
```

## Scheduling updates

To keep the corpus fresh automatically:

```bash
# Weekly corpus refresh (Sunday 3am)
0 3 * * 0  cd /path/to/ethereum-research-data && scripts/refresh.sh >> /tmp/erd-refresh.log 2>&1

# Daily incremental Meilisearch sync (4am)
0 4 * * *  cd /path/to/ethereum-research-data && ./scripts/index_meili.sh >> /tmp/erd-index.log 2>&1
```

The scraper and indexer are both incremental, so frequent runs are
inexpensive.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the corpus pipeline design and
[REVIEW.md](REVIEW.md) for the search indexer documentation (data model,
chunking, graph sidecar, spec-code linking, incremental state).

## License

The scraped content belongs to its original authors under the respective
forum licenses. This tooling is provided as-is for research purposes.
