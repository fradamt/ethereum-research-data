# Search & Indexing Architecture

Replace QMD with Meilisearch + a custom Python ingestion pipeline. Add code
indexing (Python, Go, Rust) alongside the existing markdown corpus. Use SQLite
as a graph sidecar for dependency edges and cross-references.

**Design informed by**: reading the full source of raulk's `eth-protocol-expert`
(PostgreSQL + pgvector + FalkorDB agentic RAG system) and adapting the best
ideas to a simpler, local-first stack.

---

## Table of Contents

1. [Meilisearch Document Schema](#1-meilisearch-document-schema)
2. [Python Module Structure](#2-python-module-structure)
3. [Tree-sitter Chunking Strategy](#3-tree-sitter-chunking-strategy)
4. [SQLite Graph Schema](#4-sqlite-graph-schema)
5. [Lessons from eth-protocol-expert](#5-lessons-from-eth-protocol-expert)
6. [Architecture Recommendations](#6-architecture-recommendations)
7. [Embedding Architecture](#7-embedding-architecture)

---

## 1. Meilisearch Document Schema

One primary index: `eth_chunks_v1` with alias `eth_chunks_current` for
zero-downtime reindexing swaps.

### 1.1 Core fields (all chunk types)

| Field | Type | Searchable | Filterable | Sortable | Notes |
|-------|------|:----------:|:----------:|:--------:|-------|
| `id` | string | | | | Primary key. Deterministic content hash. |
| `doc_id` | string | | yes | | Parent document. `forum:ethresearch:1000`, `eip:4844`, `code:go-ethereum:core/vm/interpreter.go` |
| `node_id` | string | | yes | | Join key into `graph.db` node table |
| `schema_version` | int | | yes | | Increment when schema changes |
| `source_kind` | string | | yes | | `forum`, `eip`, `code` |
| `chunk_kind` | string | yes | yes | | `md_heading`, `md_reply`, `eip_section`, `code_function`, `code_struct`, `code_group` |
| `source_name` | string | yes | yes | | `ethresearch`, `magicians`, `eips`, `go-ethereum`, `execution-specs`, `lighthouse` |
| `repository` | string | yes | yes | | Code repo logical name |
| `language` | string | yes | yes | | `markdown`, `python`, `go`, `rust` |
| `path` | string | yes | yes | | Repo-relative file path |
| `url` | string | yes | | | Original canonical URL if available |
| `title` | string | yes | | | Thread/EIP/file title |
| `heading_path` | string[] | yes | yes | | Markdown heading ancestry (`["Specification", "Gas costs"]`) |
| `text` | string | yes | | | Main chunk body |
| `summary` | string | yes | | | Optional concise summary |
| `tags` | string[] | yes | yes | | Frontmatter tags |
| `mentions_eips` | int[] | yes | yes | | Regex-extracted EIP references |
| `start_line` | int | | yes | yes | Source span start |
| `end_line` | int | | yes | yes | Source span end |
| `source_date` | string | | yes | | ISO date from frontmatter |
| `source_date_ts` | int | | | yes | Unix timestamp for sorting |
| `indexed_at_ts` | int | | | yes | Ingestion timestamp |
| `content_hash` | string | | yes | | SHA-256 of normalized chunk text |
| `dedupe_key` | string | | yes | | Stable duplicate suppression key |

### 1.2 Type-specific fields

**Forum chunks** (`source_kind = "forum"`):

| Field | Searchable | Filterable | Sortable | Notes |
|-------|:----------:|:----------:|:--------:|-------|
| `topic_id` | | yes | | Discourse topic id |
| `post_number` | | yes | | 1 for OP, >=2 for replies |
| `author` | yes | yes | | Enables `author = "vbuterin"` |
| `category` | yes | yes | | e.g. `Sharding` |
| `research_thread` | yes | yes | | Enrichment field |
| `views` | | | yes | |
| `likes` | | | yes | |
| `posts_count` | | yes | | |
| `influence_score` | | | yes | |

**EIP chunks** (`source_kind = "eip"`):

| Field | Searchable | Filterable | Notes |
|-------|:----------:|:----------:|-------|
| `eip` | yes | yes | EIP number as int |
| `eip_status` | yes | yes | `Draft`, `Final`, `Living`, etc. |
| `eip_type` | yes | yes | `Core`, `ERC`, `Meta`, etc. |
| `eip_category` | yes | yes | Frontmatter `category` |
| `requires_eips` | | yes | Parsed from frontmatter |
| `supersedes_eips` | | yes | |
| `replaces_eips` | | yes | |

**Code chunks** (`source_kind = "code"`):

| Field | Searchable | Filterable | Notes |
|-------|:----------:|:----------:|-------|
| `symbol_id` | | yes | Stable symbol key |
| `symbol_name` | yes | yes | Function/type name |
| `symbol_kind` | yes | yes | `function`, `method`, `struct`, etc. |
| `symbol_qualname` | yes | yes | `pkg.Type.Method` |
| `signature` | yes | | Header/signature text |
| `parent_symbol` | yes | yes | Enclosing class/impl/trait |
| `module_path` | yes | yes | Module/package path |
| `visibility` | | yes | `public`, `private`, etc. |
| `imports` | yes | yes | File-level imports |
| `used_imports` | yes | yes | Imports used in this chunk |
| `calls` | yes | yes | Called symbols (heuristic) |

### 1.3 Index settings

```json
{
  "searchableAttributes": [
    "title",
    "symbol_name",
    "symbol_qualname",
    "signature",
    "heading_path",
    "text",
    "summary",
    "tags",
    "category",
    "author",
    "module_path",
    "path"
  ],
  "filterableAttributes": [
    "schema_version", "source_kind", "chunk_kind", "source_name",
    "repository", "language", "doc_id", "node_id", "path",
    "topic_id", "post_number", "author", "category", "research_thread",
    "tags", "mentions_eips",
    "eip", "eip_status", "eip_type", "eip_category",
    "requires_eips", "supersedes_eips", "replaces_eips",
    "symbol_id", "symbol_name", "symbol_kind", "symbol_qualname",
    "parent_symbol", "module_path", "visibility",
    "imports", "used_imports",
    "content_hash", "dedupe_key"
  ],
  "sortableAttributes": [
    "source_date_ts", "indexed_at_ts", "influence_score",
    "views", "likes", "eip", "start_line"
  ],
  "distinctAttribute": "dedupe_key"
}
```

### 1.4 Example queries this enables

- **All EIP-4844 related content**: `eip = 4844 OR mentions_eips = 4844`
- **All Go functions in go-ethereum**: `source_kind = "code" AND repository = "go-ethereum" AND language = "go" AND chunk_kind = "code_function"`
- **Posts by vbuterin about sharding**: `source_kind = "forum" AND author = "vbuterin" AND (category = "Sharding" OR research_thread = "sharding")`
- **All Core EIPs in Final status**: `eip_type = "Core" AND eip_status = "Final"`
- **Code that references EIP-1559**: `source_kind = "code" AND mentions_eips = 1559`

---

## 2. Python Module Structure

The existing `scraper/` and `converter/` packages remain stdlib-only and
unchanged. The indexing pipeline is a separate uv-managed package (`erd_index/`)
with external dependencies.

### 2.1 Directory layout

```
ethereum-research-data/
  pyproject.toml              # NEW - uv-managed, covers erd_index/ only
  uv.lock                     # NEW - lockfile
  config/
    indexer.toml              # NEW - stable configuration
  erd_index/                  # NEW - indexing pipeline package
    __init__.py
    __main__.py               # python -m erd_index
    cli.py                    # argparse CLI (erd-index command)
    settings.py               # Config loading (TOML + env + CLI)
    models.py                 # Pydantic models for chunks, documents
    discover/
      __init__.py
      file_walker.py          # Walk corpus/ and code repos, yield files
      language_detector.py    # Extension -> language mapping
    parse/
      __init__.py
      frontmatter.py          # YAML frontmatter extraction
      markdown_parser.py      # Heading-based markdown parsing
      treesitter_runtime.py   # Shared tree-sitter init, language loading
      py_parser.py            # Python AST extraction via tree-sitter
      go_parser.py            # Go AST extraction via tree-sitter
      rust_parser.py          # Rust AST extraction via tree-sitter
    chunk/
      __init__.py
      markdown_chunker.py     # Heading-based + reply-aware chunking
      code_chunker.py         # Function/struct-level code chunking
      split_large_units.py    # Split oversized code units at AST boundaries
      group_small_units.py    # Group contiguous small functions
    enrich/
      __init__.py
      eip_refs.py             # Extract EIP references from any text
      forum_metadata.py       # Forum-specific metadata (influence, thread)
      code_metadata.py        # Symbol qualification, visibility, calls
      dependency_extractor.py # Import-to-usage dependency analysis
    index/
      __init__.py
      meili_client.py         # Meilisearch connection, index management
      meili_schema.py         # Index settings, schema version
      document_builder.py     # Convert chunks -> Meili documents
      writer.py               # Batch upsert/delete to Meilisearch
    graph/
      __init__.py
      schema.sql              # SQLite DDL (graph.db)
      store.py                # SQLite connection, CRUD operations
      node_builder.py         # Build graph nodes from chunks
      edge_builder.py         # Build edges (EIP deps, spec-code, xrefs)
    state/
      __init__.py
      manifest_db.py          # Incremental indexing state (index_state.db)
      run_log.py              # Run history and error tracking
  data/                       # NEW - runtime data (gitignored)
    graph.db                  # SQLite graph sidecar
    index_state.db            # Incremental indexing manifest
  tests/                      # NEW - test suite
    conftest.py
    fixtures/                 # Sample .md, .py, .go, .rs files
    test_frontmatter.py
    test_markdown_chunker.py
    test_code_chunker.py
    test_treesitter_parsers.py
    test_eip_refs.py
    test_graph_store.py
    test_document_builder.py
    test_incremental.py
  scripts/
    index_meili.sh            # NEW - convenience wrapper for full reindex

  # Unchanged existing packages:
  scraper/
  converter/
  corpus/
  raw/
  sources.json
```

### 2.2 pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "ethereum-research-data-indexer"
version = "0.1.0"
requires-python = ">=3.10"
description = "Meilisearch indexer for Ethereum research data corpus"
dependencies = [
  "meilisearch>=0.34,<1.0",
  "pydantic>=2.7,<3.0",
  "PyYAML>=6.0,<7.0",
  "tree-sitter>=0.22,<0.24",
  "tree-sitter-python>=0.23,<0.24",
  "tree-sitter-go>=0.23,<0.24",
  "tree-sitter-rust>=0.23,<0.23.3",
  "orjson>=3.10,<4.0",
  "tokenizers>=0.22.2",
  "tomli>=2.0; python_version < '3.11'",
]

[project.scripts]
erd-index = "erd_index.cli:main"
eth-search = "erd_index.search_cli:main"

[tool.hatch.build.targets.wheel]
packages = ["erd_index"]

[dependency-groups]
dev = [
  "pytest>=8.0",
  "pytest-cov>=5.0",
  "ruff>=0.6",
  "mypy>=1.10",
  "types-PyYAML>=6.0",
]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "RUF"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["erd_index"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### 2.3 CLI commands

```bash
# CLIs are installed globally via: uv tool install -e .

# Primary indexer workflow (recommended)
erd-index init
erd-index sync                    # incremental (changed files only)
erd-index sync --full-rebuild     # full reprocess
erd-index stats
erd-index stats --repo go-ethereum

# Granular indexer commands
erd-index ingest-md
erd-index ingest-md --changed-only
erd-index ingest-code --repo go-ethereum
erd-index ingest-code --repo go-ethereum --changed-only
erd-index build-graph
erd-index build-graph --changed-only
erd-index link-specs

# Search CLI
eth-search query "proposer boost"
eth-search query "how does proposer boost work" --hybrid
eth-search query "blob gas" --source-kind eip
eth-search query "attestation" --include-code
eth-search stats
```

---

## 3. Tree-sitter Chunking Strategy

### 3.1 AST extraction targets per language

| Language | Primary unit nodes | Container/context nodes | Import nodes |
|----------|-------------------|------------------------|-------------|
| **Python** | `function_definition`, `decorated_definition`, `class_definition` | `class_definition` (parent), module docstring, decorators | `import_statement`, `import_from_statement` |
| **Go** | `function_declaration`, `method_declaration`, `type_spec` + `struct_type` | receiver type, `package_clause`, comments | `import_declaration` |
| **Rust** | `function_item`, `struct_item`, `enum_item`, `trait_item`, `impl_item` | enclosing `impl_item` / `trait_item`, doc attrs | `use_declaration` |

### 3.2 Chunk sizing policy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `target_chars` | 2800 | ~700 tokens. Good for BM25 granularity. |
| `hard_max_chars` | 5500 | ~1400 tokens. Beyond this, split. |
| `small_fn_max_lines` | 12 | Candidates for grouping |
| `small_fn_max_chars` | 450 | Candidates for grouping |
| `small_group_target_chars` | 2200 | Target size for grouped chunks |
| `small_group_max_members` | 6 | Max functions per group |

### 3.3 Large-function handling

1. If unit size <= `hard_max_chars`: index as one `code_function` chunk.
2. If unit size > `hard_max_chars`: split at **top-level statement AST
   boundaries** within the function body (not fixed line windows).
3. Each split part preserves:
   - Full function signature/header
   - Doc comment/docstring
   - Enclosing class/impl/receiver context
   - Subset of imports actually used in that part
4. Split parts get `chunk_kind = "code_function"` with `part_index` and
   `part_count` in metadata.
5. Fallback (if AST splitting fails): line-window split with
   `overlap_lines = 8`.

### 3.4 Small-function grouping

1. Functions <= `small_fn_max_chars` and <= `small_fn_max_lines` are
   candidates for grouping.
2. Group only contiguous functions sharing the same parent container
   (same class, same `impl` block, or same module-level scope).
3. Grouping creates one `code_group` chunk in Meilisearch with a
   `member_symbols` array listing each function name.
4. Each individual function is still emitted as a graph node with its own
   `node_id`, pointing to the group chunk via `chunk_id`.
5. This keeps search results contextually rich without losing symbol-level
   graph resolution.

### 3.5 Context preserved per code chunk

Every code chunk includes:
- `imports`: all file-level imports
- `used_imports`: subset of imports referenced in this chunk's body
- `module_path`: Python module path, Go package, Rust crate::module
- `parent_symbol`: enclosing class/struct/impl name (if any)
- `signature`: function signature or type definition header
- Doc comment / docstring
- `start_line`, `end_line`: source span
- `calls`: heuristically-extracted called symbol names
- `mentions_eips`: EIP references found in comments/strings

---

## 4. SQLite Graph Schema

File: `erd_index/graph/schema.sql` -- applied to `data/graph.db`.

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- Nodes: every indexable entity gets a node
CREATE TABLE IF NOT EXISTS node (
  node_id       TEXT PRIMARY KEY,
  node_type     TEXT NOT NULL CHECK (node_type IN (
    'forum_topic', 'forum_post', 'eip', 'eip_section',
    'code_function', 'code_struct', 'code_enum',
    'code_trait', 'code_impl', 'code_class'
  )),
  source_name   TEXT NOT NULL,
  repository    TEXT,
  language      TEXT,
  file_path     TEXT,
  chunk_id      TEXT,             -- join key to Meilisearch document id
  title         TEXT,
  url           TEXT,
  eip           INTEGER,
  section_anchor TEXT,
  symbol_name   TEXT,
  symbol_kind   TEXT,
  start_line    INTEGER,
  end_line      INTEGER,
  content_hash  TEXT NOT NULL,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- EIP dependency edges (from frontmatter)
CREATE TABLE IF NOT EXISTS eip_dependency_edge (
  edge_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  from_eip       INTEGER NOT NULL,
  to_eip         INTEGER NOT NULL,
  relation       TEXT NOT NULL CHECK (relation IN (
    'requires', 'supersedes', 'replaces'
  )),
  source_node_id TEXT NOT NULL REFERENCES node(node_id) ON DELETE CASCADE,
  confidence     REAL NOT NULL DEFAULT 1.0
                   CHECK (confidence >= 0 AND confidence <= 1),
  evidence_text  TEXT,
  extractor      TEXT NOT NULL DEFAULT 'frontmatter',
  created_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (from_eip, to_eip, relation, source_node_id)
);

-- Spec-to-code implementation links
CREATE TABLE IF NOT EXISTS spec_code_link (
  link_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  eip                INTEGER NOT NULL,
  eip_section_anchor TEXT,
  eip_node_id        TEXT REFERENCES node(node_id) ON DELETE SET NULL,
  code_node_id       TEXT NOT NULL REFERENCES node(node_id) ON DELETE CASCADE,
  relation           TEXT NOT NULL CHECK (relation IN (
    'implements', 'partial_implements', 'tests', 'references'
  )),
  match_method       TEXT NOT NULL CHECK (match_method IN (
    'heuristic', 'llm', 'manual'
  )),
  confidence         REAL NOT NULL
                       CHECK (confidence >= 0 AND confidence <= 1),
  evidence_json      TEXT NOT NULL DEFAULT '{}',
  created_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (eip, eip_section_anchor, code_node_id, relation)
);

-- Cross-references between any documents
CREATE TABLE IF NOT EXISTS cross_reference_edge (
  edge_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  from_node_id  TEXT NOT NULL REFERENCES node(node_id) ON DELETE CASCADE,
  to_node_id    TEXT NOT NULL REFERENCES node(node_id) ON DELETE CASCADE,
  relation      TEXT NOT NULL CHECK (relation IN (
    'mentions_eip', 'mentions_section', 'discusses', 'references'
  )),
  span_start    INTEGER,
  span_end      INTEGER,
  anchor_text   TEXT,
  confidence    REAL NOT NULL DEFAULT 1.0
                  CHECK (confidence >= 0 AND confidence <= 1),
  extractor     TEXT NOT NULL,
  created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (from_node_id, to_node_id, relation, span_start, span_end)
);

-- Code-level dependency edges (function calls, type usage, imports)
CREATE TABLE IF NOT EXISTS code_dependency_edge (
  edge_id             INTEGER PRIMARY KEY AUTOINCREMENT,
  from_code_node_id   TEXT NOT NULL REFERENCES node(node_id) ON DELETE CASCADE,
  to_code_node_id     TEXT REFERENCES node(node_id) ON DELETE CASCADE,
  to_external_symbol  TEXT,
  relation            TEXT NOT NULL CHECK (relation IN (
    'calls', 'uses_type', 'imports', 'implements_trait'
  )),
  confidence          REAL NOT NULL DEFAULT 0.7
                        CHECK (confidence >= 0 AND confidence <= 1),
  extractor           TEXT NOT NULL DEFAULT 'tree_sitter',
  evidence_text       TEXT,
  created_at          TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (to_code_node_id IS NOT NULL OR to_external_symbol IS NOT NULL),
  UNIQUE (from_code_node_id, to_code_node_id, to_external_symbol, relation)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_node_type
  ON node(node_type);
CREATE INDEX IF NOT EXISTS idx_node_eip
  ON node(eip);
CREATE INDEX IF NOT EXISTS idx_node_repo_path
  ON node(repository, file_path);
CREATE INDEX IF NOT EXISTS idx_node_symbol
  ON node(symbol_name);
CREATE INDEX IF NOT EXISTS idx_eip_dep_from
  ON eip_dependency_edge(from_eip, relation);
CREATE INDEX IF NOT EXISTS idx_eip_dep_to
  ON eip_dependency_edge(to_eip, relation);
CREATE INDEX IF NOT EXISTS idx_spec_code_eip
  ON spec_code_link(eip, relation);
CREATE INDEX IF NOT EXISTS idx_cross_from
  ON cross_reference_edge(from_node_id, relation);
CREATE INDEX IF NOT EXISTS idx_cross_to
  ON cross_reference_edge(to_node_id, relation);
CREATE INDEX IF NOT EXISTS idx_code_dep_from
  ON code_dependency_edge(from_code_node_id, relation);
```

### 4.1 Incremental indexing state (separate DB)

File: `data/index_state.db`

```sql
CREATE TABLE IF NOT EXISTS indexed_file (
  repository      TEXT NOT NULL,
  file_path       TEXT NOT NULL,
  source_name     TEXT NOT NULL,
  language        TEXT NOT NULL,
  size_bytes      INTEGER NOT NULL,
  mtime_ns        INTEGER NOT NULL,
  file_hash       TEXT NOT NULL,
  parser_version  TEXT NOT NULL,
  chunker_version TEXT NOT NULL,
  chunk_ids_json  TEXT NOT NULL,     -- JSON array of chunk IDs produced
  last_indexed_at TEXT NOT NULL,
  last_error      TEXT,
  PRIMARY KEY (repository, file_path)
);
```

---

## 5. Lessons from eth-protocol-expert

| What they did | Decision | What we do |
|--------------|----------|-----------|
| Function-level chunking with header retention on split | **Keep** | `code_chunker.py` preserves full signature + docstring + enclosing context for every split part |
| Content-hash chunk IDs (SHA-256) | **Keep** | `id` and `content_hash` are deterministic. Enables dedup, incremental diffing, and stable MCP references. |
| Go and Rust tree-sitter queries | **Keep + extend** | Reuse the query patterns. Add Python parser. Normalize metadata to flat Meilisearch fields instead of nested structs. |
| Dependency extraction from function body + imports | **Keep + tighten** | Emit typed edges in `code_dependency_edge` with confidence scores and `extractor` provenance. |
| Section-aware EIP chunking (`SectionChunker`) | **Adapt** | Generic heading-based markdown chunker that works for all `.md` files (not EIP-specific). Forum reply boundaries still respected. |
| Fixed-token chunking with tiktoken (`FixedChunker`) | **Drop** | Use character + AST-boundary sizing. No tokenizer dependency. Meilisearch handles its own tokenization. |
| Forum chunker preserving reply boundaries | **Keep** | `md_reply` chunk kind with post metadata (author, post_number, reply_to). |
| LLM-based spec-impl linker (Anthropic API) | **Defer** | Phase 1 uses heuristic keyword matching only. Optional `--enable-llm-linker` flag for later. |
| FalkorDB graph store (Cypher queries) | **Replace** | SQLite with WAL mode. Same two-pass build (nodes, then edges). Simpler deployment, no extra service. |
| pgvector for embedding storage | **Replace** | Meilisearch for primary retrieval (BM25). Embeddings only for optional reranking, not stored in the index. |
| Two-pass graph build (nodes first, relationships second) | **Keep** | Pass 1: upsert nodes. Pass 2: upsert edges. Idempotent via UNIQUE constraints. |
| `tree-sitter-languages` package (pinned <0.22.0) | **Replace** | Use individual `tree-sitter-python`, `tree-sitter-go`, `tree-sitter-rust` packages with `tree-sitter>=0.22`. The `tree-sitter-languages` bundle is deprecated. |

---

## 6. Architecture Recommendations

### 6.1 Incremental indexing flow

```
1. Walk configured roots (corpus/ + code repos)
2. For each file, compare (mtime_ns, size_bytes) against index_state.db
     -> Skip if unchanged and parser_version + chunker_version match
3. Hash only the candidates that changed
4. Re-chunk changed/new files
5. Upsert new chunks to Meilisearch (batch of 1000)
6. Delete stale chunk IDs for modified/deleted files
7. Rebuild graph nodes/edges only for touched files
8. Commit manifest row updates only after Meili task succeeds
9. Run weekly --full-rebuild safety job to catch drift
```

The `--changed-only` flag (default for `sync`) follows this flow. The
`--full-rebuild` flag skips step 2 and reprocesses everything.

### 6.2 Search CLI

`erd_index/search_cli.py` provides the `eth-search` command for querying the
Meilisearch index from the terminal or scripts.

| Subcommand | Description |
|------------|-------------|
| `query` | Keyword or hybrid search with filter syntax |
| `stats` | Index statistics (document counts, embedder status) |
| `apply-terminology` | Push synonym/dictionary config to Meilisearch |

Guidelines:
- `query` uses a **read-only** search API key (`~/.config/erd/search-key`).
- `stats` uses the admin key (`~/.config/erd/admin-key`).
- `--hybrid` enables semantic search (default ratio 0.5).
- `--distinct doc_id` is on by default to deduplicate chunks per document.

### 6.3 Configuration approach

**In `config/indexer.toml`** (stable, version-controlled):
- Corpus directory path
- Code repo roots and logical names
- Database file paths (`data/graph.db`, `data/index_state.db`)
- Meilisearch endpoint and index name
- Chunk sizing thresholds
- Parser/chunker version strings
- Source include/exclude globs

**As CLI flags** (per-run):
- Run mode: `--changed-only`, `--full-rebuild`, `--dry-run`
- Source scope: `--repo <name>`, `--source-name <name>`
- Operational: `--batch-size`, `--max-files`, `--verbose`
- Optional features: `--enable-llm-linker`

**Precedence**: CLI > environment variables > config file defaults.

### 6.4 Testing strategy

| Category | Location | What it tests |
|----------|----------|---------------|
| **Unit** | `tests/test_frontmatter.py` | YAML frontmatter extraction from all corpus types |
| **Unit** | `tests/test_markdown_chunker.py` | Heading-based splitting, reply boundaries, code block atomicity |
| **Unit** | `tests/test_code_chunker.py` | Function splitting, small-function grouping, context preservation |
| **Unit** | `tests/test_treesitter_parsers.py` | AST extraction for Python, Go, Rust from fixture files |
| **Unit** | `tests/test_eip_refs.py` | EIP reference regex extraction from mixed content |
| **Unit** | `tests/test_graph_store.py` | SQLite CRUD, edge upsert idempotency, cascading deletes |
| **Unit** | `tests/test_document_builder.py` | Chunk -> Meilisearch document conversion, field completeness |
| **Golden** | `tests/fixtures/` | Snapshot tests: fixed input files -> expected chunk outputs |
| **Integration** | `tests/test_incremental.py` | Add/modify/delete files, verify stale chunk cleanup |
| **Smoke** | `tests/test_relevance.py` | Fixed queries (`EIP-4844`, `vbuterin sharding`, `go-ethereum blob`) with expected doc IDs in top-10 |

### 6.5 Data flow diagram

```
corpus/*.md + ~/EF/go-ethereum/**/*.go + ~/EF/execution-specs/**/*.py + ~/EF/lighthouse/**/*.rs
    |
    v
discover/file_walker.py ---- state/manifest_db.py (skip unchanged)
    |
    v
parse/ (frontmatter.py, markdown_parser.py, py/go/rust_parser.py)
    |
    v
chunk/ (markdown_chunker.py, code_chunker.py, split/group)
    |
    v
enrich/ (eip_refs.py, forum_metadata.py, code_metadata.py, dependency_extractor.py)
    |
    +-----> index/ (document_builder.py -> writer.py -> Meilisearch)
    |
    +-----> graph/ (node_builder.py + edge_builder.py -> graph.db)
    |
    +-----> state/manifest_db.py (record indexed files)
```

### 6.6 Deployment notes

- Meilisearch runs locally via `brew install meilisearch` or Docker.
  Default: `http://localhost:7700` with a master key in env.
- SQLite databases live in `data/` (gitignored). They are regeneratable
  from source files via `--full-rebuild`.
- For CI: use `--dry-run` to validate chunking without writing to Meili.

---

## 7. Embedding Architecture

### 7.1 Current runtime path

Hybrid search uses Meilisearch's built-in `rest` embedder, calling Ollama
directly. No proxy is in the active runtime path.

```
Meilisearch (embedder: source=rest)
  └── POST /api/embed ──> Ollama (:11434)
        └── model: embeddinggemma:300m (768 dims, 2048 context)
```

- Host/native URL: `http://localhost:11434/api/embed`
- Docker URL: `http://ollama:11434/api/embed`

### 7.2 Embedder configuration

After finalization, the embedder settings are:

| Setting | Value |
|---------|-------|
| `source` | `rest` |
| `model` | `embeddinggemma:300m` |
| `dimensions` | `768` |
| `url` | Ollama `/api/embed` endpoint |
| `documentTemplateMaxBytes` | `8000` |

`documentTemplate` uses title + text by default, and can be switched to the
asymmetric format (`title: ... | text: ...`) when finalizing with `--asymmetric`.

### 7.3 Initial and bulk embedding

Initial corpus embedding is done by `scripts/batch_embed.py`, which calls
Ollama directly and writes vectors via the Meilisearch API (`_vectors`):

1. Set embedder to `source: "userProvided"` (`--setup`).
2. Batch-embed existing documents and upsert vectors.
3. Switch embedder to `source: "rest"` for query-time embedding (`--finalize`).

Recommended wrapper:

```bash
./scripts/setup_hybrid.sh
./scripts/setup_hybrid.sh --docker
./scripts/setup_hybrid.sh --resume
```

### 7.4 Operational notes

- Meilisearch v1.35+ requires `--experimental-allowed-ip-networks any` so
  local Ollama calls are not blocked by SSRF protection.
- `documentTemplateMaxBytes` is explicitly configured to `8000`.
- Asymmetric prefixing is implemented: `embeddinggemma` expects
  `title: X | text: Y` for documents (via `documentTemplate`) and
  `task: search result | query: Q` for queries (added by `eth-search` CLI
  when `--hybrid` ratio >= 0.6).
- Legacy proxy code still exists at `erd_index/embed_proxy.py` but is not
  part of the active indexing or search path.
