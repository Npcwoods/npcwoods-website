# NPCWoods Website — Code Repo

> This repo contains the code that builds and deploys NPCWoods.com. For full context on who Chris is, goals, brand voice, and current status — see the `npcwoods-business` repo.

---

## What This Repo Is

Website code only: HTML pages, PHP templates, landing pages, and deploy scripts for NPCWoods.com.

## WordPress REST API Access

Credentials are in `.env` (local only, never committed). Don't ask for creds — just read the .env.

```
# Auth: curl -u "$WP_USERNAME:$WP_APP_PASSWORD"
# Read:   GET  https://npcwoods.com/wp-json/wp/v2/pages/{id}
# Create: POST https://npcwoods.com/wp-json/wp/v2/pages
# Update: POST https://npcwoods.com/wp-json/wp/v2/pages/{id}
```

## Key Page IDs

| Page | ID | URL |
|---|---|---|
| Homepage | 63 | https://npcwoods.com |
| Experience page | 310 | https://npcwoods.com/experience/ |
| Georgia landing | 252 | https://npcwoods.com/georgia-telemedicine/ |
| North Carolina landing | 253 | https://npcwoods.com/north-carolina-telemedicine/ |
| AZ affordable | 198 | https://npcwoods.com/affordable-telemedicine-arizona-no-insurance/ |

## Deployment

### Standard pages (WordPress content)
Push content via WordPress REST API. Always draft first, get Chris's approval, then publish.

### Experience page (static HTML bypass)
The experience page bypasses WordPress's block theme (which strips scripts):
1. Upload HTML via SFTP to `/html/experience/page.html` on the server
2. A must-use plugin (`mu-plugins/npcwoods-experience-page.php`) intercepts the URL and serves raw HTML
3. Update WP page 310 via REST API to bust cache

## Folder Structure

```
npcwoods-website/
├── CLAUDE.md          ← You are here
├── html/
│   └── experience/
│       └── index.html ← Experience page source
├── php/               ← PHP templates (future)
├── landing-pages/     ← GA, NC, AZ city pages (future)
└── scripts/           ← Deploy helpers (future)
```

## Rules
- **Always draft before publishing** — never push live without Chris's OK
- **Back up current content** before making changes
- **After completing work**, update `SHIFT-LOG.md` in the `npcwoods-business` repo
- **HIPAA** — no patient data anywhere in this repo, ever

---

*Last updated: March 12, 2026*
