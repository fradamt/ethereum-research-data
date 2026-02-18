"""Tests for erd_index.index.meili_schema — index settings and schema version."""

from __future__ import annotations

from erd_index.index.meili_schema import SCHEMA_VERSION, get_index_settings


class TestGetIndexSettings:
    """get_index_settings returns a well-formed Meilisearch settings dict."""

    def test_returns_dict(self) -> None:
        settings = get_index_settings()
        assert isinstance(settings, dict)

    def test_has_required_top_level_keys(self) -> None:
        settings = get_index_settings()
        expected_keys = {
            "searchableAttributes",
            "filterableAttributes",
            "sortableAttributes",
            "distinctAttribute",
        }
        assert expected_keys.issubset(settings.keys())

    def test_searchable_attributes_include_expected_fields(self) -> None:
        searchable = get_index_settings()["searchableAttributes"]
        assert isinstance(searchable, list)
        # Core fields a user would search by
        for field in ("title", "text", "summary", "tags", "author", "path"):
            assert field in searchable, f"expected '{field}' in searchableAttributes"

    def test_searchable_attributes_include_code_fields(self) -> None:
        searchable = get_index_settings()["searchableAttributes"]
        for field in ("symbol_name", "symbol_qualname", "signature", "module_path"):
            assert field in searchable, f"expected code field '{field}' in searchableAttributes"

    def test_filterable_attributes_include_expected_fields(self) -> None:
        filterable = get_index_settings()["filterableAttributes"]
        assert isinstance(filterable, list)
        for field in (
            "source_kind",
            "chunk_kind",
            "source_name",
            "doc_id",
            "path",
            "author",
            "category",
            "eip",
            "eip_status",
            "schema_version",
            "content_hash",
            "dedupe_key",
        ):
            assert field in filterable, f"expected '{field}' in filterableAttributes"

    def test_filterable_attributes_include_code_fields(self) -> None:
        filterable = get_index_settings()["filterableAttributes"]
        for field in (
            "repository",
            "language",
            "symbol_id",
            "symbol_name",
            "symbol_kind",
            "symbol_qualname",
            "parent_symbol",
            "module_path",
            "visibility",
        ):
            assert field in filterable, f"expected code field '{field}' in filterableAttributes"

    def test_sortable_attributes_include_expected_fields(self) -> None:
        sortable = get_index_settings()["sortableAttributes"]
        assert isinstance(sortable, list)
        for field in (
            "source_date_ts",
            "indexed_at_ts",
            "influence_score",
            "views",
            "likes",
            "eip",
            "start_line",
        ):
            assert field in sortable, f"expected '{field}' in sortableAttributes"

    def test_distinct_attribute_is_dedupe_key(self) -> None:
        settings = get_index_settings()
        assert settings["distinctAttribute"] == "dedupe_key"

    def test_all_attributes_are_strings(self) -> None:
        """Every entry in every attribute list must be a plain string."""
        settings = get_index_settings()
        for key in ("searchableAttributes", "filterableAttributes", "sortableAttributes"):
            for item in settings[key]:
                assert isinstance(item, str), f"non-string in {key}: {item!r}"

    def test_no_duplicate_searchable_attributes(self) -> None:
        searchable = get_index_settings()["searchableAttributes"]
        assert len(searchable) == len(set(searchable))

    def test_no_duplicate_filterable_attributes(self) -> None:
        filterable = get_index_settings()["filterableAttributes"]
        assert len(filterable) == len(set(filterable))

    def test_no_duplicate_sortable_attributes(self) -> None:
        sortable = get_index_settings()["sortableAttributes"]
        assert len(sortable) == len(set(sortable))

    def test_returns_fresh_dict_each_call(self) -> None:
        """Callers should not share mutable state."""
        a = get_index_settings()
        b = get_index_settings()
        assert a == b
        assert a is not b


class TestSchemaVersion:
    """SCHEMA_VERSION is a positive integer used for migration detection."""

    def test_is_positive_integer(self) -> None:
        assert isinstance(SCHEMA_VERSION, int)
        assert SCHEMA_VERSION > 0

    def test_exported_in_all(self) -> None:
        from erd_index.index import meili_schema

        assert "SCHEMA_VERSION" in meili_schema.__all__
        assert "get_index_settings" in meili_schema.__all__
