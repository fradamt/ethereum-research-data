-- Graph sidecar schema for data/graph.db
-- Applied by erd_index.graph.store.init_graph_db()

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
  chunk_id      TEXT,
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
CREATE INDEX IF NOT EXISTS idx_node_type ON node(node_type);
CREATE INDEX IF NOT EXISTS idx_node_eip ON node(eip);
CREATE INDEX IF NOT EXISTS idx_node_repo_path ON node(repository, file_path);
CREATE INDEX IF NOT EXISTS idx_node_symbol ON node(symbol_name);
CREATE INDEX IF NOT EXISTS idx_eip_dep_from ON eip_dependency_edge(from_eip, relation);
CREATE INDEX IF NOT EXISTS idx_eip_dep_to ON eip_dependency_edge(to_eip, relation);
CREATE INDEX IF NOT EXISTS idx_spec_code_eip ON spec_code_link(eip, relation);
CREATE INDEX IF NOT EXISTS idx_cross_from ON cross_reference_edge(from_node_id, relation);
CREATE INDEX IF NOT EXISTS idx_cross_to ON cross_reference_edge(to_node_id, relation);
CREATE INDEX IF NOT EXISTS idx_code_dep_from ON code_dependency_edge(from_code_node_id, relation);
