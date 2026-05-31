#!/usr/bin/env python3
"""Regenerate docs/feed.json from Citeline Insights using the Claude API.

Used by the weekly GitHub Actions workflow. Claude runs the Citeline searches
itself via the server-side web_search tool, classifies each new article, writes
the impact analysis, and returns the complete updated feed as JSON. We then
validate, enforce id ordering, and write the file. The workflow opens a PR so a
human still reviews before it goes live (the chosen "review gate").

Env:
  ANTHROPIC_API_KEY   required
  FEED_MODEL          optional, default 'claude-sonnet-4-6'

Run locally:  ANTHROPIC_API_KEY=... python3 pipeline/generate_feed.py
"""
import datetime as dt
import json
import os
import re
import sys

import anthropic
from jsonschema import validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED_PATH = os.path.join(ROOT, "docs", "feed.json")
SCHEMA_PATH = os.path.join(ROOT, "pipeline", "feed.schema.json")
PROMPT_PATH = os.path.join(ROOT, "pipeline", "generation-prompt.md")

MODEL = os.environ.get("FEED_MODEL", "claude-sonnet-4-6")
MAX_AGE_DAYS = 56  # drop articles older than ~8 weeks


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def extract_json_block(text):
    """Pull the last ```json ... ``` fenced block (or last {...}) from text."""
    fences = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    candidate = fences[-1] if fences else None
    if candidate is None:
        start, end = text.find("{"), text.rfind("}")
        candidate = text[start:end + 1] if start != -1 and end != -1 else None
    if candidate is None:
        raise ValueError("No JSON object found in model response.")
    return json.loads(candidate)


def build_prompt(current_feed, today):
    instructions = read(PROMPT_PATH)
    return (
        f"{instructions}\n\n"
        f"---\nToday's date is {today.isoformat()}.\n"
        f"Drop any article older than {MAX_AGE_DAYS} days unless it's clearly still topical.\n\n"
        f"Here is the CURRENT docs/feed.json to deduplicate against and update:\n\n"
        f"```json\n{json.dumps(current_feed, indent=2)}\n```\n\n"
        f"Return ONLY the complete updated feed.json as a single ```json fenced block."
    )


def normalize(feed, today):
    """Enforce invariants the app relies on, regardless of model output."""
    arts = feed.get("articles", [])
    # newest first by date
    arts.sort(key=lambda a: a.get("date", ""), reverse=True)
    for i, a in enumerate(arts, start=1):
        a["id"] = i
    feed["articles"] = arts
    feed["schemaVersion"] = 1
    feed["generatedAt"] = today.strftime("%Y-%m-%dT00:00:00Z")
    feed.setdefault("source", "Citeline Insights (insights.citeline.com)")
    return feed


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set.")

    today = dt.date.today()
    current = json.loads(read(FEED_PATH))
    schema = json.loads(read(SCHEMA_PATH))

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 12}],
        messages=[{"role": "user", "content": build_prompt(current, today)}],
    )

    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    feed = normalize(extract_json_block(text), today)

    validate(instance=feed, schema=schema)

    # guard: only insights.citeline.com URLs survive
    bad = [a["url"] for a in feed["articles"] if "insights.citeline.com" not in a["url"]]
    if bad:
        sys.exit(f"Non-Citeline URLs found, refusing to write: {bad}")

    with open(FEED_PATH, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)
        f.write("\n")

    new_count = len(feed["articles"]) - len(current.get("articles", []))
    print(f"Wrote {len(feed['articles'])} articles "
          f"({'+' if new_count >= 0 else ''}{new_count} vs previous). "
          f"Week: {feed.get('weekRange', '?')}")


if __name__ == "__main__":
    main()
