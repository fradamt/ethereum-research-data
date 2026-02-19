"""Configuration loading: TOML file + environment variables + CLI overrides."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field, fields
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef,import-not-found]


@dataclass
class ChunkSizing:
    target_chars: int = 2800
    hard_max_chars: int = 5500
    small_fn_max_lines: int = 12
    small_fn_max_chars: int = 450
    small_group_target_chars: int = 2200
    small_group_max_members: int = 6


@dataclass
class MeilisearchConfig:
    url: str = "http://localhost:7700"
    master_key: str = ""
    index_name: str = "eth_chunks_v1"
    index_alias: str = "eth_chunks_current"
    batch_size: int = 1000


@dataclass
class CodeRepo:
    name: str
    path: str
    language: str
    include: list[str] = field(default_factory=lambda: ["**/*"])
    exclude: list[str] = field(default_factory=list)

    def resolve_path(self, project_root: Path | None = None) -> Path:
        """Return the absolute repo path.

        Paths starting with ``~`` are expanded via :py:meth:`Path.expanduser`.
        Relative paths (including ``../``) are resolved against *project_root*
        when provided, otherwise against the current working directory.
        """
        p = Path(self.path).expanduser()
        if not p.is_absolute() and project_root is not None:
            p = project_root / p
        return p.resolve()


@dataclass
class CorpusSource:
    name: str
    path: str
    include: list[str] = field(default_factory=lambda: ["**/*.md"])
    exclude: list[str] = field(default_factory=list)


@dataclass
class Settings:
    meili: MeilisearchConfig = field(default_factory=MeilisearchConfig)
    chunk_sizing: ChunkSizing = field(default_factory=ChunkSizing)
    corpus_dir: str = "corpus"
    data_dir: str = "data"
    graph_db: str = "data/graph.db"
    state_db: str = "data/index_state.db"
    schema_version: int = 2
    parser_version: str = "0.1.0"
    chunker_version: str = "0.1.0"
    code_repos: list[CodeRepo] = field(default_factory=list)
    corpus_sources: list[CorpusSource] = field(default_factory=list)
    project_root: Path = field(default_factory=lambda: Path.cwd())

    @property
    def resolved_data_dir(self) -> Path:
        return (self.project_root / self.data_dir).resolve()

    @property
    def resolved_corpus_dir(self) -> Path:
        return (self.project_root / self.corpus_dir).resolve()

    @property
    def resolved_graph_db(self) -> Path:
        return (self.project_root / self.graph_db).resolve()

    @property
    def resolved_state_db(self) -> Path:
        return (self.project_root / self.state_db).resolve()


def load_settings(
    config_path: Path | None = None,
    project_root: Path | None = None,
) -> Settings:
    """Load settings from TOML config, then overlay environment variables."""
    root = (project_root or Path.cwd()).resolve()

    if config_path is None:
        config_path = root / "config" / "indexer.toml"

    raw: dict = {}
    if config_path.exists():
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)
    else:
        logging.getLogger(__name__).warning(
            "Config file not found: %s; using defaults", config_path,
        )

    # Meilisearch
    meili_raw = raw.get("meilisearch", {})
    meili = MeilisearchConfig(
        url=os.environ.get("ERD_MEILI_URL", meili_raw.get("url", "http://localhost:7700")),
        master_key=os.environ.get("MEILI_MASTER_KEY", meili_raw.get("master_key", "")),
        index_name=meili_raw.get("index_name", "eth_chunks_v1"),
        index_alias=meili_raw.get("index_alias", "eth_chunks_current"),
        batch_size=int(meili_raw.get("batch_size", 1000)),
    )

    # Paths
    paths_raw = raw.get("paths", {})
    corpus_dir = paths_raw.get("corpus_dir", "corpus")
    data_dir = paths_raw.get("data_dir", "data")
    graph_db = paths_raw.get("graph_db", "data/graph.db")
    state_db = paths_raw.get("state_db", "data/index_state.db")

    # Chunk sizing — filter to known fields so unknown TOML keys don't
    # cause a TypeError in the ChunkSizing constructor.
    cs_raw = raw.get("chunk_sizing", {})
    known_fields = {f.name for f in fields(ChunkSizing)}
    chunk_sizing = ChunkSizing(**{k: int(v) for k, v in cs_raw.items() if k in known_fields})

    # Versions
    ver_raw = raw.get("versions", {})
    schema_version = int(ver_raw.get("schema_version", 1))
    parser_version = str(ver_raw.get("parser_version", "0.1.0"))
    chunker_version = str(ver_raw.get("chunker_version", "0.1.0"))

    # Code repos
    code_repos = [
        CodeRepo(
            name=r["name"],
            path=r["path"],
            language=r["language"],
            include=r.get("include", ["**/*"]),
            exclude=r.get("exclude", []),
        )
        for r in raw.get("code_repos", [])
    ]

    # Corpus sources
    corpus_sources = [
        CorpusSource(
            name=s["name"],
            path=s["path"],
            include=s.get("include", ["**/*.md"]),
            exclude=s.get("exclude", []),
        )
        for s in raw.get("corpus_sources", [])
    ]

    return Settings(
        meili=meili,
        chunk_sizing=chunk_sizing,
        corpus_dir=corpus_dir,
        data_dir=data_dir,
        graph_db=graph_db,
        state_db=state_db,
        schema_version=schema_version,
        parser_version=parser_version,
        chunker_version=chunker_version,
        code_repos=code_repos,
        corpus_sources=corpus_sources,
        project_root=root,
    )
