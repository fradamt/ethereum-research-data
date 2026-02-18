"""Tests for Ethereum terminology synonyms and dictionary."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, call, patch

import pytest

from erd_index.index.terminology import (
    apply_terminology_settings,
    get_ethereum_dictionary,
    get_ethereum_synonyms,
)


# ===================================================================
# Synonym structure
# ===================================================================


class TestSynonyms:
    """Validate the synonym mapping structure and bidirectionality."""

    def test_synonyms_values_are_lists_of_strings(self) -> None:
        synonyms = get_ethereum_synonyms()
        for key, values in synonyms.items():
            assert isinstance(key, str), f"Key {key!r} is not a string"
            assert isinstance(values, list), f"Value for {key!r} is not a list"
            for v in values:
                assert isinstance(v, str), f"Synonym {v!r} for {key!r} is not a string"

    def test_synonyms_not_empty(self) -> None:
        synonyms = get_ethereum_synonyms()
        assert len(synonyms) > 0

    def test_all_values_are_nonempty_lists(self) -> None:
        synonyms = get_ethereum_synonyms()
        for key, values in synonyms.items():
            assert len(values) > 0, f"Key {key!r} has empty synonym list"

    def test_bidirectional_relationships(self) -> None:
        """Every synonym value must also appear as a key mapping back."""
        synonyms = get_ethereum_synonyms()
        for key, values in synonyms.items():
            for value in values:
                assert value in synonyms, (
                    f"Synonym {value!r} (from {key!r}) is not a key in the mapping"
                )
                assert key in synonyms[value], (
                    f"Key {key!r} not found in synonyms[{value!r}] = {synonyms[value]}"
                )

    def test_known_abbreviations_present(self) -> None:
        """Spot-check that key abbreviations are in the mapping."""
        synonyms = get_ethereum_synonyms()
        expected = ["ssz", "kzg", "das", "pbs", "mev", "evm", "ffg", "rlp", "eip"]
        for abbrev in expected:
            assert abbrev in synonyms, f"Abbreviation {abbrev!r} missing from synonyms"

    def test_ssz_expands_to_simple_serialize(self) -> None:
        """Verify a specific synonym expansion works correctly."""
        synonyms = get_ethereum_synonyms()
        assert "simple serialize" in synonyms["ssz"]
        assert "ssz" in synonyms["simple serialize"]

    def test_multi_expansion_abbreviation(self) -> None:
        """Abbreviations with multiple expansions include all of them."""
        synonyms = get_ethereum_synonyms()
        # MEV has two expansions
        assert "maximal extractable value" in synonyms["mev"]
        assert "miner extractable value" in synonyms["mev"]
        # Cross-expansion: each expansion maps to the other
        assert "miner extractable value" in synonyms["maximal extractable value"]

    def test_returns_copy_not_reference(self) -> None:
        """Mutating the returned dict must not affect future calls."""
        s1 = get_ethereum_synonyms()
        s1["test_key"] = ["test_value"]
        s2 = get_ethereum_synonyms()
        assert "test_key" not in s2


# ===================================================================
# Dictionary structure
# ===================================================================


class TestDictionary:
    """Validate the custom dictionary entries."""

    def test_dictionary_is_list_of_strings(self) -> None:
        dictionary = get_ethereum_dictionary()
        assert isinstance(dictionary, list)
        for entry in dictionary:
            assert isinstance(entry, str), f"Dictionary entry {entry!r} is not a string"

    def test_dictionary_not_empty(self) -> None:
        dictionary = get_ethereum_dictionary()
        assert len(dictionary) > 0

    def test_known_terms_present(self) -> None:
        """Spot-check that key compound terms are in the dictionary."""
        dictionary = get_ethereum_dictionary()
        expected = ["proto-danksharding", "single-slot-finality", "eip-4844"]
        for term in expected:
            assert term in dictionary, f"Term {term!r} missing from dictionary"

    def test_no_duplicates(self) -> None:
        dictionary = get_ethereum_dictionary()
        assert len(dictionary) == len(set(dictionary))

    def test_returns_copy_not_reference(self) -> None:
        """Mutating the returned list must not affect future calls."""
        d1 = get_ethereum_dictionary()
        d1.append("bogus-term")
        d2 = get_ethereum_dictionary()
        assert "bogus-term" not in d2


# ===================================================================
# apply_terminology_settings (mocked HTTP)
# ===================================================================


def _make_resp(body: dict) -> MagicMock:
    """Create a mock HTTP response with the given JSON body."""
    resp = MagicMock()
    resp.read.return_value = json.dumps(body).encode()
    return resp


def _mock_urlopen_factory(
    task1_statuses: list[str],
    task2_statuses: list[str] | None = None,
) -> list[MagicMock]:
    """Return mock urlopen responses in the interleaved call order.

    Actual call order: PUT synonyms, poll task 1 (×N), PUT dictionary,
    poll task 2 (×N).  *task1_statuses* and *task2_statuses* list the
    status values returned for each poll.  If *task2_statuses* is None,
    a single "succeeded" is used.
    """
    if task2_statuses is None:
        task2_statuses = ["succeeded"]
    responses: list[MagicMock] = []
    # PUT synonyms
    responses.append(_make_resp({"taskUid": 1}))
    # Poll task 1
    for status in task1_statuses:
        body: dict = {"status": status}
        if status == "failed":
            body["error"] = {"message": "test error"}
        responses.append(_make_resp(body))
    # PUT dictionary
    responses.append(_make_resp({"taskUid": 2}))
    # Poll task 2
    for status in task2_statuses:
        body = {"status": status}
        if status == "failed":
            body["error"] = {"message": "test error"}
        responses.append(_make_resp(body))
    return responses


class TestApplyTerminologySettings:
    """Test apply_terminology_settings with mocked HTTP."""

    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_sends_put_requests(self, mock_urlopen: MagicMock) -> None:
        """Verifies PUT requests sent for both synonyms and dictionary."""
        mock_urlopen.side_effect = _mock_urlopen_factory(["succeeded"])

        apply_terminology_settings("http://meili:7700", "testkey", "my_index")

        # 4 calls: PUT synonyms, GET task 1, PUT dictionary, GET task 2
        assert mock_urlopen.call_count == 4
        # First call is PUT synonyms
        req0 = mock_urlopen.call_args_list[0][0][0]
        assert req0.full_url == "http://meili:7700/indexes/my_index/settings/synonyms"
        assert req0.method == "PUT"
        assert req0.get_header("Authorization") == "Bearer testkey"
        # Third call is PUT dictionary
        req2 = mock_urlopen.call_args_list[2][0][0]
        assert req2.full_url == "http://meili:7700/indexes/my_index/settings/dictionary"
        assert req2.method == "PUT"

    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_synonyms_payload_contains_expected_keys(self, mock_urlopen: MagicMock) -> None:
        """The PUT synonyms payload includes our synonym keys."""
        mock_urlopen.side_effect = _mock_urlopen_factory(["succeeded"])

        apply_terminology_settings("http://meili:7700", "k", "idx")

        req0 = mock_urlopen.call_args_list[0][0][0]
        payload = json.loads(req0.data)
        assert "ssz" in payload
        assert "simple serialize" in payload["ssz"]

    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_dictionary_payload_contains_expected_terms(self, mock_urlopen: MagicMock) -> None:
        """The PUT dictionary payload includes compound terms."""
        mock_urlopen.side_effect = _mock_urlopen_factory(["succeeded"])

        apply_terminology_settings("http://meili:7700", "k", "idx")

        # Dictionary PUT is the 3rd call (index 2)
        req2 = mock_urlopen.call_args_list[2][0][0]
        payload = json.loads(req2.data)
        assert isinstance(payload, list)
        assert "proto-danksharding" in payload

    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_task_failure_raises_runtime_error(self, mock_urlopen: MagicMock) -> None:
        """A failed Meilisearch task raises RuntimeError."""
        mock_urlopen.side_effect = _mock_urlopen_factory(["failed"])

        with pytest.raises(RuntimeError, match="test error"):
            apply_terminology_settings("http://meili:7700", "k", "idx")

    @patch("erd_index.index.terminology.time.sleep")
    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_polls_until_succeeded(self, mock_urlopen: MagicMock, mock_sleep: MagicMock) -> None:
        """Task polling retries on 'enqueued'/'processing' until 'succeeded'."""
        mock_urlopen.side_effect = _mock_urlopen_factory(
            ["enqueued", "processing", "succeeded"]
        )

        apply_terminology_settings("http://meili:7700", "k", "idx")

        # PUT synonyms + 3 polls + PUT dictionary + 1 poll = 6
        assert mock_urlopen.call_count == 6
        # sleep called between polls (2 sleeps for enqueued+processing)
        assert mock_sleep.call_count >= 2

    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_no_auth_header_when_key_empty(self, mock_urlopen: MagicMock) -> None:
        """Empty admin key should not set Authorization header."""
        mock_urlopen.side_effect = _mock_urlopen_factory(["succeeded"])

        apply_terminology_settings("http://meili:7700", "", "idx")

        req0 = mock_urlopen.call_args_list[0][0][0]
        assert not req0.has_header("Authorization")

    @patch("erd_index.index.terminology.time.sleep")
    @patch("erd_index.index.terminology.urllib.request.urlopen")
    def test_timeout_raises_on_max_polls(self, mock_urlopen: MagicMock, mock_sleep: MagicMock) -> None:
        """Exceeding max_polls raises TimeoutError."""
        # All polls return "processing" — never succeeds
        responses: list[MagicMock] = []
        responses.append(_make_resp({"taskUid": 1}))
        for _ in range(120):
            responses.append(_make_resp({"status": "processing"}))
        mock_urlopen.side_effect = responses

        with pytest.raises(TimeoutError, match="did not complete"):
            apply_terminology_settings("http://meili:7700", "k", "idx")
