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
| Blog archive | 413 | https://npcwoods.com/blog/ |
| Georgia landing | 252 | https://npcwoods.com/georgia-telemedicine/ |
| North Carolina landing | 253 | https://npcwoods.com/north-carolina-telemedicine/ |
| AZ affordable | 198 | https://npcwoods.com/affordable-telemedicine-arizona-no-insurance/ |
| Dental pain (abscess) | 336 | https://npcwoods.com/dental-pain/ |
| Pharmacy | 334 | https://npcwoods.com/pharmacy/ |
| Pharmacy Partners | 335 | https://npcwoods.com/pharmacy-partners/ |

## Blog Publishing (added 2026-03-31)

Blog posts use **WordPress's native post system** — no SFTP or mu-plugins needed.

**To publish a blog post:**
```
POST https://npcwoods.com/wp-json/wp/v2/posts
{
  "title": "Post Title",
  "content": "<p>HTML content here</p>",
  "status": "draft",   ← always draft first, Chris approves, then set to "publish"
  "slug": "url-friendly-slug"
}
```

Posts automatically:
- Appear on /blog/ archive page
- Get added to Yoast's post-sitemap.xml
- Render through the WP block theme (which has the full site nav)

**Always disable comments:** Include `"comment_status": "closed", "ping_status": "closed"` in every blog post payload. Chris does not want comments on the blog.

**Workflow:** Use `/draft-content` skill to write in Chris's voice → show HTML mockup → Chris approves → publish via REST API.

## Headshot Image (added 2026-03-31)

Chris's headshot is used site-wide instead of the logo:
- **Headshot URL:** `https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png`
- **Logo URL (favicons only):** `https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg`
- When adding new pages, use the headshot for nav, about sections, OG images, footer. Use the logo only for `<link rel="icon">` and `<link rel="apple-touch-icon">`.

## SEO / Sitemap Strategy (added 2026-03-31)

**Sitemap is focused on 68 core pages.** 81 city pages are temporarily excluded from the sitemap to concentrate crawl budget while domain authority is low. City pages still work if visited directly.

Exclusions are managed in `php/npcwoods-faq-schema.php` via the `wpseo_exclude_from_sitemap_by_post_ids` filter. When domain authority grows and core pages are indexed, re-add city pages by removing their IDs from that array.

**Slug collision rule:** never publish a WordPress post on the same slug as a static HTML bypass page or page stub. If a page slug is already owned by a mu-plugin-served landing page, the blog post must use a unique slug. Collisions cause duplicate sitemap entries and mixed indexing signals.

## Deployment

### Standard pages (WordPress content)
Push content via WordPress REST API. Always draft first, get Chris's approval, then publish.

### Static HTML bypass pages (Experience, Dental, Pharmacy, LLM-SEO)
These pages bypass WordPress's block theme (which strips scripts/styles):
1. Upload HTML via SFTP to the appropriate folder on the server (e.g., `/dental-pain/index.html`)
2. A must-use plugin intercepts the URL and serves raw HTML
3. Create/update the WP page at the same slug via REST API (for sitemap/routing)

**Active mu-plugins for HTML bypass:**
- `npcwoods-experience-page.php` → `/patient-experience/`, `/how-it-works/`
- `npcwoods-dental-pages.php` → `/dental-pain/`
- `npcwoods-pharmacy-pages.php` → `/pharmacy/`, `/pharmacy-partners/`
- `npcwoods-llmseo-pages.php` → `/mesa-uti-treatment/`, `/albuquerque-uti-treatment/`, `/scottsdale-uti-treatment/`, `/blog-burning-when-you-pee-albuquerque/`
- `npcwoods-comparison-pages.php` → `/telehealth-vs-urgent-care/`, `/uti-treatment-online/`
- `npcwoods-education-pages.php` → `/learn/*` (14 conditions + hub), `/medications/*` (21 drugs) — **36 routes total**

## Shared Components (Header & Footer)

Every page on the site MUST include the shared header and footer snippets. These provide site-wide navigation and internal linking (~30 links per page).

**Files:**
- `html/shared/header-snippet.html` — Sticky nav with logo, conditions dropdown, states dropdown, how it works, pharmacy info, CTA button, mobile hamburger menu
- `html/shared/footer-snippet.html` — Dark footer with brand info, conditions list, all 11 state links, quick links, clinician trust line

**How to use:**
1. Copy the header `<style>` + `<nav>` HTML → paste right after `<body>`
2. Copy the footer `<style>` + `<footer>` HTML → paste before `</body>`

**When updating these snippets**, update ALL existing pages that include them. Consider writing a script to automate this.

## Folder Structure

```
npcwoods-website/
├── CLAUDE.md          ← You are here
├── html/
│   ├── shared/
│   │   ├── header-snippet.html  ← Shared site header (include on ALL pages)
│   │   └── footer-snippet.html  ← Shared site footer (include on ALL pages)
│   ├── experience/
│   │   └── index.html ← Experience page source
│   ├── pharmacy/
│   │   └── index.html ← Pharmacy page (for patients)
│   └── pharmacy-partners/
│       └── index.html ← Pharmacy partners page (for pharmacies)
├── landing-pages/
│   ├── conditions/
│   │   └── index.html ← Conditions index (links to all condition hubs)
│   ├── uti-treatment/
│   │   └── index.html ← UTI condition hub page
│   ├── sinus-infection-treatment/
│   │   └── index.html ← Sinus infection hub page
│   ├── dental-pain/
│   │   └── index.html ← Dental pain landing page (LIVE)
│   ├── arizona-telemedicine/
│   │   └── index.html ← Arizona state landing page
│   ├── new-mexico-telemedicine/
│   │   └── index.html ← New Mexico state landing page
│   ├── colorado-telemedicine/
│   │   └── index.html ← Colorado state landing page
│   ├── idaho-telemedicine/
│   │   └── index.html
│   ├── iowa-telemedicine/
│   │   └── index.html
│   ├── montana-telemedicine/
│   │   └── index.html
│   ├── nevada-telemedicine/
│   │   └── index.html
│   ├── oregon-telemedicine/
│   │   └── index.html
│   ├── utah-telemedicine/
│   │   └── index.html
│   ├── sitemap/
│   │   └── index.html ← HTML sitemap (links to EVERY page)
│   ├── experience/
│   ├── pharmacy/
│   └── pharmacy-partners/
├── blog/
│   └── no-insurance-no-problem.html
├── landing-pages/learn/           ← Patient education library (14 conditions + hub)
│   ├── index.html                 ← "After Your Visit" hub page
│   ├── strep-throat/index.html
│   ├── uti/index.html
│   ├── sinus-infection/index.html
│   ├── tooth-infection/index.html
│   ├── ear-infection/index.html
│   ├── stomach-bug/index.html
│   ├── pink-eye/index.html
│   ├── bronchitis/index.html
│   ├── skin-infection/index.html
│   ├── allergic-reaction/index.html
│   ├── cold-sores/index.html
│   ├── yeast-infection/index.html
│   ├── ingrown-toenail/index.html
│   └── covid-flu/index.html
├── landing-pages/medications/     ← Drug reference pages (21 medications)
│   ├── amoxicillin/index.html
│   ├── augmentin/index.html
│   ├── azithromycin/index.html
│   ├── ... (18 more)
│   └── polytrim/index.html
├── php/
│   └── npcwoods-education-pages.php ← mu-plugin for /learn/ and /medications/ routes
└── scripts/
    ├── deploy-education-library.sh  ← SFTP upload script for all education pages
    └── create-wp-page-stubs.sh      ← Creates WP page entries for sitemap
```

## Hub Page Architecture

The site uses a **hub-and-spoke** model for internal linking:

```
Homepage
  ├── /conditions/  (master index → links to all condition hubs)
  │     ├── /uti-treatment/  (condition hub → links to all UTI city pages)
  │     │     ├── /mesa-uti-treatment/
  │     │     ├── /scottsdale-uti-treatment/
  │     │     └── ...
  │     ├── /sinus-infection-treatment/
  │     ├── /dental-pain/
  │     └── ...
  ├── /arizona-telemedicine/  (state hub → links to all AZ city pages)
  │     ├── /mesa-uti-treatment/
  │     ├── /scottsdale-uti-treatment/
  │     └── ...
  ├── /georgia-telemedicine/
  ├── /experience/
  └── /pharmacy/
```

Every city page links BACK to its condition hub AND state hub. This creates a crawlable web that Google can follow.

### Patient Education Library (`/learn/` + `/medications/`)
Hub-and-spoke architecture for patient education:
```
Homepage (education section)
  └── /learn/  (hub — "After Your Visit" library index)
        ├── /learn/strep-throat/     → links to amoxicillin, penicillin, azithromycin
        ├── /learn/uti/              → links to nitrofurantoin, tmp-smx
        ├── /learn/sinus-infection/  → links to amoxicillin, augmentin, azithromycin, doxycycline
        ├── ... (14 conditions total)
        └── /medications/amoxicillin/  → links back to strep-throat, sinus-infection, ear-infection, etc.
            /medications/augmentin/    → links back to sinus-infection, ear-infection, etc.
            ... (21 drugs total)
```
Each condition page links to its relevant drug pages. Each drug page links back to conditions it treats. All pages link to the `/learn/` hub. Premium design system v3 with gradient heroes, glassmorphic badges, DM Serif Display headings, hover-lift cards, FAQ accordions, and mobile floating CTA.

## Deployment Skill

There's a full deployment skill at `skills/npcwoods-deploy/SKILL.md` — read it before deploying anything. It covers SFTP via paramiko, mu-plugin creation, WP REST API page stubs, and homepage modification. Includes helper scripts in `scripts/` and gotcha documentation in `references/gotchas.md`.

## Rules
- **Always draft before publishing** — never push live without Chris's OK
- **Back up current content** before making changes
- **Read the deploy skill** before pushing anything to the server (`skills/npcwoods-deploy/SKILL.md`)
- **After completing work**, update `SHIFT-LOG.md` in the `npcwoods-business` repo
- **HIPAA** — no patient data anywhere in this repo, ever

---

## Lessons Learned

### WL-002 — Cloudflare caches mean post-deploy curl can lie (2026-04-13)
**What happened:** After SFTP-uploading updated meta descriptions, plain `curl` verification returned the OLD content for 4 of 9 URLs. Looked like a deploy failure. Actually Cloudflare was serving cached HTML; the origin had the new content. Wasted minutes chasing a ghost bug.
**The rule:** Always verify deploys by appending a cache-bust query string (`?v=$(date +%s)`) or hitting origin directly. Never trust a raw curl against an npcwoods.com URL as the source of truth for "did the deploy land?" The origin is already updated the moment SFTP succeeds — verification is about propagation, not delivery.

### WL-003 — Meta description rewrites: use the batch script, not Edit calls (2026-04-13)
**What happened:** Updated 32 landing-page `<title>` + `<meta name="description">` tags. Built `scripts/update-meta-descriptions.py` — reads a TSV, writes a `.meta-bak` on first run and always reads from the backup on subsequent runs (idempotent), validates title ≤ 60 chars / desc ≤ 160 chars, blocks banned words (`doctor`, `insurance`, `appointment`, `board-certified`, `Text a Doctor`). TSV manifests live at `scripts/meta-rewrites-YYYY-MM-DD[-batchN].tsv`.
**The rule:** For any batch of >3 meta-tag edits, add rows to a new TSV and run the script. Don't open N files with Edit. The script's validation catches banned words and length violations before they hit the CDN.
**Delimiter gotcha:** Titles contain `|` (brand suffix). Use TSV, not pipe-delimited CSV.

### WL-004 — Generic "board-certified" is banned; "double board-certified" is OK (2026-04-13, updated 2026-04-14)
**What happened:** /about/ and /faq/ had copy saying "Board-certified FNP-C" and "double board-certified NP". Original VOICE.md rule banned "board-certified" across the board. On April 14 Chris clarified: the plain phrase "board-certified" sounds corporate and stays banned, but "double board-certified" is his specific credential claim and IS allowed site-wide (blog meta, landing pages, about page, anywhere).
**The rule:**
- ❌ Never: "board-certified provider," "board-certified NP," "board-certified Nurse Practitioner" (generic corporate)
- ✅ OK: "double board-certified Nurse Practitioner" (his specific credential — adds authority)
- ✅ Also OK: "Licensed Nurse Practitioner" (cleaner for some contexts)
**Enforcement:** The update-meta-descriptions.py script blocks the bare phrase "board-certified" but allows "double board-certified" via a negative-lookbehind check.

### WL-001 — Blog preview CSS does NOT carry to WordPress (2026-04-01)
**What happened:** Built a beautiful local HTML preview with custom CSS classes for the hero image, comparison table colors, and CTA boxes. When pushed to WordPress via REST API, all custom CSS was lost — WordPress posts only render the content HTML inside the theme's existing styles. The hero image disappeared (relied on `featured_media` which the theme doesn't render on single posts), table column colors vanished (relied on CSS classes), and CTA boxes lost some styling.
**The rule:** When translating a local preview to a WordPress post:
1. ALL styling must use inline `style=""` attributes — no CSS classes
2. Hero image must be embedded in the post body as `<figure class="wp-block-image">`, not just `featured_media`
3. Use Gutenberg block comments (`<!-- wp:image -->`, `<!-- wp:table -->`) for proper theme integration
4. Always verify the rendered content via the REST API after publishing
5. The NPCWoods block theme does NOT display `featured_media` as a hero on single post pages

### WL-005 — For patient-growth audits, review reach + conversion + trust together (2026-04-20)
**What happened:** Ran a growth audit to find the top 3 priorities for getting more patients. Reviewed the homepage, `how-it-works`, a core condition hub (`/uti-treatment/`), a state hub (`/arizona-telemedicine/`), the conditions index, tracking setup, and the indexing/sitemap notes. The key insight was that the site's next big gains are not mainly visual polish. The offer is already strong: $59, same day, real clinician, no waiting room. The bigger levers are (1) local-intent reach via city + condition pages, (2) lower-friction conversion on high-intent pages, and (3) more specific trust proof at decision points.
**The rule:** When asked how to get more patients, do not default to "redesign the homepage." Audit in this order:
1. **Reach:** Check sitemap strategy, excluded city pages, hub-and-spoke internal linking, and whether city-condition pages exist for the highest-value conditions.
2. **Conversion:** Review the homepage plus 1 condition hub, 1 state hub, and `how-it-works` for CTA specificity, objection handling, and ease of starting a text visit.
3. **Trust:** Check whether reviews, credentials, NPI/license proof, and "real human / no chatbot" proof are specific to the page intent, not just generic site-wide claims.
**Shift outcome:** Prioritize SEO/discoverability for city-condition pages first, conversion tightening on high-intent pages second, and more condition-specific/local trust proof third.

### WL-006 — Screenshot handoffs must be viewable, not just file links (2026-05-16)
**What happened:** After a local sinus page makeover, screenshots were handed off as local file links to PNGs. On Chris's phone, one opened as a generic "data" file instead of an image preview, so the visual review failed even though the PNG itself was valid locally.
**The rule:** When Chris asks for screenshots, provide a reviewable handoff, not only raw local paths. Create an HTML contact sheet under `content-output/reports/.../screenshot-review.html` with embedded images, include JPG copies alongside PNGs for broad preview compatibility, and use inline image embeds in the response when possible. Verify the files with `file` and visually inspect at least the desktop and mobile screenshot before saying they are ready.
**Why:** Chris often reviews from mobile. A screenshot that only works on the Mac filesystem is not a screenshot handoff.

---

*Last updated: May 16, 2026 — added WL-006 (screenshot handoff must be reviewable on mobile)*
