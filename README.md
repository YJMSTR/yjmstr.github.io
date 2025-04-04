# yjmstr.github.io

Personal homepage of **Yangjie Zhang** — hand-rolled static site, no framework.
Deployed via GitHub Pages from the repository root.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Homepage (about / news / recent posts / experience / education / misc) |
| `style.css` | All styles, light & dark themes (follows system, toggle in footer) |
| `script.js` | Theme toggle + footer year |
| `avatar.jpg` | Sidebar avatar photo |
| `photos/` | Photo gallery page + compressed images (astrophotography & aerial) |
| `posts/` | Blog posts in Markdown, one file per post |
| `build.py` | Builds `posts/` → `blog/` pages + refreshes the homepage post list |
| `blog/` | Generated blog pages (do not edit by hand) |

## Writing a new post

1. Create `posts/YYYY-MM-DD-my-slug.md`:

   ```markdown
   ---
   title: My post title
   date: 2026-08-01
   tag: systems
   excerpt: One-line summary shown in listings.
   ---

   Markdown body…
   ```

2. Run the build (needs `pip install markdown-it-py` once):

   ```bash
   python3 build.py
   ```

   This regenerates `blog/<slug>.html`, rebuilds `blog/index.html`, and updates
   the `~/blog` section on the homepage (the block between the
   `<!-- POSTS:BEGIN -->` / `<!-- POSTS:END -->` markers).

3. Commit and push — GitHub Pages serves the result as-is.

## Local preview

```bash
python3 -m http.server 7100   # or: npm run dev
# open http://localhost:7100/
```

## Customization notes

- **Photo**: replace `avatar.jpg` with any square photo (460×460 or similar).
- **Theme colors**: CSS variables at the top of `style.css`
  (`:root` for light, `[data-theme="dark"]` for dark).
