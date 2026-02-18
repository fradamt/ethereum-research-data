"""Tests for erd_index/graph/node_builder.py — chunk-to-node conversion."""

from __future__ import annotations

import json

from erd_index.graph.node_builder import chunk_to_node
from erd_index.models import Chunk, ChunkKind, Language, SourceKind

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _forum_chunk(
    topic_id: int = 1234,
    post_number: int = 1,
    *,
    author: str = "vbuterin",
    category: str = "Sharding",
    tags: list[str] | None = None,
    research_thread: str = "",
    influence_score: float = 0.0,
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
        category=category,
        tags=tags or [],
        research_thread=research_thread,
        influence_score=influence_score,
    )


def _eip_chunk(
    eip: int = 1559,
    *,
    heading_path: list[str] | None = None,
    url: str = "",
    title: str = "",
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.EIP,
        chunk_kind=ChunkKind.EIP_SECTION,
        source_name="eips",
        language=Language.MARKDOWN,
        path=f"EIPS/eip-{eip}.md",
        title=title or f"EIP-{eip}",
        text=f"Content of EIP-{eip}",
        start_line=1,
        end_line=50,
        eip=eip,
        heading_path=heading_path or [],
        url=url,
    )


def _code_chunk(
    repo: str = "go-ethereum",
    file_path: str = "core/vm/interpreter.go",
    symbol: str = "Run",
    *,
    symbol_kind: str = "function",
    language: Language = Language.GO,
    signature: str = "",
    parent_symbol: str = "",
    module_path: str = "",
    visibility: str = "",
    member_symbols: list[str] | None = None,
    chunk_kind: ChunkKind = ChunkKind.CODE_FUNCTION,
    start_line: int = 1,
    end_line: int = 50,
) -> Chunk:
    return Chunk(
        source_kind=SourceKind.CODE,
        chunk_kind=chunk_kind,
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
        signature=signature,
        parent_symbol=parent_symbol,
        module_path=module_path,
        visibility=visibility,
        member_symbols=member_symbols or [],
    )


# ===================================================================
# Forum chunk -> node
# ===================================================================


class TestForumChunkToNode:
    def test_topic_opener_type(self) -> None:
        node = chunk_to_node(_forum_chunk(post_number=0))
        assert node["node_type"] == "forum_topic"

    def test_post_number_1_is_topic(self) -> None:
        node = chunk_to_node(_forum_chunk(post_number=1))
        assert node["node_type"] == "forum_topic"

    def test_reply_type(self) -> None:
        node = chunk_to_node(_forum_chunk(post_number=5))
        assert node["node_type"] == "forum_post"

    def test_node_id_matches_chunk(self) -> None:
        chunk = _forum_chunk(topic_id=1234, post_number=3)
        node = chunk_to_node(chunk)
        assert node["node_id"] == chunk.node_id
        assert node["node_id"] == "forum:ethresearch:1234:3"

    def test_core_fields(self) -> None:
        chunk = _forum_chunk()
        node = chunk_to_node(chunk)
        assert node["source_name"] == "ethresearch"
        assert node["repository"] is None  # forum has no repo
        assert node["language"] == "markdown"
        assert node["file_path"] == "topics/1234.md"
        assert node["chunk_id"] == chunk.chunk_id
        assert node["title"] == "Topic 1234"
        assert node["eip"] is None
        assert node["symbol_name"] is None
        assert node["symbol_kind"] is None
        assert node["start_line"] == 1
        assert node["end_line"] == 20
        assert node["content_hash"] == chunk.content_hash

    def test_section_anchor_none_for_forum(self) -> None:
        """Forum chunks have no heading_path -> no section_anchor."""
        node = chunk_to_node(_forum_chunk())
        assert node["section_anchor"] is None

    def test_metadata_includes_author(self) -> None:
        node = chunk_to_node(_forum_chunk(author="dankrad"))
        meta = json.loads(node["metadata_json"])
        assert meta["author"] == "dankrad"

    def test_metadata_includes_category(self) -> None:
        node = chunk_to_node(_forum_chunk(category="Consensus"))
        meta = json.loads(node["metadata_json"])
        assert meta["category"] == "Consensus"

    def test_metadata_includes_tags(self) -> None:
        node = chunk_to_node(_forum_chunk(tags=["das", "sampling"]))
        meta = json.loads(node["metadata_json"])
        assert meta["tags"] == ["das", "sampling"]

    def test_metadata_includes_research_thread(self) -> None:
        node = chunk_to_node(_forum_chunk(research_thread="danksharding"))
        meta = json.loads(node["metadata_json"])
        assert meta["research_thread"] == "danksharding"

    def test_metadata_includes_influence_score(self) -> None:
        node = chunk_to_node(_forum_chunk(influence_score=0.95))
        meta = json.loads(node["metadata_json"])
        assert meta["influence_score"] == 0.95

    def test_metadata_empty_when_no_optional_fields(self) -> None:
        node = chunk_to_node(_forum_chunk(author="", category="", influence_score=0.0))
        meta = json.loads(node["metadata_json"])
        assert meta == {}

    def test_url_none_when_empty(self) -> None:
        chunk = _forum_chunk()
        chunk.url = ""
        node = chunk_to_node(chunk)
        assert node["url"] is None

    def test_url_set_when_present(self) -> None:
        chunk = _forum_chunk()
        chunk.url = "https://ethresear.ch/t/1234"
        node = chunk_to_node(chunk)
        assert node["url"] == "https://ethresear.ch/t/1234"


# ===================================================================
# EIP chunk -> node
# ===================================================================


class TestEipChunkToNode:
    def test_eip_no_heading(self) -> None:
        node = chunk_to_node(_eip_chunk(1559, heading_path=[]))
        assert node["node_type"] == "eip"
        assert node["eip"] == 1559
        assert node["section_anchor"] is None

    def test_eip_section(self) -> None:
        node = chunk_to_node(_eip_chunk(1559, heading_path=["Specification", "Gas Costs"]))
        assert node["node_type"] == "eip_section"
        assert node["section_anchor"] == "gas-costs"

    def test_eip_section_anchor_kebab_case(self) -> None:
        """Section anchor is the last heading element, kebab-cased."""
        node = chunk_to_node(_eip_chunk(1559, heading_path=["Foo", "Some Long Heading"]))
        assert node["section_anchor"] == "some-long-heading"

    def test_eip_fields(self) -> None:
        node = chunk_to_node(_eip_chunk(4844))
        assert node["eip"] == 4844
        assert node["source_name"] == "eips"
        assert node["language"] == "markdown"
        assert node["file_path"] == "EIPS/eip-4844.md"

    def test_eip_url(self) -> None:
        node = chunk_to_node(_eip_chunk(1559, url="https://eips.ethereum.org/EIPS/eip-1559"))
        assert node["url"] == "https://eips.ethereum.org/EIPS/eip-1559"

    def test_eip_title(self) -> None:
        node = chunk_to_node(_eip_chunk(1559, title="EIP-1559: Fee Market"))
        assert node["title"] == "EIP-1559: Fee Market"


# ===================================================================
# Code chunk -> node
# ===================================================================


class TestCodeChunkToNode:
    def test_function_type(self) -> None:
        node = chunk_to_node(_code_chunk(symbol_kind="function"))
        assert node["node_type"] == "code_function"

    def test_method_type(self) -> None:
        node = chunk_to_node(_code_chunk(symbol_kind="method"))
        assert node["node_type"] == "code_function"

    def test_struct_type(self) -> None:
        node = chunk_to_node(_code_chunk(
            symbol="Block",
            symbol_kind="struct",
            chunk_kind=ChunkKind.CODE_STRUCT,
        ))
        assert node["node_type"] == "code_struct"

    def test_enum_type(self) -> None:
        node = chunk_to_node(_code_chunk(
            symbol="Slot",
            symbol_kind="enum",
            chunk_kind=ChunkKind.CODE_STRUCT,
            language=Language.RUST,
        ))
        assert node["node_type"] == "code_enum"

    def test_trait_type(self) -> None:
        node = chunk_to_node(_code_chunk(
            symbol="Validator",
            symbol_kind="trait",
            chunk_kind=ChunkKind.CODE_STRUCT,
            language=Language.RUST,
        ))
        assert node["node_type"] == "code_trait"

    def test_impl_type(self) -> None:
        node = chunk_to_node(_code_chunk(
            symbol="ValidatorImpl",
            symbol_kind="impl",
            chunk_kind=ChunkKind.CODE_STRUCT,
            language=Language.RUST,
        ))
        assert node["node_type"] == "code_impl"

    def test_class_type(self) -> None:
        node = chunk_to_node(_code_chunk(
            symbol="StateProcessor",
            symbol_kind="class",
            chunk_kind=ChunkKind.CODE_STRUCT,
            language=Language.PYTHON,
        ))
        assert node["node_type"] == "code_class"

    def test_code_group_type(self) -> None:
        node = chunk_to_node(_code_chunk(
            symbol="helper",
            symbol_kind="function",
            chunk_kind=ChunkKind.CODE_GROUP,
            member_symbols=["helper_a", "helper_b"],
        ))
        assert node["node_type"] == "code_function"

    def test_unknown_symbol_kind_fallback(self) -> None:
        """Unknown symbol_kind should fall back to code_function."""
        node = chunk_to_node(_code_chunk(symbol_kind="unknown"))
        assert node["node_type"] == "code_function"

    def test_node_id_matches_chunk(self) -> None:
        chunk = _code_chunk(repo="geth", file_path="vm.go", symbol="Run")
        node = chunk_to_node(chunk)
        assert node["node_id"] == chunk.node_id

    def test_code_core_fields(self) -> None:
        chunk = _code_chunk(repo="go-ethereum", file_path="core/vm/run.go", symbol="Run")
        node = chunk_to_node(chunk)
        assert node["source_name"] == "go-ethereum"
        assert node["repository"] == "go-ethereum"
        assert node["language"] == "go"
        assert node["file_path"] == "core/vm/run.go"
        assert node["symbol_name"] == "Run"
        assert node["symbol_kind"] == "function"

    def test_metadata_signature(self) -> None:
        node = chunk_to_node(_code_chunk(signature="func Run() error"))
        meta = json.loads(node["metadata_json"])
        assert meta["signature"] == "func Run() error"

    def test_metadata_parent_symbol(self) -> None:
        node = chunk_to_node(_code_chunk(parent_symbol="EVMInterpreter"))
        meta = json.loads(node["metadata_json"])
        assert meta["parent_symbol"] == "EVMInterpreter"

    def test_metadata_module_path(self) -> None:
        node = chunk_to_node(_code_chunk(module_path="core/vm"))
        meta = json.loads(node["metadata_json"])
        assert meta["module_path"] == "core/vm"

    def test_metadata_visibility(self) -> None:
        node = chunk_to_node(_code_chunk(visibility="public"))
        meta = json.loads(node["metadata_json"])
        assert meta["visibility"] == "public"

    def test_metadata_member_symbols(self) -> None:
        node = chunk_to_node(_code_chunk(
            chunk_kind=ChunkKind.CODE_GROUP,
            member_symbols=["a", "b", "c"],
        ))
        meta = json.loads(node["metadata_json"])
        assert meta["member_symbols"] == ["a", "b", "c"]

    def test_metadata_empty_when_no_optional_code_fields(self) -> None:
        node = chunk_to_node(_code_chunk(
            signature="",
            parent_symbol="",
            module_path="",
            visibility="",
            member_symbols=[],
        ))
        meta = json.loads(node["metadata_json"])
        assert meta == {}


# ===================================================================
# Section anchor
# ===================================================================


class TestSectionAnchor:
    def test_none_for_empty_heading_path(self) -> None:
        chunk = _eip_chunk(heading_path=[])
        node = chunk_to_node(chunk)
        assert node["section_anchor"] is None

    def test_uses_last_heading(self) -> None:
        chunk = _eip_chunk(heading_path=["Top", "Middle", "Bottom Section"])
        node = chunk_to_node(chunk)
        assert node["section_anchor"] == "bottom-section"

    def test_single_heading(self) -> None:
        chunk = _eip_chunk(heading_path=["Abstract"])
        node = chunk_to_node(chunk)
        assert node["section_anchor"] == "abstract"


# ===================================================================
# content_hash in node
# ===================================================================


class TestContentHashInNode:
    def test_content_hash_present(self) -> None:
        chunk = _forum_chunk()
        node = chunk_to_node(chunk)
        assert node["content_hash"] == chunk.content_hash
        assert len(node["content_hash"]) == 16

    def test_content_hash_deterministic(self) -> None:
        chunk = _forum_chunk()
        node1 = chunk_to_node(chunk)
        node2 = chunk_to_node(chunk)
        assert node1["content_hash"] == node2["content_hash"]


# ===================================================================
# All node fields populated
# ===================================================================


class TestAllFieldsPopulated:
    def test_all_keys_present(self) -> None:
        """Every node dict should have all expected keys."""
        expected_keys = {
            "node_id", "node_type", "source_name", "repository",
            "language", "file_path", "chunk_id", "title", "url",
            "eip", "section_anchor", "symbol_name", "symbol_kind",
            "start_line", "end_line", "content_hash", "metadata_json",
        }
        for chunk in [_forum_chunk(), _eip_chunk(), _code_chunk()]:
            node = chunk_to_node(chunk)
            assert set(node.keys()) == expected_keys, (
                f"Missing keys for {chunk.source_kind}: "
                f"{expected_keys - set(node.keys())}"
            )

    def test_metadata_json_is_valid_json(self) -> None:
        for chunk in [_forum_chunk(), _eip_chunk(), _code_chunk()]:
            node = chunk_to_node(chunk)
            # Should not raise
            parsed = json.loads(node["metadata_json"])
            assert isinstance(parsed, dict)

    def test_title_none_when_empty(self) -> None:
        chunk = _eip_chunk()
        chunk.title = ""
        node = chunk_to_node(chunk)
        assert node["title"] is None

    def test_repository_none_for_forum(self) -> None:
        node = chunk_to_node(_forum_chunk())
        assert node["repository"] is None

    def test_repository_set_for_code(self) -> None:
        node = chunk_to_node(_code_chunk(repo="go-ethereum"))
        assert node["repository"] == "go-ethereum"
