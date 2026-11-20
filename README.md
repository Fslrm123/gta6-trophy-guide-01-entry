# Leonida Legend — GTA VI Trophy Guide

[![make.fun](https://make.fun/badge/gta6-trophy-guide-01.svg)](https://make.fun/bounty/gta6-trophy-guide-01)
[![rank](https://make.fun/badge/gta6-trophy-guide-01/Fslrm123/gta6-trophy-guide-01-entry/rank.svg)](https://make.fun/bounty/gta6-trophy-guide-01)
[![reward](https://make.fun/badge/gta6-trophy-guide-01/Fslrm123/gta6-trophy-guide-01-entry/reward.svg)](https://make.fun/bounty/gta6-trophy-guide-01)

An offline guide and tracker for all **55 Grand Theft Auto VI trophies** (PlayStation 5).
Every trophy carries a full authored guide — what to do, where and when to do it, practical
tips, a missable note, a difficulty rating (1–5) and a time estimate — plus a “Your road to
Platinum” roadmap, live progress ring and per-grade stat cards, search across names,
descriptions and guides, grade filters, hide-earned toggle and four sort modes. Your ticks
are saved on your device; the app makes zero network requests.

Built for the make.fun bounty
[gta6-trophy-guide-01](https://make.fun/bounty/gta6-trophy-guide-01).
New to make.fun? Join with the referral link: https://make.fun/r/3v2j7j85

## How to run

Serve the app locally (Node 22, standard library only — no install, no build step):

```sh
node serve.ts
```

Then open http://localhost:8080.

Or run the entry program, which copies `app/` and `screenshots/` to the output directory
and writes the make.fun `dossier.json`:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## What's inside

- `app/` — the static frontend: `index.html`, `app.js`, `style.css`, `data/trophies.json`
  (the official 55 trophies with authored guides).
- `main.ts` — the program/v1 entry: copies the app and screenshots to the output and
  writes `dossier.json` via the vendored make.fun library.
- `enrich_guides.py` — regenerates `app/data/trophies.json` from the official starter
  list, attaching the authored guide, tips, missable note, difficulty and time estimate
  for every trophy.
- `screenshots/` — 1280×480 captures of the checklist, a trophy detail modal, the silver
  grade filter and a search.

Keyboard: `/` focuses search, `e` toggles hide-earned, `Esc` closes the detail view.
Progress persists in `localStorage` on the device only — nothing is uploaded, ever.
