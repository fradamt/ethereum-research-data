"""Tests for erd_index/models.py — Chunk computed fields and enums."""

from __future__ import annotations

import hashlib

from erd_index.models import (
    Chunk,
    ChunkKind,
    Language,
    ParsedUnit,
    SourceKind,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _forum_chunk(**overrides) -> Chunk:
    defaults = dict(
        source_kind=SourceKind.FORUM,
        chunk_kind=ChunkKind.MD_HEADING,
        source_name="ethresearch",
        language=Language.MARKDOWN,
        path="topics/1234.md",
        title="Proto-danksharding FAQ",
        text="This is the body of a forum post about EIP-4844.",
        start_line=1,
        end_line=10,
        topic_id=1234,
        post_number=1,
        author="vbuterin",
        category="Sharding",
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def _eip_chunk(**overrides) -> Chunk:
    defaults = dict(
        source_kind=SourceKind.EIP,
        chunk_kind=ChunkKind.EIP_SECTION,
        source_name="eips",
        language=Language.MARKDOWN,
        path="eip-4844.md",
        title="EIP-4844: Shard Blob Transactions",
        text="## Abstract\n\nIntroduce blob-carrying transactions.",
        start_line=1,
        end_line=20,
        eip=4844,
        eip_status="Final",
        heading_path=["EIP-4844", "Abstract"],
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def _code_chunk(**overrides) -> Chunk:
    defaults = dict(
        source_kind=SourceKind.CODE,
        chunk_kind=ChunkKind.CODE_FUNCTION,
        source_name="go-ethereum",
        repository="go-ethereum",
        language=Language.GO,
        path="core/vm/interpreter.go",
        text="func (in *EVMInterpreter) Run(contract *Contract) ([]byte, error) {}",
        start_line=100,
        end_line=150,
        symbol_name="Run",
        symbol_kind="method",
        symbol_qualname="EVMInterpreter.Run",
    )
    defaults.update(overrides)
    return Chunk(**defaults)


# ===================================================================
# SourceKind, ChunkKind, Language enum values
# ===================================================================


class TestEnums:
    def test_source_kind_values(self) -> None:
        assert SourceKind.FORUM.value == "forum"
        assert SourceKind.EIP.value == "eip"
        assert SourceKind.CODE.value == "code"
        assert SourceKind.GENERIC.value == "generic"

    def test_source_kind_is_str_enum(self) -> None:
        assert isinstance(SourceKind.FORUM, str)
        assert SourceKind.FORUM == "forum"

    def test_chunk_kind_values(self) -> None:
        assert ChunkKind.MD_HEADING.value == "md_heading"
        assert ChunkKind.MD_REPLY.value == "md_reply"
        assert ChunkKind.EIP_SECTION.value == "eip_section"
        assert ChunkKind.CODE_FUNCTION.value == "code_function"
        assert ChunkKind.CODE_STRUCT.value == "code_struct"
        assert ChunkKind.CODE_GROUP.value == "code_group"

    def test_chunk_kind_is_str_enum(self) -> None:
        assert isinstance(ChunkKind.MD_HEADING, str)
        assert ChunkKind.MD_HEADING == "md_heading"

    def test_language_values(self) -> None:
        assert Language.MARKDOWN.value == "markdown"
        assert Language.PYTHON.value == "python"
        assert Language.GO.value == "go"
        assert Language.RUST.value == "rust"

    def test_language_is_str_enum(self) -> None:
        assert isinstance(Language.GO, str)
        assert Language.GO == "go"


# ===================================================================
# content_hash
# ===================================================================


class TestContentHash:
    def test_deterministic(self) -> None:
        """Same text produces the same hash every time."""
        chunk = _forum_chunk()
        assert chunk.content_hash == chunk.content_hash

    def test_different_text_different_hash(self) -> None:
        a = _forum_chunk(text="hello world")
        b = _forum_chunk(text="goodbye world")
        assert a.content_hash != b.content_hash

    def test_normalized_strips_whitespace(self) -> None:
        """Leading/trailing whitespace is stripped before hashing."""
        a = _forum_chunk(text="  hello world  ")
        b = _forum_chunk(text="hello world")
        assert a.content_hash == b.content_hash

    def test_internal_whitespace_preserved(self) -> None:
        """Whitespace inside the text is NOT stripped."""
        a = _forum_chunk(text="hello  world")
        b = _forum_chunk(text="hello world")
        assert a.content_hash != b.content_hash

    def test_length_is_16_hex_chars(self) -> None:
        chunk = _forum_chunk()
        assert len(chunk.content_hash) == 16
        # All characters should be valid hex
        int(chunk.content_hash, 16)  # should not raise

    def test_matches_manual_sha256(self) -> None:
        text = "test content"
        chunk = _forum_chunk(text=text)
        expected = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]
        assert chunk.content_hash == expected

    def test_empty_text(self) -> None:
        """Empty string (after strip) still produces a valid hash."""
        chunk = _forum_chunk(text="   ")
        assert len(chunk.content_hash) == 16
        expected = hashlib.sha256(b"").hexdigest()[:16]
        assert chunk.content_hash == expected


# ===================================================================
# doc_id
# ===================================================================


class TestDocId:
    def test_forum_doc_id(self) -> None:
        chunk = _forum_chunk(source_name="ethresearch", topic_id=1234)
        assert chunk.doc_id == "forum:ethresearch:1234"

    def test_forum_doc_id_different_source(self) -> None:
        chunk = _forum_chunk(source_name="magicians", topic_id=567)
        assert chunk.doc_id == "forum:magicians:567"

    def test_eip_doc_id(self) -> None:
        chunk = _eip_chunk(eip=4844)
        assert chunk.doc_id == "eip:4844"

    def test_eip_doc_id_none_eip(self) -> None:
        """When eip is None, falls back to path-based ID."""
        chunk = _eip_chunk(eip=None)
        assert chunk.doc_id == f"eip:unknown:{chunk.path}"

    def test_code_doc_id(self) -> None:
        chunk = _code_chunk(repository="go-ethereum", path="core/vm/interpreter.go")
        assert chunk.doc_id == "code:go-ethereum:core/vm/interpreter.go"

    def test_code_doc_id_no_repository(self) -> None:
        """Code chunks with empty repository still use the source_kind prefix."""
        chunk = _code_chunk(repository="", path="main.go")
        assert chunk.doc_id == "code::main.go"

    def test_forum_doc_id_no_topic_id(self) -> None:
        """FORUM chunk with topic_id=None falls back to path-based doc_id."""
        chunk = Chunk(
            source_kind=SourceKind.FORUM,
            chunk_kind=ChunkKind.MD_HEADING,
            source_name="annotated-spec",
            language=Language.MARKDOWN,
            path="phase0/beacon-chain.md",
            text="test",
            start_line=1,
            end_line=1,
            topic_id=None,
        )
        assert chunk.doc_id == "doc:annotated-spec:phase0/beacon-chain.md"
        assert not chunk.doc_id.startswith("forum:")

    def test_generic_doc_id(self) -> None:
        """GENERIC source kind uses path-based doc_id."""
        chunk = Chunk(
            source_kind=SourceKind.GENERIC,
            chunk_kind=ChunkKind.MD_HEADING,
            source_name="vault",
            language=Language.MARKDOWN,
            path="research-notes.md",
            text="test",
            start_line=1,
            end_line=1,
        )
        assert chunk.doc_id == "doc:vault:research-notes.md"


# ===================================================================
# chunk_id
# ===================================================================


class TestChunkId:
    def test_format_without_part_index(self) -> None:
        chunk = _forum_chunk()
        parts = chunk.chunk_id.split(":")
        # source_name:path:start_line:end_line:content_hash
        assert parts[0] == "ethresearch"
        assert parts[1] == "topics/1234.md"
        assert parts[2] == "1"
        assert parts[3] == "10"
        assert parts[4] == chunk.content_hash

    def test_format_with_part_index(self) -> None:
        chunk = _code_chunk(part_index=2, part_count=5)
        chunk_id = chunk.chunk_id
        # Should contain "p2" before the content_hash
        assert ":p2:" in chunk_id

    def test_deterministic(self) -> None:
        chunk = _forum_chunk()
        assert chunk.chunk_id == chunk.chunk_id

    def test_different_text_different_id(self) -> None:
        """chunk_id includes content_hash, so different text -> different id."""
        a = _forum_chunk(text="hello")
        b = _forum_chunk(text="goodbye")
        assert a.chunk_id != b.chunk_id

    def test_different_line_range_different_id(self) -> None:
        a = _forum_chunk(start_line=1, end_line=10)
        b = _forum_chunk(start_line=1, end_line=20)
        assert a.chunk_id != b.chunk_id

    def test_part_index_none_vs_absent(self) -> None:
        """part_index=None should not include the 'p' segment."""
        chunk = _forum_chunk(part_index=None)
        assert ":p" not in chunk.chunk_id

    def test_part_index_zero(self) -> None:
        """part_index=0 should be included (it's not None)."""
        chunk = _code_chunk(part_index=0, part_count=3)
        assert ":p0:" in chunk.chunk_id


# ===================================================================
# dedupe_key
# ===================================================================


class TestDedupeKey:
    # --- Forum/EIP chunks: position-based, no content hash ---

    def test_forum_no_content_hash(self) -> None:
        """Forum dedupe_key should NOT include the content hash."""
        chunk = _forum_chunk()
        assert chunk.content_hash not in chunk.dedupe_key

    def test_forum_same_position_same_key(self) -> None:
        """Same logical position should produce the same dedupe_key even with different text."""
        a = _forum_chunk(text="version 1 of the post")
        b = _forum_chunk(text="version 2 of the post, edited")
        assert a.dedupe_key == b.dedupe_key

    def test_forum_different_position_different_key(self) -> None:
        a = _forum_chunk(start_line=1, end_line=10)
        b = _forum_chunk(start_line=11, end_line=20)
        assert a.dedupe_key != b.dedupe_key

    def test_forum_with_part_index(self) -> None:
        chunk = _forum_chunk(part_index=1, part_count=3)
        assert chunk.dedupe_key.endswith("p1")

    def test_forum_dedupe_key_is_prefix_of_chunk_id(self) -> None:
        """For forum chunks, chunk_id = dedupe_key + ':' + content_hash."""
        chunk = _forum_chunk()
        assert chunk.chunk_id == f"{chunk.dedupe_key}:{chunk.content_hash}"

    # --- Code chunks: symbol_qualname:content_hash ---

    def test_code_uses_qualname_and_hash(self) -> None:
        """Code dedupe_key should be symbol_qualname:content_hash."""
        chunk = _code_chunk()
        assert chunk.dedupe_key == f"{chunk.symbol_qualname}:{chunk.content_hash}"

    def test_code_same_function_same_content_same_key(self) -> None:
        """Identical function across forks should produce the same dedupe_key."""
        text = "func process_attestation(state, attestation) { ... }"
        a = _code_chunk(
            path="specs/altair/mainnet.py", text=text,
            symbol_qualname="process_attestation",
        )
        b = _code_chunk(
            path="specs/bellatrix/mainnet.py", text=text,
            symbol_qualname="process_attestation",
        )
        assert a.dedupe_key == b.dedupe_key

    def test_code_same_function_different_content_different_key(self) -> None:
        """Same function name with different content preserves both versions."""
        a = _code_chunk(
            text="func v1() { old }", symbol_qualname="process_attestation",
        )
        b = _code_chunk(
            text="func v2() { new }", symbol_qualname="process_attestation",
        )
        assert a.dedupe_key != b.dedupe_key

    def test_code_without_qualname_falls_back_to_position(self) -> None:
        """Code chunks without symbol_qualname use position-based key."""
        chunk = _code_chunk(symbol_qualname="", symbol_name="")
        assert chunk.source_name in chunk.dedupe_key
        assert chunk.path in chunk.dedupe_key

    def test_code_mainnet_vs_minimal_same_fork_dedupes(self) -> None:
        """mainnet.py and minimal.py in the same fork have identical content → same key."""
        text = "def get_base_reward(state, index): ..."
        a = _code_chunk(
            path="specs/altair/mainnet.py", text=text,
            symbol_qualname="get_base_reward",
        )
        b = _code_chunk(
            path="specs/altair/minimal.py", text=text,
            symbol_qualname="get_base_reward",
        )
        assert a.dedupe_key == b.dedupe_key

    def test_code_with_part_index_still_uses_content_hash(self) -> None:
        """Code chunks with part_index use qualname:content_hash (part_index is in chunk_id, not dedupe_key)."""
        chunk = _code_chunk(part_index=1, part_count=3)
        assert chunk.dedupe_key == f"{chunk.symbol_qualname}:{chunk.content_hash}"
        # part_index does NOT appear in the code dedupe_key
        assert "p1" not in chunk.dedupe_key

    def test_eip_uses_position_based_key(self) -> None:
        """EIP chunks always use position-based dedupe_key."""
        chunk = _eip_chunk()
        assert chunk.source_name in chunk.dedupe_key
        assert chunk.path in chunk.dedupe_key
        assert chunk.content_hash not in chunk.dedupe_key

    def test_eip_same_position_different_text_same_key(self) -> None:
        """EIP edits at the same position should dedup (position-based)."""
        a = _eip_chunk(text="## Abstract\n\nVersion 1")
        b = _eip_chunk(text="## Abstract\n\nVersion 2, updated")
        assert a.dedupe_key == b.dedupe_key

    def test_code_different_functions_different_key(self) -> None:
        """Different functions in the same file have different dedupe_keys."""
        a = _code_chunk(symbol_qualname="process_attestation", text="func a() {}")
        b = _code_chunk(symbol_qualname="process_deposit", text="func b() {}")
        assert a.dedupe_key != b.dedupe_key


# ===================================================================
# node_id
# ===================================================================


class TestNodeId:
    def test_code_chunk_uses_symbol_qualname(self) -> None:
        chunk = _code_chunk(
            repository="go-ethereum",
            path="core/vm/interpreter.go",
            symbol_name="Run",
            symbol_qualname="EVMInterpreter.Run",
        )
        assert chunk.node_id == "go-ethereum:core/vm/interpreter.go:EVMInterpreter.Run"

    def test_code_chunk_falls_back_to_symbol_name(self) -> None:
        """When symbol_qualname is empty, falls back to symbol_name."""
        chunk = _code_chunk(
            repository="go-ethereum",
            path="util.go",
            symbol_name="Helper",
            symbol_qualname="",
        )
        assert chunk.node_id == "go-ethereum:util.go:Helper"

    def test_eip_with_heading_path(self) -> None:
        chunk = _eip_chunk(eip=4844, heading_path=["EIP-4844", "Specification", "Gas Costs"])
        expected = "eip:4844:eip-4844/specification/gas-costs"
        assert chunk.node_id == expected

    def test_eip_heading_path_avoids_collisions(self) -> None:
        """Two sections named 'Parameters' under different parents should have different node_ids."""
        a = _eip_chunk(eip=4844, heading_path=["EIP-4844", "Consensus", "Parameters"])
        b = _eip_chunk(eip=4844, heading_path=["EIP-4844", "Execution", "Parameters"])
        assert a.node_id != b.node_id
        assert "consensus/parameters" in a.node_id
        assert "execution/parameters" in b.node_id

    def test_eip_without_heading_path(self) -> None:
        chunk = _eip_chunk(eip=1559, heading_path=[])
        assert chunk.node_id == "eip:1559"

    def test_forum_chunk_with_topic_id(self) -> None:
        chunk = _forum_chunk(source_name="ethresearch", topic_id=1234, post_number=3)
        assert chunk.node_id == "forum:ethresearch:1234:3"

    def test_forum_chunk_post_number_none(self) -> None:
        chunk = _forum_chunk(source_name="ethresearch", topic_id=1234, post_number=None)
        assert chunk.node_id == "forum:ethresearch:1234:0"

    def test_fallback_node_id(self) -> None:
        """Chunk with no symbol, no eip, no topic_id uses fallback."""
        chunk = Chunk(
            source_kind=SourceKind.CODE,
            chunk_kind=ChunkKind.CODE_FUNCTION,
            source_name="misc",
            language=Language.PYTHON,
            path="script.py",
            text="some code",
            start_line=42,
            end_line=50,
        )
        assert chunk.node_id == "misc:script.py:42"

    def test_eip_heading_path_kebab_case(self) -> None:
        """Heading path elements are lowercased and spaces replaced with hyphens."""
        chunk = _eip_chunk(eip=100, heading_path=["My EIP", "Some Section"])
        assert chunk.node_id == "eip:100:my-eip/some-section"


# ===================================================================
# ParsedUnit (basic construction)
# ===================================================================


class TestParsedUnit:
    def test_basic_construction(self) -> None:
        unit = ParsedUnit(
            source_kind=SourceKind.FORUM,
            language=Language.MARKDOWN,
            source_name="ethresearch",
            path="topics/1.md",
            text="Hello",
            start_line=1,
            end_line=5,
        )
        assert unit.source_kind == SourceKind.FORUM
        assert unit.text == "Hello"

    def test_default_fields(self) -> None:
        unit = ParsedUnit(
            source_kind=SourceKind.CODE,
            language=Language.GO,
            source_name="geth",
            path="main.go",
            text="package main",
            start_line=1,
            end_line=1,
        )
        assert unit.heading_path == []
        assert unit.symbol_name == ""
        assert unit.imports == []
        assert unit.topic_id is None
        assert unit.frontmatter == {}
        assert unit.repository == ""
        assert unit.title == ""


# ===================================================================
# Chunk default values
# ===================================================================


class TestChunkDefaults:
    def test_optional_fields_default(self) -> None:
        chunk = Chunk(
            source_kind=SourceKind.FORUM,
            chunk_kind=ChunkKind.MD_HEADING,
            source_name="test",
            language=Language.MARKDOWN,
            path="test.md",
            text="content",
            start_line=1,
            end_line=5,
        )
        assert chunk.eip is None
        assert chunk.topic_id is None
        assert chunk.part_index is None
        assert chunk.part_count is None
        assert chunk.tags == []
        assert chunk.mentions_eips == []
        assert chunk.requires_eips == []
        assert chunk.supersedes_eips == []
        assert chunk.replaces_eips == []
        assert chunk.views == 0
        assert chunk.likes == 0
        assert chunk.influence_score == 0.0
        assert chunk.url == ""
        assert chunk.summary == ""
        assert chunk.source_date == ""
        assert chunk.source_date_ts == 0
