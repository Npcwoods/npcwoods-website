# Agent rules for npcwoods-website

Read the **STOP. Read this first.** banner at the top of `CLAUDE.md` before you edit, preview, match, or deploy anything.

Live site = WordPress on GoDaddy (npcwoods.com). This repo is source. Vercel is preview only.

Credentials: load SFTP/WP from `/Users/macmini/Desktop/Chris-HQ/.env` only (not `/Users/chriswoods/`). Assume that file is current. Never hardcode. Never use chat memory or leftover `vki.0b3` / `client_b58ea8ab6e` examples. Use `scripts/deploy.py` for existing pages. First-time URLs need the mu-plugin route, a WordPress stub, the HTML upload, a WPaaS cache flush, and a **clean-URL** verify (no query string).

Do not tell Chris a URL is live until `https://npcwoods.com/<path>/` (no `?`) returns the real HTML.

Homepage production map is `HOMEPAGE.md` (locked 2026-08-19): live `/` is `page-npcwoods-home.php` forced on Twenty Twenty-Four, not Gutenberg.

Then read `CLAUDE.md`, `HOMEPAGE.md`, `skills/npcwoods-live-page-launch/SKILL.md`, `PRODUCT.md`, and `DESIGN.md`.
