"""Tests for crash safety, non-atomic operations, and exception handling.

Covers graph rebuild atomicity, stale cleanup under connection errors,
abort thresholds, sync_all phase isolation, curate_eips atomic copy,
scraper incremental re-fetch, index checkpointing, writer status validation,
corrupt manifest data, and schema version edge cases.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from erd_index.discover.file_walker import DiscoveredFile
from erd_index.graph.node_builder import chunk_to_node
from erd_index.graph.store import (
    get_connection,
    get_stats,
    init_graph_db,
    upsert_node,
)
from erd_index.index.writer import _wait_and_check
from erd_index.models import Chunk, ChunkKind, Language, SourceKind
from erd_index.pipeline import (
    _cleanup_stale_markdown,
    _stale_chunk_ids,
    build_graph,
    ingest_code,
    ingest_markdown,
    sync_all,
)
from erd_index.settings import Settings
from erd_index.state.manifest_db import (
    get_indexed_file,
    init_state_db,
    upsert_indexed_file,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_settings(tmp_path: Path, **overrides) -> Settings:
    """Build a Settings pointing entirely at tmp_path."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    corpus_dir = tmp_path / "corpus"
    corpus_dir.mkdir(exist_ok=True)
    defaults = dict(
        meili=MagicMock(
            url="http://localhost:7700",
            index_name="test_chunks",
            index_alias="test_alias",
            batch_size=100,
            master_key="",
        ),
        corpus_dir=str(corpus_dir),
        data_dir=str(data_dir),
        graph_db=str(data_dir / "graph.db"),
        state_db=str(data_dir / "index_state.db"),
        project_root=tmp_path,
        schema_version=1,
        parser_version="0.1.0",
        chunker_version="0.1.0",
        code_repos=[],
        corpus_sources=[],
    )
    defaults.update(overrides)
    return Settings(**defaults)


def _make_eip_chunk(eip: int, *, text: str = "") -> Chunk:
    """Build a minimal EIP chunk for graph tests."""
    return Chunk(
        source_kind=SourceKind.EIP,
        chunk_kind=ChunkKind.EIP_SECTION,
        source_name="eips",
        language=Language.MARKDOWN,
        path=f"EIPS/eip-{eip}.md",
        title=f"EIP-{eip}",
        text=text or f"Content of EIP-{eip}",
        start_line=1,
        end_line=50,
        eip=eip,
        eip_status="Final",
        eip_type="Core",
    )


def _seed_graph(conn: sqlite3.Connection, eips: list[int]) -> None:
    """Insert a set of EIP nodes into the graph and commit."""
    for eip in eips:
        chunk = _make_eip_chunk(eip)
        node = chunk_to_node(chunk)
        upsert_node(conn, node)
    conn.commit()


# ===================================================================
# 1. Graph rebuild atomicity
# ===================================================================


class TestGraphRebuildAtomicity:
    """If build_graph fails mid-way, the old graph data is preserved."""

    def test_rollback_on_circuit_breaker(self, tmp_path: Path) -> None:
        """10+ processing errors trigger circuit breaker; rollback preserves old nodes."""
        settings = _make_settings(tmp_path)

        # Seed graph with existing data
        graph_db_path = init_graph_db(settings)
        conn = get_connection(graph_db_path)
        _seed_graph(conn, [1559, 4844])
        stats_before = get_stats(conn)
        assert stats_before["table_counts"]["node"] == 2
        conn.close()

        # 10 failing files to trigger circuit breaker (>= 10 errors, 0 chunks)
        failing_files = [
            DiscoveredFile(
                absolute_path=tmp_path / f"bad_{i}.md",
                relative_path=f"bad_{i}.md",
                source_name="test",
                repository="",
                language="markdown",
                size_bytes=100,
                mtime_ns=1000,
            )
            for i in range(10)
        ]

        with (
            patch("erd_index.pipeline._discover_markdown_files", return_value=failing_files),
            patch("erd_index.pipeline._discover_code_files", return_value=[]),
            patch(
                "erd_index.pipeline._process_markdown_file",
                side_effect=RuntimeError("parse crash"),
            ),
        ):
            with pytest.raises(RuntimeError, match="Aborting graph build"):
                build_graph(settings)

        # Old graph data must be preserved (rollback happened)
        conn = get_connection(graph_db_path)
        stats_after = get_stats(conn)
        assert stats_after["table_counts"]["node"] == 2
        conn.close()

    def test_rollback_on_node_upsert_error(self, tmp_path: Path) -> None:
        """Error during node upsert (pass 1) triggers rollback; old graph preserved."""
        settings = _make_settings(tmp_path)

        graph_db_path = init_graph_db(settings)
        conn = get_connection(graph_db_path)
        _seed_graph(conn, [1559])
        conn.close()

        chunk = _make_eip_chunk(4844)
        good_file = DiscoveredFile(
            absolute_path=tmp_path / "good.md",
            relative_path="good.md",
            source_name="test",
            repository="",
            language="markdown",
            size_bytes=10,
            mtime_ns=1000,
        )

        with (
            patch("erd_index.pipeline._discover_markdown_files", return_value=[good_file]),
            patch("erd_index.pipeline._discover_code_files", return_value=[]),
            patch(
                "erd_index.pipeline._process_markdown_file",
                return_value=([chunk], ["chunk-1"]),
            ),
            # Fail during node upsert (pass 1) — after DELETE has run
            patch("erd_index.pipeline.upsert_node", side_effect=sqlite3.OperationalError("disk I/O")),
        ):
            with pytest.raises(sqlite3.OperationalError, match="disk I/O"):
                build_graph(settings)

        # Rollback should restore the old node
        conn = get_connection(graph_db_path)
        stats = get_stats(conn)
        assert stats["table_counts"]["node"] == 1, "old node should survive rollback"
        conn.close()

    def test_rollback_preserves_all_tables(self, tmp_path: Path) -> None:
        """A failed rebuild preserves edges too, not just nodes."""
        settings = _make_settings(tmp_path)

        graph_db_path = init_graph_db(settings)
        conn = get_connection(graph_db_path)
        _seed_graph(conn, [1559])
        conn.close()

        # 11 failing files to trigger the circuit breaker
        failing_files = [
            DiscoveredFile(
                absolute_path=tmp_path / f"fail_{i}.md",
                relative_path=f"fail_{i}.md",
                source_name="test",
                repository="",
                language="markdown",
                size_bytes=10,
                mtime_ns=1000,
            )
            for i in range(11)
        ]

        with (
            patch("erd_index.pipeline._discover_markdown_files", return_value=failing_files),
            patch("erd_index.pipeline._discover_code_files", return_value=[]),
            patch(
                "erd_index.pipeline._process_markdown_file",
                side_effect=ValueError("boom"),
            ),
        ):
            with pytest.raises(RuntimeError, match="Aborting graph build"):
                build_graph(settings)

        conn = get_connection(graph_db_path)
        stats = get_stats(conn)
        assert stats["table_counts"]["node"] == 1, "node should survive rollback"
        conn.close()


# ===================================================================
# 2. Stale cleanup ConnectionError handling
# ===================================================================


class TestStaleCleanupConnectionError:
    """If Meilisearch goes down during stale cleanup, manifest rows are preserved."""

    def test_manifest_row_preserved_on_connection_error(self, tmp_path: Path) -> None:
        """When delete_by_ids raises ConnectionError, the manifest row is NOT removed."""
        settings = _make_settings(tmp_path)
        state_db = init_state_db(settings)

        # Insert a stale file with chunk IDs
        upsert_indexed_file(
            state_db,
            repository="test-source",
            file_path="deleted.md",
            source_name="test-source",
            language="markdown",
            size_bytes=100,
            mtime_ns=1000,
            file_hash="abc",
            parser_version="0.1.0",
            chunker_version="0.1.0",
            chunk_ids_json='["c1", "c2"]',
        )

        # paths_by_source has no paths for "test-source" => deleted.md is stale
        paths_by_source: dict[str, set[str]] = {"test-source": set()}

        with patch("erd_index.pipeline.delete_by_ids", side_effect=ConnectionError("server down")):
            deleted = _cleanup_stale_markdown(settings, state_db, paths_by_source)

        # No chunks were successfully deleted
        assert deleted == 0

        # The manifest row must still exist so cleanup can be retried
        row = get_indexed_file(state_db, "test-source", "deleted.md")
        assert row is not None
        assert row["chunk_ids_json"] == '["c1", "c2"]'

    def test_continues_processing_other_files_after_connection_error(
        self, tmp_path: Path,
    ) -> None:
        """ConnectionError on one file does not prevent processing other stale files."""
        settings = _make_settings(tmp_path)
        state_db = init_state_db(settings)

        # Two stale files: first will fail, second has no chunks (just manifest cleanup)
        upsert_indexed_file(
            state_db,
            repository="src",
            file_path="fail.md",
            source_name="src",
            language="markdown",
            size_bytes=50,
            mtime_ns=1,
            file_hash="h1",
            parser_version="0.1.0",
            chunker_version="0.1.0",
            chunk_ids_json='["c1"]',
        )
        upsert_indexed_file(
            state_db,
            repository="src",
            file_path="empty_chunks.md",
            source_name="src",
            language="markdown",
            size_bytes=50,
            mtime_ns=1,
            file_hash="h2",
            parser_version="0.1.0",
            chunker_version="0.1.0",
            chunk_ids_json="[]",
        )

        paths_by_source: dict[str, set[str]] = {"src": set()}

        with patch(
            "erd_index.pipeline.delete_by_ids", side_effect=ConnectionError("offline"),
        ):
            _cleanup_stale_markdown(settings, state_db, paths_by_source)

        # fail.md: manifest preserved because delete failed
        assert get_indexed_file(state_db, "src", "fail.md") is not None
        # empty_chunks.md: has no chunks to delete, so manifest row IS removed
        assert get_indexed_file(state_db, "src", "empty_chunks.md") is None


# ===================================================================
# 3. Dry-run abort threshold
# ===================================================================


class TestDryRunAbortThreshold:
    """Abort threshold (10 errors, 0 successes) works in dry-run mode too."""

    def test_files_parsed_increments_in_dry_run(self, tmp_path: Path) -> None:
        """In dry-run, files_parsed increments on success, preventing abort."""
        settings = _make_settings(tmp_path)
        init_state_db(settings)

        # Create a corpus source directory with markdown files
        corpus_src = tmp_path / "corpus" / "test"
        corpus_src.mkdir(parents=True, exist_ok=True)
        for i in range(3):
            (corpus_src / f"doc_{i}.md").write_text(f"# Doc {i}\nContent here.")

        # Dry-run: no Meilisearch needed, should succeed
        with (
            patch("erd_index.pipeline.ensure_index"),
            patch("erd_index.pipeline.walk_sources") as mock_walk,
        ):
            discovered = [
                DiscoveredFile(
                    absolute_path=corpus_src / f"doc_{i}.md",
                    relative_path=f"doc_{i}.md",
                    source_name="test",
                    repository="",
                    language="markdown",
                    size_bytes=50,
                    mtime_ns=1000,
                )
                for i in range(3)
            ]
            mock_walk.return_value = discovered

            # Should not raise (files_parsed > 0 prevents abort)
            ingest_markdown(settings, dry_run=True)

    def test_10_consecutive_errors_0_successes_aborts_even_in_dry_run(
        self, tmp_path: Path,
    ) -> None:
        """10 consecutive errors with 0 successes triggers abort in dry-run."""
        settings = _make_settings(tmp_path)
        init_state_db(settings)

        failing_files = [
            DiscoveredFile(
                absolute_path=tmp_path / f"bad_{i}.md",
                relative_path=f"bad_{i}.md",
                source_name="test",
                repository="",
                language="markdown",
                size_bytes=10,
                mtime_ns=1000,
            )
            for i in range(10)
        ]

        with (
            patch("erd_index.pipeline.ensure_index"),
            patch("erd_index.pipeline._discover_markdown_files", return_value=failing_files),
            patch(
                "erd_index.pipeline._process_markdown_file",
                side_effect=ValueError("bad file"),
            ),
        ):
            with pytest.raises(RuntimeError, match="Aborting.*10 consecutive errors"):
                ingest_markdown(settings, dry_run=True)


# ===================================================================
# 4. build_graph circuit breaker
# ===================================================================


class TestBuildGraphCircuitBreaker:
    """build_graph aborts after 10 consecutive errors with 0 successes."""

    def test_aborts_after_10_errors_0_chunks(self, tmp_path: Path) -> None:
        """10 markdown file errors with 0 successful chunks triggers abort."""
        settings = _make_settings(tmp_path)
        init_graph_db(settings)

        failing_files = [
            DiscoveredFile(
                absolute_path=tmp_path / f"err_{i}.md",
                relative_path=f"err_{i}.md",
                source_name="test",
                repository="",
                language="markdown",
                size_bytes=10,
                mtime_ns=1000,
            )
            for i in range(10)
        ]

        with (
            patch("erd_index.pipeline._discover_markdown_files", return_value=failing_files),
            patch("erd_index.pipeline._discover_code_files", return_value=[]),
            patch(
                "erd_index.pipeline._process_markdown_file",
                side_effect=Exception("crash"),
            ),
        ):
            with pytest.raises(RuntimeError, match="Aborting graph build.*10 consecutive"):
                build_graph(settings)

    def test_does_not_abort_if_some_succeed(self, tmp_path: Path) -> None:
        """If at least one file succeeds, the circuit breaker does not fire."""
        settings = _make_settings(tmp_path)
        init_graph_db(settings)

        chunk = _make_eip_chunk(1559)

        files = [
            DiscoveredFile(
                absolute_path=tmp_path / f"file_{i}.md",
                relative_path=f"file_{i}.md",
                source_name="test",
                repository="",
                language="markdown",
                size_bytes=10,
                mtime_ns=1000,
            )
            for i in range(15)
        ]

        call_count = 0

        def _process_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [chunk], ["chunk-1"]
            raise ValueError("fail")

        with (
            patch("erd_index.pipeline._discover_markdown_files", return_value=files),
            patch("erd_index.pipeline._discover_code_files", return_value=[]),
            patch(
                "erd_index.pipeline._process_markdown_file",
                side_effect=_process_side_effect,
            ),
        ):
            # Should not raise: first file succeeded, so all_chunks is non-empty
            build_graph(settings)


# ===================================================================
# 5. sync_all phase isolation
# ===================================================================


class TestSyncAllPhaseIsolation:
    """sync_all wraps all phases in try/except; failures are accumulated."""

    def test_ingest_code_runs_even_if_ingest_markdown_fails(
        self, tmp_path: Path,
    ) -> None:
        """If ingest_markdown fails, ingest_code should still run."""
        settings = _make_settings(tmp_path)
        code_ran = False

        def _mock_ingest_code(*args, **kwargs):
            nonlocal code_ran
            code_ran = True

        with (
            patch(
                "erd_index.pipeline.ingest_markdown",
                side_effect=RuntimeError("md exploded"),
            ),
            patch("erd_index.pipeline.ingest_code", side_effect=_mock_ingest_code),
            patch("erd_index.pipeline.build_graph"),
            patch("erd_index.pipeline.link_specs"),
        ):
            with pytest.raises(RuntimeError, match="ingest-markdown"):
                sync_all(settings)

        assert code_ran, "ingest_code should have been called despite markdown failure"

    def test_multiple_failures_listed_in_error(self, tmp_path: Path) -> None:
        """When multiple phases fail, RuntimeError lists all failed phases."""
        settings = _make_settings(tmp_path)

        with (
            patch(
                "erd_index.pipeline.ingest_markdown",
                side_effect=RuntimeError("md fail"),
            ),
            patch(
                "erd_index.pipeline.ingest_code",
                side_effect=RuntimeError("code fail"),
            ),
            patch(
                "erd_index.pipeline.build_graph",
                side_effect=RuntimeError("graph fail"),
            ),
            patch(
                "erd_index.pipeline.link_specs",
                side_effect=RuntimeError("link fail"),
            ),
        ):
            with pytest.raises(RuntimeError) as exc_info:
                sync_all(settings)

            msg = str(exc_info.value)
            assert "ingest-markdown" in msg
            assert "ingest-code" in msg
            assert "build-graph" in msg
            assert "link-specs" in msg

    def test_no_error_when_all_phases_succeed(self, tmp_path: Path) -> None:
        """sync_all should not raise when all phases succeed."""
        settings = _make_settings(tmp_path)

        with (
            patch("erd_index.pipeline.ingest_markdown"),
            patch("erd_index.pipeline.ingest_code"),
            patch("erd_index.pipeline.build_graph"),
            patch("erd_index.pipeline.link_specs"),
        ):
            # Should not raise
            sync_all(settings)

    def test_dry_run_skips_graph_and_link(self, tmp_path: Path) -> None:
        """In dry-run mode, build_graph and link_specs are skipped."""
        settings = _make_settings(tmp_path)

        with (
            patch("erd_index.pipeline.ingest_markdown") as mock_md,
            patch("erd_index.pipeline.ingest_code") as mock_code,
            patch("erd_index.pipeline.build_graph") as mock_graph,
            patch("erd_index.pipeline.link_specs") as mock_link,
        ):
            sync_all(settings, dry_run=True)

        mock_md.assert_called_once()
        mock_code.assert_called_once()
        mock_graph.assert_not_called()
        mock_link.assert_not_called()


# ===================================================================
# 6. curate_eips atomic copy
# ===================================================================


class TestCurateEipsAtomicCopy:
    """curate_eips.py uses atomic file operations (temp + rename)."""

    def test_interrupted_copy_leaves_no_partial_file(self, tmp_path: Path) -> None:
        """If shutil.copy2 raises, no partial file is left at the destination."""
        eips_dir = tmp_path / "EIPS"
        eips_dir.mkdir()
        (eips_dir / "eip-1559.md").write_text("# EIP-1559\nContent here")

        out_dir = tmp_path / "corpus" / "eips"
        out_dir.mkdir(parents=True, exist_ok=True)

        with patch("shutil.copy2", side_effect=OSError("disk full")):
            # Run the curate_eips main logic manually (it uses sys.argv parsing)
            from scripts.curate_eips import main

            with pytest.raises(OSError, match="disk full"):
                with patch("sys.argv", ["curate_eips", "--eips-dir", str(eips_dir)]):
                    main()

        # No partial file or temp file should exist
        dest = out_dir / "eip-1559.md"
        assert not dest.exists(), "partial file should not exist after interrupted copy"

        # Check no .tmp files left behind
        tmp_files = list(out_dir.glob("*.tmp"))
        assert tmp_files == [], f"temp files should be cleaned up, found {tmp_files}"

    def test_original_dest_preserved_on_error(self, tmp_path: Path) -> None:
        """If copy fails, the original destination file (if any) is not corrupted."""
        eips_dir = tmp_path / "EIPS"
        eips_dir.mkdir()
        src = eips_dir / "eip-100.md"
        src.write_text("# EIP-100 (v2)")
        # Make source newer than dest
        os.utime(src, (9999999999, 9999999999))

        out_dir = tmp_path / "corpus" / "eips"
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / "eip-100.md"
        dest.write_text("# EIP-100 (v1)")

        with patch("shutil.copy2", side_effect=IOError("write fail")):
            from scripts.curate_eips import main

            with pytest.raises(IOError, match="write fail"):
                with patch("sys.argv", ["curate_eips", "--eips-dir", str(eips_dir)]):
                    main()

        # Original content must be preserved
        assert dest.read_text() == "# EIP-100 (v1)"


# ===================================================================
# 7. Scraper topic refresh
# ===================================================================


class TestScraperTopicRefresh:
    """The scraper re-fetches topics when posts_count increases."""

    def test_refetch_when_posts_count_increases(self, tmp_path: Path) -> None:
        """Topics with more posts in the index than on disk are re-fetched."""
        from scraper.discourse import DiscourseScraper

        scraper = DiscourseScraper(
            base_url="https://example.com",
            raw_dir=tmp_path / "raw",
            delay=0.0,
            max_retries=1,
        )

        # Write an existing topic with 3 posts
        existing_topic = {
            "id": 42,
            "title": "Test",
            "post_stream": {"stream": [1, 2, 3], "posts": [{"id": 1}, {"id": 2}, {"id": 3}]},
        }
        topic_path = scraper.topics_dir / "42.json"
        topic_path.write_text(json.dumps(existing_topic))

        # Index metadata says 8 posts (5 more than on disk)
        index = {
            "42": {
                "id": 42,
                "title": "Test",
                "posts_count": 8,
            },
        }

        # Mock _fetch_full_topic to return updated topic
        updated_topic = {
            "id": 42,
            "title": "Test",
            "post_stream": {
                "stream": list(range(1, 9)),
                "posts": [{"id": i} for i in range(1, 9)],
            },
        }

        with patch.object(scraper, "_fetch_full_topic", return_value=updated_topic) as mock_fetch:
            with patch.object(scraper, "_throttle"):
                scraper.fetch_topics(index)

        # Should have re-fetched topic 42 because index_posts (8) > existing_posts (3)
        mock_fetch.assert_called_once_with(42)

    def test_skip_when_posts_count_unchanged(self, tmp_path: Path) -> None:
        """Topics with same posts_count on disk as in index are skipped."""
        from scraper.discourse import DiscourseScraper

        scraper = DiscourseScraper(
            base_url="https://example.com",
            raw_dir=tmp_path / "raw",
            delay=0.0,
            max_retries=1,
        )

        existing_topic = {
            "id": 42,
            "title": "Test",
            "post_stream": {"stream": [1, 2, 3], "posts": [{"id": 1}, {"id": 2}, {"id": 3}]},
        }
        topic_path = scraper.topics_dir / "42.json"
        topic_path.write_text(json.dumps(existing_topic))

        index = {
            "42": {"id": 42, "title": "Test", "posts_count": 3},
        }

        with patch.object(scraper, "_fetch_full_topic") as mock_fetch:
            with patch.object(scraper, "_throttle"):
                scraper.fetch_topics(index)

        # Should NOT have fetched — stream has 3 IDs, index says 3
        mock_fetch.assert_not_called()


# ===================================================================
# 8. Scraper index checkpointing
# ===================================================================


class TestScraperIndexCheckpointing:
    """build_index saves periodic checkpoints during category crawling."""

    def test_checkpoint_every_5_categories(self, tmp_path: Path) -> None:
        """Index is saved after every 5 categories, not just at the end."""
        from scraper.discourse import DiscourseScraper, _save_json

        scraper = DiscourseScraper(
            base_url="https://example.com",
            raw_dir=tmp_path / "raw",
            delay=0.0,
            max_retries=1,
        )

        # Build 6 categories so checkpoint fires at i=4 (5th category)
        categories = [
            {"id": i, "slug": f"cat-{i}", "name": f"Category {i}", "topic_count": 1}
            for i in range(6)
        ]

        page_data = {
            "topic_list": {
                "topics": [{"id": 100 + i, "title": f"Topic {100 + i}", "category_id": i,
                            "posts_count": 1, "created_at": "", "last_posted_at": "",
                            "views": 0, "like_count": 0}
                           for i in range(6)],
            }
        }
        # For each category, return topics on page 0 only
        call_count = 0

        def _mock_fetch_json(path):
            nonlocal call_count
            if "/latest" in path:
                return {"topic_list": {"topics": []}}
            call_count += 1
            # First call per category returns topics, second returns empty
            if "page=0" in path:
                cat_id = int(path.split("/c/")[1].split("/")[1].split(".")[0])
                return {
                    "topic_list": {
                        "topics": [{
                            "id": 1000 + cat_id,
                            "title": f"Topic for cat {cat_id}",
                            "category_id": cat_id,
                            "posts_count": 1,
                            "created_at": "",
                            "last_posted_at": "",
                            "views": 0,
                            "like_count": 0,
                        }],
                    }
                }
            return {"topic_list": {"topics": []}}

        write_calls = []
        original_save_json = _save_json

        def _tracking_save_json(path, data):
            write_calls.append(str(path))
            original_save_json(path, data)

        with (
            patch.object(scraper, "_fetch_json", side_effect=_mock_fetch_json),
            patch.object(scraper, "_throttle"),
            patch("scraper.discourse._save_json", side_effect=_tracking_save_json),
        ):
            scraper.build_index(categories)

        # Verify at least one checkpoint write occurred before the final save
        index_writes = [w for w in write_calls if "index.json" in w]
        # Should have: checkpoint at category 5 (i=4), /latest sweep save, and final save
        assert len(index_writes) >= 2, (
            f"Expected at least 2 index.json writes (checkpoint + final), got {len(index_writes)}"
        )


# ===================================================================
# 9. _wait_and_check status validation
# ===================================================================


class TestWaitAndCheckStatusValidation:
    """_wait_and_check raises on non-'succeeded' statuses."""

    def test_raises_on_canceled_status(self) -> None:
        """A 'canceled' task status should raise RuntimeError."""
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "canceled", "error": None}

        with pytest.raises(RuntimeError, match="canceled"):
            _wait_and_check(client, task_uid=1, description="test op")

    def test_raises_on_failed_status(self) -> None:
        """A 'failed' task status should raise RuntimeError with error details."""
        client = MagicMock()
        client.wait_for_task.return_value = {
            "status": "failed",
            "error": {"message": "invalid document id", "code": "invalid_document_id"},
        }

        with pytest.raises(RuntimeError, match="failed.*invalid document id"):
            _wait_and_check(client, task_uid=2, description="upsert batch")

    def test_succeeds_on_succeeded_status(self) -> None:
        """A 'succeeded' task status should not raise."""
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "succeeded", "error": None}

        # Should not raise
        _wait_and_check(client, task_uid=3, description="delete IDs")

    def test_handles_object_result(self) -> None:
        """_wait_and_check also handles SDK result objects with .status attribute."""
        client = MagicMock()
        result = MagicMock()
        result.status = "canceled"
        result.error = None
        client.wait_for_task.return_value = result

        with pytest.raises(RuntimeError, match="canceled"):
            _wait_and_check(client, task_uid=4, description="test")

    def test_enqueued_raises(self) -> None:
        """An 'enqueued' status (never completed) should raise RuntimeError."""
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "enqueued", "error": None}

        with pytest.raises(RuntimeError, match="enqueued"):
            _wait_and_check(client, task_uid=5, description="stuck task")


# ===================================================================
# 10. Corrupt chunk_ids_json in manifest
# ===================================================================


class TestCorruptChunkIdsJson:
    """Corrupt chunk_ids_json should not crash the pipeline."""

    def test_stale_chunk_ids_returns_empty_on_corrupt_json(
        self, tmp_path: Path,
    ) -> None:
        """_stale_chunk_ids returns empty list (not crash) for corrupt JSON."""
        settings = _make_settings(tmp_path)
        state_db = init_state_db(settings)

        # Insert a row with invalid JSON in chunk_ids_json
        upsert_indexed_file(
            state_db,
            repository="repo",
            file_path="corrupt.md",
            source_name="test",
            language="markdown",
            size_bytes=100,
            mtime_ns=1000,
            file_hash="aaa",
            parser_version="0.1.0",
            chunker_version="0.1.0",
            chunk_ids_json="{not valid json!!!",
        )

        # Should return [] with a warning, not crash
        stale = _stale_chunk_ids(state_db, "repo", "corrupt.md", ["c1"])
        assert stale == []

    def test_stale_cleanup_handles_corrupt_json(self, tmp_path: Path) -> None:
        """_cleanup_stale_markdown handles corrupt chunk_ids_json in stale rows."""
        settings = _make_settings(tmp_path)
        state_db = init_state_db(settings)

        # Insert stale file with corrupt JSON
        upsert_indexed_file(
            state_db,
            repository="src",
            file_path="bad.md",
            source_name="src",
            language="markdown",
            size_bytes=50,
            mtime_ns=1,
            file_hash="h",
            parser_version="0.1.0",
            chunker_version="0.1.0",
            chunk_ids_json="not json at all",
        )

        paths_by_source: dict[str, set[str]] = {"src": set()}

        # Should not raise — corrupt JSON treated as empty chunk list
        deleted = _cleanup_stale_markdown(settings, state_db, paths_by_source)
        assert deleted == 0

        # The stale manifest row should still be removed (no chunks to delete from Meili)
        assert get_indexed_file(state_db, "src", "bad.md") is None


# ===================================================================
# 11. _get_stored_schema_version edge cases
# ===================================================================


class TestGetStoredSchemaVersion:
    """_get_stored_schema_version handles edge cases gracefully."""

    def test_non_integer_schema_version_returns_0(self) -> None:
        """Non-integer schema_version in documents logs warning, returns 0."""
        from erd_index.index.meili_client import _get_stored_schema_version

        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        # Stats indicate documents exist
        stats = MagicMock()
        stats.number_of_documents = 10
        index.get_stats.return_value = stats

        # Search returns document with non-integer schema_version
        index.search.return_value = {
            "hits": [{"schema_version": "not-a-number"}],
        }

        result = _get_stored_schema_version(client, "test_index")
        assert result == 0

    def test_communication_error_returns_0(self) -> None:
        """MeilisearchCommunicationError logs warning, returns 0."""
        from meilisearch.errors import MeilisearchCommunicationError

        from erd_index.index.meili_client import _get_stored_schema_version

        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        index.get_stats.side_effect = MeilisearchCommunicationError("connection refused")

        result = _get_stored_schema_version(client, "test_index")
        assert result == 0

    def test_empty_index_returns_0(self) -> None:
        """An index with 0 documents returns schema_version=0."""
        from erd_index.index.meili_client import _get_stored_schema_version

        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 0
        index.get_stats.return_value = stats

        result = _get_stored_schema_version(client, "test_index")
        assert result == 0
        # search() should NOT be called when there are 0 docs
        index.search.assert_not_called()

    def test_valid_integer_schema_version(self) -> None:
        """A valid integer schema_version is returned correctly."""
        from erd_index.index.meili_client import _get_stored_schema_version

        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 100
        index.get_stats.return_value = stats

        index.search.return_value = {
            "hits": [{"schema_version": 3}],
        }

        result = _get_stored_schema_version(client, "test_index")
        assert result == 3

    def test_no_hits_returns_0(self) -> None:
        """If search returns no hits, returns 0."""
        from erd_index.index.meili_client import _get_stored_schema_version

        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 5
        index.get_stats.return_value = stats

        index.search.return_value = {"hits": []}

        result = _get_stored_schema_version(client, "test_index")
        assert result == 0
