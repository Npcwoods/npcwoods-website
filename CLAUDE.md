# CLAUDE.md — Website Department

> This file contains code structure, page stubs, and deployment workflows for NPCWoods.com.

## Key Page IDs & Routing
- Homepage: Page ID `63` (Template: `page-npcwoods-home.php`)
- Experience: Page ID `310` | Blog: Page ID `413` | GA: Page ID `252` | NC: Page ID `253`
- WordPress REST API Auth: `curl -u "$WP_USERNAME:$WP_APP_PASSWORD"`
- Blog posts: Set status to `draft` via `POST /wp-json/wp/v2/posts`. Closing comments and pingbacks is mandatory.

## Static HTML Routing (mu-plugins)
Marketing surfaces run as static HTML bypassed via mu-plugins:
- `npcwoods-static-pages.php`: 9 state pages + conditions + sitemap
- `npcwoods-education-pages.php`: `/learn/*` (14 conditions) + `/medications/*` (21 drugs)
- `npcwoods-dental-pages.php` / `npcwoods-pharmacy-pages.php`: Dental and pharmacy page overrides

## Shared Components
All static landing pages must include:
- Header: `html/shared/header-snippet.html` (Paste right after `<body>`)
- Footer: `html/shared/footer-snippet.html` (Paste before `</body>`)

## Vercel Review lane (Previews)
- **Do not deploy the root directly.** Build a sanitized preview bundle first:
  ```bash
  python3 scripts/build-vercel-preview-site.py --page [name]
  vercel deploy content-output/previews/vercel-review-site -y --no-wait
  ```
- Public Review URL fallback: `https://vercel-review-site.vercel.app/`

## GoDaddy Production Deployment
**Use `scripts/deploy.py` — do NOT write new dated one-off deploy scripts.** It handles the whole pipeline (remote backup → SFTP upload → WP stub touch/cache flush → live tracking verification). See `scripts/README-deploy.md`.
```bash
python3 scripts/deploy.py --pages uti-treatment/mesa-az/search-safe          # dry-run (default, safe)
python3 scripts/deploy.py --pages <path> --live                              # deploys; asks for Chris's confirmation phrase
python3 scripts/deploy.py --pages <path> --verify-only                       # live tracking check only
```
Not covered by deploy.py (do manually): first-time page launches (mu-plugin routing + WP stub creation), non-page assets (`tracking.js`, mu-plugins, `llms.txt`), IndexNow ping, sitemap exclusions.

## Search-Safe City Pages (template system)
The 8 `uti-treatment/<city>/search-safe/` pages are generated from one template. **Never hand-edit the 8 pages** — edit `landing-pages/uti-treatment/_search-safe-template/template.html` (design) or `cities.json` (per-city data), then run `python3 scripts/build-search-safe-pages.py`. New city = one cities.json entry. See the README in that folder. Verify: `python3 -m unittest tests.test_search_safe_template`.

## Site Guardian (nightly compliance sweep)
`python3 tests/guardian/guardian.py` — read-only sweep of all ~95 live pages: tracking.js/GTM present, zero Meta pixel on health pages, canonical claim wording, forbidden words, noindex on paid LPs, broken links. Report: `content-output/guardian-reports/latest.md`. Refresh page list with `tests/guardian/build_manifest.py` after adding pages. Schedule install (needs Chris's yes): `zsh tests/guardian/install.sh`. Run with `~/Desktop/Chris-HQ/gads-env/bin/python` for Playwright spot-checks (system python lacks playwright).
