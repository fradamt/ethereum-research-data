"""Generic Discourse forum scraper.

Fetches site metadata, category listings, topic index, and full topic
content (with post pagination) from any Discourse instance.  All output
is written as JSON to a configurable raw directory.

Stdlib-only — requires Python 3.10+.
"""

from __future__ import annotations

import json
import os
import ssl
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


# ---------------------------------------------------------------------------
# SSL — macOS system Python sometimes lacks default certs
# ---------------------------------------------------------------------------

_SSL_CTX = ssl.create_default_context()
for _ca in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
    if os.path.exists(_ca):
        _SSL_CTX.load_verify_locations(_ca)
        break


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _save_json(path: Path, data: object) -> None:
    """Write JSON atomically: write to a temp file then rename.

    This prevents corrupt/truncated files if the process is interrupted.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


# ---------------------------------------------------------------------------
# DiscourseScraper
# ---------------------------------------------------------------------------

class DiscourseScraper:
    """Scrape a single Discourse instance into a raw JSON directory.

    Parameters
    ----------
    base_url : str
        Root URL of the Discourse site (e.g. "https://ethresear.ch").
    raw_dir : str | Path
        Directory to write JSON output into.
    delay : float
        Base delay between HTTP requests (seconds).
    max_retries : int
        Maximum retry attempts for transient HTTP / network errors.
    """

    def __init__(
        self,
        base_url: str,
        raw_dir: str | Path,
        *,
        delay: float = 0.3,
        max_retries: int = 5,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.raw_dir = Path(raw_dir)
        self.topics_dir = self.raw_dir / "topics"
        self.delay = delay
        self.max_retries = max_retries

        # Ensure output dirs exist
        self.topics_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    def _fetch_json(self, path: str) -> dict | None:
        """GET *path* (relative to base_url) and return decoded JSON.

        Retries on 429 / 5xx / network errors with exponential backoff.
        Returns ``None`` on 404, 403, or after exhausting retries.
        """
        url = self.base_url + path
        for attempt in range(self.max_retries):
            try:
                req = urllib.request.Request(
                    url, headers={"Accept": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30, context=_SSL_CTX) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code in (404, 403, 410):
                    return None
                if exc.code == 429:
                    retry_after = exc.headers.get("Retry-After")
                    if retry_after:
                        wait = int(retry_after)
                    else:
                        wait = self.delay * (2 ** attempt)
                    print(f"  Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                if exc.code >= 500:
                    wait = self.delay * (2 ** attempt)
                    print(f"  HTTP {exc.code} on {path}, retry in {wait:.1f}s …")
                    if attempt < self.max_retries - 1:
                        time.sleep(wait)
                    continue
                print(f"  HTTP {exc.code} on {path}, not retryable")
                return None
            except json.JSONDecodeError:
                print(f"  Malformed JSON from {path}")
                return None
            except (urllib.error.URLError, OSError) as exc:
                wait = self.delay * (2 ** attempt)
                print(f"  Network error on {path}: {exc}, retry in {wait:.1f}s …")
                if attempt < self.max_retries - 1:
                    time.sleep(wait)
                continue

        print(f"  FAILED after {self.max_retries} retries: {path}")
        return None

    def _throttle(self) -> None:
        time.sleep(self.delay)

    # ------------------------------------------------------------------
    # Step 1 — Site metadata
    # ------------------------------------------------------------------

    def fetch_about(self) -> dict | None:
        """Fetch /about.json and save to raw_dir/about.json."""
        dest = self.raw_dir / "about.json"
        if dest.exists():
            print(f"  about.json exists, skipping")
            return json.loads(dest.read_text())

        print("  Fetching /about.json …")
        data = self._fetch_json("/about.json")
        if data:
            _save_json(dest, data)
            stats = data.get("about", {}).get("stats", {})
            print(
                f"    {stats.get('topics_count', '?')} topics, "
                f"{stats.get('posts_count', '?')} posts, "
                f"{stats.get('users_count', '?')} users"
            )
        self._throttle()
        return data

    # ------------------------------------------------------------------
    # Step 2 — Categories
    # ------------------------------------------------------------------

    def fetch_categories(self) -> list[dict]:
        """Fetch /categories.json and save.  Returns flat category list."""
        dest = self.raw_dir / "categories.json"
        if dest.exists():
            print(f"  categories.json exists, loading")
            data = json.loads(dest.read_text())
            cats = data.get("category_list", {}).get("categories", [])
            print(f"    {len(cats)} categories")
            return cats

        print("  Fetching /categories.json …")
        data = self._fetch_json("/categories.json?include_subcategories=true")
        if not data:
            raise RuntimeError("Failed to fetch categories from Discourse API")
        _save_json(dest, data)
        cats = data.get("category_list", {}).get("categories", [])
        print(f"    {len(cats)} categories saved")
        self._throttle()
        return cats

    # ------------------------------------------------------------------
    # Step 3 — Topic index
    # ------------------------------------------------------------------

    def build_index(self, categories: list[dict]) -> dict[str, dict]:
        """Build or incrementally update the topic index.

        On first run (no index.json), does a full category crawl plus
        /latest sweep.  On subsequent runs, only sweeps /latest pages
        until all topic IDs on a page are already known.

        Returns ``{topic_id_str: metadata_dict, …}``.
        Saves to raw_dir/index.json.
        """
        dest = self.raw_dir / "index.json"

        if dest.exists():
            index: dict[str, dict] = json.loads(dest.read_text())
            prev_count = len(index)
            print(f"  index.json exists ({prev_count} topics), checking for new …")
            index = self._update_index_from_latest(index)
            new_count = len(index) - prev_count
            if new_count > 0:
                _save_json(dest, index)
                print(f"    Added {new_count} new topics (total {len(index)})")
            else:
                print(f"    Index is up to date ({len(index)} topics)")
            return index

        # --- First-time full build ---
        print("  Building topic index …")
        index = {}

        # Flatten categories including subcategories
        all_cats = []
        for cat in categories:
            all_cats.append(cat)
            for sub in cat.get("subcategory_list", []):
                all_cats.append(sub)

        for cat in all_cats:
            cat_id = cat["id"]
            cat_slug = cat["slug"]
            cat_name = cat["name"]
            topic_count = cat.get("topic_count", 0)
            print(f"    Category: {cat_name} ({topic_count} topics)")

            page = 0
            while True:
                data = self._fetch_json(f"/c/{cat_slug}/{cat_id}.json?page={page}")
                self._throttle()
                if not data:
                    break

                topics = data.get("topic_list", {}).get("topics", [])
                if not topics:
                    break

                for t in topics:
                    tid = str(t["id"])
                    if tid not in index:
                        index[tid] = self._topic_meta(t, cat_name)

                if not data.get("topic_list", {}).get("more_topics_url"):
                    break
                page += 1

            print(f"      {len(index)} total so far")

        # Also sweep /latest for the initial build
        index = self._update_index_from_latest(index)

        _save_json(dest, index)
        print(f"    Index saved: {len(index)} topics")
        return index

    def _update_index_from_latest(self, index: dict[str, dict]) -> dict[str, dict]:
        """Sweep /latest.json pages and add new topics to *index*.

        Stops paginating when every topic ID on a page is already in the
        index (topics are returned in reverse chronological order, so
        hitting a fully-known page means we have caught up).
        """
        known_ids = set(index)
        print("    Sweeping /latest …")
        page = 0
        while True:
            data = self._fetch_json(f"/latest.json?page={page}")
            self._throttle()
            if not data:
                break

            topics = data.get("topic_list", {}).get("topics", [])
            if not topics:
                break

            all_known = True
            for t in topics:
                tid = str(t["id"])
                if tid not in known_ids:
                    all_known = False
                    known_ids.add(tid)
                    index[tid] = self._topic_meta(t, "")

            if all_known:
                print(f"      Page {page}: all topics known, stopping")
                break

            if not data.get("topic_list", {}).get("more_topics_url"):
                break
            page += 1

        return index

    @staticmethod
    def _topic_meta(t: dict, category_name: str) -> dict:
        return {
            "id": t["id"],
            "title": t.get("title", ""),
            "category_id": t.get("category_id"),
            "category_name": category_name,
            "posts_count": t.get("posts_count", 0),
            "created_at": t.get("created_at", ""),
            "last_posted_at": t.get("last_posted_at", ""),
            "views": t.get("views", 0),
            "like_count": t.get("like_count", 0),
        }

    # ------------------------------------------------------------------
    # Step 4 — Full topic content
    # ------------------------------------------------------------------

    def fetch_topics(self, index: dict[str, dict]) -> None:
        """Fetch full JSON for every topic in *index*.

        Skips topics whose JSON already exists (incremental).
        """
        topic_ids = sorted(index, key=lambda x: int(x))
        total = len(topic_ids)
        skipped = fetched = failed = 0

        print(f"  Fetching {total} topics …")

        for tid in topic_ids:
            dest = self.topics_dir / f"{tid}.json"
            if dest.exists():
                skipped += 1
                continue

            data = self._fetch_full_topic(int(tid))
            self._throttle()

            if data:
                _save_json(dest, data)
                fetched += 1
            else:
                failed += 1

            done = skipped + fetched + failed
            if done % 100 == 0 or done == total:
                print(
                    f"    {done}/{total}  "
                    f"(fetched={fetched} skipped={skipped} failed={failed})"
                )

        print(
            f"    Done: fetched={fetched}, skipped={skipped}, failed={failed}"
        )

    def _fetch_full_topic(self, topic_id: int) -> dict | None:
        """Fetch a topic and all its posts (handling Discourse pagination)."""
        data = self._fetch_json(f"/t/{topic_id}.json")
        if not data:
            return None

        post_stream = data.get("post_stream", {})
        all_ids = post_stream.get("stream", [])
        posts = post_stream.get("posts", [])
        fetched_ids = {p["id"] for p in posts}

        missing = [pid for pid in all_ids if pid not in fetched_ids]
        chunk_size = 20
        for i in range(0, len(missing), chunk_size):
            chunk = missing[i : i + chunk_size]
            params = "&".join(f"post_ids[]={pid}" for pid in chunk)
            extra = self._fetch_json(f"/t/{topic_id}/posts.json?{params}")
            self._throttle()
            if extra and "post_stream" in extra:
                posts.extend(extra["post_stream"].get("posts", []))

        if "post_stream" in data:
            data["post_stream"]["posts"] = posts

        got = len(posts)
        expected = len(all_ids)
        if got < expected:
            print(f"  Warning: topic {topic_id} has {got}/{expected} posts (some pages failed)")

        return data

    # ------------------------------------------------------------------
    # Run all steps
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Execute the full scraping pipeline for this source."""
        print(f"\n{'=' * 60}")
        print(f"Scraping {self.base_url}")
        print(f"  Output: {self.raw_dir}")
        print(f"{'=' * 60}")

        self.fetch_about()
        categories = self.fetch_categories()
        index = self.build_index(categories)
        self.fetch_topics(index)

        topic_files = list(self.topics_dir.glob("*.json"))
        print(f"\n  Summary: {len(index)} indexed, {len(topic_files)} saved")
