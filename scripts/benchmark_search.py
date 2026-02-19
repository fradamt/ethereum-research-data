"""Automated search quality benchmark for eth-search (Meilisearch index eth_chunks_v1).

Loads ground truth queries from benchmark_queries.py, runs searches against live
Meilisearch for each query x mode, scores results using regex pattern matching,
and outputs a JSON report + terminal summary table.

Usage:
    uv run python scripts/benchmark_search.py                         # run all
    uv run python scripts/benchmark_search.py --mode keyword          # one mode
    uv run python scripts/benchmark_search.py --query ssz-merkleization
    uv run python scripts/benchmark_search.py --category jargon
    uv run python scripts/benchmark_search.py --json                  # JSON only
    uv run python scripts/benchmark_search.py --output report.json    # save JSON
    uv run python scripts/benchmark_search.py --baseline prev.json    # compare
    uv run python scripts/benchmark_search.py --verbose               # per-result
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from scripts.benchmark_queries import BENCHMARK_QUERIES, DEFAULT_MODES

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MEILI_URL = "http://localhost:7700"
INDEX_UID = "eth_chunks_v1"
SEARCH_LIMIT = 5
_TIMEOUT = 30  # seconds per request

MODES: dict[str, dict | None] = {
    "keyword": None,
    "hybrid_0.5": {"semanticRatio": 0.5, "embedder": "default"},
    "hybrid_0.7": {"semanticRatio": 0.7, "embedder": "default"},
    "semantic_1.0": {"semanticRatio": 1.0, "embedder": "default"},
}

RETRIEVE_FIELDS = [
    "title",
    "text",
    "source_kind",
    "source_name",
    "author",
    "url",
    "dedupe_key",
]

# ---------------------------------------------------------------------------
# API key resolution (same precedence as search_cli.py)
# ---------------------------------------------------------------------------


def _read_key_file(path: str) -> str:
    try:
        with open(os.path.expanduser(path)) as f:
            return f.read().strip()
    except OSError:
        return ""


def resolve_api_key(cli_key: str | None) -> str:
    """Resolve search API key: --key > env > file > fallback."""
    if cli_key:
        return cli_key
    env = os.environ.get("ERD_SEARCH_KEY")
    if env is not None:
        return env
    from_file = _read_key_file("~/.config/erd/search-key")
    if from_file:
        return from_file
    return "erd-dev-key"


# ---------------------------------------------------------------------------
# Query expansion (optional — works without erd_index installed)
# ---------------------------------------------------------------------------

_expand_query_fn = None


def _get_expand_fn():
    global _expand_query_fn
    if _expand_query_fn is not None:
        return _expand_query_fn
    try:
        from erd_index.index.terminology import expand_query

        _expand_query_fn = expand_query
    except ImportError:
        _expand_query_fn = False  # sentinel: tried and failed
    return _expand_query_fn


def maybe_expand_query(query: str, mode: str, should_expand: bool) -> str:
    """Expand the query for hybrid/semantic modes if requested."""
    if mode == "keyword" or not should_expand:
        return query
    fn = _get_expand_fn()
    if fn:
        return fn(query)
    return query


_prefix_query_fn = None


def _get_prefix_fn():
    global _prefix_query_fn
    if _prefix_query_fn is not None:
        return _prefix_query_fn
    try:
        from erd_index.index.terminology import prefix_query_for_embedding

        _prefix_query_fn = prefix_query_for_embedding
    except ImportError:
        _prefix_query_fn = False
    return _prefix_query_fn


def maybe_prefix_query(query: str, mode: str) -> str:
    """Prepend the embeddinggemma retrieval prefix for pure-semantic modes.

    At ratio >= 0.6, Meilisearch uses pure vector ranking.  The prefix
    activates embeddinggemma's retrieval-optimised behaviour.
    """
    hybrid_params = MODES.get(mode)
    if hybrid_params is None:
        return query  # keyword — no prefix
    ratio = hybrid_params.get("semanticRatio", 0)
    if ratio < 0.6:
        return query  # keyword-dominant — prefix would add noise
    fn = _get_prefix_fn()
    if fn:
        return fn(query)
    return query


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def meili_search(query: str, *, api_key: str, hybrid: dict | None = None) -> dict:
    """Run a single search against Meilisearch, return the full response dict."""
    url = f"{MEILI_URL}/indexes/{INDEX_UID}/search"
    payload: dict = {
        "q": query,
        "limit": SEARCH_LIMIT,
        "filter": "source_kind != 'code'",
        "distinct": "dedupe_key",
        "attributesToRetrieve": RETRIEVE_FIELDS,
    }
    if hybrid is not None:
        payload["hybrid"] = hybrid

    data = json.dumps(payload).encode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=_TIMEOUT)
        return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        return {"error": f"HTTP {exc.code}: {body[:300]}", "hits": []}
    except urllib.error.URLError as exc:
        return {"error": f"Connection failed: {exc.reason}", "hits": []}


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_hit(hit: dict, query_def: dict) -> dict:
    """Score a single hit against query patterns. Returns enriched hit dict."""
    search_text = f"{hit.get('title', '')} {hit.get('text', '')}"
    relevant = any(re.search(p, search_text) for p in query_def["relevance_patterns"])
    strong = any(re.search(p, search_text) for p in query_def["strong_patterns"])
    anti = any(re.search(p, search_text) for p in query_def["anti_patterns"])
    return {
        "title": hit.get("title", ""),
        "source_kind": hit.get("source_kind", ""),
        "source_name": hit.get("source_name", ""),
        "dedupe_key": hit.get("dedupe_key", ""),
        "relevant": relevant,
        "strong": strong,
        "anti": anti,
    }


def compute_metrics(scored_hits: list[dict], query_def: dict) -> dict:
    """Compute precision/strong/contamination/source_kind_ok from scored hits."""
    n = len(scored_hits) if scored_hits else 1  # avoid division by zero
    relevant_count = sum(1 for h in scored_hits if h["relevant"])
    strong_count = sum(1 for h in scored_hits if h["strong"])
    anti_count = sum(1 for h in scored_hits if h["anti"])

    expected_kinds = set(query_def.get("expected_source_kinds", []))
    actual_kinds = {h["source_kind"] for h in scored_hits}
    source_kind_ok = bool(expected_kinds & actual_kinds) if expected_kinds else True

    return {
        "precision_at_5": relevant_count / n,
        "strong_at_5": strong_count / n,
        "contamination_at_5": anti_count / n,
        "source_kind_ok": source_kind_ok,
    }


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------


def run_benchmark(
    *,
    api_key: str,
    modes: list[str],
    queries: list[dict],
    verbose: bool = False,
) -> dict:
    """Run the full benchmark. Returns the JSON report structure."""
    total_searches = 0
    t0 = time.time()
    per_query_results: list[dict] = []

    for qi, qdef in enumerate(queries, 1):
        qid = qdef["id"]
        query_text = qdef["query"]
        category = qdef["category"]
        allowed_modes = qdef.get("modes_to_test", DEFAULT_MODES)

        query_result: dict = {
            "id": qid,
            "query": query_text,
            "category": category,
            "results": {},
        }

        for mode in modes:
            if mode not in allowed_modes:
                continue

            # Expand query for hybrid/semantic modes if flagged
            q = maybe_expand_query(query_text, mode, qdef.get("expand_for_hybrid", False))
            # Add embeddinggemma retrieval prefix for pure-semantic modes
            q = maybe_prefix_query(q, mode)
            hybrid_params = MODES[mode]

            # Run search
            resp = meili_search(q, api_key=api_key, hybrid=hybrid_params)
            total_searches += 1
            hits = resp.get("hits", [])

            if "error" in resp:
                print(f"  WARNING: {qid}/{mode}: {resp['error']}", file=sys.stderr)

            # Score hits
            scored = [score_hit(h, qdef) for h in hits]
            metrics = compute_metrics(scored, qdef)

            query_result["results"][mode] = {
                **metrics,
                "hits": scored,
            }

        per_query_results.append(query_result)

        if not verbose:
            print(f"\r  {qi}/{len(queries)} queries completed", end="", file=sys.stderr)

    if not verbose:
        print(file=sys.stderr)  # newline after progress

    elapsed = time.time() - t0

    # Build aggregate metrics
    aggregate = _build_aggregate(per_query_results, modes)
    by_category = _build_by_category(per_query_results, modes)

    return {
        "timestamp": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "total_queries": len(queries),
        "total_searches": total_searches,
        "elapsed_seconds": round(elapsed, 1),
        "aggregate": aggregate,
        "by_category": by_category,
        "per_query": per_query_results,
    }


def _build_aggregate(per_query: list[dict], modes: list[str]) -> dict:
    """Compute per-mode aggregate metrics across all queries."""
    agg: dict[str, dict] = {}
    for mode in modes:
        precisions = []
        strongs = []
        contaminations = []
        source_ok_count = 0
        total = 0
        for qr in per_query:
            if mode not in qr["results"]:
                continue
            m = qr["results"][mode]
            precisions.append(m["precision_at_5"])
            strongs.append(m["strong_at_5"])
            contaminations.append(m["contamination_at_5"])
            if m["source_kind_ok"]:
                source_ok_count += 1
            total += 1
        if total == 0:
            continue
        agg[mode] = {
            "precision_at_5": round(sum(precisions) / total, 3),
            "strong_at_5": round(sum(strongs) / total, 3),
            "contamination": round(sum(contaminations) / total, 3),
            "source_ok": f"{source_ok_count}/{total}",
        }
    return agg


def _build_by_category(per_query: list[dict], modes: list[str]) -> dict:
    """Compute per-category, per-mode precision."""
    cats: dict[str, dict] = {}
    for qr in per_query:
        cat = qr["category"]
        if cat not in cats:
            cats[cat] = {"n": 0, "modes": {m: [] for m in modes}}
        cats[cat]["n"] += 1
        for mode in modes:
            if mode in qr["results"]:
                cats[cat]["modes"][mode].append(qr["results"][mode]["precision_at_5"])

    result: dict[str, dict] = {}
    for cat, data in cats.items():
        entry: dict = {"n": data["n"]}
        for mode in modes:
            vals = data["modes"][mode]
            entry[mode] = round(sum(vals) / len(vals), 2) if vals else None
        result[cat] = entry
    return result


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def print_report(report: dict, *, verbose: bool = False, baseline: dict | None = None) -> None:
    """Print the terminal summary table."""
    n_queries = report["total_queries"]
    n_searches = report["total_searches"]
    elapsed = report["elapsed_seconds"]
    agg = report["aggregate"]
    by_cat = report["by_category"]
    modes = list(agg.keys())

    print(
        f"\neth-search benchmark -- {n_queries} queries x {len(modes)} modes = {n_searches} searches"
    )
    print()

    # Mode summary table
    header = (
        f"{'Mode':<16}{'Precision@5':>12}{'Strong@5':>10}{'Contamination':>15}{'Source OK':>12}"
    )
    print(header)
    for mode in modes:
        m = agg[mode]
        delta = ""
        if baseline and mode in baseline.get("aggregate", {}):
            bp = baseline["aggregate"][mode]["precision_at_5"]
            dp = m["precision_at_5"] - bp
            delta = f" ({dp:+.3f})" if dp != 0 else ""
        print(
            f"{mode:<16}{m['precision_at_5']:>12.3f}{delta}"
            f"{m['strong_at_5']:>10.3f}"
            f"{m['contamination']:>15.3f}"
            f"{m['source_ok']:>12}"
        )

    # Category breakdown
    print(f"\n{'By Category:'}")
    cat_modes = modes[:4]  # show at most 4 modes in table
    cat_header = f"{'Category':<14}{'N':>4}"
    for mode in cat_modes:
        short = mode.replace("hybrid_", "H").replace("semantic_", "S").replace("keyword", "Keyword")
        cat_header += f"{short:>10}"
    print(cat_header)
    for cat in sorted(by_cat.keys()):
        d = by_cat[cat]
        row = f"{cat:<14}{d['n']:>4}"
        for mode in cat_modes:
            val = d.get(mode)
            row += f"{val:>10.2f}" if val is not None else f"{'--':>10}"
        print(row)

    # Failures (precision < 0.40)
    failures: list[str] = []
    for qr in report["per_query"]:
        parts = []
        for mode in modes:
            if mode in qr["results"]:
                p = qr["results"][mode]["precision_at_5"]
                if p < 0.40:
                    parts.append(f"{mode}={p:.2f}")
        if parts:
            failures.append(f"  {qr['id']}   {' '.join(parts)}")

    print("\nFailures (precision@5 < 0.40):")
    if failures:
        for f in failures:
            print(f)
    else:
        print("  (none)")

    # Contamination detected
    contaminated: list[str] = []
    for qr in report["per_query"]:
        for mode in modes:
            if mode in qr["results"]:
                c = qr["results"][mode]["contamination_at_5"]
                if c > 0:
                    contaminated.append(f"  {qr['id']}   {mode}={c:.2f}")

    print("\nContamination detected:")
    if contaminated:
        for c in contaminated:
            print(c)
    else:
        print("  (none)")

    print(f"\n{n_queries} queries, {n_searches} searches, {elapsed}s")

    # Verbose per-result details
    if verbose:
        print(f"\n{'=' * 70}")
        print("Per-result details:")
        print(f"{'=' * 70}")
        for qr in report["per_query"]:
            print(f"\n--- {qr['id']}: {qr['query']} [{qr['category']}] ---")
            for mode in modes:
                if mode not in qr["results"]:
                    continue
                mr = qr["results"][mode]
                print(
                    f"  {mode}: P={mr['precision_at_5']:.2f} S={mr['strong_at_5']:.2f} C={mr['contamination_at_5']:.2f}"
                )
                for i, h in enumerate(mr["hits"], 1):
                    flags = []
                    if h["relevant"]:
                        flags.append("R")
                    if h["strong"]:
                        flags.append("S")
                    if h["anti"]:
                        flags.append("X")
                    flag_str = ",".join(flags) if flags else "-"
                    title = h["title"][:60] if h["title"] else "(untitled)"
                    print(f"    {i}. [{flag_str}] ({h['source_kind']}) {title}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="benchmark_search",
        description="Benchmark eth-search quality with ground truth queries.",
    )
    parser.add_argument(
        "--mode",
        choices=list(MODES.keys()),
        help="Run only this search mode (default: all)",
    )
    parser.add_argument(
        "--query",
        dest="query_id",
        help="Run only this query (by id)",
    )
    parser.add_argument(
        "--category",
        help="Run only queries in this category",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON report only (no terminal table)",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Save JSON report to file",
    )
    parser.add_argument(
        "--baseline",
        metavar="FILE",
        help="Compare with a previous JSON report",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show per-result scoring details",
    )
    parser.add_argument(
        "--key",
        default=None,
        help="Meilisearch API key (env: ERD_SEARCH_KEY, file: ~/.config/erd/search-key)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    api_key = resolve_api_key(args.key)

    # Filter modes
    modes = list(MODES.keys())
    if args.mode:
        modes = [args.mode]

    # Filter queries
    queries = list(BENCHMARK_QUERIES)
    if args.query_id:
        queries = [q for q in queries if q["id"] == args.query_id]
        if not queries:
            print(f"Error: no query with id '{args.query_id}'", file=sys.stderr)
            sys.exit(1)
    if args.category:
        queries = [q for q in queries if q["category"] == args.category]
        if not queries:
            print(f"Error: no queries in category '{args.category}'", file=sys.stderr)
            sys.exit(1)

    # Load baseline
    baseline = None
    if args.baseline:
        try:
            with open(args.baseline) as f:
                baseline = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not load baseline: {exc}", file=sys.stderr)

    # Run
    report = run_benchmark(
        api_key=api_key,
        modes=modes,
        queries=queries,
        verbose=args.verbose,
    )

    # Output
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report, verbose=args.verbose, baseline=baseline)

    # Save JSON report
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
