# PharmaPulse 📈💊

**A fast, static, auto-updating web app delivering weekly pharma & drug-industry
intelligence** — FDA approvals, Phase III readouts, biosimilars, complete
response letters, M&A and regulatory shifts — each paired with a concise
**impact analysis** of the competitive, pricing and market implications.

🔗 **Live:** https://sharjeel45557.github.io/drug-app/

![PharmaPulse social preview](docs/og-image.png)

## Highlights

- **Zero-backend.** A single curated data file (`docs/feed.json`) is rendered to
  a static page and served free on GitHub Pages.
- **Works without JavaScript.** Every story is server-rendered into the HTML;
  JS only layers on live search + category filtering. Robust everywhere,
  including locked-down corporate browsers.
- **Auto-updates weekly.** A GitHub Actions job regenerates the feed and opens a
  pull request for review — content refreshes without touching code.
- **Installable.** Web-app manifest + icons mean "Add to Home Screen" gives an
  app-like experience on mobile.
- **Mobile-first & dark-mode aware**, with category colour-coding and a clean
  card/expand reading flow.

## How it works

```
  Weekly pipeline                         GitHub Pages (free)        Anyone
  ───────────────                         ───────────────────        ──────
  search → classify → impact analysis     docs/feed.json
        │                                       │
        └── build_web.py renders ──────────▶ docs/index.html ──────▶ browser / phone
```

`docs/feed.json` is the single source of truth. `pipeline/build_web.py` renders
it into the static `docs/index.html`. Edit the **feed**, not the HTML.

## Repo layout

| Path | What it is |
|------|------------|
| `docs/index.html` | the published static site (generated) |
| `docs/feed.json` | the curated data — **the one file you edit** |
| `docs/*.png`, `docs/manifest.webmanifest` | icons, social preview, PWA manifest |
| `pipeline/build_web.py` | renders `feed.json` → `index.html` |
| `pipeline/make_icon.py` | regenerates icons + social card |
| `pipeline/generate_feed.py` | weekly feed generator (Claude API + web search) |
| `pipeline/feed.schema.json` | JSON schema the feed is validated against |
| `pipeline/PIPELINE.md`, `pipeline/generation-prompt.md` | the weekly runbook |
| `.github/workflows/weekly-feed.yml` | the scheduled auto-update job |

## Run / build locally

```bash
python3 pipeline/build_web.py     # regenerate docs/index.html from docs/feed.json
open docs/index.html              # view it (or just double-click)
```

No build tools or dependencies needed to view — it's plain HTML/CSS/JS.

## Deploy (GitHub Pages)

**Settings → Pages → Deploy from a branch → `main` / `/docs` → Save.**
Live at `https://sharjeel45557.github.io/drug-app/` in ~1 minute. (Free Pages
requires a public repo.)

Customise the site title/author/links at the top of `pipeline/build_web.py`
(`SITE_URL`, `REPO_URL`, `AUTHOR`, `DESCRIPTION`), then rebuild.

## Updating the content

See **[`pipeline/PIPELINE.md`](pipeline/PIPELINE.md)**. Either run the generation
prompt in a Claude session and review the result, or let the weekly GitHub
Action open a PR for you to approve. Merging to `main` publishes instantly.

## Disclaimer

Headlines summarise publicly reported pharma and drug-industry developments.
Impact analysis is editorial summary, **not investment advice**.
