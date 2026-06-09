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
1. Upload static HTML via SFTP (paramiko) to `html/{path}/index.html`.
2. Ensure routing exists in the corresponding mu-plugin PHP file.
3. Touch/update the matching WordPress page stub ID via the REST API to flush GoDaddy Varnish cache.
4. Run Playwright pixel/event verification on the live URL to prove `tracking.js` fires.
