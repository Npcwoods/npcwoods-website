---
name: npcwoods-live-page-launch
description: Use when publishing a new npcwoods.com URL, when a live page looks empty, or when git and the clean URL disagree. Covers first-time WordPress/GoDaddy launches and cache verification.
---

# NPCWoods live page launch

Live site is WordPress on GoDaddy (`https://npcwoods.com`). GitHub is source. Vercel is preview only. Nothing goes live without Chris’s explicit yes (the phrase `CHRIS APPROVED LIVE DEPLOY` for a named URL). Homepage is a different system — read `HOMEPAGE.md` before touching `/`.

## Credentials

Read Chris-HQ `.env` on the Mac. Assume it is current (`SFTP_HOST`, `SFTP_PORT=22`, `SFTP_USERNAME` or `SFTP_USER`, `SFTP_PASSWORD`, `WP_USERNAME`, `WP_APP_PASSWORD`). Never print secrets. Never paste them in chat.

## A live URL needs three pieces

1. HTML in git, usually `landing-pages/<path>/index.html`
2. The same file on GoDaddy at `html/<path>/index.html`
3. A WordPress page stub **and** an mu-plugin route, or nginx 404s before PHP runs

`scripts/deploy.py` uploads HTML and flushes known stubs. It does **not** create first-time routes or stubs.

## First-time launch order

1. Confirm the exact URL Chris approved. Ship that URL only.
2. Put the HTML in git if it is not already there.
3. Add the mu-plugin route (match the existing condition plugin; dental originally mapped only `dental-pain`).
4. Create the WP child stub (parent + slug) so nginx does not 404.
5. Upload HTML with `deploy.py` once the route exists, or SFTP to `html/<path>/index.html`.
6. Flush GoDaddy WPaaS cache (Quick Links → Flush Cache).
7. Verify the **clean URL with no query string**.

## The cache lie (non-negotiable)

A `?v=anything` can show the real HTML while `https://npcwoods.com/<path>/` still serves a ~15KB empty WordPress shell (no title, no H1).

Done means a no-query-string GET returns HTTP 200, real page weight (city templates ~60KB+, not ~15KB), and the locked `<title>` and `<h1>`.

If the clean URL is a shell and a cache-bust is real: flush WPaaS cache and re-check the clean URL. Do not tell Chris it is live until the clean URL matches.

## Do not link empty shells

Many city × condition URLs are empty WP stubs. Fetch first. If there is no title/H1 or the body is ~15KB, do not put it on `/sitemap/`, `/conditions/`, or state hubs.

## Scope locks

- One approved URL is not a general deploy.
- Do not touch `/pay`, gclid, or tracking unless Chris reopens that hop.
- No doctor / physician / MD / insurance language.
- No generated likeness of Chris. Real photo only.
- No patient data anywhere in the launch.

## Aftercare

Report the clean URL, byte size, and H1. Stop.
