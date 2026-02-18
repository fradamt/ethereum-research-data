"""Tests for converter/discourse_to_md.py — YAML frontmatter, HTML conversion, topic conversion."""

from __future__ import annotations

import json
import os
from pathlib import Path

from converter.discourse_to_md import (
    DiscourseConverter,
    _convert_tables,
    _yaml_scalar,
    dump_frontmatter,
    html_to_markdown,
    load_categories,
    parse_frontmatter,
    safe_filename,
)

# ---------------------------------------------------------------------------
# _yaml_scalar: quoting rules
# ---------------------------------------------------------------------------


class TestYamlScalar:
    def test_plain_string_unquoted(self) -> None:
        assert _yaml_scalar("hello") == "hello"

    def test_empty_string_quoted(self) -> None:
        assert _yaml_scalar("") == '""'

    def test_string_with_colon_space_quoted(self) -> None:
        result = _yaml_scalar("key: value")
        assert result.startswith('"')
        assert result.endswith('"')
        assert "key: value" in result

    def test_string_starting_with_dash_space_quoted(self) -> None:
        result = _yaml_scalar("- item")
        assert result.startswith('"')

    def test_string_starting_with_special_char_quoted(self) -> None:
        for ch in "-?:,[]{}#&*!|>'\"%@`":
            result = _yaml_scalar(f"{ch}start")
            assert result.startswith('"'), f"char {ch!r} should trigger quoting"

    def test_newline_escaped(self) -> None:
        result = _yaml_scalar("line1\nline2")
        assert "\\n" in result
        assert result.startswith('"')

    def test_carriage_return_escaped(self) -> None:
        result = _yaml_scalar("line1\rline2")
        assert "\\r" in result

    def test_boolean_like_strings_quoted(self) -> None:
        for val in ("true", "false", "null", "yes", "no", "on", "off"):
            result = _yaml_scalar(val)
            assert result.startswith('"'), f"{val!r} should be quoted"

    def test_numeric_like_strings_quoted(self) -> None:
        for val in ("123", "3.14", "1e10", "1.5E-3"):
            result = _yaml_scalar(val)
            assert result.startswith('"'), f"{val!r} should be quoted"

    def test_leading_trailing_whitespace_quoted(self) -> None:
        assert _yaml_scalar(" padded ").startswith('"')

    def test_none_returns_null(self) -> None:
        assert _yaml_scalar(None) == "null"

    def test_bool_true(self) -> None:
        assert _yaml_scalar(True) == "true"

    def test_bool_false(self) -> None:
        assert _yaml_scalar(False) == "false"

    def test_int_value(self) -> None:
        assert _yaml_scalar(42) == "42"

    def test_float_value(self) -> None:
        result = _yaml_scalar(3.14)
        assert "3.14" in result

    def test_backslash_not_quoted_unless_needed(self) -> None:
        """Backslash alone does not trigger quoting in _yaml_scalar."""
        result = _yaml_scalar("path\\to\\file")
        # No special YAML trigger, so left unquoted
        assert result == "path\\to\\file"

    def test_backslash_escaped_when_quoting_triggered(self) -> None:
        """When quoting is triggered by another rule, backslashes are escaped."""
        result = _yaml_scalar("path\\to: file")
        assert result.startswith('"')
        assert "\\\\" in result

    def test_double_quote_at_start_quoted(self) -> None:
        """A string starting with double-quote triggers quoting."""
        result = _yaml_scalar('"hello"')
        assert result.startswith('"')
        assert '\\"' in result

    def test_double_quote_mid_string_not_quoted(self) -> None:
        """Double quotes in middle of string do not trigger quoting."""
        result = _yaml_scalar('say "hello"')
        assert result == 'say "hello"'


# ---------------------------------------------------------------------------
# Round-trip: _yaml_scalar + parse_frontmatter
# ---------------------------------------------------------------------------


class TestYamlRoundTrip:
    def _round_trip(self, key: str, value: object) -> object:
        """Dump a single field as frontmatter, parse it back, return the value."""
        fm_str = dump_frontmatter({key: value})
        parsed, _ = parse_frontmatter(fm_str + "\nBody")
        return parsed[key]

    def test_plain_string(self) -> None:
        assert self._round_trip("name", "alice") == "alice"

    def test_string_with_colon(self) -> None:
        assert self._round_trip("title", "EIP-1559: Fee market") == "EIP-1559: Fee market"

    def test_string_with_newline(self) -> None:
        result = self._round_trip("desc", "line1\nline2")
        assert result == "line1\nline2"

    def test_boolean_string(self) -> None:
        assert self._round_trip("val", "true") == "true"

    def test_integer(self) -> None:
        assert self._round_trip("count", 42) == 42

    def test_none_value(self) -> None:
        assert self._round_trip("missing", None) is None

    def test_bool_value(self) -> None:
        assert self._round_trip("flag", True) is True
        assert self._round_trip("flag", False) is False

    def test_list_of_strings(self) -> None:
        result = self._round_trip("tags", ["ethereum", "consensus"])
        assert result == ["ethereum", "consensus"]

    def test_empty_list(self) -> None:
        assert self._round_trip("items", []) == []

    def test_empty_string(self) -> None:
        assert self._round_trip("val", "") == ""

    def test_backslash_in_string(self) -> None:
        result = self._round_trip("path", "a\\b\\c")
        assert result == "a\\b\\c"

    def test_mixed_special_chars(self) -> None:
        val = 'He said "hello: world"\nnew line'
        result = self._round_trip("quote", val)
        assert result == val


# ---------------------------------------------------------------------------
# Newline escaping/unescaping
# ---------------------------------------------------------------------------


class TestNewlineEscaping:
    def test_newline_survives_dump_and_parse(self) -> None:
        original = "first\nsecond\nthird"
        fm = dump_frontmatter({"text": original})
        parsed, _ = parse_frontmatter(fm + "\nbody")
        assert parsed["text"] == original

    def test_multiple_newlines(self) -> None:
        original = "a\n\nb\n\n\nc"
        fm = dump_frontmatter({"text": original})
        parsed, _ = parse_frontmatter(fm + "\nbody")
        assert parsed["text"] == original


# ---------------------------------------------------------------------------
# Backslash escaping order
# ---------------------------------------------------------------------------


class TestBackslashEscaping:
    def test_backslash_then_newline(self) -> None:
        """Backslash followed by newline should round-trip correctly."""
        original = "path\\file\nnext"
        fm = dump_frontmatter({"val": original})
        parsed, _ = parse_frontmatter(fm + "\nbody")
        assert parsed["val"] == original

    def test_literal_backslash_n(self) -> None:
        """A literal \\n (two chars) should not become a newline."""
        original = "not\\na\\nnewline"
        fm = dump_frontmatter({"val": original})
        # In the dump, \\ becomes \\\\, and \n literal doesn't exist.
        # But if original has actual backslash-n, the dump must handle it.
        parsed, _ = parse_frontmatter(fm + "\nbody")
        assert parsed["val"] == original


# ---------------------------------------------------------------------------
# html_to_markdown
# ---------------------------------------------------------------------------


class TestHtmlToMarkdown:
    def test_empty_input(self) -> None:
        assert html_to_markdown("") == ""

    def test_paragraph(self) -> None:
        result = html_to_markdown("<p>Hello world</p>")
        assert "Hello world" in result

    def test_heading(self) -> None:
        result = html_to_markdown("<h2>Section Title</h2>")
        assert "## Section Title" in result

    def test_bold(self) -> None:
        result = html_to_markdown("<p><strong>bold text</strong></p>")
        assert "**bold text**" in result

    def test_italic(self) -> None:
        result = html_to_markdown("<p><em>italic text</em></p>")
        assert "*italic text*" in result

    def test_inline_code(self) -> None:
        result = html_to_markdown("<p>Use <code>foo()</code> here</p>")
        assert "`foo()`" in result

    def test_link(self) -> None:
        result = html_to_markdown('<p><a href="https://example.com">click here</a></p>')
        assert "[click here](https://example.com)" in result

    def test_link_text_equals_href_uses_bare_url(self) -> None:
        result = html_to_markdown(
            '<a href="https://example.com">https://example.com</a>'
        )
        assert result.strip() == "https://example.com"

    def test_unordered_list(self) -> None:
        result = html_to_markdown("<ul><li>one</li><li>two</li></ul>")
        assert "- one" in result
        assert "- two" in result

    def test_ordered_list(self) -> None:
        result = html_to_markdown("<ol><li>first</li><li>second</li></ol>")
        assert "1. first" in result
        assert "2. second" in result

    def test_code_block(self) -> None:
        result = html_to_markdown(
            '<pre><code class="lang-python">def foo():\n    pass</code></pre>'
        )
        assert "```python" in result
        assert "def foo():" in result

    def test_blockquote(self) -> None:
        result = html_to_markdown("<blockquote><p>quoted text</p></blockquote>")
        assert "> " in result
        assert "quoted text" in result

    def test_image(self) -> None:
        result = html_to_markdown('<img src="https://img.png" alt="diagram" />')
        assert "![diagram](https://img.png)" in result

    def test_hr(self) -> None:
        result = html_to_markdown("<p>before</p><hr/><p>after</p>")
        # Uses *** (not ---) to avoid conflict with reply separators
        assert "***" in result

    def test_br_becomes_newline(self) -> None:
        result = html_to_markdown("line1<br/>line2")
        assert "line1\nline2" in result

    def test_html_entities_unescaped(self) -> None:
        result = html_to_markdown("<p>&amp; &lt; &gt; &quot;</p>")
        assert "& < > " in result

    def test_nested_tags_stripped(self) -> None:
        result = html_to_markdown("<div><span>text</span></div>")
        assert "text" in result
        assert "<" not in result


# ---------------------------------------------------------------------------
# _convert_tables
# ---------------------------------------------------------------------------


class TestConvertTables:
    def test_basic_table(self) -> None:
        table_html = (
            "<table>"
            "<thead><tr><th>Name</th><th>Age</th></tr></thead>"
            "<tbody><tr><td>Alice</td><td>30</td></tr>"
            "<tr><td>Bob</td><td>25</td></tr></tbody>"
            "</table>"
        )
        result = _convert_tables(table_html)
        assert "| Name | Age |" in result
        assert "| --- | --- |" in result
        assert "| Alice | 30 |" in result
        assert "| Bob | 25 |" in result

    def test_table_without_thead(self) -> None:
        """First row becomes headers when no thead present."""
        table_html = (
            "<table><tbody>"
            "<tr><td>Header1</td><td>Header2</td></tr>"
            "<tr><td>val1</td><td>val2</td></tr>"
            "</tbody></table>"
        )
        result = _convert_tables(table_html)
        assert "| Header1 | Header2 |" in result
        assert "| val1 | val2 |" in result

    def test_empty_table_returned_as_is(self) -> None:
        table_html = "<table></table>"
        result = _convert_tables(table_html)
        assert "<table></table>" in result

    def test_uneven_columns_padded(self) -> None:
        table_html = (
            "<table>"
            "<thead><tr><th>A</th><th>B</th><th>C</th></tr></thead>"
            "<tbody><tr><td>1</td><td>2</td></tr></tbody>"
            "</table>"
        )
        result = _convert_tables(table_html)
        # Row should be padded to 3 columns
        lines = [ln for ln in result.strip().split("\n") if ln.startswith("|")]
        for line in lines:
            # Count columns by counting | separators
            assert line.count("|") >= 4  # 3 cols + leading + trailing


# ---------------------------------------------------------------------------
# _merge_enrichment
# ---------------------------------------------------------------------------


class TestMergeEnrichment:
    def _make_converter(self, raw_dir: Path, corpus_dir: Path) -> DiscourseConverter:
        return DiscourseConverter(
            source_name="test",
            base_url="https://example.com",
            raw_dir=raw_dir,
            corpus_dir=corpus_dir,
        )

    def test_preserves_extra_fields(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir(parents=True, exist_ok=True)

        # Existing file with enrichment fields
        existing_fm = dump_frontmatter({
            "source": "test",
            "topic_id": 42,
            "title": "Original",
            "influence_score": 0.85,
            "research_thread": "data-availability",
        })
        out_path = corpus_dir / "42-topic.md"
        out_path.write_text(existing_fm + "\n\n# Original\n\nBody text.\n")

        # New content without enrichment fields
        new_fm = dump_frontmatter({
            "source": "test",
            "topic_id": 42,
            "title": "Updated Title",
        })
        new_content = new_fm + "\n\n# Updated Title\n\nNew body.\n"

        converter = self._make_converter(raw_dir, corpus_dir)
        merged = converter._merge_enrichment(out_path, new_content)

        parsed, body = parse_frontmatter(merged)
        assert parsed["title"] == "Updated Title"
        assert parsed["influence_score"] == 0.85
        assert parsed["research_thread"] == "data-availability"
        assert "New body." in body

    def test_new_file_returns_content_unchanged(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir(parents=True, exist_ok=True)

        converter = self._make_converter(raw_dir, corpus_dir)
        new_content = dump_frontmatter({"source": "test"}) + "\n\nBody\n"

        result = converter._merge_enrichment(corpus_dir / "nonexistent.md", new_content)
        assert result == new_content

    def test_no_frontmatter_in_existing_returns_new_content(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir(parents=True, exist_ok=True)

        out_path = corpus_dir / "42-topic.md"
        out_path.write_text("Just plain text, no frontmatter.")

        converter = self._make_converter(raw_dir, corpus_dir)
        new_content = dump_frontmatter({"source": "test"}) + "\n\nBody\n"

        result = converter._merge_enrichment(out_path, new_content)
        assert result == new_content


# ---------------------------------------------------------------------------
# convert_topic
# ---------------------------------------------------------------------------


class TestConvertTopic:
    def _make_converter(self, raw_dir: Path, corpus_dir: Path) -> DiscourseConverter:
        return DiscourseConverter(
            source_name="ethresearch",
            base_url="https://ethresear.ch",
            raw_dir=raw_dir,
            corpus_dir=corpus_dir,
        )

    def _write_topic_json(self, path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_basic_conversion(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        converter = self._make_converter(raw_dir, corpus_dir)

        topic = {
            "id": 100,
            "title": "Test Topic",
            "slug": "test-topic",
            "created_at": "2024-03-15T12:00:00Z",
            "category_id": 1,
            "tags": ["consensus", "finality"],
            "views": 500,
            "like_count": 10,
            "posts_count": 2,
            "post_stream": {
                "posts": [
                    {"id": 1, "username": "vitalik", "created_at": "2024-03-15T12:00:00Z",
                     "cooked": "<p>This is the main post.</p>"},
                    {"id": 2, "username": "dankrad", "created_at": "2024-03-16T10:00:00Z",
                     "cooked": "<p>Great analysis!</p>"},
                ],
            },
        }
        topic_path = raw_dir / "topics" / "100.json"
        self._write_topic_json(topic_path, topic)

        result = converter.convert_topic(topic_path)
        assert result is not None

        filename, content = result
        assert filename == "100-test-topic.md"

        # Check frontmatter
        fm, body = parse_frontmatter(content)
        assert fm["source"] == "ethresearch"
        assert fm["topic_id"] == 100
        assert fm["title"] == "Test Topic"
        assert fm["author"] == "vitalik"
        assert fm["views"] == 500
        assert fm["tags"] == ["consensus", "finality"]
        assert fm["url"] == "https://ethresear.ch/t/test-topic/100"

        # Check body
        assert "# Test Topic" in body
        assert "This is the main post." in body
        assert "## Replies" in body
        assert "**dankrad**" in body
        assert "Great analysis!" in body

    def test_no_posts_returns_none(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        converter = self._make_converter(raw_dir, tmp_path / "corpus")

        topic = {"id": 200, "title": "Empty", "slug": "empty", "post_stream": {"posts": []}}
        topic_path = raw_dir / "topics" / "200.json"
        self._write_topic_json(topic_path, topic)

        result = converter.convert_topic(topic_path)
        assert result is None

    def test_empty_post_body_skipped_in_replies(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        converter = self._make_converter(raw_dir, tmp_path / "corpus")

        topic = {
            "id": 300,
            "title": "With Empty Reply",
            "slug": "with-empty-reply",
            "created_at": "2024-01-01T00:00:00Z",
            "posts_count": 3,
            "post_stream": {
                "posts": [
                    {"id": 1, "username": "alice", "created_at": "2024-01-01T00:00:00Z",
                     "cooked": "<p>Main post</p>"},
                    {"id": 2, "username": "bob", "created_at": "2024-01-02T00:00:00Z",
                     "cooked": ""},  # empty
                    {"id": 3, "username": "carol", "created_at": "2024-01-03T00:00:00Z",
                     "cooked": "<p>Real reply</p>"},
                ],
            },
        }
        topic_path = raw_dir / "topics" / "300.json"
        self._write_topic_json(topic_path, topic)

        _, content = converter.convert_topic(topic_path)
        assert "**bob**" not in content  # empty reply skipped
        assert "**carol**" in content

    def test_max_replies_limit(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        converter = DiscourseConverter(
            source_name="test",
            base_url="https://example.com",
            raw_dir=raw_dir,
            corpus_dir=tmp_path / "corpus",
            max_replies=2,
        )

        posts = [
            {"id": 1, "username": "op", "created_at": "2024-01-01T00:00:00Z",
             "cooked": "<p>OP</p>"},
        ]
        for i in range(5):
            posts.append({
                "id": i + 2, "username": f"user{i}", "created_at": "2024-01-01T00:00:00Z",
                "cooked": f"<p>Reply {i}</p>",
            })

        topic = {
            "id": 400,
            "title": "Many Replies",
            "slug": "many-replies",
            "created_at": "2024-01-01T00:00:00Z",
            "posts_count": 6,
            "post_stream": {"posts": posts},
        }
        topic_path = raw_dir / "topics" / "400.json"
        self._write_topic_json(topic_path, topic)

        _, content = converter.convert_topic(topic_path)
        # Only first 2 replies shown
        assert "**user0**" in content
        assert "**user1**" in content
        assert "**user2**" not in content
        assert "more replies not shown" in content

    def test_unicode_content(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        converter = self._make_converter(raw_dir, tmp_path / "corpus")

        topic = {
            "id": 500,
            "title": "Unicode: Ethereum 2.0 \u2014 The Merge",
            "slug": "unicode-test",
            "created_at": "2024-01-01T00:00:00Z",
            "posts_count": 1,
            "post_stream": {
                "posts": [{
                    "id": 1, "username": "author",
                    "created_at": "2024-01-01T00:00:00Z",
                    "cooked": "<p>G\u00f6del\u2019s theorem \u2208 \u2200x</p>",
                }],
            },
        }
        topic_path = raw_dir / "topics" / "500.json"
        self._write_topic_json(topic_path, topic)

        result = converter.convert_topic(topic_path)
        assert result is not None
        _, content = result
        assert "G\u00f6del" in content
        assert "\u2208" in content

    def test_missing_optional_fields(self, tmp_path: Path) -> None:
        """Topic JSON missing optional fields should not crash."""
        raw_dir = tmp_path / "raw"
        converter = self._make_converter(raw_dir, tmp_path / "corpus")

        topic = {
            "id": 600,
            "post_stream": {
                "posts": [{
                    "id": 1,
                    "cooked": "<p>Minimal</p>",
                }],
            },
        }
        topic_path = raw_dir / "topics" / "600.json"
        self._write_topic_json(topic_path, topic)

        result = converter.convert_topic(topic_path)
        assert result is not None
        filename, content = result
        assert "600" in filename
        fm, _ = parse_frontmatter(content)
        assert fm["topic_id"] == 600
        assert fm["author"] == "unknown"


# ---------------------------------------------------------------------------
# Incremental skip logic (mtime comparison)
# ---------------------------------------------------------------------------


class TestIncrementalSkip:
    def _make_converter(self, raw_dir: Path, corpus_dir: Path) -> DiscourseConverter:
        return DiscourseConverter(
            source_name="test",
            base_url="https://example.com",
            raw_dir=raw_dir,
            corpus_dir=corpus_dir,
        )

    def _write_categories(self, raw_dir: Path) -> None:
        raw_dir.mkdir(parents=True, exist_ok=True)
        cats = {"category_list": {"categories": [{"id": 1, "name": "General", "slug": "general"}]}}
        (raw_dir / "categories.json").write_text(json.dumps(cats))

    def _write_topic(self, topics_dir: Path, topic_id: int, slug: str = "test") -> Path:
        topics_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "id": topic_id,
            "title": f"Topic {topic_id}",
            "slug": slug,
            "created_at": "2024-01-01T00:00:00Z",
            "category_id": 1,
            "posts_count": 1,
            "post_stream": {
                "posts": [{
                    "id": 1, "username": "alice",
                    "created_at": "2024-01-01T00:00:00Z",
                    "cooked": "<p>Content</p>",
                }],
            },
        }
        path = topics_dir / f"{topic_id}.json"
        path.write_text(json.dumps(data))
        return path

    def test_reconverts_when_source_newer_than_output(self, tmp_path: Path) -> None:
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir(parents=True, exist_ok=True)
        self._write_categories(raw_dir)

        src = self._write_topic(raw_dir / "topics", 10, "topic-ten")
        out_path = corpus_dir / "10-topic-ten.md"
        out_path.write_text("stale content")

        # Make output older than source
        os.utime(out_path, (1000, 1000))
        os.utime(src, (9999, 9999))

        converter = self._make_converter(raw_dir, corpus_dir)
        converted, skipped = converter.convert_all()

        assert converted == 1
        assert skipped == 0
        assert out_path.read_text() != "stale content"


# ---------------------------------------------------------------------------
# safe_filename
# ---------------------------------------------------------------------------


class TestSafeFilename:
    def test_basic(self) -> None:
        assert safe_filename(42, "my-topic") == "42-my-topic.md"

    def test_long_slug_truncated(self) -> None:
        result = safe_filename(1, "a" * 100)
        assert len(result) < 100

    def test_unsafe_chars_replaced(self) -> None:
        result = safe_filename(1, "hello world/foo:bar")
        assert " " not in result
        assert "/" not in result
        assert ":" not in result

    def test_empty_slug(self) -> None:
        result = safe_filename(1, "")
        assert result == "1-topic.md"


# ---------------------------------------------------------------------------
# load_categories
# ---------------------------------------------------------------------------


class TestLoadCategories:
    def test_loads_categories_and_subcategories(self, tmp_path: Path) -> None:
        data = {
            "category_list": {
                "categories": [
                    {
                        "id": 1,
                        "name": "Research",
                        "subcategory_list": [
                            {"id": 10, "name": "Consensus"},
                            {"id": 11, "name": "Execution"},
                        ],
                    },
                    {"id": 2, "name": "General"},
                ],
            },
        }
        path = tmp_path / "categories.json"
        path.write_text(json.dumps(data))

        cats = load_categories(path)

        assert cats[1] == "Research"
        assert cats[2] == "General"
        assert cats[10] == "Research > Consensus"
        assert cats[11] == "Research > Execution"
