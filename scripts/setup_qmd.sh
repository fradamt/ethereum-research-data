#!/bin/sh
# setup_qmd.sh — Create/update QMD collections for each corpus subdirectory.
# Auto-discovers all subdirectories under corpus/ that contain .md files.
# Idempotent: safe to re-run.

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

CORPUS_DIR="$REPO_ROOT/corpus"

# Check for qmd
if ! command -v qmd >/dev/null 2>&1; then
    echo "Error: qmd is not installed."
    echo "Install it from: https://github.com/tobi/qmd"
    exit 1
fi

if [ ! -d "$CORPUS_DIR" ]; then
    echo "Error: corpus/ directory not found in $REPO_ROOT"
    exit 1
fi

echo "Setting up QMD collections..."
echo ""

# Auto-discover all subdirectories under corpus/ that contain .md files
count=0
for dir in "$CORPUS_DIR"/*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"

    # Skip directories with no .md files
    md_count=$(find "$dir" -maxdepth 1 -name '*.md' -print -quit 2>/dev/null | wc -l)
    if [ "$md_count" -eq 0 ]; then
        echo "  Skipping $name — no .md files"
        continue
    fi

    # Remove existing collection (idempotent), then add fresh
    qmd collection remove --name "$name" 2>/dev/null || true
    qmd collection add "$dir" --name "$name" --mask "**/*.md"
    echo "  Added collection: $name -> $dir"
    count=$((count + 1))
done

if [ "$count" -eq 0 ]; then
    echo "  No collections found (no corpus/ subdirectories with .md files)"
    exit 0
fi

echo ""
echo "Embedding all collections..."
qmd embed

echo ""
echo "QMD setup complete ($count collections). Try: qmd search 'proposer boost'"
