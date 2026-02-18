#!/usr/bin/env python3
"""Benchmark embedding models for Ethereum research semantic search quality.

Samples documents from the Meilisearch index, embeds them with each candidate
model via Ollama, and ranks by cosine similarity to test queries.  Outputs a
side-by-side comparison of top results per query per model.

Usage:
    uv run python scripts/benchmark_embeddings.py
    uv run python scripts/benchmark_embeddings.py --models nomic-embed-text qwen3-embedding
    uv run python scripts/benchmark_embeddings.py --top 10
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/embed"
MEILI_URL = "http://localhost:7700"
MEILI_KEY = "erd-dev-key"

DEFAULT_MODELS = [
    "nomic-embed-text",
    "qwen3-embedding:0.6b",
    "embeddinggemma:300m",
]

# Queries from the user testing report, organized by category
QUERIES: list[tuple[str, str]] = [
    # (category, query)
    ("jargon", "SSZ Merkleization"),
    ("jargon", "KZG commitment verification"),
    ("jargon", "DAS polynomial commitment opening proof"),
    ("jargon", "blob gas pricing mechanism"),
    ("jargon", "validator withdrawal process"),
    ("jargon", "gossipsub mesh scoring"),
    ("natural", "how do blobs get propagated across the network"),
    ("natural", "what happens when a validator gets slashed"),
    ("natural", "why was EIP-1559 designed with a base fee"),
    ("conceptual", "proposer-builder separation"),
    ("conceptual", "single slot finality tradeoffs"),
    ("conceptual", "MEV and consensus security implications"),
    ("cross", "data availability sampling security assumptions"),
    ("cross", "beacon chain reorg resistance"),
    ("cross", "attestation aggregation subnet design"),
]

# Targeted sample queries to fetch a diverse document set from Meilisearch
SAMPLE_QUERIES: list[tuple[str, str | None]] = [
    # (query, optional filter)
    ("SSZ Merkleization", None),
    ("SSZ serialize", None),
    ("KZG commitment polynomial", None),
    ("blob gas base fee", None),
    ("proposer builder separation PBS", None),
    ("single slot finality", None),
    ("MEV extraction maximal extractable value", None),
    ("data availability sampling DAS", None),
    ("validator slashing penalty", None),
    ("gossipsub mesh peer scoring", None),
    ("EIP-1559 base fee burn", None),
    ("EIP-4844 blob transaction", None),
    ("attestation aggregation committee", None),
    ("withdrawal request", None),
    ("beacon chain fork choice", None),
    ("verkle tree state", None),
    ("LMD-GHOST fork choice", None),
    ("Casper FFG finality", None),
    ("blob propagation network", None),
    ("reorg resistance attack", None),
    ("", "source_kind = 'eip' AND eip_status = 'Final'"),
    ("", "source_kind = 'code' AND language = 'python'"),
    ("", "source_kind = 'code' AND language = 'go'"),
    ("", "source_kind = 'code' AND language = 'rust'"),
]

# Max chars per document text for embedding (fairness across context lengths)
MAX_DOC_CHARS = 6000


# ---------------------------------------------------------------------------
# Meilisearch helpers
# ---------------------------------------------------------------------------


def meili_search(
    query: str, *, filt: str | None = None, limit: int = 10
) -> list[dict]:
    body: dict = {
        "q": query,
        "limit": limit,
        "attributesToRetrieve": [
            "id", "doc_id", "title", "text", "source_kind",
            "chunk_kind", "symbol_name", "source_name", "author",
            "eip", "path",
        ],
    }
    if filt:
        body["filter"] = filt
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{MEILI_URL}/indexes/eth_chunks_v1/search",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MEILI_KEY}",
        },
    )
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read())["hits"]


# ---------------------------------------------------------------------------
# Ollama embedding
# ---------------------------------------------------------------------------


def embed(texts: list[str], model: str) -> list[list[float]]:
    """Embed texts via Ollama /api/embed.  Retries once on failure."""
    data = json.dumps({"model": model, "input": texts}).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=180)
        return json.loads(resp.read())["embeddings"]
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(f"  ERROR from Ollama ({model}): {exc.code} — {body[:200]}", file=sys.stderr)
        raise


def embed_batched(
    texts: list[str], model: str, batch_size: int = 16
) -> list[list[float]]:
    """Embed texts in batches, with progress."""
    all_embs: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        embs = embed(batch, model)
        all_embs.extend(embs)
        done = min(i + batch_size, len(texts))
        print(f"    {done}/{len(texts)} embedded", end="\r")
    print()
    return all_embs


# ---------------------------------------------------------------------------
# Math
# ---------------------------------------------------------------------------


def cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# ---------------------------------------------------------------------------
# Document sampling
# ---------------------------------------------------------------------------


def sample_documents() -> list[dict]:
    """Fetch a diverse set of documents from Meilisearch."""
    docs: list[dict] = []
    seen: set[str] = set()
    for q, f in SAMPLE_QUERIES:
        try:
            hits = meili_search(q, filt=f, limit=8)
        except Exception as exc:
            print(f"  Warning: query {q!r} failed: {exc}", file=sys.stderr)
            continue
        for h in hits:
            if h["id"] not in seen:
                seen.add(h["id"])
                docs.append(h)
    return docs


def doc_text(d: dict) -> str:
    """Build embedding text from a document, matching Meilisearch template."""
    title = d.get("title") or ""
    text = d.get("text") or ""
    combined = f"{title} {text}".strip() if title else text
    return combined[:MAX_DOC_CHARS]


def doc_label(d: dict, max_len: int = 55) -> str:
    """Short label for display."""
    sk = d.get("source_kind", "?")
    label = d.get("title") or d.get("symbol_name") or d.get("path") or d["id"]
    label = label.replace("\n", " ")
    if len(label) > max_len:
        label = label[:max_len - 1] + "\u2026"
    return f"({sk}) {label}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run_benchmark(models: list[str], top_k: int = 5) -> dict:
    """Run the full benchmark. Returns structured results."""

    # 1. Sample documents
    print("=" * 70)
    print("Phase 1: Sampling documents from Meilisearch")
    print("=" * 70)
    docs = sample_documents()
    print(f"Sampled {len(docs)} unique documents")

    # Show source distribution
    by_kind: dict[str, int] = {}
    for d in docs:
        sk = d.get("source_kind", "unknown")
        by_kind[sk] = by_kind.get(sk, 0) + 1
    for sk, count in sorted(by_kind.items()):
        print(f"  {sk}: {count}")

    texts = [doc_text(d) for d in docs]
    query_texts = [q for _, q in QUERIES]

    # 2. Embed with each model
    results: dict[str, dict] = {}

    for model in models:
        print()
        print("=" * 70)
        print(f"Phase 2: Embedding with {model}")
        print("=" * 70)

        t0 = time.time()

        # Warm up / ensure model is loaded
        print(f"  Loading model...")
        try:
            test = embed(["test"], model)
            dims = len(test[0])
        except Exception as exc:
            print(f"  FAILED to load {model}: {exc}")
            print(f"  Skipping this model.")
            continue

        print(f"  Dimensions: {dims}")

        # Embed queries
        print(f"  Embedding {len(query_texts)} queries...")
        query_embs = embed(query_texts, model)

        # Embed documents
        print(f"  Embedding {len(texts)} documents...")
        doc_embs = embed_batched(texts, model)

        elapsed = time.time() - t0
        print(f"  Completed in {elapsed:.1f}s")

        # 3. Rank
        model_results: dict[str, list[tuple[float, int]]] = {}
        for qi, (cat, query) in enumerate(QUERIES):
            scores = []
            for di, de in enumerate(doc_embs):
                sim = cosine_sim(query_embs[qi], de)
                scores.append((sim, di))
            scores.sort(reverse=True)
            model_results[query] = scores[:top_k]

        results[model] = {
            "dims": dims,
            "elapsed": elapsed,
            "rankings": model_results,
        }

    # 4. Print comparison
    print()
    print("=" * 70)
    print("RESULTS: Side-by-side top-{} per query".format(top_k))
    print("=" * 70)

    for cat, query in QUERIES:
        print(f"\n{'─' * 70}")
        print(f"[{cat.upper()}] {query}")
        print(f"{'─' * 70}")

        for model in models:
            if model not in results:
                continue
            rankings = results[model]["rankings"][query]
            short_model = model.split(":")[0].replace("nomic-embed-text", "nomic")
            short_model = short_model.replace("qwen3-embedding", "qwen3")
            short_model = short_model.replace("embeddinggemma", "gemma")
            print(f"  {short_model}:")
            for rank, (sim, di) in enumerate(rankings):
                label = doc_label(docs[di])
                print(f"    {rank + 1}. [{sim:+.4f}] {label}")

    # 5. Summary stats
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for model in models:
        if model not in results:
            continue
        r = results[model]
        short = model.split(":")[0]
        avg_top1 = sum(
            r["rankings"][q][0][0] for _, q in QUERIES
        ) / len(QUERIES)
        avg_top5 = sum(
            sum(s for s, _ in r["rankings"][q]) / len(r["rankings"][q])
            for _, q in QUERIES
        ) / len(QUERIES)
        print(f"  {short}:")
        print(f"    Dims: {r['dims']}, Time: {r['elapsed']:.1f}s")
        print(f"    Avg top-1 similarity: {avg_top1:.4f}")
        print(f"    Avg top-5 similarity: {avg_top5:.4f}")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark embedding models")
    parser.add_argument(
        "--models", nargs="+", default=DEFAULT_MODELS,
        help="Models to benchmark (default: %(default)s)",
    )
    parser.add_argument(
        "--top", type=int, default=5,
        help="Number of top results per query (default: 5)",
    )
    args = parser.parse_args()

    run_benchmark(args.models, top_k=args.top)


if __name__ == "__main__":
    main()
