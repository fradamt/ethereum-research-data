"""Tests for tree-sitter parsers: Python, Go, Rust."""

from __future__ import annotations

from pathlib import Path

import pytest

from erd_index.models import Language, SourceKind
from erd_index.parse.py_parser import parse_python_file
from erd_index.parse.go_parser import parse_go_file
from erd_index.parse.rust_parser import parse_rust_file

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Python parser
# ---------------------------------------------------------------------------


class TestPythonParser:
    @pytest.fixture()
    def units(self):
        source = (FIXTURES / "sample.py").read_text()
        return parse_python_file(
            source,
            path="eth2spec/phase0/sample.py",
            repository="consensus-specs",
            source_name="consensus-specs",
        )

    def _by_name(self, units, name: str):
        matches = [u for u in units if u.symbol_name == name]
        assert matches, f"No unit named {name!r} found"
        return matches[0]

    def test_unit_count(self, units):
        names = [u.symbol_name for u in units]
        assert "simple_function" in names
        assert "_private_helper" in names
        assert "MyClass" in names
        assert "__init__" in names
        assert "get_value" in names
        assert "create" in names
        assert len(units) == 6

    def test_source_metadata(self, units):
        for u in units:
            assert u.source_kind == SourceKind.CODE
            assert u.language == Language.PYTHON
            assert u.repository == "consensus-specs"
            assert u.path == "eth2spec/phase0/sample.py"

    def test_function_extraction(self, units):
        fn = self._by_name(units, "simple_function")
        assert fn.symbol_kind == "function"
        assert fn.parent_symbol == ""
        assert fn.docstring == "A simple function."
        assert "def simple_function" in fn.signature

    def test_private_function(self, units):
        fn = self._by_name(units, "_private_helper")
        assert fn.symbol_kind == "function"
        assert fn.parent_symbol == ""

    def test_class_extraction(self, units):
        cls = self._by_name(units, "MyClass")
        assert cls.symbol_kind == "class"
        assert cls.parent_symbol == ""
        assert cls.docstring == "A sample class."
        assert cls.signature == "class MyClass:"

    def test_method_with_parent(self, units):
        init = self._by_name(units, "__init__")
        assert init.symbol_kind == "method"
        assert init.parent_symbol == "MyClass"
        assert "MyClass.__init__" in init.symbol_qualname

    def test_method_docstring(self, units):
        gv = self._by_name(units, "get_value")
        assert gv.symbol_kind == "method"
        assert gv.parent_symbol == "MyClass"
        assert gv.docstring == "Return the value."

    def test_decorated_method(self, units):
        create = self._by_name(units, "create")
        assert create.symbol_kind == "method"
        assert create.parent_symbol == "MyClass"
        assert "@staticmethod" in create.signature
        assert "def create" in create.signature

    def test_imports_extracted(self, units):
        for u in units:
            import_strs = u.imports
            assert any("import os" in i for i in import_strs)
            assert any("from pathlib import Path" in i for i in import_strs)

    def test_module_path(self, units):
        for u in units:
            assert u.module_path == "eth2spec.phase0.sample"

    def test_qualname_with_parent(self, units):
        gv = self._by_name(units, "get_value")
        assert gv.symbol_qualname == "eth2spec.phase0.sample.MyClass.get_value"

    def test_qualname_standalone(self, units):
        fn = self._by_name(units, "simple_function")
        assert fn.symbol_qualname == "eth2spec.phase0.sample.simple_function"

    def test_line_numbers(self, units):
        cls = self._by_name(units, "MyClass")
        assert cls.start_line >= 1
        assert cls.end_line > cls.start_line

    def test_text_contains_body(self, units):
        fn = self._by_name(units, "simple_function")
        assert "return x + 1" in fn.text


# ---------------------------------------------------------------------------
# Go parser
# ---------------------------------------------------------------------------


class TestGoParser:
    @pytest.fixture()
    def units(self):
        source = (FIXTURES / "sample.go").read_text()
        return parse_go_file(
            source,
            path="core/vm/interpreter.go",
            repository="go-ethereum",
            source_name="go-ethereum",
        )

    def _by_name(self, units, name: str):
        matches = [u for u in units if u.symbol_name == name]
        assert matches, f"No unit named {name!r} found"
        return matches[0]

    def test_unit_count(self, units):
        names = [u.symbol_name for u in units]
        assert "Config" in names
        assert "Interpreter" in names
        assert "Runner" in names
        assert "Run" in names
        assert "opAdd" in names
        assert "min" in names

    def test_source_metadata(self, units):
        for u in units:
            assert u.source_kind == SourceKind.CODE
            assert u.language == Language.GO
            assert u.repository == "go-ethereum"

    def test_struct_type(self, units):
        cfg = self._by_name(units, "Config")
        assert cfg.symbol_kind == "struct"
        assert cfg.visibility == "public"
        assert "Config holds the EVM configuration." in cfg.docstring

    def test_interface_type(self, units):
        runner = self._by_name(units, "Runner")
        assert runner.symbol_kind == "interface"
        assert runner.visibility == "public"
        assert "Runner is implemented by types that can run contracts." in runner.docstring

    def test_method_with_receiver(self, units):
        run = self._by_name(units, "Run")
        assert run.symbol_kind == "method"
        assert run.parent_symbol == "Interpreter"
        assert run.visibility == "public"
        assert "Interpreter.Run" in run.symbol_qualname

    def test_function(self, units):
        add = self._by_name(units, "opAdd")
        assert add.symbol_kind == "function"
        assert add.parent_symbol == ""
        assert add.visibility == "private"
        assert "opAdd performs addition" in add.docstring

    def test_private_function(self, units):
        m = self._by_name(units, "min")
        assert m.symbol_kind == "function"
        assert m.visibility == "private"
        assert m.docstring == ""

    def test_doc_comment(self, units):
        run = self._by_name(units, "Run")
        assert "Run executes the given contract." in run.docstring

    def test_package_as_module_path(self, units):
        for u in units:
            assert u.module_path == "vm"

    def test_imports_extracted(self, units):
        cfg = self._by_name(units, "Config")
        assert len(cfg.imports) == 1  # Single import block
        assert "math/big" in cfg.imports[0]

    def test_signature_stops_at_brace(self, units):
        run = self._by_name(units, "Run")
        assert "{" not in run.signature
        assert "func (in *Interpreter) Run" in run.signature


# ---------------------------------------------------------------------------
# Rust parser
# ---------------------------------------------------------------------------


class TestRustParser:
    @pytest.fixture()
    def units(self):
        source = (FIXTURES / "sample.rs").read_text()
        return parse_rust_file(
            source,
            path="src/consensus/processor.rs",
            repository="lighthouse",
            source_name="lighthouse",
        )

    def _by_name(self, units, name: str):
        matches = [u for u in units if u.symbol_name == name]
        assert matches, f"No unit named {name!r} found"
        return matches[0]

    def _all_by_name(self, units, name: str):
        return [u for u in units if u.symbol_name == name]

    def test_unit_names(self, units):
        names = [u.symbol_name for u in units]
        assert "BlockHeader" in names
        assert "ProcessingError" in names
        assert "StateTransition" in names
        assert "BlockProcessor" in names  # impl block
        assert "new" in names
        assert "process_block" in names
        assert "validate" in names
        assert "helper" in names

    def test_source_metadata(self, units):
        for u in units:
            assert u.source_kind == SourceKind.CODE
            assert u.language == Language.RUST
            assert u.repository == "lighthouse"

    def test_struct(self, units):
        bh = self._by_name(units, "BlockHeader")
        assert bh.symbol_kind == "struct"
        assert bh.visibility == "public"
        assert "A beacon block header." in bh.docstring

    def test_enum(self, units):
        err = self._by_name(units, "ProcessingError")
        assert err.symbol_kind == "enum"
        assert err.visibility == "public"
        assert "Errors during block processing." in err.docstring

    def test_trait(self, units):
        st = self._by_name(units, "StateTransition")
        assert st.symbol_kind == "trait"
        assert st.visibility == "public"
        assert "Process state transitions." in st.docstring

    def test_trait_member_function(self, units):
        apply = self._by_name(units, "apply")
        assert apply.symbol_kind == "method"
        assert apply.parent_symbol == "StateTransition"
        assert "Apply a state transition" in apply.docstring

    def test_impl_block(self, units):
        impls = self._all_by_name(units, "BlockProcessor")
        assert len(impls) >= 1
        impl = impls[0]
        assert impl.symbol_kind == "impl"
        assert "Block processor implementation." in impl.docstring

    def test_impl_member_with_parent(self, units):
        new = self._by_name(units, "new")
        assert new.symbol_kind == "method"
        assert new.parent_symbol == "BlockProcessor"
        assert new.visibility == "public"
        assert "Create a new block processor." in new.docstring

    def test_private_impl_member(self, units):
        val = self._by_name(units, "validate")
        assert val.symbol_kind == "method"
        assert val.parent_symbol == "BlockProcessor"
        assert val.visibility == "private"

    def test_standalone_function(self, units):
        h = self._by_name(units, "helper")
        assert h.symbol_kind == "function"
        assert h.parent_symbol == ""
        assert h.visibility == "private"

    def test_use_declarations(self, units):
        bh = self._by_name(units, "BlockHeader")
        assert len(bh.imports) == 2
        assert any("std::collections::HashMap" in i for i in bh.imports)
        assert any("crate::types::BeaconState" in i for i in bh.imports)

    def test_module_path(self, units):
        for u in units:
            assert u.module_path == "consensus::processor"

    def test_qualname_with_parent(self, units):
        pb = self._by_name(units, "process_block")
        assert pb.symbol_qualname == "consensus::processor::BlockProcessor::process_block"

    def test_visibility_modifier(self, units):
        bh = self._by_name(units, "BlockHeader")
        assert bh.visibility == "public"
        h = self._by_name(units, "helper")
        assert h.visibility == "private"

    def test_signature_stops_before_brace(self, units):
        new = self._by_name(units, "new")
        assert "{" not in new.signature
        assert "fn new" in new.signature
