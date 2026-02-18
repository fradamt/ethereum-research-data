"""Tests for code chunking: normal, large split, small grouping."""

from __future__ import annotations

from erd_index.chunk.code_chunker import chunk_code_units
from erd_index.chunk.group_small_units import group_small_units, is_small
from erd_index.chunk.split_large_units import split_large_unit
from erd_index.models import ChunkKind, Language, ParsedUnit, SourceKind
from erd_index.settings import ChunkSizing


def _make_unit(
    name: str,
    text: str,
    *,
    parent: str = "",
    kind: str = "function",
    start_line: int = 1,
) -> ParsedUnit:
    """Helper to create a ParsedUnit for testing."""
    lines = text.count("\n") + 1
    return ParsedUnit(
        source_kind=SourceKind.CODE,
        language=Language.PYTHON,
        source_name="test",
        repository="test-repo",
        path="test/module.py",
        text=text,
        start_line=start_line,
        end_line=start_line + lines - 1,
        symbol_name=name,
        symbol_kind=kind,
        symbol_qualname=f"test.module.{name}",
        signature=f"def {name}():",
        parent_symbol=parent,
        module_path="test.module",
        imports=["import os"],
        docstring=f"Doc for {name}.",
    )


# ---------------------------------------------------------------------------
# Normal-sized function -> single chunk
# ---------------------------------------------------------------------------


class TestNormalChunking:
    def test_single_function_becomes_one_chunk(self):
        # ~800 chars, well within hard_max (5500) and above small threshold (450).
        body = "\n".join(f"    x_{i} = compute({i})" for i in range(30))
        text = f"def process():\n    '''Do stuff.'''\n{body}"
        unit = _make_unit("process", text)
        sizing = ChunkSizing()

        chunks = chunk_code_units([unit], sizing)

        code_fn_chunks = [c for c in chunks if c.chunk_kind == ChunkKind.CODE_FUNCTION]
        assert len(code_fn_chunks) == 1
        chunk = code_fn_chunks[0]
        assert chunk.symbol_name == "process"
        assert chunk.symbol_qualname == "test.module.process"
        assert chunk.imports == ["import os"]
        assert chunk.part_index is None
        assert chunk.part_count is None

    def test_struct_kind_for_class(self):
        # Class body must be large enough to avoid being classified as "small"
        # (>450 chars or >12 lines).
        body = "\n".join(f"    attr_{i}: int = {i}" for i in range(15))
        text = f"class Foo:\n{body}"
        unit = _make_unit("Foo", text, kind="class")

        chunks = chunk_code_units([unit], ChunkSizing())

        struct_chunks = [c for c in chunks if c.chunk_kind == ChunkKind.CODE_STRUCT]
        assert len(struct_chunks) >= 1
        assert struct_chunks[0].symbol_name == "Foo"

    def test_metadata_preserved(self):
        body = "\n".join(f"    step({i})" for i in range(25))
        text = f"def run():\n{body}"
        unit = _make_unit("run", text)

        chunks = chunk_code_units([unit], ChunkSizing())

        code_fn = [c for c in chunks if c.chunk_kind == ChunkKind.CODE_FUNCTION]
        assert len(code_fn) == 1
        c = code_fn[0]
        assert c.source_kind == SourceKind.CODE
        assert c.language == Language.PYTHON
        assert c.repository == "test-repo"
        assert c.path == "test/module.py"
        assert c.module_path == "test.module"
        assert c.parent_symbol == ""


# ---------------------------------------------------------------------------
# Large function -> split into parts
# ---------------------------------------------------------------------------


class TestLargeFunctionSplitting:
    def _make_large_unit(self, char_count: int = 8000) -> ParsedUnit:
        """Create a function that exceeds hard_max_chars."""
        lines = []
        while len("\n".join(lines)) < char_count:
            i = len(lines)
            lines.append(f"    result_{i} = compute_step({i}, data[{i}], config)")
            lines.append(f"    if result_{i} is None:")
            lines.append(f'        raise ValueError("Step {i} failed")')
        body = "\n".join(lines)
        text = f'def process_all(data, config):\n    """Process all steps."""\n{body}'
        return _make_unit("process_all", text)

    def test_large_function_is_split(self):
        unit = self._make_large_unit(8000)
        sizing = ChunkSizing()
        assert len(unit.text) > sizing.hard_max_chars

        chunks = chunk_code_units([unit], sizing)

        assert len(chunks) >= 2
        for c in chunks:
            assert c.chunk_kind == ChunkKind.CODE_FUNCTION

    def test_part_index_and_count(self):
        unit = self._make_large_unit(8000)
        sizing = ChunkSizing()

        chunks = chunk_code_units([unit], sizing)

        total = len(chunks)
        for i, c in enumerate(chunks):
            assert c.part_index == i
            assert c.part_count == total

    def test_signature_preserved_in_all_parts(self):
        unit = self._make_large_unit(8000)
        sizing = ChunkSizing()

        chunks = chunk_code_units([unit], sizing)

        for c in chunks:
            assert "def process_all" in c.text

    def test_docstring_preserved_in_all_parts(self):
        unit = self._make_large_unit(8000)
        sizing = ChunkSizing()

        chunks = chunk_code_units([unit], sizing)

        # The header rebuilds docstring from ParsedUnit.docstring field.
        for c in chunks:
            assert "Doc for process_all." in c.text

    def test_parts_within_size_limits(self):
        unit = self._make_large_unit(12000)
        sizing = ChunkSizing()

        chunks = chunk_code_units([unit], sizing)

        # Each part should be roughly around target_chars, not exceeding
        # hard_max by too much (the header is prepended so some slack is ok).
        for c in chunks:
            assert len(c.text) < sizing.hard_max_chars * 2

    def test_split_directly(self):
        unit = self._make_large_unit(8000)
        sizing = ChunkSizing()

        chunks = split_large_unit(unit, sizing)

        assert len(chunks) >= 2
        assert all(c.part_count == len(chunks) for c in chunks)
        assert [c.part_index for c in chunks] == list(range(len(chunks)))


# ---------------------------------------------------------------------------
# Small functions -> grouped
# ---------------------------------------------------------------------------


class TestSmallFunctionGrouping:
    def test_is_small_threshold(self):
        sizing = ChunkSizing()
        small_text = "def tiny():\n    return 1"
        unit = _make_unit("tiny", small_text)
        assert is_small(unit, sizing)

        big_text = "\n".join(f"    line_{i} = {i}" for i in range(20))
        big_unit = _make_unit("big", f"def big():\n{big_text}")
        assert not is_small(big_unit, sizing)

    def test_small_functions_grouped(self):
        sizing = ChunkSizing()
        units = [
            _make_unit("a", "def a():\n    return 1", start_line=1),
            _make_unit("b", "def b():\n    return 2", start_line=3),
            _make_unit("c", "def c():\n    return 3", start_line=5),
        ]

        chunks = chunk_code_units(units, sizing)

        groups = [c for c in chunks if c.chunk_kind == ChunkKind.CODE_GROUP]
        assert len(groups) == 1
        assert set(groups[0].member_symbols) == {"a", "b", "c"}

    def test_member_symbols_listed(self):
        sizing = ChunkSizing()
        units = [
            _make_unit("x", "def x():\n    pass", start_line=1),
            _make_unit("y", "def y():\n    pass", start_line=3),
        ]

        groups = group_small_units(units, sizing)

        assert len(groups) == 1
        assert groups[0].member_symbols == ["x", "y"]

    def test_scope_change_breaks_group(self):
        sizing = ChunkSizing()
        units = [
            _make_unit("a", "def a():\n    return 1", parent="ClassA", start_line=1),
            _make_unit("b", "def b():\n    return 2", parent="ClassA", start_line=3),
            _make_unit("c", "def c():\n    return 3", parent="ClassB", start_line=5),
        ]

        groups = group_small_units(units, sizing)

        assert len(groups) == 2
        assert groups[0].member_symbols == ["a", "b"]
        assert groups[0].parent_symbol == "ClassA"
        assert groups[1].member_symbols == ["c"]
        assert groups[1].parent_symbol == "ClassB"

    def test_max_members_limit(self):
        sizing = ChunkSizing(small_group_max_members=3)
        units = [
            _make_unit(f"f{i}", f"def f{i}():\n    return {i}", start_line=i * 2 + 1)
            for i in range(7)
        ]

        groups = group_small_units(units, sizing)

        assert len(groups) == 3  # 3 + 3 + 1
        assert len(groups[0].member_symbols) == 3
        assert len(groups[1].member_symbols) == 3
        assert len(groups[2].member_symbols) == 1

    def test_char_limit_breaks_group(self):
        sizing = ChunkSizing(small_group_target_chars=60)
        units = [
            _make_unit("a", "def a():\n    return 1", start_line=1),
            _make_unit("b", "def b():\n    return 2", start_line=3),
            _make_unit("c", "def c():\n    return 3", start_line=5),
        ]

        groups = group_small_units(units, sizing)

        # Each unit is ~20 chars; target is 60, so first two fit, third starts new group.
        assert len(groups) >= 2

    def test_group_text_combines_members(self):
        sizing = ChunkSizing()
        units = [
            _make_unit("a", "def a():\n    return 1", start_line=1),
            _make_unit("b", "def b():\n    return 2", start_line=3),
        ]

        groups = group_small_units(units, sizing)

        assert "def a():" in groups[0].text
        assert "def b():" in groups[0].text

    def test_group_span_covers_all_members(self):
        sizing = ChunkSizing()
        units = [
            _make_unit("a", "def a():\n    return 1", start_line=10),
            _make_unit("b", "def b():\n    return 2\n    # done", start_line=15),
        ]

        groups = group_small_units(units, sizing)

        assert groups[0].start_line == 10
        assert groups[0].end_line == 17  # line 15 + 2 lines


# ---------------------------------------------------------------------------
# Integration: mixed sizes through chunk_code_units
# ---------------------------------------------------------------------------


class TestMixedSizeChunking:
    def test_mixed_small_normal_large(self):
        sizing = ChunkSizing()
        small_text = "def tiny():\n    return 1"
        normal_body = "\n".join(f"    step_{i}()" for i in range(25))
        normal_text = f"def medium():\n{normal_body}"

        large_lines = []
        while len("\n".join(large_lines)) < 6000:
            i = len(large_lines)
            large_lines.append(f"    result_{i} = compute({i})")
        large_text = 'def huge():\n    """Big function."""\n' + "\n".join(large_lines)

        units = [
            _make_unit("tiny", small_text, start_line=1),
            _make_unit("medium", normal_text, start_line=5),
            _make_unit("huge", large_text, start_line=40),
        ]

        chunks = chunk_code_units(units, sizing)

        kinds = [c.chunk_kind for c in chunks]
        assert ChunkKind.CODE_GROUP in kinds  # tiny
        assert ChunkKind.CODE_FUNCTION in kinds  # medium + huge parts

        # The large function should have been split.
        huge_chunks = [c for c in chunks if c.symbol_name == "huge"]
        assert len(huge_chunks) >= 2
        assert all(c.part_index is not None for c in huge_chunks)

    def test_empty_input(self):
        chunks = chunk_code_units([], ChunkSizing())
        assert chunks == []

    def test_output_sorted_by_position(self):
        sizing = ChunkSizing()
        units = [
            _make_unit("z_last", "def z_last():\n    return 1", start_line=100),
            _make_unit("a_first", "def a_first():\n    return 1", start_line=1),
        ]

        chunks = chunk_code_units(units, sizing)

        # Both are small, but output should be sorted by start_line.
        assert chunks[0].start_line <= chunks[-1].start_line
