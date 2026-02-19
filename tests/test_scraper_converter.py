"""Tests for scraper retry/backoff logic, incremental index updates, and converter skip behaviour.

Mocks HTTP responses via unittest.mock to avoid real network calls.
"""

from __future__ import annotations

import json
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from converter.discourse_to_md import (
    DiscourseConverter,
    _extract_topic_id_slug,
)
from scraper.discourse import DiscourseScraper

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_http_error(
    code: int,
    *,
    headers: dict[str, str] | None = None,
) -> urllib.error.HTTPError:
    """Build an HTTPError with optional headers (e.g. Retry-After)."""
    msg = MagicMock()
    # HTTPError stores headers in exc.headers
    err = urllib.error.HTTPError(
        url="https://example.com",
        code=code,
        msg=f"HTTP {code}",
        hdrs=msg,
        fp=BytesIO(b""),
    )
    # Patch .headers to return a dict-like object supporting .get()
    hdr_dict = headers or {}
    err.headers = MagicMock()
    err.headers.get = lambda key, default=None: hdr_dict.get(key, default)
    return err


def _make_url_error() -> urllib.error.URLError:
    """Build a URLError (network-level failure, e.g. DNS resolution)."""
    return urllib.error.URLError("Name resolution failed")


def _urlopen_json(data: dict) -> MagicMock:
    """Return a context-manager mock whose .read() returns JSON bytes."""
    body = json.dumps(data).encode()
    resp = MagicMock()
    resp.read.return_value = body
    resp.__enter__ = lambda self: self
    resp.__exit__ = MagicMock(return_value=False)
    return resp


def _minimal_topic_json(topic_id: int, slug: str = "test-topic") -> dict:
    """Return a minimal Discourse topic JSON with one post."""
    return {
        "id": topic_id,
        "title": f"Topic {topic_id}",
        "slug": slug,
        "created_at": "2024-01-15T10:00:00.000Z",
        "category_id": 1,
        "tags": [],
        "views": 42,
        "like_count": 5,
        "posts_count": 1,
        "post_stream": {
            "stream": [100],
            "posts": [
                {
                    "id": 100,
                    "username": "alice",
                    "created_at": "2024-01-15T10:00:00.000Z",
                    "cooked": "<p>Hello world</p>",
                }
            ],
        },
    }


# ---------------------------------------------------------------------------
# TestRetryAfter — _fetch_json retry/backoff logic
# ---------------------------------------------------------------------------


class TestRetryAfter:
    """Verify that _fetch_json honours Retry-After and exponential backoff."""

    def _make_scraper(self, tmp_path: Path) -> DiscourseScraper:
        return DiscourseScraper(
            base_url="https://example.com",
            raw_dir=tmp_path / "raw",
            delay=1.0,
            max_retries=3,
        )

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_429_with_retry_after_header(self, mock_urlopen, mock_sleep, tmp_path):
        """429 with Retry-After header: sleep for the header value, then succeed."""
        err_429 = _make_http_error(429, headers={"Retry-After": "7"})
        success = _urlopen_json({"ok": True})
        mock_urlopen.side_effect = [err_429, success]

        scraper = self._make_scraper(tmp_path)
        result = scraper._fetch_json("/test")

        assert result == {"ok": True}
        # Should sleep for the Retry-After value (7), not exponential backoff
        mock_sleep.assert_any_call(7)

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_429_without_header_uses_exponential_backoff(
        self, mock_urlopen, mock_sleep, tmp_path
    ):
        """429 without Retry-After: fall back to delay * 2^attempt."""
        err_429 = _make_http_error(429, headers={})
        success = _urlopen_json({"ok": True})
        mock_urlopen.side_effect = [err_429, success]

        scraper = self._make_scraper(tmp_path)
        result = scraper._fetch_json("/test")

        assert result == {"ok": True}
        # attempt=0 → delay * 2^0 = 1.0
        mock_sleep.assert_any_call(1.0)

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_last_attempt_no_sleep_on_5xx(self, mock_urlopen, mock_sleep, tmp_path):
        """On the last retry attempt, 5xx does NOT sleep (no point waiting)."""
        err_500 = _make_http_error(500)
        # All 3 attempts fail with 500
        mock_urlopen.side_effect = [err_500, err_500, err_500]

        scraper = self._make_scraper(tmp_path)
        result = scraper._fetch_json("/test")

        assert result is None
        # With max_retries=3, attempts are 0, 1, 2.
        # attempt 0 (< 2): sleep(1.0)
        # attempt 1 (< 2): sleep(2.0)
        # attempt 2 (== max_retries-1): NO sleep
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1.0)
        mock_sleep.assert_any_call(2.0)

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_last_attempt_no_sleep_on_network_error(
        self, mock_urlopen, mock_sleep, tmp_path
    ):
        """On the last retry attempt, network errors do NOT sleep."""
        net_err = _make_url_error()
        mock_urlopen.side_effect = [net_err, net_err, net_err]

        scraper = self._make_scraper(tmp_path)
        result = scraper._fetch_json("/test")

        assert result is None
        # Same logic: 2 sleeps for attempts 0 and 1, none for attempt 2
        assert mock_sleep.call_count == 2


# ---------------------------------------------------------------------------
# TestIncrementalIndex — build_index / _update_index_from_latest
# ---------------------------------------------------------------------------


class TestIncrementalIndex:
    """Verify incremental index updates and error handling."""

    def _make_scraper(self, tmp_path: Path) -> DiscourseScraper:
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "topics").mkdir(exist_ok=True)
        return DiscourseScraper(
            base_url="https://example.com",
            raw_dir=raw_dir,
            delay=0.0,
            max_retries=2,
        )

    def _write_index(self, scraper: DiscourseScraper, index: dict) -> None:
        dest = scraper.raw_dir / "index.json"
        dest.write_text(json.dumps(index))

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_new_topics_merged_into_existing_index(
        self, mock_urlopen, mock_sleep, tmp_path
    ):
        """When /latest returns new topic IDs, they are merged into the index."""
        scraper = self._make_scraper(tmp_path)

        # Pre-existing index with topic 1
        existing_index = {
            "1": {
                "id": 1,
                "title": "Old topic",
                "category_id": 1,
                "category_name": "General",
                "posts_count": 3,
                "created_at": "2024-01-01",
                "last_posted_at": "2024-01-01",
                "views": 10,
                "like_count": 2,
            }
        }
        self._write_index(scraper, existing_index)

        # /latest.json?page=0 returns topic 1 (known) and topic 2 (new)
        latest_page = {
            "topic_list": {
                "topics": [
                    {
                        "id": 2,
                        "title": "New topic",
                        "category_id": 1,
                        "posts_count": 1,
                        "created_at": "2024-06-01",
                        "last_posted_at": "2024-06-01",
                        "views": 5,
                        "like_count": 1,
                    },
                    {
                        "id": 1,
                        "title": "Old topic",
                        "category_id": 1,
                        "posts_count": 3,
                        "created_at": "2024-01-01",
                        "last_posted_at": "2024-01-01",
                        "views": 10,
                        "like_count": 2,
                    },
                ],
                # No more_topics_url → single page
            }
        }
        mock_urlopen.return_value = _urlopen_json(latest_page)

        result = scraper.build_index(categories=[])

        assert "1" in result
        assert "2" in result
        assert result["2"]["title"] == "New topic"
        assert len(result) == 2

        # Verify index.json was written with merged data
        saved = json.loads((scraper.raw_dir / "index.json").read_text())
        assert "2" in saved

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_sweep_stops_when_all_known(self, mock_urlopen, mock_sleep, tmp_path):
        """When /latest has only already-known topic IDs, the sweep stops."""
        scraper = self._make_scraper(tmp_path)

        existing_index = {
            "1": {
                "id": 1,
                "title": "Known topic",
                "category_id": 1,
                "category_name": "General",
                "posts_count": 3,
                "created_at": "2024-01-01",
                "last_posted_at": "2024-01-01",
                "views": 10,
                "like_count": 2,
            },
        }
        self._write_index(scraper, existing_index)

        # /latest returns only topic 1 which is already known
        latest_page = {
            "topic_list": {
                "topics": [
                    {
                        "id": 1,
                        "title": "Known topic",
                        "category_id": 1,
                        "posts_count": 3,
                        "created_at": "2024-01-01",
                        "last_posted_at": "2024-01-01",
                        "views": 10,
                        "like_count": 2,
                    },
                ],
                "more_topics_url": "/latest?page=1",  # has more, but sweep stops
            }
        }
        mock_urlopen.return_value = _urlopen_json(latest_page)

        result = scraper.build_index(categories=[])

        # Index unchanged — still only topic 1
        assert len(result) == 1
        assert "1" in result
        # Lookahead of 2: fetches page 0, then 2 more all-known pages before stopping
        assert mock_urlopen.call_count == 3

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_fetch_categories_raises_runtime_error_on_failure(
        self, mock_urlopen, mock_sleep, tmp_path
    ):
        """fetch_categories raises RuntimeError (not sys.exit) when API fails."""
        scraper = self._make_scraper(tmp_path)

        # _fetch_json returns None when all retries exhausted
        mock_urlopen.side_effect = _make_http_error(500)

        with pytest.raises(RuntimeError, match="Failed to fetch categories"):
            scraper.fetch_categories()


# ---------------------------------------------------------------------------
# TestConverterSkipBeforeConvert — _extract_topic_id_slug and convert_all
# ---------------------------------------------------------------------------


class TestConverterSkipBeforeConvert:
    """Verify converter incremental skip logic and _extract_topic_id_slug."""

    def _make_converter(
        self, raw_dir: Path, corpus_dir: Path
    ) -> DiscourseConverter:
        return DiscourseConverter(
            source_name="test",
            base_url="https://example.com",
            raw_dir=raw_dir,
            corpus_dir=corpus_dir,
        )

    def _write_topic(self, topics_dir: Path, topic_id: int, slug: str = "test-topic"):
        """Write a minimal topic JSON to topics_dir/{id}.json."""
        topics_dir.mkdir(parents=True, exist_ok=True)
        path = topics_dir / f"{topic_id}.json"
        path.write_text(json.dumps(_minimal_topic_json(topic_id, slug)))
        return path

    def _write_categories(self, raw_dir: Path):
        """Write a minimal categories.json."""
        raw_dir.mkdir(parents=True, exist_ok=True)
        cats = {
            "category_list": {
                "categories": [
                    {"id": 1, "name": "General", "slug": "general"}
                ]
            }
        }
        (raw_dir / "categories.json").write_text(json.dumps(cats))

    def test_extract_topic_id_slug(self, tmp_path):
        """_extract_topic_id_slug returns the correct id and slug from JSON."""
        topics_dir = tmp_path / "topics"
        path = self._write_topic(topics_dir, 42, "my-cool-topic")

        topic_id, slug = _extract_topic_id_slug(path)

        assert topic_id == 42
        assert slug == "my-cool-topic"

    def test_convert_all_skips_existing(self, tmp_path):
        """convert_all skips topics whose output file already exists (incremental)."""
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir(parents=True, exist_ok=True)
        topics_dir = raw_dir / "topics"

        self._write_categories(raw_dir)
        self._write_topic(topics_dir, 10, "existing-topic")
        self._write_topic(topics_dir, 20, "new-topic")

        # Pre-create output for topic 10 — it should be skipped
        corpus_dir.mkdir(parents=True, exist_ok=True)
        (corpus_dir / "10-existing-topic.md").write_text("already here")

        converter = self._make_converter(raw_dir, corpus_dir)
        converted, skipped = converter.convert_all()

        assert converted == 1  # only topic 20
        assert skipped == 1  # topic 10 was skipped
        # Verify topic 20 was actually written
        assert (corpus_dir / "20-new-topic.md").exists()
        # Verify topic 10 was NOT overwritten
        assert (corpus_dir / "10-existing-topic.md").read_text() == "already here"

    def test_convert_all_converts_new(self, tmp_path):
        """convert_all converts new topics that have no output file yet."""
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        topics_dir = raw_dir / "topics"

        self._write_categories(raw_dir)
        self._write_topic(topics_dir, 100, "fresh-topic")
        self._write_topic(topics_dir, 200, "another-fresh")

        converter = self._make_converter(raw_dir, corpus_dir)
        converted, skipped = converter.convert_all()

        assert converted == 2
        assert skipped == 0

        # Both output files should exist and contain frontmatter
        for fname in ("100-fresh-topic.md", "200-another-fresh.md"):
            out = corpus_dir / fname
            assert out.exists()
            content = out.read_text()
            assert content.startswith("---")
            assert "source: test" in content

    def test_convert_all_force_reconverts_everything(self, tmp_path):
        """convert_all(force=True) re-converts even when output exists."""
        raw_dir = tmp_path / "raw"
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir(parents=True, exist_ok=True)
        topics_dir = raw_dir / "topics"

        self._write_categories(raw_dir)
        self._write_topic(topics_dir, 50, "topic-fifty")

        # Pre-create a stale output file
        (corpus_dir / "50-topic-fifty.md").write_text("stale content")

        converter = self._make_converter(raw_dir, corpus_dir)
        converted, skipped = converter.convert_all(force=True)

        assert converted == 1
        assert skipped == 0

        # Content should be freshly generated, not the stale placeholder
        content = (corpus_dir / "50-topic-fifty.md").read_text()
        assert content != "stale content"
        assert content.startswith("---")
        assert "topic_id: 50" in content
        assert "Hello world" in content  # from the minimal fixture's cooked HTML
