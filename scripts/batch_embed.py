#!/usr/bin/env python3
"""Batch-embed documents in Meilisearch using Ollama.

Fetches documents from Meilisearch in pages, embeds the text via Ollama's
``/api/embed`` endpoint, and writes the vectors back via the ``_vectors``
field.  Progress is checkpointed to disk so the script can resume after
failures without re-embedding already-processed documents.

This bypasses Meilisearch's built-in embedding pipeline to avoid:

- **Ollama request queuing**: Meilisearch sends concurrent embedding requests;
  Ollama processes them sequentially.  Queue wait + processing time exceeds
  the per-request timeout, causing "timeout: global" errors.
- **All-or-nothing failures**: Meilisearch's auto-embedding task aborts on
  timeout, losing all progress.
- **No per-batch visibility**: no way to track which documents succeeded.

Prerequisites:

- The embedder must be set to ``source: "userProvided"`` with the correct
  dimensions.  Use ``--setup`` to configure this automatically.
- The embedding model must be loaded in Ollama (``ollama pull <model>``).
- Meilisearch payload limit must accommodate the batch size (~8 KB per
  document with 768-dim vectors; 1000 docs ≈ 8 MB).

Usage::

    uv run python scripts/batch_embed.py --setup       # configure + embed
    uv run python scripts/batch_embed.py --resume       # continue from checkpoint
    uv run python scripts/batch_embed.py --dry-run      # preview without changes
    uv run python scripts/batch_embed.py --setup-only   # configure, don't embed

Configuration precedence: CLI flags > environment variables > built-in defaults.

Environment variables::

    ERD_BATCH_MEILI_URL       (default http://localhost:7700)
    ERD_BATCH_OLLAMA_URL      (default http://localhost:11434/api/embed)
    ERD_BATCH_INDEX           (default eth_chunks_v1)
    ERD_BATCH_MODEL           (default embeddinggemma:300m)
    ERD_BATCH_SIZE            (default 1000)
    ERD_BATCH_OLLAMA_SIZE     (default 10)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

log = logging.getLogger("batch_embed")

# ---------------------------------------------------------------------------
# Defaults (overridable via env vars and CLI flags)
# ---------------------------------------------------------------------------

DEFAULT_MEILI_URL = "http://localhost:7700"
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/embed"
DEFAULT_INDEX = "eth_chunks_v1"
DEFAULT_EMBEDDER_NAME = "default"
DEFAULT_MODEL = "embeddinggemma:300m"

DEFAULT_BATCH_SIZE = 1000  # documents per Meilisearch page
DEFAULT_OLLAMA_BATCH_SIZE = 10  # texts per Ollama API call
DEFAULT_OLLAMA_TIMEOUT = 60  # seconds per Ollama request

DEFAULT_CHECKPOINT_DIR = Path("/tmp/batch-embed")

# Retry config
DEFAULT_RETRY_COUNT = 3
_RETRY_BACKOFF_BASE = 0.5
_TRANSIENT_CODES = frozenset({408, 502, 503, 504})


# ---------------------------------------------------------------------------
# Graceful shutdown
# ---------------------------------------------------------------------------

_shutdown_requested = False


def _request_shutdown(signum: int, frame: object) -> None:
    """Signal handler: request graceful shutdown after current batch."""
    global _shutdown_requested
    if _shutdown_requested:
        log.warning("Second signal received — forcing exit")
        sys.exit(1)
    _shutdown_requested = True
    log.info("Shutdown requested (signal %d) — finishing current batch", signum)


# ---------------------------------------------------------------------------
# Meilisearch HTTP helpers
# ---------------------------------------------------------------------------


def _read_key_file(path: str) -> str | None:
    """Read a single-line key from *path*, or return ``None`` if missing."""
    p = Path(path).expanduser()
    if p.exists():
        return p.read_text().strip()
    return None


def _meili_key() -> str:
    """Resolve the Meilisearch admin API key."""
    return _read_key_file("~/.config/erd/admin-key") or "erd-dev-key"


def _meili_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_meili_key()}", "Content-Type": "application/json"}


def _meili_request(method: str, url: str, body: bytes | None, timeout: float) -> dict:
    """Send an HTTP request to Meilisearch and return the parsed JSON response."""
    req = urllib.request.Request(url, data=body, headers=_meili_headers(), method=method)
    resp = urllib.request.urlopen(req, timeout=timeout)
    return json.loads(resp.read())


def meili_get(base_url: str, path: str, params: dict[str, str] | None = None) -> dict:
    """GET request to Meilisearch."""
    url = f"{base_url}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    return _meili_request("GET", url, None, 30)


def meili_put(base_url: str, path: str, body: list | dict) -> dict:
    """PUT request to Meilisearch (used for document updates)."""
    url = f"{base_url}{path}"
    return _meili_request("PUT", url, json.dumps(body).encode(), 120)


def meili_patch(base_url: str, path: str, body: dict) -> dict:
    """PATCH request to Meilisearch (used for settings updates)."""
    url = f"{base_url}{path}"
    return _meili_request("PATCH", url, json.dumps(body).encode(), 60)


def wait_for_task(
    base_url: str, task_uid: int, *, poll_interval: float = 1.0, timeout: float = 120
) -> dict:
    """Poll a Meilisearch task until it reaches a terminal status.

    Returns the task dict.  If *timeout* elapses, returns the last polled
    state (which may still be ``processing``).
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        task = meili_get(base_url, f"/tasks/{task_uid}")
        if task["status"] in ("succeeded", "failed", "canceled"):
            return task
        time.sleep(poll_interval)
    return meili_get(base_url, f"/tasks/{task_uid}")


# ---------------------------------------------------------------------------
# Ollama embedding
# ---------------------------------------------------------------------------


def embed_texts(
    texts: list[str],
    model: str,
    *,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    timeout: int = DEFAULT_OLLAMA_TIMEOUT,
    retry_count: int = DEFAULT_RETRY_COUNT,
) -> list[list[float]]:
    """Embed a batch of texts via Ollama with retries.

    Returns the list of embedding vectors (one per input text).
    Raises on non-recoverable errors after exhausting retries.
    """
    data = json.dumps({"model": model, "input": texts}).encode()
    last_exc: Exception | None = None

    for attempt in range(retry_count):
        try:
            req = urllib.request.Request(
                ollama_url, data=data, headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=timeout)
            result = json.loads(resp.read())
            embeddings = result.get("embeddings")
            if not embeddings or len(embeddings) != len(texts):
                raise ValueError(
                    f"Expected {len(texts)} embeddings, got "
                    f"{len(embeddings) if embeddings else 0}"
                )
            return embeddings
        except urllib.error.HTTPError as exc:
            if exc.code not in _TRANSIENT_CODES:
                raise
            last_exc = exc
        except urllib.error.URLError as exc:
            last_exc = exc
        except (TimeoutError, OSError) as exc:
            last_exc = exc

        wait = _RETRY_BACKOFF_BASE * (2**attempt)
        log.warning(
            "Ollama request failed (%s); retry %d/%d in %.1fs",
            last_exc, attempt + 1, retry_count, wait,
        )
        time.sleep(wait)

    raise last_exc  # type: ignore[misc]


def build_text(doc: dict, *, asymmetric: bool = False) -> str:
    """Build embedding text from a document.

    When *asymmetric* is ``False`` (default), mirrors the Meilisearch
    ``documentTemplate``:
    ``{% if doc.title %}{{doc.title}} {% endif %}{{doc.text}}``

    When *asymmetric* is ``True``, uses the embeddinggemma document prefix
    format: ``title: {title} | text: {content}``.  If no title is present,
    uses ``title: none``.
    """
    title = doc.get("title") or ""
    text = doc.get("text") or ""
    if asymmetric:
        return f"title: {title or 'none'} | text: {text}"
    parts = []
    if title:
        parts.append(title)
    if text:
        parts.append(text)
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Checkpoint management
# ---------------------------------------------------------------------------


def checkpoint_path(checkpoint_dir: Path, index: str) -> Path:
    """Return the checkpoint file path for *index*."""
    return checkpoint_dir / f"{index}.json"


def load_checkpoint(checkpoint_dir: Path, index: str) -> dict:
    """Load checkpoint from disk, or return a fresh initial state."""
    path = checkpoint_path(checkpoint_dir, index)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Corrupt checkpoint %s: %s — starting fresh", path, exc)
    return {"offset": 0, "embedded": 0, "failed_batches": [], "failed_docs": 0}


def save_checkpoint(checkpoint_dir: Path, index: str, data: dict) -> None:
    """Atomically save checkpoint to disk.

    Writes to a temporary file in the same directory, then renames.  This
    prevents partial writes from corrupting the checkpoint if the process
    is killed mid-write.
    """
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    target = checkpoint_path(checkpoint_dir, index)
    content = json.dumps(data, indent=2).encode()
    fd, tmp_path = tempfile.mkstemp(dir=checkpoint_dir, suffix=".tmp")
    closed = False
    try:
        os.write(fd, content)
        os.fsync(fd)
        os.close(fd)
        closed = True
        os.replace(tmp_path, target)
    except BaseException:
        if not closed:
            os.close(fd)
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Main batch embedding loop
# ---------------------------------------------------------------------------


def run_batch_embed(
    *,
    model: str = DEFAULT_MODEL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    ollama_batch_size: int = DEFAULT_OLLAMA_BATCH_SIZE,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    meili_url: str = DEFAULT_MEILI_URL,
    index: str = DEFAULT_INDEX,
    embedder_name: str = DEFAULT_EMBEDDER_NAME,
    checkpoint_dir: Path = DEFAULT_CHECKPOINT_DIR,
    resume: bool = False,
    dry_run: bool = False,
    asymmetric: bool = False,
) -> dict:
    """Embed all documents in batches.

    Returns a summary dict with ``embedded``, ``failed_docs``, and
    ``failed_batches`` counts.
    """
    # -- Pre-flight checks --------------------------------------------------

    embedders = meili_get(meili_url, f"/indexes/{index}/settings/embedders")
    embedder = embedders.get(embedder_name)
    if not embedder:
        log.error("No embedder '%s' configured on index '%s'", embedder_name, index)
        sys.exit(1)
    if embedder.get("source") != "userProvided":
        log.error(
            "Embedder source is '%s', expected 'userProvided'. "
            "Set it first with: --setup",
            embedder.get("source"),
        )
        sys.exit(1)

    try:
        test_emb = embed_texts(["test"], model, ollama_url=ollama_url, timeout=30)
        dims = len(test_emb[0])
        log.info("Ollama OK: model=%s, dimensions=%d", model, dims)
    except Exception as exc:
        log.error("Cannot reach Ollama at %s: %s", ollama_url, exc)
        sys.exit(1)

    stats = meili_get(meili_url, f"/indexes/{index}/stats")
    total = stats["numberOfDocuments"]
    log.info("Index has %d documents", total)

    # -- Checkpoint ---------------------------------------------------------

    if resume:
        ckpt = load_checkpoint(checkpoint_dir, index)
        log.info(
            "Resuming from checkpoint: offset=%d, embedded=%d",
            ckpt["offset"], ckpt["embedded"],
        )
    else:
        ckpt = {"offset": 0, "embedded": 0, "failed_batches": [], "failed_docs": 0}

    offset = ckpt["offset"]
    embedded = ckpt["embedded"]
    failed_batches: list[dict] = ckpt["failed_batches"]
    failed_docs = ckpt["failed_docs"]
    start_time = time.monotonic()

    # -- Main loop ----------------------------------------------------------

    while offset < total and not _shutdown_requested:
        batch_start = time.monotonic()

        # Fetch a page of documents
        result = meili_get(
            meili_url,
            f"/indexes/{index}/documents",
            {"offset": str(offset), "limit": str(batch_size), "fields": "id,title,text"},
        )
        docs = result["results"]
        if not docs:
            break

        texts = [build_text(doc, asymmetric=asymmetric) for doc in docs]
        doc_ids = [doc["id"] for doc in docs]

        if dry_run:
            avg_len = sum(len(t) for t in texts) / len(texts) if texts else 0
            log.info(
                "[DRY RUN] Batch %d-%d: %d docs, avg text len %.0f chars",
                offset, offset + len(docs), len(docs), avg_len,
            )
            offset += len(docs)
            embedded += len(docs)
            save_checkpoint(checkpoint_dir, index, {
                "offset": offset, "embedded": embedded,
                "failed_batches": failed_batches, "failed_docs": failed_docs,
            })
            continue

        # Embed in sub-batches via Ollama
        all_embeddings: list[list[float] | None] = [None] * len(texts)
        batch_failures = 0

        for i in range(0, len(texts), ollama_batch_size):
            if _shutdown_requested:
                break
            sub_texts = texts[i : i + ollama_batch_size]
            sub_ids = doc_ids[i : i + ollama_batch_size]
            try:
                embs = embed_texts(sub_texts, model, ollama_url=ollama_url)
                for j, emb in enumerate(embs):
                    all_embeddings[i + j] = emb
            except Exception as exc:
                log.warning(
                    "Sub-batch %d-%d failed: %s — retrying individually",
                    offset + i, offset + i + len(sub_texts), exc,
                )
                for j, (text, doc_id) in enumerate(zip(sub_texts, sub_ids, strict=True)):
                    try:
                        embs = embed_texts([text], model, ollama_url=ollama_url)
                        all_embeddings[i + j] = embs[0]
                    except Exception as exc2:
                        log.error("Doc %s failed: %s", doc_id, exc2)
                        batch_failures += 1

        # Push vectors to Meilisearch
        updates = [
            {"id": doc["id"], "_vectors": {embedder_name: emb}}
            for doc, emb in zip(docs, all_embeddings, strict=True)
            if emb is not None
        ]

        if updates:
            try:
                task_resp = meili_put(meili_url, f"/indexes/{index}/documents", updates)
                task = wait_for_task(meili_url, task_resp["taskUid"], timeout=120)
                if task["status"] != "succeeded":
                    log.error(
                        "Document update task %d: %s",
                        task_resp["taskUid"], task.get("error"),
                    )
                    failed_batches.append({"offset": offset, "error": str(task.get("error"))})
            except Exception as exc:
                log.error("PUT batch at offset %d failed: %s", offset, exc)
                failed_batches.append({"offset": offset, "error": str(exc)})

        batch_elapsed = time.monotonic() - batch_start
        embedded += len(updates)
        failed_docs += batch_failures
        offset += len(docs)

        # Atomic checkpoint
        save_checkpoint(checkpoint_dir, index, {
            "offset": offset, "embedded": embedded,
            "failed_batches": failed_batches, "failed_docs": failed_docs,
        })

        # Progress report
        pct = offset / total * 100
        elapsed = time.monotonic() - start_time
        rate = (offset - ckpt["offset"]) / elapsed if elapsed > 0 else 0
        eta = (total - offset) / rate if rate > 0 else 0
        log.info(
            "Batch %d-%d: %d ok, %d failed (%.1fs) | "
            "Total: %d/%d (%.1f%%) | %.0f docs/s | ETA %.0fm",
            offset - len(docs), offset,
            len(updates), batch_failures, batch_elapsed,
            offset, total, pct,
            rate, eta / 60,
        )

    # -- Summary ------------------------------------------------------------

    elapsed = time.monotonic() - start_time
    summary = {
        "embedded": embedded,
        "failed_docs": failed_docs,
        "failed_batches": len(failed_batches),
        "elapsed_minutes": round(elapsed / 60, 1),
        "shutdown_requested": _shutdown_requested,
    }

    if _shutdown_requested:
        log.info(
            "Stopped at offset %d/%d. %d embedded, %d failed. "
            "Resume with --resume.",
            offset, total, embedded, failed_docs,
        )
    else:
        log.info(
            "Done. %d embedded, %d failed docs, %d batch errors. Took %.1fm",
            embedded, failed_docs, len(failed_batches), elapsed / 60,
        )
    if failed_batches:
        log.warning("Failed batch offsets: %s", [b["offset"] for b in failed_batches])

    return summary


# ---------------------------------------------------------------------------
# Embedder setup helper
# ---------------------------------------------------------------------------


def setup_user_provided(
    meili_url: str = DEFAULT_MEILI_URL,
    index: str = DEFAULT_INDEX,
    embedder_name: str = DEFAULT_EMBEDDER_NAME,
    dimensions: int = 768,
) -> None:
    """Configure the Meilisearch embedder as ``userProvided``.

    Waits for any active indexing to finish before applying the change,
    then waits for the settings update task to succeed.
    """
    log.info("Setting embedder to userProvided (dims=%d) on %s...", dimensions, index)

    # Wait for active indexing to finish
    for _ in range(120):  # 10 minutes max
        stats = meili_get(meili_url, f"/indexes/{index}/stats")
        if not stats.get("isIndexing"):
            break
        log.info("Waiting for indexing to finish...")
        time.sleep(5)

    body = {
        "embedders": {
            embedder_name: {
                "source": "userProvided",
                "dimensions": dimensions,
            }
        }
    }
    task_resp = meili_patch(meili_url, f"/indexes/{index}/settings", body)
    task = wait_for_task(meili_url, task_resp["taskUid"], timeout=300)
    if task["status"] == "succeeded":
        log.info("Embedder set to userProvided (task %d)", task["uid"])
    else:
        log.error("Failed to update embedder: %s", task.get("error"))
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _env(name: str, default: str) -> str:
    """Read a string from the environment, falling back to *default*."""
    return os.environ.get(name, default)


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
    """Build the argument parser for ``batch_embed``."""
    parser = argparse.ArgumentParser(
        prog="batch_embed",
        description=(
            "Batch-embed Meilisearch documents via Ollama.  "
            "Processes documents in configurable pages with per-batch "
            "checkpointing for fault-tolerant re-embedding."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  %(prog)s --setup                    # configure embedder + embed all\n"
            "  %(prog)s --resume                   # continue from last checkpoint\n"
            "  %(prog)s --dry-run                  # preview without changes\n"
            "  %(prog)s --setup-only               # configure embedder only\n"
            "  %(prog)s --model nomic-embed-text    # use a different model\n"
        ),
    )
    parser.add_argument(
        "--model",
        default=_env("ERD_BATCH_MODEL", DEFAULT_MODEL),
        help="Ollama model name (env: ERD_BATCH_MODEL, default: %(default)s)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=_env_int("ERD_BATCH_SIZE", DEFAULT_BATCH_SIZE),
        help="Documents per Meilisearch page (env: ERD_BATCH_SIZE, default: %(default)s)",
    )
    parser.add_argument(
        "--ollama-batch-size",
        type=int,
        default=_env_int("ERD_BATCH_OLLAMA_SIZE", DEFAULT_OLLAMA_BATCH_SIZE),
        help="Texts per Ollama API call (env: ERD_BATCH_OLLAMA_SIZE, default: %(default)s)",
    )
    parser.add_argument(
        "--meili-url",
        default=_env("ERD_BATCH_MEILI_URL", DEFAULT_MEILI_URL),
        help="Meilisearch base URL (env: ERD_BATCH_MEILI_URL, default: %(default)s)",
    )
    parser.add_argument(
        "--ollama-url",
        default=_env("ERD_BATCH_OLLAMA_URL", DEFAULT_OLLAMA_URL),
        help="Ollama embed endpoint (env: ERD_BATCH_OLLAMA_URL, default: %(default)s)",
    )
    parser.add_argument(
        "--index",
        default=_env("ERD_BATCH_INDEX", DEFAULT_INDEX),
        help="Meilisearch index name (env: ERD_BATCH_INDEX, default: %(default)s)",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=DEFAULT_CHECKPOINT_DIR,
        help="Directory for checkpoint files (default: %(default)s)",
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Resume from last checkpoint instead of starting fresh",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview batches without embedding or updating Meilisearch",
    )
    parser.add_argument(
        "--setup", action="store_true",
        help="Set embedder to userProvided before embedding",
    )
    parser.add_argument(
        "--setup-only", action="store_true",
        help="Set embedder to userProvided and exit (no embedding)",
    )
    parser.add_argument(
        "--asymmetric", action="store_true",
        help="Use asymmetric prefixes (title: X | text: Y) for embeddinggemma",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for ``batch_embed``."""
    parser = build_parser()
    args = parser.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )

    # Install signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, _request_shutdown)
    signal.signal(signal.SIGTERM, _request_shutdown)

    if args.setup or args.setup_only:
        setup_user_provided(meili_url=args.meili_url, index=args.index)
        if args.setup_only:
            return

    run_batch_embed(
        model=args.model,
        batch_size=args.batch_size,
        ollama_batch_size=args.ollama_batch_size,
        ollama_url=args.ollama_url,
        meili_url=args.meili_url,
        index=args.index,
        checkpoint_dir=args.checkpoint_dir,
        resume=args.resume,
        dry_run=args.dry_run,
        asymmetric=args.asymmetric,
    )


if __name__ == "__main__":
    main()
