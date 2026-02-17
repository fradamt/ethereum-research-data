"""Pipeline orchestration — ties together discover, parse, chunk, enrich, index, graph.

Each public function is called by cli.py.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from erd_index.chunk import chunk_parsed_units
from erd_index.chunk.code_chunker import chunk_code_units
from erd_index.discover import DiscoveredFile, walk_sources
from erd_index.enrich.code_metadata import enrich_code_chunk
from erd_index.enrich.dependency_extractor import extract_dependencies
from erd_index.enrich.eip_refs import extract_eip_refs
from erd_index.enrich.forum_metadata import enrich_forum_chunk
from erd_index.graph.edge_builder import build_edges_from_chunk
from erd_index.graph.node_builder import chunk_to_node
from erd_index.graph.store import (
    get_connection,
    init_graph_db,
    upsert_code_dep,
    upsert_cross_ref,
    upsert_eip_dep,
    upsert_node,
)
from erd_index.index.document_builder import chunk_to_document, sanitize_chunk_id
from erd_index.index.meili_client import ensure_index
from erd_index.index.writer import batch_upsert, delete_by_ids, get_index_stats
from erd_index.models import Chunk, SourceKind
from erd_index.parse import parse_markdown
from erd_index.parse.go_parser import parse_go_file
from erd_index.parse.py_parser import parse_python_file
from erd_index.parse.rust_parser import parse_rust_file
from erd_index.state.manifest_db import (
    compute_file_hash,
    get_indexed_file,
    get_stale_files,
    init_state_db,
    is_file_changed,
    remove_indexed_file,
    upsert_indexed_file,
)
from erd_index.state.run_log import finish_run, get_recent_runs, start_run

if TYPE_CHECKING:
    from erd_index.settings import Settings

log = logging.getLogger(__name__)

# Language string -> parser function mapping
_CODE_PARSERS = {
    "python": parse_python_file,
    "go": parse_go_file,
    "rust": parse_rust_file,
}


# ---------------------------------------------------------------------------
# Markdown ingestion
# ---------------------------------------------------------------------------


def ingest_markdown(
    settings: Settings,
    *,
    changed_only: bool = False,
    source_name: str | None = None,
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    """Ingest markdown files from corpus sources."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # 1. Init state DB
    state_db = init_state_db(settings)

    # 2. Ensure Meilisearch index exists (skip if dry_run)
    if not dry_run:
        ensure_index(settings)

    # 3. Start run log
    run_id = start_run(state_db, "ingest-md")

    # 4. Walk corpus sources (markdown only)
    files = _discover_markdown_files(settings, source_name=source_name)
    log.info("Discovered %d markdown file(s)", len(files))

    # Track current paths per source for stale detection
    paths_by_source: dict[str, set[str]] = {}
    for f in files:
        paths_by_source.setdefault(f.source_name, set()).add(f.relative_path)

    files_processed = 0
    files_skipped = 0
    total_chunks_upserted = 0
    errors = 0
    error_details: list[str] = []

    # 5. Process each file
    for discovered in files:
        # 5a. Skip unchanged files
        if changed_only and not is_file_changed(
            state_db,
            repository=discovered.repository or discovered.source_name,
            file_path=discovered.relative_path,
            size_bytes=discovered.size_bytes,
            mtime_ns=discovered.mtime_ns,
            parser_version=settings.parser_version,
            chunker_version=settings.chunker_version,
        ):
            files_skipped += 1
            continue

        try:
            chunks, chunk_ids = _process_markdown_file(discovered, settings)
            repo_key = discovered.repository or discovered.source_name

            if not dry_run and chunks:
                # Build Meilisearch documents
                documents = [
                    chunk_to_document(c, settings.schema_version) for c in chunks
                ]
                batch_upsert(settings, documents)
                total_chunks_upserted += len(documents)

                # Delete stale chunks from previous indexing of this file
                stale = _stale_chunk_ids(
                    state_db, repo_key, discovered.relative_path, chunk_ids,
                )
                if stale:
                    delete_by_ids(settings, stale)
                    log.debug("Deleted %d stale chunks for %s", len(stale), discovered.relative_path)

            if not dry_run:
                file_hash = compute_file_hash(discovered.absolute_path)
                upsert_indexed_file(
                    state_db,
                    repository=repo_key,
                    file_path=discovered.relative_path,
                    source_name=discovered.source_name,
                    language=discovered.language,
                    size_bytes=discovered.size_bytes,
                    mtime_ns=discovered.mtime_ns,
                    file_hash=file_hash,
                    parser_version=settings.parser_version,
                    chunker_version=settings.chunker_version,
                    chunk_ids_json=json.dumps(chunk_ids),
                )
            files_processed += 1

        except Exception:
            errors += 1
            msg = f"{discovered.source_name}:{discovered.relative_path}"
            error_details.append(msg)
            log.exception("Error processing %s", msg)

    # 6. Clean up stale files
    chunks_deleted = 0
    if not dry_run:
        chunks_deleted = _cleanup_stale_markdown(settings, state_db, paths_by_source)

    # 7. Finish run log
    finish_run(
        state_db,
        run_id,
        files_processed=files_processed,
        files_skipped=files_skipped,
        chunks_upserted=total_chunks_upserted,
        chunks_deleted=chunks_deleted,
        errors=errors,
        error_details=error_details or None,
    )

    log.info(
        "ingest-md complete: %d processed, %d skipped, %d chunks upserted, "
        "%d chunks deleted, %d errors",
        files_processed,
        files_skipped,
        total_chunks_upserted,
        chunks_deleted,
        errors,
    )


def _discover_markdown_files(
    settings: Settings,
    *,
    source_name: str | None = None,
) -> list[DiscoveredFile]:
    """Walk sources and filter to markdown corpus files only."""
    files: list[DiscoveredFile] = []
    for f in walk_sources(settings):
        # Only corpus sources (no code repos — those have repository set)
        if f.repository:
            continue
        if f.language != "markdown":
            continue
        if source_name and f.source_name != source_name:
            continue
        files.append(f)
    return files


def _process_markdown_file(
    discovered: DiscoveredFile,
    settings: Settings,
) -> tuple[list[Chunk], list[str]]:
    """Parse, chunk, and enrich a single markdown file.

    Returns (chunks, chunk_ids).
    """
    text = discovered.absolute_path.read_text(encoding="utf-8", errors="replace")

    # Parse
    units = parse_markdown(
        text,
        path=discovered.relative_path,
        source_name=discovered.source_name,
        repository=discovered.repository,
    )

    # Chunk
    chunks = chunk_parsed_units(units, settings.chunk_sizing)

    # Enrich: EIP refs + forum metadata
    for chunk in chunks:
        eip_refs = extract_eip_refs(chunk.text)
        if eip_refs:
            chunk.mentions_eips = eip_refs

        if chunk.source_kind == SourceKind.FORUM:
            # Forum metadata is already set from frontmatter by the chunker,
            # but enrich_forum_chunk computes influence_score.
            enrich_forum_chunk(chunk)

    chunk_ids = [sanitize_chunk_id(c.chunk_id) for c in chunks]
    return chunks, chunk_ids


def _stale_chunk_ids(
    state_db: Path,
    repository: str,
    file_path: str,
    new_chunk_ids: list[str],
) -> list[str]:
    """Return chunk IDs that were in the previous manifest entry but not in *new_chunk_ids*.

    Both old and new IDs are expected to be sanitized Meilisearch IDs.
    """
    old_entry = get_indexed_file(state_db, repository, file_path)
    if old_entry is None:
        return []
    old_ids = set(json.loads(old_entry.get("chunk_ids_json", "[]")))
    return sorted(old_ids - set(new_chunk_ids))


def _cleanup_stale_markdown(
    settings: Settings,
    state_db: Path,
    paths_by_source: dict[str, set[str]],
) -> int:
    """Delete stale chunks for files that no longer exist on disk.

    Returns the total number of chunk IDs deleted.
    """
    total_deleted = 0
    for src_name, current_paths in paths_by_source.items():
        stale_rows = get_stale_files(state_db, src_name, current_paths)
        for row in stale_rows:
            chunk_ids = json.loads(row.get("chunk_ids_json", "[]"))
            if chunk_ids:
                delete_by_ids(settings, chunk_ids)
                total_deleted += len(chunk_ids)
            remove_indexed_file(state_db, row["repository"], row["file_path"])
            log.info("Removed stale file: %s:%s", row["repository"], row["file_path"])
    return total_deleted


# ---------------------------------------------------------------------------
# Code ingestion
# ---------------------------------------------------------------------------


def ingest_code(
    settings: Settings,
    *,
    repo_name: str | None = None,
    changed_only: bool = False,
    dry_run: bool = False,
    max_files: int = 0,
    verbose: bool = False,
) -> None:
    """Ingest code files from configured repos."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # 1. Init state DB
    state_db = init_state_db(settings)

    # 2. Ensure Meilisearch index exists (skip if dry_run)
    if not dry_run:
        ensure_index(settings)

    # 3. Start run log
    run_id = start_run(state_db, "ingest-code")

    # 4. Walk sources — filter to code repos only
    files = _discover_code_files(settings, repo_name=repo_name)
    log.info("Discovered %d code file(s)", len(files))

    if max_files > 0:
        files = files[:max_files]

    # Track current paths per repo for stale detection
    paths_by_repo: dict[str, set[str]] = {}
    for f in files:
        paths_by_repo.setdefault(f.repository, set()).add(f.relative_path)

    files_processed = 0
    files_skipped = 0
    total_chunks_upserted = 0
    errors = 0
    error_details: list[str] = []

    # 5. Process each file
    for discovered in files:
        # 5a. Skip unchanged files
        if changed_only and not is_file_changed(
            state_db,
            repository=discovered.repository,
            file_path=discovered.relative_path,
            size_bytes=discovered.size_bytes,
            mtime_ns=discovered.mtime_ns,
            parser_version=settings.parser_version,
            chunker_version=settings.chunker_version,
        ):
            files_skipped += 1
            continue

        try:
            chunks, chunk_ids = _process_code_file(discovered, settings)

            if not dry_run and chunks:
                documents = [
                    chunk_to_document(c, settings.schema_version) for c in chunks
                ]
                batch_upsert(settings, documents)
                total_chunks_upserted += len(documents)

                # Delete stale chunks from previous indexing of this file
                stale = _stale_chunk_ids(
                    state_db, discovered.repository, discovered.relative_path, chunk_ids,
                )
                if stale:
                    delete_by_ids(settings, stale)
                    log.debug("Deleted %d stale chunks for %s", len(stale), discovered.relative_path)

            if not dry_run:
                file_hash = compute_file_hash(discovered.absolute_path)
                upsert_indexed_file(
                    state_db,
                    repository=discovered.repository,
                    file_path=discovered.relative_path,
                    source_name=discovered.source_name,
                    language=discovered.language,
                    size_bytes=discovered.size_bytes,
                    mtime_ns=discovered.mtime_ns,
                    file_hash=file_hash,
                    parser_version=settings.parser_version,
                    chunker_version=settings.chunker_version,
                    chunk_ids_json=json.dumps(chunk_ids),
                )
            files_processed += 1

        except Exception:
            errors += 1
            msg = f"{discovered.source_name}:{discovered.relative_path}"
            error_details.append(msg)
            log.exception("Error processing %s", msg)

    # 6. Clean up stale files
    chunks_deleted = 0
    if not dry_run:
        chunks_deleted = _cleanup_stale_code(settings, state_db, paths_by_repo)

    # 7. Finish run log
    finish_run(
        state_db,
        run_id,
        files_processed=files_processed,
        files_skipped=files_skipped,
        chunks_upserted=total_chunks_upserted,
        chunks_deleted=chunks_deleted,
        errors=errors,
        error_details=error_details or None,
    )

    log.info(
        "ingest-code complete: %d processed, %d skipped, %d chunks upserted, "
        "%d chunks deleted, %d errors",
        files_processed,
        files_skipped,
        total_chunks_upserted,
        chunks_deleted,
        errors,
    )


def _discover_code_files(
    settings: Settings,
    *,
    repo_name: str | None = None,
) -> list[DiscoveredFile]:
    """Walk sources and filter to code repo files only."""
    files: list[DiscoveredFile] = []
    for f in walk_sources(settings):
        # Only code repos (have repository set, language != markdown)
        if not f.repository:
            continue
        if f.language == "markdown":
            continue
        if repo_name and f.repository != repo_name:
            continue
        files.append(f)
    return files


def _process_code_file(
    discovered: DiscoveredFile,
    settings: Settings,
) -> tuple[list[Chunk], list[str]]:
    """Parse, chunk, and enrich a single code file.

    Returns (chunks, chunk_ids).
    """
    source = discovered.absolute_path.read_text(encoding="utf-8", errors="replace")

    # Parse using language-specific parser
    parser_fn = _CODE_PARSERS.get(discovered.language)
    if parser_fn is None:
        log.warning("No parser for language %r: %s", discovered.language, discovered.relative_path)
        return [], []

    units = parser_fn(
        source,
        path=discovered.relative_path,
        repository=discovered.repository,
        source_name=discovered.source_name,
    )

    if not units:
        return [], []

    # Chunk
    chunks = chunk_code_units(units, settings.chunk_sizing)

    # Enrich each chunk
    for chunk in chunks:
        # EIP refs from comments/strings in code
        eip_refs = extract_eip_refs(chunk.text)
        if eip_refs:
            chunk.mentions_eips = eip_refs

        # Code metadata: qualname, used_imports, calls, visibility
        enrich_code_chunk(chunk)

    chunk_ids = [sanitize_chunk_id(c.chunk_id) for c in chunks]
    return chunks, chunk_ids


def _cleanup_stale_code(
    settings: Settings,
    state_db: Path,
    paths_by_repo: dict[str, set[str]],
) -> int:
    """Delete stale chunks for code files that no longer exist on disk.

    Returns the total number of chunk IDs deleted.
    """
    total_deleted = 0
    for repo_name, current_paths in paths_by_repo.items():
        stale_rows = get_stale_files(state_db, repo_name, current_paths)
        for row in stale_rows:
            chunk_ids = json.loads(row.get("chunk_ids_json", "[]"))
            if chunk_ids:
                delete_by_ids(settings, chunk_ids)
                total_deleted += len(chunk_ids)
            remove_indexed_file(state_db, row["repository"], row["file_path"])
            log.info("Removed stale code file: %s:%s", row["repository"], row["file_path"])
    return total_deleted


# ---------------------------------------------------------------------------
# Graph building
# ---------------------------------------------------------------------------


def build_graph(
    settings: Settings,
    *,
    changed_only: bool = False,
    verbose: bool = False,
) -> None:
    """Build or update the dependency graph.

    Two-pass approach:
    1. For all discoverable files, parse + chunk + enrich, then upsert graph nodes.
    2. For all chunks, build edges (EIP deps, cross-refs, code deps) and upsert.

    This re-derives chunks from source files to avoid storing intermediate state.
    The graph DB is fully rebuildable from source.

    Note: *changed_only* is accepted for API consistency with ``sync_all`` but
    the graph is always fully rebuilt (incremental graph updates are not yet
    implemented).
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    if changed_only:
        log.info("build_graph: changed_only is not yet implemented; doing full rebuild")

    # Init both databases
    state_db = init_state_db(settings)
    graph_db_path = init_graph_db(settings)
    conn = get_connection(graph_db_path)

    run_id = start_run(state_db, "build-graph")

    try:
        # Collect all chunks and their dependencies
        all_chunks: list[Chunk] = []
        all_deps: list[tuple[Chunk, list[tuple[str, str, str]]]] = []

        # Process markdown files
        md_files = _discover_markdown_files(settings)
        for discovered in md_files:
            try:
                chunks, _ = _process_markdown_file(discovered, settings)
                all_chunks.extend(chunks)
                for chunk in chunks:
                    all_deps.append((chunk, []))
            except Exception:
                log.exception("Graph build: error processing %s", discovered.relative_path)

        # Process code files
        code_files = _discover_code_files(settings)
        for discovered in code_files:
            try:
                chunks, _ = _process_code_file(discovered, settings)
                all_chunks.extend(chunks)
                for chunk in chunks:
                    deps = extract_dependencies(chunk)
                    all_deps.append((chunk, deps))
            except Exception:
                log.exception("Graph build: error processing %s", discovered.relative_path)

        # Pass 1: upsert all nodes
        nodes_upserted = 0
        for chunk in all_chunks:
            node = chunk_to_node(chunk)
            upsert_node(conn, node)
            nodes_upserted += 1

        conn.commit()
        log.info("Graph pass 1: %d nodes upserted", nodes_upserted)

        # Pass 2: upsert all edges
        edges_upserted = 0
        for chunk, deps in all_deps:
            edge_sets = build_edges_from_chunk(chunk, dependencies=deps)

            for edge in edge_sets["eip_deps"]:
                upsert_eip_dep(conn, edge)
                edges_upserted += 1

            for edge in edge_sets["cross_refs"]:
                upsert_cross_ref(conn, edge)
                edges_upserted += 1

            for edge in edge_sets["code_deps"]:
                upsert_code_dep(conn, edge)
                edges_upserted += 1

        conn.commit()
        log.info("Graph pass 2: %d edges upserted", edges_upserted)

        finish_run(
            state_db,
            run_id,
            files_processed=len(md_files) + len(code_files),
            files_skipped=0,
            chunks_upserted=nodes_upserted,
            chunks_deleted=0,
            errors=0,
        )

    except Exception:
        log.exception("Graph build failed")
        finish_run(state_db, run_id, files_processed=0, files_skipped=0,
                   chunks_upserted=0, chunks_deleted=0, errors=1,
                   error_details=["graph build failed"])
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


def sync_all(
    settings: Settings,
    *,
    changed_only: bool = True,
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    """Full sync: markdown + code + graph.

    Each phase is isolated so that a failure in code ingestion (e.g. missing
    repos) or graph building does not prevent markdown ingestion from completing.
    """
    ingest_markdown(settings, changed_only=changed_only, dry_run=dry_run, verbose=verbose)

    try:
        ingest_code(settings, changed_only=changed_only, dry_run=dry_run, verbose=verbose)
    except Exception:
        log.exception("Code ingestion failed; continuing with graph build")

    if not dry_run:
        try:
            build_graph(settings, changed_only=changed_only, verbose=verbose)
        except Exception:
            log.exception("Graph build failed; sync completing without graph update")


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


def show_stats(settings: Settings, *, repo: str | None = None) -> None:
    """Show index and graph statistics.

    If *repo* is given, only show stats for that repository.
    """
    print("=== Meilisearch Index ===")
    meili_stats = get_index_stats(settings)
    if "error" in meili_stats:
        print(f"  Meilisearch: {meili_stats['error']}")
    else:
        print(f"  Documents: {meili_stats.get('numberOfDocuments', '?')}")
        print(f"  Is indexing: {meili_stats.get('isIndexing', '?')}")
        field_dist = meili_stats.get("fieldDistribution", {})
        if field_dist:
            print(f"  Fields: {len(field_dist)} distinct fields")

    print()
    header = f"=== Graph DB ({repo}) ===" if repo else "=== Graph DB ==="
    print(header)
    try:
        from erd_index.graph.store import get_connection, get_stats

        graph_path = settings.resolved_graph_db
        if graph_path.exists():
            conn = get_connection(graph_path)
            try:
                stats = get_stats(conn, repository=repo)
                for table, count in stats["table_counts"].items():
                    print(f"  {table}: {count}")
                if stats["node_types"]:
                    print("  Node types:")
                    for ntype, count in sorted(stats["node_types"].items()):
                        print(f"    {ntype}: {count}")
            finally:
                conn.close()
        else:
            print("  graph.db not found (run build-graph first)")
    except Exception as exc:
        print(f"  Error reading graph: {exc}")

    print()
    print("=== State DB ===")
    state_path = settings.resolved_state_db
    if state_path.exists():
        runs = get_recent_runs(state_path, limit=5)
        if runs:
            print(f"  Recent runs ({len(runs)}):")
            for run in runs:
                status = "done" if run.get("finished_at") else "running"
                print(
                    f"    [{run['run_id']}] {run['command']} "
                    f"({status}) — {run.get('files_processed', 0)} files, "
                    f"{run.get('chunks_upserted', 0)} chunks, "
                    f"{run.get('errors', 0)} errors"
                )
        else:
            print("  No runs recorded yet")
    else:
        print("  index_state.db not found (run init first)")
