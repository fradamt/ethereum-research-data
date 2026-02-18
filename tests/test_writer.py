"""Tests for erd_index.index.writer — batch upsert, delete, stats.

All Meilisearch interactions are mocked so tests run without a server.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from erd_index.index.writer import (
    _wait_and_check,
    batch_upsert,
    delete_by_filter,
    delete_by_ids,
    get_index_stats,
)
from erd_index.settings import MeilisearchConfig, Settings

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_settings(batch_size: int = 100) -> Settings:
    """Build a minimal Settings with a MeilisearchConfig."""
    return Settings(
        meili=MeilisearchConfig(
            url="http://localhost:7700",
            index_name="test_chunks",
            batch_size=batch_size,
        ),
    )


def _mock_task(uid: int = 0) -> MagicMock:
    task = MagicMock()
    task.task_uid = uid
    return task


# ===================================================================
# batch_upsert
# ===================================================================


class TestBatchUpsert:
    """batch_upsert sends documents in batches and waits for each task."""

    @patch("erd_index.index.writer.get_client")
    def test_empty_input_returns_zero(self, mock_get_client: MagicMock) -> None:
        result = batch_upsert(_mock_settings(), [])
        assert result == 0
        mock_get_client.assert_not_called()

    @patch("erd_index.index.writer.get_client")
    def test_single_batch(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.add_documents_json.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "succeeded"}

        docs = [{"id": f"doc-{i}", "text": f"text {i}"} for i in range(5)]
        result = batch_upsert(_mock_settings(batch_size=100), docs)

        assert result == 5
        assert index.add_documents_json.call_count == 1
        assert client.wait_for_task.call_count == 1

    @patch("erd_index.index.writer.get_client")
    def test_multiple_batches(self, mock_get_client: MagicMock) -> None:
        """10 docs with batch_size=3 should produce 4 batches (3+3+3+1)."""
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.add_documents_json.return_value = _mock_task(0)
        client.wait_for_task.return_value = {"status": "succeeded"}

        docs = [{"id": f"d-{i}"} for i in range(10)]
        result = batch_upsert(_mock_settings(batch_size=3), docs)

        assert result == 10
        assert index.add_documents_json.call_count == 4
        assert client.wait_for_task.call_count == 4

    @patch("erd_index.index.writer.get_client")
    def test_all_docs_submitted_across_batches(self, mock_get_client: MagicMock) -> None:
        """Every document is included in exactly one batch payload."""
        import orjson

        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.add_documents_json.return_value = _mock_task(0)
        client.wait_for_task.return_value = {"status": "succeeded"}

        docs = [{"id": f"x-{i}", "v": i} for i in range(7)]
        batch_upsert(_mock_settings(batch_size=3), docs)

        all_payloads = []
        for call in index.add_documents_json.call_args_list:
            payload = orjson.loads(call[0][0])
            all_payloads.extend(payload)

        submitted_ids = {d["id"] for d in all_payloads}
        expected_ids = {f"x-{i}" for i in range(7)}
        assert submitted_ids == expected_ids

    @patch("erd_index.index.writer.get_client")
    def test_raises_on_task_failure(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.add_documents_json.return_value = _mock_task(1)
        client.wait_for_task.return_value = {
            "status": "failed",
            "error": {"message": "bad payload"},
        }

        with pytest.raises(RuntimeError, match=r"failed.*bad payload"):
            batch_upsert(_mock_settings(), [{"id": "a"}])

    @patch("erd_index.index.writer.get_client")
    def test_exact_batch_boundary(self, mock_get_client: MagicMock) -> None:
        """6 docs with batch_size=3 should produce exactly 2 batches."""
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.add_documents_json.return_value = _mock_task(0)
        client.wait_for_task.return_value = {"status": "succeeded"}

        docs = [{"id": f"d-{i}"} for i in range(6)]
        result = batch_upsert(_mock_settings(batch_size=3), docs)

        assert result == 6
        assert index.add_documents_json.call_count == 2


# ===================================================================
# delete_by_ids
# ===================================================================


class TestDeleteByIds:
    """delete_by_ids sends IDs in batches and waits for each task."""

    @patch("erd_index.index.writer.get_client")
    def test_empty_input_returns_zero(self, mock_get_client: MagicMock) -> None:
        result = delete_by_ids(_mock_settings(), [])
        assert result == 0
        mock_get_client.assert_not_called()

    @patch("erd_index.index.writer.get_client")
    def test_single_batch(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.delete_documents.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "succeeded"}

        result = delete_by_ids(_mock_settings(), ["id-1", "id-2"])
        assert result == 2
        index.delete_documents.assert_called_once_with(ids=["id-1", "id-2"])

    @patch("erd_index.index.writer.get_client")
    def test_multiple_batches(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.delete_documents.return_value = _mock_task(0)
        client.wait_for_task.return_value = {"status": "succeeded"}

        ids = [f"chunk-{i}" for i in range(7)]
        result = delete_by_ids(_mock_settings(batch_size=3), ids)

        assert result == 7
        assert index.delete_documents.call_count == 3  # 3+3+1

    @patch("erd_index.index.writer.get_client")
    def test_raises_on_task_failure(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.delete_documents.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "failed", "error": "oops"}

        with pytest.raises(RuntimeError, match="failed"):
            delete_by_ids(_mock_settings(), ["id-1"])


# ===================================================================
# delete_by_filter
# ===================================================================


class TestDeleteByFilter:
    """delete_by_filter passes the filter string to Meilisearch."""

    @patch("erd_index.index.writer.get_client")
    def test_correct_filter_passed(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.delete_documents.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "succeeded"}

        filter_str = "source_name = 'ethresearch' AND doc_id = 'forum:ethresearch:1000'"
        delete_by_filter(_mock_settings(), filter_str)

        index.delete_documents.assert_called_once_with(filter=filter_str)

    @patch("erd_index.index.writer.get_client")
    def test_raises_on_task_failure(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index
        index.delete_documents.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "failed", "error": "bad filter"}

        with pytest.raises(RuntimeError, match="failed"):
            delete_by_filter(_mock_settings(), "invalid")


# ===================================================================
# get_index_stats
# ===================================================================


class TestGetIndexStats:
    """get_index_stats returns a normalized dict or an error dict."""

    @patch("erd_index.index.writer.get_client")
    def test_success_returns_correct_dict(self, mock_get_client: MagicMock) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index

        raw = MagicMock()
        raw.number_of_documents = 42
        raw.is_indexing = False
        raw.field_distribution = {"text": 42, "title": 40}
        index.get_stats.return_value = raw

        result = get_index_stats(_mock_settings())

        assert result["numberOfDocuments"] == 42
        assert result["isIndexing"] is False
        assert result["fieldDistribution"] == {"text": 42, "title": 40}
        assert "error" not in result

    @patch("erd_index.index.writer.get_client")
    def test_connection_error_returns_error_dict(self, mock_get_client: MagicMock) -> None:
        mock_get_client.side_effect = ConnectionError("unreachable")
        result = get_index_stats(_mock_settings())

        assert "error" in result
        assert "unreachable" in result["error"]

    @patch("erd_index.index.writer.get_client")
    def test_api_error_returns_error_dict(self, mock_get_client: MagicMock) -> None:
        from meilisearch.errors import MeilisearchApiError

        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index

        # MeilisearchApiError.__init__ parses request.text as JSON, so we
        # construct the exception manually to avoid needing a real response.
        err = MeilisearchApiError.__new__(MeilisearchApiError)
        err.status_code = 404
        err.code = "index_not_found"
        err.message = "Index not found"
        err.link = ""
        err.type = ""
        index.get_stats.side_effect = err

        result = get_index_stats(_mock_settings())
        assert "error" in result

    @patch("erd_index.index.writer.get_client")
    def test_none_field_distribution_becomes_empty_dict(
        self, mock_get_client: MagicMock,
    ) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        index = MagicMock()
        client.index.return_value = index

        raw = MagicMock()
        raw.number_of_documents = 0
        raw.is_indexing = False
        raw.field_distribution = None
        index.get_stats.return_value = raw

        result = get_index_stats(_mock_settings())
        assert result["fieldDistribution"] == {}


# ===================================================================
# _wait_and_check
# ===================================================================


class TestWaitAndCheck:
    """_wait_and_check validates task status from Meilisearch."""

    def test_succeeded_does_not_raise(self) -> None:
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "succeeded", "error": None}
        _wait_and_check(client, task_uid=1, description="test op")

    def test_failed_raises_with_error_details(self) -> None:
        client = MagicMock()
        client.wait_for_task.return_value = {
            "status": "failed",
            "error": {"message": "invalid document id"},
        }
        with pytest.raises(RuntimeError, match=r"failed.*invalid document id"):
            _wait_and_check(client, task_uid=2, description="upsert")

    def test_canceled_raises(self) -> None:
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "canceled", "error": None}
        with pytest.raises(RuntimeError, match="canceled"):
            _wait_and_check(client, task_uid=3, description="delete")

    def test_enqueued_raises(self) -> None:
        """A task stuck in 'enqueued' (timed out) should raise."""
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "enqueued", "error": None}
        with pytest.raises(RuntimeError, match="enqueued"):
            _wait_and_check(client, task_uid=4, description="stuck")

    def test_handles_object_result_succeeded(self) -> None:
        """SDK may return a typed result object instead of a dict."""
        client = MagicMock()
        result = MagicMock()
        result.status = "succeeded"
        result.error = None
        client.wait_for_task.return_value = result
        # Should not raise
        _wait_and_check(client, task_uid=5, description="object result")

    def test_handles_object_result_failed(self) -> None:
        client = MagicMock()
        result = MagicMock()
        result.status = "failed"
        result.error = "something broke"
        client.wait_for_task.return_value = result
        with pytest.raises(RuntimeError, match=r"failed.*something broke"):
            _wait_and_check(client, task_uid=6, description="object fail")

    def test_timeout_parameter(self) -> None:
        """_wait_and_check passes 120_000 ms timeout to client."""
        client = MagicMock()
        client.wait_for_task.return_value = {"status": "succeeded"}
        _wait_and_check(client, task_uid=7, description="timeout check")
        client.wait_for_task.assert_called_once_with(7, timeout_in_ms=120_000)
