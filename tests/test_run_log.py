"""Tests for erd_index/state/run_log.py — run-log diagnostics."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from erd_index.state.manifest_db import init_state_db
from erd_index.state.run_log import finish_run, get_recent_runs, start_run

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_settings(tmp_path: Path):
    """Build a minimal Settings pointing at tmp_path."""
    from unittest.mock import MagicMock

    from erd_index.settings import Settings

    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    return Settings(
        meili=MagicMock(),
        corpus_dir=str(tmp_path / "corpus"),
        data_dir=str(data_dir),
        graph_db=str(data_dir / "graph.db"),
        state_db=str(data_dir / "index_state.db"),
        project_root=tmp_path,
    )


def _init_db(tmp_path: Path) -> Path:
    """Initialise the state DB and return its path."""
    settings = _make_settings(tmp_path)
    return init_state_db(settings)


# ---------------------------------------------------------------------------
# start_run
# ---------------------------------------------------------------------------


class TestStartRun:
    def test_returns_positive_integer(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "sync_all")
        assert isinstance(run_id, int)
        assert run_id >= 1

    def test_creates_row_with_correct_fields(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "ingest_markdown")

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT * FROM run_log WHERE run_id = ?", (run_id,)).fetchone()
        con.close()

        assert row is not None
        assert row["command"] == "ingest_markdown"
        assert row["started_at"] is not None
        assert row["finished_at"] is None
        assert row["files_processed"] == 0
        assert row["chunks_upserted"] == 0
        assert row["errors"] == 0
        assert row["error_details"] is None

    def test_sequential_ids_increment(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        id1 = start_run(db, "run_a")
        id2 = start_run(db, "run_b")
        id3 = start_run(db, "run_c")

        assert id1 < id2 < id3


# ---------------------------------------------------------------------------
# finish_run
# ---------------------------------------------------------------------------


class TestFinishRun:
    def test_updates_row_with_stats(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "sync_all")

        finish_run(
            db,
            run_id,
            files_processed=100,
            files_skipped=5,
            chunks_upserted=800,
            chunks_deleted=20,
            errors=2,
            error_details=["file1.md: parse error", "file2.md: timeout"],
        )

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT * FROM run_log WHERE run_id = ?", (run_id,)).fetchone()
        con.close()

        assert row["finished_at"] is not None
        assert row["files_processed"] == 100
        assert row["files_skipped"] == 5
        assert row["chunks_upserted"] == 800
        assert row["chunks_deleted"] == 20
        assert row["errors"] == 2

        details = json.loads(row["error_details"])
        assert len(details) == 2
        assert "file1.md" in details[0]

    def test_finished_at_is_set(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "build_graph")
        finish_run(db, run_id, files_processed=10)

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT * FROM run_log WHERE run_id = ?", (run_id,)).fetchone()
        con.close()

        assert row["finished_at"] is not None
        assert row["started_at"] != row["finished_at"] or row["started_at"] is not None

    def test_no_error_details_stores_null(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "ingest_code")
        finish_run(db, run_id, files_processed=50)

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT * FROM run_log WHERE run_id = ?", (run_id,)).fetchone()
        con.close()

        assert row["error_details"] is None

    def test_empty_error_details_list_stores_null(self, tmp_path: Path) -> None:
        """An empty list for error_details stores NULL (not '[]')."""
        db = _init_db(tmp_path)
        run_id = start_run(db, "ingest_code")
        # error_details=[] is falsy, so the code stores None
        finish_run(db, run_id, error_details=[])

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT * FROM run_log WHERE run_id = ?", (run_id,)).fetchone()
        con.close()

        assert row["error_details"] is None

    def test_defaults_to_zero_stats(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "test")
        finish_run(db, run_id)

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT * FROM run_log WHERE run_id = ?", (run_id,)).fetchone()
        con.close()

        assert row["files_processed"] == 0
        assert row["files_skipped"] == 0
        assert row["chunks_upserted"] == 0
        assert row["chunks_deleted"] == 0
        assert row["errors"] == 0


# ---------------------------------------------------------------------------
# get_recent_runs
# ---------------------------------------------------------------------------


class TestGetRecentRuns:
    def test_returns_runs_in_reverse_chronological_order(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        id1 = start_run(db, "first")
        id2 = start_run(db, "second")
        id3 = start_run(db, "third")

        runs = get_recent_runs(db, limit=10)

        assert len(runs) == 3
        assert runs[0]["run_id"] == id3
        assert runs[1]["run_id"] == id2
        assert runs[2]["run_id"] == id1

    def test_limit_parameter_respected(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        for i in range(5):
            start_run(db, f"run_{i}")

        runs = get_recent_runs(db, limit=2)

        assert len(runs) == 2

    def test_returns_dicts_not_rows(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        start_run(db, "test")

        runs = get_recent_runs(db)

        assert isinstance(runs, list)
        assert isinstance(runs[0], dict)
        assert "run_id" in runs[0]
        assert "command" in runs[0]
        assert "started_at" in runs[0]

    def test_empty_database_returns_empty_list(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        runs = get_recent_runs(db)
        assert runs == []

    def test_finished_and_unfinished_both_returned(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        id1 = start_run(db, "finished_run")
        finish_run(db, id1, files_processed=10)
        start_run(db, "still_running")

        runs = get_recent_runs(db)

        assert len(runs) == 2
        # Most recent is the unfinished one
        assert runs[0]["finished_at"] is None
        # Older one is finished
        assert runs[1]["finished_at"] is not None


# ---------------------------------------------------------------------------
# Multiple runs tracked correctly
# ---------------------------------------------------------------------------


class TestMultipleRuns:
    def test_each_run_has_independent_stats(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)

        id1 = start_run(db, "run_a")
        finish_run(db, id1, files_processed=10, chunks_upserted=100)

        id2 = start_run(db, "run_b")
        finish_run(db, id2, files_processed=20, chunks_upserted=200, errors=3)

        runs = get_recent_runs(db)

        run_b = runs[0]
        run_a = runs[1]

        assert run_a["files_processed"] == 10
        assert run_a["chunks_upserted"] == 100
        assert run_a["errors"] == 0

        assert run_b["files_processed"] == 20
        assert run_b["chunks_upserted"] == 200
        assert run_b["errors"] == 3

    def test_error_details_stored_and_retrieved(self, tmp_path: Path) -> None:
        db = _init_db(tmp_path)
        run_id = start_run(db, "failing_run")
        details = [
            "corpus/ethresearch/123-topic.md: UnicodeDecodeError",
            "corpus/eips/eip-999.md: KeyError: 'title'",
            "code/geth/core/vm.go: tree-sitter parse failure",
        ]
        finish_run(db, run_id, errors=3, error_details=details)

        runs = get_recent_runs(db, limit=1)
        stored_details = json.loads(runs[0]["error_details"])

        assert stored_details == details
        assert len(stored_details) == 3
        assert "UnicodeDecodeError" in stored_details[0]
