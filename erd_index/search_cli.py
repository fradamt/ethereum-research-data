"""CLI for searching the Meilisearch index.

Wraps the Meilisearch search API with structured subcommands for querying
and viewing index statistics.

Configuration precedence: CLI flags > environment variables > built-in defaults.

Environment variables::

    ERD_MEILI_URL    (default http://localhost:7700)
    ERD_SEARCH_KEY   (default: read from ~/.config/erd/search-key, or empty)
    ERD_ADMIN_KEY    (default: read from ~/.config/erd/admin-key, or empty)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_MEILI_URL = "http://localhost:7700"
DEFAULT_INDEX = "eth_chunks_v1"
DEFAULT_LIMIT = 10
DEFAULT_SEMANTIC_RATIO = 0.5
DEFAULT_MIN_TEXT_LENGTH = 50
DEFAULT_FIELDS = "title,text,url,path,start_line,heading_path,source_kind,source_name,author"
DEFAULT_DISTINCT = "doc_id"
_TEXT_PREVIEW_LEN = 200
_TEXT_FULL_LEN = 4000

# ---------------------------------------------------------------------------
# Env helpers
# ---------------------------------------------------------------------------


def _env_str(name: str, default: str) -> str:
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
        return default


def _read_key_file(path: str) -> str:
    """Read a single-line key from *path*, returning empty string on failure."""
    try:
        with open(os.path.expanduser(path)) as f:
            return f.read().strip()
    except OSError:
        return ""


def _default_search_key() -> str:
    """Resolve the search API key: env var > file > empty."""
    env = os.environ.get("ERD_SEARCH_KEY")
    if env is not None:
        return env
    return _read_key_file("~/.config/erd/search-key")


def _default_admin_key() -> str:
    """Resolve the admin API key: env var > file > empty."""
    env = os.environ.get("ERD_ADMIN_KEY")
    if env is not None:
        return env
    return _read_key_file("~/.config/erd/admin-key")


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

_TIMEOUT = 10  # seconds


def _meili_request(
    url: str,
    key: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
) -> dict:
    """Send an HTTP request to Meilisearch and return the JSON response."""
    data = json.dumps(payload).encode() if payload is not None else None
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=_TIMEOUT)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(f"Error: Meilisearch returned {exc.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Error: cannot reach Meilisearch at {url}: {exc.reason}", file=sys.stderr)
        sys.exit(1)
    return json.loads(resp.read())


# ---------------------------------------------------------------------------
# Search payload builder
# ---------------------------------------------------------------------------


def build_search_params(args: argparse.Namespace) -> dict:
    """Build the Meilisearch search payload from parsed CLI args."""
    query_text = args.query_text

    # Hybrid
    ratio = getattr(args, "hybrid", None)
    if ratio is not None:
        # Expand Ethereum abbreviations so the embedding model gets richer
        # context.  Keyword search already has Meilisearch synonyms.
        no_expand = getattr(args, "no_expand", False)
        if not no_expand:
            from erd_index.index.terminology import expand_query

            query_text = expand_query(query_text)

        # At ratio >= 0.6, Meilisearch uses pure vector ranking (binary
        # switch).  Prepend the embeddinggemma retrieval prefix so the model
        # activates its retrieval-optimised behaviour.
        if ratio >= 0.6:
            from erd_index.index.terminology import prefix_query_for_embedding

            query_text = prefix_query_for_embedding(query_text)

    params: dict = {"q": query_text, "limit": args.limit}

    # Filters
    filters = _build_filters(args)

    if ratio is not None:
        params["hybrid"] = {"semanticRatio": ratio, "embedder": "default"}
        # Filter short chunks whose embeddings are too generic for semantic search
        min_len = getattr(args, "min_text_length", DEFAULT_MIN_TEXT_LENGTH)
        if min_len is None:
            min_len = DEFAULT_MIN_TEXT_LENGTH
        if min_len > 0:
            filters.append(f"text_length >= {min_len}")

    if filters:
        params["filter"] = " AND ".join(filters)

    # Sort
    sort = getattr(args, "sort", None)
    if sort:
        params["sort"] = [sort]

    # Fields
    fields = getattr(args, "fields", DEFAULT_FIELDS)
    if fields:
        params["attributesToRetrieve"] = [f.strip() for f in fields.split(",")]

    # Distinct
    no_distinct = getattr(args, "no_distinct", False)
    if no_distinct:
        pass  # omit distinct
    else:
        distinct = getattr(args, "distinct", DEFAULT_DISTINCT)
        if distinct:
            params["distinct"] = distinct

    return params


def _build_filters(args: argparse.Namespace) -> list[str]:
    """Collect filter expressions from typed flags and raw --filter."""
    filters: list[str] = []

    source_kind = getattr(args, "source_kind", None)
    if source_kind:
        filters.append(f'source_kind = "{source_kind}"')
    elif not getattr(args, "include_code", False):
        filters.append("source_kind != 'code'")

    source_name = getattr(args, "source_name", None)
    if source_name:
        filters.append(f'source_name = "{source_name}"')

    author = getattr(args, "author", None)
    if author:
        filters.append(f'author = "{author}"')

    eip = getattr(args, "eip", None)
    if eip is not None:
        filters.append(f"eip = {eip}")

    eip_status = getattr(args, "eip_status", None)
    if eip_status:
        filters.append(f'eip_status = "{eip_status}"')

    repo = getattr(args, "repo", None)
    if repo:
        filters.append(f'repository = "{repo}"')

    raw_filter = getattr(args, "filter", None)
    if raw_filter:
        filters.append(raw_filter)

    return filters


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def format_hit(idx: int, hit: dict, *, full: bool = False) -> str:
    """Format a single search hit for terminal display."""
    lines: list[str] = []

    # Title line
    title = hit.get("title") or hit.get("symbol_name") or "(untitled)"
    lines.append(f"[{idx}] {title}")

    # Metadata line
    meta_parts: list[str] = []
    for field in ("source_kind", "source_name", "author"):
        val = hit.get(field)
        if val:
            meta_parts.append(str(val))
    if meta_parts:
        lines.append("    " + " | ".join(meta_parts))

    # Heading path (section context)
    heading_path = hit.get("heading_path")
    if heading_path:
        lines.append("    " + " > ".join(heading_path))

    # URL / path line — show both when available
    url = hit.get("url")
    path = hit.get("path")
    start_line = hit.get("start_line")
    if url:
        lines.append(f"    {url}")
    if path:
        loc = f"{path}:{start_line}" if start_line else path
        lines.append(f"    {loc}")

    # Text: full mode shows up to 4000 chars, default shows 200-char preview
    text = hit.get("text", "")
    if text:
        max_len = _TEXT_FULL_LEN if full else _TEXT_PREVIEW_LEN
        preview = text[:max_len].replace("\n", " ").strip()
        if len(text) > max_len:
            preview += "..."
        wrapped = textwrap.fill(preview, width=96, initial_indent="    ", subsequent_indent="    ")
        lines.append(wrapped)

    return "\n".join(lines)


def _print_results(data: dict, *, json_mode: bool, verbose: bool, full: bool = False) -> None:
    """Print search results to stdout."""
    if json_mode:
        print(json.dumps(data, indent=2))
        return

    hits = data.get("hits", [])
    for i, hit in enumerate(hits, 1):
        if i > 1:
            print()
        print(format_hit(i, hit, full=full))

    # Summary
    total = data.get("estimatedTotalHits", len(hits))
    ms = data.get("processingTimeMs", 0)
    print(f"\n{total} results ({ms}ms)")

    if verbose:
        for key in ("query", "filter", "sort", "semanticHitCount"):
            val = data.get(key)
            if val is not None:
                print(f"  {key}: {val}")


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------


def _cmd_query(args: argparse.Namespace) -> None:
    """Execute a search query against the index."""
    url = f"{args.url}/indexes/{DEFAULT_INDEX}/search"
    params = build_search_params(args)
    data = _meili_request(url, args.key, method="POST", payload=params)
    _print_results(data, json_mode=args.json, verbose=args.verbose, full=getattr(args, "full", False))


def _cmd_stats(args: argparse.Namespace) -> None:
    """Show index statistics."""
    url = f"{args.url}/indexes/{DEFAULT_INDEX}/stats"
    data = _meili_request(url, args.key)
    if args.json:
        print(json.dumps(data, indent=2))
        return
    print(f"Documents:  {data.get('numberOfDocuments', '?')}")
    field_dist = data.get("fieldDistribution", {})
    if field_dist:
        print("Field distribution:")
        for field, count in sorted(field_dist.items()):
            print(f"  {field}: {count}")


def _cmd_apply_terminology(args: argparse.Namespace) -> None:
    """Apply Ethereum synonyms and dictionary to the Meilisearch index."""
    from erd_index.index.terminology import (
        apply_terminology_settings,
        get_ethereum_dictionary,
        get_ethereum_synonyms,
    )

    synonyms = get_ethereum_synonyms()
    dictionary = get_ethereum_dictionary()
    print(f"Applying {len(synonyms)} synonym entries and {len(dictionary)} dictionary terms...")
    apply_terminology_settings(args.url, args.key, DEFAULT_INDEX)
    print("Terminology settings applied successfully.")


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for ``eth-search``."""
    parser = argparse.ArgumentParser(
        prog="eth-search",
        description="Search the Ethereum Research Data Meilisearch index.",
    )
    parser.add_argument(
        "--url",
        default=_env_str("ERD_MEILI_URL", DEFAULT_MEILI_URL),
        help=f"Meilisearch URL (env: ERD_MEILI_URL, default: {DEFAULT_MEILI_URL})",
    )
    parser.add_argument(
        "--key",
        default=None,
        help="API key (env: ERD_SEARCH_KEY or ERD_ADMIN_KEY)",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show search metadata")

    sub = parser.add_subparsers(dest="command")

    # --- query ---
    q = sub.add_parser("query", help="Search the index")
    q.add_argument("query_text", help="Search query text")
    q.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max results (default {DEFAULT_LIMIT})")
    q.add_argument(
        "--source-kind", choices=["forum", "eip", "code", "generic"],
        help="Filter by source kind",
    )
    q.add_argument("--source-name", help="Filter by source name")
    q.add_argument("--author", help="Filter by author")
    q.add_argument("--eip", type=int, help="Filter by EIP number")
    q.add_argument("--eip-status", help="Filter by EIP status")
    q.add_argument("--repo", help="Filter by repository name")
    q.add_argument("--filter", help="Raw Meilisearch filter expression")
    q.add_argument(
        "--hybrid", type=float, nargs="?", const=DEFAULT_SEMANTIC_RATIO, default=None,
        help=(
            f"Enable hybrid (semantic) search. "
            f"Optional ratio 0.0-1.0 (default {DEFAULT_SEMANTIC_RATIO} if flag given without value)"
        ),
    )
    q.add_argument("--sort", help='Sort expression (e.g. "source_date_ts:desc")')
    q.add_argument(
        "--fields", default=DEFAULT_FIELDS,
        help=f"Comma-separated fields to retrieve (default: {DEFAULT_FIELDS})",
    )
    q.add_argument(
        "--distinct", default=DEFAULT_DISTINCT,
        help=f"Distinct field (default: {DEFAULT_DISTINCT})",
    )
    q.add_argument("--no-distinct", action="store_true", help="Disable distinct (show all chunks)")
    q.add_argument(
        "--include-code", action="store_true",
        help="Include code chunks in results (excluded by default)",
    )
    q.add_argument(
        "--no-expand", action="store_true",
        help="Disable query expansion for hybrid search (expands Ethereum abbreviations by default)",
    )
    q.add_argument(
        "--min-text-length", type=int, default=None,
        help=(
            f"Minimum text length for hybrid search results "
            f"(default {DEFAULT_MIN_TEXT_LENGTH}; 0 to disable)"
        ),
    )
    q.add_argument(
        "--full", action="store_true",
        help="Show full text instead of 200-char preview (up to 4000 chars)",
    )

    # --- stats ---
    sub.add_parser("stats", help="Show index statistics")

    # --- apply-terminology ---
    sub.add_parser("apply-terminology", help="Apply Ethereum synonyms and dictionary to the index")

    return parser


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for ``eth-search``."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Resolve API key: --key flag > env/file defaults
    if args.key is None:
        if args.command in ("stats", "apply-terminology"):
            args.key = _default_admin_key()
        else:
            args.key = _default_search_key()

    if args.command == "query":
        _cmd_query(args)
    elif args.command == "stats":
        _cmd_stats(args)
    elif args.command == "apply-terminology":
        _cmd_apply_terminology(args)


if __name__ == "__main__":
    main()
