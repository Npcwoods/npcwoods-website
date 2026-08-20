# Homepage — locked production map (2026-08-19)

**Docs only.** This file is the locked map for live `/`. Do not invent extras. Do not change live-site PHP, deploy scripts, or page HTML from this document.

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

- `https://npcwoods.com/?n=1` is 200
- Title is `NPCWoods Telemedicine: $59 Text-Based Urgent Care`
- HTML contains `npc-redesign` and Chris's hero
- HTML is **not** `wp-site-blocks` with a blue underlined nav list
- `/wp-admin/` should be the login page (200), not "WordPress Error"

## Deploy

- Dry-run first. Nothing live without Chris's yes — except restoring a down homepage/login, which is an emergency.
- Don't touch homepage CSS or mu-plugins "while you're in there."
- Verify with a cache buster (`?n=1`). City pages can look fine from cache while PHP is dead.

## If the site is 500

1. Do not upload another PHP file.
2. SFTP list mu-plugins. Delete only `*copy*.php` and `*PATCHED.php`. Keep the original.
3. Confirm homepage template still exists in `twentytwentyfour`.
4. Confirm `?n=1` is real homepage HTML and `/wp-admin/` is login. Then STOP.
