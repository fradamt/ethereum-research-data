#!/bin/sh
# refresh.sh — Full pipeline: scrape all sources, then convert to markdown.
# Only operates on sources defined in sources.json. Drop-in directories
# under corpus/ that are not listed in sources.json are left untouched.
# Usage: scripts/refresh.sh [--source NAME]

set -e

python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" 2>/dev/null \
  || { echo "Error: Python 3.10+ is required"; exit 1; }

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
echo "Run './scripts/index_meili.sh' to update the Meilisearch search index."
echo "Run 'scripts/setup_qmd.sh' to update QMD collections (if using QMD)."
