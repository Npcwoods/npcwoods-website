# Screening Labs Explained (kitchen series)

Kitchen food only. **Nothing here is live** until Chris says "push it live". A GitHub save is not the dining room.
Cooked 2026-11-24 from the dental-abscess layout, using the generic builder `scripts/build-condition-series.py`.

## URLs (not live until plated)

- Hub: `https://npcwoods.com/learn/screening-labs/`
- Offer one-pager: `https://npcwoods.com/screening-labs/`
- Stops:
  - `/learn/screening-labs/metabolic-panel/`
  - `/learn/screening-labs/cholesterol/`
  - `/learn/screening-labs/a1c/`
  - `/learn/screening-labs/thyroid/`
  - `/learn/screening-labs/cbc/`
  - `/learn/screening-labs/who-and-how-often/`
  - `/learn/screening-labs/reading-results/`

## How to edit

The copy lives in `content.json`, the metadata in `series.json`, and the pictures in `art.json` plus `assets/`. The look is in `_shared/series.css` (accent blue #0369A1) and `_shared/art.css`.
The box-side source scripts that generated the JSON and SVG files are saved in `scripts/condition-series-gen/`. Edit the JSON directly from here on.

Rebuild:

```bash
python3 scripts/build-condition-series-og.py screening-labs --cutout assets/img/people/chris-cutout-900.webp   # share cards (only if titles change)
python3 scripts/build-condition-series.py screening-labs
python3 tests/test_condition_series.py
```

Do not hand-edit the generated `index.html` files.

## Rules baked in

$59 flat, pay only if text care fits. License line "14 states, including Florida by telehealth registration (TPAN3355)". No medication or class names (the test greps them), no banned words, no trackers, a 911 line on every page. Hero is Chris's real cutout (`/assets/img/people/chris-cutout-*.webp`, unaltered). Each page has its own 1200x630 card in `assets/og/`.

## Open questions for Chris (do not push until answered)

- How lab orders work today: which lab(s) patients use, how the order gets to them, and which states.
- Lab fees: the page says the lab charges its own fee, separate from the $59. Confirm, and whether you want a price range shown.
- Is reviewing the results by text included in the $59, or a new visit?
- Can you see labs another clinic ordered (the page says yes, by text)?

## Push live later (Chris says "push it live" first)

First-time URLs: `deploy.py` does not create routes or WordPress stubs.

1. Add path routes for the hub + stops in `php/npcwoods-education-pages.php` and the offer page route (same pattern as dental). One copy of each mu-plugin only.
2. Create WP stubs: child `screening-labs` under `learn`, grandchildren for each stop, and root page `screening-labs`.
3. Upload `assets/` (SVGs + og JPGs) alongside the HTML; `deploy.py` uploads `index.html` only.
4. Dry-run, then live with Chris's yes:

```bash
python3 scripts/deploy.py --pages \
  learn/screening-labs \
  learn/screening-labs/metabolic-panel \
  learn/screening-labs/cholesterol \
  learn/screening-labs/a1c \
  learn/screening-labs/thyroid \
  learn/screening-labs/cbc \
  learn/screening-labs/who-and-how-often \
  learn/screening-labs/reading-results \
  screening-labs
```

5. Purge cache, run the pre-flight on every clean URL (0 FAIL), FB Sharing Debugger re-scrape, then add the learn hub card, `/sitemap/`, `/conditions/`, and `llms.txt` lines in the same batch.
