"""CLI entry point for erd-index command.

Config precedence: CLI flags > environment variables > config/indexer.toml defaults.
See ``erd_index/settings.py`` for env var names (``ERD_MEILI_URL``, ``MEILI_MASTER_KEY``).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="erd-index",
        description="Ethereum Research Data indexer — Meilisearch ingestion pipeline",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config TOML (default: config/indexer.toml)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root directory (default: cwd)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=0,
        help="Override Meilisearch batch size (0 = use config default)",
    )

    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init", help="Initialize Meilisearch index and SQLite databases")

    # ingest-md
    md = sub.add_parser("ingest-md", help="Ingest markdown from corpus/")
    md.add_argument(
        "--changed-only", action="store_true", help="Only process changed files"
    )
    md.add_argument("--source-name", help="Only process a specific source")
    md.add_argument(
        "--dry-run", action="store_true", help="Parse and chunk without writing to Meilisearch"
    )

    # ingest-code
    code = sub.add_parser("ingest-code", help="Ingest code from configured repos")
    code.add_argument("--repo", help="Only process a specific repo")
    code.add_argument("--changed-only", action="store_true", help="Only process changed files")
    code.add_argument("--dry-run", action="store_true", help="Parse and chunk without writing")
    code.add_argument(
        "--max-files", type=int, default=0, help="Limit files processed (0 = all)"
    )

    # build-graph
    graph = sub.add_parser("build-graph", help="Build/update dependency graph")
    graph.add_argument("--changed-only", action="store_true")

    # sync
    sync = sub.add_parser("sync", help="Full sync: md + code + graph")
    sync.add_argument(
        "--full-rebuild",
        action="store_true",
        help="Reprocess all files (default: only changed files)",
    )
    sync.add_argument("--dry-run", action="store_true", help="Parse and chunk without writing")

    # link-specs
    sub.add_parser("link-specs", help="Find and upsert spec-to-code links via heuristics")

    # stats
    stats = sub.add_parser("stats", help="Show index and graph statistics")
    stats.add_argument("--repo", help="Show stats for a specific repo only")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s %(levelname)s %(message)s")

    # Lazy imports to keep CLI startup fast
    from erd_index.settings import load_settings

    settings = load_settings(
        config_path=args.config,
        project_root=args.project_root,
    )

    # Apply CLI overrides
    if args.batch_size > 0:
        settings.meili.batch_size = args.batch_size

    if args.command == "init":
        _cmd_init(settings)
    elif args.command == "ingest-md":
        _cmd_ingest_md(settings, args)
    elif args.command == "ingest-code":
        _cmd_ingest_code(settings, args)
    elif args.command == "build-graph":
        _cmd_build_graph(settings, args)
    elif args.command == "link-specs":
        _cmd_link_specs(settings, args)
    elif args.command == "sync":
        _cmd_sync(settings, args)
    elif args.command == "stats":
        _cmd_stats(settings, args)


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def _cmd_init(settings) -> None:
    from erd_index.graph.store import init_graph_db
    from erd_index.index.meili_client import init_index
    from erd_index.state.manifest_db import init_state_db

    init_index(settings)
    init_graph_db(settings)
    init_state_db(settings)
    print("Initialized Meilisearch index, graph DB, and state DB.")


def _cmd_ingest_md(settings, args) -> None:
    from erd_index.pipeline import ingest_markdown

    ingest_markdown(
        settings,
        changed_only=args.changed_only,
        source_name=args.source_name,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


def _cmd_ingest_code(settings, args) -> None:
    from erd_index.pipeline import ingest_code

    ingest_code(
        settings,
        repo_name=args.repo,
        changed_only=args.changed_only,
        dry_run=args.dry_run,
        max_files=args.max_files,
        verbose=args.verbose,
    )


def _cmd_build_graph(settings, args) -> None:
    from erd_index.pipeline import build_graph

    build_graph(settings, changed_only=args.changed_only, verbose=args.verbose)


def _cmd_link_specs(settings, args) -> None:
    from erd_index.pipeline import link_specs

    link_specs(settings, verbose=args.verbose)


def _cmd_sync(settings, args) -> None:
    from erd_index.pipeline import sync_all

    sync_all(
        settings,
        changed_only=not args.full_rebuild,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


def _cmd_stats(settings, args) -> None:
    from erd_index.pipeline import show_stats

    show_stats(settings, repo=getattr(args, "repo", None))
