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
| [uv](https://docs.astral.sh/uv/) | package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/installation) | search infrastructure | see below |
| [Ollama](https://ollama.com) + `embeddinggemma:300m` | hybrid search (optional) | `ollama pull embeddinggemma:300m` |

### Installing Meilisearch + Ollama

**Option A: Docker Compose (recommended)**

The included `docker-compose.yml` runs both Meilisearch and Ollama:

```bash
export MEILI_MASTER_KEY=changeme
docker compose up -d
```

This starts Meilisearch on port 7700 and Ollama on port 11434, with
persistent volumes for data and models.

**Option B: Native install**

```bash
# macOS
brew install meilisearch
# or Linux
curl -L https://install.meilisearch.com | sh
sudo mv ./meilisearch /usr/local/bin/

# Start with SSRF workaround (required for v1.35+) and large payload support
meilisearch --master-key=changeme --experimental-allowed-ip-networks any \
  --http-payload-size-limit 104857600 &

# Ollama (optional, for hybrid search)
# Install from https://ollama.com, then:
ollama pull embeddinggemma:300m
```

## Quick start

The corpus is included in the repo, so you can index immediately:

```bash
# Install Python dependencies
uv sync

# Install CLI tools globally (erd-search, erd-index)
uv tool install -e .

# Set the master key (must match what Meilisearch was started with)
export MEILI_MASTER_KEY=changeme

# Start services (skip if using native install)
docker compose up -d

# Index the corpus into Meilisearch
./scripts/index_meili.sh
```

This takes a few minutes to parse, chunk, and index ~6,500 forum posts
into ~93k searchable chunks (each post is split into sections and replies).
After it finishes, search is available via the Meilisearch API at
`http://localhost:7700`, or via the `erd-search` CLI:

```bash
# Keyword search
erd-search query "proposer boost"

# Hybrid search (requires embedding setup — see below)
erd-search query "how does proposer boost work" --hybrid
```

### Updating the corpus

To scrape new posts from the forums (incremental -- only fetches new topics):

```bash
./scripts/refresh.sh        # scrape + convert
./scripts/index_meili.sh    # re-index
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

## CLI reference

The CLIs are installed globally via `uv tool install -e .` (see Quick Start):

```bash
erd-search query "proposer boost"                  # keyword search
erd-search query "how does X work" --hybrid        # hybrid (semantic)
erd-search query "blob gas" --source-kind eip      # filter by source
erd-search query "sharding" --author vbuterin      # filter by author
erd-search query "attestation" --include-code      # include code results
erd-search query "SSF" --sort "source_date_ts:desc"  # sort by date
erd-search --json query "EIP-4844"                 # JSON output
erd-search stats                                   # index statistics
erd-search apply-terminology                       # push synonym config
```

Key flags: `--hybrid [RATIO]`, `--source-kind`, `--source-name`, `--author`,
`--eip NUMBER`, `--repo NAME`, `--filter EXPR`, `--include-code`,
`--sort EXPR`, `--limit N`, `--json`. Run `erd-search query --help`
for full details.

The indexer CLI manages the search index:

```bash
erd-index init          # initialize databases
erd-index sync          # incremental sync (changed files only)
erd-index sync --full-rebuild  # reprocess everything
erd-index stats         # show index statistics
```

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

### Native service configs (non-Docker)

For running Meilisearch as a persistent background service without Docker:

- **macOS**: `config/com.meilisearch.plist` -- copy to
  `~/Library/LaunchAgents/` and load with `launchctl`
- **Linux**: `config/meilisearch.service` -- copy to
  `/etc/systemd/system/` and enable with `systemctl`

Edit the paths and master key in each file before installing.

### API keys

Meilisearch uses a **master key** (set at startup) to derive scoped API keys.
The `erd-search` CLI resolves keys automatically:
**CLI flag** (`--key`) > **env var** > **key file** > empty string fallback.

**For development without a master key**, everything works with empty keys --
just start Meilisearch without `--master-key` and skip this section.

**When running with a master key**, create scoped keys and store them:

```bash
# 1. Start Meilisearch with a master key
export MEILI_MASTER_KEY=changeme

# 2. Create the config directory
mkdir -p ~/.config/erd

# 3. Create a search-only key
curl -s -X POST 'http://localhost:7700/keys' \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"description": "erd search key", "actions": ["search"], "indexes": ["eth_chunks_v1"], "expiresAt": null}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['key'])" \
  > ~/.config/erd/search-key

# 4. Create an admin key (for stats, settings, terminology)
curl -s -X POST 'http://localhost:7700/keys' \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"description": "erd admin key", "actions": ["*"], "indexes": ["eth_chunks_v1"], "expiresAt": null}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['key'])" \
  > ~/.config/erd/admin-key
```

The CLI reads keys from `~/.config/erd/search-key` and `~/.config/erd/admin-key`.
You can also set `ERD_SEARCH_KEY` and `ERD_ADMIN_KEY` environment variables instead.

The `query` subcommand uses the search key; `stats` and `apply-terminology` use
the admin key.

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

## Hybrid search (optional)

Hybrid search combines keyword matching with semantic embeddings for
conceptual queries ("how does inactivity leak work"). Requires Ollama
running with `embeddinggemma:300m`.

The setup script handles everything: pulling the model, batch-embedding
all documents (~30 min for 93k docs), and configuring query-time
embedding.

```bash
# Docker Compose
./scripts/setup_hybrid.sh --docker

# Native Ollama install
./scripts/setup_hybrid.sh

# Resume if interrupted
./scripts/setup_hybrid.sh --resume
```

After setup, hybrid search is available:

```bash
erd-search query "what happens during an inactivity leak" --hybrid
```

The `--hybrid` flag defaults to `semanticRatio=0.5`. Note that Meilisearch's
semantic ratio acts as a binary switch: 0.0-0.5 is keyword-dominated, 0.6-1.0
is semantic-dominated, and 0.5 is the only value that produces blended results.
Use `--hybrid 0.7` for pure semantic mode. See the `erd-search` skill for
detailed query routing guidance.

## Development

```bash
uv sync --group dev

# Run tests (~1100 tests, ~2s)
uv run pytest

# Lint
uv run ruff check erd_index/ tests/
```

## Scheduling updates

To keep the corpus fresh automatically:

```bash
# Weekly corpus refresh (Sunday 3am)
0 3 * * 0  cd /path/to/ethereum-research-data && ./scripts/refresh.sh >> /tmp/erd-refresh.log 2>&1

# Daily incremental Meilisearch sync (4am)
0 4 * * *  cd /path/to/ethereum-research-data && ./scripts/index_meili.sh >> /tmp/erd-index.log 2>&1
```

The scraper and indexer are both incremental, so frequent runs are
inexpensive.

## Claude Code integration

This repo includes an `erd-search` skill (`skills/erd-search/SKILL.md`)
that teaches Claude Code how to search the index. It covers query routing,
filter syntax, the full CLI reference, and search workflow guidance.

Install it to make it available globally:

```bash
./scripts/install_skill.sh    # symlink — updates when you pull
```

Type `/erd-search` in Claude Code to invoke the skill directly.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the corpus pipeline design,
data model, chunking, graph sidecar, and incremental state.

## License

The scraped content belongs to its original authors under the respective
forum licenses. This tooling is provided as-is for research purposes.
