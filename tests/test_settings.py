"""Tests for erd_index/settings.py — configuration loading."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

from erd_index.settings import (
    ChunkSizing,
    CodeRepo,
    CorpusSource,
    MeilisearchConfig,
    Settings,
    load_settings,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_toml(path: Path, content: str) -> Path:
    """Write TOML content to a file and return the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ===================================================================
# ChunkSizing defaults
# ===================================================================


class TestChunkSizing:
    def test_defaults(self) -> None:
        cs = ChunkSizing()
        assert cs.target_chars == 2800
        assert cs.hard_max_chars == 5500
        assert cs.small_fn_max_lines == 12
        assert cs.small_fn_max_chars == 450
        assert cs.small_group_target_chars == 2200
        assert cs.small_group_max_members == 6

    def test_override(self) -> None:
        cs = ChunkSizing(target_chars=3000, hard_max_chars=6000)
        assert cs.target_chars == 3000
        assert cs.hard_max_chars == 6000
        # Other fields remain default
        assert cs.small_fn_max_lines == 12


# ===================================================================
# MeilisearchConfig defaults
# ===================================================================


class TestMeilisearchConfig:
    def test_defaults(self) -> None:
        m = MeilisearchConfig()
        assert m.url == "http://localhost:7700"
        assert m.master_key == ""
        assert m.index_name == "eth_chunks_v1"
        assert m.index_alias == "eth_chunks_current"
        assert m.batch_size == 1000


# ===================================================================
# CodeRepo.resolve_path
# ===================================================================


class TestCodeRepoResolvePath:
    def test_absolute_path(self, tmp_path: Path) -> None:
        repo = CodeRepo(name="geth", path=str(tmp_path / "go-ethereum"), language="go")
        resolved = repo.resolve_path(project_root=tmp_path)
        assert resolved == (tmp_path / "go-ethereum").resolve()
        assert resolved.is_absolute()

    def test_relative_path_with_project_root(self, tmp_path: Path) -> None:
        repo = CodeRepo(name="geth", path="../go-ethereum", language="go")
        resolved = repo.resolve_path(project_root=tmp_path)
        assert resolved == (tmp_path / "../go-ethereum").resolve()
        assert resolved.is_absolute()

    def test_relative_path_without_project_root(self) -> None:
        """Without project_root, relative paths resolve against cwd."""
        repo = CodeRepo(name="geth", path="go-ethereum", language="go")
        resolved = repo.resolve_path(project_root=None)
        assert resolved == Path("go-ethereum").resolve()
        assert resolved.is_absolute()

    def test_tilde_expansion(self) -> None:
        repo = CodeRepo(name="geth", path="~/go-ethereum", language="go")
        resolved = repo.resolve_path()
        assert resolved == Path("~/go-ethereum").expanduser().resolve()
        assert "~" not in str(resolved)

    def test_absolute_path_ignores_project_root(self, tmp_path: Path) -> None:
        """An absolute path should not be joined with project_root."""
        abs_path = "/opt/repos/go-ethereum"
        repo = CodeRepo(name="geth", path=abs_path, language="go")
        resolved = repo.resolve_path(project_root=tmp_path)
        assert resolved == Path(abs_path).resolve()

    def test_default_include_and_exclude(self) -> None:
        repo = CodeRepo(name="geth", path="/tmp/geth", language="go")
        assert repo.include == ["**/*"]
        assert repo.exclude == []


# ===================================================================
# CorpusSource
# ===================================================================


class TestCorpusSource:
    def test_default_include(self) -> None:
        cs = CorpusSource(name="ethresearch", path="corpus/ethresearch")
        assert cs.include == ["**/*.md"]
        assert cs.exclude == []


# ===================================================================
# Settings — resolved properties
# ===================================================================


class TestSettingsResolved:
    def test_resolved_data_dir(self, tmp_path: Path) -> None:
        s = Settings(data_dir="data", project_root=tmp_path)
        assert s.resolved_data_dir == (tmp_path / "data").resolve()

    def test_resolved_corpus_dir(self, tmp_path: Path) -> None:
        s = Settings(corpus_dir="corpus", project_root=tmp_path)
        assert s.resolved_corpus_dir == (tmp_path / "corpus").resolve()

    def test_resolved_graph_db(self, tmp_path: Path) -> None:
        s = Settings(graph_db="data/graph.db", project_root=tmp_path)
        assert s.resolved_graph_db == (tmp_path / "data" / "graph.db").resolve()

    def test_resolved_state_db(self, tmp_path: Path) -> None:
        s = Settings(state_db="data/index_state.db", project_root=tmp_path)
        assert s.resolved_state_db == (tmp_path / "data" / "index_state.db").resolve()

    def test_resolved_paths_are_absolute(self, tmp_path: Path) -> None:
        s = Settings(project_root=tmp_path)
        assert s.resolved_data_dir.is_absolute()
        assert s.resolved_corpus_dir.is_absolute()
        assert s.resolved_graph_db.is_absolute()
        assert s.resolved_state_db.is_absolute()


# ===================================================================
# load_settings — valid TOML
# ===================================================================


class TestLoadSettingsValid:
    def test_full_config(self, tmp_path: Path) -> None:
        toml_content = """\
[meilisearch]
url = "http://meili.example.com:7700"
master_key = "test-key-123"
index_name = "my_index"
index_alias = "my_alias"
batch_size = 500

[paths]
corpus_dir = "my_corpus"
data_dir = "my_data"
graph_db = "my_data/graph.db"
state_db = "my_data/state.db"

[chunk_sizing]
target_chars = 3000
hard_max_chars = 6000

[versions]
schema_version = 2
parser_version = "0.2.0"
chunker_version = "0.3.0"

[[code_repos]]
name = "go-ethereum"
path = "../go-ethereum"
language = "go"
include = ["**/*.go"]
exclude = ["vendor/**"]

[[corpus_sources]]
name = "ethresearch"
path = "corpus/ethresearch"
include = ["**/*.md"]
"""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", toml_content)
        # Clear env vars that would override TOML values
        env = {k: v for k, v in os.environ.items()
               if k not in ("MEILI_MASTER_KEY", "ERD_MEILI_URL")}
        with patch.dict(os.environ, env, clear=True):
            settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.meili.url == "http://meili.example.com:7700"
        assert settings.meili.master_key == "test-key-123"
        assert settings.meili.index_name == "my_index"
        assert settings.meili.index_alias == "my_alias"
        assert settings.meili.batch_size == 500

        assert settings.corpus_dir == "my_corpus"
        assert settings.data_dir == "my_data"
        assert settings.graph_db == "my_data/graph.db"
        assert settings.state_db == "my_data/state.db"

        assert settings.chunk_sizing.target_chars == 3000
        assert settings.chunk_sizing.hard_max_chars == 6000
        # Unspecified fields remain defaults
        assert settings.chunk_sizing.small_fn_max_lines == 12

        assert settings.schema_version == 2
        assert settings.parser_version == "0.2.0"
        assert settings.chunker_version == "0.3.0"

        assert len(settings.code_repos) == 1
        assert settings.code_repos[0].name == "go-ethereum"
        assert settings.code_repos[0].language == "go"
        assert settings.code_repos[0].include == ["**/*.go"]
        assert settings.code_repos[0].exclude == ["vendor/**"]

        assert len(settings.corpus_sources) == 1
        assert settings.corpus_sources[0].name == "ethresearch"

    def test_minimal_config(self, tmp_path: Path) -> None:
        """An empty TOML file should produce all defaults."""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", "")
        env = {k: v for k, v in os.environ.items()
               if k not in ("MEILI_MASTER_KEY", "ERD_MEILI_URL")}
        with patch.dict(os.environ, env, clear=True):
            settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.meili.url == "http://localhost:7700"
        assert settings.meili.master_key == ""
        assert settings.chunk_sizing.target_chars == 2800
        assert settings.corpus_dir == "corpus"
        assert settings.data_dir == "data"
        assert settings.code_repos == []
        assert settings.corpus_sources == []

    def test_project_root_set(self, tmp_path: Path) -> None:
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", "")
        settings = load_settings(config_path=config_path, project_root=tmp_path)
        assert settings.project_root == tmp_path.resolve()


# ===================================================================
# load_settings — missing config file
# ===================================================================


class TestLoadSettingsMissingConfig:
    def test_warns_and_uses_defaults(self, tmp_path: Path, caplog) -> None:
        """A missing config file should log a warning and use defaults."""
        missing = tmp_path / "nonexistent.toml"
        env = {k: v for k, v in os.environ.items()
               if k not in ("MEILI_MASTER_KEY", "ERD_MEILI_URL")}
        with patch.dict(os.environ, env, clear=True), caplog.at_level("WARNING"):
            settings = load_settings(config_path=missing, project_root=tmp_path)

        assert "not found" in caplog.text.lower() or "Config file" in caplog.text
        assert settings.meili.url == "http://localhost:7700"
        assert settings.chunk_sizing.target_chars == 2800

    def test_default_config_path(self, tmp_path: Path, caplog) -> None:
        """With no config_path, it looks for config/indexer.toml under project_root."""
        env = {k: v for k, v in os.environ.items()
               if k not in ("MEILI_MASTER_KEY", "ERD_MEILI_URL")}
        with patch.dict(os.environ, env, clear=True), caplog.at_level("WARNING"):
            settings = load_settings(project_root=tmp_path)

        # Should warn because tmp_path/config/indexer.toml doesn't exist
        assert settings.meili.url == "http://localhost:7700"


# ===================================================================
# load_settings — environment variable overrides
# ===================================================================


class TestLoadSettingsEnvOverrides:
    def test_meili_master_key_from_env(self, tmp_path: Path) -> None:
        config_path = _write_toml(
            tmp_path / "config" / "indexer.toml",
            '[meilisearch]\nmaster_key = "from-toml"',
        )
        with patch.dict(os.environ, {"MEILI_MASTER_KEY": "from-env"}):
            settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.meili.master_key == "from-env"

    def test_meili_url_from_env(self, tmp_path: Path) -> None:
        config_path = _write_toml(
            tmp_path / "config" / "indexer.toml",
            '[meilisearch]\nurl = "http://toml:7700"',
        )
        with patch.dict(os.environ, {"ERD_MEILI_URL": "http://env:7700"}):
            settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.meili.url == "http://env:7700"

    def test_env_overrides_with_no_toml_value(self, tmp_path: Path) -> None:
        """Env vars should work even when the TOML section is absent."""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", "")
        with patch.dict(os.environ, {"MEILI_MASTER_KEY": "env-key"}):
            settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.meili.master_key == "env-key"

    def test_no_env_uses_toml_value(self, tmp_path: Path) -> None:
        """Without env vars, TOML values are used."""
        config_path = _write_toml(
            tmp_path / "config" / "indexer.toml",
            '[meilisearch]\nmaster_key = "toml-key"',
        )
        # Ensure env vars are not set
        env = {
            k: v for k, v in os.environ.items()
            if k not in ("MEILI_MASTER_KEY", "ERD_MEILI_URL")
        }
        with patch.dict(os.environ, env, clear=True):
            settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.meili.master_key == "toml-key"


# ===================================================================
# load_settings — unknown TOML keys filtered
# ===================================================================


class TestLoadSettingsUnknownKeys:
    def test_unknown_chunk_sizing_keys_ignored(self, tmp_path: Path) -> None:
        """Unknown keys in [chunk_sizing] should be silently filtered out."""
        toml_content = """\
[chunk_sizing]
target_chars = 3000
unknown_future_key = 999
another_unknown = 42
"""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", toml_content)
        settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.chunk_sizing.target_chars == 3000
        # Should not raise and defaults for other fields are intact
        assert settings.chunk_sizing.hard_max_chars == 5500

    def test_all_chunk_sizing_fields_accepted(self, tmp_path: Path) -> None:
        toml_content = """\
[chunk_sizing]
target_chars = 3000
hard_max_chars = 6000
small_fn_max_lines = 15
small_fn_max_chars = 500
small_group_target_chars = 2500
small_group_max_members = 8
"""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", toml_content)
        settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert settings.chunk_sizing.target_chars == 3000
        assert settings.chunk_sizing.hard_max_chars == 6000
        assert settings.chunk_sizing.small_fn_max_lines == 15
        assert settings.chunk_sizing.small_fn_max_chars == 500
        assert settings.chunk_sizing.small_group_target_chars == 2500
        assert settings.chunk_sizing.small_group_max_members == 8


# ===================================================================
# load_settings — code_repos and corpus_sources
# ===================================================================


class TestLoadSettingsCollections:
    def test_multiple_code_repos(self, tmp_path: Path) -> None:
        toml_content = """\
[[code_repos]]
name = "geth"
path = "/opt/go-ethereum"
language = "go"

[[code_repos]]
name = "lighthouse"
path = "/opt/lighthouse"
language = "rust"
include = ["**/*.rs"]
exclude = ["target/**"]
"""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", toml_content)
        settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert len(settings.code_repos) == 2
        assert settings.code_repos[0].name == "geth"
        assert settings.code_repos[0].include == ["**/*"]  # default
        assert settings.code_repos[1].name == "lighthouse"
        assert settings.code_repos[1].include == ["**/*.rs"]
        assert settings.code_repos[1].exclude == ["target/**"]

    def test_multiple_corpus_sources(self, tmp_path: Path) -> None:
        toml_content = """\
[[corpus_sources]]
name = "ethresearch"
path = "corpus/ethresearch"

[[corpus_sources]]
name = "magicians"
path = "corpus/magicians"
exclude = ["archive/**"]
"""
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", toml_content)
        settings = load_settings(config_path=config_path, project_root=tmp_path)

        assert len(settings.corpus_sources) == 2
        assert settings.corpus_sources[0].name == "ethresearch"
        assert settings.corpus_sources[0].include == ["**/*.md"]  # default
        assert settings.corpus_sources[1].exclude == ["archive/**"]

    def test_no_repos_or_sources(self, tmp_path: Path) -> None:
        config_path = _write_toml(tmp_path / "config" / "indexer.toml", "")
        settings = load_settings(config_path=config_path, project_root=tmp_path)
        assert settings.code_repos == []
        assert settings.corpus_sources == []
