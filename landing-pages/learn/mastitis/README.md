# Mastitis Explained (kitchen series)

Kitchen food only. **Nothing here is live** until Chris says "push it live". A GitHub save is not the dining room.
Cooked 2026-11-24. Rebuilt the same day on the **gold look** (Chris: "do these match our UTI lander as the gold standard?"): the offer page uses the live UTI lander's chassis (`landing-pages/uti-treatment/index.html`) and the series uses the UTI Explained look (`landing-pages/learn/uti/`). Builder: `scripts/build-condition-series-gold.py`.

## URLs (not live until plated)

- Hub: `https://npcwoods.com/learn/mastitis/`
- Offer one-pager: `https://npcwoods.com/mastitis-treatment/`
- Stops:
  - `/learn/mastitis/how-it-starts/`
  - `/learn/mastitis/what-it-feels-like/`
  - `/learn/mastitis/lookalikes/`
  - `/learn/mastitis/comfort-at-home/`
  - `/learn/mastitis/red-flags/`
  - `/learn/mastitis/keep-feeding/`
  - `/learn/mastitis/text-vs-in-person/`

## How to edit

The copy lives in `content.json`, the metadata in `series.json`, and the pictures in `art.json` plus `assets/`. The look is read straight from the gold UTI pages at build time (one look, no copy that drifts). Gold-chassis copy (hero, pricing block, comparison rows, road-map blurbs, short-version bullets) lives in `gold.json`.
The box-side source scripts that generated the JSON and SVG files are saved in `scripts/condition-series-gen/`. Edit the JSON directly from here on.

Rebuild:

```bash
python3 scripts/build-condition-series-og.py mastitis --cutout assets/img/people/chris-cutout-900.webp   # share cards (only if titles change)
python3 scripts/build-condition-series-gold.py mastitis
python3 -m unittest discover -s tests -p test_condition_series.py
```

Do not hand-edit the generated `index.html` files.

## Rules baked in

$59 flat, pay only if text care fits. License line "14 states, including Florida by telehealth registration (TPAN3355)". No medication or class names (the test greps them), no banned words, no trackers, a 911 line on every page. Hero is Chris's real cutout (`/assets/img/people/chris-cutout-*.webp`, unaltered). Each page has its own 1200x630 card in `assets/og/`.

## Answered by Chris (2026-11-24)

- The ER line keeps 103°F as the cutoff.

## Still open (not asked yet)

- Text visits: words only to start (the page says no photo needed). Confirm.
- Fit list says adults who are breastfeeding or pumping, in a state you treat. Anything to add (e.g. weeks postpartum limit)?

## Push live later (Chris says "push it live" first)

First-time URLs: `deploy.py` does not create routes or WordPress stubs.

1. Add path routes for the hub + stops in `php/npcwoods-education-pages.php` and the offer page route (same pattern as dental). One copy of each mu-plugin only.
2. Create WP stubs: child `mastitis` under `learn`, grandchildren for each stop, and root page `mastitis-treatment`.
3. Upload `assets/` (SVGs + og JPGs) alongside the HTML; `deploy.py` uploads `index.html` only.
4. Dry-run, then live with Chris's yes:

```bash
python3 scripts/deploy.py --pages \
  learn/mastitis \
  learn/mastitis/how-it-starts \
  learn/mastitis/what-it-feels-like \
  learn/mastitis/lookalikes \
  learn/mastitis/comfort-at-home \
  learn/mastitis/red-flags \
  learn/mastitis/keep-feeding \
  learn/mastitis/text-vs-in-person \
  mastitis-treatment
```

5. Purge cache, run the pre-flight on every clean URL (0 FAIL), FB Sharing Debugger re-scrape, then add the learn hub card, `/sitemap/`, `/conditions/`, and `llms.txt` lines in the same batch.
