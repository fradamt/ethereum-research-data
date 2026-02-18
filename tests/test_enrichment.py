"""Tests for forum_metadata, code_metadata, and dependency_extractor enrichment modules."""

from __future__ import annotations

import pytest

from erd_index.enrich.code_metadata import enrich_code_chunk
from erd_index.enrich.dependency_extractor import extract_dependencies
from erd_index.enrich.forum_metadata import enrich_forum_chunk
from erd_index.models import Chunk, ChunkKind, Language, SourceKind

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _forum_chunk(**overrides) -> Chunk:
    defaults = dict(
        source_kind=SourceKind.FORUM,
        chunk_kind=ChunkKind.MD_REPLY,
        source_name="ethresearch",
        language=Language.MARKDOWN,
        path="t/1234.md",
        text="some forum text",
        start_line=1,
        end_line=10,
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def _code_chunk(language: Language = Language.PYTHON, **overrides) -> Chunk:
    defaults = dict(
        source_kind=SourceKind.CODE,
        chunk_kind=ChunkKind.CODE_FUNCTION,
        source_name="test-repo",
        repository="test-repo",
        language=language,
        path="src/module.py",
        text="def foo(): pass",
        start_line=1,
        end_line=1,
        symbol_name="foo",
        symbol_kind="function",
    )
    defaults.update(overrides)
    return Chunk(**defaults)


# ===========================================================================
# enrich_forum_chunk
# ===========================================================================


class TestForumMetadata:
    def test_field_population(self):
        c = _forum_chunk()
        fm = {
            "topic_id": 1234,
            "post_number": 1,
            "author": "vbuterin",
            "category": "Sharding",
            "views": 5000,
            "likes": 120,
            "posts_count": 30,
            "research_thread": "danksharding",
            "url": "https://ethresear.ch/t/1234",
        }
        result = enrich_forum_chunk(c, fm)
        assert result.topic_id == 1234
        assert result.post_number == 1
        assert result.author == "vbuterin"
        assert result.category == "Sharding"
        assert result.views == 5000
        assert result.likes == 120
        assert result.posts_count == 30
        assert result.research_thread == "danksharding"
        assert result.url == "https://ethresear.ch/t/1234"

    def test_influence_score_formula(self):
        c = _forum_chunk()
        fm = {"likes": 100, "views": 2000, "posts_count": 10}
        result = enrich_forum_chunk(c, fm)
        expected = 100 * 2.0 + 2000 * 0.01 + 10 * 0.5
        assert result.influence_score == pytest.approx(expected)

    def test_influence_score_zero_engagement(self):
        c = _forum_chunk()
        result = enrich_forum_chunk(c, {"likes": 0, "views": 0, "posts_count": 0})
        assert result.influence_score == 0.0

    def test_no_frontmatter_uses_existing_values(self):
        c = _forum_chunk(likes=10, views=500, posts_count=5)
        result = enrich_forum_chunk(c)
        expected = 10 * 2.0 + 500 * 0.01 + 5 * 0.5
        assert result.influence_score == pytest.approx(expected)

    def test_source_date_from_frontmatter(self):
        c = _forum_chunk()
        fm = {"date": "2024-03-15"}
        result = enrich_forum_chunk(c, fm)
        assert result.source_date == "2024-03-15"

    def test_source_date_not_overwritten(self):
        c = _forum_chunk(source_date="2023-01-01")
        fm = {"date": "2024-03-15"}
        result = enrich_forum_chunk(c, fm)
        assert result.source_date == "2023-01-01"

    def test_returns_same_chunk(self):
        c = _forum_chunk()
        result = enrich_forum_chunk(c, {"likes": 1})
        assert result is c

    def test_non_numeric_values_handled(self):
        c = _forum_chunk()
        fm = {"likes": "not_a_number", "views": None, "posts_count": "10"}
        result = enrich_forum_chunk(c, fm)
        assert result.likes == 0
        assert result.views == 0
        assert result.posts_count == 10


# ===========================================================================
# enrich_code_chunk
# ===========================================================================


class TestCodeMetadataQualname:
    def test_full_qualname(self):
        c = _code_chunk(
            module_path="ethereum.vm",
            parent_symbol="EVM",
            symbol_name="run",
        )
        result = enrich_code_chunk(c)
        assert result.symbol_qualname == "ethereum.vm.EVM.run"

    def test_qualname_no_parent(self):
        c = _code_chunk(module_path="ethereum.vm", symbol_name="process_block")
        result = enrich_code_chunk(c)
        assert result.symbol_qualname == "ethereum.vm.process_block"

    def test_qualname_no_module(self):
        c = _code_chunk(module_path="", symbol_name="helper")
        result = enrich_code_chunk(c)
        assert result.symbol_qualname == "helper"

    def test_qualname_not_overwritten(self):
        c = _code_chunk(symbol_qualname="already.set")
        result = enrich_code_chunk(c)
        assert result.symbol_qualname == "already.set"


class TestCodeMetadataUsedImports:
    def test_filters_to_used(self):
        c = _code_chunk(
            text="x = Uint256(10)",
            imports=["from ethereum.base_types import Uint256", "from ethereum.utils import unused"],
        )
        result = enrich_code_chunk(c)
        assert "from ethereum.base_types import Uint256" in result.used_imports
        assert "from ethereum.utils import unused" not in result.used_imports

    def test_empty_imports(self):
        c = _code_chunk(text="x = 1", imports=[])
        result = enrich_code_chunk(c)
        assert result.used_imports == []

    def test_not_overwritten_when_set(self):
        c = _code_chunk(
            imports=["import os"],
            used_imports=["import os"],
            text="os.path.join()",
        )
        result = enrich_code_chunk(c)
        assert result.used_imports == ["import os"]


class TestCodeMetadataCalls:
    def test_basic_calls(self):
        c = _code_chunk(
            text="def foo():\n    bar()\n    baz.qux()\n",
        )
        result = enrich_code_chunk(c)
        assert "bar" in result.calls
        assert "baz.qux" in result.calls

    def test_excludes_control_keywords(self):
        c = _code_chunk(
            text="if(x):\n    for(y):\n        real_func(z)\n",
        )
        result = enrich_code_chunk(c)
        assert "real_func" in result.calls
        assert "if" not in result.calls
        assert "for" not in result.calls

    def test_calls_sorted(self):
        c = _code_chunk(text="zebra()\nalpha()\nmid()\n")
        result = enrich_code_chunk(c)
        assert result.calls == sorted(result.calls)

    def test_calls_deduplicated(self):
        c = _code_chunk(text="foo()\nfoo()\nfoo()\n")
        result = enrich_code_chunk(c)
        assert result.calls.count("foo") == 1


class TestCodeMetadataVisibility:
    # Python
    def test_python_public(self):
        c = _code_chunk(language=Language.PYTHON, symbol_name="process")
        assert enrich_code_chunk(c).visibility == "public"

    def test_python_single_underscore_private(self):
        c = _code_chunk(language=Language.PYTHON, symbol_name="_helper")
        assert enrich_code_chunk(c).visibility == "private"

    def test_python_dunder_private(self):
        c = _code_chunk(language=Language.PYTHON, symbol_name="__secret")
        assert enrich_code_chunk(c).visibility == "private"

    def test_python_dunder_magic_public(self):
        c = _code_chunk(language=Language.PYTHON, symbol_name="__init__")
        assert enrich_code_chunk(c).visibility == "public"

    # Go
    def test_go_uppercase_public(self):
        c = _code_chunk(language=Language.GO, symbol_name="Run", path="vm.go")
        assert enrich_code_chunk(c).visibility == "public"

    def test_go_lowercase_private(self):
        c = _code_chunk(language=Language.GO, symbol_name="run", path="vm.go")
        assert enrich_code_chunk(c).visibility == "private"

    # Rust
    def test_rust_pub_public(self):
        c = _code_chunk(
            language=Language.RUST,
            symbol_name="process",
            signature="pub fn process()",
            path="lib.rs",
        )
        assert enrich_code_chunk(c).visibility == "public"

    def test_rust_no_pub_private(self):
        c = _code_chunk(
            language=Language.RUST,
            symbol_name="helper",
            signature="fn helper()",
            path="lib.rs",
        )
        assert enrich_code_chunk(c).visibility == "private"

    def test_visibility_not_overwritten(self):
        c = _code_chunk(symbol_name="foo", visibility="protected")
        result = enrich_code_chunk(c)
        assert result.visibility == "protected"


# ===========================================================================
# extract_dependencies
# ===========================================================================


class TestDependencyPython:
    def test_from_import_used(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f():\n    x = Uint256(10)\n",
            symbol_qualname="mod.f",
            imports=["from ethereum.base_types import Uint256"],
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "ethereum.base_types.Uint256" in targets

    def test_from_import_unused_excluded(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f():\n    pass\n",
            symbol_qualname="mod.f",
            imports=["from ethereum.base_types import Uint256"],
        )
        deps = extract_dependencies(c)
        assert len(deps) == 0

    def test_import_with_alias(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f():\n    log.info('hi')\n",
            symbol_qualname="mod.f",
            imports=["import logging as log"],
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "logging" in targets

    def test_type_vs_import_relation(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f():\n    x = Uint256(1)\n    log.info('x')\n",
            symbol_qualname="mod.f",
            imports=[
                "from ethereum.base_types import Uint256",
                "import logging as log",
            ],
        )
        deps = extract_dependencies(c)
        dep_dict = {d[1]: d[2] for d in deps}
        assert dep_dict["ethereum.base_types.Uint256"] == "uses_type"
        assert dep_dict["logging"] == "imports"

    def test_from_symbol_fallback(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f():\n    x = Foo()\n",
            symbol_qualname="",
            symbol_name="f",
            path="src/mod.py",
            imports=["from bar import Foo"],
        )
        deps = extract_dependencies(c)
        assert deps[0][0] == "src/mod.py:f"


class TestDependencyGo:
    def test_go_import_used(self):
        c = _code_chunk(
            language=Language.GO,
            text='func run() {\n\tcommon.BytesToHash(data)\n}\n',
            symbol_qualname="vm.run",
            imports=['"github.com/ethereum/go-ethereum/common"'],
            path="vm.go",
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "github.com/ethereum/go-ethereum/common" in targets

    def test_go_import_unused_excluded(self):
        c = _code_chunk(
            language=Language.GO,
            text="func run() {\n\tx := 1\n}\n",
            symbol_qualname="vm.run",
            imports=['"github.com/ethereum/go-ethereum/common"'],
            path="vm.go",
        )
        deps = extract_dependencies(c)
        assert len(deps) == 0

    def test_go_aliased_import(self):
        c = _code_chunk(
            language=Language.GO,
            text='func run() {\n\tbig.NewInt(1)\n}\n',
            symbol_qualname="vm.run",
            imports=['big "math/big"'],
            path="vm.go",
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "math/big" in targets


class TestDependencyRust:
    def test_rust_use_used(self):
        c = _code_chunk(
            language=Language.RUST,
            text="fn process() {\n    let h: Hash256 = Hash256::zero();\n}\n",
            symbol_qualname="mod::process",
            imports=["use types::Hash256;"],
            path="lib.rs",
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "types::Hash256" in targets

    def test_rust_use_unused_excluded(self):
        c = _code_chunk(
            language=Language.RUST,
            text="fn process() {\n    let x = 1;\n}\n",
            symbol_qualname="mod::process",
            imports=["use types::Hash256;"],
            path="lib.rs",
        )
        deps = extract_dependencies(c)
        assert len(deps) == 0

    def test_rust_braced_import(self):
        c = _code_chunk(
            language=Language.RUST,
            text="fn f() {\n    let a = Foo::new();\n    let b = Bar::new();\n}\n",
            symbol_qualname="mod::f",
            imports=["use crate::types::{Foo, Bar};"],
            path="lib.rs",
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "crate::types::Foo" in targets
        assert "crate::types::Bar" in targets

    def test_rust_aliased_import(self):
        c = _code_chunk(
            language=Language.RUST,
            text="fn f() {\n    let x = H256::zero();\n}\n",
            symbol_qualname="mod::f",
            imports=["use types::{Hash256 as H256};"],
            path="lib.rs",
        )
        deps = extract_dependencies(c)
        targets = {d[1] for d in deps}
        assert "types::Hash256" in targets


class TestDependencyEdgeCases:
    def test_unsupported_language(self):
        c = _code_chunk(language=Language.MARKDOWN, text="# heading")
        deps = extract_dependencies(c)
        assert deps == []

    def test_empty_imports(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f(): pass",
            symbol_qualname="mod.f",
            imports=[],
        )
        deps = extract_dependencies(c)
        assert deps == []

    def test_no_duplicate_edges(self):
        c = _code_chunk(
            language=Language.PYTHON,
            text="def f():\n    Foo()\n    Foo()\n    Foo()\n",
            symbol_qualname="mod.f",
            imports=["from bar import Foo"],
        )
        deps = extract_dependencies(c)
        assert len(deps) == 1
