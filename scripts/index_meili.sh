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

if ! command -v erd-index &>/dev/null || ! command -v eth-search &>/dev/null; then
    echo "[index_meili] ERROR: erd-index/eth-search not found." >&2
    echo "  Install with: uv tool install -e /path/to/ethereum-research-data" >&2
    exit 1
fi

if [ -z "${MEILI_MASTER_KEY:-}" ]; then
    echo "[index_meili] ERROR: MEILI_MASTER_KEY is not set." >&2
    echo "  Export the key that Meilisearch was started with, e.g.:" >&2
    echo "    export MEILI_MASTER_KEY='your-key-here'" >&2
    exit 1
fi

MEILI_URL="${ERD_MEILI_URL:-http://localhost:7700}"
# Wait up to 30s for Meilisearch to become reachable (handles Docker startup delay)
for i in $(seq 1 6); do
    if curl -sf "${MEILI_URL}/health" >/dev/null 2>&1; then
        break
    fi
    if [ "$i" -eq 6 ]; then
        echo "[index_meili] ERROR: Meilisearch is not reachable at ${MEILI_URL}" >&2
        echo "  Start it with:  meilisearch --master-key \"\$MEILI_MASTER_KEY\"" >&2
        echo "  Or: docker compose up -d" >&2
        exit 1
    fi
    echo "[index_meili] Waiting for Meilisearch to start... (${i}/6)"
    sleep 5
done

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
    erd-index init
fi

echo "[index_meili] Starting sync..."
erd-index sync "$@"

# Apply Ethereum terminology (synonyms) — idempotent, fast, ensures
# search quality for abbreviations like SSZ, KZG, DAS, PBS, etc.
echo "[index_meili] Applying terminology..."
eth-search --key "$MEILI_MASTER_KEY" apply-terminology

echo "[index_meili] Showing stats..."
erd-index stats

echo "[index_meili] Done."
