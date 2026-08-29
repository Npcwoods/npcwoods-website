# Live HTML inventory — 2026-08-29

Read-only crawl of the dining room (`https://npcwoods.com`). Nothing was uploaded. Nothing was pushed live.

This kitchen does not have the Mini `.env`, so there was no SFTP listing of GoDaddy disk. The crawl used public URLs only: Yoast sitemaps, the WordPress pages API, and a clean-URL GET of each candidate (no query string).

## What we already had

The freezer already held **161** HTML/PHP paths (landing pages, shared snippets, homepage template, blog HTML). Guardian’s 116 live marketing URLs were already mapped.

WordPress currently publishes **207** pages. Yoast’s public page sitemap lists **125**. The gap is leftover city × condition URLs, plus a few legal/content plates that were never copied into git.

WordPress also has **40** blog posts. Those stay in WordPress. They are not static HTML plates.

## Pulled into `landing-pages/` (9 unique plates)

These were dining-room-only. They have a real title and H1. They are not empty shells. They are not copies of a page we already had under another URL.

| Live URL | Bytes | What it is |
|---|---:|---|
| https://npcwoods.com/terms-of-service/ | 9,614 | Legal plate. Linked from the shared footer. |
| https://npcwoods.com/privacy-policy/ | 7,864 | Legal plate. Linked from the shared footer. Noindexed in Yoast. |
| https://npcwoods.com/medical-disclaimer/ | 7,092 | Legal plate. Linked from the shared footer. |
| https://npcwoods.com/services/ | 59,436 | Full custom services plate. In the public sitemap. |
| https://npcwoods.com/urgent-care-price-guide/ | 26,847 | Price-guide article plate. |
| https://npcwoods.com/when-to-see-provider-for-uti/ | 17,311 | UTI education plate. |
| https://npcwoods.com/conditions/poison-ivy-treatment/ | 37,293 | Condition leftover plate (separate from `/poison-ivy/`). In the sitemap. |
| https://npcwoods.com/conditions/nausea-vomiting-treatment/ | 34,365 | Condition leftover plate. In the sitemap. |
| https://npcwoods.com/conditions/albuterol-inhaler-refill-preview/ | 29,514 | Preview leftover. Slug still says preview. |

GitHub save is not live. These files are freezer copies. The dining room still plates them from WordPress leftover PHP until Chris says to push a named URL live.

Do not add these to `/sitemap/`, `/conditions/`, or a state hub until the clean URL is verified as the real plate you want people to see.

## Archived leftover city × condition plates (55)

Not empty shells. They have a title and H1. They are leftover WordPress city pages plated by `npcwoods-wp-singular-plates.php` (~7–10 KB), not the ~60 KB city templates.

They live at `_archive/live-leftover-city-plates-2026-08-29/`. That shelf is a snapshot so the freezer has the current dining-room HTML. It is **not** first-class kitchen food.

- Do not link them from `/sitemap/`, `/conditions/`, or state hubs.
- Do not deploy them with `deploy.py`.
- Do not hand-edit them as if they were the 8 search-safe city pages.
- Several still have a Meta pixel and the word “insurance.” That is what the dining room is serving today. This inventory did not rewrite them.

Cities in this leftover set: Athens, Augusta, Columbus, Savannah, Durham, Greensboro, Raleigh, Wilmington, Chandler, Gilbert, Glendale, Mesa, Peoria, Phoenix, Scottsdale, Surprise, Tempe, Tucson.

Conditions: ED, sinus, strep/ear leftover slug, and a few UTI cities that never got a full template.

## Not copied (redirects — we already have the destination)

These old slugs 301 to a plate already in the freezer. Copying them would have saved the destination HTML under the old name.

| Old URL | Already in the freezer as |
|---|---|
| `/albuquerque-uti-treatment/` | `/uti-treatment/albuquerque-nm/` |
| `/mesa-uti-treatment/` | `/uti-treatment/mesa-az/` |
| `/scottsdale-uti-treatment/` | `/uti-treatment/scottsdale-az/` |
| `/home/phoenix-telemedicine/` | `/arizona-telemedicine/` |
| `/tucson-telemedicine/` | `/arizona-telemedicine/` |
| `/pharmacy-info/` | `/pharmacy/` |
| `/strep-throat-ear-infection/` | `/strep-throat-treatment/` |
| `/states/` | `/` |

## Not copied (wrong plate)

These leftover URLs stay on the requested path, but the HTML they serve is the Atlanta or Charlotte **UTI** city page (canonical points at `/uti-treatment/atlanta-ga/` or `/uti-treatment/charlotte-nc/`). That is a dining-room routing bug, not a missing freezer file.

- `/ed-treatment/atlanta-ga/`
- `/ed-treatment/charlotte-nc/`
- `/sinus-infection-treatment/atlanta-ga/`
- `/sinus-infection-treatment/charlotte-nc/`
- `/strep-throat-ear-infection/atlanta-ga/`
- `/strep-throat-ear-infection/charlotte-nc/`

## What this could not see

Files that exist only on GoDaddy disk and are not a public WordPress page or sitemap URL. That needs SFTP from `/Users/macmini/Desktop/Chris-HQ/.env` on the Mini.

## How to run this again

```bash
python3 scripts/server-sync/inventory-live-html.py
```

Default is inventory only. `--pull` copies only unique first-class plates into `landing-pages/`. It will not dump leftover city stubs or redirect copies there.
