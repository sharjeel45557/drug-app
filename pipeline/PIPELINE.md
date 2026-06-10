# PharmaPulse — Update Runbook

`docs/feed.json` is the single source of truth. Updating the content means
**regenerating that file, rebuilding the page, and pushing** — no code changes.

```
update docs/feed.json → build_web.py renders docs/index.html → commit & push
   → GitHub Pages serves it → visitors see the new briefing
```

There are three ways to update it, in order of how this project runs day to day.

---

## 1. Daily Claude scheduled session (primary)

A scheduled Claude session runs **every day**, checks the source for genuinely
new, significant news, and updates the feed **only when warranted** (most days
there's nothing new — that's expected). When it does update, it rebuilds the page
and pushes straight to `main`, so the site goes live within ~a minute.

**Set it up once:** create a daily schedule (Claude Code on the web) pointed at
the `sharjeel45557/drug-app` repo, and paste the task from
[`generation-prompt.md`](generation-prompt.md) — with `{source}` replaced by your
real source domain. The domain lives only in the schedule config, never in this
repo, which keeps the public repo source-neutral.

The Validate CI runs on every push to `main` as a structural safety net. Because
updates publish unreviewed, the prompt enforces a strict quality bar; spot-check
the live site periodically.

## 2. Manual update (any time)

1. Start a Claude session on the repo and paste the task from
   `generation-prompt.md` (with the real `{source}`).
2. **Review** the draft `docs/feed.json` — headlines, impact analysis, categories.
3. Rebuild & validate:
   ```bash
   python3 pipeline/build_web.py
   python3 -m json.tool docs/feed.json > /dev/null && echo OK
   ```
4. Commit & push to `main`.

## 3. GitHub Actions (company-grade fallback)

`.github/workflows/weekly-feed.yml` regenerates the feed via the Claude API
(server-side web search) and opens a PR for review. Unlike a personal Claude
schedule, this is **account-independent infrastructure your org can own** — a
good option if the company adopts the project.

Activate it with two repo settings (Settings → Secrets and variables → Actions):
- Secret `ANTHROPIC_API_KEY`
- Variable `SOURCE_DOMAIN` (e.g. `news.example.com`)

It stays dormant until those are set.

---

## Rules every update follows

- Only genuinely new, significant articles from the configured source.
- Deduplicate against the existing feed by headline; drop items older than ~8 weeks.
- Newest articles get the lowest `id`s after a full re-number (1…N).
- `catClass` / `borderClass` must come from the enum in `feed.schema.json`.
- No `url` field in the public feed (source links are stripped).
- Always publish to `main` — GitHub Pages serves `main`/`docs`, so the feed only
  goes live once the commit is on `main`. Even when a session works on a
  development/feature branch, merge/fast-forward into `main` and push `main`; a
  feed commit that lands only on a branch is not published.
- Impact analysis is specific and conservative: name drugs, companies,
  competitors, markets — without overstating.

## Category → CSS class map

| Category                                          | catClass        | borderClass        |
|---------------------------------------------------|-----------------|--------------------|
| FDA Drug Approval / Accelerated Approval          | cat-approval    | border-approval    |
| FDA Regulatory                                    | cat-regulatory  | border-regulatory  |
| Phase III / Approvals / Phase III Clinical Trial  | cat-phase3      | border-phase3      |
| Biosimilar / FDA Biosimilar Policy / Generics     | cat-biosimilar  | border-biosimilar  |
| Complete Response Letter                          | cat-crl         | border-crl         |
| M&A / Deals                                       | cat-deals       | border-deals       |
| Industry Outlook / Industry R&D / Medtech         | cat-outlook     | border-outlook     |
| EU Regulatory / Global Regulatory                 | cat-eu          | border-eu          |

## Hosting (GitHub Pages — free)

**Settings → Pages → Deploy from a branch → Branch `main`, Folder `/docs`.**
GitHub serves `docs/` at `https://sharjeel45557.github.io/drug-app/`.
Site title / author / links are configured at the top of `pipeline/build_web.py`.
