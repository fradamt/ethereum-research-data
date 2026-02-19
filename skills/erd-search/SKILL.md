---
name: erd-search
description: Search Ethereum research data (forum posts, EIPs, code) via the Meilisearch index. Use when answering questions about Ethereum protocol, looking up EIPs, finding spec details, researching protocol history, or searching implementation code. Also use when user types /erd-search.
user_invocable: true
---

# erd-search — Ethereum Research Data Search

Search the Meilisearch-based Ethereum research index covering forum posts
(ethresear.ch, Ethereum Magicians), EIPs, consensus/execution specs, and
client code (go-ethereum, lighthouse, execution-specs).

## Current state

- **Index**: `eth_chunks_v1` — ~93k documents indexed
- **Keyword search**: fully operational
- **Hybrid search**: requires Ollama + embedding setup (see README).
  If embeddings are not ready, use keyword search only.
- **Source breakdown**: forum (~53k), code (~35k), eip (~4k)

## Prerequisites

Meilisearch must be running at `http://localhost:7700` (or `$ERD_MEILI_URL`).

API keys are resolved automatically from `~/.config/erd/search-key` and
`~/.config/erd/admin-key`. You can also set them via environment variables:

```bash
export ERD_SEARCH_KEY=<your-search-key>   # for queries
export ERD_ADMIN_KEY=<your-admin-key>     # for stats/settings
```

If no key files or env vars exist, the CLI falls back to an empty key
(works if Meilisearch has no master key set).

## Search via CLI

The `erd-search` CLI is installed globally (`uv tool install -e`) and works
from any directory. It wraps the Meilisearch API with sensible defaults:
code excluded, distinct by doc_id, Ethereum query expansion for hybrid.

```bash
# Keyword search
erd-search query "proposer boost"

# Filter by source
erd-search query "blob gas" --source-kind eip

# Hybrid search (requires embedding setup)
erd-search query "how does inactivity leak work" --hybrid

# Hybrid with pure semantic mode
erd-search query "what happens during reorganization" --hybrid 0.7

# Filter by author
erd-search query "sharding" --source-kind forum --author vbuterin

# Include code results (excluded by default)
erd-search query "process_attestation" --include-code --repo consensus-specs

# Sort by date
erd-search query "single slot finality" --sort "source_date_ts:desc"

# JSON output for programmatic use
erd-search --json query "EIP-4844"

# Index stats
erd-search stats
```

### CLI flags reference

| Flag | Description |
|------|-------------|
| `--hybrid [RATIO]` | Enable hybrid search (default ratio 0.5 if no value) |
| `--source-kind KIND` | Filter: `forum`, `eip`, `code`, `generic` |
| `--source-name NAME` | Filter: `ethresearch`, `magicians`, `eips`, etc. |
| `--author AUTHOR` | Filter by author name |
| `--eip NUMBER` | Filter by EIP number |
| `--eip-status STATUS` | Filter by EIP status (`Draft`, `Final`, etc.) |
| `--repo NAME` | Filter by repository name |
| `--filter EXPR` | Raw Meilisearch filter expression |
| `--include-code` | Include code chunks (excluded by default) |
| `--no-expand` | Disable query expansion for hybrid mode |
| `--min-text-length N` | Min text length for hybrid results (default 50; 0 to disable) |
| `--sort EXPR` | Sort expression (e.g. `source_date_ts:desc`) |
| `--distinct FIELD` | Distinct field (default: `doc_id`) |
| `--no-distinct` | Show all chunks (disable deduplication) |
| `--limit N` | Max results (default 10) |
| `--fields LIST` | Comma-separated fields to retrieve |
| `--json` | Output raw JSON |
| `-v` / `--verbose` | Show search metadata |

## Query routing

**Keyword search is the default.** Only use hybrid for conceptual or natural
language queries. Technical jargon and exact identifiers score poorly with
the embedding model.

| Query Pattern | Mode | Rationale |
|---------------|------|-----------|
| EIP numbers, function names, exact identifiers | Keyword (no hybrid) | Exact terms; semantic hurts precision |
| Technical jargon (KZG, SSZ, DAS, MEV, PeerDAS) | Keyword (no hybrid) | Embedding model does not understand these acronyms |
| Conceptual questions ("how does X work") | Hybrid (ratio 0.5) | Best precision; binary switch means 0.5 is the only blended mode |
| Natural language ("what happens when...") | Hybrid (ratio 0.5) | Default hybrid ratio; 0.5 is empirically best (0.948 precision) |
| Pure semantic (no keyword matching) | Hybrid (ratio 0.7) | Crosses the binary switch to pure vector mode |

## Default code exclusion

**Code is excluded by default** in the CLI. Code results cause problems:

- The same function appears across every consensus-spec fork version
- Code chunks dominate semantic results, crowding out useful content
- When you DO want code, use `--include-code` with `--repo` to scope results

## Hybrid search notes

**Binary switch behavior:** Meilisearch hybrid search does NOT blend
smoothly. The semanticRatio acts as a binary switch:

- **0.0 - 0.5**: keyword-dominated (results identical across this range)
- **0.6 - 1.0**: semantic-dominated (results identical across this range)
- **0.5**: the ONLY ratio that produces actual blended results

Recommendations:
- Use **keyword** for most queries (the default)
- Use **hybrid 0.5** for conceptual/exploratory questions
- Use **hybrid 0.7** only for pure semantic (rare)
- **Never use hybrid** for specific terms, EIP numbers, identifiers, or jargon

**Short chunk filtering:** Hybrid mode automatically filters chunks shorter
than 50 characters (section headers, stub replies produce generic embeddings).
Use `--min-text-length 0` to disable.

## Search via curl (advanced)

For direct API access or when the CLI is unavailable:

```bash
# Read the search key (from key file or env var)
ERD_KEY="${ERD_SEARCH_KEY:-$(cat ~/.config/erd/search-key 2>/dev/null)}"

# Keyword search
curl -s -X POST 'http://localhost:7700/indexes/eth_chunks_v1/search' \
  -H "Authorization: Bearer $ERD_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "blob gas pricing", "filter": "source_kind != '\''code'\''", "distinct": "doc_id", "limit": 10}'

# Hybrid search
curl -s -X POST 'http://localhost:7700/indexes/eth_chunks_v1/search' \
  -H "Authorization: Bearer $ERD_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "how does proposer boost work", "filter": "source_kind != '\''code'\'' AND text_length >= 50", "hybrid": {"semanticRatio": 0.5, "embedder": "default"}, "distinct": "doc_id", "limit": 10}'
```

## Collection guidance

Route queries using `--source-kind` and `--source-name` filters:

| Question type | CLI flags |
|---------------|-----------|
| General research question | (no filter, or `--source-kind forum`) |
| EIP details, status, content | `--source-kind eip` |
| Specific EIP by number | `--eip 4844` |
| ethresear.ch discussions | `--source-name ethresearch` |
| Ethereum Magicians discussions | `--source-name magicians` |
| Posts by a specific author | `--author vbuterin` |
| Code in go-ethereum | `--include-code --repo go-ethereum` |
| Code in lighthouse (Rust) | `--include-code --repo lighthouse` |
| Content mentioning an EIP | `--filter "mentions_eips = 1559"` |
| Recent discussions | `--sort "source_date_ts:desc"` |

### Combining filters

Use `--filter` for complex expressions:

```bash
erd-search query "sharding" \
  --source-kind forum --author vbuterin \
  --filter "category = 'Sharding' OR mentions_eips = 4844"
```

## Available filterable fields

**All chunks**: `source_kind`, `chunk_kind`, `source_name`, `repository`,
`language`, `doc_id`, `node_id`, `path`, `mentions_eips`,
`schema_version`, `content_hash`, `dedupe_key`, `text_length`

**Forum chunks**: `topic_id`, `post_number`, `author`, `category`,
`research_thread`

**EIP chunks**: `eip`, `eip_status`, `eip_type`, `eip_category`,
`requires_eips`, `supersedes_eips`, `replaces_eips`

**Code chunks**: `symbol_id`, `symbol_name`, `symbol_kind`,
`symbol_qualname`, `parent_symbol`, `module_path`, `visibility`,
`imports`, `used_imports`

## Sortable fields

Use `--sort "field:asc"` or `--sort "field:desc"`:

- `source_date_ts` — publication date
- `indexed_at_ts` — indexing time
- `influence_score` — forum post influence
- `views`, `likes` — forum post engagement
- `eip` — EIP number
- `start_line` — code chunk source position

## Graph queries

For dependency lookups, cross-references, and context expansion, the SQLite
graph database is available at `~/EF/ethereum-research-data/data/graph.db`.

```bash
# EIP dependency graph
sqlite3 ~/EF/ethereum-research-data/data/graph.db \
  "SELECT from_eip, relation, to_eip FROM eip_dependency_edge WHERE from_eip = 4844 OR to_eip = 4844;"

# Code-to-spec links
sqlite3 ~/EF/ethereum-research-data/data/graph.db \
  "SELECT n.symbol_name, n.file_path, l.relation, l.confidence
   FROM spec_code_link l JOIN node n ON l.code_node_id = n.node_id
   WHERE l.eip = 1559;"

# Index stats
erd-index stats
```

## Workflow

1. **Identify the question type** from the collection guidance table above.
2. **Route the query**: keyword for specific terms; hybrid 0.5 for conceptual.
3. **Run the search** with appropriate CLI flags.
4. **Read the `text` field** of top results. Use `path` + `start_line` for context.
5. **Follow cross-references**: use `mentions_eips` or the graph DB.
6. **Cite the source** — include the `url` or `path` in your answer.

If the first search misses, try:
- Switching modes (keyword <-> hybrid)
- Broadening or removing filters
- Searching a different `source_kind` or `source_name`
- Using the graph DB for dependency/reference traversal
