#!/bin/bash
# Install the erd-search skill globally for Claude Code.
#
# This makes the skill available from any project directory,
# not just when working inside this repo.
#
# Usage:
#   ./scripts/install_skill.sh          # symlink (updates automatically)
#   ./scripts/install_skill.sh --copy   # copy (independent snapshot)
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$REPO/skills/erd-search"
TARGET="$HOME/.claude/skills/erd-search"

if [ ! -d "$SOURCE" ]; then
    echo "ERROR: Skill not found at $SOURCE" >&2
    exit 1
fi

mkdir -p "$HOME/.claude/skills"

if [ "${1:-}" = "--copy" ]; then
    rm -rf "$TARGET"
    cp -r "$SOURCE" "$TARGET"
    echo "Copied skill to $TARGET"
else
    if [ -L "$TARGET" ]; then
        rm "$TARGET"
    elif [ -d "$TARGET" ]; then
        echo "WARNING: $TARGET already exists (not a symlink). Use --copy to overwrite." >&2
        exit 1
    fi
    ln -s "$SOURCE" "$TARGET"
    echo "Symlinked $TARGET -> $SOURCE"
fi

echo "Done. The erd-search skill is now available globally in Claude Code."
