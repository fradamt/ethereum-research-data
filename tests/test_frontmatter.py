"""Tests for YAML frontmatter extraction."""

from __future__ import annotations

import logging

from erd_index.parse.frontmatter import extract_frontmatter

# ---------------------------------------------------------------------------
# Valid frontmatter
# ---------------------------------------------------------------------------


class TestValidFrontmatter:
    def test_simple_fields(self):
        text = "---\ntitle: Hello\nauthor: alice\n---\n\nBody text."
        fm, body = extract_frontmatter(text)
        assert fm == {"title": "Hello", "author": "alice"}
        assert body.strip() == "Body text."

    def test_body_starts_after_closing_delimiter(self):
        text = "---\nk: v\n---\n\n# Heading\n\nParagraph."
        fm, body = extract_frontmatter(text)
        assert fm == {"k": "v"}
        assert body.lstrip().startswith("# Heading")

    def test_numeric_values(self):
        text = "---\neip: 1559\nviews: 42\nscore: 0.95\n---\nBody"
        fm, _body = extract_frontmatter(text)
        assert fm["eip"] == 1559
        assert fm["views"] == 42
        assert fm["score"] == 0.95

    def test_list_values(self):
        text = "---\ntags: [a, b, c]\n---\nBody"
        fm, _body = extract_frontmatter(text)
        assert fm["tags"] == ["a", "b", "c"]

    def test_nested_dict(self):
        text = "---\nmeta:\n  key1: val1\n  key2: val2\n---\nBody"
        fm, _body = extract_frontmatter(text)
        assert fm["meta"] == {"key1": "val1", "key2": "val2"}

    def test_quoted_string_values(self):
        text = '---\ntitle: "Hello: World"\ndate: "2024-01-01"\n---\nBody'
        fm, _body = extract_frontmatter(text)
        assert fm["title"] == "Hello: World"
        assert fm["date"] == "2024-01-01"

    def test_multiline_body_preserved(self):
        text = "---\nk: v\n---\n\nLine 1\nLine 2\nLine 3"
        _, body = extract_frontmatter(text)
        assert "Line 1\nLine 2\nLine 3" in body

    def test_real_ethresearch_file(self, fixtures_dir):
        path = fixtures_dir.parent.parent / "corpus" / "ethresearch"
        files = sorted(path.glob("*.md"))
        if not files:
            return
        text = files[0].read_text()
        fm, body = extract_frontmatter(text)
        assert isinstance(fm, dict)
        assert "source" in fm or "topic_id" in fm
        assert len(body) > 0

    def test_real_eip_file(self, fixtures_dir):
        path = fixtures_dir.parent.parent / "corpus" / "eips" / "eip-1559.md"
        if not path.exists():
            return
        text = path.read_text()
        fm, _body = extract_frontmatter(text)
        assert fm["eip"] == 1559
        assert fm["status"] == "Final"
        assert "requires" in fm


# ---------------------------------------------------------------------------
# Missing frontmatter
# ---------------------------------------------------------------------------


class TestMissingFrontmatter:
    def test_no_delimiters(self):
        text = "Just plain text\nwith no frontmatter."
        fm, body = extract_frontmatter(text)
        assert fm == {}
        assert body == text

    def test_single_delimiter_only(self):
        text = "---\ntitle: orphan\nno closing delimiter"
        fm, body = extract_frontmatter(text)
        assert fm == {}
        assert body == text

    def test_empty_string(self):
        fm, body = extract_frontmatter("")
        assert fm == {}
        assert body == ""

    def test_starts_with_heading(self):
        text = "# Heading\n\nBody text."
        fm, body = extract_frontmatter(text)
        assert fm == {}
        assert body == text


# ---------------------------------------------------------------------------
# Malformed YAML
# ---------------------------------------------------------------------------


class TestMalformedYaml:
    def test_invalid_yaml_returns_empty_dict(self, caplog):
        text = "---\nbad: [yaml: broken\n---\nBody text."
        with caplog.at_level(logging.WARNING):
            fm, body = extract_frontmatter(text)
        assert fm == {}
        assert "Body text." in body
        assert any("Malformed YAML" in r.message for r in caplog.records)

    def test_yaml_is_scalar_not_dict(self):
        """If the YAML block parses to a non-dict (e.g. a string), return empty."""
        text = "---\njust a string\n---\nBody"
        fm, _body = extract_frontmatter(text)
        assert fm == {}

    def test_yaml_is_list_not_dict(self):
        text = "---\n- item1\n- item2\n---\nBody"
        fm, _body = extract_frontmatter(text)
        assert fm == {}


# ---------------------------------------------------------------------------
# Empty frontmatter
# ---------------------------------------------------------------------------


class TestEmptyFrontmatter:
    def test_empty_yaml_block(self):
        text = "---\n\n---\nBody"
        fm, _body = extract_frontmatter(text)
        # yaml.safe_load("") returns None, which is not a dict.
        assert fm == {}

    def test_whitespace_only_yaml(self):
        text = "---\n   \n---\nBody"
        fm, _body = extract_frontmatter(text)
        assert fm == {}


# ---------------------------------------------------------------------------
# Complex types
# ---------------------------------------------------------------------------


class TestComplexTypes:
    def test_comma_separated_requires(self):
        """EIP-style `requires: 2718, 2930` parses as a string in YAML."""
        text = "---\nrequires: 2718, 2930\n---\nBody"
        fm, _ = extract_frontmatter(text)
        # PyYAML parses "2718, 2930" as the string "2718, 2930"
        assert isinstance(fm["requires"], str)

    def test_requires_as_yaml_list(self):
        text = "---\nrequires: [2718, 2930]\n---\nBody"
        fm, _ = extract_frontmatter(text)
        assert fm["requires"] == [2718, 2930]

    def test_boolean_values(self):
        text = "---\nactive: true\ndeprecated: false\n---\nBody"
        fm, _ = extract_frontmatter(text)
        assert fm["active"] is True
        assert fm["deprecated"] is False

    def test_multiline_string(self):
        text = "---\ndescription: |\n  Line one.\n  Line two.\n---\nBody"
        fm, _ = extract_frontmatter(text)
        assert "Line one." in fm["description"]
        assert "Line two." in fm["description"]
