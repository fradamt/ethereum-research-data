"""Tests for Meilisearch document builder."""

from __future__ import annotations

from erd_index.index.document_builder import (
    chunk_to_document,
    chunks_to_documents,
    sanitize_chunk_id,
    sanitize_text,
)
from erd_index.models import Chunk, ChunkKind, Language, SourceKind

SCHEMA_VERSION = 1


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
        research_thread="danksharding",
        views=5000,
        likes=42,
        posts_count=15,
        influence_score=0.95,
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
        eip_type="Core",
        eip_category="Core",
        requires_eips=[1559, 4895],
        heading_path=["EIP-4844", "Abstract"],
        tags=["dencun", "blobs"],
        mentions_eips=[1559],
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
        text="func (in *EVMInterpreter) Run(contract *Contract) ([]byte, error) {",
        start_line=100,
        end_line=150,
        symbol_name="Run",
        symbol_kind="method",
        symbol_qualname="EVMInterpreter.Run",
        signature="func (in *EVMInterpreter) Run(contract *Contract) ([]byte, error)",
        parent_symbol="EVMInterpreter",
        module_path="core/vm",
        visibility="public",
        imports=["math/big", "github.com/ethereum/go-ethereum/common"],
        used_imports=["math/big"],
        calls=["contract.GetOp", "in.cfg.Tracer.CaptureState"],
    )
    defaults.update(overrides)
    return Chunk(**defaults)


# ---------------------------------------------------------------------------
# Forum chunk -> document
# ---------------------------------------------------------------------------


class TestForumDocument:
    def test_core_fields(self) -> None:
        chunk = _forum_chunk()
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        # Meilisearch IDs are sanitized (: -> -, / -> _)
        expected_id = chunk.chunk_id.replace(":", "-").replace("/", "_").replace(".", "_")
        assert doc["id"] == expected_id
        assert doc["doc_id"] == "forum:ethresearch:1234"
        assert doc["schema_version"] == SCHEMA_VERSION
        assert doc["source_kind"] == "forum"
        assert doc["chunk_kind"] == "md_heading"
        assert doc["language"] == "markdown"
        assert doc["text"] == chunk.text
        assert doc["start_line"] == 1
        assert doc["end_line"] == 10
        assert doc["content_hash"] == chunk.content_hash
        assert doc["dedupe_key"] == chunk.dedupe_key
        assert doc["text_length"] == len(chunk.text)
        assert "indexed_at_ts" in doc

    def test_forum_fields(self) -> None:
        doc = chunk_to_document(_forum_chunk(), SCHEMA_VERSION)
        assert doc["topic_id"] == 1234
        assert doc["post_number"] == 1
        assert doc["author"] == "vbuterin"
        assert doc["category"] == "Sharding"
        assert doc["research_thread"] == "danksharding"
        assert doc["views"] == 5000
        assert doc["likes"] == 42
        assert doc["posts_count"] == 15
        assert doc["influence_score"] == 0.95

    def test_optional_fields_present(self) -> None:
        doc = chunk_to_document(_forum_chunk(), SCHEMA_VERSION)
        assert doc["source_name"] == "ethresearch"
        assert doc["path"] == "topics/1234.md"
        assert doc["title"] == "Proto-danksharding FAQ"


# ---------------------------------------------------------------------------
# EIP chunk -> document
# ---------------------------------------------------------------------------


class TestEipDocument:
    def test_eip_fields(self) -> None:
        doc = chunk_to_document(_eip_chunk(), SCHEMA_VERSION)
        assert doc["eip"] == 4844
        assert doc["eip_status"] == "Final"
        assert doc["eip_type"] == "Core"
        assert doc["eip_category"] == "Core"
        assert doc["requires_eips"] == [1559, 4895]
        assert doc["heading_path"] == ["EIP-4844", "Abstract"]
        assert doc["tags"] == ["dencun", "blobs"]
        assert doc["mentions_eips"] == [1559]

    def test_doc_id(self) -> None:
        doc = chunk_to_document(_eip_chunk(), SCHEMA_VERSION)
        assert doc["doc_id"] == "eip:4844"

    def test_no_code_fields(self) -> None:
        doc = chunk_to_document(_eip_chunk(), SCHEMA_VERSION)
        assert "symbol_name" not in doc
        assert "symbol_kind" not in doc
        assert "imports" not in doc


# ---------------------------------------------------------------------------
# Code chunk -> document
# ---------------------------------------------------------------------------


class TestCodeDocument:
    def test_code_fields(self) -> None:
        doc = chunk_to_document(_code_chunk(), SCHEMA_VERSION)
        assert doc["symbol_name"] == "Run"
        assert doc["symbol_kind"] == "method"
        assert doc["symbol_qualname"] == "EVMInterpreter.Run"
        assert doc["signature"].startswith("func (in *EVMInterpreter)")
        assert doc["parent_symbol"] == "EVMInterpreter"
        assert doc["module_path"] == "core/vm"
        assert doc["visibility"] == "public"
        assert doc["imports"] == ["math/big", "github.com/ethereum/go-ethereum/common"]
        assert doc["used_imports"] == ["math/big"]
        assert doc["calls"] == ["contract.GetOp", "in.cfg.Tracer.CaptureState"]

    def test_symbol_id(self) -> None:
        doc = chunk_to_document(_code_chunk(), SCHEMA_VERSION)
        assert "symbol_id" in doc
        assert doc["symbol_id"] == doc["node_id"]

    def test_doc_id(self) -> None:
        doc = chunk_to_document(_code_chunk(), SCHEMA_VERSION)
        assert doc["doc_id"] == "code:go-ethereum:core/vm/interpreter.go"
        assert doc["repository"] == "go-ethereum"

    def test_no_forum_fields(self) -> None:
        doc = chunk_to_document(_code_chunk(), SCHEMA_VERSION)
        assert "topic_id" not in doc
        assert "author" not in doc
        assert "views" not in doc


# ---------------------------------------------------------------------------
# Empty/None field omission
# ---------------------------------------------------------------------------


class TestFieldOmission:
    def test_empty_strings_omitted(self) -> None:
        chunk = _forum_chunk(
            title="",
            url="",
            summary="",
            author="",
            category="",
            research_thread="",
        )
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "title" not in doc
        assert "url" not in doc
        assert "summary" not in doc
        assert "author" not in doc
        assert "category" not in doc
        assert "research_thread" not in doc

    def test_empty_lists_omitted(self) -> None:
        chunk = _eip_chunk(
            heading_path=[],
            tags=[],
            mentions_eips=[],
            requires_eips=[],
            supersedes_eips=[],
            replaces_eips=[],
        )
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "heading_path" not in doc
        assert "tags" not in doc
        assert "mentions_eips" not in doc
        assert "requires_eips" not in doc
        assert "supersedes_eips" not in doc
        assert "replaces_eips" not in doc

    def test_zero_numeric_fields_omitted(self) -> None:
        chunk = _forum_chunk(views=0, likes=0, posts_count=0, influence_score=0.0)
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "views" not in doc
        assert "likes" not in doc
        assert "posts_count" not in doc
        assert "influence_score" not in doc

    def test_none_topic_id_omitted(self) -> None:
        chunk = _forum_chunk(topic_id=None, post_number=None)
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "topic_id" not in doc
        assert "post_number" not in doc

    def test_none_eip_omitted(self) -> None:
        chunk = _code_chunk()
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "eip" not in doc

    def test_no_symbol_id_without_symbol_name(self) -> None:
        chunk = _forum_chunk()
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "symbol_id" not in doc


# ---------------------------------------------------------------------------
# chunk_id as document id
# ---------------------------------------------------------------------------


class TestDocumentId:
    def test_chunk_id_used(self) -> None:
        chunk = _forum_chunk()
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        expected_id = chunk.chunk_id.replace(":", "-").replace("/", "_").replace(".", "_")
        assert doc["id"] == expected_id

    def test_deterministic(self) -> None:
        chunk = _forum_chunk()
        doc1 = chunk_to_document(chunk, SCHEMA_VERSION)
        doc2 = chunk_to_document(chunk, SCHEMA_VERSION)
        assert doc1["id"] == doc2["id"]


# ---------------------------------------------------------------------------
# schema_version and indexed_at_ts
# ---------------------------------------------------------------------------


class TestMetaFields:
    def test_schema_version(self) -> None:
        doc = chunk_to_document(_forum_chunk(), 42)
        assert doc["schema_version"] == 42

    def test_indexed_at_ts_is_int(self) -> None:
        doc = chunk_to_document(_forum_chunk(), SCHEMA_VERSION)
        assert isinstance(doc["indexed_at_ts"], int)
        assert doc["indexed_at_ts"] > 0


# ---------------------------------------------------------------------------
# chunks_to_documents batch
# ---------------------------------------------------------------------------


class TestBatch:
    def test_batch_conversion(self) -> None:
        chunks = [_forum_chunk(), _eip_chunk(), _code_chunk()]
        docs = chunks_to_documents(chunks, SCHEMA_VERSION)
        assert len(docs) == 3
        assert docs[0]["source_kind"] == "forum"
        assert docs[1]["source_kind"] == "eip"
        assert docs[2]["source_kind"] == "code"

    def test_empty_batch(self) -> None:
        assert chunks_to_documents([], SCHEMA_VERSION) == []


# ---------------------------------------------------------------------------
# Split metadata
# ---------------------------------------------------------------------------


class TestSplitMetadata:
    def test_part_fields_included(self) -> None:
        chunk = _code_chunk(part_index=0, part_count=3)
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert doc["part_index"] == 0
        assert doc["part_count"] == 3

    def test_part_fields_omitted_when_none(self) -> None:
        chunk = _code_chunk()
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "part_index" not in doc
        assert "part_count" not in doc


# ---------------------------------------------------------------------------
# sanitize_chunk_id
# ---------------------------------------------------------------------------


class TestSanitizeChunkId:
    def test_colons_replaced(self) -> None:
        assert sanitize_chunk_id("forum:ethresearch:1234") == "forum-ethresearch-1234"

    def test_slashes_replaced(self) -> None:
        assert sanitize_chunk_id("code/path/to/file") == "code_path_to_file"

    def test_dots_replaced(self) -> None:
        assert sanitize_chunk_id("eip-4844.md") == "eip-4844_md"

    def test_all_special_chars(self) -> None:
        raw = "eips:eip-4844.md:1:20:abcdef0123456789"
        expected = "eips-eip-4844_md-1-20-abcdef0123456789"
        assert sanitize_chunk_id(raw) == expected

    def test_special_chars_replaced(self) -> None:
        """Characters outside [A-Za-z0-9_-] are replaced with underscores."""
        assert sanitize_chunk_id("path+with@special=chars") == "path_with_special_chars"
        assert sanitize_chunk_id("file (copy).md") == "file__copy__md"
        assert sanitize_chunk_id("a#b&c") == "a_b_c"

    def test_unicode_replaced(self) -> None:
        assert sanitize_chunk_id("eip-café") == "eip-caf_"

    def test_matches_document_id(self) -> None:
        chunk = _eip_chunk()
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert doc["id"] == sanitize_chunk_id(chunk.chunk_id)

    def test_result_only_contains_valid_chars(self) -> None:
        """The sanitized ID must match the Meilisearch ID regex."""
        import re

        raw = "forum:ethresearch:path/to/@types/file+name.md:1:20:abc123"
        result = sanitize_chunk_id(raw)
        assert re.fullmatch(r"[A-Za-z0-9_-]+", result), f"Invalid ID chars in: {result}"


# ---------------------------------------------------------------------------
# sanitize_text
# ---------------------------------------------------------------------------


class TestSanitizeText:
    def test_preserves_normal_text(self) -> None:
        assert sanitize_text("Hello, world!") == "Hello, world!"

    def test_preserves_newlines(self) -> None:
        assert sanitize_text("line1\nline2\n") == "line1\nline2\n"

    def test_preserves_tabs(self) -> None:
        assert sanitize_text("\tindented\t") == "\tindented\t"

    def test_preserves_carriage_returns(self) -> None:
        assert sanitize_text("line1\r\nline2") == "line1\r\nline2"

    def test_strips_null(self) -> None:
        assert sanitize_text("hello\x00world") == "helloworld"

    def test_strips_bell(self) -> None:
        assert sanitize_text("alert\x07!") == "alert!"

    def test_strips_backspace(self) -> None:
        assert sanitize_text("back\x08space") == "backspace"

    def test_strips_vertical_tab(self) -> None:
        assert sanitize_text("line1\x0bline2") == "line1line2"

    def test_strips_form_feed(self) -> None:
        assert sanitize_text("page\x0cbreak") == "pagebreak"

    def test_strips_escape(self) -> None:
        assert sanitize_text("esc\x1b[0m") == "esc[0m"

    def test_strips_all_c0_except_whitespace(self) -> None:
        # Build a string with all C0 control chars (0x00-0x1F)
        all_c0 = "".join(chr(i) for i in range(0x20))
        result = sanitize_text(all_c0)
        # Only tab (0x09), newline (0x0A), carriage return (0x0D) survive
        assert result == "\t\n\r"

    def test_hex_code_with_embedded_nulls(self) -> None:
        # Simulates code chunks like TestPush that can have weird bytes
        code = "code := common.FromHex(\"0011\x002233\")"
        result = sanitize_text(code)
        assert "\x00" not in result
        assert "0011" in result and "2233" in result

    def test_applied_in_chunk_to_document(self) -> None:
        chunk = _code_chunk(text="func main() {\x00\n\treturn\n}")
        doc = chunk_to_document(chunk, SCHEMA_VERSION)
        assert "\x00" not in doc["text"]
        assert doc["text"] == "func main() {\n\treturn\n}"

    def test_empty_string(self) -> None:
        assert sanitize_text("") == ""

    def test_unicode_preserved(self) -> None:
        assert sanitize_text("Vitalik Buterin \u2014 Ethereum") == "Vitalik Buterin \u2014 Ethereum"
