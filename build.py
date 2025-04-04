#!/usr/bin/env python3
"""Build the blog: posts/*.md -> blog/<slug>.html + blog/index.html,
and refresh the recent-posts block in index.html.

Usage:
    python3 build.py

Requires: markdown-it-py  (pip install markdown-it-py)

Post format (posts/YYYY-MM-DD-slug.md):

    ---
    title: My post
    date: 2026-07-27
    tag: systems
    excerpt: One-line summary shown in listings.
    ---

    Markdown body...
"""

from __future__ import annotations

import html
import re
import sys
from datetime import date
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError:
    sys.exit("error: markdown-it-py not installed — run: pip install markdown-it-py")

ROOT = Path(__file__).resolve().parent
POSTS_DIR = ROOT / "posts"
BLOG_DIR = ROOT / "blog"
INDEX_HTML = ROOT / "index.html"
MAX_RECENT = 5  # posts shown on the homepage

md = MarkdownIt("default", {"html": True})

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — YJMSTR</title>
  <meta name="description" content="{description}" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23111618'/%3E%3Ctext x='32' y='43' font-family='Menlo, monospace' font-size='30' font-weight='700' fill='%234ade80' text-anchor='middle'%3E%3E_%3C/text%3E%3C/svg%3E" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{prefix}style.css" />
  <script>
    window.MathJax = {{ tex: {{ inlineMath: [['$', '$']], displayMath: [['$$', '$$']] }}, svg: {{ fontCache: 'global' }} }};
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
"""

HEADER = """  <div class="page">
    <header class="page-header">
      <span class="crumb mono"><a href="{prefix}index.html">~</a> / <a href="{prefix}blog/index.html">blog</a></span>
      <button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">
        <svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
        <svg class="icon-moon" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
      </button>
    </header>
"""

FOOT = """  </div>
  <script src="{prefix}script.js"></script>
</body>
</html>
"""


def parse_post(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        sys.exit(f"error: {path.name} is missing its --- front matter --- block")
    meta_raw, body = m.group(1), m.group(2)

    meta: dict[str, str] = {}
    for line in meta_raw.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")

    for field in ("title", "date"):
        if field not in meta:
            sys.exit(f"error: {path.name} front matter missing '{field}'")

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    words = len(re.sub(r"[#*`>\-\[\]()`]", " ", body).split())
    return {
        "slug": slug,
        "title": meta["title"],
        "date": meta["date"],
        "tag": meta.get("tag", "notes"),
        "excerpt": meta.get("excerpt", ""),
        "minutes": max(1, round(words / 200)),
        "html": md.render(body),
    }


def post_item_html(post: dict, prefix: str) -> str:
    excerpt = (
        f'\n            <p class="post-excerpt">{html.escape(post["excerpt"])}</p>'
        if post["excerpt"]
        else ""
    )
    return (
        f'          <li>\n'
        f'            <a class="post-title" href="{prefix}blog/{post["slug"]}.html">{html.escape(post["title"])}</a>\n'
        f'            <span class="post-meta mono">{post["date"]} · {html.escape(post["tag"])} · {post["minutes"]} min</span>'
        f'{excerpt}\n'
        f'          </li>'
    )


def build_post_page(post: dict, prev_post: dict | None, next_post: dict | None) -> str:
    nav_prev = (
        f'<a class="nav-prev" href="{prev_post["slug"]}.html" title="{html.escape(prev_post["title"])}">← {html.escape(prev_post["title"])}</a>'
        if prev_post else "<span></span>"
    )
    nav_next = (
        f'<a class="nav-next" href="{next_post["slug"]}.html" title="{html.escape(next_post["title"])}">{html.escape(next_post["title"])} →</a>'
        if next_post else "<span></span>"
    )
    return (
        HEAD.format(title=html.escape(post["title"]), description=html.escape(post["excerpt"]), prefix="../")
        + '  <div class="progress-bar" id="progress-bar"></div>\n'
        + HEADER.format(prefix="../")
        + f"""    <article class="article">
      <h1 class="article-title"><span class="prompt mono">~/</span>{html.escape(post["title"])}</h1>
      <p class="article-meta mono">{post["date"]} · {html.escape(post["tag"])} · {post["minutes"]} min read</p>
      {post["html"]}
      <p class="eof mono">// EOF</p>
      <nav class="post-nav mono">
        {nav_prev}
        {nav_next}
      </nav>
    </article>
"""
        + FOOT.format(prefix="../")
    )


def build_blog_index(posts: list[dict]) -> str:
    items = "\n".join(
        f'        <div class="index-post">\n'
        f'          <span class="index-num mono">{i:02d}</span>\n'
        f'          <div class="index-body">\n'
        f'            <a class="post-title" href="{p["slug"]}.html">{html.escape(p["title"])}</a>\n'
        f'            <span class="post-meta mono">{p["date"]} · {html.escape(p["tag"])} · {p["minutes"]} min</span>\n'
        + (f'            <p class="post-excerpt">{html.escape(p["excerpt"])}</p>\n' if p["excerpt"] else "")
        + f'          </div>\n'
        f'        </div>'
        for i, p in enumerate(posts, 1)
    )
    return (
        HEAD.format(title="Blog", description="Writing by YJMSTR", prefix="../")
        + HEADER.format(prefix="../")
        + f"""    <h1 class="article-title"><span class="prompt mono">~/</span>blog</h1>
    <p class="article-meta mono">{len(posts)} post(s) · mlsys &amp; notes</p>
    <div class="blog-index">
{items}
    </div>
"""
        + FOOT.format(prefix="../")
    )


def update_homepage(posts: list[dict]) -> None:
    source = INDEX_HTML.read_text(encoding="utf-8")
    recent = posts[:MAX_RECENT]
    if recent:
        items = "\n".join(post_item_html(p, "") for p in recent)
        block = f'        <ul class="post-list">\n{items}\n        </ul>'
    else:
        block = '        <p class="post-excerpt">Nothing here yet — first post is in the works.</p>'

    pattern = re.compile(r"(<!-- POSTS:BEGIN.*?-->).*?(<!-- POSTS:END -->)", re.DOTALL)
    if not pattern.search(source):
        sys.exit("error: POSTS:BEGIN/END markers not found in index.html")
    updated = pattern.sub(lambda m: m.group(1) + "\n" + block + "\n        " + m.group(2), source)
    INDEX_HTML.write_text(updated, encoding="utf-8")


def main() -> None:
    BLOG_DIR.mkdir(exist_ok=True)
    post_files = sorted(POSTS_DIR.glob("*.md"))
    posts = [parse_post(p) for p in post_files]
    posts.sort(key=lambda p: p["date"], reverse=True)

    slugs = [p["slug"] for p in posts]
    if len(slugs) != len(set(slugs)):
        sys.exit("error: duplicate post slugs — check filenames in posts/")

    for i, post in enumerate(posts):
        prev_post = posts[i - 1] if i > 0 else None  # newer
        next_post = posts[i + 1] if i + 1 < len(posts) else None  # older
        out = BLOG_DIR / f"{post['slug']}.html"
        out.write_text(build_post_page(post, prev_post, next_post), encoding="utf-8")
        print(f"built  blog/{post['slug']}.html")

    (BLOG_DIR / "index.html").write_text(build_blog_index(posts), encoding="utf-8")
    print(f"built  blog/index.html")

    update_homepage(posts)
    print(f"updated index.html ({min(len(posts), MAX_RECENT)} recent post(s))")


if __name__ == "__main__":
    main()
