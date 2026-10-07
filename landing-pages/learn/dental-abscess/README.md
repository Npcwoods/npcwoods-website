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

Generic words are allowed: `antibiotic`, `medicine`, `prescription` as a possibility, never a product list.

## Clinical honesty (do not soften)

Many abscesses need a dentist or the ER. Text care fits some stable, local cases only. A consult does not guarantee a prescription. Helper medicine is a bridge. The dentist still fixes the source.

License wording: **13 states, including Florida by telehealth registration**. Never Florida-licensed.
