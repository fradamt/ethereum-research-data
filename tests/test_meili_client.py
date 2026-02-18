"""Tests for erd_index.index.meili_client — connection management and index lifecycle.

All Meilisearch interactions are mocked so tests run without a server.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from meilisearch.errors import MeilisearchApiError, MeilisearchCommunicationError

from erd_index.index.meili_client import (
    _get_stored_schema_version,
    _update_alias,
    ensure_index,
    get_client,
)
from erd_index.settings import MeilisearchConfig, Settings

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_settings(
    url: str = "http://localhost:7700",
    index_name: str = "test_chunks",
    index_alias: str = "test_alias",
    master_key: str = "",
) -> Settings:
    return Settings(
        meili=MeilisearchConfig(
            url=url,
            index_name=index_name,
            index_alias=index_alias,
            master_key=master_key,
        ),
    )


def _api_error(code: str) -> MeilisearchApiError:
    """Build a MeilisearchApiError with the given error code."""
    resp = MagicMock()
    resp.status_code = 404
    resp.text = f'{{"code": "{code}"}}'
    err = MeilisearchApiError.__new__(MeilisearchApiError)
    err.status_code = 404
    err.code = code
    err.message = code
    err.link = ""
    err.type = ""
    return err


def _mock_task(uid: int = 0) -> MagicMock:
    t = MagicMock()
    t.task_uid = uid
    return t


# ===================================================================
# get_client
# ===================================================================


class TestGetClient:
    """get_client creates a cached client and validates server health."""

    def setup_method(self) -> None:
        """Reset the module-level client cache before each test."""
        import erd_index.index.meili_client as mod

        mod._cached_client = None
        mod._cached_url = None

    @patch("erd_index.index.meili_client.meilisearch.Client")
    def test_creates_client_and_checks_health(self, MockClient: MagicMock) -> None:
        client_instance = MagicMock()
        MockClient.return_value = client_instance

        result = get_client(_mock_settings())

        MockClient.assert_called_once_with("http://localhost:7700", None)
        client_instance.health.assert_called_once()
        assert result is client_instance

    @patch("erd_index.index.meili_client.meilisearch.Client")
    def test_caching_returns_same_client(self, MockClient: MagicMock) -> None:
        """Second call with same URL returns cached client without new health check."""
        client_instance = MagicMock()
        MockClient.return_value = client_instance
        settings = _mock_settings()

        first = get_client(settings)
        second = get_client(settings)

        assert first is second
        assert MockClient.call_count == 1
        assert client_instance.health.call_count == 1

    @patch("erd_index.index.meili_client.meilisearch.Client")
    def test_different_url_creates_new_client(self, MockClient: MagicMock) -> None:
        client_a = MagicMock()
        client_b = MagicMock()
        MockClient.side_effect = [client_a, client_b]

        first = get_client(_mock_settings(url="http://host-a:7700"))
        second = get_client(_mock_settings(url="http://host-b:7700"))

        assert first is client_a
        assert second is client_b
        assert MockClient.call_count == 2

    @patch("erd_index.index.meili_client.meilisearch.Client")
    def test_raises_connection_error_on_health_failure(
        self, MockClient: MagicMock,
    ) -> None:
        client_instance = MagicMock()
        client_instance.health.side_effect = MeilisearchCommunicationError("refused")
        MockClient.return_value = client_instance

        with pytest.raises(ConnectionError, match="Cannot reach Meilisearch"):
            get_client(_mock_settings())

    @patch("erd_index.index.meili_client.meilisearch.Client")
    def test_master_key_passed_when_set(self, MockClient: MagicMock) -> None:
        MockClient.return_value = MagicMock()
        get_client(_mock_settings(master_key="secret123"))
        MockClient.assert_called_once_with("http://localhost:7700", "secret123")

    @patch("erd_index.index.meili_client.meilisearch.Client")
    def test_empty_master_key_passes_none(self, MockClient: MagicMock) -> None:
        MockClient.return_value = MagicMock()
        get_client(_mock_settings(master_key=""))
        MockClient.assert_called_once_with("http://localhost:7700", None)


# ===================================================================
# ensure_index
# ===================================================================


class TestEnsureIndex:
    """ensure_index creates or updates the index as needed."""

    def setup_method(self) -> None:
        import erd_index.index.meili_client as mod

        mod._cached_client = None
        mod._cached_url = None

    @patch("erd_index.index.meili_client.init_index")
    @patch("erd_index.index.meili_client.get_client")
    def test_creates_new_index_when_not_found(
        self,
        mock_get_client: MagicMock,
        mock_init_index: MagicMock,
    ) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        client.get_index.side_effect = _api_error("index_not_found")
        mock_init_index.return_value = client

        settings = _mock_settings()
        result = ensure_index(settings)

        mock_init_index.assert_called_once_with(settings)
        assert result is client

    @patch("erd_index.index.meili_client._apply_settings")
    @patch("erd_index.index.meili_client._get_stored_schema_version")
    @patch("erd_index.index.meili_client.get_client")
    def test_applies_settings_when_schema_version_stale(
        self,
        mock_get_client: MagicMock,
        mock_get_version: MagicMock,
        mock_apply: MagicMock,
    ) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        client.get_index.return_value = MagicMock()
        mock_get_version.return_value = 0  # stale: current SCHEMA_VERSION >= 1

        ensure_index(_mock_settings())

        mock_apply.assert_called_once_with(client, "test_chunks")

    @patch("erd_index.index.meili_client._apply_settings")
    @patch("erd_index.index.meili_client._get_stored_schema_version")
    @patch("erd_index.index.meili_client.get_client")
    def test_skips_settings_when_schema_version_current(
        self,
        mock_get_client: MagicMock,
        mock_get_version: MagicMock,
        mock_apply: MagicMock,
    ) -> None:
        from erd_index.index.meili_schema import SCHEMA_VERSION

        client = MagicMock()
        mock_get_client.return_value = client
        client.get_index.return_value = MagicMock()
        mock_get_version.return_value = SCHEMA_VERSION  # current

        ensure_index(_mock_settings())

        mock_apply.assert_not_called()

    @patch("erd_index.index.meili_client.get_client")
    def test_reraises_non_not_found_api_error(
        self, mock_get_client: MagicMock,
    ) -> None:
        client = MagicMock()
        mock_get_client.return_value = client
        client.get_index.side_effect = _api_error("invalid_api_key")

        with pytest.raises(MeilisearchApiError):
            ensure_index(_mock_settings())


# ===================================================================
# _get_stored_schema_version
# ===================================================================


class TestGetStoredSchemaVersion:
    """_get_stored_schema_version reads schema version from a sampled document."""

    def test_empty_index_returns_zero(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 0
        index.get_stats.return_value = stats

        assert _get_stored_schema_version(client, "idx") == 0
        index.search.assert_not_called()

    def test_valid_version_returned(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 50
        index.get_stats.return_value = stats
        index.search.return_value = {"hits": [{"schema_version": 3}]}

        assert _get_stored_schema_version(client, "idx") == 3

    def test_no_hits_returns_zero(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 5
        index.get_stats.return_value = stats
        index.search.return_value = {"hits": []}

        assert _get_stored_schema_version(client, "idx") == 0

    def test_non_integer_version_returns_zero(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 10
        index.get_stats.return_value = stats
        index.search.return_value = {"hits": [{"schema_version": "bad"}]}

        assert _get_stored_schema_version(client, "idx") == 0

    def test_missing_schema_version_field_returns_zero(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index

        stats = MagicMock()
        stats.number_of_documents = 10
        index.get_stats.return_value = stats
        index.search.return_value = {"hits": [{}]}

        assert _get_stored_schema_version(client, "idx") == 0

    def test_communication_error_returns_zero(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index
        index.get_stats.side_effect = MeilisearchCommunicationError("down")

        assert _get_stored_schema_version(client, "idx") == 0

    def test_api_error_returns_zero(self) -> None:
        client = MagicMock()
        index = MagicMock()
        client.index.return_value = index
        index.get_stats.side_effect = _api_error("index_not_found")

        assert _get_stored_schema_version(client, "idx") == 0


# ===================================================================
# _update_alias
# ===================================================================


class TestUpdateAlias:
    """_update_alias manages the swap-indexes alias lifecycle."""

    def test_noop_when_alias_equals_index_name(self) -> None:
        client = MagicMock()
        _update_alias(client, "same_name", "same_name")
        client.get_index.assert_not_called()
        client.swap_indexes.assert_not_called()

    def test_creates_alias_index_when_not_found(self) -> None:
        client = MagicMock()
        client.get_index.side_effect = _api_error("index_not_found")
        client.create_index.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "succeeded"}
        client.swap_indexes.return_value = _mock_task(2)

        _update_alias(client, "alias", "target")

        client.create_index.assert_called_once_with("alias", {"primaryKey": "id"})
        client.swap_indexes.assert_called_once_with(
            [{"indexes": ["alias", "target"]}],
        )

    def test_swaps_when_alias_points_elsewhere(self) -> None:
        client = MagicMock()
        alias_index = MagicMock()
        alias_index.uid = "old_target"
        client.get_index.return_value = alias_index
        client.swap_indexes.return_value = _mock_task(1)
        client.wait_for_task.return_value = {"status": "succeeded"}

        _update_alias(client, "alias", "new_target")

        client.swap_indexes.assert_called_once()

    def test_noop_when_alias_already_correct(self) -> None:
        client = MagicMock()
        alias_index = MagicMock()
        alias_index.uid = "target"
        client.get_index.return_value = alias_index

        _update_alias(client, "alias", "target")

        client.swap_indexes.assert_not_called()
        client.create_index.assert_not_called()

    def test_reraises_non_not_found_error(self) -> None:
        client = MagicMock()
        client.get_index.side_effect = _api_error("invalid_api_key")

        with pytest.raises(MeilisearchApiError):
            _update_alias(client, "alias", "target")
