# PharmaPulse 📈💊

A native **SwiftUI iOS app** that delivers weekly pharma & drug-industry
intelligence curated from [Citeline Insights](https://insights.citeline.com),
with impact analysis for each story.

It is built to be loaded onto an iPhone and published to the App Store.

## How it works

```
 Weekly pipeline (you + Claude)            GitHub Pages (free hosting)        iPhone app
 ─────────────────────────────            ───────────────────────────        ──────────
 Citeline searches → classify  ──writes──▶ docs/feed.json  ◀──fetches──  PharmaPulse (SwiftUI)
 → impact analysis → review                                              caches offline, pull-to-refresh
```

Content updates ship by **regenerating `docs/feed.json` and pushing** — no App
Store resubmission needed. The app only changes when the *code* changes.

## Repo layout

| Path | What it is |
|------|------------|
| `PharmaPulse/` | SwiftUI app source (Models, Services, Views, Theme, Assets) |
| `PharmaPulse.xcodeproj` | Xcode project — open and run |
| `PharmaPulse/Resources/seed-feed.json` | bundled fallback feed (offline / first launch) |
| `docs/feed.json` | the live feed the app downloads (served by GitHub Pages) |
| `pipeline/` | weekly update runbook, JSON schema, reusable generation prompt |
| `project.yml` | XcodeGen spec (only for regenerating the project) |

## Run it (on a Mac)

1. Open `PharmaPulse.xcodeproj` in **Xcode 16+**.
2. Select an iPhone simulator (or your device) and press **▶︎ Run**.
3. The app shows the bundled seed feed instantly, then fetches the latest
   `feed.json` from GitHub Pages.

> Set your **Team** under *Signing & Capabilities* to run on a physical device,
> and change the bundle id `com.mpchealthcare.pharmapulse` if needed.

## Enable the live feed (one-time)

In repo **Settings → Pages**: build from branch `main`, folder `/docs`.
The feed is then served at:

```
https://sharjeel45557.github.io/drug-app/feed.json
```

This URL is set in `PharmaPulse/Services/FeedService.swift` (`feedURL`). Update
it if you host elsewhere.

## Update the news (weekly)

See **[`pipeline/PIPELINE.md`](pipeline/PIPELINE.md)**. In short: run the
generation prompt in a Claude Code session, review the draft `docs/feed.json`,
then commit & push.

## Publishing to the App Store (later)

- Add a 1024×1024 app icon to `PharmaPulse/Assets.xcassets/AppIcon.appiconset`.
- Set version/build, archive in Xcode (*Product → Archive*), upload via the
  Organizer to App Store Connect.
- Because content updates come from the remote feed, the app satisfies the
  "ongoing content" expectation (App Store Guideline 4.2).

## Disclaimer

Headlines and links come from Citeline Insights; full articles may require a
subscription. Impact analysis is editorial summary, **not investment advice**.
