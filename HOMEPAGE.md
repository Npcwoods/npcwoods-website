# Homepage — locked production map (2026-09-07)

**Docs only.** This file is the locked map for live `/`. Do not invent extras. Do not change live-site PHP, deploy scripts, or page HTML from this document.

Live `/` is the custom PHP plate `page-npcwoods-home.php`, forced onto Twenty Twenty-Four. It is not a Gutenberg page. If the dining room shows `wp-site-blocks` and a blue underlined nav list, the forcer died — read the 500 steps below. Do not ignore this file.

## Credentials

Load SFTP/WP from `/Users/macmini/Desktop/Chris-HQ/.env` only. Never hardcode. Never use chat memory. Never use skills that still say `vki.0b3` or `client_b58ea8ab6e`.

- Path is `/Users/macmini/Desktop/Chris-HQ/` (not `/Users/chriswoods/`).
- GoDaddy SFTP reset changes USERNAME and password. Re-read `.env`. If SFTP fails once, stop and ask Chris — don't brute-force.
- SSH/SFTP host: `1085255.us30.ssh.myftpupload.com` port 22. Not the HTTPS ftp host.

Do not put passwords in this file, in chat, or in skills.

## mu-plugins

WordPress loads **every** `.php` in `html/wp-content/mu-plugins/`.

- NEVER two PHP files with the same functions.
- NEVER upload `copy 1.php`, `.PATCHED.php`, or a second copy of a plugin.
- Backups = `.bak` only (not `.php`). Rename, don't duplicate.
- Do not use WP File Manager to edit PHP. It creates `filename copy 1.php` and takes the site down. wp-admin File Manager is also down during that 500 — use SFTP.
- Keep `npcwoods-faq-schema.php` (the ~24KB original). Do not edit it unless Chris says so.

## Homepage

The cause of the "unstyled"/default WP look was **not** missing CSS. Active theme is Twenty Twenty-Four (block theme). It ignores PHP templates unless forced.

Real homepage is `page-npcwoods-home.php`. It MUST exist at:

```
html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php
```

Also keep a copy under `themes/flavor/`.

Force it with mu-plugin `npcwoods-force-php-templates.php` (already live). Do not delete it. Do not add a second copy of it.

- Do NOT enqueue `wp-block-library` or `twentytwentyfour/style.css` on the homepage. They unstyle the custom template. `site.css` (shared nav/footer) is OK.
- Theme updates can delete custom PHP from `twentytwentyfour`. After any WP/theme update, verify the homepage file is still there.

### Done check

Patients hit the ordinary address. That is the done check:

- `https://npcwoods.com/` (no `?`) is 200
- Title is `NPCWoods Telemedicine: $59 Text-Based Urgent Care`
- H1 is `You feel awful.` (scroll plate live 2026-09-07)
- HTML contains `npc-redesign` and Chris's hero
- HTML is **not** `wp-site-blocks` with a blue underlined nav list
- `/wp-admin/` should be the login page (200), not "WordPress Error"

`?n=1` is diagnosis only. If the clean URL is Gutenberg/empty and `?n=1` is the real homepage, flush cache. Do not tell Chris `/` is live until the clean URL matches.

## Deploy

- Dry-run first. Nothing live without Chris's yes — except restoring a down homepage/login, which is an emergency.
- Don't touch homepage CSS or mu-plugins "while you're in there."
- Verify the clean URL (`https://npcwoods.com/`, no `?`). `?n=1` is diagnosis only. City pages can look fine from a cache-bust while PHP is dead.

## If the site is 500

1. Do not upload another PHP file.
2. SFTP list mu-plugins. Delete only `*copy*.php` and `*PATCHED.php`. Keep the original.
3. Confirm homepage template still exists in `twentytwentyfour`.
4. Confirm the clean URL `https://npcwoods.com/` is real homepage HTML and `/wp-admin/` is login. Then STOP. Use `?n=1` only to see whether the file is on disk while cache is lying.
