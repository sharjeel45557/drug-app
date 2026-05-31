# PharmaPulse — Weekly Update Runbook (semi-manual + review)

This is how the news in the app gets refreshed. The app reads
`docs/feed.json` from GitHub Pages; updating the app's content means
**regenerating that one file and pushing it** — no App Store resubmission.

```
[You + Claude] → regenerate docs/feed.json → review/edit → commit & push
       → GitHub Pages serves it → iPhone app picks it up on pull-to-refresh
```

## Weekly steps (~10 minutes)

1. **Start a Claude Code session** on the web (https://claude.ai/code) targeting
   the `sharjeel45557/drug-app` repo, branch `claude/pharmapulse-ios-app-IwjCJ`
   (or `main` once merged).

2. **Paste the generation prompt** (see `generation-prompt.md` in this folder).
   Claude will run the Citeline searches, classify each new article, write the
   impact analysis, and produce an updated `docs/feed.json`.

3. **Review the draft.** This is the human gate you chose:
   - Confirm every `url` is on `insights.citeline.com`.
   - Sanity-check headlines and impact analysis against the snippets.
   - Fix any classification you disagree with.
   - Edit `weekRange` and `generatedAt`.

4. **Validate the JSON** (optional but recommended):
   ```bash
   python3 -m json.tool docs/feed.json > /dev/null && echo OK
   # or, with a schema validator:
   # npx ajv-cli validate -s pipeline/feed.schema.json -d docs/feed.json
   ```

5. **Commit & push.** If you develop on the feature branch, merge to `main`
   afterward so GitHub Pages publishes it (see hosting note below).

6. **Refresh the app** on your iPhone (pull down on the feed). New stories appear.

## Rules the generator follows

- Only `insights.citeline.com` articles.
- Deduplicate against the existing `docs/feed.json` by `url` and `headline`.
- Newest articles get the lowest `id`s after a full re-number (1…N).
- `catClass` / `borderClass` must come from the enum in `feed.schema.json`.
- Impact analysis is specific: name drugs, companies, competitors, market size.

## Category → CSS class map

| Category                                              | catClass        | borderClass        |
|-------------------------------------------------------|-----------------|--------------------|
| FDA Drug Approval / Accelerated Approval              | cat-approval    | border-approval    |
| FDA Regulatory                                        | cat-regulatory  | border-regulatory  |
| Phase III / Approvals / Phase III Clinical Trial      | cat-phase3      | border-phase3      |
| Biosimilar / FDA Biosimilar Policy / Generics         | cat-biosimilar  | border-biosimilar  |
| Complete Response Letter                              | cat-crl         | border-crl         |
| M&A / Deals                                           | cat-deals       | border-deals       |
| Industry Outlook / Industry R&D / Medtech             | cat-outlook     | border-outlook     |
| EU Regulatory / Global Regulatory                     | cat-eu          | border-eu          |

## Hosting note (GitHub Pages — free)

The app fetches: `https://sharjeel45557.github.io/drug-app/feed.json`

Enable once, in the repo settings:
**Settings → Pages → Build from a branch → Branch: `main`, Folder: `/docs`.**

GitHub then serves everything in `docs/` at `https://sharjeel45557.github.io/drug-app/`.
If you publish from a different branch/folder, update `feedURL` in
`PharmaPulse/Services/FeedService.swift` to match.

## Automated weekly job (built — keeps your review gate)

`.github/workflows/weekly-feed.yml` runs every **Monday 13:00 UTC** (and on
demand via *Actions → Weekly PharmaPulse feed → Run workflow*). It:

1. runs `pipeline/generate_feed.py`, which calls the **Claude API** with the
   built-in **web_search** tool — Claude does the Citeline searches itself,
   classifies, writes impact analysis, dedupes against the current feed, and
   returns the updated `docs/feed.json`;
2. validates it against `pipeline/feed.schema.json` and enforces ids/ordering
   and the insights.citeline.com-only rule;
3. opens a **pull request** — nothing publishes until *you* review and merge.

### One-time setup to activate it
1. Add the API key: **Settings → Secrets and variables → Actions → New
   repository secret**, name `ANTHROPIC_API_KEY`.
2. **Merge this branch into `main`.** GitHub only runs *scheduled* workflows
   from the default branch, and Pages serves from `main`/`docs`.
3. (Optional) test immediately with *Run workflow*; review the PR it opens.

No web-search API subscription is needed — search is handled server-side by the
Claude API. The semi-manual prompt above still works any time you prefer to
drive it yourself.
