-- Incremental indexing state schema for data/index_state.db
-- Applied by erd_index.state.manifest_db.init_state_db()

PRAGMA journal_mode = WAL;

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
  chunk_ids_json  TEXT NOT NULL,
  last_indexed_at TEXT NOT NULL,
  last_error      TEXT,
  PRIMARY KEY (repository, file_path)
);

CREATE TABLE IF NOT EXISTS run_log (
  run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at      TEXT NOT NULL,
  finished_at     TEXT,
  command         TEXT NOT NULL,
  files_processed INTEGER DEFAULT 0,
  files_skipped   INTEGER DEFAULT 0,
  chunks_upserted INTEGER DEFAULT 0,
  chunks_deleted  INTEGER DEFAULT 0,
  errors          INTEGER DEFAULT 0,
  error_details   TEXT
);
