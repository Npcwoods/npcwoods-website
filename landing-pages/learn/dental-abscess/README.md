# Dental Abscess Explained (kitchen series)

Kitchen food only. **Nothing here is live** until Chris says push it live and uses `CHRIS APPROVED LIVE DEPLOY`. A GitHub save is not the dining room.

This is the first hub-and-stop SEO mini-series in this repo. There was no UTI or GLP-1 `series.json` yet. The pattern follows existing `/learn/` education HTML, homepage brand colors, and path-based dental mu-plugin routing.

## URLs (not live until plated)

- Hub: `https://npcwoods.com/learn/dental-abscess/`
- Offer one-pager (ads land here): `https://npcwoods.com/dental-abscess-treatment/`
- Stops:
  - `/learn/dental-abscess/how-it-starts/`
  - `/learn/dental-abscess/what-it-feels-like/`
  - `/learn/dental-abscess/tooth-vs-gum/`
  - `/learn/dental-abscess/lookalikes/`
  - `/learn/dental-abscess/red-flags/`
  - `/learn/dental-abscess/what-care-looks-like/`
  - `/learn/dental-abscess/dentist-vs-text/`
  - `/learn/dental-abscess/why-it-comes-back/`
  - `/learn/dental-abscess/myths/`

## How to edit

1. Change copy in `content.json` or metadata in `series.json`.
2. Change look in `_shared/series.css`.
3. Rebuild:

```bash
python3 scripts/build-dental-abscess-series.py
```

4. Run the checklist:

```bash
python3 -m unittest tests.test_dental_abscess_series
```

Do not hand-edit the generated `index.html` files. They will be overwritten.

Accent is one red only: `{ "name": "red", "hex": "#B42318" }` (homepage safety red). The rest of the page uses homepage cream, ink, and blue.

Background matches the GLP-1 series per page type (body classes set by the build): `series-hub` copies `/learn/glp1/` (vertical night → neon blue → cream → white body gradient, white cards behind all text), `series-stop` copies the GLP-1 stops (dark neon-glow hero band, white page), `series-offer` copies `/glp1-weight-loss/` (blue hero band, white page).

## How to push live later (Chris yes required)

First-time URLs. `deploy.py` will not create routes or WordPress stubs.

1. Dry-run HTML only after stubs exist:

```bash
python3 scripts/deploy.py --pages \
  learn/dental-abscess \
  learn/dental-abscess/how-it-starts \
  learn/dental-abscess/what-it-feels-like \
  learn/dental-abscess/tooth-vs-gum \
  learn/dental-abscess/lookalikes \
  learn/dental-abscess/red-flags \
  learn/dental-abscess/what-care-looks-like \
  learn/dental-abscess/dentist-vs-text \
  learn/dental-abscess/why-it-comes-back \
  learn/dental-abscess/myths \
  dental-abscess-treatment \
  learn
```

2. Upload mu-plugins from `php/npcwoods-education-pages.php` and `php/npcwoods-dental-pages.php` (path maps). Do not upload a second copy of either file.
3. Create WordPress child stubs so nginx does not 404:
   - Parent `/learn/` already exists.
   - Child `dental-abscess` under `learn`.
   - Grandchildren: `how-it-starts`, `what-it-feels-like`, `tooth-vs-gum`, `lookalikes`, `red-flags`, `what-care-looks-like`, `dentist-vs-text`, `why-it-comes-back`, `myths`.
   - Sibling page `dental-abscess-treatment` at the root.
4. Live deploy only with Chris's explicit yes and `CHRIS APPROVED LIVE DEPLOY`.
5. Flush GoDaddy WPaaS cache.
6. Verify each **clean URL with no query string**. Done means 200, real HTML weight, locked title and H1.

Do not add these URLs to the live `/sitemap/` or `/conditions/` plates until the clean URLs are real. The learn hub card in `landing-pages/learn/index.html` should ship in the same live batch as the series.

`llms.txt` / `llms-full.txt` already name the new URLs in kitchen. Those files are not live until they are uploaded.

## Medication-name grep checklist

Run against the series HTML, JSON, and CSS only. Shared header/footer may say "No appointment." That is existing site chrome, not a drug name.

```bash
python3 -m unittest tests.test_dental_abscess_series
```

That test greps HTML, JSON, and CSS for common brand and generic names. Do not paste those names into series copy, comments, alt text, schema, or bubbles.

Must also stay clean of:

- `Florida-licensed` / `Florida licensed`
- Google / Meta / Ahrefs tags (`googletagmanager`, `google-analytics`, `googleadservices`, `connect.facebook.net`, `facebook.com/tr`, `analytics.ahrefs`, `/tracking.js`)
- Patient-facing "no tracking" notes
- Guaranteed results, before/after dental promises

Generic words are allowed: `medicine`, `prescription` as a possibility, never a product list. The class word `antibiotic` / `antibiotics` is banned in this series (PMax safety). Keep the real CDC source URL if needed; soften the display title so scanners do not see the class word.

## Clinical honesty (do not soften)

Many abscesses need a dentist or the ER. Text care fits some stable, local cases only. A consult does not guarantee a prescription. Helper medicine is a bridge. The dentist still fixes the source.

License wording: **13 states, including Florida by telehealth registration**. Never Florida-licensed.

## Pictures and hero art (2026-10-08)

- Hero (hub + 9 stops): Chris's real wink + stethoscope cutout, shared with the GLP-1 and UTI series at `/learn/glp1/assets/chris-cutout-{600,900}.webp?v=20261006arms`. Never generate or edit images of Chris.
- Two hero bubbles per page (black with a thin white outline, iMessage blue `#007AFF`), placed off the face. Text lives in `art.json`.
- Ghost graphic: inline, `aria-hidden`, a big tooth outline plus one topic motif per stop (`ghost_svg()` in the build). No text, no numbers.
- Body figures: clean SVGs in `assets/`, drawn by `scripts/build-dental-abscess-art.py`. Placement, alt text, and captions in `art.json` (`after_section` is the 0-based section index).
- Share cards: `assets/og/og-<page>.jpg` (1200x630), rendered by `scripts/build-dental-abscess-og.py`. Also used as `image` in the MedicalWebPage JSON-LD.
- `_shared/art.css` loads on the explainer pages only. The offer page does not use it.
- Deploy note: `scripts/deploy.py` uploads `index.html` only. Upload `assets/` (SVGs + og JPGs) alongside it.

Rebuild order: `build-dental-abscess-art.py` → `build-dental-abscess-og.py` → `build-dental-abscess-series.py` → tests.
