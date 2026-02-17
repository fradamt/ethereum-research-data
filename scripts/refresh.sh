#!/bin/sh
# refresh.sh — Full pipeline: scrape all sources, then convert to markdown.
# Only operates on sources defined in sources.json. Drop-in directories
# under corpus/ that are not listed in sources.json are left untouched.
# Usage: scripts/refresh.sh [--source NAME]

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [ "$1" = "--source" ] && [ -n "$2" ]; then
    echo "Refreshing source: $2"
    echo ""
    echo "=== Scraping ==="
    python3 -m scraper --source "$2"
    echo ""
    echo "=== Converting ==="
    python3 -m converter --source "$2"
else
    echo "Refreshing all sources (from sources.json)"
    echo ""
    echo "=== Scraping ==="
    python3 -m scraper
    echo ""
    echo "=== Converting ==="
    python3 -m converter
fi

echo ""
echo "Done. Corpus updated."
echo "Run 'scripts/setup_qmd.sh' to reindex for search."
