"""Pydantic models for chunks and documents.

These are the shared data types that all pipeline stages produce and consume.
The pipeline flow is: parse -> chunk -> enrich -> index.
"""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, computed_field


class SourceKind(str, Enum):
    FORUM = "forum"
    EIP = "eip"
    CODE = "code"
    GENERIC = "generic"


class ChunkKind(str, Enum):
    MD_HEADING = "md_heading"
    MD_REPLY = "md_reply"
    EIP_SECTION = "eip_section"
    CODE_FUNCTION = "code_function"
    CODE_STRUCT = "code_struct"
    CODE_GROUP = "code_group"


class Language(str, Enum):
    MARKDOWN = "markdown"
    PYTHON = "python"
    GO = "go"
    RUST = "rust"


# ---------------------------------------------------------------------------
# Parsed unit: output of parse/ stage, input to chunk/ stage
# ---------------------------------------------------------------------------


class ParsedUnit(BaseModel):
    """A logical unit extracted by a parser (a heading section, a function, etc.).

    Parsers emit these; chunkers may split/group them into Chunks.
    """

    source_kind: SourceKind
    language: Language
    source_name: str
    repository: str = ""
    path: str  # repo-relative file path
    title: str = ""

    # Content
    text: str
    start_line: int
    end_line: int

    # Markdown-specific
    heading_path: list[str] = Field(default_factory=list)

    # Code-specific
    symbol_name: str = ""
    symbol_kind: str = ""  # function, method, struct, enum, trait, impl, class
    symbol_qualname: str = ""
    signature: str = ""
    parent_symbol: str = ""
    module_path: str = ""
    visibility: str = ""
    imports: list[str] = Field(default_factory=list)
    docstring: str = ""

    # Forum-specific
    topic_id: int | None = None
    post_number: int | None = None
    author: str = ""
    category: str = ""

    # Frontmatter (any source)
    frontmatter: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Chunk: output of chunk/ stage, input to enrich/ and index/ stages
# ---------------------------------------------------------------------------


class Chunk(BaseModel):
    """A chunk ready for enrichment and indexing.

    Each chunk maps to one Meilisearch document and optionally one graph node.
    """

    # Identity
    source_kind: SourceKind
    chunk_kind: ChunkKind
    source_name: str
    repository: str = ""
    language: Language
    path: str
    title: str = ""

    # Content
    text: str
    start_line: int
    end_line: int

    # Markdown
    heading_path: list[str] = Field(default_factory=list)

    # Code
    symbol_name: str = ""
    symbol_kind: str = ""
    symbol_qualname: str = ""
    signature: str = ""
    parent_symbol: str = ""
    module_path: str = ""
    visibility: str = ""
    imports: list[str] = Field(default_factory=list)
    used_imports: list[str] = Field(default_factory=list)
    calls: list[str] = Field(default_factory=list)
    member_symbols: list[str] = Field(default_factory=list)  # for code_group chunks

    # Forum
    topic_id: int | None = None
    post_number: int | None = None
    author: str = ""
    category: str = ""
    research_thread: str = ""
    views: int = 0
    likes: int = 0
    posts_count: int = 0
    influence_score: float = 0.0

    # EIP
    eip: int | None = None
    eip_status: str = ""
    eip_type: str = ""
    eip_category: str = ""
    requires_eips: list[int] = Field(default_factory=list)
    supersedes_eips: list[int] = Field(default_factory=list)
    replaces_eips: list[int] = Field(default_factory=list)

    # Cross-cutting enrichment
    tags: list[str] = Field(default_factory=list)
    mentions_eips: list[int] = Field(default_factory=list)
    url: str = ""
    summary: str = ""
    source_date: str = ""
    source_date_ts: int = 0

    # Split metadata (for large functions split into parts)
    part_index: int | None = None
    part_count: int | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def content_hash(self) -> str:
        """SHA-256 of normalized chunk text (first 16 hex chars)."""
        normalized = self.text.strip().encode("utf-8")
        return hashlib.sha256(normalized).hexdigest()[:16]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def doc_id(self) -> str:
        """Parent document identifier."""
        if self.source_kind == SourceKind.FORUM:
            if self.topic_id is not None:
                return f"forum:{self.source_name}:{self.topic_id}"
            return f"doc:{self.source_name}:{self.path}"
        if self.source_kind == SourceKind.EIP:
            return f"eip:{self.eip}" if self.eip is not None else f"eip:unknown:{self.path}"
        if self.source_kind == SourceKind.GENERIC:
            return f"doc:{self.source_name}:{self.path}"
        return f"code:{self.repository}:{self.path}"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def chunk_id(self) -> str:
        """Deterministic chunk ID: source:path:start:end:content_hash."""
        parts = [self.source_name, self.path, str(self.start_line), str(self.end_line)]
        if self.part_index is not None:
            parts.append(f"p{self.part_index}")
        base = ":".join(parts)
        return f"{base}:{self.content_hash}"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def dedupe_key(self) -> str:
        """Stable deduplication key (without content hash, so same logical
        position deduplicates across minor edits)."""
        parts = [self.source_name, self.path, str(self.start_line), str(self.end_line)]
        if self.part_index is not None:
            parts.append(f"p{self.part_index}")
        return ":".join(parts)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def node_id(self) -> str:
        """Graph node identifier."""
        if self.symbol_name:
            return f"{self.repository}:{self.path}:{self.symbol_qualname or self.symbol_name}"
        if self.eip is not None:
            if self.heading_path:
                # Use full heading path to avoid collisions between sections
                # with the same final heading (e.g., "Parameters" under
                # different parent headings).
                anchor = "/".join(
                    h.lower().replace(" ", "-") for h in self.heading_path
                )
                return f"eip:{self.eip}:{anchor}"
            return f"eip:{self.eip}"
        if self.topic_id is not None:
            return f"forum:{self.source_name}:{self.topic_id}:{self.post_number or 0}"
        return f"{self.source_name}:{self.path}:{self.start_line}"
