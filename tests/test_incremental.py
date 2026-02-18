"""Tests for incremental indexing state: manifest_db and run_log."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

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

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db_path(tmp_settings) -> Path:
    """Initialize the state DB and return its path."""
    return init_state_db(tmp_settings)


# ---------------------------------------------------------------------------
# init_state_db
# ---------------------------------------------------------------------------


class TestInitStateDb:
    def test_creates_database_file(self, db_path: Path) -> None:
        assert db_path.exists()

    def test_creates_indexed_file_table(self, db_path: Path) -> None:
        import sqlite3

        con = sqlite3.connect(db_path)
        cur = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='indexed_file'"
        )
        assert cur.fetchone() is not None
        con.close()

    def test_creates_run_log_table(self, db_path: Path) -> None:
        import sqlite3

        con = sqlite3.connect(db_path)
        cur = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='run_log'"
        )
        assert cur.fetchone() is not None
        con.close()

    def test_idempotent(self, tmp_settings) -> None:
        """Calling init twice does not raise."""
        init_state_db(tmp_settings)
        init_state_db(tmp_settings)


# ---------------------------------------------------------------------------
# upsert + get roundtrip
# ---------------------------------------------------------------------------


class TestUpsertAndGet:
    def test_insert_then_get(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="test-repo",
            file_path="src/main.py",
            source_name="test",
            language="python",
            size_bytes=1024,
            mtime_ns=1000000,
            file_hash="abc123",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        row = get_indexed_file(db_path, "test-repo", "src/main.py")
        assert row is not None
        assert row["repository"] == "test-repo"
        assert row["file_path"] == "src/main.py"
        assert row["source_name"] == "test"
        assert row["language"] == "python"
        assert row["size_bytes"] == 1024
        assert row["mtime_ns"] == 1000000
        assert row["file_hash"] == "abc123"
        assert row["parser_version"] == "0.1.0"
        assert row["chunker_version"] == "0.1.0"
        assert row["last_indexed_at"] is not None

    def test_update_existing(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="repo",
            file_path="f.py",
            source_name="s",
            language="python",
            size_bytes=100,
            mtime_ns=1,
            file_hash="h1",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        upsert_indexed_file(
            db_path,
            repository="repo",
            file_path="f.py",
            source_name="s",
            language="python",
            size_bytes=200,
            mtime_ns=2,
            file_hash="h2",
            parser_version="0.2.0",
            chunker_version="0.1.0",
        )
        row = get_indexed_file(db_path, "repo", "f.py")
        assert row is not None
        assert row["size_bytes"] == 200
        assert row["mtime_ns"] == 2
        assert row["file_hash"] == "h2"
        assert row["parser_version"] == "0.2.0"

    def test_get_missing_returns_none(self, db_path: Path) -> None:
        assert get_indexed_file(db_path, "nope", "nope.py") is None

    def test_chunk_ids_and_error(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="r",
            file_path="f.py",
            source_name="s",
            language="python",
            size_bytes=50,
            mtime_ns=1,
            file_hash="h",
            parser_version="0.1.0",
            chunker_version="0.1.0",
            chunk_ids_json='["c1","c2"]',
            last_error="parse failed",
        )
        row = get_indexed_file(db_path, "r", "f.py")
        assert row is not None
        assert row["chunk_ids_json"] == '["c1","c2"]'
        assert row["last_error"] == "parse failed"


# ---------------------------------------------------------------------------
# is_file_changed
# ---------------------------------------------------------------------------


class TestIsFileChanged:
    def _insert(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="repo",
            file_path="lib.go",
            source_name="go-ethereum",
            language="go",
            size_bytes=500,
            mtime_ns=9999,
            file_hash="deadbeef",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )

    def test_new_file(self, db_path: Path) -> None:
        assert is_file_changed(db_path, "repo", "new.go", 100, 1, "0.1.0", "0.1.0")

    def test_unchanged(self, db_path: Path) -> None:
        self._insert(db_path)
        assert not is_file_changed(db_path, "repo", "lib.go", 500, 9999, "0.1.0", "0.1.0")

    def test_mtime_changed(self, db_path: Path) -> None:
        self._insert(db_path)
        assert is_file_changed(db_path, "repo", "lib.go", 500, 10000, "0.1.0", "0.1.0")

    def test_size_changed(self, db_path: Path) -> None:
        self._insert(db_path)
        assert is_file_changed(db_path, "repo", "lib.go", 501, 9999, "0.1.0", "0.1.0")

    def test_parser_version_changed(self, db_path: Path) -> None:
        self._insert(db_path)
        assert is_file_changed(db_path, "repo", "lib.go", 500, 9999, "0.2.0", "0.1.0")

    def test_chunker_version_changed(self, db_path: Path) -> None:
        self._insert(db_path)
        assert is_file_changed(db_path, "repo", "lib.go", 500, 9999, "0.1.0", "0.2.0")


# ---------------------------------------------------------------------------
# get_stale_files
# ---------------------------------------------------------------------------


class TestGetStaleFiles:
    def test_finds_deleted(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="repo",
            file_path="old.py",
            source_name="s",
            language="python",
            size_bytes=1,
            mtime_ns=1,
            file_hash="h",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        upsert_indexed_file(
            db_path,
            repository="repo",
            file_path="current.py",
            source_name="s",
            language="python",
            size_bytes=2,
            mtime_ns=2,
            file_hash="h2",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        stale = get_stale_files(db_path, "repo", {"current.py"})
        assert len(stale) == 1
        assert stale[0]["file_path"] == "old.py"

    def test_no_stale(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="repo",
            file_path="a.py",
            source_name="s",
            language="python",
            size_bytes=1,
            mtime_ns=1,
            file_hash="h",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        stale = get_stale_files(db_path, "repo", {"a.py"})
        assert stale == []

    def test_scoped_to_repository(self, db_path: Path) -> None:
        """Stale detection only considers files in the given repository."""
        upsert_indexed_file(
            db_path,
            repository="repo-a",
            file_path="f.py",
            source_name="s",
            language="python",
            size_bytes=1,
            mtime_ns=1,
            file_hash="h",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        # Ask about repo-b — should find nothing
        stale = get_stale_files(db_path, "repo-b", set())
        assert stale == []


# ---------------------------------------------------------------------------
# remove_indexed_file
# ---------------------------------------------------------------------------


class TestRemoveIndexedFile:
    def test_remove(self, db_path: Path) -> None:
        upsert_indexed_file(
            db_path,
            repository="r",
            file_path="gone.py",
            source_name="s",
            language="python",
            size_bytes=1,
            mtime_ns=1,
            file_hash="h",
            parser_version="0.1.0",
            chunker_version="0.1.0",
        )
        assert get_indexed_file(db_path, "r", "gone.py") is not None
        remove_indexed_file(db_path, "r", "gone.py")
        assert get_indexed_file(db_path, "r", "gone.py") is None

    def test_remove_nonexistent(self, db_path: Path) -> None:
        """Removing a file that doesn't exist should not raise."""
        remove_indexed_file(db_path, "r", "nope.py")


# ---------------------------------------------------------------------------
# compute_file_hash
# ---------------------------------------------------------------------------


class TestComputeFileHash:
    def test_sha256(self, tmp_path: Path) -> None:
        f = tmp_path / "test.txt"
        content = b"hello world"
        f.write_bytes(content)
        expected = hashlib.sha256(content).hexdigest()
        assert compute_file_hash(f) == expected

    def test_consistent(self, tmp_path: Path) -> None:
        f = tmp_path / "stable.txt"
        f.write_text("same content")
        h1 = compute_file_hash(f)
        h2 = compute_file_hash(f)
        assert h1 == h2

    def test_different_content(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("aaa")
        f2.write_text("bbb")
        assert compute_file_hash(f1) != compute_file_hash(f2)

    def test_empty_file(self, tmp_path: Path) -> None:
        f = tmp_path / "empty.txt"
        f.write_bytes(b"")
        expected = hashlib.sha256(b"").hexdigest()
        assert compute_file_hash(f) == expected


# ---------------------------------------------------------------------------
# Run log
# ---------------------------------------------------------------------------


class TestRunLog:
    def test_start_run(self, db_path: Path) -> None:
        run_id = start_run(db_path, "sync --changed-only")
        assert isinstance(run_id, int)
        assert run_id >= 1

    def test_finish_run(self, db_path: Path) -> None:
        run_id = start_run(db_path, "ingest-md")
        finish_run(
            db_path,
            run_id,
            files_processed=10,
            files_skipped=5,
            chunks_upserted=20,
            chunks_deleted=3,
            errors=1,
            error_details=["parse error in foo.md"],
        )
        runs = get_recent_runs(db_path, limit=1)
        assert len(runs) == 1
        r = runs[0]
        assert r["run_id"] == run_id
        assert r["command"] == "ingest-md"
        assert r["files_processed"] == 10
        assert r["files_skipped"] == 5
        assert r["chunks_upserted"] == 20
        assert r["chunks_deleted"] == 3
        assert r["errors"] == 1
        assert r["finished_at"] is not None
        assert "parse error" in r["error_details"]

    def test_get_recent_runs_ordering(self, db_path: Path) -> None:
        id1 = start_run(db_path, "run-1")
        id2 = start_run(db_path, "run-2")
        id3 = start_run(db_path, "run-3")
        runs = get_recent_runs(db_path, limit=10)
        assert len(runs) == 3
        # Newest first
        assert runs[0]["run_id"] == id3
        assert runs[1]["run_id"] == id2
        assert runs[2]["run_id"] == id1

    def test_get_recent_runs_limit(self, db_path: Path) -> None:
        for i in range(5):
            start_run(db_path, f"run-{i}")
        runs = get_recent_runs(db_path, limit=2)
        assert len(runs) == 2

    def test_unfinished_run(self, db_path: Path) -> None:
        start_run(db_path, "unfinished")
        runs = get_recent_runs(db_path, limit=1)
        assert runs[0]["finished_at"] is None
        assert runs[0]["files_processed"] == 0
