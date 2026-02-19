"""Tests for scripts/batch_embed.py — batch embedding pipeline."""

from __future__ import annotations

import json
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.batch_embed import (
    build_text,
    checkpoint_path,
    load_checkpoint,
    save_checkpoint,
)

# ===================================================================
# build_text
# ===================================================================


class TestBuildText:
    def test_title_and_text(self) -> None:
        doc = {"title": "Proto-danksharding FAQ", "text": "This explains EIP-4844."}
        assert build_text(doc) == "Proto-danksharding FAQ This explains EIP-4844."

    def test_text_only(self) -> None:
        doc = {"text": "Some content without a title."}
        assert build_text(doc) == "Some content without a title."

    def test_title_only(self) -> None:
        doc = {"title": "Just a Title"}
        assert build_text(doc) == "Just a Title"

    def test_empty_doc(self) -> None:
        assert build_text({}) == ""

    def test_empty_strings(self) -> None:
        doc = {"title": "", "text": ""}
        assert build_text(doc) == ""

    def test_none_values(self) -> None:
        doc = {"title": None, "text": None}
        assert build_text(doc) == ""

    def test_whitespace_title(self) -> None:
        """Non-empty whitespace title is included."""
        doc = {"title": "  ", "text": "body"}
        assert build_text(doc) == "   body"

    def test_mirrors_meilisearch_template(self) -> None:
        """Verify our build_text matches the Meilisearch documentTemplate behavior.

        Template: ``{% if doc.title %}{{doc.title}} {% endif %}{{doc.text}}``
        """
        # Both present: "title text"
        assert build_text({"title": "T", "text": "B"}) == "T B"
        # No title: just text
        assert build_text({"text": "B"}) == "B"
        # No text: just title
        assert build_text({"title": "T"}) == "T"

    # --- asymmetric mode ---

    def test_asymmetric_title_and_text(self) -> None:
        doc = {"title": "EIP-4844", "text": "Proto-danksharding introduces blobs."}
        assert build_text(doc, asymmetric=True) == "title: EIP-4844 | text: Proto-danksharding introduces blobs."

    def test_asymmetric_text_only(self) -> None:
        doc = {"text": "Some content without a title."}
        assert build_text(doc, asymmetric=True) == "title: none | text: Some content without a title."

    def test_asymmetric_title_only(self) -> None:
        doc = {"title": "Just a Title"}
        assert build_text(doc, asymmetric=True) == "title: Just a Title | text: "

    def test_asymmetric_empty_doc(self) -> None:
        assert build_text({}, asymmetric=True) == "title: none | text: "

    def test_asymmetric_none_values(self) -> None:
        doc = {"title": None, "text": None}
        assert build_text(doc, asymmetric=True) == "title: none | text: "

    def test_asymmetric_empty_strings(self) -> None:
        doc = {"title": "", "text": ""}
        assert build_text(doc, asymmetric=True) == "title: none | text: "

    def test_default_mode_unchanged(self) -> None:
        """Explicitly passing asymmetric=False should match default behavior."""
        doc = {"title": "T", "text": "B"}
        assert build_text(doc, asymmetric=False) == build_text(doc)


class TestAsymmetricCLIFlag:
    def test_flag_present(self) -> None:
        from scripts.batch_embed import build_parser
        args = build_parser().parse_args(["--asymmetric"])
        assert args.asymmetric is True

    def test_flag_absent(self) -> None:
        from scripts.batch_embed import build_parser
        args = build_parser().parse_args([])
        assert args.asymmetric is False


# ===================================================================
# Checkpoint management
# ===================================================================


class TestCheckpointPath:
    def test_returns_json_file(self) -> None:
        path = checkpoint_path(Path("/tmp/test"), "my_index")
        assert path == Path("/tmp/test/my_index.json")

    def test_different_indexes(self) -> None:
        a = checkpoint_path(Path("/tmp"), "index_a")
        b = checkpoint_path(Path("/tmp"), "index_b")
        assert a != b


class TestLoadCheckpoint:
    def test_missing_file_returns_fresh_state(self, tmp_path: Path) -> None:
        ckpt = load_checkpoint(tmp_path, "nonexistent")
        assert ckpt == {"offset": 0, "embedded": 0, "failed_batches": [], "failed_docs": 0}

    def test_loads_existing_checkpoint(self, tmp_path: Path) -> None:
        data = {"offset": 5000, "embedded": 5000, "failed_batches": [], "failed_docs": 0}
        (tmp_path / "test_idx.json").write_text(json.dumps(data))
        ckpt = load_checkpoint(tmp_path, "test_idx")
        assert ckpt == data

    def test_corrupt_json_returns_fresh_state(self, tmp_path: Path) -> None:
        (tmp_path / "bad.json").write_text("not valid json{{{")
        ckpt = load_checkpoint(tmp_path, "bad")
        assert ckpt["offset"] == 0

    def test_preserves_failed_batches(self, tmp_path: Path) -> None:
        data = {
            "offset": 3000,
            "embedded": 2900,
            "failed_batches": [{"offset": 2000, "error": "timeout"}],
            "failed_docs": 100,
        }
        (tmp_path / "idx.json").write_text(json.dumps(data))
        ckpt = load_checkpoint(tmp_path, "idx")
        assert len(ckpt["failed_batches"]) == 1
        assert ckpt["failed_docs"] == 100


class TestSaveCheckpoint:
    def test_creates_directory_and_file(self, tmp_path: Path) -> None:
        ckpt_dir = tmp_path / "subdir" / "deep"
        data = {"offset": 1000, "embedded": 1000, "failed_batches": [], "failed_docs": 0}
        save_checkpoint(ckpt_dir, "test", data)
        assert (ckpt_dir / "test.json").exists()
        loaded = json.loads((ckpt_dir / "test.json").read_text())
        assert loaded == data

    def test_overwrites_existing(self, tmp_path: Path) -> None:
        save_checkpoint(tmp_path, "idx", {"offset": 100, "embedded": 100, "failed_batches": [], "failed_docs": 0})
        save_checkpoint(tmp_path, "idx", {"offset": 200, "embedded": 200, "failed_batches": [], "failed_docs": 0})
        loaded = json.loads((tmp_path / "idx.json").read_text())
        assert loaded["offset"] == 200

    def test_atomic_write_no_temp_files_left(self, tmp_path: Path) -> None:
        """After save, no .tmp files should remain in the directory."""
        save_checkpoint(tmp_path, "idx", {"offset": 0, "embedded": 0, "failed_batches": [], "failed_docs": 0})
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert tmp_files == []

    def test_content_is_valid_json(self, tmp_path: Path) -> None:
        data = {
            "offset": 5000,
            "embedded": 4900,
            "failed_batches": [{"offset": 3000, "error": "connection reset"}],
            "failed_docs": 100,
        }
        save_checkpoint(tmp_path, "idx", data)
        # Should not raise
        loaded = json.loads((tmp_path / "idx.json").read_text())
        assert loaded["failed_batches"][0]["error"] == "connection reset"

    def test_roundtrip(self, tmp_path: Path) -> None:
        """save then load should return identical data."""
        original = {
            "offset": 42000,
            "embedded": 41500,
            "failed_batches": [{"offset": 10000, "error": "test"}],
            "failed_docs": 500,
        }
        save_checkpoint(tmp_path, "roundtrip", original)
        loaded = load_checkpoint(tmp_path, "roundtrip")
        assert loaded == original


# ===================================================================
# embed_texts (with mocked Ollama)
# ===================================================================


class TestEmbedTexts:
    """Tests for embed_texts using mocked HTTP responses."""

    def _mock_response(self, embeddings: list[list[float]]) -> MagicMock:
        """Create a mock urllib response returning the given embeddings."""
        mock = MagicMock()
        mock.read.return_value = json.dumps({"embeddings": embeddings}).encode()
        mock.__enter__ = lambda s: s
        mock.__exit__ = MagicMock(return_value=False)
        return mock

    @patch("scripts.batch_embed.urllib.request.urlopen")
    def test_returns_embeddings(self, mock_urlopen: MagicMock) -> None:
        from scripts.batch_embed import embed_texts

        expected = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_urlopen.return_value = self._mock_response(expected)
        result = embed_texts(["hello", "world"], "test-model")
        assert result == expected

    @patch("scripts.batch_embed.urllib.request.urlopen")
    def test_single_text(self, mock_urlopen: MagicMock) -> None:
        from scripts.batch_embed import embed_texts

        expected = [[0.1, 0.2]]
        mock_urlopen.return_value = self._mock_response(expected)
        result = embed_texts(["single"], "test-model")
        assert len(result) == 1

    @patch("scripts.batch_embed.urllib.request.urlopen")
    def test_validates_response_count(self, mock_urlopen: MagicMock) -> None:
        from scripts.batch_embed import embed_texts

        # Return 1 embedding for 2 inputs
        mock_urlopen.return_value = self._mock_response([[0.1, 0.2]])
        with pytest.raises(ValueError, match="Expected 2 embeddings"):
            embed_texts(["a", "b"], "test-model", retry_count=1)

    @patch("scripts.batch_embed.urllib.request.urlopen")
    def test_retries_on_transient_error(self, mock_urlopen: MagicMock) -> None:
        from scripts.batch_embed import embed_texts

        # First call: 503, second call: success
        error = urllib_http_error(503)
        expected = [[0.1]]
        mock_urlopen.side_effect = [error, self._mock_response(expected)]
        result = embed_texts(["test"], "model", retry_count=2)
        assert result == expected
        assert mock_urlopen.call_count == 2

    @patch("scripts.batch_embed.urllib.request.urlopen")
    def test_raises_on_non_transient_error(self, mock_urlopen: MagicMock) -> None:
        from scripts.batch_embed import embed_texts

        mock_urlopen.side_effect = urllib_http_error(400)
        with pytest.raises(urllib.error.HTTPError):
            embed_texts(["test"], "model", retry_count=3)
        assert mock_urlopen.call_count == 1  # no retries for 400


def urllib_http_error(code: int) -> urllib.error.HTTPError:
    """Create a urllib HTTPError with the given status code."""
    return urllib.error.HTTPError(
        url="http://test", code=code, msg="test", hdrs=None, fp=None  # type: ignore[arg-type]
    )
