"""Tests for erd_index.search_cli — Meilisearch search CLI.

All HTTP interactions are mocked so tests run without a server.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from erd_index.search_cli import (
    DEFAULT_DISTINCT,
    DEFAULT_FIELDS,
    DEFAULT_LIMIT,
    DEFAULT_MIN_TEXT_LENGTH,
    DEFAULT_SEMANTIC_RATIO,
    build_parser,
    build_search_params,
    format_hit,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_query(argv: list[str]) -> object:
    """Parse a query subcommand and return the namespace."""
    parser = build_parser()
    return parser.parse_args(["query", *argv])


# ===================================================================
# build_search_params
# ===================================================================


class TestBuildSearchParams:
    """build_search_params constructs the Meilisearch search payload."""

    def test_minimal_query(self) -> None:
        args = _parse_query(["hello world"])
        params = build_search_params(args)
        assert params["q"] == "hello world"
        assert params["limit"] == DEFAULT_LIMIT
        assert "hybrid" not in params  # keyword by default
        assert params["distinct"] == DEFAULT_DISTINCT
        fields = [f.strip() for f in DEFAULT_FIELDS.split(",")]
        assert params["attributesToRetrieve"] == fields

    def test_custom_limit(self) -> None:
        args = _parse_query(["test", "--limit", "5"])
        params = build_search_params(args)
        assert params["limit"] == 5

    def test_source_kind_filter(self) -> None:
        args = _parse_query(["test", "--source-kind", "eip"])
        params = build_search_params(args)
        assert 'source_kind = "eip"' in params["filter"]

    def test_source_name_filter(self) -> None:
        args = _parse_query(["test", "--source-name", "ethresear.ch"])
        params = build_search_params(args)
        assert 'source_name = "ethresear.ch"' in params["filter"]

    def test_author_filter(self) -> None:
        args = _parse_query(["test", "--author", "vbuterin"])
        params = build_search_params(args)
        assert 'author = "vbuterin"' in params["filter"]

    def test_eip_filter(self) -> None:
        args = _parse_query(["test", "--eip", "4844"])
        params = build_search_params(args)
        assert "eip = 4844" in params["filter"]

    def test_eip_status_filter(self) -> None:
        args = _parse_query(["test", "--eip-status", "Final"])
        params = build_search_params(args)
        assert 'eip_status = "Final"' in params["filter"]

    def test_repo_filter(self) -> None:
        args = _parse_query(["test", "--repo", "go-ethereum"])
        params = build_search_params(args)
        assert 'repository = "go-ethereum"' in params["filter"]

    def test_raw_filter(self) -> None:
        args = _parse_query(["test", "--filter", "source_date_ts > 1700000000"])
        params = build_search_params(args)
        assert "source_date_ts > 1700000000" in params["filter"]

    def test_combined_filters(self) -> None:
        args = _parse_query([
            "test",
            "--source-kind", "forum",
            "--author", "vbuterin",
            "--filter", "source_date_ts > 1700000000",
        ])
        params = build_search_params(args)
        parts = params["filter"].split(" AND ")
        assert len(parts) == 3
        assert 'source_kind = "forum"' in parts
        assert 'author = "vbuterin"' in parts
        assert "source_date_ts > 1700000000" in parts

    def test_code_excluded_by_default(self) -> None:
        args = _parse_query(["test"])
        params = build_search_params(args)
        assert params["filter"] == "source_kind != 'code'"

    def test_include_code_removes_exclusion(self) -> None:
        args = _parse_query(["test", "--include-code"])
        params = build_search_params(args)
        assert "filter" not in params

    def test_include_code_with_other_filters(self) -> None:
        args = _parse_query(["test", "--include-code", "--author", "vbuterin"])
        params = build_search_params(args)
        assert params["filter"] == 'author = "vbuterin"'
        assert "source_kind" not in params["filter"]

    def test_source_kind_code_overrides_exclusion(self) -> None:
        args = _parse_query(["test", "--source-kind", "code"])
        params = build_search_params(args)
        assert params["filter"] == 'source_kind = "code"'

    def test_sort(self) -> None:
        args = _parse_query(["test", "--sort", "source_date_ts:desc"])
        params = build_search_params(args)
        assert params["sort"] == ["source_date_ts:desc"]

    def test_no_sort_by_default(self) -> None:
        args = _parse_query(["test"])
        params = build_search_params(args)
        assert "sort" not in params

    def test_custom_fields(self) -> None:
        args = _parse_query(["test", "--fields", "title,url"])
        params = build_search_params(args)
        assert params["attributesToRetrieve"] == ["title", "url"]

    def test_no_distinct(self) -> None:
        args = _parse_query(["test", "--no-distinct"])
        params = build_search_params(args)
        assert "distinct" not in params

    def test_custom_distinct(self) -> None:
        args = _parse_query(["test", "--distinct", "source_name"])
        params = build_search_params(args)
        assert params["distinct"] == "source_name"

    def test_hybrid_flag_without_value(self) -> None:
        args = _parse_query(["test", "--hybrid"])
        params = build_search_params(args)
        assert params["hybrid"]["semanticRatio"] == pytest.approx(DEFAULT_SEMANTIC_RATIO)

    def test_custom_hybrid_ratio(self) -> None:
        args = _parse_query(["test", "--hybrid", "0.3"])
        params = build_search_params(args)
        assert params["hybrid"]["semanticRatio"] == pytest.approx(0.3)

    def test_no_hybrid_by_default(self) -> None:
        args = _parse_query(["test"])
        params = build_search_params(args)
        assert "hybrid" not in params

    def test_hybrid_expands_query(self) -> None:
        args = _parse_query(["SSZ Merkleization", "--hybrid"])
        params = build_search_params(args)
        assert "ssz serialization format" in params["q"].lower()
        assert params["q"].startswith("SSZ Merkleization")

    def test_no_expansion_without_hybrid(self) -> None:
        args = _parse_query(["SSZ Merkleization"])
        params = build_search_params(args)
        assert params["q"] == "SSZ Merkleization"

    def test_no_expand_flag_disables_expansion(self) -> None:
        args = _parse_query(["SSZ Merkleization", "--hybrid", "--no-expand"])
        params = build_search_params(args)
        assert params["q"] == "SSZ Merkleization"

    def test_hybrid_07_adds_query_prefix(self) -> None:
        """At ratio 0.7 (pure semantic), query gets embeddinggemma prefix."""
        args = _parse_query(["test query", "--hybrid", "0.7"])
        params = build_search_params(args)
        assert params["q"].startswith("task: search result | query: ")
        assert "test query" in params["q"]

    def test_hybrid_05_no_query_prefix(self) -> None:
        """At ratio 0.5 (keyword-dominant), no prefix applied."""
        args = _parse_query(["test query", "--hybrid", "0.5"])
        params = build_search_params(args)
        assert not params["q"].startswith("task: search result")

    def test_hybrid_default_05_no_prefix(self) -> None:
        """Default --hybrid (0.5) is below threshold — no prefix."""
        args = _parse_query(["test query", "--hybrid"])
        params = build_search_params(args)
        assert not params["q"].startswith("task: search result")

    def test_no_prefix_without_hybrid(self) -> None:
        """Keyword mode never gets a prefix."""
        args = _parse_query(["test query"])
        params = build_search_params(args)
        assert params["q"] == "test query"

    def test_hybrid_adds_text_length_filter(self) -> None:
        args = _parse_query(["test", "--hybrid"])
        params = build_search_params(args)
        assert f"text_length >= {DEFAULT_MIN_TEXT_LENGTH}" in params["filter"]

    def test_no_text_length_filter_without_hybrid(self) -> None:
        args = _parse_query(["test"])
        params = build_search_params(args)
        assert "text_length" not in params.get("filter", "")

    def test_custom_min_text_length(self) -> None:
        args = _parse_query(["test", "--hybrid", "--min-text-length", "100"])
        params = build_search_params(args)
        assert "text_length >= 100" in params["filter"]

    def test_min_text_length_zero_disables_filter(self) -> None:
        args = _parse_query(["test", "--hybrid", "--min-text-length", "0"])
        params = build_search_params(args)
        assert "text_length" not in params.get("filter", "")


# ===================================================================
# format_hit
# ===================================================================


class TestFormatHit:
    """format_hit renders a single search hit for the terminal."""

    def test_basic_hit(self) -> None:
        hit = {
            "title": "EIP-4844: Shard Blob Transactions",
            "source_kind": "eip",
            "source_name": "eips",
            "url": "https://eips.ethereum.org/EIPS/eip-4844",
            "text": "Introduces a new transaction format.",
        }
        out = format_hit(1, hit)
        assert "[1] EIP-4844: Shard Blob Transactions" in out
        assert "eip | eips" in out
        assert "https://eips.ethereum.org/EIPS/eip-4844" in out
        assert "Introduces a new transaction format." in out

    def test_hit_with_author(self) -> None:
        hit = {
            "title": "Post Title",
            "source_kind": "forum",
            "source_name": "ethresear.ch",
            "author": "vbuterin",
            "url": "https://ethresear.ch/t/1234",
            "text": "Some content.",
        }
        out = format_hit(1, hit)
        assert "forum | ethresear.ch | vbuterin" in out

    def test_hit_with_path_and_line(self) -> None:
        hit = {
            "title": "my_function",
            "source_kind": "code",
            "path": "src/main.py",
            "start_line": 42,
            "text": "def my_function():",
        }
        out = format_hit(1, hit)
        assert "src/main.py:42" in out

    def test_hit_with_path_no_line(self) -> None:
        hit = {"title": "test", "path": "src/main.py", "text": "content"}
        out = format_hit(1, hit)
        assert "src/main.py" in out
        assert ":" not in out.split("src/main.py")[1].split("\n")[0]

    def test_untitled_hit(self) -> None:
        hit = {"text": "Some text without a title."}
        out = format_hit(1, hit)
        assert "[1] (untitled)" in out

    def test_symbol_name_fallback(self) -> None:
        hit = {"symbol_name": "process_block", "text": "..."}
        out = format_hit(1, hit)
        assert "[1] process_block" in out

    def test_long_text_truncated(self) -> None:
        hit = {"title": "T", "text": "x" * 500}
        out = format_hit(1, hit)
        assert "..." in out

    def test_short_text_not_truncated(self) -> None:
        hit = {"title": "T", "text": "short"}
        out = format_hit(1, hit)
        assert "..." not in out

    def test_newlines_in_text_replaced(self) -> None:
        hit = {"title": "T", "text": "line1\nline2\nline3"}
        out = format_hit(1, hit)
        # Text preview should be single-line (newlines replaced with spaces)
        text_line = next(line for line in out.split("\n") if "line1" in line)
        assert "\n" not in text_line.replace("\n", "")

    def test_no_metadata_line_when_empty(self) -> None:
        hit = {"title": "T", "url": "https://x.com", "text": "t"}
        out = format_hit(1, hit)
        lines = out.strip().split("\n")
        # line 0: title, line 1: url, line 2: text — no metadata line
        assert lines[1].strip().startswith("https://")


# ===================================================================
# CLI argument parsing
# ===================================================================


class TestCLIParsing:
    """CLI argument parsing and defaults."""

    def test_query_defaults(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "hello"])
        assert args.command == "query"
        assert args.query_text == "hello"
        assert args.limit == DEFAULT_LIMIT
        assert args.hybrid is None  # keyword by default
        assert args.distinct == DEFAULT_DISTINCT

    def test_stats_command(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["stats"])
        assert args.command == "stats"

    def test_json_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--json", "query", "test"])
        assert args.json is True

    def test_verbose_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["-v", "query", "test"])
        assert args.verbose is True

    def test_url_override(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--url", "http://remote:7700", "query", "test"])
        assert args.url == "http://remote:7700"

    def test_key_override(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--key", "mykey", "query", "test"])
        assert args.key == "mykey"

    def test_all_query_filters(self) -> None:
        parser = build_parser()
        args = parser.parse_args([
            "query", "test",
            "--source-kind", "forum",
            "--source-name", "ethresear.ch",
            "--author", "vbuterin",
            "--eip", "4844",
            "--eip-status", "Final",
            "--repo", "go-ethereum",
            "--filter", "custom > 0",
            "--sort", "source_date_ts:desc",
            "--fields", "title,url",
            "--distinct", "source_name",
            "--limit", "5",
            "--hybrid", "0.3",
        ])
        assert args.source_kind == "forum"
        assert args.source_name == "ethresear.ch"
        assert args.author == "vbuterin"
        assert args.eip == 4844
        assert args.eip_status == "Final"
        assert args.repo == "go-ethereum"
        assert args.filter == "custom > 0"
        assert args.sort == "source_date_ts:desc"
        assert args.fields == "title,url"
        assert args.distinct == "source_name"
        assert args.limit == 5
        assert args.hybrid == pytest.approx(0.3)

    def test_no_distinct_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "test", "--no-distinct"])
        assert args.no_distinct is True

    def test_include_code_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "test", "--include-code"])
        assert args.include_code is True

    def test_include_code_default_false(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "test"])
        assert args.include_code is False

    def test_source_kind_accepts_generic(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "test", "--source-kind", "generic"])
        assert args.source_kind == "generic"

    def test_no_expand_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "test", "--no-expand"])
        assert args.no_expand is True

    def test_no_expand_default_false(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["query", "test"])
        assert args.no_expand is False

    def test_apply_terminology_command(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["apply-terminology"])
        assert args.command == "apply-terminology"


# ===================================================================
# main / HTTP integration (mocked)
# ===================================================================


class TestMainIntegration:
    """Integration tests with mocked HTTP."""

    @patch("erd_index.search_cli._meili_request")
    def test_query_sends_correct_payload(self, mock_req: MagicMock) -> None:
        mock_req.return_value = {"hits": [], "estimatedTotalHits": 0, "processingTimeMs": 1}
        from erd_index.search_cli import main

        main(["--key", "testkey", "query", "EIP-4844", "--limit", "3"])

        mock_req.assert_called_once()
        call_args = mock_req.call_args
        url = call_args[0][0]
        key = call_args[0][1]
        payload = call_args[1]["payload"]

        assert "eth_chunks_v1/search" in url
        assert key == "testkey"
        assert payload["q"] == "EIP-4844"
        assert payload["limit"] == 3

    @patch("erd_index.search_cli._meili_request")
    def test_query_json_output(self, mock_req: MagicMock, capsys) -> None:
        mock_req.return_value = {
            "hits": [{"title": "EIP-4844", "text": "Proto-danksharding"}],
            "estimatedTotalHits": 1,
            "processingTimeMs": 5,
        }
        from erd_index.search_cli import main

        main(["--key", "k", "--json", "query", "test"])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["hits"][0]["title"] == "EIP-4844"

    @patch("erd_index.search_cli._meili_request")
    def test_query_formatted_output(self, mock_req: MagicMock, capsys) -> None:
        mock_req.return_value = {
            "hits": [
                {
                    "title": "Proto-danksharding",
                    "source_kind": "eip",
                    "source_name": "eips",
                    "url": "https://eips.ethereum.org/EIPS/eip-4844",
                    "text": "Shard blob transactions.",
                },
            ],
            "estimatedTotalHits": 42,
            "processingTimeMs": 12,
        }
        from erd_index.search_cli import main

        main(["--key", "k", "query", "test"])
        captured = capsys.readouterr()
        assert "[1] Proto-danksharding" in captured.out
        assert "42 results (12ms)" in captured.out

    @patch("erd_index.search_cli._meili_request")
    def test_stats_command(self, mock_req: MagicMock, capsys) -> None:
        mock_req.return_value = {
            "numberOfDocuments": 1234,
            "fieldDistribution": {"title": 1234, "text": 1234},
        }
        from erd_index.search_cli import main

        main(["--key", "k", "stats"])
        captured = capsys.readouterr()
        assert "1234" in captured.out
        assert "title" in captured.out

    @patch("erd_index.search_cli._meili_request")
    def test_query_payload_excludes_code_by_default(self, mock_req: MagicMock) -> None:
        mock_req.return_value = {"hits": [], "estimatedTotalHits": 0, "processingTimeMs": 1}
        from erd_index.search_cli import main

        main(["--key", "k", "query", "test"])

        payload = mock_req.call_args[1]["payload"]
        assert "source_kind != 'code'" in payload["filter"]

    @patch("erd_index.search_cli._meili_request")
    def test_query_payload_includes_code_when_flagged(self, mock_req: MagicMock) -> None:
        mock_req.return_value = {"hits": [], "estimatedTotalHits": 0, "processingTimeMs": 1}
        from erd_index.search_cli import main

        main(["--key", "k", "query", "test", "--include-code"])

        payload = mock_req.call_args[1]["payload"]
        assert "filter" not in payload

    @patch("erd_index.search_cli._cmd_apply_terminology")
    def test_apply_terminology_uses_admin_key(self, mock_cmd: MagicMock) -> None:
        from erd_index.search_cli import main

        main(["--key", "admin-key", "apply-terminology"])

        mock_cmd.assert_called_once()
        args = mock_cmd.call_args[0][0]
        assert args.key == "admin-key"
        assert args.command == "apply-terminology"

    def test_no_command_exits(self) -> None:
        from erd_index.search_cli import main

        with pytest.raises(SystemExit) as exc_info:
            main([])
        assert exc_info.value.code == 1
