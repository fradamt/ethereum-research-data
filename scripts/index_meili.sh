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
#   - MEILI_MASTER_KEY env var set (must match the key Meilisearch was started with)
#
# Config: config/indexer.toml
# Data:   data/graph.db, data/index_state.db (gitignored, rebuildable)
set -euo pipefail

# ── Preflight checks ────────────────────────────────────────────────

if ! command -v uv &>/dev/null; then
    echo "[index_meili] ERROR: uv is not installed. Install it from https://docs.astral.sh/uv/" >&2
    exit 1
fi

if [ -z "${MEILI_MASTER_KEY:-}" ]; then
    echo "[index_meili] ERROR: MEILI_MASTER_KEY is not set." >&2
    echo "  Export the key that Meilisearch was started with, e.g.:" >&2
    echo "    export MEILI_MASTER_KEY='your-key-here'" >&2
    exit 1
fi

MEILI_URL="${ERD_MEILI_URL:-http://localhost:7700}"
if ! curl -sf "${MEILI_URL}/health" >/dev/null 2>&1; then
    echo "[index_meili] ERROR: Meilisearch is not reachable at ${MEILI_URL}" >&2
    echo "  Start it with:  meilisearch --master-key \"\$MEILI_MASTER_KEY\"" >&2
    exit 1
fi

# ── Setup ────────────────────────────────────────────────────────────

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

if [ -z "$(ls -A corpus/ 2>/dev/null)" ]; then
    echo "[index_meili] WARNING: corpus/ is empty — there may be nothing to index."
fi

# Ensure data directory exists
mkdir -p data

# Initialize databases if first run (or if either DB is missing)
if [ ! -f data/index_state.db ] || [ ! -f data/graph.db ]; then
    echo "[index_meili] First run — initializing databases..."
    uv run erd-index init
fi

echo "[index_meili] Starting sync..."
uv run erd-index sync "$@"

echo "[index_meili] Showing stats..."
uv run erd-index stats

echo "[index_meili] Done."
