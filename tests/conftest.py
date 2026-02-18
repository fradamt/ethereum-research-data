"""Shared fixtures for erd_index tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from erd_index.settings import ChunkSizing, MeilisearchConfig, Settings

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def tmp_settings(tmp_path: Path) -> Settings:
    """Settings pointing to a temporary directory for isolated tests."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return Settings(
        meili=MeilisearchConfig(
            url="http://localhost:7700",
            index_name="test_chunks",
        ),
        chunk_sizing=ChunkSizing(),
        corpus_dir=str(tmp_path / "corpus"),
        data_dir=str(data_dir),
        graph_db=str(data_dir / "graph.db"),
        state_db=str(data_dir / "index_state.db"),
        project_root=tmp_path,
    )
