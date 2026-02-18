"""SQLite-backed incremental indexing state (index_state.db).

Tracks which files have been indexed, their content hashes, and version info
so the pipeline can skip unchanged files on subsequent runs.
"""

from __future__ import annotations

import hashlib
import logging
import sqlite3
from pathlib import Path
from typing import Any

from erd_index.settings import Settings

__all__ = [
    "compute_file_hash",
    "get_indexed_file",
    "get_stale_files",
    "init_state_db",
    "is_file_changed",
    "remove_indexed_file",
    "upsert_indexed_file",
]

log = logging.getLogger(__name__)

# Read buffer size for SHA-256 hashing (64 KiB).
_HASH_BUF_SIZE = 65_536


# ---------------------------------------------------------------------------
# Database initialization
# ---------------------------------------------------------------------------


def init_state_db(settings: Settings) -> Path:
    """Create the state database and tables if they don't exist.

    Returns the resolved database path.
    """
    db_path = settings.resolved_state_db
    db_path.parent.mkdir(parents=True, exist_ok=True)

    schema_file = Path(__file__).parent / "schema.sql"
    schema_sql = schema_file.read_text()

    con = sqlite3.connect(db_path)
    try:
        con.executescript(schema_sql)
    finally:
        con.close()

    log.info("State DB ready: %s", db_path)
    return db_path


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


def _connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def get_indexed_file(
    db_path: Path,
    repository: str,
    file_path: str,
) -> dict[str, Any] | None:
    """Return the indexed_file row as a dict, or None if not present."""
    con = _connect(db_path)
    try:
        row = con.execute(
            "SELECT * FROM indexed_file WHERE repository = ? AND file_path = ?",
            (repository, file_path),
        ).fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def is_file_changed(
    db_path: Path,
    repository: str,
    file_path: str,
    size_bytes: int,
    mtime_ns: int,
    parser_version: str,
    chunker_version: str,
) -> bool:
    """Determine whether a file needs re-indexing.

    Fast path: if (mtime_ns, size_bytes) match and versions match, skip.
    This avoids reading and hashing file contents for unchanged files.
    """
    row = get_indexed_file(db_path, repository, file_path)
    if row is None:
        return True  # new file

    if row["parser_version"] != parser_version or row["chunker_version"] != chunker_version:
        return True  # version bump forces reprocessing

    if row["mtime_ns"] != mtime_ns or row["size_bytes"] != size_bytes:
        return True  # stat changed

    return False


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------


def upsert_indexed_file(
    db_path: Path,
    *,
    repository: str,
    file_path: str,
    source_name: str,
    language: str,
    size_bytes: int,
    mtime_ns: int,
    file_hash: str,
    parser_version: str,
    chunker_version: str,
    chunk_ids_json: str = "[]",
    last_error: str | None = None,
) -> None:
    """Insert or update an indexed_file row after successful processing."""
    con = _connect(db_path)
    try:
        con.execute(
            """INSERT INTO indexed_file
                   (repository, file_path, source_name, language,
                    size_bytes, mtime_ns, file_hash,
                    parser_version, chunker_version,
                    chunk_ids_json, last_indexed_at, last_error)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)
               ON CONFLICT (repository, file_path) DO UPDATE SET
                    source_name     = excluded.source_name,
                    language        = excluded.language,
                    size_bytes      = excluded.size_bytes,
                    mtime_ns        = excluded.mtime_ns,
                    file_hash       = excluded.file_hash,
                    parser_version  = excluded.parser_version,
                    chunker_version = excluded.chunker_version,
                    chunk_ids_json  = excluded.chunk_ids_json,
                    last_indexed_at = excluded.last_indexed_at,
                    last_error      = excluded.last_error
            """,
            (
                repository, file_path, source_name, language,
                size_bytes, mtime_ns, file_hash,
                parser_version, chunker_version,
                chunk_ids_json, last_error,
            ),
        )
        con.commit()
    finally:
        con.close()


def remove_indexed_file(db_path: Path, repository: str, file_path: str) -> None:
    """Remove a file's manifest row (e.g. when the file is deleted from disk)."""
    con = _connect(db_path)
    try:
        con.execute(
            "DELETE FROM indexed_file WHERE repository = ? AND file_path = ?",
            (repository, file_path),
        )
        con.commit()
    finally:
        con.close()


def get_stale_files(
    db_path: Path,
    repository: str,
    current_paths: set[str],
) -> list[dict[str, Any]]:
    """Return indexed_file rows for files that no longer exist on disk.

    *current_paths* is the set of relative paths currently discovered for
    the given repository/source.
    """
    con = _connect(db_path)
    try:
        rows = con.execute(
            "SELECT * FROM indexed_file WHERE repository = ?",
            (repository,),
        ).fetchall()
        return [dict(r) for r in rows if r["file_path"] not in current_paths]
    finally:
        con.close()


def get_all_repositories(db_path: Path) -> list[str]:
    """Return all distinct repository names in the manifest."""
    con = _connect(db_path)
    try:
        rows = con.execute(
            "SELECT DISTINCT repository FROM indexed_file"
        ).fetchall()
        return [r["repository"] for r in rows]
    finally:
        con.close()


# ---------------------------------------------------------------------------
# File hashing
# ---------------------------------------------------------------------------


def compute_file_hash(path: Path) -> str:
    """Return the hex SHA-256 digest of a file's contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            buf = f.read(_HASH_BUF_SIZE)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()
