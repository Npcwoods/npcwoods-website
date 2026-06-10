# Server Sync Report — 2026-06-10

Read-only reconnaissance. Nothing was uploaded, modified, or deleted on the server.
Snapshot script: `scripts/server-sync/download-mu-plugins-2026-06-10.py`
Downloaded files: `scripts/server-sync/mu-plugins-2026-06-10/` (37 files)

Connection: paramiko SFTP to `SFTP_HOST` (vki.0b3.myftpupload.com:22), credentials from
`~/Desktop/Chris-HQ/.env`. Remote mu-plugins dir: `html/wp-content/mu-plugins/`.

---

## TASK 1 — Server vs repo `php/` drift

### A. Files on the SERVER but NOT in the repo (server-only routing)

| File | Size | What it routes |
|---|---|---|
| `npcwoods-faq-page.php` | 314 B | `/faq/` → `faq/index.html` (simple `is_page('faq')` + readfile) |
| `npcwoods-ga-nc-pages.php` | 725 B | `/murphy-nc/`, `/blairsville-ga/`, `/blue-ridge-ga/` |
| `npcwoods-glp1-pages.php` | 638 B | `/glp1-weight-loss/` |

These explain 4 of the 7 "live pages with no repo route." Note the server's
`npcwoods-static-pages.php` ALSO has a `"faq" => "faq/index.html"` entry, so `/faq/`
is double-routed on the server (faq-page.php + static-pages.php).

**`/poison-ivy/` and `/thank-you/` have NO mu-plugin route anywhere on the server.**
They exist only as physical directories in the web root:

- `html/poison-ivy/index.html` — 26,576 B
- `html/thank-you/index.html` — 41,998 B

They are evidently served directly by the web server (existing file/dir bypasses WP
rewrite), not through any mu-plugin. If a WP page stub with those slugs is ever
created/changed, routing behavior could shift — worth knowing during reconciliation.

Server also contains non-repo housekeeping files (no action needed, listed for
completeness): GoDaddy system files (`gd-system-plugin.php`, `gd-system-plugin/`,
`object-cache-pro.php`, `object-cache-pro/`, `vendor/`) and 9 `.bak`/`.backup` copies
(`compliance-footer .bak-scrub-20260423`, `eeat .bak-20260429` + `.bak-scrub-20260423`,
`faq-schema .bak-2026-04-14` + `.bak-20260409`, `how-it-works-page.php.bak`,
`payment-link .backup-20260523` ×2, `redirects .backup-20260325` + `.bak-20260412`).

### B. Files in the repo but NOT on the server

None (only `npcwoods-org-schema.php.DEPRECATED-20260429`, intentionally not deployed).

### C. Files that DIFFER (8 of 22 shared files)

Direction key: **SERVER-AHEAD** = server has changes the repo lacks (repo drifted behind
production). **REPO-AHEAD** = repo has newer work that was never deployed (or is being
edited right now by concurrent agents — repo mtimes of Jun 10 00:32–00:33 are concurrent
edits in this session).

| File | Direction | Summary |
|---|---|---|
| `npcwoods-static-pages.php` | SERVER-AHEAD | Server adds `"faq" => "faq/index.html"` to `$page_map`. Otherwise identical. |
| `npcwoods-robots-extras.php` | SERVER-AHEAD | Server runs **v3.0.0** (2026-05-11): per-bot AI blocks collapsed into a single `User-agent: *` block, AI welcome kept as comments. Repo still has **v2.0.0** (per-vendor GPTBot/ClaudeBot/PerplexityBot/etc. blocks). Functionally equivalent allow-all, but repo text is stale. |
| `npcwoods-payment-link.php` | REPO-AHEAD (not deployed) | Repo (2026-05-24, 6,209 B) adds gclid/gbraid/wbraid capture, localStorage attribution (`npc_attribution_last/first`), click-id → `client_reference_id` fallback. Server (3,739 B) is the older UTM-only version. **The May 24 attribution upgrade never went live.** Server backups from 05-23 suggest a deploy was attempted/rolled back. |
| `npcwoods-compliance-footer.php` | REPO-AHEAD (not deployed) | Repo (2026-05-26) adds the `$GLOBALS['npcwoods_shared_footer_rendered']` double-render guard; server lacks it. |
| `npcwoods-eeat.php` | REPO-AHEAD (being edited now) | Server still ships `aggregateRating` (5.0/58) + 3 inline `Review` items. Repo (edited 06-10 00:32) removes self-hosted review markup ("violates Google policy" comment), adds NPI `identifier`, `sameAs` links, `address`, `paymentAccepted`, `makesOffer`, `honorificSuffix`; `credentialCategory` certification vs server's license. |
| `npcwoods-faq-schema.php` | REPO-AHEAD (being edited now) | Repo (edited 06-10 00:33) flips canonical for page 191 to `/strep-throat-treatment/` with option flag `npcwoods_canonicals_set_v6`; server has `/strep-throat-ear-infection/` + `v5`. |
| `npcwoods-dental-pages.php` | MIXED (repo edited now) | Server's copy has an extra `'arizona-telemedicine'` entry — redundant, since server `npcwoods-static-pages.php` also routes it. Repo copy (edited 06-10 00:32) is the clean single-entry version. |

### D. Files that MATCH exactly (14)

about-pages, affordable-arizona-page, blog-page, comparison-pages, education-pages,
experience-page, llmseo-pages, paid-pages, pharmacy-pages, redirects-404-cleanup,
redirects, review-page, save-contact, security-headers, tracking.

### E. ABQ blog file

`html/llmseo/blog-burning-when-you-pee-albuquerque.html` **EXISTS on the server**
(52,997 B) — downloaded to `scripts/server-sync/blog-burning-when-you-pee-albuquerque.html`.
The remote `html/llmseo/` dir holds 4 files total: `albuquerque-uti-treatment.html`,
`blog-burning-when-you-pee-albuquerque.html`, `mesa-uti-treatment.html`,
`scottsdale-uti-treatment.html`.

### Reconciliation cheat-sheet (for the main session — NOT done here)

1. Pull into repo (server is source of truth): `npcwoods-faq-page.php`,
   `npcwoods-ga-nc-pages.php`, `npcwoods-glp1-pages.php`, robots-extras v3.0.0,
   static-pages `faq` entry. Copies sit in `scripts/server-sync/mu-plugins-2026-06-10/`.
2. Decide whether to (re)deploy repo-ahead work: payment-link attribution upgrade,
   compliance-footer guard, eeat schema rewrite, faq-schema v6 canonical.
3. `/poison-ivy/` and `/thank-you/` rely on physical dirs only — consider adding
   explicit mu-plugin routes for resilience.

---

## TASK 2 — AI crawler access at host/Cloudflare layer

All requests via curl from this Mac (i.e., spoofed UAs from a non-bot IP), 1 s apart,
2026-06-10 ~04:34 UTC.

### Results matrix (HTTP status)

| User-Agent | /robots.txt | /llms.txt | / (homepage) |
|---|---|---|---|
| OAI-SearchBot/1.0; +https://openai.com/searchbot | 200 | 200 | 200 |
| **ChatGPT-User/1.0; +https://openai.com/bot** | **403** | **403** | **403** |
| GPTBot/1.1; +https://openai.com/gptbot | 200 | 200 | 200 |
| PerplexityBot/1.0; +https://perplexity.ai/perplexitybot | 200 | 200 | 200 |
| ClaudeBot/1.0; +claudebot@anthropic.com | 200 | 200 | 200 |
| Mozilla/5.0 (control) | 200 | 200 | 200 |

### The ChatGPT-User block

- 403 on **all three URLs including robots.txt**.
- Response is a **Cloudflare** block page: `server: cloudflare`, `cf-ray: a095aa5b…-ATL`,
  body title "Attention Required! | Cloudflare", sets `__cf_bm` bot-management cookie.
- So the block is at the **Cloudflare bot-management/WAF layer**, before
  GoDaddy/Varnish/WordPress ever see the request.
- Caveat: this test sends the UA from a residential IP, so Cloudflare may be flagging
  it as an *impersonated* verified bot. However, the other four AI UAs (GPTBot,
  OAI-SearchBot, PerplexityBot, ClaudeBot) passed from the same IP — so Cloudflare is
  not applying impersonation blocking uniformly; **ChatGPT-User is specifically on a
  block rule**. Since real ChatGPT-User traffic is what fetches pages when a ChatGPT
  user clicks/loads a cited link, this rule is worth reviewing in the Cloudflare
  dashboard (Bot Fight Mode / Super Bot Fight Mode "definitely automated" or an AI-bots
  block toggle). Confirm with Cloudflare firewall events whether genuine OpenAI-ASN
  ChatGPT-User requests are also being challenged.

### Live robots.txt content

Live robots.txt is the **v3.0.0 collapsed format** (matches the SERVER copy of
`npcwoods-robots-extras.php`, NOT the repo's v2.0.0 per-bot copy):

- Single `User-agent: *` block, no per-AI-bot Allow blocks anymore.
- Disallows only noise dirs: `/automation-output/`, `/backups/`, `/scripts/`,
  `/*.bak`, `/*.meta-bak`, `/*.synced.bak`.
- AI welcome (GPTBot, Google-Extended, ClaudeBot, PerplexityBot, Applebot-Extended,
  CCBot, Bytespider, FacebookBot, Amazonbot, Grok) kept as comments; links to
  `/llms.txt` and `/llms-full.txt`; sitemap line present.
- Net effect: **all AI crawlers are allowed at the robots.txt level**. The only
  enforcement-layer problem found is the Cloudflare 403 on the ChatGPT-User UA.
