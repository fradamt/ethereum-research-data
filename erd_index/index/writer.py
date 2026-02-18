"""Batch upsert and delete operations against Meilisearch."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import orjson
from meilisearch.errors import MeilisearchApiError, MeilisearchCommunicationError

from erd_index.index.meili_client import get_client

if TYPE_CHECKING:
    from erd_index.settings import Settings

__all__ = ["batch_upsert", "delete_by_filter", "delete_by_ids", "get_index_stats"]

log = logging.getLogger(__name__)


def batch_upsert(settings: Settings, documents: list[dict]) -> int:
    """Upsert *documents* into Meilisearch in batches.

    Returns the total number of documents submitted.  Raises on any task
    failure so callers can avoid committing stale manifest state.
    """
    if not documents:
        return 0

    client = get_client(settings)
    index = client.index(settings.meili.index_name)
    batch_size = settings.meili.batch_size
    submitted = 0

    for start in range(0, len(documents), batch_size):
        batch = documents[start : start + batch_size]
        payload = orjson.dumps(batch)
        task = index.add_documents_json(payload)
        _wait_and_check(client, task.task_uid, f"upsert batch [{start}:{start + len(batch)}]")
        submitted += len(batch)
        log.info("Upserted %d / %d documents", submitted, len(documents))

    return submitted


def delete_by_ids(settings: Settings, chunk_ids: list[str]) -> int:
    """Delete documents by their chunk IDs.

    Returns the number of IDs submitted for deletion.
    """
    if not chunk_ids:
        return 0

    client = get_client(settings)
    index = client.index(settings.meili.index_name)
    batch_size = settings.meili.batch_size
    deleted = 0

    for start in range(0, len(chunk_ids), batch_size):
        batch = chunk_ids[start : start + batch_size]
        task = index.delete_documents(ids=batch)
        _wait_and_check(client, task.task_uid, f"delete IDs [{start}:{start + len(batch)}]")
        deleted += len(batch)

    log.info("Deleted %d document(s) by ID", deleted)
    return deleted


def delete_by_filter(settings: Settings, filter_str: str) -> None:
    """Delete documents matching a Meilisearch filter expression.

    Example filter_str: ``"source_name = 'ethresearch' AND doc_id = 'forum:ethresearch:1000'"``
    """
    client = get_client(settings)
    index = client.index(settings.meili.index_name)
    task = index.delete_documents(filter=filter_str)
    _wait_and_check(client, task.task_uid, f"delete by filter: {filter_str}")
    log.info("Deleted documents matching filter: %s", filter_str)


def get_index_stats(settings: Settings) -> dict:
    """Return document count, index size, field distribution, etc."""
    try:
        client = get_client(settings)
        index = client.index(settings.meili.index_name)
        raw = index.get_stats()
        # The SDK returns a typed object with snake_case attributes.
        # Normalize to a plain dict with camelCase keys for compatibility.
        return {
            "numberOfDocuments": getattr(raw, "number_of_documents", 0),
            "isIndexing": getattr(raw, "is_indexing", False),
            "fieldDistribution": dict(getattr(raw, "field_distribution", {}) or {}),
        }
    except (MeilisearchCommunicationError, MeilisearchApiError, ConnectionError) as exc:
        return {"error": str(exc)}


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------


def _wait_and_check(client, task_uid: int, description: str) -> None:
    """Wait for a Meilisearch task to complete and raise on failure."""
    result = client.wait_for_task(task_uid, timeout_in_ms=120_000)
    status = result.get("status") if isinstance(result, dict) else getattr(result, "status", None)
    if status == "failed":
        error = result.get("error") if isinstance(result, dict) else getattr(result, "error", None)
        raise RuntimeError(f"Meilisearch task failed ({description}): {error}")
