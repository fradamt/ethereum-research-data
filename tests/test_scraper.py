"""Tests for scraper/discourse.py — topic meta, incremental index, fetch logic, retry behavior."""

from __future__ import annotations

import json
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

from scraper.discourse import DiscourseScraper, _save_json

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_http_error(
    code: int,
    *,
    headers: dict[str, str] | None = None,
) -> urllib.error.HTTPError:
    """Build an HTTPError with optional headers."""
    msg = MagicMock()
    err = urllib.error.HTTPError(
        url="https://example.com",
        code=code,
        msg=f"HTTP {code}",
        hdrs=msg,
        fp=BytesIO(b""),
    )
    hdr_dict = headers or {}
    err.headers = MagicMock()
    err.headers.get = lambda key, default=None: hdr_dict.get(key, default)
    return err


def _urlopen_json(data: dict) -> MagicMock:
    """Return a context-manager mock whose .read() returns JSON bytes."""
    body = json.dumps(data).encode()
    resp = MagicMock()
    resp.read.return_value = body
    resp.__enter__ = lambda self: self
    resp.__exit__ = MagicMock(return_value=False)
    return resp


def _make_scraper(tmp_path: Path, **kwargs) -> DiscourseScraper:
    defaults = dict(
        base_url="https://example.com",
        raw_dir=tmp_path / "raw",
        delay=0.0,
        max_retries=3,
    )
    defaults.update(kwargs)
    return DiscourseScraper(**defaults)


def _write_index(scraper: DiscourseScraper, index: dict) -> None:
    dest = scraper.raw_dir / "index.json"
    dest.write_text(json.dumps(index))


def _make_topic_meta(
    topic_id: int,
    *,
    posts_count: int = 1,
    last_posted_at: str = "2024-01-01",
    category_name: str = "General",
    title: str = "",
) -> dict:
    return {
        "id": topic_id,
        "title": title or f"Topic {topic_id}",
        "category_id": 1,
        "category_name": category_name,
        "posts_count": posts_count,
        "created_at": "2024-01-01",
        "last_posted_at": last_posted_at,
        "views": 10,
        "like_count": 2,
    }


# ---------------------------------------------------------------------------
# _topic_meta
# ---------------------------------------------------------------------------


class TestTopicMeta:
    def test_all_fields_extracted(self) -> None:
        raw = {
            "id": 42,
            "title": "Test Topic",
            "category_id": 5,
            "posts_count": 12,
            "created_at": "2024-03-15T10:00:00Z",
            "last_posted_at": "2024-06-20T14:30:00Z",
            "views": 500,
            "like_count": 25,
        }
        meta = DiscourseScraper._topic_meta(raw, "Research > Consensus")

        assert meta["id"] == 42
        assert meta["title"] == "Test Topic"
        assert meta["category_id"] == 5
        assert meta["category_name"] == "Research > Consensus"
        assert meta["posts_count"] == 12
        assert meta["created_at"] == "2024-03-15T10:00:00Z"
        assert meta["last_posted_at"] == "2024-06-20T14:30:00Z"
        assert meta["views"] == 500
        assert meta["like_count"] == 25

    def test_missing_optional_fields_default(self) -> None:
        raw = {"id": 99}
        meta = DiscourseScraper._topic_meta(raw, "")

        assert meta["id"] == 99
        assert meta["title"] == ""
        assert meta["category_id"] is None
        assert meta["posts_count"] == 0
        assert meta["created_at"] == ""
        assert meta["views"] == 0
        assert meta["like_count"] == 0


# ---------------------------------------------------------------------------
# _update_index_from_latest: metadata updates for known topics
# ---------------------------------------------------------------------------


class TestUpdateIndexMetadata:
    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_updates_posts_count_for_known_topic(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Known topics with changed posts_count get their metadata updated."""
        scraper = _make_scraper(tmp_path)

        index = {
            "1": _make_topic_meta(1, posts_count=3, last_posted_at="2024-01-01"),
        }

        latest_page = {
            "topic_list": {
                "topics": [{
                    "id": 1,
                    "title": "Known Topic",
                    "category_id": 1,
                    "posts_count": 8,  # increased from 3
                    "created_at": "2024-01-01",
                    "last_posted_at": "2024-06-01",  # changed
                    "views": 100,
                    "like_count": 5,
                }],
                # No more_topics_url — single page
            },
        }
        mock_urlopen.return_value = _urlopen_json(latest_page)

        result = scraper._update_index_from_latest(index)

        assert result["1"]["posts_count"] == 8
        assert result["1"]["last_posted_at"] == "2024-06-01"

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_unchanged_metadata_counts_as_all_known(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Pages where all topics are known AND unchanged increment consecutive_all_known."""
        scraper = _make_scraper(tmp_path)

        index = {
            "1": _make_topic_meta(1, posts_count=3, last_posted_at="2024-01-01"),
        }

        # Same topic with same posts_count and last_posted_at
        page = {
            "topic_list": {
                "topics": [{
                    "id": 1,
                    "title": "Known",
                    "category_id": 1,
                    "posts_count": 3,
                    "created_at": "2024-01-01",
                    "last_posted_at": "2024-01-01",
                    "views": 10,
                    "like_count": 2,
                }],
                "more_topics_url": "/latest?page=1",
            },
        }
        mock_urlopen.return_value = _urlopen_json(page)

        scraper._update_index_from_latest(index)

        # With max_lookahead=2, should fetch pages 0, 1, 2 then stop
        assert mock_urlopen.call_count == 3


# ---------------------------------------------------------------------------
# _update_index_from_latest: lookahead behavior
# ---------------------------------------------------------------------------


class TestUpdateIndexLookahead:
    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_continues_past_all_known_pages_within_lookahead(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """The sweep continues for max_lookahead pages past the first all-known page."""
        scraper = _make_scraper(tmp_path)

        # Known topic
        index = {
            "1": _make_topic_meta(1, posts_count=3, last_posted_at="2024-01-01"),
        }

        all_known_page = {
            "topic_list": {
                "topics": [{
                    "id": 1, "title": "Known", "category_id": 1,
                    "posts_count": 3, "created_at": "2024-01-01",
                    "last_posted_at": "2024-01-01", "views": 10, "like_count": 2,
                }],
                "more_topics_url": "/latest?page=X",
            },
        }

        # Page 0 = all known, page 1 = all known, page 2 = all known -> stop
        mock_urlopen.return_value = _urlopen_json(all_known_page)

        scraper._update_index_from_latest(index)

        # max_lookahead=2: page 0 (all_known=1), page 1 (=2), page 2 (=3 > 2 -> stop)
        assert mock_urlopen.call_count == 3

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_new_topic_resets_consecutive_counter(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Finding a new topic resets the consecutive all-known counter."""
        scraper = _make_scraper(tmp_path)

        index = {
            "1": _make_topic_meta(1, posts_count=3, last_posted_at="2024-01-01"),
        }

        # Page 0: all known
        page_0 = {
            "topic_list": {
                "topics": [{
                    "id": 1, "title": "Known", "category_id": 1,
                    "posts_count": 3, "created_at": "2024-01-01",
                    "last_posted_at": "2024-01-01", "views": 10, "like_count": 2,
                }],
                "more_topics_url": "/latest?page=1",
            },
        }
        # Page 1: has new topic (resets counter)
        page_1 = {
            "topic_list": {
                "topics": [{
                    "id": 2, "title": "New!", "category_id": 1,
                    "posts_count": 1, "created_at": "2024-06-01",
                    "last_posted_at": "2024-06-01", "views": 5, "like_count": 1,
                }],
                "more_topics_url": "/latest?page=2",
            },
        }
        # Pages 2-4: all known (only topic 1)
        page_known = {
            "topic_list": {
                "topics": [{
                    "id": 1, "title": "Known", "category_id": 1,
                    "posts_count": 3, "created_at": "2024-01-01",
                    "last_posted_at": "2024-01-01", "views": 10, "like_count": 2,
                }],
                "more_topics_url": "/latest?page=X",
            },
        }

        mock_urlopen.side_effect = [
            _urlopen_json(page_0),
            _urlopen_json(page_1),
            _urlopen_json(page_known),
            _urlopen_json(page_known),
            _urlopen_json(page_known),
        ]

        result = scraper._update_index_from_latest(index)

        assert "2" in result
        # page 0 (all_known=1), page 1 (new=reset to 0), page 2 (=1), page 3 (=2), page 4 (=3 > 2 -> stop)
        assert mock_urlopen.call_count == 5


# ---------------------------------------------------------------------------
# fetch_topics: re-fetch and skip logic
# ---------------------------------------------------------------------------


class TestFetchTopics:
    def test_refetch_when_posts_count_increases(self, tmp_path: Path) -> None:
        scraper = _make_scraper(tmp_path)

        existing_topic = {
            "id": 42,
            "post_stream": {"stream": [1, 2, 3], "posts": [{"id": 1}, {"id": 2}, {"id": 3}]},
        }
        (scraper.topics_dir / "42.json").write_text(json.dumps(existing_topic))

        index = {"42": {"id": 42, "posts_count": 8}}

        updated = {
            "id": 42,
            "post_stream": {
                "stream": list(range(1, 9)),
                "posts": [{"id": i} for i in range(1, 9)],
            },
        }

        with (
            patch.object(scraper, "_fetch_full_topic", return_value=updated) as mock_fetch,
            patch.object(scraper, "_throttle"),
        ):
            scraper.fetch_topics(index)

        mock_fetch.assert_called_once_with(42)

    def test_skip_when_posts_count_unchanged(self, tmp_path: Path) -> None:
        scraper = _make_scraper(tmp_path)

        existing_topic = {
            "id": 42,
            "post_stream": {"stream": [1, 2, 3], "posts": [{"id": 1}, {"id": 2}, {"id": 3}]},
        }
        (scraper.topics_dir / "42.json").write_text(json.dumps(existing_topic))

        index = {"42": {"id": 42, "posts_count": 3}}

        with (
            patch.object(scraper, "_fetch_full_topic") as mock_fetch,
            patch.object(scraper, "_throttle"),
        ):
            scraper.fetch_topics(index)

        mock_fetch.assert_not_called()

    def test_corrupt_json_triggers_refetch(self, tmp_path: Path) -> None:
        """If existing topic JSON is corrupt, it should be re-fetched."""
        scraper = _make_scraper(tmp_path)

        (scraper.topics_dir / "42.json").write_text("{not valid json")

        index = {"42": {"id": 42, "posts_count": 5}}

        fetched = {
            "id": 42,
            "post_stream": {
                "stream": [1, 2, 3, 4, 5],
                "posts": [{"id": i} for i in range(1, 6)],
            },
        }

        with (
            patch.object(scraper, "_fetch_full_topic", return_value=fetched) as mock_fetch,
            patch.object(scraper, "_throttle"),
        ):
            scraper.fetch_topics(index)

        mock_fetch.assert_called_once_with(42)


# ---------------------------------------------------------------------------
# _fetch_full_topic: pagination handling
# ---------------------------------------------------------------------------


class TestFetchFullTopic:
    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_fetches_missing_posts_in_chunks(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Paginated posts are fetched in chunks of 20 and merged."""
        scraper = _make_scraper(tmp_path)

        # Initial topic fetch: stream has 25 IDs, but only 5 posts inline
        initial = {
            "post_stream": {
                "stream": list(range(1, 26)),  # 25 post IDs
                "posts": [{"id": i} for i in range(1, 6)],  # 5 posts
            },
        }

        # Paginated fetch returns the remaining posts
        extra_page = {
            "post_stream": {
                "posts": [{"id": i} for i in range(6, 26)],  # 20 posts
            },
        }

        mock_urlopen.side_effect = [
            _urlopen_json(initial),
            _urlopen_json(extra_page),
        ]

        result = scraper._fetch_full_topic(1)

        assert result is not None
        assert len(result["post_stream"]["posts"]) == 25

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_tolerance_threshold_returns_none(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """If >5% of posts are missing after pagination, returns None."""
        scraper = _make_scraper(tmp_path)

        # Stream has 100 IDs but we only get 90 (10% missing)
        initial = {
            "post_stream": {
                "stream": list(range(1, 101)),  # 100 IDs
                "posts": [{"id": i} for i in range(1, 91)],  # 90 posts
            },
        }
        # No extra pages succeed
        mock_urlopen.side_effect = [
            _urlopen_json(initial),
            _urlopen_json({"post_stream": {"posts": []}}),  # empty extra
        ]

        result = scraper._fetch_full_topic(1)

        assert result is None

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_within_tolerance_returns_data(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """If <=5% posts are missing, data is returned with a note."""
        scraper = _make_scraper(tmp_path)

        # Stream has 100 IDs, we get 96 (4% missing)
        initial = {
            "post_stream": {
                "stream": list(range(1, 101)),
                "posts": [{"id": i} for i in range(1, 97)],  # 96 posts
            },
        }
        mock_urlopen.side_effect = [
            _urlopen_json(initial),
            _urlopen_json({"post_stream": {"posts": []}}),
            _urlopen_json({"post_stream": {"posts": []}}),
        ]

        result = scraper._fetch_full_topic(1)

        assert result is not None
        assert len(result["post_stream"]["posts"]) == 96

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_404_returns_none(self, mock_urlopen, mock_sleep, tmp_path: Path) -> None:
        scraper = _make_scraper(tmp_path)
        mock_urlopen.side_effect = _make_http_error(404)
        result = scraper._fetch_full_topic(999)
        assert result is None


# ---------------------------------------------------------------------------
# _fetch_json: retry behavior
# ---------------------------------------------------------------------------


class TestFetchJsonRetry:
    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_429_with_retry_after_respects_min_delay(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """429 with Retry-After lower than delay uses delay instead."""
        scraper = _make_scraper(tmp_path, delay=10.0)

        err_429 = _make_http_error(429, headers={"Retry-After": "1"})
        success = _urlopen_json({"ok": True})
        mock_urlopen.side_effect = [err_429, success]

        result = scraper._fetch_json("/test")

        assert result == {"ok": True}
        # max(1, 10.0) = 10.0
        mock_sleep.assert_any_call(10.0)

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_429_invalid_retry_after_uses_backoff(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """429 with non-integer Retry-After uses exponential backoff."""
        scraper = _make_scraper(tmp_path, delay=1.0)

        err_429 = _make_http_error(429, headers={"Retry-After": "Wed, 01 Jan 2025 00:00:00 GMT"})
        success = _urlopen_json({"ok": True})
        mock_urlopen.side_effect = [err_429, success]

        result = scraper._fetch_json("/test")

        assert result == {"ok": True}
        # Fallback: delay * 2^0 = 1.0
        mock_sleep.assert_any_call(1.0)

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_403_returns_none_immediately(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """403 is not retried, returns None."""
        scraper = _make_scraper(tmp_path)
        mock_urlopen.side_effect = _make_http_error(403)

        result = scraper._fetch_json("/forbidden")

        assert result is None
        assert mock_urlopen.call_count == 1  # no retry

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_410_returns_none_immediately(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """410 Gone is not retried, returns None."""
        scraper = _make_scraper(tmp_path)
        mock_urlopen.side_effect = _make_http_error(410)

        result = scraper._fetch_json("/gone")

        assert result is None
        assert mock_urlopen.call_count == 1

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_malformed_json_returns_none(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Malformed JSON response returns None (no retry)."""
        scraper = _make_scraper(tmp_path)

        resp = MagicMock()
        resp.read.return_value = b"not json at all"
        resp.__enter__ = lambda self: self
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp

        result = scraper._fetch_json("/test")

        assert result is None

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_5xx_exponential_backoff(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """5xx errors use exponential backoff: delay * 2^attempt."""
        scraper = _make_scraper(tmp_path, delay=1.0, max_retries=3)

        err_500 = _make_http_error(500)
        success = _urlopen_json({"ok": True})
        mock_urlopen.side_effect = [err_500, err_500, success]

        result = scraper._fetch_json("/test")

        assert result == {"ok": True}
        assert mock_sleep.call_count >= 2
        mock_sleep.assert_any_call(1.0)   # attempt 0: 1.0 * 2^0
        mock_sleep.assert_any_call(2.0)   # attempt 1: 1.0 * 2^1

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_network_error_retried(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Network errors (URLError) are retried with backoff."""
        scraper = _make_scraper(tmp_path, delay=0.5, max_retries=3)

        net_err = urllib.error.URLError("connection refused")
        success = _urlopen_json({"ok": True})
        mock_urlopen.side_effect = [net_err, success]

        result = scraper._fetch_json("/test")

        assert result == {"ok": True}

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_all_retries_exhausted_returns_none(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """After exhausting max_retries, returns None."""
        scraper = _make_scraper(tmp_path, delay=0.1, max_retries=2)

        err_500 = _make_http_error(500)
        mock_urlopen.side_effect = [err_500, err_500]

        result = scraper._fetch_json("/test")

        assert result is None


# ---------------------------------------------------------------------------
# build_index: periodic checkpoint saves
# ---------------------------------------------------------------------------


class TestBuildIndexCheckpoint:
    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_checkpoint_saves_during_category_crawl(
        self, mock_urlopen, mock_sleep, tmp_path: Path,
    ) -> None:
        """Index is saved to disk every 5 categories during initial build."""
        scraper = _make_scraper(tmp_path)

        categories = [
            {"id": i, "slug": f"cat-{i}", "name": f"Cat {i}", "topic_count": 1}
            for i in range(7)
        ]

        def _mock_fetch_json(path):
            if "/latest" in path:
                return {"topic_list": {"topics": []}}
            if "page=0" in path:
                cat_id = int(path.split("/c/")[1].split("/")[1].split(".")[0])
                return {
                    "topic_list": {
                        "topics": [{
                            "id": 1000 + cat_id,
                            "title": f"Topic {cat_id}",
                            "category_id": cat_id,
                            "posts_count": 1,
                            "created_at": "",
                            "last_posted_at": "",
                            "views": 0,
                            "like_count": 0,
                        }],
                    },
                }
            return {"topic_list": {"topics": []}}

        save_calls = []
        original_save = _save_json

        def tracking_save(path, data):
            save_calls.append(str(path))
            original_save(path, data)

        with (
            patch.object(scraper, "_fetch_json", side_effect=_mock_fetch_json),
            patch.object(scraper, "_throttle"),
            patch("scraper.discourse._save_json", side_effect=tracking_save),
        ):
            scraper.build_index(categories)

        index_saves = [s for s in save_calls if "index.json" in s]
        # Checkpoint at i=4 (5th category) + final save = at least 2
        assert len(index_saves) >= 2


# ---------------------------------------------------------------------------
# _save_json: atomic writes
# ---------------------------------------------------------------------------


class TestSaveJson:
    def test_atomic_write_creates_file(self, tmp_path: Path) -> None:
        path = tmp_path / "data.json"
        _save_json(path, {"key": "value"})

        assert path.exists()
        data = json.loads(path.read_text())
        assert data == {"key": "value"}

    def test_atomic_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        path = tmp_path / "deep" / "nested" / "data.json"
        _save_json(path, [1, 2, 3])

        assert path.exists()
        assert json.loads(path.read_text()) == [1, 2, 3]

    def test_atomic_write_overwrites_existing(self, tmp_path: Path) -> None:
        path = tmp_path / "data.json"
        _save_json(path, {"v": 1})
        _save_json(path, {"v": 2})

        assert json.loads(path.read_text()) == {"v": 2}

    def test_no_temp_files_left_on_success(self, tmp_path: Path) -> None:
        path = tmp_path / "data.json"
        _save_json(path, {"ok": True})

        tmp_files = list(tmp_path.glob("*.tmp"))
        assert tmp_files == []

    def test_unicode_content_preserved(self, tmp_path: Path) -> None:
        path = tmp_path / "unicode.json"
        _save_json(path, {"text": "G\u00f6del \u2208 \u2200x"})

        data = json.loads(path.read_text(encoding="utf-8"))
        assert "G\u00f6del" in data["text"]
