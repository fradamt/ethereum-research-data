"""Run-log diagnostics: track indexing runs for stats and debugging."""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

__all__ = ["start_run", "finish_run", "get_recent_runs"]

log = logging.getLogger(__name__)


def _connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def start_run(db_path: Path, command: str) -> int:
    """Insert a new run_log row and return the run_id."""
    con = _connect(db_path)
    try:
        cur = con.execute(
            "INSERT INTO run_log (started_at, command) VALUES (datetime('now'), ?)",
            (command,),
        )
        con.commit()
        assert cur.lastrowid is not None
        return cur.lastrowid
    finally:
        con.close()


def finish_run(
    db_path: Path,
    run_id: int,
    *,
    files_processed: int = 0,
    files_skipped: int = 0,
    chunks_upserted: int = 0,
    chunks_deleted: int = 0,
    errors: int = 0,
    error_details: list[str] | None = None,
) -> None:
    """Update a run_log row with final stats."""
    details_json = json.dumps(error_details) if error_details else None
    con = _connect(db_path)
    try:
        con.execute(
            """UPDATE run_log SET
                   finished_at     = datetime('now'),
                   files_processed = ?,
                   files_skipped   = ?,
                   chunks_upserted = ?,
                   chunks_deleted  = ?,
                   errors          = ?,
                   error_details   = ?
               WHERE run_id = ?
            """,
            (
                files_processed, files_skipped,
                chunks_upserted, chunks_deleted,
                errors, details_json,
                run_id,
            ),
        )
        con.commit()
    finally:
        con.close()


def get_recent_runs(db_path: Path, limit: int = 10) -> list[dict[str, Any]]:
    """Return the last *limit* run_log entries, newest first."""
    con = _connect(db_path)
    try:
        rows = con.execute(
            "SELECT * FROM run_log ORDER BY run_id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        con.close()
