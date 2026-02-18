#!/bin/bash
# Convenience wrapper for Meilisearch indexing.
#
# Usage:
#   ./scripts/index_meili.sh                  # incremental sync (changed files only)
#   ./scripts/index_meili.sh --full-rebuild   # reprocess everything
#   ./scripts/index_meili.sh --dry-run        # parse and chunk without writing
#   ./scripts/index_meili.sh -v               # verbose output
#
# Prerequisites:
#   - Meilisearch running at http://localhost:7700 (or set ERD_MEILI_URL)
#   - MEILI_MASTER_KEY env var set (e.g. export MEILI_MASTER_KEY=erd-dev-key)
#
# Config: config/indexer.toml
# Data:   data/graph.db, data/index_state.db (gitignored, rebuildable)
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

# Ensure data directory exists
mkdir -p data

# Initialize databases if first run
if [ ! -f data/index_state.db ]; then
    echo "[index_meili] First run — initializing databases..."
    uv run erd-index init
fi

echo "[index_meili] Starting sync..."
uv run erd-index sync "$@"

echo "[index_meili] Showing stats..."
uv run erd-index stats

echo "[index_meili] Done."
