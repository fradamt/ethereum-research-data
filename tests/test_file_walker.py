"""Tests for erd_index.discover.file_walker — directory walking and file discovery."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from erd_index.discover.file_walker import (
    DiscoveredFile,
    _is_excluded,
    _walk_code_repo,
    _walk_corpus_source,
    walk_sources,
)
from erd_index.settings import ChunkSizing, CodeRepo, CorpusSource, MeilisearchConfig, Settings


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_settings(
    tmp_path: Path,
    corpus_sources: list[CorpusSource] | None = None,
    code_repos: list[CodeRepo] | None = None,
) -> Settings:
    """Build a Settings object pointing into tmp_path."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    return Settings(
        meili=MeilisearchConfig(),
        chunk_sizing=ChunkSizing(),
        corpus_dir=str(tmp_path / "corpus"),
        data_dir=str(data_dir),
        graph_db=str(data_dir / "graph.db"),
        state_db=str(data_dir / "index_state.db"),
        project_root=tmp_path,
        corpus_sources=corpus_sources or [],
        code_repos=code_repos or [],
    )


def _populate_tree(base: Path, files: dict[str, str]) -> None:
    """Create files under *base*.  Keys are relative paths, values are content."""
    for rel, content in files.items():
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)


# ---------------------------------------------------------------------------
# _is_excluded
# ---------------------------------------------------------------------------


class TestIsExcluded:
    def test_no_patterns(self):
        assert not _is_excluded("any/path.py", [])

    def test_exact_match(self):
        assert _is_excluded("vendor/dep.go", ["vendor/dep.go"])

    def test_glob_star(self):
        assert _is_excluded("vendor/dep.go", ["vendor/*"])

    def test_double_star(self):
        """fnmatch does NOT support ** natively (it doesn't cross /), so
        we verify the current behaviour: ** works like * within fnmatch."""
        # fnmatch.fnmatch("a/b/c.go", "**/*.go") is True on most platforms
        # because fnmatch treats ** as "any chars" including /
        assert _is_excluded("a/b/c.go", ["**/*.go"])

    def test_no_match(self):
        assert not _is_excluded("src/main.py", ["vendor/*"])

    def test_multiple_patterns_first_matches(self):
        assert _is_excluded("test_data/big.md", ["test_data/*", "vendor/*"])

    def test_multiple_patterns_second_matches(self):
        assert _is_excluded("vendor/x.go", ["test_data/*", "vendor/*"])

    def test_extension_pattern(self):
        assert _is_excluded("notes.txt", ["*.txt"])

    def test_extension_pattern_no_match(self):
        assert not _is_excluded("notes.md", ["*.txt"])


# ---------------------------------------------------------------------------
# _walk_corpus_source
# ---------------------------------------------------------------------------


class TestWalkCorpusSource:
    def test_discovers_markdown_files(self, tmp_path: Path):
        corpus = tmp_path / "corpus" / "ethresearch"
        _populate_tree(corpus, {
            "topic-1.md": "# Topic 1",
            "topic-2.md": "# Topic 2",
            "nested/deep.md": "# Deep",
        })
        source = CorpusSource(name="ethresearch", path="corpus/ethresearch")
        found = _walk_corpus_source(source, tmp_path)
        rel_paths = sorted(f.relative_path for f in found)
        assert "topic-1.md" in rel_paths
        assert "topic-2.md" in rel_paths
        assert "nested/deep.md" in rel_paths

    def test_fields_populated(self, tmp_path: Path):
        corpus = tmp_path / "corpus" / "test"
        _populate_tree(corpus, {"hello.md": "hello world"})
        source = CorpusSource(name="test-source", path="corpus/test")
        found = _walk_corpus_source(source, tmp_path)
        assert len(found) == 1
        f = found[0]
        assert f.source_name == "test-source"
        assert f.repository == ""
        assert f.language == "markdown"
        assert f.relative_path == "hello.md"
        assert f.absolute_path == corpus / "hello.md"
        assert f.size_bytes > 0
        assert f.mtime_ns > 0

    def test_exclude_patterns(self, tmp_path: Path):
        corpus = tmp_path / "corpus" / "src"
        _populate_tree(corpus, {
            "keep.md": "keep",
            "drafts/skip.md": "skip",
        })
        source = CorpusSource(
            name="src",
            path="corpus/src",
            exclude=["drafts/*"],
        )
        found = _walk_corpus_source(source, tmp_path)
        rel_paths = [f.relative_path for f in found]
        assert "keep.md" in rel_paths
        assert "drafts/skip.md" not in rel_paths

    def test_include_patterns(self, tmp_path: Path):
        corpus = tmp_path / "corpus" / "mixed"
        _populate_tree(corpus, {
            "readme.md": "yes",
            "data.json": "no",
            "script.py": "no",
        })
        # Default include is **/*.md — only markdown should come through
        source = CorpusSource(name="mixed", path="corpus/mixed")
        found = _walk_corpus_source(source, tmp_path)
        rel_paths = [f.relative_path for f in found]
        assert "readme.md" in rel_paths
        # .json has no language mapping, .py is python but include limits to *.md
        assert "data.json" not in rel_paths
        assert "script.py" not in rel_paths

    def test_missing_directory_returns_empty(self, tmp_path: Path, caplog):
        source = CorpusSource(name="missing", path="corpus/nonexistent")
        with caplog.at_level(logging.WARNING):
            found = _walk_corpus_source(source, tmp_path)
        assert found == []
        assert "does not exist" in caplog.text

    def test_non_file_entries_skipped(self, tmp_path: Path):
        """Directories matching the glob pattern are skipped."""
        corpus = tmp_path / "corpus" / "d"
        _populate_tree(corpus, {"file.md": "content"})
        # Create a directory named "subdir.md" — should not appear
        (corpus / "subdir.md").mkdir()
        source = CorpusSource(name="d", path="corpus/d")
        found = _walk_corpus_source(source, tmp_path)
        assert all(f.relative_path != "subdir.md" for f in found)

    def test_unsupported_extension_skipped(self, tmp_path: Path):
        """Files with unsupported extensions (language=None) are skipped."""
        corpus = tmp_path / "corpus" / "ext"
        _populate_tree(corpus, {
            "good.md": "markdown",
            "bad.txt": "text file",
            "bad.json": '{"key": "val"}',
        })
        source = CorpusSource(
            name="ext",
            path="corpus/ext",
            include=["**/*"],  # include everything
        )
        found = _walk_corpus_source(source, tmp_path)
        rel_paths = [f.relative_path for f in found]
        assert "good.md" in rel_paths
        assert "bad.txt" not in rel_paths
        assert "bad.json" not in rel_paths


# ---------------------------------------------------------------------------
# _walk_code_repo
# ---------------------------------------------------------------------------


class TestWalkCodeRepo:
    def test_discovers_code_files(self, tmp_path: Path):
        repo = tmp_path / "myrepo"
        _populate_tree(repo, {
            "main.go": "package main",
            "lib/util.go": "package lib",
            "README.md": "# My Repo",
        })
        cr = CodeRepo(name="myrepo", path=str(repo), language="go")
        found = _walk_code_repo(cr)
        rel_paths = sorted(f.relative_path for f in found)
        # All supported files found: .go and .md
        assert "main.go" in rel_paths
        assert "lib/util.go" in rel_paths
        assert "README.md" in rel_paths

    def test_fields_populated(self, tmp_path: Path):
        repo = tmp_path / "repo"
        _populate_tree(repo, {"src/lib.rs": "fn main() {}"})
        cr = CodeRepo(name="test-repo", path=str(repo), language="rust")
        found = _walk_code_repo(cr)
        assert len(found) == 1
        f = found[0]
        assert f.source_name == "test-repo"
        assert f.repository == "test-repo"
        assert f.language == "rust"
        assert f.relative_path == "src/lib.rs"
        assert f.absolute_path == repo / "src" / "lib.rs"
        assert f.size_bytes > 0
        assert f.mtime_ns > 0

    def test_exclude_patterns(self, tmp_path: Path):
        repo = tmp_path / "excl"
        _populate_tree(repo, {
            "src/good.py": "# good",
            "vendor/dep.py": "# vendor",
            "tests/test_foo.py": "# test",
        })
        cr = CodeRepo(
            name="excl",
            path=str(repo),
            language="python",
            exclude=["vendor/*", "tests/*"],
        )
        found = _walk_code_repo(cr)
        rel_paths = [f.relative_path for f in found]
        assert "src/good.py" in rel_paths
        assert "vendor/dep.py" not in rel_paths
        assert "tests/test_foo.py" not in rel_paths

    def test_include_patterns(self, tmp_path: Path):
        repo = tmp_path / "inc"
        _populate_tree(repo, {
            "src/app.go": "package main",
            "src/util.go": "package main",
            "docs/guide.md": "# Guide",
        })
        cr = CodeRepo(
            name="inc",
            path=str(repo),
            language="go",
            include=["src/**/*.go"],  # only .go files under src/
        )
        found = _walk_code_repo(cr)
        rel_paths = [f.relative_path for f in found]
        assert "src/app.go" in rel_paths
        assert "src/util.go" in rel_paths
        assert "docs/guide.md" not in rel_paths

    def test_missing_directory_returns_empty(self, tmp_path: Path, caplog):
        cr = CodeRepo(name="gone", path=str(tmp_path / "nonexistent"), language="go")
        with caplog.at_level(logging.WARNING):
            found = _walk_code_repo(cr)
        assert found == []
        assert "does not exist" in caplog.text

    def test_language_detection_filters(self, tmp_path: Path):
        """Only .py, .go, .rs, .md are discovered; others skipped."""
        repo = tmp_path / "langtest"
        _populate_tree(repo, {
            "main.py": "print('hello')",
            "main.go": "package main",
            "lib.rs": "fn main() {}",
            "README.md": "# readme",
            "config.toml": "[section]",
            "data.json": "{}",
            "style.css": "body {}",
        })
        cr = CodeRepo(name="langtest", path=str(repo), language="mixed")
        found = _walk_code_repo(cr)
        rel_paths = sorted(f.relative_path for f in found)
        assert "main.py" in rel_paths
        assert "main.go" in rel_paths
        assert "lib.rs" in rel_paths
        assert "README.md" in rel_paths
        assert "config.toml" not in rel_paths
        assert "data.json" not in rel_paths
        assert "style.css" not in rel_paths


# ---------------------------------------------------------------------------
# walk_sources (integration)
# ---------------------------------------------------------------------------


class TestWalkSources:
    def test_yields_discovered_files(self, tmp_path: Path):
        corpus = tmp_path / "corpus" / "ethresearch"
        _populate_tree(corpus, {"topic.md": "# Topic"})

        settings = _make_settings(
            tmp_path,
            corpus_sources=[
                CorpusSource(name="ethresearch", path="corpus/ethresearch"),
            ],
        )
        results = list(walk_sources(settings))
        assert len(results) == 1
        assert isinstance(results[0], DiscoveredFile)
        assert results[0].relative_path == "topic.md"

    def test_combines_corpus_and_code(self, tmp_path: Path):
        corpus = tmp_path / "corpus" / "docs"
        _populate_tree(corpus, {"readme.md": "# Docs"})

        repo = tmp_path / "myrepo"
        _populate_tree(repo, {"main.py": "print('hello')"})

        settings = _make_settings(
            tmp_path,
            corpus_sources=[
                CorpusSource(name="docs", path="corpus/docs"),
            ],
            code_repos=[
                CodeRepo(name="myrepo", path=str(repo), language="python"),
            ],
        )
        results = list(walk_sources(settings))
        sources = {f.source_name for f in results}
        assert "docs" in sources
        assert "myrepo" in sources

    def test_sorted_by_source_then_path(self, tmp_path: Path):
        corpus_a = tmp_path / "corpus" / "aaa"
        corpus_b = tmp_path / "corpus" / "zzz"
        _populate_tree(corpus_a, {"z.md": "z", "a.md": "a"})
        _populate_tree(corpus_b, {"b.md": "b"})

        settings = _make_settings(
            tmp_path,
            corpus_sources=[
                CorpusSource(name="zzz", path="corpus/zzz"),
                CorpusSource(name="aaa", path="corpus/aaa"),
            ],
        )
        results = list(walk_sources(settings))
        keys = [(f.source_name, f.relative_path) for f in results]
        assert keys == sorted(keys)

    def test_empty_sources(self, tmp_path: Path):
        settings = _make_settings(tmp_path)
        results = list(walk_sources(settings))
        assert results == []

    def test_multiple_corpus_sources(self, tmp_path: Path):
        for name in ("alpha", "beta"):
            d = tmp_path / "corpus" / name
            _populate_tree(d, {"doc.md": f"# {name}"})

        settings = _make_settings(
            tmp_path,
            corpus_sources=[
                CorpusSource(name="alpha", path="corpus/alpha"),
                CorpusSource(name="beta", path="corpus/beta"),
            ],
        )
        results = list(walk_sources(settings))
        assert len(results) == 2
        names = {f.source_name for f in results}
        assert names == {"alpha", "beta"}

    def test_corpus_has_empty_repository_field(self, tmp_path: Path):
        """Corpus files always have repository == '' ."""
        corpus = tmp_path / "corpus" / "s"
        _populate_tree(corpus, {"f.md": "text"})
        settings = _make_settings(
            tmp_path,
            corpus_sources=[CorpusSource(name="s", path="corpus/s")],
        )
        results = list(walk_sources(settings))
        assert all(f.repository == "" for f in results)

    def test_code_repo_has_repository_field(self, tmp_path: Path):
        """Code repo files have repository == repo name."""
        repo = tmp_path / "geth"
        _populate_tree(repo, {"main.go": "package main"})
        settings = _make_settings(
            tmp_path,
            code_repos=[CodeRepo(name="geth", path=str(repo), language="go")],
        )
        results = list(walk_sources(settings))
        assert all(f.repository == "geth" for f in results)
