# North Shore Presbyterian — Shared Kitchen

A single-page site for the Shared Kitchen ministry at North Shore Presbyterian Church.
Matches the ministry flyer branding (deep green + gold script) and adapts automatically
to the viewer's light or dark mode.

## Contents
- `index.html` — the page (self-contained HTML/CSS, no build step)
- `images/` — web-optimized photos (hero, worship, fellowship)

## View locally
Open `index.html` in any browser, or serve the folder:
```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Publish with GitHub Pages (optional)
1. Push this repo to GitHub (see below).
2. Repo → Settings → Pages → Source: `main` branch, `/root`.
3. Your page goes live at `https://<username>.github.io/<repo>/`.

## Notes for Squarespace
Relative image paths work on GitHub Pages and local hosting. If you instead paste the
markup into a Squarespace Code block, use the self-contained version with embedded images
(images inlined as base64) since a Code block can't resolve `./images/` paths.
