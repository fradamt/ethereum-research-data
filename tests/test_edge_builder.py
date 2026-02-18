"""Tests for erd_index/graph/edge_builder.py — edge construction from chunks."""

from __future__ import annotations

from erd_index.graph.edge_builder import build_edges_from_chunk
from erd_index.models import Chunk, ChunkKind, Language, SourceKind

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _eip_chunk(
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
        heading_path=heading_path or [],
        requires_eips=requires or [],
        supersedes_eips=supersedes or [],
        replaces_eips=replaces or [],
        mentions_eips=mentions or [],
    )


def _forum_chunk(
    topic_id: int,
    post_number: int = 1,
    *,
    mentions: list[int] | None = None,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.FORUM,
        chunk_kind=ChunkKind.MD_HEADING,
        source_name="ethresearch",
        language=Language.MARKDOWN,
        path=f"topics/{topic_id}.md",
        title=f"Topic {topic_id}",
        text=f"Forum post content for topic {topic_id}",
        start_line=1,
        end_line=20,
        topic_id=topic_id,
        post_number=post_number,
        mentions_eips=mentions or [],
    )


def _code_chunk(
    repo: str = "go-ethereum",
    file_path: str = "core/vm/run.go",
    symbol: str = "Run",
    *,
    language: Language = Language.GO,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.CODE,
        chunk_kind=ChunkKind.CODE_FUNCTION,
        source_name=repo,
        repository=repo,
        language=language,
        path=file_path,
        text=f"func {symbol}() {{}}",
        start_line=1,
        end_line=50,
        symbol_name=symbol,
        symbol_kind="function",
        symbol_qualname=symbol,
    )


# ===================================================================
# EIP dependency edges
# ===================================================================


class TestEipDependencyEdges:
    def test_requires_edge(self) -> None:
        chunk = _eip_chunk(1559, requires=[2718])
        edges = build_edges_from_chunk(chunk)
        deps = edges["eip_deps"]
        assert len(deps) == 1
        assert deps[0]["from_eip"] == 1559
        assert deps[0]["to_eip"] == 2718
        assert deps[0]["relation"] == "requires"
        assert deps[0]["confidence"] == 1.0
        assert deps[0]["extractor"] == "frontmatter"

    def test_multiple_requires(self) -> None:
        chunk = _eip_chunk(4844, requires=[1559, 2930, 2718])
        edges = build_edges_from_chunk(chunk)
        deps = edges["eip_deps"]
        assert len(deps) == 3
        to_eips = {e["to_eip"] for e in deps}
        assert to_eips == {1559, 2930, 2718}
        # All should be "requires"
        assert all(e["relation"] == "requires" for e in deps)

    def test_supersedes_edge_direction(self) -> None:
        """supersedes_eips means 'this EIP is superseded BY these EIPs'.

        So the superseder is from_eip, and chunk.eip is to_eip.
        """
        chunk = _eip_chunk(1559, supersedes=[4844])
        edges = build_edges_from_chunk(chunk)
        deps = edges["eip_deps"]
        assert len(deps) == 1
        # 4844 supersedes 1559
        assert deps[0]["from_eip"] == 4844
        assert deps[0]["to_eip"] == 1559
        assert deps[0]["relation"] == "supersedes"

    def test_replaces_edge(self) -> None:
        chunk = _eip_chunk(1559, replaces=[999])
        edges = build_edges_from_chunk(chunk)
        deps = edges["eip_deps"]
        assert len(deps) == 1
        assert deps[0]["from_eip"] == 1559
        assert deps[0]["to_eip"] == 999
        assert deps[0]["relation"] == "replaces"

    def test_combined_deps(self) -> None:
        chunk = _eip_chunk(4844, requires=[1559], supersedes=[100], replaces=[200])
        edges = build_edges_from_chunk(chunk)
        deps = edges["eip_deps"]
        assert len(deps) == 3
        rels = {(e["from_eip"], e["to_eip"], e["relation"]) for e in deps}
        assert (4844, 1559, "requires") in rels
        assert (100, 4844, "supersedes") in rels
        assert (4844, 200, "replaces") in rels

    def test_no_eip_deps_for_non_eip_chunk(self) -> None:
        chunk = _forum_chunk(100)
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []

    def test_no_eip_deps_with_empty_lists(self) -> None:
        chunk = _eip_chunk(1559, requires=[], supersedes=[], replaces=[])
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []

    def test_source_node_id_in_edge(self) -> None:
        chunk = _eip_chunk(1559, requires=[2718])
        edges = build_edges_from_chunk(chunk)
        dep = edges["eip_deps"][0]
        assert dep["source_node_id"] == chunk.node_id

    def test_evidence_text_is_none(self) -> None:
        chunk = _eip_chunk(1559, requires=[2718])
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"][0]["evidence_text"] is None


# ===================================================================
# Cross-reference edges
# ===================================================================


class TestCrossReferenceEdges:
    def test_forum_mentions_eip(self) -> None:
        chunk = _forum_chunk(100, mentions=[1559])
        edges = build_edges_from_chunk(chunk)
        refs = edges["cross_refs"]
        assert len(refs) == 1
        assert refs[0]["from_node_id"] == chunk.node_id
        assert refs[0]["to_node_id"] == "eip:1559"
        assert refs[0]["relation"] == "mentions_eip"
        assert refs[0]["anchor_text"] == "EIP-1559"
        assert refs[0]["confidence"] == 1.0
        assert refs[0]["extractor"] == "eip_refs"

    def test_multiple_mentions(self) -> None:
        chunk = _forum_chunk(100, mentions=[1559, 4844, 2930])
        edges = build_edges_from_chunk(chunk)
        refs = edges["cross_refs"]
        assert len(refs) == 3
        targets = {r["to_node_id"] for r in refs}
        assert targets == {"eip:1559", "eip:4844", "eip:2930"}

    def test_self_reference_skipped(self) -> None:
        """EIP chunks should not create edges to themselves."""
        chunk = _eip_chunk(1559, mentions=[1559, 4844])
        edges = build_edges_from_chunk(chunk)
        refs = edges["cross_refs"]
        assert len(refs) == 1
        assert refs[0]["to_node_id"] == "eip:4844"

    def test_only_self_reference(self) -> None:
        """If the only mention is self, no cross-ref edges are produced."""
        chunk = _eip_chunk(1559, mentions=[1559])
        edges = build_edges_from_chunk(chunk)
        assert edges["cross_refs"] == []

    def test_no_mentions(self) -> None:
        chunk = _forum_chunk(100, mentions=[])
        edges = build_edges_from_chunk(chunk)
        assert edges["cross_refs"] == []

    def test_code_chunk_with_mentions(self) -> None:
        """Code chunks can also have mentions_eips (from comments)."""
        chunk = _code_chunk()
        chunk.mentions_eips = [1559]
        edges = build_edges_from_chunk(chunk)
        refs = edges["cross_refs"]
        assert len(refs) == 1
        assert refs[0]["to_node_id"] == "eip:1559"

    def test_span_fields_are_none(self) -> None:
        chunk = _forum_chunk(100, mentions=[1559])
        edges = build_edges_from_chunk(chunk)
        ref = edges["cross_refs"][0]
        assert ref["span_start"] is None
        assert ref["span_end"] is None


# ===================================================================
# Code dependency edges
# ===================================================================


class TestCodeDependencyEdges:
    def test_resolved_internal_dep(self) -> None:
        """A single colon in to_symbol means it's resolved to a node_id."""
        chunk = _code_chunk("geth", "a.go", "A")
        deps = [("A", "geth:b.go:B", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        code_deps = edges["code_deps"]
        assert len(code_deps) == 1
        assert code_deps[0]["from_code_node_id"] == chunk.node_id
        assert code_deps[0]["to_code_node_id"] == "geth:b.go:B"
        assert code_deps[0]["to_external_symbol"] is None
        assert code_deps[0]["relation"] == "calls"
        assert code_deps[0]["confidence"] == 0.7
        assert code_deps[0]["extractor"] == "tree_sitter"

    def test_external_dep_no_colon(self) -> None:
        """No colon means it's an external/unresolved symbol."""
        chunk = _code_chunk("geth", "a.go", "A")
        deps = [("A", "fmt.Println", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        code_deps = edges["code_deps"]
        assert len(code_deps) == 1
        assert code_deps[0]["to_code_node_id"] is None
        assert code_deps[0]["to_external_symbol"] == "fmt.Println"

    def test_rust_double_colon_is_external(self) -> None:
        """Rust paths with :: should be treated as external."""
        chunk = _code_chunk("lighthouse", "beacon.rs", "process", language=Language.RUST)
        deps = [("process", "std::collections::HashMap", "uses_type")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        code_deps = edges["code_deps"]
        assert len(code_deps) == 1
        assert code_deps[0]["to_code_node_id"] is None
        assert code_deps[0]["to_external_symbol"] == "std::collections::HashMap"
        assert code_deps[0]["relation"] == "uses_type"

    def test_multiple_dependencies(self) -> None:
        chunk = _code_chunk("geth", "a.go", "A")
        deps = [
            ("A", "geth:b.go:B", "calls"),
            ("A", "fmt.Println", "calls"),
            ("A", "geth:types.go:Block", "uses_type"),
        ]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        code_deps = edges["code_deps"]
        assert len(code_deps) == 3

    def test_no_dependencies(self) -> None:
        chunk = _code_chunk()
        edges = build_edges_from_chunk(chunk, dependencies=[])
        assert edges["code_deps"] == []

    def test_none_dependencies(self) -> None:
        chunk = _code_chunk()
        edges = build_edges_from_chunk(chunk, dependencies=None)
        assert edges["code_deps"] == []

    def test_from_node_id_uses_chunk_node_id(self) -> None:
        """from_code_node_id should use chunk.node_id, not the raw from_sym."""
        chunk = _code_chunk("geth", "a.go", "A")
        deps = [("raw_sym_A", "geth:b.go:B", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        # Should use chunk.node_id, which is "geth:a.go:A"
        assert edges["code_deps"][0]["from_code_node_id"] == chunk.node_id
        assert edges["code_deps"][0]["from_code_node_id"] != "raw_sym_A"

    def test_evidence_text_is_none(self) -> None:
        chunk = _code_chunk("geth", "a.go", "A")
        deps = [("A", "geth:b.go:B", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        assert edges["code_deps"][0]["evidence_text"] is None

    def test_relation_types(self) -> None:
        """Various relation types should be passed through."""
        chunk = _code_chunk("lighthouse", "beacon.rs", "process", language=Language.RUST)
        deps = [
            ("process", "lighthouse:types.rs:Validator", "uses_type"),
            ("process", "lighthouse:traits.rs:BeaconChain", "implements_trait"),
            ("process", "lighthouse:imports.rs:load", "imports"),
        ]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        rels = {e["relation"] for e in edges["code_deps"]}
        assert rels == {"uses_type", "implements_trait", "imports"}


# ===================================================================
# build_edges_from_chunk — combined output
# ===================================================================


class TestBuildEdgesFromChunkCombined:
    def test_returns_all_three_keys(self) -> None:
        chunk = _forum_chunk(100)
        edges = build_edges_from_chunk(chunk)
        assert "eip_deps" in edges
        assert "cross_refs" in edges
        assert "code_deps" in edges

    def test_empty_chunk_no_edges(self) -> None:
        chunk = _forum_chunk(100, mentions=[])
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []
        assert edges["cross_refs"] == []
        assert edges["code_deps"] == []

    def test_all_edge_types_together(self) -> None:
        chunk = _eip_chunk(1559, requires=[2718], mentions=[4844])
        deps = [("1559", "geth:tx.go:Apply", "calls")]
        edges = build_edges_from_chunk(chunk, dependencies=deps)
        assert len(edges["eip_deps"]) == 1
        assert len(edges["cross_refs"]) == 1
        assert len(edges["code_deps"]) == 1

    def test_code_chunk_with_no_eip_or_mentions(self) -> None:
        chunk = _code_chunk()
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []
        assert edges["cross_refs"] == []
        assert edges["code_deps"] == []


# ===================================================================
# Edge cases — None/empty inputs
# ===================================================================


class TestEdgeCasesNoneCrash:
    def test_eip_none_no_crash(self) -> None:
        """Chunk with eip=None should not produce eip_deps."""
        chunk = _forum_chunk(100)
        assert chunk.eip is None
        edges = build_edges_from_chunk(chunk)
        assert edges["eip_deps"] == []

    def test_empty_mentions_no_crash(self) -> None:
        chunk = _forum_chunk(100, mentions=[])
        edges = build_edges_from_chunk(chunk)
        assert edges["cross_refs"] == []

    def test_empty_dependencies_no_crash(self) -> None:
        chunk = _code_chunk()
        edges = build_edges_from_chunk(chunk, dependencies=[])
        assert edges["code_deps"] == []
