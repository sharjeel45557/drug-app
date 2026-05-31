# Weekly generation prompt

Paste the block below into a Claude Code session on the `drug-app` repo each week.

---

You are updating the PharmaPulse pharma-news feed. Find the latest pharma/drug
industry news from Citeline Insights (insights.citeline.com) for the most recent
week and update `docs/feed.json`.

## 1. Target period
Determine today's date and the past week's range (e.g. "May 25 – May 31, 2026").
Note the current month and year for the search queries.

## 2. Search (replace {month}/{year})
- site:insights.citeline.com FDA drug approval {month} {year}
- site:insights.citeline.com pipeline watch phase III {month} {year}
- site:insights.citeline.com biosimilar approval {month} {year}
- site:insights.citeline.com pharma regulatory {month} {year}
- site:insights.citeline.com M&A deals pharma {month} {year}
- site:insights.citeline.com complete response letter CRL {month} {year}
- site:insights.citeline.com clinical trial readout {month} {year}
- site:insights.citeline.com EU drug approval EMA {month} {year}
- site:insights.citeline.com pharma industry outlook {month} {year}

## 3. For each NEW article, produce
- category, catClass, borderClass (use pipeline/feed.schema.json enums + the map in PIPELINE.md)
- headline (clean title)
- details (1–2 sentence summary from the snippet)
- drugs (specific drug names, companies, competing products, markets)
- impact (2–3 sentences: market-share shifts, competitive dynamics, pricing, investor relevance)
- url (must be on insights.citeline.com)
- date ("yyyy-MM-dd")

## 4. Deduplicate
Read existing `docs/feed.json`. Skip any article whose `url` or `headline`
already appears. Keep prior articles unless they age out (optional: drop items
older than ~8 weeks).

## 5. Write `docs/feed.json`
- Merge new + kept articles, newest first.
- Re-number `id` sequentially 1…N (newest = 1).
- Update `weekRange` and `generatedAt`.
- Keep `schemaVersion: 1` and the `source` string.
- Validate it parses: `python3 -m json.tool docs/feed.json > /dev/null`.

## 6. Report
- How many new articles were added.
- The most significant new headlines.
- Any categories with no new content this week.

Then commit and push. Do NOT open a PR unless asked.
