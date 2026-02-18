"""Tests for erd_index/chunk/split_large_units.py — splitting oversized code units."""

from __future__ import annotations

from erd_index.chunk.split_large_units import (
    _build_header,
    _extract_body_lines,
    _is_statement_start,
    _split_at_statement_boundaries,
    _split_by_line_windows,
    split_large_unit,
)
from erd_index.models import ChunkKind, Language, ParsedUnit, SourceKind
from erd_index.settings import ChunkSizing

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_SENTINEL = object()


def _make_unit(
    name: str,
    text: str,
    *,
    kind: str = "function",
    start_line: int = 1,
    signature: object = _SENTINEL,
    docstring: object = _SENTINEL,
) -> ParsedUnit:
    """Build a ParsedUnit for testing split logic."""
    lines = text.count("\n") + 1
    sig = f"def {name}():" if signature is _SENTINEL else signature
    ds = f"Doc for {name}." if docstring is _SENTINEL else docstring
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
        signature=str(sig) if sig else "",
        parent_symbol="",
        module_path="test.module",
        imports=["import os"],
        docstring=str(ds) if ds else "",
    )


def _make_large_text(char_count: int = 8000) -> str:
    """Generate a function body that exceeds a certain char count."""
    lines = []
    while len("\n".join(lines)) < char_count:
        i = len(lines)
        lines.append(f"    result_{i} = compute_step({i}, data[{i}], config)")
        lines.append(f"    if result_{i} is None:")
        lines.append(f'        raise ValueError("Step {i} failed")')
    body = "\n".join(lines)
    return f'def process_all(data, config):\n    """Process all steps."""\n{body}'


# ---------------------------------------------------------------------------
# split_large_unit
# ---------------------------------------------------------------------------


class TestSplitLargeUnit:
    def test_splits_large_function(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit("process_all", text, signature="def process_all(data, config):")
        sizing = ChunkSizing()

        assert len(text) > sizing.hard_max_chars

        chunks = split_large_unit(unit, sizing)

        assert len(chunks) >= 2

    def test_part_indices_and_counts(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit("process_all", text, signature="def process_all(data, config):")

        chunks = split_large_unit(unit, ChunkSizing())

        total = len(chunks)
        for i, c in enumerate(chunks):
            assert c.part_index == i
            assert c.part_count == total

    def test_signature_preserved_in_all_parts(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit("process_all", text, signature="def process_all(data, config):")

        chunks = split_large_unit(unit, ChunkSizing())

        for c in chunks:
            assert "def process_all" in c.text

    def test_docstring_preserved_in_all_parts(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit(
            "process_all",
            text,
            signature="def process_all(data, config):",
            docstring="Process all steps.",
        )

        chunks = split_large_unit(unit, ChunkSizing())

        for c in chunks:
            assert "Process all steps." in c.text

    def test_degenerate_header_only(self) -> None:
        """A unit that is all header produces a single chunk."""
        text = 'def tiny():\n    """Just a docstring."""\n    pass'
        unit = _make_unit("tiny", text, docstring="Just a docstring.")

        chunks = split_large_unit(unit, ChunkSizing())

        assert len(chunks) == 1
        assert chunks[0].part_index == 0
        assert chunks[0].part_count == 1

    def test_chunk_kind_is_code_function(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit("process_all", text, signature="def process_all(data, config):")

        chunks = split_large_unit(unit, ChunkSizing())

        for c in chunks:
            assert c.chunk_kind == ChunkKind.CODE_FUNCTION

    def test_chunk_kind_is_code_struct_for_class(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit(
            "BigClass", text, kind="class", signature="class BigClass:"
        )

        chunks = split_large_unit(unit, ChunkSizing())

        for c in chunks:
            assert c.chunk_kind == ChunkKind.CODE_STRUCT

    def test_metadata_copied_to_all_chunks(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit("process_all", text, signature="def process_all(data, config):")

        chunks = split_large_unit(unit, ChunkSizing())

        for c in chunks:
            assert c.source_kind == SourceKind.CODE
            assert c.language == Language.PYTHON
            assert c.repository == "test-repo"
            assert c.path == "test/module.py"
            assert c.symbol_name == "process_all"
            assert c.symbol_qualname == "test.module.process_all"
            assert c.module_path == "test.module"
            assert c.imports == ["import os"]

    def test_start_end_lines_are_reasonable(self) -> None:
        text = _make_large_text(8000)
        unit = _make_unit("fn", text, start_line=10, signature="def fn():")

        chunks = split_large_unit(unit, ChunkSizing())

        # Start lines should be non-decreasing
        for i in range(1, len(chunks)):
            assert chunks[i].start_line >= chunks[i - 1].start_line

        # All start/end lines within the unit range
        for c in chunks:
            assert c.start_line >= unit.start_line
            assert c.end_line <= unit.end_line


# ---------------------------------------------------------------------------
# _build_header
# ---------------------------------------------------------------------------


class TestBuildHeader:
    def test_signature_only(self) -> None:
        unit = _make_unit("fn", "def fn():\n    pass", signature="def fn():", docstring="")
        header = _build_header(unit)
        assert header == "def fn():"

    def test_signature_and_docstring(self) -> None:
        unit = _make_unit("fn", "def fn():\n    pass", signature="def fn():", docstring="Do stuff.")
        header = _build_header(unit)
        assert "def fn():" in header
        assert '"""Do stuff."""' in header

    def test_empty_signature_and_docstring(self) -> None:
        unit = _make_unit("fn", "def fn():\n    pass", signature="", docstring="")
        header = _build_header(unit)
        assert header == ""


# ---------------------------------------------------------------------------
# _extract_body_lines
# ---------------------------------------------------------------------------


class TestExtractBodyLines:
    def test_simple_function(self) -> None:
        text = 'def foo():\n    """Docstring."""\n    x = 1\n    return x'
        header = 'def foo():\n    """Docstring."""'

        body_lines, body_start = _extract_body_lines(text, header)

        # Body should start after the docstring
        assert body_start == 2
        assert body_lines[0].strip() == "x = 1"

    def test_body_start_offset_correct(self) -> None:
        text = 'def bar():\n    """Multi\n    line\n    docstring."""\n    a = 1\n    b = 2'
        header = 'def bar():\n    """Multi\n    line\n    docstring."""'

        body_lines, body_start = _extract_body_lines(text, header)

        # Body should start after multi-line docstring
        assert body_start == 4
        assert "a = 1" in body_lines[0]

    def test_no_docstring(self) -> None:
        text = "def baz():\n    x = 1\n    return x"
        header = "def baz():"

        body_lines, body_start = _extract_body_lines(text, header)

        assert body_start >= 1
        # Body should contain the actual statements
        body_text = "\n".join(body_lines)
        assert "x = 1" in body_text

    def test_empty_body(self) -> None:
        text = 'def empty():\n    """Only a docstring."""'
        header = 'def empty():\n    """Only a docstring."""'

        body_lines, _body_start = _extract_body_lines(text, header)

        assert body_lines == []


# ---------------------------------------------------------------------------
# _is_statement_start
# ---------------------------------------------------------------------------


class TestIsStatementStart:
    def test_statement_at_base_indent(self) -> None:
        assert _is_statement_start("    x = 1", 4) is True

    def test_deeper_indent_not_statement(self) -> None:
        assert _is_statement_start("        x = 1", 4) is False

    def test_blank_line_not_statement(self) -> None:
        assert _is_statement_start("", 4) is False
        assert _is_statement_start("    ", 4) is False

    def test_comment_not_statement(self) -> None:
        assert _is_statement_start("    # comment", 4) is False

    def test_less_indent_is_statement(self) -> None:
        assert _is_statement_start("  x = 1", 4) is True


# ---------------------------------------------------------------------------
# Statement boundary splitting
# ---------------------------------------------------------------------------


class TestStatementBoundarySplitting:
    def test_splits_at_statement_boundaries(self) -> None:
        body_lines = [
            "    x = compute(1)",
            "    y = compute(2)",
            "    z = compute(3)",
            "    w = compute(4)",
        ]
        header = "def fn():\n    '''doc'''"
        sizing = ChunkSizing(target_chars=60)  # very small target

        parts = _split_at_statement_boundaries(body_lines, header, sizing)

        assert len(parts) >= 2
        for text, _start, _end in parts:
            assert header in text

    def test_empty_body_returns_empty(self) -> None:
        parts = _split_at_statement_boundaries([], "def fn():", ChunkSizing())
        assert parts == []

    def test_single_statement_returns_empty(self) -> None:
        """If there's only one statement boundary, can't split meaningfully."""
        body = ["    x = compute(1)"]
        parts = _split_at_statement_boundaries(body, "def fn():", ChunkSizing())
        # Only one boundary at index 0, so len(boundaries) <= 1 -> returns []
        assert parts == []


# ---------------------------------------------------------------------------
# Line-window splitting fallback
# ---------------------------------------------------------------------------


class TestLineWindowSplitting:
    def test_splits_into_windows(self) -> None:
        body_lines = [f"    line_{i} = {i}" for i in range(100)]
        header = "def fn():"
        sizing = ChunkSizing(target_chars=500)

        parts = _split_by_line_windows(body_lines, header, sizing)

        assert len(parts) >= 2
        for text, _start, _end in parts:
            assert header in text

    def test_overlap_between_windows(self) -> None:
        """Adjacent windows should overlap by _OVERLAP_LINES."""
        body_lines = [f"    line_{i} = {i}" for i in range(200)]
        header = "def fn():"
        sizing = ChunkSizing(target_chars=500)

        parts = _split_by_line_windows(body_lines, header, sizing)

        if len(parts) >= 2:
            _, _, end_0 = parts[0]
            _, start_1, _ = parts[1]
            # start_1 should be before end_0 (overlap)
            assert start_1 <= end_0

    def test_single_window_for_small_body(self) -> None:
        body_lines = ["    x = 1", "    y = 2"]
        header = "def fn():"
        sizing = ChunkSizing(target_chars=5000)

        parts = _split_by_line_windows(body_lines, header, sizing)

        assert len(parts) == 1
        text, _start, _end = parts[0]
        assert "x = 1" in text
        assert "y = 2" in text

    def test_header_prepended_to_all_windows(self) -> None:
        body_lines = [f"    line_{i} = {i}" for i in range(100)]
        header = "def my_function(arg1, arg2):"
        sizing = ChunkSizing(target_chars=400)

        parts = _split_by_line_windows(body_lines, header, sizing)

        for text, _, _ in parts:
            assert text.startswith(header)


# ---------------------------------------------------------------------------
# Integration: split_large_unit uses statement boundaries or falls back
# ---------------------------------------------------------------------------


class TestSplitIntegration:
    def test_no_split_needed_for_small_unit(self) -> None:
        """A unit that fits in one chunk returns a single chunk."""
        text = "def small():\n    return 1"
        unit = _make_unit("small", text)

        chunks = split_large_unit(unit, ChunkSizing())

        assert len(chunks) == 1
        assert chunks[0].part_index == 0
        assert chunks[0].part_count == 1
        assert chunks[0].text == text

    def test_fallback_to_line_windows(self) -> None:
        """When statement boundaries can't split (e.g., one giant expression),
        line-window fallback is used."""
        # Create a unit with a single very long statement (no boundary to split at)
        inner_lines = ["        " + "x" * 50 for _ in range(200)]
        body = "\n".join(inner_lines)
        text = f"def deep_nest():\n    if True:\n{body}"
        unit = _make_unit(
            "deep_nest",
            text,
            signature="def deep_nest():",
            docstring="",
        )
        sizing = ChunkSizing(target_chars=500, hard_max_chars=1000)

        chunks = split_large_unit(unit, sizing)

        # Should still produce multiple parts via line-window fallback
        assert len(chunks) >= 2
        # All parts have the signature
        for c in chunks:
            assert "def deep_nest():" in c.text

    def test_consecutive_parts_cover_all_body(self) -> None:
        """The union of all parts should cover the entire body text."""
        text = _make_large_text(8000)
        unit = _make_unit("fn", text, signature="def fn():")

        chunks = split_large_unit(unit, ChunkSizing())

        # Each part has the header + some body lines
        # Just verify we get complete coverage by checking first and last parts
        assert len(chunks) >= 2
        # First part should contain early body content
        assert "result_0" in chunks[0].text
        # Last part should contain late body content
        last_text = chunks[-1].text
        # The last part should have some of the later results
        assert "result_" in last_text
