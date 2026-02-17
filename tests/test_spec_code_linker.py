"""Tests for erd_index.enrich.spec_code_linker — heuristic spec-to-code matching."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from erd_index.graph.node_builder import chunk_to_node
from erd_index.graph.store import (
    get_connection,
    init_graph_db,
    upsert_node,
    upsert_spec_code_link,
)
from erd_index.enrich.spec_code_linker import (
    find_spec_code_links,
    find_spec_code_links_from_text,
    _heuristic_symbol_name,
    _heuristic_file_path,
    _heuristic_eip_ref_in_text,
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


def _make_eip_chunk(eip: int) -> Chunk:
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
        heading_path=[],
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
    text: str | None = None,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.CODE,
        chunk_kind=ChunkKind.CODE_FUNCTION,
        source_name=repo,
        repository=repo,
        language=language,
        path=file_path,
        text=text or f"func {symbol}() {{}}",
        start_line=start_line,
        end_line=end_line,
        symbol_name=symbol,
        symbol_kind=symbol_kind,
        symbol_qualname=symbol,
    )


def _insert_eip(conn, eip: int) -> Chunk:
    """Insert an EIP node and return the chunk."""
    chunk = _make_eip_chunk(eip)
    upsert_node(conn, chunk_to_node(chunk))
    return chunk


def _insert_code(conn, repo: str, path: str, symbol: str, **kwargs) -> Chunk:
    """Insert a code node and return the chunk."""
    chunk = _make_code_chunk(repo, path, symbol, **kwargs)
    upsert_node(conn, chunk_to_node(chunk))
    return chunk


# ===================================================================
# Heuristic 2 — Symbol name contains EIP number
# ===================================================================


class TestHeuristicSymbolName:
    def test_camel_case_eip(self, conn):
        """applyEIP1559 -> links to EIP-1559."""
        _insert_eip(conn, 1559)
        code = _insert_code(conn, "geth", "core/fee.go", "applyEIP1559")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_symbol_name(node, {1559})
        assert len(links) == 1
        assert links[0]["eip"] == 1559
        assert links[0]["relation"] == "implements"
        assert links[0]["confidence"] == 0.9

    def test_underscore_eip(self, conn):
        """eip_4844_blob_gas -> links to EIP-4844."""
        _insert_eip(conn, 4844)
        code = _insert_code(conn, "geth", "core/eip4844.go", "eip_4844_blob_gas")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_symbol_name(node, {4844})
        assert len(links) == 1
        assert links[0]["eip"] == 4844

    def test_eip_prefix(self, conn):
        """EIP1559BaseFee -> links to EIP-1559."""
        _insert_eip(conn, 1559)
        code = _insert_code(conn, "geth", "core/fee.go", "EIP1559BaseFee")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_symbol_name(node, {1559})
        assert len(links) == 1
        assert links[0]["eip"] == 1559

    def test_no_match(self, conn):
        """Symbol name without EIP reference produces no links."""
        _insert_eip(conn, 1559)
        code = _insert_code(conn, "geth", "core/vm.go", "applyTransaction")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_symbol_name(node, {1559})
        assert links == []

    def test_unindexed_eip_ignored(self, conn):
        """Even if symbol mentions EIP-9999, it's skipped if not indexed."""
        code = _insert_code(conn, "geth", "core/fee.go", "applyEIP9999")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_symbol_name(node, {1559})
        assert links == []

    def test_multiple_eips_in_name(self, conn):
        """Symbol mentioning multiple EIPs produces multiple links."""
        _insert_eip(conn, 1559)
        _insert_eip(conn, 4844)
        code = _insert_code(conn, "geth", "core/fee.go", "eip1559_eip4844_handler")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_symbol_name(node, {1559, 4844})
        eips = {link["eip"] for link in links}
        assert eips == {1559, 4844}


# ===================================================================
# Heuristic 3 — Test file path
# ===================================================================


class TestHeuristicFilePath:
    def test_test_file_with_eip(self, conn):
        """test_eip4844.py -> links to EIP-4844 as 'tests'."""
        _insert_eip(conn, 4844)
        code = _insert_code(
            conn, "geth", "tests/test_eip4844.py", "test_blob_gas",
            language=Language.PYTHON,
        )
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_file_path(node, {4844})
        assert len(links) == 1
        assert links[0]["eip"] == 4844
        assert links[0]["relation"] == "tests"
        assert links[0]["confidence"] == 0.7

    def test_go_test_file(self, conn):
        """eip1559_test.go -> links to EIP-1559."""
        _insert_eip(conn, 1559)
        code = _insert_code(conn, "geth", "core/eip1559_test.go", "TestApplyFee")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_file_path(node, {1559})
        assert len(links) == 1
        assert links[0]["eip"] == 1559
        assert links[0]["relation"] == "tests"

    def test_non_test_file_skipped(self, conn):
        """Non-test file with eip in path should NOT produce links."""
        _insert_eip(conn, 1559)
        code = _insert_code(conn, "geth", "core/eip1559.go", "ApplyFee")
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_file_path(node, {1559})
        assert links == []

    def test_unindexed_eip_ignored(self, conn):
        """Test file for unindexed EIP produces no links."""
        code = _insert_code(
            conn, "geth", "tests/test_eip9999.py", "test_something",
            language=Language.PYTHON,
        )
        conn.commit()

        node = dict(conn.execute(
            "SELECT * FROM node WHERE node_id = ?", (code.node_id,)
        ).fetchone())

        links = _heuristic_file_path(node, {1559})
        assert links == []


# ===================================================================
# Heuristic 1 — EIP reference in text
# ===================================================================


class TestHeuristicEipRefInText:
    def test_reference_in_comment(self):
        """Code text with EIP-1559 reference -> 'references' link."""
        node = {
            "node_id": "geth:core/fee.go:applyFee",
            "symbol_name": "applyFee",
        }
        text = "// Implements the base fee mechanism from EIP-1559\nfunc applyFee() {}"

        links = _heuristic_eip_ref_in_text(node, text, {1559})
        assert len(links) == 1
        assert links[0]["eip"] == 1559
        assert links[0]["relation"] == "references"
        assert links[0]["confidence"] == 0.8

    def test_implements_when_symbol_matches(self):
        """If symbol also contains EIP number, relation is 'implements'."""
        node = {
            "node_id": "geth:core/fee.go:applyEIP1559",
            "symbol_name": "applyEIP1559",
        }
        text = "// EIP-1559 base fee calculation\nfunc applyEIP1559() {}"

        links = _heuristic_eip_ref_in_text(node, text, {1559})
        assert len(links) == 1
        assert links[0]["relation"] == "implements"

    def test_multiple_eips_in_text(self):
        """Text referencing multiple EIPs produces multiple links."""
        node = {
            "node_id": "geth:core/tx.go:processTx",
            "symbol_name": "processTx",
        }
        text = "// Uses EIP-1559 and EIP-4844 gas pricing\nfunc processTx() {}"

        links = _heuristic_eip_ref_in_text(node, text, {1559, 4844})
        eips = {link["eip"] for link in links}
        assert eips == {1559, 4844}

    def test_no_eip_in_text(self):
        """Text without EIP references produces no links."""
        node = {
            "node_id": "geth:core/vm.go:run",
            "symbol_name": "run",
        }
        text = "func run() {}"

        links = _heuristic_eip_ref_in_text(node, text, {1559})
        assert links == []


# ===================================================================
# find_spec_code_links — integration
# ===================================================================


class TestFindSpecCodeLinks:
    def test_finds_symbol_name_links(self, conn):
        """Integration: symbol name heuristic finds links."""
        _insert_eip(conn, 1559)
        _insert_code(conn, "geth", "core/fee.go", "applyEIP1559")
        conn.commit()

        links = find_spec_code_links(conn)
        assert len(links) >= 1
        link = next(l for l in links if l["eip"] == 1559)
        assert link["relation"] == "implements"
        assert link["confidence"] == 0.9
        assert link["match_method"] == "heuristic"

    def test_finds_test_file_links(self, conn):
        """Integration: test file heuristic finds links."""
        _insert_eip(conn, 4844)
        _insert_code(
            conn, "geth", "core/tests/test_eip4844.go", "TestBlobGas",
        )
        conn.commit()

        links = find_spec_code_links(conn)
        assert len(links) >= 1
        link = next(l for l in links if l["eip"] == 4844)
        assert link["relation"] == "tests"
        assert link["confidence"] == 0.7

    def test_deduplication(self, conn):
        """If both heuristics match same (eip, code_node, relation), keep highest confidence."""
        _insert_eip(conn, 1559)
        # Symbol name matches EIP-1559 -> implements at 0.9
        # Test file also matches -> tests at 0.7 (different relation, so both kept)
        _insert_code(
            conn, "geth", "tests/test_eip1559.go", "applyEIP1559",
        )
        conn.commit()

        links = find_spec_code_links(conn)
        # Should have both implements (from symbol) and tests (from path)
        relations = {l["relation"] for l in links if l["eip"] == 1559}
        assert "implements" in relations
        assert "tests" in relations

    def test_eip_node_id_resolved(self, conn):
        """Links should have eip_node_id pointing to the EIP node."""
        eip = _insert_eip(conn, 1559)
        _insert_code(conn, "geth", "core/fee.go", "applyEIP1559")
        conn.commit()

        links = find_spec_code_links(conn)
        assert len(links) >= 1
        link = next(l for l in links if l["eip"] == 1559)
        assert link["eip_node_id"] == eip.node_id

    def test_no_code_nodes(self, conn):
        """No code nodes -> empty result."""
        _insert_eip(conn, 1559)
        conn.commit()

        links = find_spec_code_links(conn)
        assert links == []

    def test_no_eip_nodes(self, conn):
        """No EIP nodes -> empty result."""
        _insert_code(conn, "geth", "core/fee.go", "applyEIP1559")
        conn.commit()

        links = find_spec_code_links(conn)
        assert links == []

    def test_no_matching_code(self, conn):
        """Code without EIP references -> empty result."""
        _insert_eip(conn, 1559)
        _insert_code(conn, "geth", "core/vm.go", "Run")
        conn.commit()

        links = find_spec_code_links(conn)
        assert links == []


# ===================================================================
# Idempotency — upserting links twice
# ===================================================================


class TestIdempotency:
    def test_upsert_twice_no_duplicates(self, conn):
        """Running find + upsert twice should not create duplicate links."""
        _insert_eip(conn, 1559)
        _insert_code(conn, "geth", "core/fee.go", "applyEIP1559")
        conn.commit()

        # First pass
        links = find_spec_code_links(conn)
        for link in links:
            upsert_spec_code_link(conn, link)
        conn.commit()

        count_1 = conn.execute(
            "SELECT COUNT(*) AS cnt FROM spec_code_link"
        ).fetchone()["cnt"]

        # Second pass
        links = find_spec_code_links(conn)
        for link in links:
            upsert_spec_code_link(conn, link)
        conn.commit()

        count_2 = conn.execute(
            "SELECT COUNT(*) AS cnt FROM spec_code_link"
        ).fetchone()["cnt"]

        assert count_1 == count_2
        assert count_1 >= 1


# ===================================================================
# find_spec_code_links_from_text — text-based linking
# ===================================================================


class TestFindSpecCodeLinksFromText:
    def test_returns_links_for_text_refs(self):
        """Text with EIP-1559 reference produces links."""
        node = {
            "node_id": "geth:core/fee.go:applyFee",
            "symbol_name": "applyFee",
        }
        text = "// EIP-1559 base fee\nfunc applyFee() {}"

        links = find_spec_code_links_from_text(node, text, {1559})
        assert len(links) == 1
        assert links[0]["eip"] == 1559

    def test_empty_for_no_refs(self):
        """Text without EIP refs produces no links."""
        node = {
            "node_id": "geth:core/vm.go:run",
            "symbol_name": "run",
        }
        links = find_spec_code_links_from_text(node, "func run() {}", {1559})
        assert links == []


# ===================================================================
# Evidence JSON
# ===================================================================


class TestEvidenceJson:
    def test_symbol_name_evidence(self, conn):
        """Symbol name heuristic stores match details in evidence_json."""
        _insert_eip(conn, 1559)
        _insert_code(conn, "geth", "core/fee.go", "applyEIP1559")
        conn.commit()

        links = find_spec_code_links(conn)
        link = next(l for l in links if l["eip"] == 1559 and l["relation"] == "implements")
        evidence = json.loads(link["evidence_json"])
        assert evidence["heuristic"] == "symbol_name"
        assert "applyEIP1559" in evidence["symbol"]

    def test_file_path_evidence(self, conn):
        """File path heuristic stores path details in evidence_json."""
        _insert_eip(conn, 4844)
        _insert_code(
            conn, "geth", "core/tests/test_eip4844.go", "TestBlobGas",
        )
        conn.commit()

        links = find_spec_code_links(conn)
        link = next(l for l in links if l["eip"] == 4844 and l["relation"] == "tests")
        evidence = json.loads(link["evidence_json"])
        assert evidence["heuristic"] == "test_file_path"
        assert "eip4844" in evidence["file_path"]
