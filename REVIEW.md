# erd-index: Review Document

> Comprehensive documentation for the `erd_index` package — a Meilisearch-based
> indexing pipeline for Ethereum research data. Written to facilitate code review.

**Package**: `ethereum-research-data-indexer` 0.1.0
**Location**: `/Users/francesco/EF/ethereum-research-data/erd_index/`
**Codebase**: ~6,700 lines of implementation + ~3,700 lines of tests (305 passing)
**Dependencies**: meilisearch, pydantic v2, PyYAML, tree-sitter 0.23, orjson
**Runtime**: Meilisearch 1.35.1 (localhost:7700), Ollama + nomic-embed-text (optional, for hybrid search)

---

## Table of Contents

1. [Purpose and Context](#1-purpose-and-context)
2. [Architecture Overview](#2-architecture-overview)
3. [Data Model](#3-data-model)
4. [Pipeline Stages](#4-pipeline-stages)
5. [Meilisearch Integration](#5-meilisearch-integration)
6. [Graph Sidecar](#6-graph-sidecar)
7. [Incremental State](#7-incremental-state)
8. [CLI Interface](#8-cli-interface)
9. [Configuration](#9-configuration)
10. [Testing](#10-testing)
11. [Key Design Decisions](#11-key-design-decisions)
12. [Known Issues and Remaining Work](#12-known-issues-and-remaining-work)
13. [File Reference](#13-file-reference)

---

## 1. Purpose and Context

This package replaces QMD (a local markdown search engine) with a richer
search infrastructure built on Meilisearch. It indexes three source types:

| Source | Example | Volume |
|--------|---------|--------|
| **Forum posts** | ethresear.ch, Ethereum Magicians | ~6,500 markdown files (scraped via existing `scraper/` + `converter/`) |
| **EIPs** | EIP-4844, EIP-1559 | ~3,700 files (copied from EIPs repo into `corpus/eips/`) |
| **Source code** | go-ethereum, execution-specs, lighthouse, consensus-specs | 4 repos, Python/Go/Rust |

The existing `scraper/`, `converter/`, and `scripts/refresh.sh` pipeline
(stdlib Python, no deps) remains untouched. This package (`erd_index/`) is a
separate indexing layer that reads the `corpus/` output and code repos, then
writes to Meilisearch and a SQLite graph database.

**Design informed by**: raulk's `eth-protocol-expert` (PostgreSQL + pgvector +
FalkorDB). We adapted the graph-sidecar idea but chose a simpler local-first
stack: Meilisearch for search, SQLite for the graph, no external database.

---

## 2. Architecture Overview

```
                                    config/indexer.toml
                                           │
                                      ┌────┴────┐
                                      │ Settings │
                                      └────┬────┘
                                           │
    ┌──────────────┬───────────────┬────────┼────────┬──────────────┬────────────┐
    │              │               │        │        │              │            │
 discover/      parse/          chunk/    enrich/   index/       graph/       state/
 ─────────   ──────────────   ────────   ────────   ──────────   ─────────   ──────────
 file_walker  frontmatter     markdown_  eip_refs   meili_schema store       manifest_db
 language_    markdown_parser chunker    forum_meta meili_client node_builder run_log
 detector     py_parser       code_      code_meta  document_    edge_builder
              go_parser       chunker    dependency builder
              rust_parser     split_     extractor  writer
              treesitter_     large_
              runtime         group_small
    │              │               │        │        │              │            │
    └──────────────┴───────────────┴────────┼────────┴──────────────┴────────────┘
                                           │
                                      ┌────┴────┐
                                      │ pipeline │  ← orchestration
                                      └────┬────┘
                                           │
                                      ┌────┴────┐
                                      │   cli   │
                                      └─────────┘
```

**Data flow** for a single file:

```
disk file
  → discover (walk + language detect + stat)
  → state check (skip if unchanged: mtime_ns + size_bytes + version match)
  → parse (markdown: heading-split + frontmatter; code: tree-sitter AST)
  → chunk (merge small sections / split large ones / group small functions)
  → enrich (EIP refs, forum metadata, code metadata, dependency extraction)
  → index (build Meilisearch document → batch_upsert; delete stale chunk IDs)
  → graph (chunk → node dict → upsert; chunk + deps → edge dicts → upsert)
  → state update (upsert manifest row with chunk_ids, hash, mtime)
```

---

## 3. Data Model

Defined in `erd_index/models.py`. Two Pydantic v2 models flow through the pipeline:

### ParsedUnit (parse → chunk boundary)

Output of parsers. Represents a logical unit: a heading section, a forum reply,
an EIP section, a function definition, a struct, etc.

Key fields: `source_kind`, `language`, `text`, `start_line`/`end_line`,
`heading_path` (markdown), `symbol_name`/`symbol_kind`/`signature` (code),
`topic_id`/`post_number`/`author` (forum), `frontmatter` dict.

### Chunk (chunk → enrich → index → graph)

Output of chunkers. Each Chunk maps to exactly one Meilisearch document and
optionally one graph node. Has all ParsedUnit fields plus enrichment fields
(`mentions_eips`, `used_imports`, `calls`, `influence_score`, etc.) and four
computed properties:

| Computed Field | Format | Purpose |
|---------------|--------|---------|
| `content_hash` | SHA-256[:16] of normalized text | Change detection |
| `doc_id` | `forum:ethresearch:1234`, `eip:4844`, `code:go-ethereum:core/vm/interpreter.go` | Parent document grouping |
| `chunk_id` | `source_name:path:start:end[:pN]:content_hash` | Deterministic document ID |
| `node_id` | `repo:path:qualname` (code), `eip:N[:anchor]` (EIP), `forum:source:topic:post` (forum) | Graph join key |
| `dedupe_key` | Same as chunk_id but without content_hash | Stable dedup across edits |

### Enums

- `SourceKind`: `forum`, `eip`, `code`
- `ChunkKind`: `md_heading`, `md_reply`, `eip_section`, `code_function`, `code_struct`, `code_group`
- `Language`: `markdown`, `python`, `go`, `rust`

---

## 4. Pipeline Stages

### 4.1 Discovery (`discover/`)

**`file_walker.py`** — `walk_sources(settings)` generator yields `DiscoveredFile`
dataclasses. Walks both `corpus_sources` (markdown) and `code_repos` (code),
applying include/exclude glob patterns from config. Each `DiscoveredFile` carries
`absolute_path`, `relative_path`, `source_name`, `repository`, `language`,
`size_bytes`, `mtime_ns`.

**`language_detector.py`** — `detect_language(path)` based on file extension
(`.md` → markdown, `.py` → python, `.go` → go, `.rs` → rust).

### 4.2 Parsing (`parse/`)

**`frontmatter.py`** — `extract_frontmatter(text)` → `(dict, body_str)`. Handles
malformed YAML gracefully (returns empty dict on parse error).

**`markdown_parser.py`** — `parse_markdown(text, path, source_name, repository)`
→ `list[ParsedUnit]`. Two modes:

- **Forum mode** (`source_name` in `{"ethresearch", "magicians"}`): Splits OP at
  heading boundaries, then detects replies at `---` + `### Reply by ...` boundaries.
  Each reply gets its own ParsedUnit with `post_number`, `author` from the separator.
- **EIP mode** (`path` matches `eip-*.md`): Extracts eip number, status, type,
  category, requires/supersedes/replaces from frontmatter. Splits at heading boundaries.
- **Generic mode**: Heading-split only.

All modes are code-fence-aware: never splits inside fenced blocks.

**`treesitter_runtime.py`** — `get_language(name)` with `@lru_cache`, wraps the
tree-sitter 0.23 API (Language + Parser objects).

**`py_parser.py`** — Extracts functions, classes, decorated defs, docstrings, imports.

**`go_parser.py`** — Extracts functions, methods (with receivers), struct/interface
types, doc comments, package declarations.

**`rust_parser.py`** — Extracts functions, structs, enums, traits + trait members,
impl blocks + members, use declarations.

All three return `list[ParsedUnit]` with `symbol_name`, `symbol_kind`, `signature`,
`parent_symbol`, `visibility`, `imports` populated.

### 4.3 Chunking (`chunk/`)

**`markdown_chunker.py`** — `chunk_parsed_units(units, sizing)` → `list[Chunk]`:

1. **Merge small sections** (`_merge_small`): Consecutive units under the same
   parent heading and below `target_chars/3` (~933 chars) are merged. Forum
   replies (`post_number > 1`) are never merged (preserves per-reply metadata).
2. **Split large sections** (`_split_large`): Units exceeding `hard_max_chars`
   (5500) are split at paragraph boundaries. Each part gets `part_index`/`part_count`.
3. Normal-sized sections pass through as-is.

**`code_chunker.py`** — `chunk_code_units(units, sizing)` → `list[Chunk]`:

1. **Split large functions** (`split_large_units.py`): Functions exceeding
   `hard_max_chars` are split at AST statement boundaries, preserving the
   function header in each part.
2. **Group small functions** (`group_small_units.py`): Functions below
   `small_fn_max_lines` (12) / `small_fn_max_chars` (450) sharing a parent
   scope are grouped into `code_group` chunks (max 6 members, target 2200 chars).
3. Normal-sized functions pass through as-is.

### 4.4 Enrichment (`enrich/`)

**`eip_refs.py`** — `extract_eip_refs(text)` → `list[int]`. Regex-based extraction
of EIP/ERC references. Skips code blocks. Handles `EIP-N`, `ERC-N`, `EIP N` formats.

**`forum_metadata.py`** — `enrich_forum_chunk(chunk)` → mutates chunk. Computes
`influence_score` from views, likes, posts_count using a weighted formula.

**`code_metadata.py`** — `enrich_code_chunk(chunk)` → mutates chunk. Derives
`symbol_qualname` (parent.symbol), filters `used_imports` from `imports` based on
text references, extracts `calls` from text, sets `visibility` (public/private/dunder).

**`dependency_extractor.py`** — `extract_dependencies(chunk)` →
`list[tuple[str, str, str]]` where each tuple is `(from_node_id, to_symbol, relation)`.
Relations: `calls`, `uses_type`, `imports`, `implements_trait`. Used to build
code dependency graph edges.

### 4.5 Indexing (`index/`)

**`meili_schema.py`** — Defines `SCHEMA_VERSION = 1` and `get_index_settings()`:
searchable attributes (title, text, symbol_name, ...), filterable attributes
(source_kind, eip, language, ...), sortable attributes (source_date_ts,
influence_score, views, ...), distinct attribute (`dedupe_key`).

**`meili_client.py`** — Connection management:
- `get_client(settings)` — creates client with health check
- `init_index(settings)` — creates index + applies settings + sets up alias
- `ensure_index(settings)` — idempotent: creates if missing, re-applies settings
  if schema version changed. Schema version is detected by sampling a document.

**`document_builder.py`** — `chunk_to_document(chunk, schema_version)` → `dict`.
Converts a Chunk to a Meilisearch document. Key behaviors:
- `sanitize_chunk_id(chunk_id)` replaces `:` → `-`, `/` → `_`, `.` → `_`
  (Meilisearch IDs allow only alphanumeric, hyphens, underscores)
- Omits None/empty fields for compact storage
- `symbol_id` set to `node_id` for code chunks with a `symbol_name`

**`writer.py`** — Batch operations:
- `batch_upsert(settings, documents)` — upserts in batches of `batch_size` (1000),
  waits for each task to complete, raises on failure
- `delete_by_ids(settings, chunk_ids)` — deletes by sanitized Meilisearch IDs
- `delete_by_filter(settings, filter_str)` — filter-based deletion
- `get_index_stats(settings)` — returns document count, field distribution

### 4.6 Graph (`graph/`)

**`schema.sql`** — 5 tables in `data/graph.db` (WAL mode, FK enforcement):

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `node` | Every indexable entity | `node_id` (PK), `node_type`, `eip`, `symbol_name`, `content_hash` |
| `eip_dependency_edge` | EIP requires/supersedes/replaces | `from_eip`, `to_eip`, `relation` |
| `spec_code_link` | Spec-to-code implementation links | `eip`, `code_node_id`, `relation`, `match_method` |
| `cross_reference_edge` | Any-to-any cross-references | `from_node_id`, `to_node_id`, `relation` |
| `code_dependency_edge` | Code calls/imports/uses | `from_code_node_id`, `to_code_node_id` or `to_external_symbol` |

10 indexes for common query patterns.

**`store.py`** — CRUD operations + query helpers:
- `upsert_node` — `INSERT ... ON CONFLICT(node_id) DO UPDATE SET ...`
  (preserves FK-referenced edges; was `INSERT OR REPLACE` which cascade-deleted edges)
- `upsert_eip_dep` — `INSERT OR IGNORE` (UNIQUE constraint on from/to/relation/source)
- `upsert_cross_ref`, `upsert_code_dep`, `upsert_spec_code_link` — manual
  NULL-aware existence checks (SQLite `NULL != NULL` in UNIQUE constraints)
- `get_neighbors(node_id, depth, relation)` — iterative BFS across all 4 edge tables
- `get_eip_context(eip_number)` — returns EIP nodes, implementing code, forum
  discussions, dependencies, dependents

**`node_builder.py`** — `chunk_to_node(chunk)` → dict mapping ChunkKind to
node_type (`code_function` → `code_function`, `eip_section` → `eip_section`,
forum OP → `forum_topic`, forum reply → `forum_post`).

**`edge_builder.py`** — `build_edges_from_chunk(chunk, dependencies)` → dict with
three lists:
- `eip_deps`: from `requires_eips`, `supersedes_eips`, `replaces_eips` frontmatter
- `cross_refs`: from `mentions_eips` (regex-extracted EIP references)
- `code_deps`: from dependency extractor tuples. Heuristic: `":"` in target symbol
  → resolved node_id; otherwise → external symbol.

---

## 5. Meilisearch Integration

### Index lifecycle

```
erd-index init
  → creates eth_chunks_v1 index
  → applies searchableAttributes, filterableAttributes, sortableAttributes
  → creates eth_chunks_current alias (via swap-indexes API)

erd-index sync (or individual ingest commands)
  → ensure_index: checks if index exists + schema version is current
  → batch_upsert: adds/updates documents in batches of 1000
  → delete_by_ids: removes stale chunks when files change
  → Meilisearch handles BM25 scoring and typo tolerance internally
```

### Document ID sanitization

Raw `chunk_id` format: `ethresearch:topics/1234.md:1:20:abcdef0123456789`

Meilisearch requires IDs with only alphanumeric chars, hyphens, underscores.
The `sanitize_chunk_id()` function replaces `:` → `-`, `/` → `_`, `.` → `_`:

`ethresearch-topics_1234_md-1-20-abcdef0123456789`

Both the document builder and the pipeline manifest store sanitized IDs, so
`delete_by_ids()` works correctly against Meilisearch.

### Hybrid search (optional)

Meilisearch 1.35.1 supports vector search via an external embedder. Configured
to use Ollama with `nomic-embed-text` (768 dimensions, 8192 token context).
This is optional — BM25 keyword search works without it.

---

## 6. Graph Sidecar

The graph in `data/graph.db` serves two purposes:

1. **EIP dependency navigation** — given EIP-4844, find all EIPs it requires,
   all EIPs that require it, implementing code, and forum discussions.
2. **Code dependency traversal** — find what a function calls, what calls it,
   what types it uses.

The graph is **fully rebuildable from source** — `build_graph()` re-derives
all chunks from disk and rebuilds all nodes and edges. No intermediate state
is needed.

### Two-pass build

1. **Pass 1 (nodes)**: Parse + chunk all files → `upsert_node` for each chunk
2. **Pass 2 (edges)**: For each chunk, `build_edges_from_chunk` → `upsert_eip_dep`,
   `upsert_cross_ref`, `upsert_code_dep`

Nodes must exist before edges due to FK constraints.

### NULL-aware idempotency

SQLite treats `NULL != NULL` in UNIQUE constraints. Edge tables with nullable
columns (`span_start`, `span_end`, `to_code_node_id`, `to_external_symbol`,
`eip_section_anchor`) use manual existence checks with `IS NULL`/`IS ?` instead
of `INSERT OR IGNORE`.

---

## 7. Incremental State

`data/index_state.db` tracks what has been indexed to avoid reprocessing unchanged files.

### indexed_file table

| Column | Purpose |
|--------|---------|
| `repository` + `file_path` | Composite PK |
| `mtime_ns` + `size_bytes` | Fast-skip check (avoids hashing) |
| `file_hash` | SHA-256 for content-level change detection |
| `parser_version` + `chunker_version` | Forces reprocessing on version bumps |
| `chunk_ids_json` | JSON array of sanitized Meilisearch document IDs |
| `last_indexed_at` | Timestamp for staleness queries |

### Change detection flow

```
is_file_changed(repo, path, size, mtime, parser_v, chunker_v):
  1. No manifest row? → changed (new file)
  2. Version mismatch? → changed (force reprocess)
  3. mtime_ns or size_bytes differ? → changed
  4. Otherwise → unchanged, skip
```

### Stale file cleanup

After processing all files in a source, `get_stale_files(source, current_paths)`
finds manifest rows whose file_path is not in the current discovery set.
These represent deleted files. Their `chunk_ids_json` is used to call
`delete_by_ids()` on Meilisearch, then the manifest row is removed.

### Stale chunk cleanup (within a file)

When a file is re-indexed and produces different chunk IDs than before
(e.g., a heading was renamed, changing the content hash), `_stale_chunk_ids()`
diffs the old manifest's `chunk_ids_json` against the new chunk IDs. Removed
IDs are deleted from Meilisearch before the manifest is updated.

### Dry-run safety

The `--dry-run` flag skips both Meilisearch writes and manifest updates. This
ensures that a dry-run followed by `--changed-only` will still process all files
(since the manifest was never updated to reflect "done").

---

## 8. CLI Interface

```
erd-index <command> [options]

Commands:
  init           Initialize Meilisearch index and SQLite databases
  ingest-md      Ingest markdown from corpus/
  ingest-code    Ingest code from configured repos
  build-graph    Build/update dependency graph
  sync           Full sync: md + code + graph
  stats          Show index and graph statistics

Global options:
  --config PATH        Config TOML (default: config/indexer.toml)
  --project-root PATH  Project root (default: cwd)
  --verbose, -v        Debug logging
  --batch-size N       Override Meilisearch batch size
```

### sync command

`sync` runs all three phases with error isolation:

```python
ingest_markdown(...)
try:
    ingest_code(...)     # won't block markdown results on failure
except Exception: ...
if not dry_run:
    try:
        build_graph(...)  # won't block indexing on failure
    except Exception: ...
```

### Convenience script

`scripts/index_meili.sh` — initializes databases on first run, then calls
`erd-index sync` with passthrough args (`--full-rebuild`, `--dry-run`, `-v`).

---

## 9. Configuration

`config/indexer.toml`:

```toml
[meilisearch]
url = "http://localhost:7700"        # or ERD_MEILI_URL env var
index_name = "eth_chunks_v1"
index_alias = "eth_chunks_current"
batch_size = 1000                    # documents per Meilisearch task
# master_key via MEILI_MASTER_KEY env var

[chunk_sizing]
target_chars = 2800                  # ideal chunk size
hard_max_chars = 5500                # absolute maximum before splitting
small_fn_max_lines = 12              # code function "small" threshold
small_fn_max_chars = 450
small_group_target_chars = 2200      # target for grouped small functions
small_group_max_members = 6

[versions]
schema_version = 1                   # bump to force settings re-apply
parser_version = "0.1.0"             # bump to force reparse of all files
chunker_version = "0.1.0"            # bump to force rechunk of all files

[[code_repos]]
name = "go-ethereum"
path = "~/EF/go-ethereum"
language = "go"
include = ["**/*.go"]
exclude = ["vendor/**", "build/**", "tests/testdata/**"]
# ... (4 repos total)

[[corpus_sources]]
name = "ethresearch"
path = "corpus/ethresearch"
include = ["**/*.md"]
# ... (3 sources total)
```

**Precedence**: CLI flags > environment variables > TOML defaults.

---

## 10. Testing

305 tests across 10 test files, all passing in ~0.5s.

| Test File | Tests | What It Covers |
|-----------|-------|----------------|
| `test_frontmatter.py` | 22 | YAML extraction, malformed input, edge cases |
| `test_markdown_chunker.py` | 35 | Reply splitting, EIP parsing, merge/split logic, code fences |
| `test_eip_refs.py` | 30 | EIP/ERC regex extraction, code block skipping |
| `test_enrichment.py` | 43 | Forum metadata, code metadata, visibility, dependencies |
| `test_incremental.py` | 29 | Change detection, manifest CRUD, stale file detection |
| `test_document_builder.py` | 29 | Document conversion, field omission, ID sanitization |
| `test_graph_store.py` | 58 | Node/edge CRUD, idempotency, neighbors, EIP context, stats |
| `test_treesitter_parsers.py` | 39 | Python/Go/Rust AST extraction with fixture files |
| `test_code_chunker.py` | 20 | Split/group logic, part metadata |
| `conftest.py` | — | Shared fixtures: `fixtures_dir`, `tmp_settings` |

**Test fixtures**: `tests/fixtures/` contains sample markdown files, a Python file,
Go file, and Rust file for parser tests.

**No integration tests** against a live Meilisearch instance — all Meili interactions
are in writer.py/meili_client.py and tested manually via E2E smoke runs.

---

## 11. Key Design Decisions

### Why Meilisearch over Postgres/pgvector/Elasticsearch?

- **Local-first**: Runs as a single binary, no Docker/cluster needed
- **BM25 out of the box**: Typo-tolerant, prefix search, faceted filtering
- **Hybrid search**: Optional vector embeddings via external embedder (Ollama)
- **Simple ops**: Single data directory, no WAL/vacuum tuning, backup = copy the dir
- Tradeoff: no SQL joins — the graph sidecar in SQLite fills that gap

### Why SQLite graph sidecar instead of a graph database?

- No external dependencies (FalkorDB/Neo4j are heavyweight for a single-user tool)
- Fully rebuildable from source, so it's a cache, not a source of truth
- BFS traversal over 4 typed edge tables is sufficient for the query patterns
  (EIP context, code dependency navigation)
- WAL mode gives concurrent read access while writing

### Why tree-sitter 0.23 (not 0.24+)?

- At time of implementation, tree-sitter-rust 0.23.3 had a language version
  incompatibility with tree-sitter 0.23.2. Pinned to `>=0.23,<0.23.3`.
- The 0.23 API (Language + Parser objects) is stable and sufficient.

### Why not an MCP server?

Decided against building an MCP server. Instead, search is exposed via a
Claude Code skill (`~/.claude/skills/erd-search/SKILL.md`) that wraps
`curl` calls to the Meilisearch REST API. This avoids the complexity of
maintaining an MCP server process and keeps the search interface simple.

### Chunk ID sanitization

Meilisearch document IDs only allow `[a-zA-Z0-9_-]`. Raw chunk_ids contain
`:`, `/`, `.` from path and source identifiers. Rather than changing the
chunk_id format (which would break node_id references), we sanitize at the
Meilisearch boundary: `sanitize_chunk_id()` replaces prohibited characters.
Both the document builder and the manifest store sanitized IDs.

### Forum reply non-merging

Forum replies are never merged by the chunker, even when short. Each reply
has distinct `author` and `post_number` metadata that would be lost by
merging. This is enforced in `_merge_small()` with an explicit `is_reply` check.

---

## 12. Known Issues and Remaining Work

### Fixed (this session)

These bugs were found by a GPT-5.3-codex architecture review and fixed:

| # | Bug | Fix |
|---|-----|-----|
| 1 | **Stale chunk accumulation** — re-indexing a file didn't delete old chunk IDs from Meili | Added `_stale_chunk_ids()` diffing old vs new manifest entries |
| 2 | **`--dry-run` wrote to manifest** — subsequent `--changed-only` skipped files | Wrapped `upsert_indexed_file()` in `if not dry_run:` |
| 3 | **Forum reply merge** — small replies got merged, losing author/post_number | `_merge_small()` now skips forum replies |
| 4 | **`INSERT OR REPLACE` cascade-deleted edges** — re-upserting a graph node deleted its FK edges | Changed to `ON CONFLICT(node_id) DO UPDATE SET ...` |
| 5 | **chunk_id/Meili ID mismatch** — manifest stored raw IDs, Meili had sanitized IDs | Added `sanitize_chunk_id()` helper; both now use sanitized IDs |

### Remaining (moderate priority)

These were identified by the Codex review but not yet fixed:

| Issue | Description | Impact |
|-------|-------------|--------|
| **Rust `::` in edge builder** | `_build_code_deps` heuristic: `":" in to_symbol` misclassifies Rust paths like `std::collections::HashMap` as resolved node_ids | Wrong `to_code_node_id` for Rust deps |
| **`build_graph(changed_only=True)` ignores the flag** | The `changed_only` parameter is accepted but never passed to file discovery | Graph always fully rebuilds |
| **Go multi-type declarations** | `type ( A struct{}; B struct{} )` produces units with same line span → chunk_id collision | Rare; only affects grouped type blocks |
| **`superseded-by` edge direction** | `supersedes_eips` edges go from→to but "superseded-by" semantics may expect the reverse | Review spec intent |
| **`source_date_ts` never populated** | Chunk field exists but no enrichment step converts `source_date` string to timestamp | Sort by date doesn't work |
| **Stale cleanup misses empty sources** | If a source is removed from config, its files aren't discovered, so `paths_by_source` has no entry and stale cleanup doesn't run | Orphaned docs persist in Meili |
| **`stats --repo` flag unused** | CLI accepts `--repo` but `show_stats()` ignores it | Minor UX |
| **Small-function grouping loses individual graph nodes** | Grouped functions produce one `code_group` node, individual functions don't get their own nodes | Graph loses per-function resolution |
| **Markdown line numbers off** | Frontmatter stripping shifts line numbers but ParsedUnit.start_line isn't adjusted | start_line inaccurate by ~frontmatter length |

### Not yet implemented

| Feature | Notes |
|---------|-------|
| **Full corpus ingestion** | Only 3,682 EIP docs indexed so far; 6,500+ forum files pending |
| **Code repo ingestion** | Not yet run against the 4 configured repos |
| **Ollama embeddings** | Meilisearch embedder configured but embedding task was cancelled (was blocking all writes) |
| **Spec-code linking** | `spec_code_link` table exists but no automated linker populates it |
| **Claude Code search skill testing** | Skill file exists but not exercised end-to-end |

---

## 13. File Reference

### Source (`erd_index/`, ~6,700 lines)

| File | Lines | Purpose |
|------|-------|---------|
| `models.py` | 209 | Pydantic models: ParsedUnit, Chunk, enums |
| `settings.py` | 166 | Config dataclasses, TOML loader |
| `cli.py` | 183 | argparse CLI, subcommand dispatch |
| `pipeline.py` | ~690 | Orchestration: ingest_markdown, ingest_code, build_graph, sync_all, show_stats |
| `discover/file_walker.py` | ~130 | Source walking with glob include/exclude |
| `discover/language_detector.py` | ~20 | Extension → language mapping |
| `parse/frontmatter.py` | ~60 | YAML frontmatter extraction |
| `parse/markdown_parser.py` | ~280 | Markdown heading-split + forum reply detection + EIP extraction |
| `parse/treesitter_runtime.py` | ~40 | tree-sitter Language/Parser wrapper |
| `parse/py_parser.py` | ~180 | Python AST → ParsedUnit |
| `parse/go_parser.py` | ~200 | Go AST → ParsedUnit |
| `parse/rust_parser.py` | ~220 | Rust AST → ParsedUnit |
| `chunk/markdown_chunker.py` | ~210 | Merge small / split large / convert to Chunk |
| `chunk/code_chunker.py` | ~80 | Code chunk orchestration |
| `chunk/split_large_units.py` | ~100 | AST-boundary splitting for large functions |
| `chunk/group_small_units.py` | ~90 | Parent-scope grouping for small functions |
| `enrich/eip_refs.py` | ~70 | Regex EIP/ERC reference extraction |
| `enrich/forum_metadata.py` | ~50 | Influence score computation |
| `enrich/code_metadata.py` | ~100 | Qualname, used_imports, calls, visibility |
| `enrich/dependency_extractor.py` | ~80 | Code dependency tuple extraction |
| `index/meili_schema.py` | 80 | Schema version + index settings dict |
| `index/meili_client.py` | 156 | Connection, init, ensure, alias management |
| `index/document_builder.py` | ~140 | Chunk → Meilisearch document dict |
| `index/writer.py` | 103 | batch_upsert, delete_by_ids, delete_by_filter |
| `graph/schema.sql` | 118 | DDL for 5 tables + 10 indexes |
| `graph/store.py` | ~540 | CRUD + get_neighbors + get_eip_context + get_stats |
| `graph/node_builder.py` | ~112 | Chunk → graph node dict |
| `graph/edge_builder.py` | 162 | Chunk → edge dicts (EIP deps, cross-refs, code deps) |
| `state/schema.sql` | 34 | DDL for indexed_file + run_log |
| `state/manifest_db.py` | ~217 | CRUD for incremental state |
| `state/run_log.py` | ~70 | Run audit log |

### Tests (`tests/`, ~3,700 lines, 305 tests)

| File | Tests | Focus |
|------|-------|-------|
| `test_frontmatter.py` | 22 | YAML parsing edge cases |
| `test_markdown_chunker.py` | 35 | Full markdown pipeline: parse → chunk |
| `test_eip_refs.py` | 30 | EIP reference regex |
| `test_enrichment.py` | 43 | Forum + code enrichment |
| `test_incremental.py` | 29 | State DB, change detection |
| `test_document_builder.py` | 29 | Meili document conversion |
| `test_graph_store.py` | 58 | Graph CRUD, traversal, idempotency |
| `test_treesitter_parsers.py` | 39 | Python/Go/Rust AST extraction |
| `test_code_chunker.py` | 20 | Code chunk split/group |

### Config and scripts

| File | Purpose |
|------|---------|
| `config/indexer.toml` | All configuration: Meili, paths, chunk sizing, repos, sources |
| `pyproject.toml` | Package metadata, dependencies, ruff/pytest config |
| `scripts/index_meili.sh` | Convenience wrapper for `erd-index sync` |
| `.gitignore` | Ignores data/, .venv/, corpus/, raw/ |

### External artifacts

| File | Purpose |
|------|---------|
| `~/.claude/skills/erd-search/SKILL.md` | Claude Code search skill (replaces QMD for search) |
| `~/Library/LaunchAgents/com.meilisearch.plist` | Auto-start Meilisearch |
| `~/Library/LaunchAgents/com.erd-index.sync.plist` | Hourly sync cron |
| `~/.local/bin/erd-index-sync.sh` | Sync script for launchd |
