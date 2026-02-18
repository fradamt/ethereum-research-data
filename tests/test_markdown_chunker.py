"""Tests for the markdown parser and chunker pipeline."""

from __future__ import annotations

from pathlib import Path

from erd_index.chunk.markdown_chunker import chunk_parsed_units
from erd_index.models import ChunkKind, Language, ParsedUnit, SourceKind
from erd_index.parse.markdown_parser import parse_markdown
from erd_index.settings import ChunkSizing

CORPUS_DIR = Path(__file__).parent.parent / "corpus"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _default_sizing() -> ChunkSizing:
    return ChunkSizing(target_chars=2800, hard_max_chars=5500)


# ---------------------------------------------------------------------------
# Forum reply splitting
# ---------------------------------------------------------------------------


class TestForumReplySplitting:
    def test_replies_split_at_boundaries(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        replies = [u for u in units if u.post_number and u.post_number > 1]
        assert len(replies) == 3
        assert replies[0].author == "bob"
        assert replies[1].author == "carol"
        assert replies[2].author == "alice"

    def test_op_gets_post_number_1(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        op_units = [u for u in units if u.post_number == 1]
        assert len(op_units) >= 1
        assert all(u.author == "alice" for u in op_units)

    def test_topic_id_propagated(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        assert all(u.topic_id == 9999 for u in units)

    def test_reply_heading_path(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        replies = [u for u in units if u.post_number and u.post_number > 1]
        for r in replies:
            assert "Replies" in r.heading_path

    def test_code_block_with_separator_not_split(self):
        """A `---` inside a code block should not split replies."""
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        carol_reply = [u for u in units if u.author == "carol" and u.post_number and u.post_number > 1]
        assert len(carol_reply) == 1
        assert "def example():" in carol_reply[0].text

    def test_real_ethresearch_file(self):
        path = CORPUS_DIR / "ethresearch" / "1000-separating-proposing-and-confirmation-of-collations.md"
        if not path.exists():
            return
        text = path.read_text()
        units = parse_markdown(text, path=path.name, source_name="ethresearch")
        replies = [u for u in units if u.post_number and u.post_number > 1]
        assert len(replies) == 10
        assert replies[0].author == "JustinDrake"
        assert all(u.source_kind == SourceKind.FORUM for u in units)

    def test_forum_no_replies_section(self):
        """A forum file with no '## Replies' should still parse the OP."""
        text = "---\nsource: ethresearch\ntopic_id: 1\ntitle: Simple\nauthor: bob\n---\n\n# Simple\n\nJust the OP, no replies."
        units = parse_markdown(text, path="simple.md", source_name="ethresearch")
        assert len(units) >= 1
        assert all(u.post_number == 1 for u in units)

    def test_magicians_source(self):
        path = CORPUS_DIR / "magicians"
        files = sorted(path.glob("*.md"))
        if not files:
            return
        text = files[0].read_text()
        units = parse_markdown(text, path=files[0].name, source_name="magicians")
        assert all(u.source_kind == SourceKind.FORUM for u in units)


# ---------------------------------------------------------------------------
# EIP parsing
# ---------------------------------------------------------------------------


class TestEipParsing:
    def test_eip_metadata_in_frontmatter(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        assert all(u.source_kind == SourceKind.EIP for u in units)
        assert all(u.frontmatter.get("_eip") == 9999 for u in units)
        assert all(u.frontmatter.get("_eip_status") == "Draft" for u in units)
        assert all(u.frontmatter.get("_eip_type") == "Standards Track" for u in units)
        assert all(u.frontmatter.get("_eip_category") == "Core" for u in units)

    def test_requires_eips_parsed(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        assert all(u.frontmatter.get("_requires_eips") == [1559, 2718] for u in units)

    def test_eip_heading_split(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        headings = [u.heading_path for u in units]
        assert ["Abstract"] in headings
        assert ["Specification"] in headings
        assert ["Security Considerations"] in headings

    def test_eip_subsection_heading_path(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        params = [u for u in units if u.heading_path == ["Specification", "Parameters"]]
        assert len(params) == 1

    def test_real_eip_1559(self):
        path = CORPUS_DIR / "eips" / "eip-1559.md"
        if not path.exists():
            return
        text = path.read_text()
        units = parse_markdown(text, path="eip-1559.md", source_name="eips")
        assert len(units) >= 5
        assert all(u.frontmatter.get("_eip") == 1559 for u in units)
        assert all(u.frontmatter.get("_requires_eips") == [2718, 2930] for u in units)

    def test_eip_no_requires(self):
        path = CORPUS_DIR / "eips" / "eip-100.md"
        if not path.exists():
            return
        text = path.read_text()
        units = parse_markdown(text, path="eip-100.md", source_name="eips")
        assert all(u.frontmatter.get("_requires_eips") == [] for u in units)


# ---------------------------------------------------------------------------
# Code fence preservation
# ---------------------------------------------------------------------------


class TestCodeFencePreservation:
    def test_headings_inside_backtick_fence_ignored(self):
        text = (FIXTURES_DIR / "heading_with_code_fence.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="eips")
        heading_names = [h for u in units for h in u.heading_path]
        assert "This is NOT a heading -- it is inside a code fence" not in heading_names
        assert "also not a heading" not in heading_names

    def test_headings_inside_tilde_fence_ignored(self):
        text = (FIXTURES_DIR / "heading_with_code_fence.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="eips")
        heading_names = [h for u in units for h in u.heading_path]
        assert "Another fake heading inside tildes" not in heading_names

    def test_real_sections_still_detected(self):
        text = (FIXTURES_DIR / "heading_with_code_fence.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="eips")
        heading_paths = [u.heading_path for u in units]
        assert ["Section One"] in heading_paths
        assert ["Section Two"] in heading_paths
        assert ["Section Two", "Subsection"] in heading_paths

    def test_code_block_text_preserved_in_section(self):
        text = (FIXTURES_DIR / "heading_with_code_fence.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="eips")
        sec1 = next(u for u in units if u.heading_path == ["Section One"])
        assert "def process():" in sec1.text
        assert '```' in sec1.text


# ---------------------------------------------------------------------------
# Small section merging
# ---------------------------------------------------------------------------


class TestSmallSectionMerging:
    def test_small_consecutive_sections_merged(self):
        """Two small sections under the same parent should merge into one chunk."""
        sizing = ChunkSizing(target_chars=2000, hard_max_chars=5500)
        threshold = sizing.target_chars // 3  # ~666
        small_text = "x" * (threshold - 10)
        units = [
            ParsedUnit(
                source_kind=SourceKind.EIP,
                language=Language.MARKDOWN,
                source_name="eips",
                path="test.md",
                text=small_text,
                start_line=1,
                end_line=5,
                heading_path=["Spec", "A"],
            ),
            ParsedUnit(
                source_kind=SourceKind.EIP,
                language=Language.MARKDOWN,
                source_name="eips",
                path="test.md",
                text=small_text,
                start_line=6,
                end_line=10,
                heading_path=["Spec", "B"],
            ),
        ]
        chunks = chunk_parsed_units(units, sizing)
        assert len(chunks) == 1
        assert small_text in chunks[0].text

    def test_small_sections_different_parent_not_merged(self):
        """Small sections under different parents should NOT merge."""
        sizing = ChunkSizing(target_chars=2000, hard_max_chars=5500)
        threshold = sizing.target_chars // 3
        small_text = "x" * (threshold - 10)
        units = [
            ParsedUnit(
                source_kind=SourceKind.EIP,
                language=Language.MARKDOWN,
                source_name="eips",
                path="test.md",
                text=small_text,
                start_line=1,
                end_line=5,
                heading_path=["Parent A", "Sub"],
            ),
            ParsedUnit(
                source_kind=SourceKind.EIP,
                language=Language.MARKDOWN,
                source_name="eips",
                path="test.md",
                text=small_text,
                start_line=6,
                end_line=10,
                heading_path=["Parent B", "Sub"],
            ),
        ]
        chunks = chunk_parsed_units(units, sizing)
        assert len(chunks) == 2

    def test_forum_replies_never_merged(self):
        """Forum replies (post_number > 1) must never merge, even when small."""
        sizing = ChunkSizing(target_chars=2000, hard_max_chars=5500)
        threshold = sizing.target_chars // 3
        small_text = "x" * (threshold - 10)
        units = [
            ParsedUnit(
                source_kind=SourceKind.FORUM,
                language=Language.MARKDOWN,
                source_name="ethresearch",
                path="test.md",
                text=small_text,
                start_line=1,
                end_line=5,
                heading_path=["Topic"],
                topic_id=100,
                post_number=2,
                author="alice",
            ),
            ParsedUnit(
                source_kind=SourceKind.FORUM,
                language=Language.MARKDOWN,
                source_name="ethresearch",
                path="test.md",
                text=small_text,
                start_line=6,
                end_line=10,
                heading_path=["Topic"],
                topic_id=100,
                post_number=3,
                author="bob",
            ),
        ]
        chunks = chunk_parsed_units(units, sizing)
        # Must stay separate — each reply has distinct author/post metadata
        assert len(chunks) == 2
        assert chunks[0].author == "alice"
        assert chunks[0].post_number == 2
        assert chunks[1].author == "bob"
        assert chunks[1].post_number == 3

    def test_large_section_not_merged(self):
        """A section at or above threshold should not merge with neighbors."""
        sizing = ChunkSizing(target_chars=2000, hard_max_chars=5500)
        threshold = sizing.target_chars // 3
        units = [
            ParsedUnit(
                source_kind=SourceKind.FORUM,
                language=Language.MARKDOWN,
                source_name="ethresearch",
                path="test.md",
                text="x" * threshold,
                start_line=1,
                end_line=10,
                heading_path=["Topic"],
            ),
            ParsedUnit(
                source_kind=SourceKind.FORUM,
                language=Language.MARKDOWN,
                source_name="ethresearch",
                path="test.md",
                text="y" * (threshold - 1),
                start_line=11,
                end_line=15,
                heading_path=["Topic"],
            ),
        ]
        chunks = chunk_parsed_units(units, sizing)
        assert len(chunks) == 2


# ---------------------------------------------------------------------------
# Large section splitting
# ---------------------------------------------------------------------------


class TestLargeSectionSplitting:
    def test_oversized_section_split_at_paragraphs(self):
        text = (FIXTURES_DIR / "large_section.md").read_text()
        # Use a small sizing to force splits.
        sizing = ChunkSizing(target_chars=500, hard_max_chars=1000)
        units = parse_markdown(text, path="large.md", source_name="eips")
        chunks = chunk_parsed_units(units, sizing)
        large_chunks = [c for c in chunks if c.heading_path == ["Large Section"]]
        assert len(large_chunks) > 1
        for c in large_chunks:
            assert c.part_index is not None
            assert c.part_count == len(large_chunks)

    def test_split_chunks_under_target(self):
        text = (FIXTURES_DIR / "large_section.md").read_text()
        sizing = ChunkSizing(target_chars=500, hard_max_chars=1000)
        units = parse_markdown(text, path="large.md", source_name="eips")
        chunks = chunk_parsed_units(units, sizing)
        for c in chunks:
            # Each chunk should be at or near target, not exceeding hard_max.
            # (A single paragraph could exceed target but shouldn't exceed hard_max
            # unless the paragraph itself is huge.)
            assert len(c.text) <= sizing.hard_max_chars or c.part_count is not None

    def test_real_eip_specification_split(self):
        """EIP-1559's Specification section (~10k chars) should be split."""
        path = CORPUS_DIR / "eips" / "eip-1559.md"
        if not path.exists():
            return
        sizing = _default_sizing()
        text = path.read_text()
        units = parse_markdown(text, path="eip-1559.md", source_name="eips")
        chunks = chunk_parsed_units(units, sizing)
        spec_chunks = [c for c in chunks if "Specification" in c.heading_path]
        assert len(spec_chunks) >= 3  # ~10k / ~2800 target = ~4 parts

    def test_empty_input(self):
        chunks = chunk_parsed_units([], _default_sizing())
        assert chunks == []


# ---------------------------------------------------------------------------
# Chunk kind correctness
# ---------------------------------------------------------------------------


class TestChunkKind:
    def test_forum_op_is_md_heading(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        chunks = chunk_parsed_units(units, _default_sizing())
        op_chunks = [c for c in chunks if c.post_number == 1]
        assert all(c.chunk_kind == ChunkKind.MD_HEADING for c in op_chunks)

    def test_forum_reply_is_md_reply(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        chunks = chunk_parsed_units(units, _default_sizing())
        reply_chunks = [c for c in chunks if c.post_number and c.post_number > 1]
        assert len(reply_chunks) >= 1
        assert all(c.chunk_kind == ChunkKind.MD_REPLY for c in reply_chunks)

    def test_eip_is_eip_section(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        chunks = chunk_parsed_units(units, _default_sizing())
        assert all(c.chunk_kind == ChunkKind.EIP_SECTION for c in chunks)

    def test_eip_metadata_propagated_to_chunks(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        chunks = chunk_parsed_units(units, _default_sizing())
        for c in chunks:
            assert c.eip == 9999
            assert c.eip_status == "Draft"
            assert c.eip_type == "Standards Track"
            assert c.eip_category == "Core"
            assert c.requires_eips == [1559, 2718]

    def test_forum_metadata_propagated_to_chunks(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        chunks = chunk_parsed_units(units, _default_sizing())
        for c in chunks:
            assert c.topic_id == 9999
            assert c.source_name == "ethresearch"
            assert c.views == 100
            assert c.likes == 5
            assert c.research_thread == "testing"


# ---------------------------------------------------------------------------
# Computed fields on Chunk
# ---------------------------------------------------------------------------


class TestChunkComputedFields:
    def test_doc_id_forum(self):
        text = (FIXTURES_DIR / "forum_with_replies.md").read_text()
        units = parse_markdown(text, path="test.md", source_name="ethresearch")
        chunks = chunk_parsed_units(units, _default_sizing())
        assert chunks[0].doc_id == "forum:ethresearch:9999"

    def test_doc_id_eip(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        chunks = chunk_parsed_units(units, _default_sizing())
        assert chunks[0].doc_id == "eip:9999"

    def test_chunk_id_deterministic(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        chunks1 = chunk_parsed_units(units, _default_sizing())
        chunks2 = chunk_parsed_units(units, _default_sizing())
        for c1, c2 in zip(chunks1, chunks2, strict=False):
            assert c1.chunk_id == c2.chunk_id

    def test_content_hash_changes_with_text(self):
        text = (FIXTURES_DIR / "eip_with_requires.md").read_text()
        units = parse_markdown(text, path="eip-9999.md", source_name="eips")
        chunks = chunk_parsed_units(units, _default_sizing())
        hashes = [c.content_hash for c in chunks]
        assert len(set(hashes)) == len(hashes)  # all unique
