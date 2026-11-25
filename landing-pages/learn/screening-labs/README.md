# Screening Labs Explained (kitchen series)

Kitchen food only. **Nothing here is live** until Chris says "push it live". A GitHub save is not the dining room.
Cooked 2026-11-24. Rebuilt the same day on the **gold look** (Chris: "do these match our UTI lander as the gold standard?"): the offer page uses the live UTI lander's chassis (`landing-pages/uti-treatment/index.html`) and the series uses the UTI Explained look (`landing-pages/learn/uti/`). Builder: `scripts/build-condition-series-gold.py`.

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

The copy lives in `content.json`, the metadata in `series.json`, and the pictures in `art.json` plus `assets/`. The look is read straight from the gold UTI pages at build time (one look, no copy that drifts). Gold-chassis copy (hero, pricing block, comparison rows, road-map blurbs, short-version bullets) lives in `gold.json`.
The box-side source scripts that generated the JSON and SVG files are saved in `scripts/condition-series-gen/`. Edit the JSON directly from here on.

Rebuild:

```bash
python3 scripts/build-condition-series-og.py screening-labs --cutout assets/img/people/chris-cutout-900.webp   # share cards (only if titles change)
python3 scripts/build-condition-series-gold.py screening-labs
python3 -m unittest discover -s tests -p test_condition_series.py
```

Do not hand-edit the generated `index.html` files.

## Rules baked in

$59 covers the consultation and the lab order, with the results walk-through by text included. The lab bills its own fee. A prescription, if needed, is a separate fee. If labs by text are not the right fit, no charge. License line "14 states, including Florida by telehealth registration (TPAN3355)". No medication or class names (the test greps them), no banned words, no trackers, a 911 line on every page. Hero is Chris's real cutout (`/assets/img/people/chris-cutout-*.webp`, unaltered). Each page has its own 1200x630 card in `assets/og/`.

## Answered by Chris (2026-11-24)

- Lab-order process and the generic wording: fine as written.
- Lab fees: separate, set by the lab. Make it obvious the $59 is for the consultation and lab order. Done on the offer page, FAQs, hub, and share copy.
- Results review by text: included in the $59. A prescription, if needed, is a separate fee.

## Still open (not asked yet)

- Can you see labs another clinic ordered? The offer fit list still says "Already have results and want them explained."

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
