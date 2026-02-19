"""Tests for scripts/benchmark_search.py — search quality benchmark.

All HTTP interactions are mocked so tests run without a live Meilisearch server.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from scripts.benchmark_search import (
    build_parser,
    compute_metrics,
    maybe_expand_query,
    print_report,
    run_benchmark,
    score_hit,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_QUERY_DEF = {
    "id": "test-query",
    "query": "KZG commitment",
    "category": "jargon",
    "expand_for_hybrid": True,
    "relevance_patterns": [
        r"(?i)\bKZG\b",
        r"(?i)polynomial.*commit",
    ],
    "strong_patterns": [
        r"(?i)\bKZG\b.*commit",
    ],
    "anti_patterns": [
        r"(?i)TestPush",
        r"(?i)Mining attacks on PoRA",
    ],
    "expected_source_kinds": ["forum", "eip"],
}


def _make_hit(title: str, text: str, source_kind: str = "forum") -> dict:
    return {
        "title": title,
        "text": text,
        "source_kind": source_kind,
        "source_name": "ethresear.ch",
        "author": "test",
        "url": "https://example.com",
        "dedupe_key": f"dk-{title[:10]}",
    }


# ===================================================================
# score_hit
# ===================================================================


class TestScoreHit:
    """score_hit classifies a single hit against query patterns."""

    def test_relevant_hit(self) -> None:
        hit = _make_hit("KZG polynomial commitment scheme", "Detailed proof verification.")
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["relevant"] is True

    def test_strong_hit(self) -> None:
        hit = _make_hit("KZG commitment verification", "Opening proof protocol.")
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["strong"] is True
        assert result["relevant"] is True

    def test_irrelevant_hit(self) -> None:
        hit = _make_hit("Merkle Patricia Trie", "State storage implementation details.")
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["relevant"] is False
        assert result["strong"] is False

    def test_anti_pattern_detected(self) -> None:
        hit = _make_hit("Mining attacks on PoRA", "A completely unrelated topic.")
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["anti"] is True

    def test_relevant_but_not_strong(self) -> None:
        hit = _make_hit("Some polynomial commitment background", "General introduction.")
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["relevant"] is True
        assert result["strong"] is False

    def test_no_anti_on_clean_hit(self) -> None:
        hit = _make_hit("KZG commitment proof", "Valid content about KZG.")
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["anti"] is False

    def test_preserves_metadata(self) -> None:
        hit = _make_hit("KZG proof", "KZG text")
        hit["source_kind"] = "eip"
        hit["dedupe_key"] = "dk-123"
        result = score_hit(hit, SAMPLE_QUERY_DEF)
        assert result["source_kind"] == "eip"
        assert result["dedupe_key"] == "dk-123"


# ===================================================================
# compute_metrics
# ===================================================================


class TestComputeMetrics:
    """compute_metrics calculates precision/strong/contamination from scored hits."""

    def test_perfect_results(self) -> None:
        scored = [
            {"relevant": True, "strong": True, "anti": False, "source_kind": "forum"},
            {"relevant": True, "strong": True, "anti": False, "source_kind": "forum"},
            {"relevant": True, "strong": True, "anti": False, "source_kind": "eip"},
            {"relevant": True, "strong": True, "anti": False, "source_kind": "forum"},
            {"relevant": True, "strong": True, "anti": False, "source_kind": "forum"},
        ]
        m = compute_metrics(scored, SAMPLE_QUERY_DEF)
        assert m["precision_at_5"] == 1.0
        assert m["strong_at_5"] == 1.0
        assert m["contamination_at_5"] == 0.0
        assert m["source_kind_ok"] is True

    def test_partial_results(self) -> None:
        scored = [
            {"relevant": True, "strong": True, "anti": False, "source_kind": "forum"},
            {"relevant": True, "strong": False, "anti": False, "source_kind": "forum"},
            {"relevant": False, "strong": False, "anti": False, "source_kind": "forum"},
            {"relevant": True, "strong": False, "anti": False, "source_kind": "forum"},
            {"relevant": False, "strong": False, "anti": False, "source_kind": "forum"},
        ]
        m = compute_metrics(scored, SAMPLE_QUERY_DEF)
        assert m["precision_at_5"] == pytest.approx(0.6)
        assert m["strong_at_5"] == pytest.approx(0.2)
        assert m["contamination_at_5"] == 0.0

    def test_contamination(self) -> None:
        scored = [
            {"relevant": True, "strong": False, "anti": False, "source_kind": "forum"},
            {"relevant": False, "strong": False, "anti": True, "source_kind": "forum"},
            {"relevant": False, "strong": False, "anti": True, "source_kind": "forum"},
            {"relevant": True, "strong": False, "anti": False, "source_kind": "forum"},
            {"relevant": False, "strong": False, "anti": False, "source_kind": "forum"},
        ]
        m = compute_metrics(scored, SAMPLE_QUERY_DEF)
        assert m["contamination_at_5"] == pytest.approx(0.4)

    def test_empty_results(self) -> None:
        m = compute_metrics([], SAMPLE_QUERY_DEF)
        assert m["precision_at_5"] == 0.0
        assert m["strong_at_5"] == 0.0
        assert m["contamination_at_5"] == 0.0

    def test_source_kind_ok_when_matching(self) -> None:
        scored = [
            {"relevant": True, "strong": False, "anti": False, "source_kind": "eip"},
        ]
        m = compute_metrics(scored, SAMPLE_QUERY_DEF)
        assert m["source_kind_ok"] is True

    def test_source_kind_fail_when_no_match(self) -> None:
        scored = [
            {"relevant": True, "strong": False, "anti": False, "source_kind": "code"},
            {"relevant": True, "strong": False, "anti": False, "source_kind": "generic"},
        ]
        m = compute_metrics(scored, SAMPLE_QUERY_DEF)
        assert m["source_kind_ok"] is False

    def test_source_kind_ok_with_no_expected(self) -> None:
        qdef = {**SAMPLE_QUERY_DEF, "expected_source_kinds": []}
        scored = [
            {"relevant": True, "strong": False, "anti": False, "source_kind": "code"},
        ]
        m = compute_metrics(scored, qdef)
        assert m["source_kind_ok"] is True


# ===================================================================
# maybe_expand_query
# ===================================================================


class TestMaybeExpandQuery:
    """maybe_expand_query conditionally expands queries for hybrid/semantic modes."""

    def test_keyword_never_expands(self) -> None:
        result = maybe_expand_query("SSZ", "keyword", should_expand=True)
        assert result == "SSZ"

    def test_no_expand_flag(self) -> None:
        result = maybe_expand_query("SSZ", "hybrid_0.5", should_expand=False)
        assert result == "SSZ"

    def test_hybrid_with_expand(self) -> None:
        # This tests that expand_query is called (if available)
        result = maybe_expand_query("SSZ", "hybrid_0.5", should_expand=True)
        # If erd_index is installed, result should be expanded; otherwise original
        assert isinstance(result, str)
        assert len(result) >= 3  # at minimum the original query


# ===================================================================
# CLI argument parsing
# ===================================================================


class TestCLIParsing:
    """CLI argument parsing and defaults."""

    def test_defaults(self) -> None:
        parser = build_parser()
        args = parser.parse_args([])
        assert args.mode is None
        assert args.query_id is None
        assert args.category is None
        assert args.json is False
        assert args.output is None
        assert args.baseline is None
        assert args.verbose is False

    def test_mode_filter(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--mode", "keyword"])
        assert args.mode == "keyword"

    def test_query_filter(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--query", "ssz-merkleization"])
        assert args.query_id == "ssz-merkleization"

    def test_category_filter(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--category", "jargon"])
        assert args.category == "jargon"

    def test_json_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--json"])
        assert args.json is True

    def test_output_file(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output", "report.json"])
        assert args.output == "report.json"

    def test_baseline_file(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--baseline", "prev.json"])
        assert args.baseline == "prev.json"

    def test_verbose_flag(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["-v"])
        assert args.verbose is True

    def test_key_override(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--key", "mykey"])
        assert args.key == "mykey"

    def test_invalid_mode_rejected(self) -> None:
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--mode", "invalid_mode"])


# ===================================================================
# JSON report structure
# ===================================================================


class TestReportStructure:
    """The JSON report has the expected structure."""

    @patch("scripts.benchmark_search.meili_search")
    def test_report_has_required_keys(self, mock_search: MagicMock) -> None:
        mock_search.return_value = {
            "hits": [
                _make_hit("KZG commitment proof", "KZG polynomial commitment opening."),
                _make_hit("KZG trusted setup", "The KZG commitment scheme requires a setup."),
            ],
        }
        queries = [SAMPLE_QUERY_DEF]
        report = run_benchmark(
            api_key="test-key",
            modes=["keyword"],
            queries=queries,
            verbose=False,
        )
        assert "timestamp" in report
        assert "total_queries" in report
        assert "total_searches" in report
        assert "elapsed_seconds" in report
        assert "aggregate" in report
        assert "by_category" in report
        assert "per_query" in report

    @patch("scripts.benchmark_search.meili_search")
    def test_per_query_structure(self, mock_search: MagicMock) -> None:
        mock_search.return_value = {
            "hits": [_make_hit("KZG proof", "KZG commitment verification.")],
        }
        report = run_benchmark(
            api_key="test-key",
            modes=["keyword"],
            queries=[SAMPLE_QUERY_DEF],
        )
        qr = report["per_query"][0]
        assert qr["id"] == "test-query"
        assert qr["query"] == "KZG commitment"
        assert qr["category"] == "jargon"
        assert "keyword" in qr["results"]
        kr = qr["results"]["keyword"]
        assert "precision_at_5" in kr
        assert "strong_at_5" in kr
        assert "contamination_at_5" in kr
        assert "source_kind_ok" in kr
        assert "hits" in kr

    @patch("scripts.benchmark_search.meili_search")
    def test_aggregate_structure(self, mock_search: MagicMock) -> None:
        mock_search.return_value = {
            "hits": [_make_hit("KZG proof", "KZG commitment verification.")],
        }
        report = run_benchmark(
            api_key="test-key",
            modes=["keyword", "hybrid_0.5"],
            queries=[SAMPLE_QUERY_DEF],
        )
        agg = report["aggregate"]
        for mode in ["keyword", "hybrid_0.5"]:
            assert mode in agg
            assert "precision_at_5" in agg[mode]
            assert "strong_at_5" in agg[mode]
            assert "contamination" in agg[mode]
            assert "source_ok" in agg[mode]

    @patch("scripts.benchmark_search.meili_search")
    def test_by_category_structure(self, mock_search: MagicMock) -> None:
        mock_search.return_value = {
            "hits": [_make_hit("KZG proof", "KZG commitment verification.")],
        }
        report = run_benchmark(
            api_key="test-key",
            modes=["keyword"],
            queries=[SAMPLE_QUERY_DEF],
        )
        by_cat = report["by_category"]
        assert "jargon" in by_cat
        assert by_cat["jargon"]["n"] == 1
        assert "keyword" in by_cat["jargon"]

    @patch("scripts.benchmark_search.meili_search")
    def test_total_searches_counted(self, mock_search: MagicMock) -> None:
        mock_search.return_value = {"hits": []}
        report = run_benchmark(
            api_key="test-key",
            modes=["keyword", "hybrid_0.5"],
            queries=[SAMPLE_QUERY_DEF],
        )
        assert report["total_searches"] == 2  # 2 modes x 1 query

    @patch("scripts.benchmark_search.meili_search")
    def test_respects_modes_to_test(self, mock_search: MagicMock) -> None:
        mock_search.return_value = {"hits": []}
        qdef = {**SAMPLE_QUERY_DEF, "modes_to_test": ["keyword"]}
        report = run_benchmark(
            api_key="test-key",
            modes=["keyword", "hybrid_0.5", "semantic_1.0"],
            queries=[qdef],
        )
        # Only keyword should be in results (hybrid_0.5 and semantic_1.0 skipped)
        assert report["total_searches"] == 1
        assert "keyword" in report["per_query"][0]["results"]
        assert "hybrid_0.5" not in report["per_query"][0]["results"]


# ===================================================================
# print_report (smoke test)
# ===================================================================


class TestPrintReport:
    """print_report renders without errors."""

    def test_smoke(self, capsys) -> None:
        report = {
            "timestamp": "2026-02-18T18:30:00",
            "total_queries": 1,
            "total_searches": 2,
            "elapsed_seconds": 1.5,
            "aggregate": {
                "keyword": {
                    "precision_at_5": 0.8,
                    "strong_at_5": 0.6,
                    "contamination": 0.0,
                    "source_ok": "1/1",
                },
            },
            "by_category": {
                "jargon": {"n": 1, "keyword": 0.8},
            },
            "per_query": [
                {
                    "id": "test",
                    "query": "test query",
                    "category": "jargon",
                    "results": {
                        "keyword": {
                            "precision_at_5": 0.8,
                            "strong_at_5": 0.6,
                            "contamination_at_5": 0.0,
                            "source_kind_ok": True,
                            "hits": [
                                {
                                    "title": "Test Hit",
                                    "source_kind": "forum",
                                    "relevant": True,
                                    "strong": True,
                                    "anti": False,
                                },
                            ],
                        },
                    },
                },
            ],
        }
        print_report(report, verbose=False)
        captured = capsys.readouterr()
        assert "eth-search benchmark" in captured.out
        assert "keyword" in captured.out
        assert "Precision@5" in captured.out

    def test_verbose_output(self, capsys) -> None:
        report = {
            "timestamp": "2026-02-18T18:30:00",
            "total_queries": 1,
            "total_searches": 1,
            "elapsed_seconds": 0.5,
            "aggregate": {
                "keyword": {
                    "precision_at_5": 1.0,
                    "strong_at_5": 1.0,
                    "contamination": 0.0,
                    "source_ok": "1/1",
                },
            },
            "by_category": {"jargon": {"n": 1, "keyword": 1.0}},
            "per_query": [
                {
                    "id": "test",
                    "query": "test",
                    "category": "jargon",
                    "results": {
                        "keyword": {
                            "precision_at_5": 1.0,
                            "strong_at_5": 1.0,
                            "contamination_at_5": 0.0,
                            "source_kind_ok": True,
                            "hits": [
                                {
                                    "title": "Hit Title",
                                    "source_kind": "forum",
                                    "relevant": True,
                                    "strong": True,
                                    "anti": False,
                                },
                            ],
                        },
                    },
                },
            ],
        }
        print_report(report, verbose=True)
        captured = capsys.readouterr()
        assert "Per-result details" in captured.out
        assert "Hit Title" in captured.out

    def test_baseline_delta(self, capsys) -> None:
        report = {
            "timestamp": "2026-02-18T19:00:00",
            "total_queries": 1,
            "total_searches": 1,
            "elapsed_seconds": 1.0,
            "aggregate": {
                "keyword": {
                    "precision_at_5": 0.9,
                    "strong_at_5": 0.7,
                    "contamination": 0.0,
                    "source_ok": "1/1",
                },
            },
            "by_category": {"jargon": {"n": 1, "keyword": 0.9}},
            "per_query": [],
        }
        baseline = {
            "aggregate": {
                "keyword": {
                    "precision_at_5": 0.8,
                    "strong_at_5": 0.6,
                    "contamination": 0.0,
                    "source_ok": "1/1",
                },
            },
        }
        print_report(report, baseline=baseline)
        captured = capsys.readouterr()
        assert "+0.100" in captured.out
