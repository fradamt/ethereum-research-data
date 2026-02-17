"""Tests for pipeline helper functions that don't require Meilisearch.

Focuses on _stale_chunk_ids which determines which chunk IDs from a previous
indexing run are no longer present after re-chunking a file.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from erd_index.pipeline import _stale_chunk_ids
from erd_index.state.manifest_db import (
    get_indexed_file,
    init_state_db,
    upsert_indexed_file,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db_path(tmp_settings) -> Path:
    """Initialize the state DB and return its path."""
    return init_state_db(tmp_settings)


def _insert_file(
    db_path: Path,
    *,
    repository: str = "repo",
    file_path: str = "doc.md",
    chunk_ids: list[str] | None = None,
) -> None:
    """Insert a manifest row with the given chunk_ids."""
    upsert_indexed_file(
        db_path,
        repository=repository,
        file_path=file_path,
        source_name="test",
        language="markdown",
        size_bytes=100,
        mtime_ns=1000,
        file_hash="aaa",
        parser_version="0.1.0",
        chunker_version="0.1.0",
        chunk_ids_json=json.dumps(chunk_ids or []),
    )


# ---------------------------------------------------------------------------
# _stale_chunk_ids
# ---------------------------------------------------------------------------


class TestStaleChunkIds:
    """Test the _stale_chunk_ids helper from pipeline.py."""

    def test_new_file_no_old_entry(self, db_path: Path):
        """When the file has never been indexed, there are no stale IDs."""
        stale = _stale_chunk_ids(db_path, "repo", "brand-new.md", ["c1", "c2"])
        assert stale == []

    def test_unchanged_chunks(self, db_path: Path):
        """When the same chunk IDs come back, nothing is stale."""
        _insert_file(db_path, chunk_ids=["c1", "c2", "c3"])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", ["c1", "c2", "c3"])
        assert stale == []

    def test_some_chunks_removed(self, db_path: Path):
        """Chunks in old set but not in new set are stale."""
        _insert_file(db_path, chunk_ids=["c1", "c2", "c3"])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", ["c1", "c3"])
        assert stale == ["c2"]

    def test_all_chunks_removed(self, db_path: Path):
        """If the file is re-chunked into zero chunks, all old IDs are stale."""
        _insert_file(db_path, chunk_ids=["c1", "c2"])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", [])
        assert sorted(stale) == ["c1", "c2"]

    def test_new_chunks_added(self, db_path: Path):
        """New chunks that weren't in the old set do not appear in stale list."""
        _insert_file(db_path, chunk_ids=["c1"])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", ["c1", "c2", "c3"])
        assert stale == []

    def test_mixed_add_and_remove(self, db_path: Path):
        """Some old chunks removed, some new added — only removed ones are stale."""
        _insert_file(db_path, chunk_ids=["old-a", "shared", "old-b"])
        stale = _stale_chunk_ids(
            db_path, "repo", "doc.md", ["shared", "new-x"]
        )
        assert sorted(stale) == ["old-a", "old-b"]

    def test_stale_ids_sorted(self, db_path: Path):
        """Stale IDs are returned sorted (deterministic output)."""
        _insert_file(db_path, chunk_ids=["z", "a", "m"])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", [])
        assert stale == ["a", "m", "z"]

    def test_scoped_to_repository(self, db_path: Path):
        """Files in a different repository are not considered."""
        _insert_file(db_path, repository="repo-a", file_path="f.md", chunk_ids=["c1"])
        _insert_file(db_path, repository="repo-b", file_path="f.md", chunk_ids=["c2"])
        # Ask about repo-a — repo-b's chunks should not appear
        stale = _stale_chunk_ids(db_path, "repo-a", "f.md", [])
        assert stale == ["c1"]

    def test_empty_old_chunk_list(self, db_path: Path):
        """File was indexed with zero chunks; nothing is stale."""
        _insert_file(db_path, chunk_ids=[])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", ["c1"])
        assert stale == []

    def test_old_entry_with_empty_json(self, db_path: Path):
        """If chunk_ids_json is '[]', nothing is stale."""
        _insert_file(db_path, chunk_ids=[])
        stale = _stale_chunk_ids(db_path, "repo", "doc.md", [])
        assert stale == []

    def test_different_file_paths_independent(self, db_path: Path):
        """Two files in the same repo have independent stale tracking."""
        _insert_file(db_path, file_path="a.md", chunk_ids=["a1", "a2"])
        _insert_file(db_path, file_path="b.md", chunk_ids=["b1", "b2"])
        stale_a = _stale_chunk_ids(db_path, "repo", "a.md", ["a1"])
        stale_b = _stale_chunk_ids(db_path, "repo", "b.md", ["b1", "b2"])
        assert stale_a == ["a2"]
        assert stale_b == []
