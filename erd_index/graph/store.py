"""SQLite graph store: connection management and CRUD operations.

Manages data/graph.db — a WAL-mode SQLite database holding nodes and edges
for the Ethereum research knowledge graph.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING, Any

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from erd_index.settings import Settings

__all__ = [
    "delete_nodes_by_file",
    "get_connection",
    "get_eip_context",
    "get_neighbors",
    "get_stats",
    "init_graph_db",
    "upsert_code_dep",
    "upsert_cross_ref",
    "upsert_eip_dep",
    "upsert_node",
    "upsert_spec_code_link",
]

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def init_graph_db(settings: Settings) -> Path:
    """Create the data directory (if needed) and apply schema.sql.

    Returns the resolved path to graph.db.
    """
    db_path = settings.resolved_graph_db
    db_path.parent.mkdir(parents=True, exist_ok=True)

    schema_sql = _SCHEMA_PATH.read_text(encoding="utf-8")
    conn = get_connection(db_path)
    try:
        conn.executescript(schema_sql)
    finally:
        conn.close()

    return db_path


def get_connection(db_path: Path | str) -> sqlite3.Connection:
    """Return a WAL-mode connection with foreign keys enabled.

    Row factory is set to ``sqlite3.Row`` for dict-like access.
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Node CRUD
# ---------------------------------------------------------------------------


def upsert_node(conn: sqlite3.Connection, node: dict[str, Any]) -> None:
    """Upsert a node row using ON CONFLICT DO UPDATE.

    *node* must contain at minimum ``node_id``, ``node_type``, ``source_name``,
    and ``content_hash``.  All other fields are optional and default to NULL or
    the schema default.

    Uses ON CONFLICT ... DO UPDATE instead of INSERT OR REPLACE to avoid
    cascade-deleting edges that reference this node via foreign keys.
    """
    conn.execute(
        """
        INSERT INTO node (
            node_id, node_type, source_name, repository, language, file_path,
            chunk_id, title, url, eip, section_anchor, symbol_name, symbol_kind,
            start_line, end_line, content_hash, metadata_json, updated_at
        ) VALUES (
            :node_id, :node_type, :source_name, :repository, :language, :file_path,
            :chunk_id, :title, :url, :eip, :section_anchor, :symbol_name, :symbol_kind,
            :start_line, :end_line, :content_hash, :metadata_json, CURRENT_TIMESTAMP
        )
        ON CONFLICT(node_id) DO UPDATE SET
            node_type       = excluded.node_type,
            source_name     = excluded.source_name,
            repository      = excluded.repository,
            language        = excluded.language,
            file_path       = excluded.file_path,
            chunk_id        = excluded.chunk_id,
            title           = excluded.title,
            url             = excluded.url,
            eip             = excluded.eip,
            section_anchor  = excluded.section_anchor,
            symbol_name     = excluded.symbol_name,
            symbol_kind     = excluded.symbol_kind,
            start_line      = excluded.start_line,
            end_line        = excluded.end_line,
            content_hash    = excluded.content_hash,
            metadata_json   = excluded.metadata_json,
            updated_at      = CURRENT_TIMESTAMP
        """,
        {
            "node_id": node["node_id"],
            "node_type": node["node_type"],
            "source_name": node["source_name"],
            "repository": node.get("repository"),
            "language": node.get("language"),
            "file_path": node.get("file_path"),
            "chunk_id": node.get("chunk_id"),
            "title": node.get("title"),
            "url": node.get("url"),
            "eip": node.get("eip"),
            "section_anchor": node.get("section_anchor"),
            "symbol_name": node.get("symbol_name"),
            "symbol_kind": node.get("symbol_kind"),
            "start_line": node.get("start_line"),
            "end_line": node.get("end_line"),
            "content_hash": node["content_hash"],
            "metadata_json": node.get("metadata_json", "{}"),
        },
    )


def delete_nodes_by_file(
    conn: sqlite3.Connection, repository: str, file_path: str
) -> int:
    """Delete all nodes for a given file.  Cascading deletes remove associated edges.

    Returns the number of deleted rows.
    """
    cur = conn.execute(
        "DELETE FROM node WHERE repository = ? AND file_path = ?",
        (repository, file_path),
    )
    return cur.rowcount


# ---------------------------------------------------------------------------
# Edge CRUD
# ---------------------------------------------------------------------------


def upsert_eip_dep(conn: sqlite3.Connection, edge: dict[str, Any]) -> None:
    """INSERT OR IGNORE an EIP dependency edge."""
    conn.execute(
        """
        INSERT OR IGNORE INTO eip_dependency_edge (
            from_eip, to_eip, relation, source_node_id,
            confidence, evidence_text, extractor
        ) VALUES (
            :from_eip, :to_eip, :relation, :source_node_id,
            :confidence, :evidence_text, :extractor
        )
        """,
        {
            "from_eip": edge["from_eip"],
            "to_eip": edge["to_eip"],
            "relation": edge["relation"],
            "source_node_id": edge["source_node_id"],
            "confidence": edge.get("confidence", 1.0),
            "evidence_text": edge.get("evidence_text"),
            "extractor": edge.get("extractor", "frontmatter"),
        },
    )


def upsert_spec_code_link(conn: sqlite3.Connection, link: dict[str, Any]) -> None:
    """INSERT OR IGNORE a spec-to-code implementation link.

    The UNIQUE constraint includes nullable eip_section_anchor.  SQLite
    treats NULL != NULL, so we check existence manually.
    """
    section_anchor = link.get("eip_section_anchor")

    exists = conn.execute(
        """SELECT 1 FROM spec_code_link
           WHERE eip = ? AND code_node_id = ? AND relation = ?
           AND eip_section_anchor IS ?""",
        (link["eip"], link["code_node_id"], link["relation"], section_anchor),
    ).fetchone()

    if exists:
        return

    conn.execute(
        """
        INSERT INTO spec_code_link (
            eip, eip_section_anchor, eip_node_id, code_node_id,
            relation, match_method, confidence, evidence_json
        ) VALUES (
            :eip, :eip_section_anchor, :eip_node_id, :code_node_id,
            :relation, :match_method, :confidence, :evidence_json
        )
        """,
        {
            "eip": link["eip"],
            "eip_section_anchor": section_anchor,
            "eip_node_id": link.get("eip_node_id"),
            "code_node_id": link["code_node_id"],
            "relation": link["relation"],
            "match_method": link["match_method"],
            "confidence": link["confidence"],
            "evidence_json": link.get("evidence_json", "{}"),
        },
    )


def upsert_cross_ref(conn: sqlite3.Connection, edge: dict[str, Any]) -> None:
    """INSERT OR IGNORE a cross-reference edge.

    The UNIQUE constraint includes nullable span_start/span_end columns.
    SQLite treats NULL != NULL for uniqueness, so we check existence manually.
    """
    span_start = edge.get("span_start")
    span_end = edge.get("span_end")

    # Build existence check that handles NULLs correctly
    if span_start is None and span_end is None:
        exists = conn.execute(
            """SELECT 1 FROM cross_reference_edge
               WHERE from_node_id = ? AND to_node_id = ? AND relation = ?
               AND span_start IS NULL AND span_end IS NULL""",
            (edge["from_node_id"], edge["to_node_id"], edge["relation"]),
        ).fetchone()
    else:
        exists = conn.execute(
            """SELECT 1 FROM cross_reference_edge
               WHERE from_node_id = ? AND to_node_id = ? AND relation = ?
               AND span_start IS ? AND span_end IS ?""",
            (edge["from_node_id"], edge["to_node_id"], edge["relation"],
             span_start, span_end),
        ).fetchone()

    if exists:
        return

    try:
        conn.execute(
            """
            INSERT INTO cross_reference_edge (
                from_node_id, to_node_id, relation,
                span_start, span_end, anchor_text,
                confidence, extractor
            ) VALUES (
                :from_node_id, :to_node_id, :relation,
                :span_start, :span_end, :anchor_text,
                :confidence, :extractor
            )
            """,
            {
                "from_node_id": edge["from_node_id"],
                "to_node_id": edge["to_node_id"],
                "relation": edge["relation"],
                "span_start": span_start,
                "span_end": span_end,
                "anchor_text": edge.get("anchor_text"),
                "confidence": edge.get("confidence", 1.0),
                "extractor": edge["extractor"],
            },
        )
    except sqlite3.IntegrityError:
        # Target node doesn't exist (e.g., EIP not indexed). Skip gracefully.
        log.debug(
            "Skipping cross-ref edge: target node %r not found",
            edge["to_node_id"],
        )


def upsert_code_dep(conn: sqlite3.Connection, edge: dict[str, Any]) -> None:
    """INSERT OR IGNORE a code dependency edge.

    The UNIQUE constraint includes nullable to_code_node_id and
    to_external_symbol columns.  SQLite treats NULL != NULL, so we check
    existence manually.
    """
    to_node = edge.get("to_code_node_id")
    to_ext = edge.get("to_external_symbol")

    exists = conn.execute(
        """SELECT 1 FROM code_dependency_edge
           WHERE from_code_node_id = ? AND relation = ?
           AND to_code_node_id IS ? AND to_external_symbol IS ?""",
        (edge["from_code_node_id"], edge["relation"], to_node, to_ext),
    ).fetchone()

    if exists:
        return

    try:
        conn.execute(
            """
            INSERT INTO code_dependency_edge (
                from_code_node_id, to_code_node_id, to_external_symbol,
                relation, confidence, extractor, evidence_text
            ) VALUES (
                :from_code_node_id, :to_code_node_id, :to_external_symbol,
                :relation, :confidence, :extractor, :evidence_text
            )
            """,
            {
                "from_code_node_id": edge["from_code_node_id"],
                "to_code_node_id": to_node,
                "to_external_symbol": to_ext,
                "relation": edge["relation"],
                "confidence": edge.get("confidence", 0.7),
                "extractor": edge.get("extractor", "tree_sitter"),
                "evidence_text": edge.get("evidence_text"),
            },
        )
    except sqlite3.IntegrityError:
        # Source or target node doesn't exist. Skip gracefully.
        log.debug(
            "Skipping code dep edge: node not found (from=%r, to=%r)",
            edge["from_code_node_id"],
            to_node or to_ext,
        )


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------


def get_neighbors(
    conn: sqlite3.Connection,
    node_id: str,
    *,
    relation: str | None = None,
    depth: int = 1,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Return neighboring nodes up to *depth* hops away.

    Traverses all four edge tables (eip_dependency_edge, spec_code_link,
    cross_reference_edge, code_dependency_edge).  Optionally filter by
    *relation* type.

    For depth > 1, performs iterative expansion (BFS) rather than recursive
    SQL to keep queries simple and predictable.
    """
    visited: set[str] = {node_id}
    frontier: set[str] = {node_id}
    results: list[dict[str, Any]] = []

    for _ in range(depth):
        if not frontier:
            break
        next_frontier: set[str] = set()

        for current_id in frontier:
            neighbor_ids = _find_adjacent(conn, current_id, relation=relation)
            for nid in neighbor_ids:
                if nid not in visited:
                    visited.add(nid)
                    next_frontier.add(nid)

        frontier = next_frontier

    # Fetch full node rows for all discovered neighbors (excluding the seed)
    all_neighbor_ids = visited - {node_id}
    for nid in sorted(all_neighbor_ids):
        row = conn.execute("SELECT * FROM node WHERE node_id = ?", (nid,)).fetchone()
        if row:
            results.append(dict(row))
        if len(results) >= limit:
            break

    return results


def _find_adjacent(
    conn: sqlite3.Connection,
    node_id: str,
    *,
    relation: str | None = None,
) -> set[str]:
    """Return node IDs adjacent to *node_id* across all edge tables."""
    ids: set[str] = set()

    # --- EIP dependency edges (keyed by EIP number, need node lookup) ---
    # First find if this node is an EIP node
    row = conn.execute(
        "SELECT eip FROM node WHERE node_id = ? AND eip IS NOT NULL", (node_id,)
    ).fetchone()
    if row:
        eip_num = row["eip"]
        # Outgoing: this EIP depends on other EIPs
        q = "SELECT to_eip FROM eip_dependency_edge WHERE from_eip = ?"
        params: list[Any] = [eip_num]
        if relation:
            q += " AND relation = ?"
            params.append(relation)
        for r in conn.execute(q, params):
            for nr in conn.execute(
                "SELECT node_id FROM node WHERE eip = ? AND node_type = 'eip'",
                (r["to_eip"],),
            ):
                ids.add(nr["node_id"])

        # Incoming: other EIPs depend on this one
        q = "SELECT from_eip FROM eip_dependency_edge WHERE to_eip = ?"
        params = [eip_num]
        if relation:
            q += " AND relation = ?"
            params.append(relation)
        for r in conn.execute(q, params):
            for nr in conn.execute(
                "SELECT node_id FROM node WHERE eip = ? AND node_type = 'eip'",
                (r["from_eip"],),
            ):
                ids.add(nr["node_id"])

    # --- Cross-reference edges ---
    q = "SELECT to_node_id FROM cross_reference_edge WHERE from_node_id = ?"
    params = [node_id]
    if relation:
        q += " AND relation = ?"
        params.append(relation)
    for r in conn.execute(q, params):
        ids.add(r["to_node_id"])

    q = "SELECT from_node_id FROM cross_reference_edge WHERE to_node_id = ?"
    params = [node_id]
    if relation:
        q += " AND relation = ?"
        params.append(relation)
    for r in conn.execute(q, params):
        ids.add(r["from_node_id"])

    # --- Code dependency edges ---
    q = "SELECT to_code_node_id FROM code_dependency_edge WHERE from_code_node_id = ?"
    params = [node_id]
    if relation:
        q += " AND relation = ?"
        params.append(relation)
    for r in conn.execute(q, params):
        if r["to_code_node_id"]:
            ids.add(r["to_code_node_id"])

    q = "SELECT from_code_node_id FROM code_dependency_edge WHERE to_code_node_id = ?"
    params = [node_id]
    if relation:
        q += " AND relation = ?"
        params.append(relation)
    for r in conn.execute(q, params):
        ids.add(r["from_code_node_id"])

    # --- Spec-code links ---
    q = "SELECT code_node_id FROM spec_code_link WHERE eip_node_id = ?"
    params = [node_id]
    if relation:
        q += " AND relation = ?"
        params.append(relation)
    for r in conn.execute(q, params):
        ids.add(r["code_node_id"])

    q = "SELECT eip_node_id FROM spec_code_link WHERE code_node_id = ?"
    params = [node_id]
    if relation:
        q += " AND relation = ?"
        params.append(relation)
    for r in conn.execute(q, params):
        if r["eip_node_id"]:
            ids.add(r["eip_node_id"])

    return ids


def get_eip_context(conn: sqlite3.Connection, eip_number: int) -> dict[str, Any]:
    """Return all nodes related to an EIP: the EIP itself, implementing code,
    and forum discussions.

    Returns a dict with keys ``eip_nodes``, ``code_nodes``, ``forum_nodes``,
    ``dependencies``, ``dependents``.
    """
    # The EIP node(s) themselves
    eip_nodes = [
        dict(r)
        for r in conn.execute("SELECT * FROM node WHERE eip = ?", (eip_number,))
    ]

    # Code implementing this EIP (via spec_code_link)
    code_nodes = [
        dict(r)
        for r in conn.execute(
            """
            SELECT n.* FROM node n
            JOIN spec_code_link scl ON n.node_id = scl.code_node_id
            WHERE scl.eip = ?
            """,
            (eip_number,),
        )
    ]

    # Forum posts that mention this EIP (via cross_reference_edge)
    eip_node_ids = [n["node_id"] for n in eip_nodes]
    forum_nodes: list[dict[str, Any]] = []
    for eip_nid in eip_node_ids:
        for r in conn.execute(
            """
            SELECT n.* FROM node n
            JOIN cross_reference_edge cre ON n.node_id = cre.from_node_id
            WHERE cre.to_node_id = ? AND cre.relation = 'mentions_eip'
            AND n.node_type IN ('forum_topic', 'forum_post')
            """,
            (eip_nid,),
        ):
            forum_nodes.append(dict(r))

    # EIP dependencies (outgoing)
    dependencies = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM eip_dependency_edge WHERE from_eip = ?",
            (eip_number,),
        )
    ]

    # EIP dependents (incoming)
    dependents = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM eip_dependency_edge WHERE to_eip = ?",
            (eip_number,),
        )
    ]

    return {
        "eip_nodes": eip_nodes,
        "code_nodes": code_nodes,
        "forum_nodes": forum_nodes,
        "dependencies": dependencies,
        "dependents": dependents,
    }


def get_stats(
    conn: sqlite3.Connection, *, repository: str | None = None
) -> dict[str, Any]:
    """Return counts per table and node type breakdown.

    If *repository* is given, only count nodes (and node types) for that repo.
    Edge counts are always global since edges span repos.
    """
    counts: dict[str, int] = {}

    if repository:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM node WHERE repository = ?", (repository,)
        ).fetchone()
        counts["node"] = row["cnt"]
    else:
        tables = [
            "node",
            "eip_dependency_edge",
            "spec_code_link",
            "cross_reference_edge",
            "code_dependency_edge",
        ]
        for table in tables:
            row = conn.execute(f"SELECT COUNT(*) AS cnt FROM {table}").fetchone()
            counts[table] = row["cnt"]

    # Node type breakdown
    type_counts: dict[str, int] = {}
    if repository:
        for r in conn.execute(
            "SELECT node_type, COUNT(*) AS cnt FROM node WHERE repository = ? GROUP BY node_type",
            (repository,),
        ):
            type_counts[r["node_type"]] = r["cnt"]
    else:
        for r in conn.execute(
            "SELECT node_type, COUNT(*) AS cnt FROM node GROUP BY node_type"
        ):
            type_counts[r["node_type"]] = r["cnt"]

    return {"table_counts": counts, "node_types": type_counts}
