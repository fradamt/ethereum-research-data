"""Tests for erd_index.discover.language_detector — extension-based language detection."""

from __future__ import annotations

from pathlib import Path

from erd_index.discover.language_detector import detect_language


# ---------------------------------------------------------------------------
# Known extensions
# ---------------------------------------------------------------------------


class TestKnownExtensions:
    def test_python(self):
        assert detect_language("src/main.py") == "python"

    def test_go(self):
        assert detect_language("cmd/server.go") == "go"

    def test_rust(self):
        assert detect_language("src/lib.rs") == "rust"

    def test_markdown(self):
        assert detect_language("README.md") == "markdown"

    def test_case_insensitive(self):
        assert detect_language("NOTES.MD") == "markdown"
        assert detect_language("main.PY") == "python"
        assert detect_language("lib.Go") == "go"
        assert detect_language("mod.Rs") == "rust"

    def test_accepts_path_object(self):
        assert detect_language(Path("src/foo.py")) == "python"

    def test_accepts_string(self):
        assert detect_language("src/foo.go") == "go"

    def test_nested_path(self):
        assert detect_language("a/b/c/d/deep.rs") == "rust"


# ---------------------------------------------------------------------------
# Unknown / no extension
# ---------------------------------------------------------------------------


class TestUnknownExtension:
    def test_unknown_extension_returns_none(self):
        assert detect_language("data.json") is None

    def test_txt_returns_none(self):
        assert detect_language("notes.txt") is None

    def test_toml_returns_none(self):
        assert detect_language("config.toml") is None

    def test_yaml_returns_none(self):
        assert detect_language("config.yaml") is None

    def test_c_returns_none(self):
        assert detect_language("main.c") is None

    def test_js_returns_none(self):
        assert detect_language("app.js") is None


class TestNoExtension:
    def test_no_extension(self):
        assert detect_language("Makefile") is None

    def test_dotfile(self):
        assert detect_language(".gitignore") is None

    def test_empty_string(self):
        assert detect_language("") is None
