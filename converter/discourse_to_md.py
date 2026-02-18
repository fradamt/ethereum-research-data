"""Convert Discourse topic JSON files to markdown with YAML frontmatter.

Handles HTML-to-markdown conversion for Discourse 'cooked' content and
preserves any enrichment fields already present in existing output files.

Stdlib-only, Python 3.10+.
"""

from __future__ import annotations

import html
import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# YAML frontmatter helpers
# ---------------------------------------------------------------------------

def _yaml_scalar(value: object) -> str:
    """Encode a scalar value for YAML frontmatter."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value}"
    s = str(value)
    # Quote if the string contains characters that need quoting in YAML
    if (
        s == ""
        or s[0] in "-?:,[]{}#&*!|>'\"%@`"
        or ": " in s
        or s.startswith("- ")
        or "\n" in s
        or "\r" in s
        or s in ("true", "false", "null", "yes", "no", "on", "off")
        or s != s.strip()
        or re.match(r"^[\d.eE+-]+$", s)
    ):
        escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
        return f'"{escaped}"'
    return s


def _yaml_list(items: list) -> str:
    """Encode a list for inline YAML: [item1, item2]."""
    return "[" + ", ".join(_yaml_scalar(i) for i in items) + "]"


def dump_frontmatter(fields: dict) -> str:
    """Render a dict as YAML frontmatter (--- delimited).

    Supports scalars and flat lists.  Does not attempt nested dicts — those
    are serialized as JSON strings to keep parsing simple.
    """
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}: {_yaml_list(value)}")
        elif isinstance(value, dict):
            # Fallback: serialize nested dicts as JSON strings
            lines.append(f"{key}: {_yaml_scalar(json.dumps(value))}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown string.

    Returns (frontmatter_dict, body_without_frontmatter).
    Only handles the subset of YAML we produce: scalars, inline lists, quoted
    strings.  This keeps us stdlib-only.
    """
    if not text.startswith("---"):
        return {}, text

    # Find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    fm_text = text[4:end]  # skip opening ---\n
    body = text[end + 4:]  # skip \n---
    if body.startswith("\n"):
        body = body[1:]

    result: dict = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        colon = line.find(":")
        if colon == -1:
            continue
        key = line[:colon].strip()
        raw_value = line[colon + 1:].strip()
        result[key] = _parse_yaml_value(raw_value)

    return result, body


def _parse_yaml_value(raw: str) -> object:
    """Parse a simple YAML value: string, int, float, bool, null, or list."""
    if not raw:
        return ""

    # Inline list: [a, b, c]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items = _split_yaml_list(inner)
        return [_parse_yaml_value(item.strip()) for item in items]

    # Quoted string
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        s = raw[1:-1]
        s = s.replace("\\\\", "\x00").replace('\\"', '"').replace("\\n", "\n").replace("\\r", "\r").replace("\x00", "\\")
        return s

    # Bool / null
    if raw in ("true", "yes", "on"):
        return True
    if raw in ("false", "no", "off"):
        return False
    if raw == "null":
        return None

    # Int
    try:
        return int(raw)
    except ValueError:
        pass

    # Float
    try:
        return float(raw)
    except ValueError:
        pass

    return raw


def _split_yaml_list(s: str) -> list[str]:
    """Split a comma-separated inline YAML list, respecting quotes."""
    items = []
    current = []
    in_quote = None
    for ch in s:
        if ch in ('"', "'") and in_quote is None:
            in_quote = ch
            current.append(ch)
        elif ch == in_quote:
            in_quote = None
            current.append(ch)
        elif ch == "," and in_quote is None:
            items.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        items.append("".join(current))
    return items


# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------

def html_to_markdown(h: str) -> str:
    """Convert Discourse 'cooked' HTML to markdown.

    Handles the elements commonly found in Discourse posts: headings, bold,
    italic, code, links, lists, blockquotes, pre/code blocks, images, tables,
    line breaks, and horizontal rules.
    """
    if not h:
        return ""
    text = h

    # --- Pre/code blocks (must come first to protect contents) ---
    text = _convert_pre_blocks(text)

    # --- Block-level elements ---

    # Headings — strip inner anchor tags that Discourse adds
    def _heading(m: re.Match) -> str:
        level = int(m.group(1))
        inner = re.sub(r"<a[^>]*>.*?</a>", "", m.group(2), flags=re.DOTALL).strip()
        inner = _strip_tags(inner)
        return f"\n\n{'#' * level} {inner}\n\n"

    text = re.sub(
        r"<h([1-6])[^>]*>(.*?)</h\1>",
        _heading,
        text,
        flags=re.DOTALL,
    )

    # Blockquotes (may be nested — handle outer only, inner tags cleaned later)
    text = re.sub(
        r"<blockquote[^>]*>(.*?)</blockquote>",
        _convert_blockquote,
        text,
        flags=re.DOTALL,
    )

    # Tables
    text = _convert_tables(text)

    # Horizontal rules
    text = re.sub(r"<hr\s*/?>", "\n\n---\n\n", text)

    # --- Lists ---
    text = _convert_lists(text)

    # --- Inline elements ---

    # Images — use alt text and src
    text = re.sub(
        r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/?\s*>',
        r"![\2](\1)",
        text,
    )
    text = re.sub(
        r'<img[^>]*alt="([^"]*)"[^>]*src="([^"]*)"[^>]*/?\s*>',
        r"![\1](\2)",
        text,
    )
    # Images with no alt
    text = re.sub(
        r'<img[^>]*src="([^"]*)"[^>]*/?\s*>',
        r"![image](\1)",
        text,
    )

    # Links
    text = re.sub(
        r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        _convert_link,
        text,
        flags=re.DOTALL,
    )

    # Bold / strong
    text = re.sub(r"<(?:strong|b)>(.*?)</(?:strong|b)>", r"**\1**", text, flags=re.DOTALL)

    # Italic / em
    text = re.sub(r"<(?:em|i)>(.*?)</(?:em|i)>", r"*\1*", text, flags=re.DOTALL)

    # Inline code (not inside pre blocks — those are already handled)
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)

    # Strikethrough
    text = re.sub(r"<(?:del|s)>(.*?)</(?:del|s)>", r"~~\1~~", text, flags=re.DOTALL)

    # Superscript / subscript — just keep the text
    text = re.sub(r"<su[bp]>(.*?)</su[bp]>", r"\1", text, flags=re.DOTALL)

    # --- Paragraph / line breaks ---
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<p[^>]*>", "\n\n", text)
    text = re.sub(r"</p>", "\n\n", text)

    # Discourse aside / details blocks — just keep content
    text = re.sub(r"<aside[^>]*>", "\n\n", text)
    text = re.sub(r"</aside>", "\n\n", text)
    text = re.sub(r"<details[^>]*>", "\n\n", text)
    text = re.sub(r"</details>", "\n\n", text)
    text = re.sub(r"<summary[^>]*>(.*?)</summary>", r"**\1**\n\n", text, flags=re.DOTALL)

    # Discourse mentions — @username
    text = re.sub(r'<a class="mention"[^>]*>(@\w+)</a>', r"\1", text)

    # Divs, spans, and other wrapper tags — just remove them
    text = re.sub(r"</?(?:div|span|section|article|header|footer|nav|figure|figcaption)[^>]*>", "", text)

    # Strip any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Unescape HTML entities
    text = html.unescape(text)

    # --- Whitespace cleanup ---
    # Collapse runs of blank lines to at most two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove leading/trailing whitespace on each line but preserve blank lines
    lines = text.split("\n")
    lines = [line.rstrip() for line in lines]
    text = "\n".join(lines)

    return text.strip()


def _convert_pre_blocks(text: str) -> str:
    """Convert <pre><code>...</code></pre> blocks to fenced code blocks."""

    def _replace_pre(m: re.Match) -> str:
        # Try to extract language from class attribute
        lang = ""
        class_match = re.search(r'class="[^"]*lang-(\w+)', m.group(0))
        if class_match:
            lang = class_match.group(1)
        # Get the content between the innermost tags
        content = m.group(1)
        # Strip <code> wrapper if present
        code_match = re.match(r"\s*<code[^>]*>(.*)</code>\s*", content, re.DOTALL)
        if code_match:
            content = code_match.group(1)
        content = html.unescape(content)
        # Trim a single leading/trailing newline
        if content.startswith("\n"):
            content = content[1:]
        if content.endswith("\n"):
            content = content[:-1]
        return f"\n\n```{lang}\n{content}\n```\n\n"

    text = re.sub(r"<pre[^>]*>(.*?)</pre>", _replace_pre, text, flags=re.DOTALL)
    return text


def _convert_blockquote(m: re.Match) -> str:
    """Convert a blockquote to markdown > prefix lines."""
    inner = m.group(1).strip()
    # Strip <p> tags inside blockquotes
    inner = re.sub(r"</?p[^>]*>", "\n", inner)
    inner = re.sub(r"<[^>]+>", "", inner)
    inner = html.unescape(inner).strip()
    lines = inner.split("\n")
    return "\n\n" + "\n".join("> " + line for line in lines) + "\n\n"


def _convert_link(m: re.Match) -> str:
    """Convert an <a> tag to a markdown link."""
    href = m.group(1)
    inner = _strip_tags(m.group(2)).strip()
    if not inner or inner == href:
        return href
    return f"[{inner}]({href})"


def _convert_lists(text: str) -> str:
    """Convert HTML ordered and unordered lists to markdown."""

    def _replace_list(m: re.Match) -> str:
        tag = m.group(1)  # "ul" or "ol"
        content = m.group(2)
        items = re.findall(r"<li[^>]*>(.*?)</li>", content, re.DOTALL)
        lines = []
        for i, item in enumerate(items):
            item_text = re.sub(r"</?p[^>]*>", " ", item).strip()
            item_text = _strip_tags(item_text).strip()
            item_text = html.unescape(item_text)
            if tag == "ol":
                lines.append(f"{i + 1}. {item_text}")
            else:
                lines.append(f"- {item_text}")
        return "\n\n" + "\n".join(lines) + "\n\n"

    text = re.sub(
        r"<(ol|ul)[^>]*>(.*?)</\1>",
        _replace_list,
        text,
        flags=re.DOTALL,
    )
    return text


def _convert_tables(text: str) -> str:
    """Convert HTML tables to markdown tables."""

    def _replace_table(m: re.Match) -> str:
        table_html = m.group(0)

        # Extract header cells
        thead_match = re.search(r"<thead>(.*?)</thead>", table_html, re.DOTALL)
        headers = []
        if thead_match:
            headers = re.findall(r"<th[^>]*>(.*?)</th>", thead_match.group(1), re.DOTALL)
            headers = [_strip_tags(h).strip() for h in headers]

        # Extract body rows
        tbody_match = re.search(r"<tbody>(.*?)</tbody>", table_html, re.DOTALL)
        body_html = tbody_match.group(1) if tbody_match else table_html
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", body_html, re.DOTALL)

        md_rows = []
        for row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
            cells = [_strip_tags(c).strip() for c in cells]
            if cells:
                md_rows.append(cells)

        if not headers and not md_rows:
            return m.group(0)  # Give up — return original

        # If no explicit headers but we have rows, use the first row
        if not headers and md_rows:
            headers = md_rows.pop(0)

        ncols = max(len(headers), *(len(r) for r in md_rows) if md_rows else [0])
        # Pad headers and rows to uniform width
        headers += [""] * (ncols - len(headers))
        md_rows = [r + [""] * (ncols - len(r)) for r in md_rows]

        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
        for row in md_rows:
            lines.append("| " + " | ".join(row) + " |")

        return "\n\n" + "\n".join(lines) + "\n\n"

    text = re.sub(r"<table[^>]*>.*?</table>", _replace_table, text, flags=re.DOTALL)
    return text


def _strip_tags(s: str) -> str:
    """Remove all HTML tags from a string."""
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------------------
# Category loader
# ---------------------------------------------------------------------------

def load_categories(path: Path) -> dict[int, str]:
    """Load category_id → name mapping from a Discourse categories.json."""
    data = json.loads(path.read_text(encoding="utf-8"))
    cats: dict[int, str] = {}
    for c in data.get("category_list", {}).get("categories", []):
        cats[c["id"]] = c["name"]
        for sub in c.get("subcategory_list", []):
            cats[sub["id"]] = f"{c['name']} > {sub['name']}"
    return cats


# ---------------------------------------------------------------------------
# Safe filename
# ---------------------------------------------------------------------------

_UNSAFE_RE = re.compile(r"[^\w\-]")


def safe_filename(topic_id: int, slug: str, max_slug_len: int = 60) -> str:
    """Build a filesystem-safe filename: {id}-{slug}.md."""
    slug = slug[:max_slug_len]
    slug = _UNSAFE_RE.sub("-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        slug = "topic"
    return f"{topic_id}-{slug}.md"


# ---------------------------------------------------------------------------
# Quick metadata extraction (avoids full HTML→markdown conversion)
# ---------------------------------------------------------------------------

def _extract_topic_id_slug(path: Path) -> tuple[int, str]:
    """Read just the topic_id and slug from a topic JSON file.

    This is much cheaper than a full ``convert_topic()`` call because it skips
    all HTML-to-markdown conversion.  Used by ``convert_all()`` to determine
    the output filename before deciding whether to run the expensive conversion.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    topic_id: int = data["id"]
    slug: str = data.get("slug", "topic")
    return topic_id, slug


# ---------------------------------------------------------------------------
# Converter
# ---------------------------------------------------------------------------

@dataclass
class DiscourseConverter:
    """Converts raw Discourse JSON topics to markdown files.

    Parameters
    ----------
    source_name : str
        Identifier for the source (e.g. "ethresearch").
    base_url : str
        Forum base URL (e.g. "https://ethresear.ch").
    raw_dir : Path
        Directory containing raw JSON (with topics/ and categories.json).
    corpus_dir : Path
        Output directory for markdown files.
    max_replies : int
        Maximum number of replies to include per topic (default 20).
    """

    source_name: str
    base_url: str
    raw_dir: Path
    corpus_dir: Path
    max_replies: int = 20
    _categories: dict[int, str] = field(default_factory=dict, init=False, repr=False)

    def load_categories(self) -> None:
        """Load category mappings from raw_dir/categories.json."""
        cats_path = self.raw_dir / "categories.json"
        if cats_path.exists():
            self._categories = load_categories(cats_path)

    def convert_all(self, *, force: bool = False) -> tuple[int, int]:
        """Convert all topic JSON files. Returns (converted, skipped) counts.

        By default, skips topics whose output file already exists (incremental).
        Pass ``force=True`` to re-convert everything.
        """
        self.load_categories()
        self.corpus_dir.mkdir(parents=True, exist_ok=True)

        topics_dir = self.raw_dir / "topics"
        if not topics_dir.is_dir():
            return 0, 0

        converted = 0
        skipped = 0

        for path in sorted(topics_dir.iterdir()):
            if path.suffix != ".json":
                continue

            # Quick check: extract id+slug without full conversion to
            # determine the output filename cheaply.
            try:
                topic_id, slug = _extract_topic_id_slug(path)
            except (json.JSONDecodeError, KeyError, ValueError, UnicodeDecodeError) as exc:
                print(f"  Skipping {path.name}: {exc}")
                skipped += 1
                continue

            out_path = self.corpus_dir / safe_filename(topic_id, slug)

            # Skip if output already exists and is newer than source
            if not force and out_path.exists():
                if out_path.stat().st_mtime >= path.stat().st_mtime:
                    skipped += 1
                    continue

            # Full conversion only for new/missing topics
            try:
                result = self.convert_topic(path)
            except (json.JSONDecodeError, KeyError, ValueError, UnicodeDecodeError) as exc:
                print(f"  Skipping {path.name}: {type(exc).__name__}: {exc}")
                skipped += 1
                continue

            if result is None:
                skipped += 1
                continue

            filename, content = result

            if not content.strip():
                print(f"  Warning: empty output from non-empty input {path.name}")

            out_path = self.corpus_dir / filename

            # Preserve enrichment fields from existing file
            content = self._merge_enrichment(out_path, content)

            # Atomic write: temp file + rename to prevent truncated output
            fd, tmp = tempfile.mkstemp(dir=self.corpus_dir, suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(content)
                os.replace(tmp, out_path)
            except BaseException:
                os.unlink(tmp)
                raise
            converted += 1

        return converted, skipped

    def convert_topic(self, topic_path: Path) -> tuple[str, str] | None:
        """Convert a single topic JSON to (filename, markdown_content).

        Returns None if the topic has no posts.
        """
        data = json.loads(topic_path.read_text(encoding="utf-8"))

        topic_id: int = data["id"]
        title: str = data.get("title", f"Topic {topic_id}")
        slug: str = data.get("slug", "topic")
        created: str = data.get("created_at", "")[:10]
        category = self._categories.get(data.get("category_id", 0), "Uncategorized")
        tags: list[str] = data.get("tags", []) or []
        views: int = data.get("views", 0)
        like_count: int = data.get("like_count", 0)
        posts_count: int = data.get("posts_count", 0)
        url = f"{self.base_url}/t/{slug}/{topic_id}"

        posts = data.get("post_stream", {}).get("posts", [])
        if not posts:
            return None

        # First post is the topic body
        op = posts[0]
        author = op.get("username", "unknown")
        body = html_to_markdown(op.get("cooked", ""))

        # Build frontmatter
        fm: dict = {
            "source": self.source_name,
            "topic_id": topic_id,
            "title": title,
            "author": author,
            "date": created,
            "category": category,
            "tags": tags,
            "url": url,
            "views": views,
            "likes": like_count,
            "posts_count": posts_count,
        }

        # Build markdown body
        lines: list[str] = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(body)

        # Replies
        reply_posts = posts[1: 1 + self.max_replies]
        if reply_posts:
            lines.append("")
            lines.append("## Replies")

            for post in reply_posts:
                username = post.get("username", "unknown")
                post_date = post.get("created_at", "")[:10]
                post_body = html_to_markdown(post.get("cooked", ""))
                if not post_body:
                    continue
                lines.append("")
                lines.append(f"**{username}** ({post_date}):")
                lines.append("")
                lines.append(post_body)
                lines.append("")
                lines.append("---")

            # Remove trailing --- after last reply
            if lines and lines[-1] == "---":
                lines.pop()

        remaining = len(posts) - 1 - self.max_replies
        if remaining > 0:
            lines.append("")
            lines.append(f"*({remaining} more replies not shown)*")

        filename = safe_filename(topic_id, slug)
        content = dump_frontmatter(fm) + "\n\n" + "\n".join(lines) + "\n"
        return filename, content

    def _merge_enrichment(self, out_path: Path, new_content: str) -> str:
        """If out_path already exists, preserve any extra frontmatter fields.

        This ensures that enrichment tools (influence_score, research_thread,
        related, etc.) can add metadata that survives re-conversion.
        """
        if not out_path.exists():
            return new_content

        existing_text = out_path.read_text(encoding="utf-8")
        existing_fm, _ = parse_frontmatter(existing_text)
        if not existing_fm:
            return new_content

        new_fm, new_body = parse_frontmatter(new_content)
        if not new_fm:
            return new_content

        # Find fields in existing frontmatter that are NOT in the converter's output
        converter_keys = set(new_fm.keys())
        for key, value in existing_fm.items():
            if key not in converter_keys:
                new_fm[key] = value

        return dump_frontmatter(new_fm) + "\n\n" + new_body.lstrip("\n")
