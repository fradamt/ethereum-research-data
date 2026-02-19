#!/usr/bin/env python3
"""Backfill text_length field on existing Meilisearch documents.

Fetches documents in pages, computes len(text) for each, and sends
partial updates with the new text_length field.  Also re-applies index
settings to register text_length as filterable.

Usage::

    uv run python scripts/backfill_text_length.py            # run backfill
    uv run python scripts/backfill_text_length.py --dry-run   # preview only
    uv run python scripts/backfill_text_length.py --settings-only  # apply settings only
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request

MEILI_URL = "http://localhost:7700"
INDEX = "eth_chunks_v1"
ADMIN_KEY = ""
BATCH_SIZE = 1000


def _read_key() -> str:
    import os
    env = os.environ.get("ERD_ADMIN_KEY") or os.environ.get("MEILI_MASTER_KEY")
    if env:
        return env
    try:
        with open(os.path.expanduser("~/.config/erd/admin-key")) as f:
            return f.read().strip()
    except OSError:
        return "erd-dev-key"


def _request(url: str, *, method: str = "GET", payload: dict | list | None = None) -> dict | list:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {ADMIN_KEY}"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())


def _wait_task(task_uid: int) -> None:
    for _ in range(300):
        info = _request(f"{MEILI_URL}/tasks/{task_uid}")
        if info["status"] == "succeeded":
            return
        if info["status"] == "failed":
            raise RuntimeError(f"Task {task_uid} failed: {info.get('error', {}).get('message')}")
        time.sleep(1.0)
    raise TimeoutError(f"Task {task_uid} timed out")


def apply_settings() -> None:
    """Re-apply index settings to register text_length as filterable."""
    from erd_index.index.meili_schema import get_index_settings

    settings = get_index_settings()
    print(f"Applying settings (text_length in filterableAttributes: {'text_length' in settings['filterableAttributes']})")
    data = json.dumps(settings).encode()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {ADMIN_KEY}"}
    req = urllib.request.Request(f"{MEILI_URL}/indexes/{INDEX}/settings", data=data, headers=headers, method="PATCH")
    resp = urllib.request.urlopen(req, timeout=30)
    task_info = json.loads(resp.read())
    task_uid = task_info.get("taskUid")
    if task_uid:
        print(f"  Waiting for settings task {task_uid}...")
        _wait_task(task_uid)
    print("  Settings applied.")


def backfill(*, dry_run: bool = False) -> None:
    """Fetch all docs, compute text_length, send partial updates."""
    # Get total count
    stats = _request(f"{MEILI_URL}/indexes/{INDEX}/stats")
    total = stats["numberOfDocuments"]
    print(f"Total documents: {total}")

    # Check how many already have text_length
    field_dist = stats.get("fieldDistribution", {})
    existing = field_dist.get("text_length", 0)
    if existing == total:
        print(f"All {total} documents already have text_length. Nothing to do.")
        return
    print(f"Documents with text_length: {existing}/{total}")

    offset = 0
    updated = 0

    while offset < total:
        # Fetch a batch
        result = _request(
            f"{MEILI_URL}/indexes/{INDEX}/documents/fetch",
            method="POST",
            payload={
                "fields": ["id", "text"],
                "limit": BATCH_SIZE,
                "offset": offset,
            },
        )
        docs = result.get("results", [])
        if not docs:
            break

        # Build partial updates
        updates = []
        for doc in docs:
            text = doc.get("text", "")
            updates.append({"id": doc["id"], "text_length": len(text)})

        if dry_run:
            print(f"  [dry-run] Would update {len(updates)} docs (offset {offset})")
        else:
            resp = _request(
                f"{MEILI_URL}/indexes/{INDEX}/documents",
                method="PUT",
                payload=updates,
            )
            task_uid = resp.get("taskUid")
            if task_uid:
                _wait_task(task_uid)
            updated += len(updates)
            print(f"  Updated {updated}/{total} (offset {offset})")

        offset += BATCH_SIZE

    if not dry_run:
        print(f"Backfill complete: {updated} documents updated.")


def main() -> None:
    global ADMIN_KEY
    ADMIN_KEY = _read_key()

    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    settings_only = "--settings-only" in args

    apply_settings()
    if not settings_only:
        backfill(dry_run=dry_run)


if __name__ == "__main__":
    main()
