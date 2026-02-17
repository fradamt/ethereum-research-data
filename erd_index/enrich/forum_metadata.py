"""Extract forum-specific metadata from frontmatter into a Chunk.

Populates fields like topic_id, author, category, views, likes,
influence_score, and url from the YAML frontmatter dict that the
parse/chunk stages extracted from forum posts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from erd_index.models import Chunk

__all__ = ["enrich_forum_chunk"]


def _int_or(value: object, default: int = 0) -> int:
    """Coerce *value* to int, returning *default* on failure."""
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _influence_score(likes: int, views: int, posts_count: int) -> float:
    """Simple engagement heuristic (un-normalized)."""
    return likes * 2.0 + views * 0.01 + posts_count * 0.5


def enrich_forum_chunk(chunk: Chunk, frontmatter: dict[str, Any] | None = None) -> Chunk:
    """Populate forum-specific fields on *chunk* from *frontmatter*.

    If *frontmatter* is ``None``, computes ``influence_score`` from whatever
    values are already set on the chunk. Mutates and returns *chunk*.
    """
    fm = frontmatter or {}

    if fm:
        chunk.topic_id = _int_or(fm.get("topic_id"), 0) or chunk.topic_id
        chunk.post_number = _int_or(fm.get("post_number"), 0) or chunk.post_number
        chunk.author = str(fm.get("author", "")) or chunk.author
        chunk.category = str(fm.get("category", "")) or chunk.category
        chunk.views = _int_or(fm.get("views"))
        chunk.likes = _int_or(fm.get("likes"))
        chunk.posts_count = _int_or(fm.get("posts_count"))
        chunk.research_thread = str(fm.get("research_thread", "")) or chunk.research_thread
        chunk.url = str(fm.get("url", "")) or chunk.url

        # Derive source_date from frontmatter if present
        if fm.get("date") and not chunk.source_date:
            chunk.source_date = str(fm["date"])

    chunk.influence_score = _influence_score(chunk.likes, chunk.views, chunk.posts_count)

    return chunk
