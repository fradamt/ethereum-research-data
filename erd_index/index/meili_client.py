"""Meilisearch connection management and index lifecycle."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import meilisearch
from meilisearch.errors import MeilisearchApiError, MeilisearchCommunicationError

from erd_index.index.meili_schema import SCHEMA_VERSION, get_index_settings

if TYPE_CHECKING:
    from erd_index.settings import Settings

__all__ = ["ensure_index", "get_client", "init_index"]

log = logging.getLogger(__name__)

# Metadata key stored on the index to track which schema version was applied.
_SCHEMA_VERSION_KEY = "_erd_schema_version"

# Cached client instance — avoids re-creating and health-checking per batch.
# Not thread-safe; acceptable for the single-threaded CLI pipeline.
_cached_client: meilisearch.Client | None = None
_cached_url: str | None = None


def get_client(settings: Settings) -> meilisearch.Client:
    """Return a (cached) Meilisearch client from settings.

    The client is cached for the lifetime of the process. A health check
    runs only on the first call (or when the URL changes).

    Raises a clear error if Meilisearch is unreachable.
    """
    global _cached_client, _cached_url
    if _cached_client is not None and _cached_url == settings.meili.url:
        return _cached_client
    try:
        client = meilisearch.Client(settings.meili.url, settings.meili.master_key or None)
        # Quick health check so callers get a clear error immediately.
        client.health()
        _cached_client = client
        _cached_url = settings.meili.url
        return client
    except MeilisearchCommunicationError as exc:
        raise ConnectionError(
            f"Cannot reach Meilisearch at {settings.meili.url}. "
            "Is the server running?  Start it with: meilisearch --master-key <key>"
        ) from exc


def init_index(settings: Settings) -> meilisearch.Client:
    """Create the index if it does not exist, apply settings, and set up the alias.

    Returns the connected client.
    """
    client = get_client(settings)
    index_name = settings.meili.index_name
    alias_name = settings.meili.index_alias

    # Create index (idempotent — Meilisearch returns the existing UID if present).
    task = client.create_index(index_name, {"primaryKey": "id"})
    client.wait_for_task(task.task_uid, timeout_in_ms=30_000)
    log.info("Index '%s' ready", index_name)

    # Apply full settings.
    _apply_settings(client, index_name)

    # Point the alias at this index for zero-downtime reindex swaps.
    _update_alias(client, alias_name, index_name)

    return client


def ensure_index(settings: Settings) -> meilisearch.Client:
    """Idempotent index setup: create if missing, update settings if schema version changed.

    Returns the connected client.
    """
    client = get_client(settings)
    index_name = settings.meili.index_name

    # Check whether the index exists.
    try:
        client.get_index(index_name)
    except MeilisearchApiError as exc:
        if exc.code == "index_not_found":
            log.info("Index '%s' not found — creating", index_name)
            return init_index(settings)
        raise

    # Index exists.  Check schema version stored in its settings/metadata.
    current_version = _get_stored_schema_version(client, index_name)
    if current_version < SCHEMA_VERSION:
        log.info(
            "Schema version %d -> %d — re-applying settings on '%s'",
            current_version,
            SCHEMA_VERSION,
            index_name,
        )
        _apply_settings(client, index_name)
    else:
        log.debug("Index '%s' schema version %d is current", index_name, current_version)

    # Note: alias swap is only done during init_index(), not here.
    # Swapping on every ensure_index() call caused data splits when
    # sync() called ensure_index() for both md and code ingestion.
    return client


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _apply_settings(client: meilisearch.Client, index_name: str) -> None:
    """Push the canonical index settings to Meilisearch and wait for completion."""
    index = client.index(index_name)
    idx_settings = get_index_settings()
    task = index.update_settings(idx_settings)
    client.wait_for_task(task.task_uid, timeout_in_ms=60_000)
    log.info("Applied index settings (schema v%d) to '%s'", SCHEMA_VERSION, index_name)


def _update_alias(client: meilisearch.Client, alias_name: str, index_name: str) -> None:
    """Point *alias_name* at *index_name* via the swap-indexes API.

    Meilisearch 1.x uses index swaps for alias-like behaviour.  If the alias
    index doesn't exist yet we create it and swap, otherwise we only swap if
    the alias is pointing at a different UID.
    """
    # If alias and index are the same name, nothing to do.
    if alias_name == index_name:
        return

    try:
        alias_index = client.get_index(alias_name)
        if alias_index.uid == index_name:
            return  # already correct
    except MeilisearchApiError as exc:
        if exc.code == "index_not_found":
            # Create the alias index so we can swap into it.
            task = client.create_index(alias_name, {"primaryKey": "id"})
            client.wait_for_task(task.task_uid, timeout_in_ms=30_000)
        else:
            raise

    task = client.swap_indexes([{"indexes": [alias_name, index_name]}])
    client.wait_for_task(task.task_uid, timeout_in_ms=30_000)
    log.info("Alias '%s' now points to '%s'", alias_name, index_name)


def _get_stored_schema_version(client: meilisearch.Client, index_name: str) -> int:
    """Read the schema version from an existing document sentinel, or return 0."""
    index = client.index(index_name)
    try:
        stats = index.get_stats()
        if stats.number_of_documents == 0:
            return 0
        # Sample a document to check its schema_version field.
        result = index.search("", {"limit": 1, "attributesToRetrieve": ["schema_version"]})
        hits = result.get("hits", [])
        if hits:
            return int(hits[0].get("schema_version", 0))
    except (MeilisearchApiError, MeilisearchCommunicationError):
        pass
    return 0
