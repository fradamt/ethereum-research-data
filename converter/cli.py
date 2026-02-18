"""CLI entry point for the converter module.

Usage:
    python -m converter                          # Convert all sources
    python -m converter --source ethresearch     # Convert one source
    python -m converter --max-replies 10         # Limit replies
    python -m converter --force                  # Re-convert even if output exists
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .discourse_to_md import DiscourseConverter


def load_sources(repo_root: Path) -> list[dict]:
    """Load source definitions from sources.json."""
    sources_path = repo_root / "sources.json"
    if not sources_path.exists():
        print(f"Error: {sources_path} not found", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(sources_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: {sources_path} contains invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    return data.get("sources", [])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="converter",
        description="Convert raw Discourse JSON topics to markdown.",
    )
    parser.add_argument(
        "--source",
        help="Convert only this source (by name from sources.json).",
    )
    parser.add_argument(
        "--max-replies",
        type=int,
        default=20,
        help="Maximum replies to include per topic (default: 20).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-convert all topics even if output already exists.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    sources = load_sources(repo_root)

    if not sources:
        print("No sources defined in sources.json", file=sys.stderr)
        sys.exit(1)

    # Filter to requested source
    if args.source:
        sources = [s for s in sources if s["name"] == args.source]
        if not sources:
            print(f"Error: source '{args.source}' not found in sources.json", file=sys.stderr)
            sys.exit(1)

    total_converted = 0
    total_skipped = 0

    for source in sources:
        if source.get("type") != "discourse":
            continue

        name = source["name"]
        raw_dir = repo_root / source["raw_dir"]
        corpus_dir = repo_root / source["corpus_dir"]

        if not raw_dir.exists():
            print(f"[{name}] raw directory not found: {raw_dir} — skipping")
            continue

        converter = DiscourseConverter(
            source_name=name,
            base_url=source["url"],
            raw_dir=raw_dir,
            corpus_dir=corpus_dir,
            max_replies=args.max_replies,
        )

        print(f"[{name}] Converting topics from {raw_dir} → {corpus_dir}")
        converted, skipped = converter.convert_all(force=args.force)
        print(f"[{name}] Converted {converted}, skipped {skipped}")
        total_converted += converted
        total_skipped += skipped

    print(f"\nTotal: converted {total_converted}, skipped {total_skipped}")
