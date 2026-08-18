# Agent rules for npcwoods-website

Read the **STOP. Read this first.** banner at the top of `CLAUDE.md` before you edit, preview, match, or deploy anything.

Live site = WordPress on GoDaddy (npcwoods.com). This repo is source. Vercel is preview only.

Credentials live in Chris-HQ `.env`. Assume that file is current. Use `scripts/deploy.py` for existing pages. First-time URLs need the mu-plugin route, a WordPress stub, the HTML upload, a WPaaS cache flush, and a **clean-URL** verify (no query string).

Do not tell Chris a URL is live until `https://npcwoods.com/<path>/` (no `?`) returns the real HTML.

Then read `CLAUDE.md`, `skills/npcwoods-live-page-launch/SKILL.md`, `PRODUCT.md`, and `DESIGN.md`.
