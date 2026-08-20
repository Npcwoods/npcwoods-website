# Homepage source of truth

Verified 2026-08-19 evening. **Docs only.** Do not deploy from this file. Do not edit live WordPress.

Live `/` is **not** the git PHP file and is **not** on the city/blog static-HTML flow.

## What is live

| Fact | Value |
|---|---|
| Production | WordPress on GoDaddy: https://npcwoods.com/ |
| Page | WordPress page ID **63** |
| Theme in body class | `wp-theme-twentytwentyfour` |
| Live body class includes | `home page-template-page-npcwoods-home page-template-page-npcwoods-home-php page-id-63 wp-theme-twentytwentyfour` |
| Live H1 | `Same-Day Telemedicine — $59, No Appointment` |
| Where that H1 lives | Gutenberg / page-63 content |

Live head is Twenty Twenty-Four / core `wp_head`. The block header is `wp-block-template-part`.

## Files that are not live

Do not upload or edit these as if they were `/`:

- **`homepage/page-npcwoods-home.php` in git** — H1 is `$59 text-based telemedicine.` That string is **not** what is live. Do not deploy this file as the homepage.
- **`wp-content/themes/twentytwentyfour/page-npcwoods-home.php`** — **does not exist** on the server.
- **`wp-content/themes/flavor/page-npcwoods-home.php`** — exists on the server and is the **wrong** file. Edits do not appear on the clean URL.

## CSS (separate track)

After a 2026-08-19 mu-plugin 500 + WPaaS flush, stylesheet tags disappeared (`0` `rel=stylesheet`, no `site.css`, no `global-styles`). CSS restore is in progress separately. Missing CSS is not a reason to upload homepage PHP.

## Homepage is not the city/blog flow

City and blog pages use: `landing-pages/.../index.html` + mu-plugin route + WP page stub + `scripts/deploy.py`.

The homepage is **not** on that flow yet. `deploy.py` does not ship `/`.

## mu-plugin on page 63

`php/npcwoods-faq-schema.php` has an output-buffer guardrail on page 63 (string replace only). Edit or replace that original filename only.

## Locked rules

1. **Never upload a second mu-plugin like `*.PATCHED.php`.** Edit or replace the original filename only. Two files with the same functions = sitewide 500.
2. **After any mu-plugin change**, verify uncached `https://npcwoods.com/?n=1` **and** `/wp-admin/` are 200 before the next upload.
3. **Do not edit homepage PHP, flavor templates, or TT4 `functions.php`** when shipping city or blog pages unless Chris explicitly says to change the homepage.
4. **Git `homepage/page-npcwoods-home.php` is not the live homepage.** Do not deploy it as if it were.
5. **Chris approves homepage changes from hero / middle / footer screenshots**, not from a PR.

## Planned next (not this PR)

Convert the homepage to the same static HTML flow as Phoenix UTI: first-screen mock with mobile photo fix, screenshot approve, then live. Do not start that work from this doc.
