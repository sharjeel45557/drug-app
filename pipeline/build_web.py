#!/usr/bin/env python3
"""Generate docs/index.html (the web preview) from docs/feed.json.

Design goal: the feed must be fully visible with NO JavaScript, so it renders
even inside sandboxed in-app file previews that block inline scripts. All cards
are baked as static HTML using native <details> for expand/collapse. JavaScript
is layered on top purely as progressive enhancement (search + category filter).

Run:  python3 pipeline/build_web.py
"""
import json
import os
import html as _h

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "docs", "feed.json")
OUT = os.path.join(ROOT, "docs", "index.html")

# catClass -> (solid hex, short label, SVG path)
CATS = {
    "cat-approval":  ("#16A34A", "Approvals",   "M9 12l2 2 4-4"),
    "cat-regulatory":("#2563EB", "FDA",         "M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6"),
    "cat-phase3":    ("#7C3AED", "Phase III",   "M9 3v6l-5 9a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-5-9V3"),
    "cat-biosimilar":("#0D9488", "Biosimilars", "M10.5 20.5a5 5 0 0 1-7-7l6-6a5 5 0 0 1 7 7zM8 8l8 8"),
    "cat-crl":       ("#DC2626", "CRLs",        "M12 9v4m0 4h.01M10.3 3.3 2.3 17a2 2 0 0 0 1.7 3h16a2 2 0 0 0 1.7-3L13.7 3.3a2 2 0 0 0-3.4 0z"),
    "cat-deals":     ("#EA580C", "M&A",         "M7 7l5 5 5-5M12 12v8M5 4h14"),
    "cat-outlook":   ("#4F46E5", "Outlook",     "M3 3v18h18M7 14l3-3 3 3 5-6"),
    "cat-eu":        ("#0891B2", "EU/Global",   "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM2 12h20M12 2c3 3 3 17 0 20M12 2c-3 3-3 17 0 20"),
    "default":       ("#64748B", "Other",       "M4 4h16v16H4z"),
}


def meta(cc):
    return CATS.get(cc, CATS["default"])


def tint(hexv, a=0.13):
    h = hexv.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def icon(path, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/></svg>')


def fmt_date(s):
    if not s:
        return ""
    import datetime as dt
    try:
        d = dt.date.fromisoformat(s)
        return d.strftime("%b %-d")
    except ValueError:
        return s


def esc(s):
    return _h.escape(s or "", quote=True)


def card_html(a):
    cc = a.get("catClass", "default")
    color, _, path = meta(cc)
    searchable = esc((a.get("headline", "") + " " + a.get("drugs", "") + " " +
                      a.get("category", "")).lower())
    pill = f'<span class="pill">{icon(path)}{esc(a.get("category",""))}</span>'
    url = a.get("url", "")
    cta = (f'<a class="cta" href="{esc(url)}" target="_blank" rel="noopener">'
           f'Read on Citeline Insights ↗</a>'
           f'<div class="fineprint">Full article may require a Citeline subscription.</div>'
           ) if url else ""
    return f"""<details class="card" data-cat="{cc}" data-text="{searchable}" style="--c:{color};--tint:{tint(color)}">
  <summary>
    <div class="toprow">{pill}<span class="date">{fmt_date(a.get('date'))}</span></div>
    <h2>{esc(a.get('headline',''))}</h2>
    <p class="snippet">{esc(a.get('details',''))}</p>
    <span class="more">Tap for impact analysis ›</span>
  </summary>
  <div class="body">
    <div class="section"><div class="lbl">{icon("M10.5 20.5a5 5 0 0 1-7-7l6-6a5 5 0 0 1 7 7zM8 8l8 8")} Drugs &amp; Markets Affected</div><p>{esc(a.get('drugs',''))}</p></div>
    <div class="section"><div class="lbl">{icon("M3 3v18h18M7 14l3-3 3 3 5-6")} Industry Impact Analysis</div><p>{esc(a.get('impact',''))}</p></div>
    {cta}
  </div>
</details>"""


def chip_html(cc, label, active=False):
    color, _, path = meta(cc) if cc else ("#1E3A8A", "All", "")
    ico = icon(path) if cc else ""
    pressed = "true" if active else "false"
    data = cc or ""
    return (f'<button class="chip" data-cat="{data}" aria-pressed="{pressed}" '
            f'style="--c:{color};--tint:{tint(color)}">{ico}{esc(label)}</button>')


def build():
    feed = json.loads(open(FEED, encoding="utf-8").read())
    arts = sorted(feed.get("articles", []), key=lambda a: a.get("date", ""), reverse=True)

    cards = "\n".join(card_html(a) for a in arts)

    present = []
    for a in arts:
        if a["catClass"] not in present:
            present.append(a["catClass"])
    chips = chip_html(None, "All", active=True) + "".join(
        chip_html(cc, meta(cc)[1]) for cc in present)

    week = esc(feed.get("weekRange", ""))
    import datetime as dt
    try:
        upd = dt.datetime.fromisoformat(feed["generatedAt"].replace("Z", "+00:00"))
        updated = "Updated " + upd.strftime("%b %-d")
    except Exception:
        updated = ""

    html = TEMPLATE
    for k, v in {
        "__COUNT__": str(len(arts)),
        "__WEEK__": ("📅 " + week) if week else "",
        "__UPDATED__": updated,
        "__CHIPS__": chips,
        "__CARDS__": cards,
    }.items():
        html = html.replace(k, v)

    open(OUT, "w", encoding="utf-8").write(html)
    print(f"Wrote {OUT} with {len(arts)} static cards.")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>PharmaPulse</title>
<meta name="theme-color" content="#1E3A8A" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="apple-mobile-web-app-title" content="PharmaPulse" />
<link rel="apple-touch-icon" href="apple-touch-icon.png" />
<link rel="icon" type="image/png" href="icon-192.png" />
<link rel="manifest" href="manifest.webmanifest" />
<style>
  :root{
    --accent:#1E3A8A; --accent2:#2563EB;
    --bg:#f2f3f7; --card:#ffffff; --text:#0f172a; --muted:#64748b; --line:#e5e7eb;
  }
  @media (prefers-color-scheme: dark){
    :root{ --bg:#0b1020; --card:#151b2e; --text:#e7ebf3; --muted:#94a3b8; --line:#26304a; }
  }
  *{ box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
  html,body{ margin:0; }
  body{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
        background:var(--bg); color:var(--text); line-height:1.45; }
  .wrap{ max-width:720px; margin:0 auto; padding:0 14px 48px; }
  header.hero{ background:linear-gradient(135deg,var(--accent),var(--accent2));
    color:#fff; border-radius:0 0 22px 22px; padding:calc(16px + env(safe-area-inset-top)) 18px 20px; }
  .brandrow{ display:flex; align-items:center; gap:8px; font-weight:600; font-size:.92rem; opacity:.95; }
  .kpi{ display:flex; align-items:baseline; gap:8px; margin-top:8px; }
  .kpi b{ font-size:2.6rem; font-weight:800; letter-spacing:-1px; }
  .kpi span{ font-weight:600; opacity:.92; }
  .meta{ margin-top:6px; font-size:.82rem; opacity:.9; display:flex; gap:14px; flex-wrap:wrap; }
  .controls{ position:sticky; top:0; z-index:5; background:var(--bg); padding:12px 0 6px; }
  .search{ display:flex; align-items:center; gap:8px; background:var(--card);
           border:1px solid var(--line); border-radius:12px; padding:10px 12px; }
  .search input{ border:0; outline:0; background:transparent; color:var(--text); font-size:1rem; width:100%; }
  .chips{ display:flex; gap:8px; overflow-x:auto; padding:10px 0 4px; scrollbar-width:none; }
  .chips::-webkit-scrollbar{ display:none; }
  .chip{ flex:0 0 auto; border:0; cursor:pointer; font-size:.82rem; font-weight:600;
         padding:7px 13px; border-radius:999px; display:inline-flex; align-items:center; gap:6px;
         color:var(--c); background:var(--tint); white-space:nowrap; }
  .chip[aria-pressed="true"]{ color:#fff; background:var(--c); }
  .card{ position:relative; background:var(--card); border:1px solid var(--line);
         border-radius:14px; margin-bottom:12px; overflow:hidden; }
  .card::before{ content:""; position:absolute; left:0; top:0; bottom:0; width:5px; background:var(--c); }
  .card[hidden]{ display:none; }
  summary{ list-style:none; cursor:pointer; padding:14px 14px 14px 18px; }
  summary::-webkit-details-marker{ display:none; }
  .toprow{ display:flex; align-items:center; justify-content:space-between; gap:8px; }
  .date{ font-size:.74rem; color:var(--muted); }
  .pill{ display:inline-flex; align-items:center; gap:5px; font-size:.72rem; font-weight:700;
         color:var(--c); background:var(--tint); padding:3px 9px; border-radius:999px; }
  .card h2{ font-size:1.05rem; margin:8px 0 6px; line-height:1.3; }
  .snippet{ margin:0; color:var(--muted); font-size:.92rem; }
  .more{ display:inline-block; margin-top:8px; font-size:.78rem; font-weight:600; color:var(--c); }
  details[open] .more{ display:none; }
  .body{ padding:0 14px 14px 18px; }
  .section{ background:var(--bg); border:1px solid var(--line); border-radius:12px; padding:12px; margin:10px 0; }
  .section .lbl{ font-weight:700; font-size:.8rem; margin-bottom:6px; color:var(--c); display:flex; align-items:center; gap:6px; }
  .section p{ margin:0; font-size:.92rem; }
  .cta{ display:block; text-align:center; text-decoration:none; color:#fff; background:var(--c);
        font-weight:700; padding:13px; border-radius:12px; margin-top:6px; }
  .fineprint{ text-align:center; color:var(--muted); font-size:.72rem; margin-top:8px; }
  .empty{ text-align:center; color:var(--muted); padding:40px 10px; }
  .ico{ width:1em; height:1em; display:inline-block; vertical-align:-2px; flex:0 0 auto; }
</style>
</head>
<body>
<header class="hero">
  <div class="brandrow">
    <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-7 4 14 2-9 1.5 4H21"/></svg>
    Citeline Pharma Intelligence
  </div>
  <div class="kpi"><b>__COUNT__</b><span>stories this week</span></div>
  <div class="meta"><span>__WEEK__</span><span>__UPDATED__</span></div>
</header>

<div class="wrap">
  <div class="controls">
    <div class="search">
      <svg class="ico" style="color:var(--muted)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="q" type="search" placeholder="Search drugs, companies, topics" autocomplete="off" />
    </div>
    <div class="chips" id="chips">__CHIPS__</div>
  </div>

  <div id="feed">
__CARDS__
  </div>
  <div class="empty" id="empty" hidden>No stories match. Try another category or search.</div>
</div>

<script>
/* Progressive enhancement only. With JS blocked, every card above is already
   visible and expandable via native <details>. */
(function(){
  var q = document.getElementById('q');
  var cards = [].slice.call(document.querySelectorAll('.card'));
  var chips = [].slice.call(document.querySelectorAll('.chip'));
  var empty = document.getElementById('empty');
  var activeCat = null;

  function refresh(){
    var term = (q.value || '').toLowerCase().trim();
    var shown = 0;
    cards.forEach(function(c){
      var okCat = !activeCat || c.getAttribute('data-cat') === activeCat;
      var okQ = !term || (c.getAttribute('data-text') || '').indexOf(term) !== -1;
      var show = okCat && okQ;
      c.hidden = !show; if (show) shown++;
    });
    empty.hidden = shown !== 0;
  }

  q.addEventListener('input', refresh);
  chips.forEach(function(b){
    b.addEventListener('click', function(){
      var cat = b.getAttribute('data-cat') || null;
      activeCat = (activeCat === cat) ? null : cat;
      chips.forEach(function(x){ x.setAttribute('aria-pressed', String((x.getAttribute('data-cat')||null) === activeCat)); });
      refresh();
    });
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
