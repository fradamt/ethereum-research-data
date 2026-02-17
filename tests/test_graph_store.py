"""Tests for erd_index.graph — store, node_builder, edge_builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from erd_index.graph.edge_builder import build_edges_from_chunk
from erd_index.graph.node_builder import chunk_to_node
from erd_index.graph.store import (
    delete_nodes_by_file,
    get_connection,
    get_eip_context,
    get_neighbors,
    get_stats,
    init_graph_db,
    upsert_code_dep,
    upsert_cross_ref,
    upsert_eip_dep,
    upsert_node,
    upsert_spec_code_link,
)
from erd_index.models import Chunk, ChunkKind, Language, SourceKind
from erd_index.settings import Settings


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path):
    """Initialize a fresh graph.db and return its path."""
    settings = Settings(
        data_dir=str(tmp_path),
        graph_db=str(tmp_path / "graph.db"),
        project_root=tmp_path,
    )
    return init_graph_db(settings)


@pytest.fixture()
def conn(db_path: Path):
    """Return a connection to the test graph.db; closed after the test."""
    c = get_connection(db_path)
    yield c
    c.close()


def _make_eip_chunk(
    eip: int,
    *,
    heading_path: list[str] | None = None,
    requires: list[int] | None = None,
    supersedes: list[int] | None = None,
    replaces: list[int] | None = None,
    mentions: list[int] | None = None,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.EIP,
        chunk_kind=ChunkKind.EIP_SECTION,
        source_name="eips",
        language=Language.MARKDOWN,
        path=f"EIPS/eip-{eip}.md",
        title=f"EIP-{eip}",
        text=f"Content of EIP-{eip}",
        start_line=1,
        end_line=50,
        eip=eip,
        eip_status="Final",
        eip_type="Core",
        heading_path=heading_path or [],
        requires_eips=requires or [],
        supersedes_eips=supersedes or [],
        replaces_eips=replaces or [],
        mentions_eips=mentions or [],
    )


def _make_forum_chunk(
    topic_id: int,
    post_number: int = 0,
    *,
    author: str = "vbuterin",
    mentions: list[int] | None = None,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.FORUM,
        chunk_kind=ChunkKind.MD_HEADING if post_number <= 1 else ChunkKind.MD_REPLY,
        source_name="ethresearch",
        language=Language.MARKDOWN,
        path=f"topics/{topic_id}.md",
        title=f"Topic {topic_id}",
        text=f"Forum post content for topic {topic_id}",
        start_line=1,
        end_line=20,
        topic_id=topic_id,
        post_number=post_number,
        author=author,
        mentions_eips=mentions or [],
    )


def _make_code_chunk(
    repo: str,
    file_path: str,
    symbol: str,
    *,
    symbol_kind: str = "function",
    language: Language = Language.GO,
    start_line: int = 1,
    end_line: int = 50,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.CODE,
        chunk_kind=ChunkKind.CODE_FUNCTION,
        source_name=repo,
        repository=repo,
        language=language,
        path=file_path,
        text=f"func {symbol}() {{}}",
        start_line=start_line,
        end_line=end_line,
        symbol_name=symbol,
        symbol_kind=symbol_kind,
        symbol_qualname=symbol,
    )


# ===================================================================
# init_graph_db
# ===================================================================


class TestInitGraphDb:
    def test_creates_tables(self, conn):
        """init_graph_db should create all five tables from schema.sql."""
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        table_names = {r["name"] for r in rows}
        assert "node" in table_names
        assert "eip_dependency_edge" in table_names
        assert "spec_code_link" in table_names
        assert "cross_reference_edge" in table_names
        assert "code_dependency_edge" in table_names

    def test_creates_indexes(self, conn):
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
        ).fetchall()
        index_names = {r["name"] for r in rows}
        assert "idx_node_type" in index_names
        assert "idx_node_eip" in index_names
        assert "idx_node_repo_path" in index_names

    def test_idempotent(self, tmp_path):
        """Running init_graph_db twice should not raise."""
        settings = Settings(
            data_dir=str(tmp_path),
            graph_db=str(tmp_path / "graph.db"),
            project_root=tmp_path,
        )
        init_graph_db(settings)
        init_graph_db(settings)  # should not raise

    def test_wal_mode(self, conn):
        row = conn.execute("PRAGMA journal_mode").fetchone()
        assert row[0] == "wal"

    def test_foreign_keys_enabled(self, conn):
        row = conn.execute("PRAGMA foreign_keys").fetchone()
        assert row[0] == 1


# ===================================================================
# upsert_node
# ===================================================================


class TestUpsertNode:
    def test_insert_and_read(self, conn):
        chunk = _make_eip_chunk(1559)
        node = chunk_to_node(chunk)
        upsert_node(conn, node)
        conn.commit()

        row = conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (chunk.node_id,)
        ).fetchone()
        assert row is not None
        assert row["node_type"] == "eip"
        assert row["eip"] == 1559
        assert row["source_name"] == "eips"
        assert row["content_hash"] == chunk.content_hash

    def test_update_existing(self, conn):
        """ON CONFLICT DO UPDATE should update the row without deleting it."""
        chunk = _make_eip_chunk(1559)
        node = chunk_to_node(chunk)
        upsert_node(conn, node)
        conn.commit()

        # Modify title and re-upsert
        node["title"] = "Updated title"
        upsert_node(conn, node)
        conn.commit()

        row = conn.execute(
            "SELECT title FROM node WHERE node_id = ?", (chunk.node_id,)
        ).fetchone()
        assert row["title"] == "Updated title"

        # Still only one row
        count = conn.execute("SELECT COUNT(*) AS cnt FROM node").fetchone()["cnt"]
        assert count == 1

    def test_upsert_preserves_edges(self, conn):
        """Re-upserting a node must NOT cascade-delete its edges."""
        # Create two EIP nodes with an edge between them
        chunk_a = _make_eip_chunk(1559, requires=[4844])
        chunk_b = _make_eip_chunk(4844)
        upsert_node(conn, chunk_to_node(chunk_a))
        upsert_node(conn, chunk_to_node(chunk_b))

        edges = build_edges_from_chunk(chunk_a)
        for edge in edges["eip_deps"]:
            upsert_eip_dep(conn, edge)
        conn.commit()

        # Verify edge exists
        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM eip_dependency_edge WHERE from_eip = 1559"
        ).fetchone()["cnt"]
        assert count >= 1

        # Re-upsert node_a with a title change
        node_a = chunk_to_node(chunk_a)
        node_a["title"] = "Updated EIP-1559"
        upsert_node(conn, node_a)
        conn.commit()

        # Edge must still exist (this was the bug: INSERT OR REPLACE deleted + re-inserted,
        # which cascade-deleted the edge via FK)
        count_after = conn.execute(
            "SELECT COUNT(*) AS cnt FROM eip_dependency_edge WHERE from_eip = 1559"
        ).fetchone()["cnt"]
        assert count_after >= 1


# ===================================================================
# upsert_eip_dep — idempotency
# ===================================================================


class TestUpsertEipDep:
    def test_insert(self, conn):
        chunk = _make_eip_chunk(1559, requires=[2718])
        upsert_node(conn, chunk_to_node(chunk))
        conn.commit()

        edges = build_edges_from_chunk(chunk)
        for e in edges["eip_deps"]:
            upsert_eip_dep(conn, e)
        conn.commit()

        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM eip_dependency_edge"
        ).fetchone()["cnt"]
        assert count == 1

    def test_idempotent(self, conn):
        """Inserting the same edge twice should not raise or duplicate."""
        chunk = _make_eip_chunk(1559, requires=[2718])
        upsert_node(conn, chunk_to_node(chunk))
        conn.commit()

        edge = build_edges_from_chunk(chunk)["eip_deps"][0]
        upsert_eip_dep(conn, edge)
        upsert_eip_dep(conn, edge)
        conn.commit()

        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM eip_dependency_edge"
        ).fetchone()["cnt"]
        assert count == 1

    def test_multiple_relations(self, conn):
        chunk = _make_eip_chunk(4844, requires=[1559], supersedes=[2718])
        upsert_node(conn, chunk_to_node(chunk))
        conn.commit()

        edges = build_edges_from_chunk(chunk)
        for e in edges["eip_deps"]:
            upsert_eip_dep(conn, e)
        conn.commit()

        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM eip_dependency_edge"
        ).fetchone()["cnt"]
        assert count == 2


# ===================================================================
# upsert_cross_ref — idempotency
# ===================================================================


class TestUpsertCrossRef:
    def test_insert_and_idempotent(self, conn):
        # Create both source and target nodes
        forum = _make_forum_chunk(100, mentions=[1559])
        eip = _make_eip_chunk(1559)
        upsert_node(conn, chunk_to_node(forum))
        upsert_node(conn, chunk_to_node(eip))
        conn.commit()

        edges = build_edges_from_chunk(forum)
        for e in edges["cross_refs"]:
            upsert_cross_ref(conn, e)
        conn.commit()
        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM cross_reference_edge"
        ).fetchone()["cnt"]
        assert count == 1

        # Repeat — should stay at 1
        for e in edges["cross_refs"]:
            upsert_cross_ref(conn, e)
        conn.commit()
        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM cross_reference_edge"
        ).fetchone()["cnt"]
        assert count == 1

    def test_self_reference_skipped(self, conn):
        """EIP chunks should not create cross-ref edges to themselves."""
        chunk = _make_eip_chunk(1559, mentions=[1559, 4844])
        edges = build_edges_from_chunk(chunk)
        # Only 4844 should appear (self-ref to 1559 skipped)
        assert len(edges["cross_refs"]) == 1
        assert edges["cross_refs"][0]["to_node_id"] == "eip:4844"


# ===================================================================
# upsert_code_dep — idempotency
# ===================================================================


class TestUpsertCodeDep:
    def test_internal_dep(self, conn):
        a = _make_code_chunk("geth", "core/vm/run.go", "Run")
        b = _make_code_chunk("geth", "core/vm/stack.go", "Push")
        upsert_node(conn, chunk_to_node(a))
        upsert_node(conn, chunk_to_node(b))
        conn.commit()

        edges = build_edges_from_chunk(
            a, dependencies=[(a.node_id, b.node_id, "calls")]
        )
        for e in edges["code_deps"]:
            upsert_code_dep(conn, e)
        conn.commit()

        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM code_dependency_edge"
        ).fetchone()["cnt"]
        assert count == 1

    def test_external_dep(self, conn):
        a = _make_code_chunk("geth", "core/vm/run.go", "Run")
        upsert_node(conn, chunk_to_node(a))
        conn.commit()

        edges = build_edges_from_chunk(
            a, dependencies=[(a.node_id, "fmt.Println", "calls")]
        )
        for e in edges["code_deps"]:
            upsert_code_dep(conn, e)
        conn.commit()

        row = conn.execute(
            "SELECT * FROM code_dependency_edge"
        ).fetchone()
        assert row["to_code_node_id"] is None
        assert row["to_external_symbol"] == "fmt.Println"

    def test_idempotent(self, conn):
        a = _make_code_chunk("geth", "core/vm/run.go", "Run")
        upsert_node(conn, chunk_to_node(a))
        conn.commit()

        edge = {
            "from_code_node_id": a.node_id,
            "to_code_node_id": None,
            "to_external_symbol": "fmt.Println",
            "relation": "calls",
        }
        upsert_code_dep(conn, edge)
        upsert_code_dep(conn, edge)
        conn.commit()

        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM code_dependency_edge"
        ).fetchone()["cnt"]
        assert count == 1


# ===================================================================
# upsert_spec_code_link — idempotency
# ===================================================================


class TestUpsertSpecCodeLink:
    def test_insert_and_idempotent(self, conn):
        eip = _make_eip_chunk(1559)
        code = _make_code_chunk("geth", "core/state_transition.go", "ApplyTransaction")
        upsert_node(conn, chunk_to_node(eip))
        upsert_node(conn, chunk_to_node(code))
        conn.commit()

        link = {
            "eip": 1559,
            "eip_section_anchor": None,
            "eip_node_id": eip.node_id,
            "code_node_id": code.node_id,
            "relation": "implements",
            "match_method": "heuristic",
            "confidence": 0.8,
        }
        upsert_spec_code_link(conn, link)
        upsert_spec_code_link(conn, link)
        conn.commit()

        count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM spec_code_link"
        ).fetchone()["cnt"]
        assert count == 1


# ===================================================================
# delete_nodes_by_file — cascading
# ===================================================================


class TestDeleteNodesByFile:
    def test_cascade_to_edges(self, conn):
        """Deleting a node should cascade-delete its edges."""
        a = _make_code_chunk("geth", "core/vm/run.go", "Run")
        b = _make_code_chunk("geth", "core/vm/stack.go", "Push")
        upsert_node(conn, chunk_to_node(a))
        upsert_node(conn, chunk_to_node(b))
        conn.commit()

        upsert_code_dep(conn, {
            "from_code_node_id": a.node_id,
            "to_code_node_id": b.node_id,
            "to_external_symbol": None,
            "relation": "calls",
        })
        conn.commit()

        assert conn.execute(
            "SELECT COUNT(*) AS cnt FROM code_dependency_edge"
        ).fetchone()["cnt"] == 1

        # Delete node a
        deleted = delete_nodes_by_file(conn, "geth", "core/vm/run.go")
        conn.commit()
        assert deleted == 1

        # Edge should be cascade-deleted (from_code_node_id was a)
        assert conn.execute(
            "SELECT COUNT(*) AS cnt FROM code_dependency_edge"
        ).fetchone()["cnt"] == 0

    def test_returns_zero_for_missing(self, conn):
        deleted = delete_nodes_by_file(conn, "geth", "nonexistent.go")
        assert deleted == 0

    def test_deletes_multiple_nodes(self, conn):
        """Multiple nodes in the same file should all be deleted."""
        a = _make_code_chunk("geth", "core/vm/ops.go", "Add", start_line=1, end_line=10)
        b = _make_code_chunk("geth", "core/vm/ops.go", "Sub", start_line=11, end_line=20)
        upsert_node(conn, chunk_to_node(a))
        upsert_node(conn, chunk_to_node(b))
        conn.commit()

        deleted = delete_nodes_by_file(conn, "geth", "core/vm/ops.go")
        conn.commit()
        assert deleted == 2


# ===================================================================
# get_neighbors
# ===================================================================


class TestGetNeighbors:
    def test_depth_1_code(self, conn):
        a = _make_code_chunk("geth", "a.go", "A")
        b = _make_code_chunk("geth", "b.go", "B")
        c = _make_code_chunk("geth", "c.go", "C")
        for ch in [a, b, c]:
            upsert_node(conn, chunk_to_node(ch))
        conn.commit()

        # A -> B -> C
        upsert_code_dep(conn, {
            "from_code_node_id": a.node_id,
            "to_code_node_id": b.node_id,
            "to_external_symbol": None,
            "relation": "calls",
        })
        upsert_code_dep(conn, {
            "from_code_node_id": b.node_id,
            "to_code_node_id": c.node_id,
            "to_external_symbol": None,
            "relation": "calls",
        })
        conn.commit()

        n1 = get_neighbors(conn, a.node_id, depth=1)
        ids1 = {n["node_id"] for n in n1}
        assert b.node_id in ids1
        assert c.node_id not in ids1

    def test_depth_2_code(self, conn):
        a = _make_code_chunk("geth", "a.go", "A")
        b = _make_code_chunk("geth", "b.go", "B")
        c = _make_code_chunk("geth", "c.go", "C")
        for ch in [a, b, c]:
            upsert_node(conn, chunk_to_node(ch))
        conn.commit()

        upsert_code_dep(conn, {
            "from_code_node_id": a.node_id,
            "to_code_node_id": b.node_id,
            "to_external_symbol": None,
            "relation": "calls",
        })
        upsert_code_dep(conn, {
            "from_code_node_id": b.node_id,
            "to_code_node_id": c.node_id,
            "to_external_symbol": None,
            "relation": "calls",
        })
        conn.commit()

        n2 = get_neighbors(conn, a.node_id, depth=2)
        ids2 = {n["node_id"] for n in n2}
        assert b.node_id in ids2
        assert c.node_id in ids2

    def test_eip_dependency_neighbors(self, conn):
        eip_a = _make_eip_chunk(1559)
        eip_b = _make_eip_chunk(2718)
        upsert_node(conn, chunk_to_node(eip_a))
        upsert_node(conn, chunk_to_node(eip_b))
        conn.commit()

        upsert_eip_dep(conn, {
            "from_eip": 1559,
            "to_eip": 2718,
            "relation": "requires",
            "source_node_id": eip_a.node_id,
        })
        conn.commit()

        # From A, should find B
        neighbors = get_neighbors(conn, eip_a.node_id, depth=1)
        assert any(n["node_id"] == eip_b.node_id for n in neighbors)

        # Reverse: from B, should find A
        neighbors_rev = get_neighbors(conn, eip_b.node_id, depth=1)
        assert any(n["node_id"] == eip_a.node_id for n in neighbors_rev)

    def test_cross_ref_neighbors(self, conn):
        forum = _make_forum_chunk(100, mentions=[1559])
        eip = _make_eip_chunk(1559)
        upsert_node(conn, chunk_to_node(forum))
        upsert_node(conn, chunk_to_node(eip))
        conn.commit()

        edges = build_edges_from_chunk(forum)
        for e in edges["cross_refs"]:
            upsert_cross_ref(conn, e)
        conn.commit()

        neighbors = get_neighbors(conn, forum.node_id, depth=1)
        assert any(n["node_id"] == eip.node_id for n in neighbors)

    def test_relation_filter(self, conn):
        a = _make_code_chunk("geth", "a.go", "A")
        b = _make_code_chunk("geth", "b.go", "B")
        c = _make_code_chunk("geth", "c.go", "TypeC", symbol_kind="struct")
        for ch in [a, b, c]:
            upsert_node(conn, chunk_to_node(ch))
        conn.commit()

        upsert_code_dep(conn, {
            "from_code_node_id": a.node_id,
            "to_code_node_id": b.node_id,
            "to_external_symbol": None,
            "relation": "calls",
        })
        upsert_code_dep(conn, {
            "from_code_node_id": a.node_id,
            "to_code_node_id": c.node_id,
            "to_external_symbol": None,
            "relation": "uses_type",
        })
        conn.commit()

        # Filter by 'calls' — should only find B
        n = get_neighbors(conn, a.node_id, relation="calls")
        ids = {r["node_id"] for r in n}
        assert b.node_id in ids
        assert c.node_id not in ids

    def test_limit(self, conn):
        """get_neighbors should respect the limit parameter."""
        source = _make_code_chunk("geth", "src.go", "Source")
        upsert_node(conn, chunk_to_node(source))
        targets = []
        for i in range(5):
            t = _make_code_chunk("geth", f"t{i}.go", f"T{i}")
            targets.append(t)
            upsert_node(conn, chunk_to_node(t))
        conn.commit()

        for t in targets:
            upsert_code_dep(conn, {
                "from_code_node_id": source.node_id,
                "to_code_node_id": t.node_id,
                "to_external_symbol": None,
                "relation": "calls",
            })
        conn.commit()

        n = get_neighbors(conn, source.node_id, limit=3)
        assert len(n) == 3

    def test_empty(self, conn):
        a = _make_code_chunk("geth", "a.go", "A")
        upsert_node(conn, chunk_to_node(a))
        conn.commit()

        n = get_neighbors(conn, a.node_id)
        assert n == []

    def test_spec_code_link_neighbors(self, conn):
        eip = _make_eip_chunk(1559)
        code = _make_code_chunk("geth", "tx.go", "ApplyTx")
        upsert_node(conn, chunk_to_node(eip))
        upsert_node(conn, chunk_to_node(code))
        conn.commit()

        upsert_spec_code_link(conn, {
            "eip": 1559,
            "eip_section_anchor": None,
            "eip_node_id": eip.node_id,
            "code_node_id": code.node_id,
            "relation": "implements",
            "match_method": "heuristic",
            "confidence": 0.9,
        })
        conn.commit()

        # From EIP node, should find code
        n = get_neighbors(conn, eip.node_id, depth=1)
        assert any(r["node_id"] == code.node_id for r in n)

        # From code node, should find EIP
        n_rev = get_neighbors(conn, code.node_id, depth=1)
        assert any(r["node_id"] == eip.node_id for r in n_rev)


# ===================================================================
# get_eip_context
# ===================================================================


class TestGetEipContext:
    def test_full_context(self, conn):
        """get_eip_context returns eip_nodes, code_nodes, forum_nodes, deps."""
        eip = _make_eip_chunk(1559, requires=[2718])
        eip_dep = _make_eip_chunk(2718)
        code = _make_code_chunk("geth", "tx.go", "ApplyTx")
        forum = _make_forum_chunk(100, mentions=[1559])

        for ch in [eip, eip_dep, code, forum]:
            upsert_node(conn, chunk_to_node(ch))
        conn.commit()

        # EIP dep edge
        for e in build_edges_from_chunk(eip)["eip_deps"]:
            upsert_eip_dep(conn, e)

        # Spec-code link
        upsert_spec_code_link(conn, {
            "eip": 1559,
            "eip_section_anchor": None,
            "eip_node_id": eip.node_id,
            "code_node_id": code.node_id,
            "relation": "implements",
            "match_method": "heuristic",
            "confidence": 0.8,
        })

        # Forum cross-ref
        for e in build_edges_from_chunk(forum)["cross_refs"]:
            upsert_cross_ref(conn, e)
        conn.commit()

        ctx = get_eip_context(conn, 1559)

        assert len(ctx["eip_nodes"]) == 1
        assert ctx["eip_nodes"][0]["eip"] == 1559

        assert len(ctx["code_nodes"]) == 1
        assert ctx["code_nodes"][0]["symbol_name"] == "ApplyTx"

        assert len(ctx["forum_nodes"]) == 1
        assert ctx["forum_nodes"][0]["node_type"] == "forum_topic"

        assert len(ctx["dependencies"]) == 1
        assert ctx["dependencies"][0]["to_eip"] == 2718

    def test_dependents(self, conn):
        eip_a = _make_eip_chunk(1559)
        eip_b = _make_eip_chunk(4844, requires=[1559])
        upsert_node(conn, chunk_to_node(eip_a))
        upsert_node(conn, chunk_to_node(eip_b))
        conn.commit()

        for e in build_edges_from_chunk(eip_b)["eip_deps"]:
            upsert_eip_dep(conn, e)
        conn.commit()

        ctx = get_eip_context(conn, 1559)
        assert len(ctx["dependents"]) == 1
        assert ctx["dependents"][0]["from_eip"] == 4844

    def test_empty_context(self, conn):
        ctx = get_eip_context(conn, 9999)
        assert ctx["eip_nodes"] == []
        assert ctx["code_nodes"] == []
        assert ctx["forum_nodes"] == []
        assert ctx["dependencies"] == []
        assert ctx["dependents"] == []


# ===================================================================
# get_stats
# ===================================================================


class TestGetStats:
    def test_empty_db(self, conn):
        stats = get_stats(conn)
        assert stats["table_counts"]["node"] == 0
        assert stats["table_counts"]["eip_dependency_edge"] == 0
        assert stats["node_types"] == {}

    def test_counts(self, conn):
        eip = _make_eip_chunk(1559, requires=[2718])
        forum = _make_forum_chunk(100, mentions=[1559])
        code = _make_code_chunk("geth", "tx.go", "Apply")

        for ch in [eip, forum, code]:
            upsert_node(conn, chunk_to_node(ch))
        conn.commit()

        stats = get_stats(conn)
        assert stats["table_counts"]["node"] == 3
        assert stats["node_types"]["eip"] == 1
        assert stats["node_types"]["forum_topic"] == 1
        assert stats["node_types"]["code_function"] == 1


# ===================================================================
# chunk_to_node — node type mapping
# ===================================================================


class TestChunkToNode:
    def test_eip_no_heading(self):
        chunk = _make_eip_chunk(1559)
        node = chunk_to_node(chunk)
        assert node["node_type"] == "eip"
        assert node["eip"] == 1559
        assert node["section_anchor"] is None

    def test_eip_section(self):
        chunk = _make_eip_chunk(1559, heading_path=["Specification", "Gas Costs"])
        node = chunk_to_node(chunk)
        assert node["node_type"] == "eip_section"
        assert node["section_anchor"] == "gas-costs"

    def test_forum_topic(self):
        chunk = _make_forum_chunk(100, post_number=0)
        node = chunk_to_node(chunk)
        assert node["node_type"] == "forum_topic"

    def test_forum_topic_post1(self):
        chunk = _make_forum_chunk(100, post_number=1)
        node = chunk_to_node(chunk)
        assert node["node_type"] == "forum_topic"

    def test_forum_reply(self):
        chunk = _make_forum_chunk(100, post_number=5)
        node = chunk_to_node(chunk)
        assert node["node_type"] == "forum_post"

    def test_code_function(self):
        chunk = _make_code_chunk("geth", "vm.go", "Run", symbol_kind="function")
        node = chunk_to_node(chunk)
        assert node["node_type"] == "code_function"

    def test_code_method(self):
        chunk = _make_code_chunk("geth", "vm.go", "Run", symbol_kind="method")
        node = chunk_to_node(chunk)
        assert node["node_type"] == "code_function"

    def test_code_struct(self):
        chunk = Chunk(
            source_kind=SourceKind.CODE,
            chunk_kind=ChunkKind.CODE_STRUCT,
            source_name="geth",
            repository="geth",
            language=Language.GO,
            path="types.go",
            text="type Block struct {}",
            start_line=1,
            end_line=10,
            symbol_name="Block",
            symbol_kind="struct",
            symbol_qualname="Block",
        )
        node = chunk_to_node(chunk)
        assert node["node_type"] == "code_struct"

    def test_code_enum(self):
        chunk = Chunk(
            source_kind=SourceKind.CODE,
            chunk_kind=ChunkKind.CODE_STRUCT,
            source_name="lighthouse",
            repository="lighthouse",
            language=Language.RUST,
            path="types.rs",
            text="enum Slot {}",
            start_line=1,
            end_line=10,
            symbol_name="Slot",
            symbol_kind="enum",
            symbol_qualname="Slot",
        )
        node = chunk_to_node(chunk)
        assert node["node_type"] == "code_enum"

    def test_code_trait(self):
        chunk = Chunk(
            source_kind=SourceKind.CODE,
            chunk_kind=ChunkKind.CODE_STRUCT,
            source_name="lighthouse",
            repository="lighthouse",
            language=Language.RUST,
            path="traits.rs",
            text="trait Validator {}",
            start_line=1,
            end_line=10,
            symbol_name="Validator",
            symbol_kind="trait",
            symbol_qualname="Validator",
        )
        node = chunk_to_node(chunk)
        assert node["node_type"] == "code_trait"

    def test_code_group(self):
        chunk = Chunk(
            source_kind=SourceKind.CODE,
            chunk_kind=ChunkKind.CODE_GROUP,
            source_name="geth",
            repository="geth",
            language=Language.GO,
            path="helpers.go",
            text="func a() {}\nfunc b() {}",
            start_line=1,
            end_line=10,
            symbol_name="a",
            symbol_kind="function",
            symbol_qualname="a",
            member_symbols=["a", "b"],
        )
        node = chunk_to_node(chunk)
        assert node["node_type"] == "code_function"
        meta = json.loads(node["metadata_json"])
        assert meta["member_symbols"] == ["a", "b"]

    def test_metadata_fields(self):
        chunk = _make_forum_chunk(100, author="vbuterin")
        chunk.category = "Sharding"
        chunk.tags = ["das", "sampling"]
        node = chunk_to_node(chunk)
        meta = json.loads(node["metadata_json"])
        assert meta["author"] == "vbuterin"
        assert meta["category"] == "Sharding"
        assert meta["tags"] == ["das", "sampling"]

    def test_content_hash_set(self):
        chunk = _make_eip_chunk(1559)
        node = chunk_to_node(chunk)
        assert node["content_hash"] == chunk.content_hash
        assert len(node["content_hash"]) == 16

    def test_node_id_matches_chunk(self):
        chunk = _make_code_chunk("geth", "vm.go", "Run")
        node = chunk_to_node(chunk)
        assert node["node_id"] == chunk.node_id


# ===================================================================
# build_edges_from_chunk
# ===================================================================


class TestBuildEdgesFromChunk:
    def test_eip_deps_from_requires(self):
        chunk = _make_eip_chunk(1559, requires=[2718, 2930])
        edges = build_edges_from_chunk(chunk)
        assert len(edges["eip_deps"]) == 2
        rels = {(e["from_eip"], e["to_eip"], e["relation"]) for e in edges["eip_deps"]}
        assert (1559, 2718, "requires") in rels
        assert (1559, 2930, "requires") in rels

    def test_eip_deps_from_supersedes(self):
        chunk = _make_eip_chunk(1559, supersedes=[1234])
        edges = build_edges_from_chunk(chunk)
        assert len(edges["eip_deps"]) == 1
        assert edges["eip_deps"][0]["relation"] == "supersedes"

    def test_eip_deps_from_replaces(self):
        chunk = _make_eip_chunk(1559, replaces=[999])
        edges = build_edges_from_chunk(chunk)
        assert len(edges["eip_deps"]) == 1
        assert edges["eip_deps"][0]["relation"] == "replaces"

    def test_no_eip_deps_for_non_eip(self):
        chunk = _make_forum_chunk(100)
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []

    def test_cross_refs_from_mentions(self):
        chunk = _make_forum_chunk(100, mentions=[1559, 4844])
        edges = build_edges_from_chunk(chunk)
        assert len(edges["cross_refs"]) == 2
        targets = {e["to_node_id"] for e in edges["cross_refs"]}
        assert targets == {"eip:1559", "eip:4844"}

    def test_cross_refs_skip_self(self):
        chunk = _make_eip_chunk(1559, mentions=[1559, 4844])
        edges = build_edges_from_chunk(chunk)
        assert len(edges["cross_refs"]) == 1
        assert edges["cross_refs"][0]["to_node_id"] == "eip:4844"

    def test_code_deps_resolved(self):
        chunk = _make_code_chunk("geth", "a.go", "A")
        deps = [(chunk.node_id, "geth:b.go:B", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        assert len(edges["code_deps"]) == 1
        assert edges["code_deps"][0]["to_code_node_id"] == "geth:b.go:B"
        assert edges["code_deps"][0]["to_external_symbol"] is None

    def test_code_deps_external(self):
        chunk = _make_code_chunk("geth", "a.go", "A")
        deps = [(chunk.node_id, "fmt.Println", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        assert len(edges["code_deps"]) == 1
        assert edges["code_deps"][0]["to_code_node_id"] is None
        assert edges["code_deps"][0]["to_external_symbol"] == "fmt.Println"

    def test_no_deps(self):
        chunk = _make_code_chunk("geth", "a.go", "A")
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []
        assert edges["cross_refs"] == []
        assert edges["code_deps"] == []

    def test_all_edge_types_together(self):
        chunk = _make_eip_chunk(1559, requires=[2718], mentions=[4844])
        deps = [(chunk.node_id, "fmt.Println", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        assert len(edges["eip_deps"]) == 1
        assert len(edges["cross_refs"]) == 1
        assert len(edges["code_deps"]) == 1

    def test_edge_confidence_and_extractor(self):
        chunk = _make_eip_chunk(1559, requires=[2718])
        edges = build_edges_from_chunk(chunk)
        dep = edges["eip_deps"][0]
        assert dep["confidence"] == 1.0
        assert dep["extractor"] == "frontmatter"
        assert dep["source_node_id"] == chunk.node_id
