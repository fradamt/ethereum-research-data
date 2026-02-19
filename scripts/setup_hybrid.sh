#!/bin/bash
# setup_hybrid.sh — Set up hybrid (semantic) search.
#
# Pulls the embedding model, batch-embeds all documents via Ollama,
# then switches the embedder to REST mode for query-time embedding.
#
# Usage:
#   ./scripts/setup_hybrid.sh                   # default setup
#   ./scripts/setup_hybrid.sh --docker           # Meilisearch + Ollama in Docker
#   ./scripts/setup_hybrid.sh --model MODEL      # use a different embedding model
#   ./scripts/setup_hybrid.sh --resume           # resume interrupted embedding
#
# Prerequisites:
#   - Meilisearch running (localhost:7700 or ERD_MEILI_URL)
#   - Ollama running (localhost:11434 or ERD_BATCH_OLLAMA_URL)
#   - MEILI_MASTER_KEY set
#   - Index populated (run ./scripts/index_meili.sh first)
set -euo pipefail

# ── Parse flags ────────────────────────────────────────────────────
DOCKER_MODE=false
RESUME=""
MODEL="${ERD_BATCH_MODEL:-embeddinggemma:300m}"
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --docker)
            DOCKER_MODE=true
            shift
            ;;
        --resume)
            RESUME="--resume"
            shift
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        *)
            EXTRA_ARGS+=("$1")
            shift
            ;;
    esac
done

# ── Preflight checks ──────────────────────────────────────────────

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

if ! command -v uv &>/dev/null; then
    echo "[setup_hybrid] ERROR: uv is not installed." >&2
    exit 1
fi

if [ -z "${MEILI_MASTER_KEY:-}" ]; then
    echo "[setup_hybrid] ERROR: MEILI_MASTER_KEY is not set." >&2
    exit 1
fi

MEILI_URL="${ERD_MEILI_URL:-http://localhost:7700}"
for i in $(seq 1 6); do
    if curl -sf "${MEILI_URL}/health" >/dev/null 2>&1; then break; fi
    if [ "$i" -eq 6 ]; then
        echo "[setup_hybrid] ERROR: Meilisearch is not reachable at ${MEILI_URL}" >&2
        exit 1
    fi
    echo "[setup_hybrid] Waiting for Meilisearch... (${i}/6)"
    sleep 5
done

OLLAMA_URL="${ERD_BATCH_OLLAMA_URL:-http://localhost:11434/api/embed}"
OLLAMA_BASE="${OLLAMA_URL%/api/embed}"
for i in $(seq 1 6); do
    if curl -sf "${OLLAMA_BASE}/" >/dev/null 2>&1; then break; fi
    if [ "$i" -eq 6 ]; then
        echo "[setup_hybrid] ERROR: Ollama is not reachable at ${OLLAMA_BASE}" >&2
        echo "  Start Ollama or set ERD_BATCH_OLLAMA_URL" >&2
        exit 1
    fi
    echo "[setup_hybrid] Waiting for Ollama... (${i}/6)"
    sleep 5
done

# ── Pull the embedding model ──────────────────────────────────────

echo "[setup_hybrid] Pulling embedding model: ${MODEL}"
if command -v ollama &>/dev/null; then
    ollama pull "$MODEL"
elif $DOCKER_MODE; then
    docker compose exec ollama ollama pull "$MODEL"
else
    echo "[setup_hybrid] WARNING: ollama CLI not found; assuming model is already pulled" >&2
fi

# ── Determine embedder URL (Docker vs host) ───────────────────────

if $DOCKER_MODE; then
    # In Docker, Meilisearch reaches Ollama via the Docker service name
    EMBEDDER_URL="http://ollama:11434/api/embed"
    echo "[setup_hybrid] Docker mode: Meilisearch will reach Ollama at ${EMBEDDER_URL}"
else
    EMBEDDER_URL="$OLLAMA_URL"
fi

# ── Batch embed + finalize ────────────────────────────────────────

echo "[setup_hybrid] Starting batch embedding..."
uv run python scripts/batch_embed.py \
    --setup --finalize --asymmetric \
    --model "$MODEL" \
    --embedder-url "$EMBEDDER_URL" \
    $RESUME \
    "${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}"

echo ""
echo "[setup_hybrid] Done! Hybrid search is ready."
echo "  Try: erd-search query 'how does inactivity leak work' --hybrid"
