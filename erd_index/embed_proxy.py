"""Splitting proxy for Ollama /api/embed endpoint.

Sits between Meilisearch and Ollama.  Long inputs are split into sub-chunks,
embedded independently via a thread pool, then averaged back into a single
vector.  This avoids hitting nomic-embed-text's 2048-token context limit while
preserving information from the full document.

Token-aware splitting: the proxy loads the ``bert-base-uncased`` tokenizer
(used by nomic-embed-text) via the ``tokenizers`` library to count tokens
before splitting.  This handles variable token density (hex strings, minified
code, binary escapes) correctly.  Character-based splitting is kept as a
fallback when the tokenizer is unavailable.

Resilience: if embedding fails for an individual input after retries, the proxy
logs the failure and returns a zero vector for that input.  This prevents a
single bad document from aborting Meilisearch's entire embedding run (which
would roll back the embedder settings and lose all progress).  Failed inputs
are tracked in stats and logged at WARNING level so they can be identified and
re-embedded later.

Configuration precedence: CLI flags > environment variables > built-in defaults.

Environment variables::

    ERD_PROXY_PORT                (default 11435)
    ERD_PROXY_MAX_CHARS           (default 4000)
    ERD_PROXY_MAX_TOKENS          (default 1800)
    ERD_PROXY_OLLAMA_URL          (default http://localhost:11434/api/embed)
    ERD_PROXY_OLLAMA_BATCH_SIZE   (default 10)
    ERD_PROXY_WORKERS             (default 4)
    ERD_PROXY_RETRY_COUNT         (default 3)
    ERD_PROXY_OLLAMA_CONCURRENCY  (default 1)
"""

from __future__ import annotations

import argparse
import concurrent.futures
import http.server
import json
import logging
import os
import signal
import socketserver
import sys
import threading
import time
import urllib.error
import urllib.request
from typing import ClassVar

log = logging.getLogger("erd.embed_proxy")

# ---------------------------------------------------------------------------
# Defaults (overridable via env vars and CLI flags)
# ---------------------------------------------------------------------------

DEFAULT_PORT = 11435
DEFAULT_MAX_CHARS = 4000
DEFAULT_MAX_TOKENS = 1800  # ~12% margin below nomic-embed-text's 2048-token limit
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/embed"
DEFAULT_BATCH_SIZE = 10
DEFAULT_WORKERS = 4
DEFAULT_RETRY_COUNT = 3
DEFAULT_DIMENSIONS = 768  # nomic-embed-text

# Retry back-off base (doubles each attempt: 0.5 s, 1 s, 2 s)
_RETRY_BACKOFF_BASE = 0.5

# HTTP status codes considered transient
_TRANSIENT_CODES = frozenset({502, 503, 504, 408})

# Timeout for individual Ollama requests (seconds)
_OLLAMA_TIMEOUT = 60


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def split_text(text: str, max_chars: int) -> list[str]:
    """Split *text* into chunks of at most *max_chars*, on paragraph boundaries.

    Returns the original text as a single-element list when it already fits.
    """
    if not text:
        return [text]
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    while text:
        if len(text) <= max_chars:
            chunks.append(text)
            break
        # Try to split at a paragraph boundary
        cut = text.rfind("\n\n", 0, max_chars)
        if cut < max_chars // 2:
            cut = text.rfind("\n", 0, max_chars)
        if cut < max_chars // 2:
            cut = max_chars
        chunks.append(text[:cut])
        text = text[cut:].lstrip()
    return chunks


# ---------------------------------------------------------------------------
# Tokenizer (lazy-loaded)
# ---------------------------------------------------------------------------

_tokenizer_cache: object | None = None  # tokenizers.Tokenizer once loaded


def load_tokenizer() -> object | None:
    """Load and cache the ``bert-base-uncased`` tokenizer.

    Returns ``None`` if the ``tokenizers`` library is not installed.
    The tokenizer is loaded once and reused for all subsequent calls.
    """
    global _tokenizer_cache
    if _tokenizer_cache is not None:
        return _tokenizer_cache
    try:
        from tokenizers import Tokenizer

        tok = Tokenizer.from_pretrained("bert-base-uncased")
        tok.no_truncation()
        _tokenizer_cache = tok
        log.info("Loaded bert-base-uncased tokenizer for token-aware splitting")
        return tok
    except Exception as exc:
        log.warning("Could not load tokenizer (%s); using character-based splitting", exc)
        return None


def count_tokens(text: str) -> int | None:
    """Return the token count for *text*, or ``None`` if no tokenizer is loaded."""
    tok = load_tokenizer()
    if tok is None:
        return None
    return len(tok.encode(text).ids)  # type: ignore[union-attr]


def split_text_by_tokens(text: str, max_tokens: int) -> list[str]:
    """Split *text* into chunks that each fit within *max_tokens*.

    Uses the ``bert-base-uncased`` tokenizer's offset mapping to find the
    exact character position where the token budget is exhausted, then searches
    backward for a paragraph or newline boundary.

    *max_tokens* includes the [CLS] and [SEP] special tokens that BERT adds,
    so the usable budget for text tokens is ``max_tokens - 2``.
    """
    if not text:
        return [text]

    tok = load_tokenizer()
    if tok is None:
        # Fallback: use character-based splitting with a conservative limit
        return split_text(text, DEFAULT_MAX_CHARS)

    enc = tok.encode(text)  # type: ignore[union-attr]
    if len(enc.ids) <= max_tokens:
        return [text]

    text_budget = max_tokens - 2  # exclude [CLS] and [SEP]
    chunks: list[str] = []
    remaining = text

    while remaining:
        enc = tok.encode(remaining)  # type: ignore[union-attr]
        if len(enc.ids) <= max_tokens:
            chunks.append(remaining)
            break

        # Find the character position at the text_budget-th text token.
        # Offsets: [0]=CLS(0,0), [1..N-1]=text tokens, [N]=SEP(0,0)
        if text_budget >= len(enc.offsets) - 1:
            chunks.append(remaining)
            break

        char_pos = enc.offsets[text_budget][1]

        # Search backward for a paragraph or newline boundary
        search_start = max(char_pos * 2 // 3, 0)
        cut = remaining.rfind("\n\n", search_start, char_pos)
        if cut < search_start:
            cut = remaining.rfind("\n", search_start, char_pos)
        if cut < search_start:
            cut = char_pos

        chunk = remaining[:cut]
        if not chunk:
            chunk = remaining[:char_pos]
        chunks.append(chunk)
        remaining = remaining[cut:].lstrip()
        if not remaining:
            break

    return chunks if chunks else [text]


def avg_embeddings(embeddings: list[list[float]]) -> list[float]:
    """Element-wise average of a list of embedding vectors."""
    n = len(embeddings)
    dim = len(embeddings[0])
    result = [0.0] * dim
    for emb in embeddings:
        for i in range(dim):
            result[i] += emb[i]
    return [v / n for v in result]


def _embed_single_batch(
    texts: list[str],
    model: str,
    ollama_url: str,
    retry_count: int = DEFAULT_RETRY_COUNT,
) -> list[list[float]]:
    """Embed a single batch of texts via Ollama with retries."""
    data = json.dumps({"model": model, "input": texts, "truncate": False}).encode()
    return _request_with_retry(ollama_url, data, retry_count)


# Maximum number of adaptive split levels (text → halves → quarters → eighths)
_MAX_ADAPTIVE_DEPTH = 3


def _embed_adaptive(
    text: str,
    model: str,
    ollama_url: str,
    retry_count: int = DEFAULT_RETRY_COUNT,
    _depth: int = 0,
) -> list[float]:
    """Embed a single text, adaptively splitting on context-length errors.

    If Ollama returns 400 (input too long for the model's context window),
    the text is split in half and each half is embedded separately.  The
    results are averaged.  This recurses up to ``_MAX_ADAPTIVE_DEPTH`` levels
    (i.e. up to 2^3 = 8 sub-chunks), which handles even pathological inputs
    like hex strings or minified code.

    Raises on non-recoverable errors (e.g. Ollama down, or text still too
    long after maximum splits).
    """
    try:
        embs = _embed_single_batch([text], model, ollama_url, retry_count)
        return embs[0]
    except urllib.error.HTTPError as exc:
        if exc.code != 400 or _depth >= _MAX_ADAPTIVE_DEPTH:
            raise
        # Split in half and recurse
        mid = len(text) // 2
        # Try to split at a newline near the midpoint for cleaner chunks
        cut = text.rfind("\n", mid - mid // 2, mid + mid // 2)
        if cut < 0:
            cut = mid
        left = text[:cut].rstrip()
        right = text[cut:].lstrip()
        if not left or not right:
            raise  # Degenerate split, give up
        log.debug(
            "Adaptive split at depth %d: %d chars → %d + %d",
            _depth + 1, len(text), len(left), len(right),
        )
        emb_left = _embed_adaptive(left, model, ollama_url, retry_count, _depth + 1)
        emb_right = _embed_adaptive(right, model, ollama_url, retry_count, _depth + 1)
        return avg_embeddings([emb_left, emb_right])


def embed_batch(
    texts: list[str],
    model: str,
    *,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    retry_count: int = DEFAULT_RETRY_COUNT,
) -> list[list[float]]:
    """Embed *texts* sequentially in sub-batches.  Raises on any failure.

    This is the simple sequential path; the handler uses the concurrent path.
    """
    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        embs = _embed_single_batch(batch, model, ollama_url, retry_count)
        all_embeddings.extend(embs)
    return all_embeddings


def _request_with_retry(
    url: str, data: bytes, retry_count: int = DEFAULT_RETRY_COUNT
) -> list[list[float]]:
    """POST *data* to *url* and return the ``embeddings`` list.

    Retries up to *retry_count* times on transient HTTP errors (502/503/504/408)
    and connection failures, with exponential back-off (0.5 s, 1 s, 2 s, ...).
    Non-transient errors are raised immediately.
    """
    last_exc: Exception | None = None
    for attempt in range(retry_count):
        try:
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=_OLLAMA_TIMEOUT)
            return json.loads(resp.read())["embeddings"]
        except urllib.error.HTTPError as exc:
            if exc.code not in _TRANSIENT_CODES:
                raise
            last_exc = exc
            wait = _RETRY_BACKOFF_BASE * (2**attempt)
            log.warning(
                "Ollama returned %d; retrying in %.1fs (attempt %d/%d)",
                exc.code,
                wait,
                attempt + 1,
                retry_count,
            )
            time.sleep(wait)
        except urllib.error.URLError as exc:
            last_exc = exc
            wait = _RETRY_BACKOFF_BASE * (2**attempt)
            log.warning(
                "Ollama unreachable (%s); retrying in %.1fs (attempt %d/%d)",
                exc.reason,
                wait,
                attempt + 1,
                retry_count,
            )
            time.sleep(wait)

    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Concurrent embedding
# ---------------------------------------------------------------------------


def embed_batch_concurrent(
    texts: list[str],
    model: str,
    *,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    retry_count: int = DEFAULT_RETRY_COUNT,
    executor: concurrent.futures.ThreadPoolExecutor,
) -> list[list[float]]:
    """Embed *texts* concurrently in sub-batches.  Raises on any failure.

    Sub-batches of up to *batch_size* texts are submitted to *executor* in
    parallel, reducing wall-clock time from O(N) to roughly O(N/workers).
    If any sub-batch fails after retries, the first error is re-raised so
    the caller can return an error to Meilisearch.
    """
    n = len(texts)
    if n == 0:
        return []

    # Submit all sub-batches to the thread pool
    futures: list[tuple[int, concurrent.futures.Future[list[list[float]]]]] = []
    for i in range(0, n, batch_size):
        batch = texts[i : i + batch_size]
        fut = executor.submit(_embed_single_batch, batch, model, ollama_url, retry_count)
        futures.append((i, fut))

    # Collect results in submission order; raises on first failure
    all_embeddings: list[list[float]] = [[] for _ in range(n)]
    for start, fut in futures:
        embs = fut.result()
        for j, emb in enumerate(embs):
            all_embeddings[start + j] = emb

    return all_embeddings


def embed_batch_concurrent_safe(
    texts: list[str],
    model: str,
    *,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    retry_count: int = DEFAULT_RETRY_COUNT,
    executor: concurrent.futures.ThreadPoolExecutor,
) -> list[list[float] | None]:
    """Like :func:`embed_batch_concurrent` but returns ``None`` for failed chunks.

    Fast path: texts are sent in sub-batches of *batch_size*.  If a sub-batch
    fails (e.g. one bad input causes Ollama to return 400), each text in that
    batch is retried individually so only the truly problematic text(s) get
    ``None``.  This avoids one bad document poisoning an entire sub-batch.
    """
    n = len(texts)
    if n == 0:
        return []

    # Phase 1: submit batched requests (fast path)
    futures: list[tuple[int, int, concurrent.futures.Future[list[list[float]]]]] = []
    for i in range(0, n, batch_size):
        batch = texts[i : i + batch_size]
        fut = executor.submit(_embed_single_batch, batch, model, ollama_url, retry_count)
        futures.append((i, len(batch), fut))

    all_embeddings: list[list[float] | None] = [None] * n
    failed_ranges: list[tuple[int, int]] = []  # (start, count) of failed sub-batches

    for start, count, fut in futures:
        try:
            embs = fut.result()
            for j, emb in enumerate(embs):
                all_embeddings[start + j] = emb
        except Exception as exc:
            log.warning(
                "Sub-batch at offset %d (%d texts) failed: %s — retrying individually",
                start, count, exc,
            )
            failed_ranges.append((start, count))

    # Phase 2: retry failed sub-batches individually with adaptive splitting
    if failed_ranges:
        individual_futures: list[tuple[int, concurrent.futures.Future[list[float]]]] = []
        for start, count in failed_ranges:
            for j in range(count):
                idx = start + j
                fut = executor.submit(
                    _embed_adaptive, texts[idx], model, ollama_url, retry_count,
                )
                individual_futures.append((idx, fut))

        for idx, fut in individual_futures:
            try:
                all_embeddings[idx] = fut.result()
            except Exception as exc:
                log.warning(
                    "Individual text at offset %d failed: %s", idx, exc,
                )
                # Leave as None

    return all_embeddings


# ---------------------------------------------------------------------------
# Threading HTTP server — accepts concurrent connections from Meilisearch
# while the semaphore in the handler serializes actual Ollama calls.
# ---------------------------------------------------------------------------


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """HTTP server that handles each request in a separate thread.

    This prevents Meilisearch's many parallel embedding requests from
    timing out while waiting in the TCP accept queue.  Actual Ollama
    concurrency is controlled by ``_ProxyHandler.ollama_semaphore``.
    """

    daemon_threads = True


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------


class _ProxyHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler that splits long texts, embeds sub-chunks, and averages."""

    # Set by configure_handler() before the server starts
    max_chars: int = DEFAULT_MAX_CHARS
    max_tokens: int = DEFAULT_MAX_TOKENS
    ollama_url: str = DEFAULT_OLLAMA_URL
    batch_size: int = DEFAULT_BATCH_SIZE
    retry_count: int = DEFAULT_RETRY_COUNT
    dimensions: int = DEFAULT_DIMENSIONS
    executor: concurrent.futures.ThreadPoolExecutor | None = None

    # Semaphore controlling how many concurrent Ollama requests are in-flight.
    # With ThreadingHTTPServer, many Meilisearch connections are accepted
    # concurrently, but this semaphore prevents overwhelming Ollama.
    ollama_semaphore: threading.Semaphore = threading.Semaphore(1)

    # Shared mutable stats — guarded by _stats_lock for thread safety
    stats: ClassVar[dict[str, int]] = {
        "total": 0, "split": 0, "sub_chunks": 0, "failed": 0,
    }
    _stats_lock: ClassVar[threading.Lock] = threading.Lock()

    def do_POST(self) -> None:
        request_start = time.monotonic()

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_error(400, "Invalid JSON body")
            return

        model: str = data.get("model", "nomic-embed-text")
        inputs = data.get("input", [])
        if isinstance(inputs, str):
            inputs = [inputs]
        if not inputs:
            self._send_json(200, {"embeddings": []})
            return

        # Split all inputs, tracking which chunks belong to which input
        all_chunks: list[str] = []
        chunk_map: list[tuple[int, int]] = []  # (start_idx, count)
        n_split = 0
        n_sub_chunks = 0

        for text in inputs:
            tok = load_tokenizer()
            if tok is not None:
                chunks = split_text_by_tokens(text, self.max_tokens)
            else:
                chunks = split_text(text, self.max_chars)
            if len(chunks) > 1:
                n_split += 1
                n_sub_chunks += len(chunks)
            chunk_map.append((len(all_chunks), len(chunks)))
            all_chunks.extend(chunks)

        # Acquire semaphore to limit concurrent Ollama requests.
        # With ThreadingHTTPServer, many Meilisearch connections are accepted
        # in parallel, but this prevents overwhelming Ollama.
        with self.ollama_semaphore:
            all_embeddings = embed_batch_concurrent_safe(
                all_chunks,
                model,
                ollama_url=self.ollama_url,
                batch_size=self.batch_size,
                retry_count=self.retry_count,
                executor=self.executor,
            )

        # Auto-detect dimensions from first successful embedding
        for emb in all_embeddings:
            if emb is not None:
                if len(emb) != self.dimensions:
                    self.dimensions = len(emb)
                break

        # Assemble per-input embeddings: all chunks must succeed or input gets zero vector.
        # No partial results — if any chunk for an input failed, the whole input is
        # treated as failed so it can be identified and re-embedded later.
        result_embeddings: list[list[float]] = []
        failed_in_batch = 0
        zero = [0.0] * self.dimensions

        for idx, (start, count) in enumerate(chunk_map):
            sub = all_embeddings[start : start + count]
            if any(e is None for e in sub):
                failed_in_batch += 1
                n_good = sum(1 for e in sub if e is not None)
                preview = inputs[idx][:120].replace("\n", " ")
                log.warning(
                    "FAILED input (%d chars, %d chunks, %d/%d succeeded): %r",
                    len(inputs[idx]),
                    count,
                    n_good,
                    count,
                    preview,
                )
                result_embeddings.append(zero)
            elif count == 1:
                result_embeddings.append(sub[0])
            else:
                result_embeddings.append(avg_embeddings(sub))

        elapsed = time.monotonic() - request_start

        # Update shared stats under lock (thread-safe)
        with self._stats_lock:
            self.stats["total"] += len(inputs)
            self.stats["split"] += n_split
            self.stats["sub_chunks"] += n_sub_chunks
            self.stats["failed"] += failed_in_batch

        if failed_in_batch:
            log.warning(
                "Batch: %d/%d inputs failed (%.1fs). Total failures: %d",
                failed_in_batch,
                len(inputs),
                elapsed,
                self.stats["failed"],
            )
        else:
            log.debug(
                "Embedded %d inputs (%d chunks) in %.1fs",
                len(inputs),
                len(all_chunks),
                elapsed,
            )

        self._send_json(200, {"embeddings": result_embeddings})

    # -- response helpers ---------------------------------------------------

    def _send_json(self, code: int, obj: object) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, code: int, message: str) -> None:
        self._send_json(code, {"error": message})

    # -- logging override ---------------------------------------------------

    def log_message(self, format: str, *args: object) -> None:
        """Route request logging through the module logger."""
        log.debug(format, *args)

    # Track last progress milestone for periodic INFO logging
    _last_progress: ClassVar[int] = 0

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        with self._stats_lock:
            total = self.stats["total"]
            milestone = total // 500
            if milestone > self._last_progress:
                _ProxyHandler._last_progress = milestone
                log.info(
                    "Progress: %d inputs, %d split (%d sub-chunks), %d failed",
                    total,
                    self.stats["split"],
                    self.stats["sub_chunks"],
                    self.stats["failed"],
                )


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------


def configure_handler(
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    retry_count: int = DEFAULT_RETRY_COUNT,
    dimensions: int = DEFAULT_DIMENSIONS,
    executor: concurrent.futures.ThreadPoolExecutor | None = None,
    ollama_concurrency: int = 1,
) -> type[_ProxyHandler]:
    """Return a handler class configured with the given parameters."""
    _ProxyHandler.max_chars = max_chars
    _ProxyHandler.max_tokens = max_tokens
    _ProxyHandler.ollama_url = ollama_url
    _ProxyHandler.batch_size = batch_size
    _ProxyHandler.retry_count = retry_count
    _ProxyHandler.dimensions = dimensions
    _ProxyHandler.executor = executor
    _ProxyHandler.ollama_semaphore = threading.Semaphore(ollama_concurrency)
    _ProxyHandler.stats = {"total": 0, "split": 0, "sub_chunks": 0, "failed": 0}
    _ProxyHandler._stats_lock = threading.Lock()
    _ProxyHandler._last_progress = 0
    return _ProxyHandler


def run_server(
    *,
    port: int = DEFAULT_PORT,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    retry_count: int = DEFAULT_RETRY_COUNT,
    workers: int = DEFAULT_WORKERS,
    ollama_concurrency: int = 1,
) -> None:
    """Start the proxy server (blocking).  Handles SIGTERM for graceful shutdown."""
    # Pre-load tokenizer at startup so the first request isn't slow
    load_tokenizer()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
    handler = configure_handler(
        max_chars=max_chars,
        max_tokens=max_tokens,
        ollama_url=ollama_url,
        batch_size=batch_size,
        retry_count=retry_count,
        executor=executor,
        ollama_concurrency=ollama_concurrency,
    )
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)

    def _shutdown(signum: int, frame: object) -> None:
        log.info("Received signal %d, shutting down", signum)
        server.shutdown()

    signal.signal(signal.SIGTERM, _shutdown)

    tok_status = "token-aware" if load_tokenizer() is not None else "char-based"
    log.info(
        "Embed proxy on :%d -> %s (%s, max %d tokens / %d chars, "
        "batch %d, workers %d, ollama-concurrency %d)",
        port,
        ollama_url,
        tok_status,
        max_tokens,
        max_chars,
        batch_size,
        workers,
        ollama_concurrency,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stats = handler.stats
        log.info(
            "Final stats: %d inputs, %d split (%d sub-chunks), %d failed",
            stats["total"],
            stats["split"],
            stats["sub_chunks"],
            stats["failed"],
        )
        executor.shutdown(wait=False)
        server.server_close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _env_int(name: str, default: int) -> int:
    """Read an integer from the environment, falling back to *default*."""
    val = os.environ.get(name)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        log.warning("Invalid integer for %s=%r; using default %d", name, val, default)
        return default


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for ``erd-embed-proxy``."""
    parser = argparse.ArgumentParser(
        prog="erd-embed-proxy",
        description=(
            "Splitting Ollama embed proxy.  Splits long texts into sub-chunks, "
            "embeds each independently via a thread pool, then averages the "
            "vectors back into one embedding per input."
        ),
    )
    parser.add_argument(
        "--port",
        type=int,
        default=_env_int("ERD_PROXY_PORT", DEFAULT_PORT),
        help=f"Listen port (env: ERD_PROXY_PORT, default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=_env_int("ERD_PROXY_MAX_CHARS", DEFAULT_MAX_CHARS),
        help=(
            f"Max characters per sub-chunk when tokenizer unavailable "
            f"(env: ERD_PROXY_MAX_CHARS, default: {DEFAULT_MAX_CHARS})"
        ),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=_env_int("ERD_PROXY_MAX_TOKENS", DEFAULT_MAX_TOKENS),
        help=(
            f"Max tokens per sub-chunk including [CLS]/[SEP] "
            f"(env: ERD_PROXY_MAX_TOKENS, default: {DEFAULT_MAX_TOKENS})"
        ),
    )
    parser.add_argument(
        "--ollama-url",
        default=os.environ.get("ERD_PROXY_OLLAMA_URL", DEFAULT_OLLAMA_URL),
        help=(f"Ollama embed endpoint (env: ERD_PROXY_OLLAMA_URL, default: {DEFAULT_OLLAMA_URL})"),
    )
    parser.add_argument(
        "--ollama-batch-size",
        type=int,
        default=_env_int("ERD_PROXY_OLLAMA_BATCH_SIZE", DEFAULT_BATCH_SIZE),
        help=(
            f"Max texts per Ollama request "
            f"(env: ERD_PROXY_OLLAMA_BATCH_SIZE, default: {DEFAULT_BATCH_SIZE})"
        ),
    )
    parser.add_argument(
        "--retry-count",
        type=int,
        default=_env_int("ERD_PROXY_RETRY_COUNT", DEFAULT_RETRY_COUNT),
        help=(
            f"Retries per Ollama request on transient errors "
            f"(env: ERD_PROXY_RETRY_COUNT, default: {DEFAULT_RETRY_COUNT})"
        ),
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=_env_int("ERD_PROXY_WORKERS", DEFAULT_WORKERS),
        help=(
            f"Thread pool size for concurrent Ollama requests "
            f"(env: ERD_PROXY_WORKERS, default: {DEFAULT_WORKERS})"
        ),
    )
    parser.add_argument(
        "--ollama-concurrency",
        type=int,
        default=_env_int("ERD_PROXY_OLLAMA_CONCURRENCY", 1),
        help=(
            "Max concurrent embedding requests forwarded to Ollama.  "
            "Meilisearch sends many parallel requests; this semaphore "
            "prevents Ollama queue buildup and timeouts "
            "(env: ERD_PROXY_OLLAMA_CONCURRENCY, default: 1)"
        ),
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for ``erd-embed-proxy``."""
    parser = build_parser()
    args = parser.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )

    run_server(
        port=args.port,
        max_chars=args.max_chars,
        max_tokens=args.max_tokens,
        ollama_url=args.ollama_url,
        batch_size=args.ollama_batch_size,
        retry_count=args.retry_count,
        workers=args.workers,
        ollama_concurrency=args.ollama_concurrency,
    )


if __name__ == "__main__":
    main()
