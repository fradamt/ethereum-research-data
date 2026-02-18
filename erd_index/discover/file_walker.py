"""Walk configured directories and yield files to index."""

from __future__ import annotations

import fnmatch
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from erd_index.discover.language_detector import detect_language
from erd_index.settings import CodeRepo, CorpusSource, Settings

__all__ = ["DiscoveredFile", "walk_sources"]

log = logging.getLogger(__name__)


@dataclass
class DiscoveredFile:
    """A file discovered on disk that is a candidate for indexing."""

    absolute_path: Path
    relative_path: str  # repo-relative path
    source_name: str  # e.g. "ethresearch", "go-ethereum"
    repository: str  # e.g. "go-ethereum", "" for corpus
    language: str  # "markdown", "python", "go", "rust"
    size_bytes: int
    mtime_ns: int


def walk_sources(settings: Settings) -> Iterator[DiscoveredFile]:
    """Yield all discoverable files from corpus sources and code repos.

    Files are yielded sorted by (source_name, relative_path) for deterministic
    ordering across runs.

    In addition to explicitly configured ``corpus_sources``, any subdirectory
    of ``corpus/`` that contains ``.md`` files and is not already covered by a
    configured source is auto-discovered as a drop-in corpus source.  This
    matches the QMD auto-discovery behaviour.
    """
    results: list[DiscoveredFile] = []

    all_corpus_sources = list(settings.corpus_sources)
    all_corpus_sources.extend(_auto_discover_corpus_sources(settings))

    for source in all_corpus_sources:
        results.extend(_walk_corpus_source(source, settings.project_root))

    for repo in settings.code_repos:
        results.extend(_walk_code_repo(repo, settings.project_root))

    results.sort(key=lambda f: (f.source_name, f.relative_path))
    yield from results


def _auto_discover_corpus_sources(settings: Settings) -> list[CorpusSource]:
    """Scan ``corpus/`` for subdirectories not already in *settings.corpus_sources*.

    A subdirectory qualifies as a drop-in corpus source if it contains at
    least one ``.md`` file (non-recursive check for speed).
    """
    corpus_root = settings.project_root / settings.corpus_dir
    if not corpus_root.is_dir():
        return []

    configured_names = {s.name for s in settings.corpus_sources}
    discovered: list[CorpusSource] = []

    for subdir in sorted(corpus_root.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name in configured_names:
            continue
        # Check if the directory contains .md files
        if any(subdir.glob("*.md")):
            relative_path = f"{settings.corpus_dir}/{subdir.name}"
            discovered.append(CorpusSource(
                name=subdir.name,
                path=relative_path,
            ))
            log.info(
                "Auto-discovered corpus source %r at %s",
                subdir.name,
                relative_path,
            )

    return discovered


def _walk_corpus_source(
    source: CorpusSource,
    project_root: Path,
) -> list[DiscoveredFile]:
    """Walk a single corpus source directory."""
    root = (project_root / source.path).resolve()
    if not root.is_dir():
        log.warning("Corpus source %r path does not exist: %s", source.name, root)
        return []

    found: list[DiscoveredFile] = []
    for pattern in source.include:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            rel = str(path.relative_to(root))
            if _is_excluded(rel, source.exclude):
                continue
            lang = detect_language(path)
            if lang is None:
                continue
            stat = path.stat()
            found.append(DiscoveredFile(
                absolute_path=path,
                relative_path=rel,
                source_name=source.name,
                repository="",
                language=lang,
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
            ))
    return found


def _walk_code_repo(repo: CodeRepo, project_root: Path | None = None) -> list[DiscoveredFile]:
    """Walk a single code repository."""
    root = repo.resolve_path(project_root)
    if not root.is_dir():
        log.warning("Code repo %r path does not exist: %s", repo.name, root)
        return []

    found: list[DiscoveredFile] = []
    for pattern in repo.include:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            rel = str(path.relative_to(root))
            if _is_excluded(rel, repo.exclude):
                continue
            lang = detect_language(path)
            if lang is None:
                continue
            stat = path.stat()
            found.append(DiscoveredFile(
                absolute_path=path,
                relative_path=rel,
                source_name=repo.name,
                repository=repo.name,
                language=lang,
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
            ))
    return found


def _is_excluded(relative_path: str, exclude_patterns: list[str]) -> bool:
    """Check whether *relative_path* matches any of the exclude glob patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
    return False
