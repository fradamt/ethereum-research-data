"""Tests for erd_index.embed_proxy — splitting proxy for Ollama /api/embed.

All Ollama HTTP interactions are mocked so tests run without a server.
"""

from __future__ import annotations

import concurrent.futures
import io
import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from erd_index.embed_proxy import (
    DEFAULT_DIMENSIONS,
    DEFAULT_MAX_TOKENS,
    _embed_adaptive,
    _embed_single_batch,
    _request_with_retry,
    avg_embeddings,
    configure_handler,
    count_tokens,
    embed_batch,
    embed_batch_concurrent,
    embed_batch_concurrent_safe,
    load_tokenizer,
    split_text,
    split_text_by_tokens,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ollama_response(embeddings: list[list[float]]) -> bytes:
    """Encode an Ollama-style JSON response."""
    return json.dumps({"embeddings": embeddings}).encode()


def _make_http_error(code: int, body: bytes = b"{}") -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        url="http://localhost:11434/api/embed",
        code=code,
        msg=f"HTTP {code}",
        hdrs={},  # type: ignore[arg-type]
        fp=io.BytesIO(body),
    )


# ===================================================================
# split_text
# ===================================================================


class TestSplitText:
    """split_text splits on paragraph/newline boundaries."""

    def test_empty_string(self) -> None:
        assert split_text("", 100) == [""]

    def test_short_text_unchanged(self) -> None:
        text = "Hello world"
        assert split_text(text, 100) == [text]

    def test_exact_boundary(self) -> None:
        text = "a" * 100
        assert split_text(text, 100) == [text]

    def test_splits_on_paragraph_boundary(self) -> None:
        para1 = "A" * 40
        para2 = "B" * 40
        text = f"{para1}\n\n{para2}"
        # max_chars=50: paragraph break is at position 40, which is >= 50//2=25
        chunks = split_text(text, 50)
        assert len(chunks) == 2
        assert chunks[0] == para1
        assert chunks[1] == para2

    def test_splits_on_newline_when_no_paragraph(self) -> None:
        line1 = "A" * 40
        line2 = "B" * 40
        text = f"{line1}\n{line2}"
        chunks = split_text(text, 50)
        assert len(chunks) == 2
        assert chunks[0] == line1
        assert chunks[1] == line2

    def test_hard_split_when_no_boundary(self) -> None:
        text = "A" * 200
        chunks = split_text(text, 100)
        assert len(chunks) == 2
        assert chunks[0] == "A" * 100
        assert chunks[1] == "A" * 100

    def test_strips_leading_whitespace_after_split(self) -> None:
        text = "A" * 40 + "\n\n   " + "B" * 40
        chunks = split_text(text, 50)
        assert len(chunks) == 2
        assert not chunks[1].startswith(" ")

    def test_prefers_paragraph_over_newline(self) -> None:
        # Paragraph break at 30, newline at 45 — both >= max//2=25
        text = "A" * 30 + "\n\n" + "B" * 13 + "\n" + "C" * 40
        chunks = split_text(text, 50)
        # rfind("\n\n", 0, 50) finds the paragraph at position 30
        assert chunks[0] == "A" * 30

    def test_falls_back_to_newline_when_paragraph_too_early(self) -> None:
        # Paragraph break at position 5 (< max//2=25), newline at 40
        text = "A" * 5 + "\n\n" + "B" * 33 + "\n" + "C" * 40
        chunks = split_text(text, 50)
        # Paragraph at 5 < 25, so rfind("\n") is tried: newline at 40 >= 25
        assert len(chunks[0]) == 40

    def test_multiple_chunks(self) -> None:
        paras = [f"Para{i} " + "x" * 30 for i in range(5)]
        text = "\n\n".join(paras)
        chunks = split_text(text, 50)
        assert len(chunks) >= 3


# ===================================================================
# split_text_by_tokens
# ===================================================================


class TestSplitTextByTokens:
    """split_text_by_tokens uses the BERT tokenizer for accurate splitting."""

    def test_tokenizer_loads(self) -> None:
        tok = load_tokenizer()
        assert tok is not None

    def test_count_tokens_short(self) -> None:
        n = count_tokens("Hello world")
        assert n is not None
        assert 3 <= n <= 5  # [CLS] hello world [SEP]

    def test_short_text_not_split(self) -> None:
        text = "Hello world, this is a short sentence."
        chunks = split_text_by_tokens(text, DEFAULT_MAX_TOKENS)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_empty_string(self) -> None:
        assert split_text_by_tokens("", 100) == [""]

    def test_splits_long_prose(self) -> None:
        """A long text exceeding token budget gets split."""
        # ~800 tokens of prose should split at max_tokens=500
        prose = "The Ethereum protocol uses proof of stake. " * 100
        chunks = split_text_by_tokens(prose, 500)
        assert len(chunks) >= 2
        # Each chunk should be under the limit
        for chunk in chunks:
            n = count_tokens(chunk)
            assert n is not None
            assert n <= 500, f"Chunk has {n} tokens, expected <= 500"

    def test_splits_hex_heavy_content(self) -> None:
        """Hex addresses (high token density) split correctly by token count."""
        addrs = "\n".join(["0x" + "ab" * 20 for _ in range(100)])
        chunks = split_text_by_tokens(addrs, 500)
        assert len(chunks) >= 2
        for chunk in chunks:
            n = count_tokens(chunk)
            assert n is not None
            assert n <= 500

    def test_respects_paragraph_boundaries(self) -> None:
        """Splits prefer paragraph boundaries over arbitrary positions."""
        para1 = "Word " * 200  # ~200 tokens
        para2 = "Token " * 200  # ~200 tokens
        text = para1.strip() + "\n\n" + para2.strip()
        chunks = split_text_by_tokens(text, 250)
        # Should split at the paragraph boundary
        assert len(chunks) == 2
        assert "Word" in chunks[0]
        assert "Token" in chunks[1]

    def test_all_chunks_within_budget(self) -> None:
        """Every chunk produced is within the token budget."""
        # Mixed content: prose + hex to create variable density
        mixed = (
            "The beacon chain finalizes blocks through Casper FFG.\n" * 20
            + "\n0x" + "ff" * 20 + "\n" + "0x" + "aa" * 20 + "\n"
            + "Validators attest to the head of the chain.\n" * 20
        )
        max_tok = 300
        chunks = split_text_by_tokens(mixed, max_tok)
        for i, chunk in enumerate(chunks):
            n = count_tokens(chunk)
            assert n is not None
            assert n <= max_tok, f"Chunk {i} has {n} tokens (max {max_tok})"


# ===================================================================
# avg_embeddings
# ===================================================================


class TestAvgEmbeddings:
    """avg_embeddings computes element-wise average."""

    def test_single_vector(self) -> None:
        result = avg_embeddings([[1.0, 2.0, 3.0]])
        assert result == [1.0, 2.0, 3.0]

    def test_two_vectors(self) -> None:
        result = avg_embeddings([[1.0, 0.0], [3.0, 4.0]])
        assert result == [2.0, 2.0]

    def test_three_vectors(self) -> None:
        result = avg_embeddings([[3.0, 6.0, 9.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        assert result == [1.0, 2.0, 3.0]

    def test_preserves_dimension(self) -> None:
        vecs = [[float(i) for i in range(128)] for _ in range(3)]
        result = avg_embeddings(vecs)
        assert len(result) == 128


# ===================================================================
# _request_with_retry
# ===================================================================


class TestRequestWithRetry:
    """_request_with_retry handles retries and error propagation."""

    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_success_first_attempt(self, mock_urlopen: MagicMock) -> None:
        embs = [[1.0, 2.0]]
        mock_resp = MagicMock()
        mock_resp.read.return_value = _ollama_response(embs)
        mock_urlopen.return_value = mock_resp

        result = _request_with_retry("http://localhost/api/embed", b"{}", retry_count=3)
        assert result == embs
        assert mock_urlopen.call_count == 1

    @patch("erd_index.embed_proxy.time.sleep")
    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_retries_on_transient_502(
        self, mock_urlopen: MagicMock, mock_sleep: MagicMock
    ) -> None:
        embs = [[1.0]]
        mock_resp = MagicMock()
        mock_resp.read.return_value = _ollama_response(embs)
        mock_urlopen.side_effect = [
            _make_http_error(502),
            mock_resp,
        ]

        result = _request_with_retry("http://localhost/api/embed", b"{}", retry_count=3)
        assert result == embs
        assert mock_urlopen.call_count == 2
        mock_sleep.assert_called_once()

    @patch("erd_index.embed_proxy.time.sleep")
    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_retries_on_url_error(
        self, mock_urlopen: MagicMock, mock_sleep: MagicMock
    ) -> None:
        embs = [[2.0]]
        mock_resp = MagicMock()
        mock_resp.read.return_value = _ollama_response(embs)
        mock_urlopen.side_effect = [
            urllib.error.URLError("Connection refused"),
            mock_resp,
        ]

        result = _request_with_retry("http://localhost/api/embed", b"{}", retry_count=3)
        assert result == embs
        assert mock_urlopen.call_count == 2

    @patch("erd_index.embed_proxy.time.sleep")
    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_raises_after_all_retries_exhausted(
        self, mock_urlopen: MagicMock, mock_sleep: MagicMock
    ) -> None:
        mock_urlopen.side_effect = [
            _make_http_error(503),
            _make_http_error(503),
            _make_http_error(503),
        ]

        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _request_with_retry("http://localhost/api/embed", b"{}", retry_count=3)
        assert exc_info.value.code == 503
        assert mock_urlopen.call_count == 3

    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_non_transient_error_raises_immediately(
        self, mock_urlopen: MagicMock
    ) -> None:
        mock_urlopen.side_effect = _make_http_error(400)

        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _request_with_retry("http://localhost/api/embed", b"{}", retry_count=3)
        assert exc_info.value.code == 400
        assert mock_urlopen.call_count == 1

    @patch("erd_index.embed_proxy.time.sleep")
    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_exponential_backoff_timing(
        self, mock_urlopen: MagicMock, mock_sleep: MagicMock
    ) -> None:
        mock_urlopen.side_effect = [
            _make_http_error(502),
            _make_http_error(502),
            _make_http_error(502),
        ]

        with pytest.raises(urllib.error.HTTPError):
            _request_with_retry("http://localhost/api/embed", b"{}", retry_count=3)

        # Back-off: 0.5, 1.0, 2.0
        waits = [call.args[0] for call in mock_sleep.call_args_list]
        assert waits == [0.5, 1.0, 2.0]

    @patch("erd_index.embed_proxy.time.sleep")
    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_url_error_exhausts_retries(
        self, mock_urlopen: MagicMock, mock_sleep: MagicMock
    ) -> None:
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        with pytest.raises(urllib.error.URLError):
            _request_with_retry("http://localhost/api/embed", b"{}", retry_count=2)
        assert mock_urlopen.call_count == 2

    @patch("erd_index.embed_proxy.time.sleep")
    @patch("erd_index.embed_proxy.urllib.request.urlopen")
    def test_retries_all_transient_codes(
        self, mock_urlopen: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """All transient codes (502, 503, 504, 408) trigger retries."""
        embs = [[1.0]]
        mock_resp = MagicMock()
        mock_resp.read.return_value = _ollama_response(embs)
        for code in (502, 503, 504, 408):
            mock_urlopen.reset_mock()
            mock_urlopen.side_effect = [_make_http_error(code), mock_resp]
            result = _request_with_retry(
                "http://localhost/api/embed", b"{}", retry_count=3
            )
            assert result == embs, f"Should retry on {code}"


# ===================================================================
# embed_batch (sequential)
# ===================================================================


class TestEmbedBatch:
    """embed_batch sends texts in sequential sub-batches."""

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_single_batch(self, mock_single: MagicMock) -> None:
        embs = [[1.0], [2.0]]
        mock_single.return_value = embs

        result = embed_batch(
            ["a", "b"], "model", ollama_url="http://x", batch_size=10, retry_count=3
        )
        assert result == embs
        mock_single.assert_called_once_with(["a", "b"], "model", "http://x", 3)

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_multiple_batches(self, mock_single: MagicMock) -> None:
        mock_single.side_effect = [[[1.0]], [[2.0]], [[3.0]]]

        result = embed_batch(
            ["a", "b", "c"], "model", ollama_url="http://x", batch_size=1, retry_count=3
        )
        assert result == [[1.0], [2.0], [3.0]]
        assert mock_single.call_count == 3

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_error_propagates(self, mock_single: MagicMock) -> None:
        mock_single.side_effect = _make_http_error(500)

        with pytest.raises(urllib.error.HTTPError):
            embed_batch(
                ["a"], "model", ollama_url="http://x", batch_size=10, retry_count=3
            )


# ===================================================================
# embed_batch_concurrent
# ===================================================================


class TestEmbedBatchConcurrent:
    """embed_batch_concurrent sends sub-batches via a thread pool."""

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_returns_embeddings_in_order(self, mock_single: MagicMock) -> None:
        # Map each text to a unique embedding so order is deterministic
        # regardless of thread scheduling.
        text_to_emb = {"a": [[1.0]], "b": [[2.0]], "c": [[3.0]]}
        mock_single.side_effect = lambda texts, *a, **kw: text_to_emb[texts[0]]

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            result = embed_batch_concurrent(
                ["a", "b", "c"],
                "model",
                ollama_url="http://x",
                batch_size=1,
                retry_count=3,
                executor=executor,
            )
        assert result == [[1.0], [2.0], [3.0]]

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_empty_input(self, mock_single: MagicMock) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            result = embed_batch_concurrent(
                [], "model", ollama_url="http://x", batch_size=10, executor=executor
            )
        assert result == []
        mock_single.assert_not_called()

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_batching(self, mock_single: MagicMock) -> None:
        mock_single.side_effect = [
            [[1.0], [2.0]],  # batch 1
            [[3.0]],  # batch 2
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            result = embed_batch_concurrent(
                ["a", "b", "c"],
                "model",
                ollama_url="http://x",
                batch_size=2,
                retry_count=3,
                executor=executor,
            )
        assert result == [[1.0], [2.0], [3.0]]
        assert mock_single.call_count == 2

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_error_propagates_no_partial_results(self, mock_single: MagicMock) -> None:
        """If any sub-batch fails, the error propagates — no partial results."""
        mock_single.side_effect = _make_http_error(502)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            with pytest.raises(urllib.error.HTTPError):
                embed_batch_concurrent(
                    ["a", "b"],
                    "model",
                    ollama_url="http://x",
                    batch_size=1,
                    retry_count=1,
                    executor=executor,
                )


# ===================================================================
# embed_batch_concurrent_safe
# ===================================================================


class TestEmbedBatchConcurrentSafe:
    """embed_batch_concurrent_safe retries failed sub-batches individually."""

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_all_succeed(self, mock_single: MagicMock) -> None:
        mock_single.side_effect = [[[1.0], [2.0]], [[3.0]]]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            result = embed_batch_concurrent_safe(
                ["a", "b", "c"], "model",
                ollama_url="http://x", batch_size=2, retry_count=1, executor=executor,
            )
        assert result == [[1.0], [2.0], [3.0]]

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_batch_fails_retries_individually(self, mock_single: MagicMock) -> None:
        """When a batch of 2 fails, each text is retried individually."""
        mock_single.side_effect = [
            RuntimeError("batch failed"),  # batch ["a","b"] fails
            [[3.0]],                       # batch ["c"] succeeds
            [[1.0]],                       # individual retry "a" succeeds
            [[2.0]],                       # individual retry "b" succeeds
        ]
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            result = embed_batch_concurrent_safe(
                ["a", "b", "c"], "model",
                ollama_url="http://x", batch_size=2, retry_count=1, executor=executor,
            )
        assert result == [[1.0], [2.0], [3.0]]
        assert mock_single.call_count == 4

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_individual_retry_isolates_bad_input(self, mock_single: MagicMock) -> None:
        """One bad input in a batch: batch fails, individual retry isolates it."""
        mock_single.side_effect = [
            RuntimeError("batch failed"),  # batch ["good","bad"] fails
            [[1.0]],                       # individual retry "good" succeeds
            RuntimeError("still bad"),     # individual retry "bad" fails
        ]
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            result = embed_batch_concurrent_safe(
                ["good", "bad"], "model",
                ollama_url="http://x", batch_size=2, retry_count=1, executor=executor,
            )
        assert result[0] == [1.0]
        assert result[1] is None

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_empty_input(self, mock_single: MagicMock) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            result = embed_batch_concurrent_safe(
                [], "model", ollama_url="http://x", batch_size=10, executor=executor,
            )
        assert result == []
        mock_single.assert_not_called()


# ===================================================================
# _ProxyHandler.do_POST (integration via configure_handler)
# ===================================================================


class TestProxyHandler:
    """Integration tests for the HTTP handler with mocked Ollama."""

    def _post(
        self,
        handler_class: type,
        body: dict | bytes,
    ) -> tuple[int, dict]:
        """Simulate a POST request to the handler and return (status, json_body)."""
        if isinstance(body, dict):
            raw = json.dumps(body).encode()
        else:
            raw = body

        # Build a mock request object
        handler = object.__new__(handler_class)
        handler.rfile = io.BytesIO(raw)
        handler.wfile = io.BytesIO()
        handler.headers = {"Content-Length": str(len(raw))}
        handler.requestline = "POST /api/embed HTTP/1.1"
        handler.client_address = ("127.0.0.1", 12345)
        handler.request_version = "HTTP/1.1"
        handler.command = "POST"

        # Capture response
        responses: list[int] = []

        def mock_send_response(code: int) -> None:
            responses.append(code)

        def mock_send_header(key: str, val: str) -> None:
            pass

        def mock_end_headers() -> None:
            pass

        handler.send_response = mock_send_response
        handler.send_header = mock_send_header
        handler.end_headers = mock_end_headers

        handler.do_POST()

        status = responses[0] if responses else 0
        handler.wfile.seek(0)
        resp_body = handler.wfile.read()
        try:
            resp_json = json.loads(resp_body)
        except (json.JSONDecodeError, ValueError):
            resp_json = {}
        return status, resp_json

    def _configured_handler(
        self, max_chars: int = 4000, batch_size: int = 10
    ) -> type:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        return configure_handler(
            max_chars=max_chars,
            ollama_url="http://mock-ollama/api/embed",
            batch_size=batch_size,
            executor=executor,
        )

    def test_invalid_json(self) -> None:
        handler_cls = self._configured_handler()
        status, body = self._post(handler_cls, b"not json{{{")
        assert status == 400
        assert "error" in body

    def test_empty_input_returns_empty(self) -> None:
        handler_cls = self._configured_handler()
        status, body = self._post(handler_cls, {"model": "m", "input": []})
        assert status == 200
        assert body == {"embeddings": []}

    def test_string_input_normalized_to_list(self) -> None:
        handler_cls = self._configured_handler()
        with patch(
            "erd_index.embed_proxy.embed_batch_concurrent_safe",
            return_value=[[1.0, 2.0]],
        ):
            status, body = self._post(
                handler_cls, {"model": "m", "input": "single string"}
            )
        assert status == 200
        assert body["embeddings"] == [[1.0, 2.0]]

    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_short_inputs_no_split(self, mock_safe: MagicMock) -> None:
        # All chunks batched in one call
        mock_safe.return_value = [[1.0], [2.0]]
        handler_cls = self._configured_handler(max_chars=4000)

        status, body = self._post(
            handler_cls, {"model": "m", "input": ["short1", "short2"]}
        )
        assert status == 200
        assert body["embeddings"] == [[1.0], [2.0]]
        # One call with all chunks
        assert mock_safe.call_count == 1
        assert mock_safe.call_args[0][0] == ["short1", "short2"]

    @patch("erd_index.embed_proxy.load_tokenizer", return_value=None)
    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_long_input_split_and_averaged(
        self, mock_safe: MagicMock, _mock_tok: MagicMock
    ) -> None:
        # Two sub-chunks for the long input (char-based splitting via mock)
        mock_safe.return_value = [[2.0, 4.0], [4.0, 8.0]]
        handler_cls = self._configured_handler(max_chars=50)

        long_text = "A" * 40 + "\n\n" + "B" * 40
        status, body = self._post(handler_cls, {"model": "m", "input": [long_text]})

        assert status == 200
        embs = body["embeddings"]
        assert len(embs) == 1
        # Average of [2,4] and [4,8] = [3,6]
        assert embs[0] == [3.0, 6.0]

    @patch("erd_index.embed_proxy.load_tokenizer", return_value=None)
    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_mixed_short_and_long(
        self, mock_safe: MagicMock, _mock_tok: MagicMock
    ) -> None:
        """Short input (1 chunk) + long input (2 chunks) = 3 chunks total."""
        # All 3 chunks in one batched call (char-based splitting via mock)
        mock_safe.return_value = [[1.0, 1.0], [2.0, 4.0], [4.0, 8.0]]
        handler_cls = self._configured_handler(max_chars=50)

        short = "short"
        long_text = "A" * 40 + "\n\n" + "B" * 40
        status, body = self._post(
            handler_cls, {"model": "m", "input": [short, long_text]}
        )

        assert status == 200
        embs = body["embeddings"]
        assert len(embs) == 2
        assert embs[0] == [1.0, 1.0]  # short: single chunk, no averaging
        assert embs[1] == [3.0, 6.0]  # long: avg of [2,4] and [4,8]

    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_failed_input_returns_zero_vector(self, mock_safe: MagicMock) -> None:
        """A failed input produces a zero vector instead of aborting the batch."""
        # All chunks failed (None)
        mock_safe.return_value = [None]
        handler_cls = self._configured_handler()

        status, body = self._post(
            handler_cls, {"model": "m", "input": ["text"]}
        )
        assert status == 200
        embs = body["embeddings"]
        assert len(embs) == 1
        assert embs[0] == [0.0] * DEFAULT_DIMENSIONS
        assert handler_cls.stats["failed"] == 1

    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_mixed_success_and_failure(self, mock_safe: MagicMock) -> None:
        """Good inputs succeed, bad inputs get zero vectors — batch still returns 200."""
        # 3 inputs: good (1 chunk), bad (1 chunk=None), good (1 chunk)
        mock_safe.return_value = [[1.0, 2.0], None, [3.0, 4.0]]
        handler_cls = self._configured_handler()

        status, body = self._post(
            handler_cls, {"model": "m", "input": ["good1", "bad", "good2"]}
        )
        assert status == 200
        embs = body["embeddings"]
        assert len(embs) == 3
        assert embs[0] == [1.0, 2.0]
        assert embs[1] == [0.0, 0.0]  # failed → zero vector (dim auto-detected as 2)
        assert embs[2] == [3.0, 4.0]
        assert handler_cls.stats["failed"] == 1

    @patch("erd_index.embed_proxy.load_tokenizer", return_value=None)
    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_partial_chunk_failure_gives_zero_vector(
        self, mock_safe: MagicMock, _mock_tok: MagicMock
    ) -> None:
        """If any chunk for a multi-chunk input fails, the entire input gets zero vector.

        No partial embeddings — averaging a subset of chunks would give a
        distorted embedding that misrepresents the document.
        """
        # Simulate a long input that splits into 2 chunks: first succeeds, second fails
        long_text = "a" * 3000 + "\n\n" + "b" * 3000  # Will split at paragraph boundary
        mock_safe.return_value = [[1.0, 2.0], None]  # chunk 0 ok, chunk 1 failed
        handler_cls = self._configured_handler()

        status, body = self._post(
            handler_cls, {"model": "m", "input": [long_text]}
        )
        assert status == 200
        embs = body["embeddings"]
        assert len(embs) == 1
        # All-or-nothing: one chunk failed → entire input gets zero vector
        assert embs[0] == [0.0, 0.0]
        assert handler_cls.stats["failed"] == 1

    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_stats_tracking(self, mock_safe: MagicMock) -> None:
        mock_safe.return_value = [[1.0]]
        handler_cls = self._configured_handler()

        self._post(handler_cls, {"model": "m", "input": ["text"]})
        assert handler_cls.stats["total"] == 1
        assert handler_cls.stats["split"] == 0
        assert handler_cls.stats["failed"] == 0

    @patch("erd_index.embed_proxy.load_tokenizer", return_value=None)
    @patch("erd_index.embed_proxy.embed_batch_concurrent_safe")
    def test_stats_count_split(
        self, mock_safe: MagicMock, _mock_tok: MagicMock
    ) -> None:
        mock_safe.return_value = [[1.0, 2.0], [3.0, 4.0]]
        handler_cls = self._configured_handler(max_chars=50)

        long_text = "A" * 40 + "\n\n" + "B" * 40
        self._post(handler_cls, {"model": "m", "input": [long_text]})
        assert handler_cls.stats["total"] == 1
        assert handler_cls.stats["split"] == 1
        assert handler_cls.stats["sub_chunks"] == 2

    def test_default_model(self) -> None:
        """When no model is specified, defaults to nomic-embed-text."""
        handler_cls = self._configured_handler()
        with patch(
            "erd_index.embed_proxy.embed_batch_concurrent_safe",
            return_value=[[1.0]],
        ) as mock_safe:
            self._post(handler_cls, {"input": ["text"]})
            args = mock_safe.call_args
            assert args[0][1] == "nomic-embed-text"


# ===================================================================
# configure_handler
# ===================================================================


class TestConfigureHandler:
    """configure_handler sets class-level attributes on _ProxyHandler."""

    def test_sets_attributes(self) -> None:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        handler_cls = configure_handler(
            max_chars=2000,
            max_tokens=1500,
            ollama_url="http://custom:1234/api/embed",
            batch_size=5,
            retry_count=5,
            executor=executor,
        )
        assert handler_cls.max_chars == 2000
        assert handler_cls.max_tokens == 1500
        assert handler_cls.ollama_url == "http://custom:1234/api/embed"
        assert handler_cls.batch_size == 5
        assert handler_cls.retry_count == 5
        assert handler_cls.executor is executor
        executor.shutdown(wait=False)

    def test_resets_stats(self) -> None:
        handler_cls = configure_handler()
        handler_cls.stats["total"] = 42
        handler_cls = configure_handler()
        assert handler_cls.stats["total"] == 0


# ===================================================================
# _embed_single_batch
# ===================================================================


class TestEmbedSingleBatch:
    """_embed_single_batch serializes and delegates to _request_with_retry."""

    @patch("erd_index.embed_proxy._request_with_retry")
    def test_passes_correct_payload(self, mock_retry: MagicMock) -> None:
        mock_retry.return_value = [[1.0]]
        _embed_single_batch(["hello"], "nomic", "http://x/api/embed", retry_count=2)

        call_args = mock_retry.call_args
        url = call_args[0][0]
        data = json.loads(call_args[0][1])
        assert url == "http://x/api/embed"
        assert data == {"model": "nomic", "input": ["hello"], "truncate": False}
        assert call_args[0][2] == 2  # retry_count


# ===================================================================
# _embed_adaptive
# ===================================================================


class TestEmbedAdaptive:
    """_embed_adaptive splits text on 400 errors and averages sub-embeddings."""

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_succeeds_first_try(self, mock_batch: MagicMock) -> None:
        mock_batch.return_value = [[1.0, 2.0]]
        result = _embed_adaptive("short text", "model", "http://x")
        assert result == [1.0, 2.0]
        assert mock_batch.call_count == 1

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_splits_on_400_and_averages(self, mock_batch: MagicMock) -> None:
        """400 on full text → split in half → embed each half → average."""
        mock_batch.side_effect = [
            _make_http_error(400),  # Full text fails
            [[1.0, 4.0]],          # Left half succeeds
            [[3.0, 6.0]],          # Right half succeeds
        ]
        # Need a text long enough to split (with a newline near middle)
        text = "a" * 50 + "\n" + "b" * 50
        result = _embed_adaptive(text, "model", "http://x")
        assert result == [2.0, 5.0]  # Average of [1,4] and [3,6]
        assert mock_batch.call_count == 3

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_recursive_split_depth_2(self, mock_batch: MagicMock) -> None:
        """400 on full text and left half → splits to depth 2."""
        mock_batch.side_effect = [
            _make_http_error(400),  # Full text fails
            _make_http_error(400),  # Left half also fails
            [[1.0]],               # Left-left quarter succeeds
            [[3.0]],               # Left-right quarter succeeds
            [[5.0]],               # Right half succeeds
        ]
        text = "a" * 40 + "\n" + "b" * 40 + "\n" + "c" * 40
        result = _embed_adaptive(text, "model", "http://x")
        # Left = avg([1.0], [3.0]) = [2.0], Right = [5.0], final = avg([2.0], [5.0]) = [3.5]
        assert result == [3.5]
        assert mock_batch.call_count == 5

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_gives_up_at_max_depth(self, mock_batch: MagicMock) -> None:
        """Raises after _MAX_ADAPTIVE_DEPTH splits."""
        mock_batch.side_effect = _make_http_error(400)
        text = "a" * 40 + "\n" + "b" * 40 + "\n" + "c" * 40 + "\n" + "d" * 40
        with pytest.raises(urllib.error.HTTPError):
            _embed_adaptive(text, "model", "http://x")

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_non_400_error_raises_immediately(self, mock_batch: MagicMock) -> None:
        mock_batch.side_effect = _make_http_error(500)
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _embed_adaptive("text", "model", "http://x")
        assert exc_info.value.code == 500
        assert mock_batch.call_count == 1

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_hex_heavy_go_test(self, mock_batch: MagicMock) -> None:
        """Realistic case: Go test with long hex string exceeds token limit."""
        hex_text = (
            'TestPush func TestPush(t *testing.T) {\n'
            '\tcode := common.FromHex("'
            + "0011223344556677889900aabbccddeeff" * 50
            + '")\n'
            '\tpush32 := makePush(32, 32)\n'
            '\tscope := &ScopeContext{Memory: nil, Stack: newstack()}\n'
        )
        mock_batch.side_effect = [
            _make_http_error(400),  # Full text too long for tokenizer
            [[1.0, 2.0]],          # First half ok
            [[3.0, 4.0]],          # Second half ok
        ]
        result = _embed_adaptive(hex_text, "model", "http://x")
        assert result == [2.0, 3.0]  # Average

    @patch("erd_index.embed_proxy._embed_single_batch")
    def test_concurrent_safe_uses_adaptive(self, mock_batch: MagicMock) -> None:
        """embed_batch_concurrent_safe uses adaptive splitting in retry phase."""
        mock_batch.side_effect = [
            RuntimeError("batch failed"),  # Batch of ["good", "long\nhex"] fails
            [[1.0]],                       # "good" individual retry succeeds first try
            _make_http_error(400),         # "long\nhex" too long
            [[2.0]],                       # left half of "long\nhex"
            [[4.0]],                       # right half of "long\nhex"
        ]
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            result = embed_batch_concurrent_safe(
                ["good", "long\nhex"], "model",
                ollama_url="http://x", batch_size=2, retry_count=1, executor=executor,
            )
        assert result[0] == [1.0]
        assert result[1] == [3.0]  # avg([2.0], [4.0])


# ===================================================================
# CLI / build_parser
# ===================================================================


class TestCLI:
    """CLI argument parsing and env var fallback."""

    def test_defaults(self) -> None:
        from erd_index.embed_proxy import build_parser

        parser = build_parser()
        args = parser.parse_args([])
        assert args.port == 11435
        assert args.max_chars == 4000
        assert args.max_tokens == DEFAULT_MAX_TOKENS
        assert args.ollama_batch_size == 10
        assert args.retry_count == 3

    def test_custom_flags(self) -> None:
        from erd_index.embed_proxy import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "--port", "9999",
            "--max-chars", "2000",
            "--max-tokens", "1500",
            "--ollama-batch-size", "5",
            "--retry-count", "5",
            "--workers", "8",
            "--ollama-url", "http://remote:1234/api/embed",
            "--verbose",
        ])
        assert args.port == 9999
        assert args.max_chars == 2000
        assert args.max_tokens == 1500
        assert args.ollama_batch_size == 5
        assert args.retry_count == 5
        assert args.workers == 8
        assert args.ollama_url == "http://remote:1234/api/embed"
        assert args.verbose is True
