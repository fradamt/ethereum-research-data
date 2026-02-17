"""Incremental indexing state: file manifest, run log."""

from erd_index.state.manifest_db import (
    compute_file_hash,
    get_indexed_file,
    get_stale_files,
    init_state_db,
    is_file_changed,
    remove_indexed_file,
    upsert_indexed_file,
)
from erd_index.state.run_log import finish_run, get_recent_runs, start_run

__all__ = [
    "compute_file_hash",
    "finish_run",
    "get_indexed_file",
    "get_recent_runs",
    "get_stale_files",
    "init_state_db",
    "is_file_changed",
    "remove_indexed_file",
    "start_run",
    "upsert_indexed_file",
]
