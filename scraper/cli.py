"""CLI entry point for the scraper.

Usage::

    python -m scraper                           # scrape all sources
    python -m scraper --source ethresearch      # scrape one source
    python -m scraper --url URL --output DIR    # one-off URL
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .discourse import DiscourseScraper


def _load_sources(repo_root: Path) -> list[dict]:
    """Load and validate sources.json from the repo root."""
    path = repo_root / "sources.json"
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("sources", [])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="scraper",
        description="Scrape Discourse forums defined in sources.json",
    )
    parser.add_argument(
        "--source",
        help="Name of a single source to scrape (from sources.json)",
    )
    parser.add_argument(
        "--url",
        help="One-off Discourse URL (not in sources.json)",
    )
    parser.add_argument(
        "--output",
        help="Output directory for --url mode (required with --url)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="Base delay between requests in seconds (default: 0.3)",
    )
    args = parser.parse_args(argv)

    # --url mode: one-off scrape
    if args.url:
        if not args.output:
            parser.error("--output is required when using --url")
        scraper = DiscourseScraper(
            args.url, args.output, delay=args.delay
        )
        scraper.run()
        return

    # Config-driven mode: read sources.json
    # Walk up to find repo root (directory containing sources.json)
    repo_root = Path(__file__).resolve().parent.parent
    sources = _load_sources(repo_root)

    if not sources:
        print("No sources defined in sources.json", file=sys.stderr)
        sys.exit(1)

    if args.source:
        matches = [s for s in sources if s["name"] == args.source]
        if not matches:
            names = ", ".join(s["name"] for s in sources)
            print(
                f"Unknown source '{args.source}'. Available: {names}",
                file=sys.stderr,
            )
            sys.exit(1)
        sources = matches

    for src in sources:
        if src.get("type") != "discourse":
            print(f"  Skipping '{src['name']}': type '{src.get('type')}' not supported")
            continue

        raw_dir = repo_root / src["raw_dir"]
        scraper = DiscourseScraper(
            src["url"], raw_dir, delay=args.delay
        )
        scraper.run()

    print("\nAll done.")
