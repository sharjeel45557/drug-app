# Daily update prompt (for a scheduled Claude session)

This is the task a **scheduled Claude session** runs to keep the feed fresh.
`{source}` is the news-source domain — when you create the schedule, paste this
prompt with `{source}` replaced by the real domain (e.g. `news.example.com`).
Keeping the domain in the schedule config (not in this repo) is what keeps the
public repo source-neutral.

The schedule runs **daily**, but **only publishes when there is genuinely new,
significant news** — most days there will be nothing to add, and that's fine.

---

You are maintaining the PharmaPulse pharma-news feed in this repo. Today, check
`{source}` for genuinely new, significant pharma/drug-industry news and update
the feed **only if warranted**.

## 1. Look for new news
Note today's date. Search `{source}` for items published in roughly the last
7 days that are NOT already in `docs/feed.json`:
- site:{source} FDA drug approval
- site:{source} pipeline watch phase III
- site:{source} biosimilar approval
- site:{source} pharma regulatory
- site:{source} complete response letter CRL
- site:{source} M&A deals pharma
- site:{source} clinical trial readout
- site:{source} EU drug approval EMA
- site:{source} pharma industry outlook

## 2. Quality bar (important)
- Include an item ONLY if it is **clearly new** (not already in the feed by
  headline) AND **significant** (a real approval, CRL, Phase III readout,
  biosimilar, major deal, or material regulatory change). Skip minor/duplicative
  items. **Quality over quantity — adding nothing is an acceptable outcome.**
- Every item must be sourced from `{source}`. Be conservative and accurate;
  do not overstate. This is published, investor-relevant content.

## 3. For each NEW article, produce
- category, catClass, borderClass (use the enums in `pipeline/feed.schema.json`
  and the category map in `pipeline/PIPELINE.md`)
- headline (clean title)
- details (1–2 sentence factual summary)
- drugs (specific drug names, companies, competing products, markets)
- impact (2–3 sentences: market-share shifts, competitive dynamics, pricing,
  investor relevance)
- date ("yyyy-MM-dd")
- (note the source url internally for dedup; it is NOT stored in the public feed)

## 4. Update `docs/feed.json` (only if there are new items)
- Merge new + existing articles; drop anything older than ~8 weeks.
- Sort newest first and re-number `id` 1…N (newest = 1).
- Do NOT include a `url` field (the public feed carries no source links).
- Set `generatedAt` to today; set `weekRange` to the trailing 7-day window
  (e.g. "May 25 – May 31, 2026"). Keep `schemaVersion: 1` and
  `source: "PharmaPulse Weekly Briefing"`.

## 5. Rebuild and publish
- Run `python3 pipeline/build_web.py` to regenerate `docs/index.html`.
- Verify: `python3 -m json.tool docs/feed.json > /dev/null`.
- If (and only if) files changed, commit with a message like
  `feed: add N stories (YYYY-MM-DD)` and **push to `main`**.
- If nothing new was worth adding, make NO commit and stop.

## 6. Report
Briefly state how many items you added (or that there was nothing new) and the
headlines added.
