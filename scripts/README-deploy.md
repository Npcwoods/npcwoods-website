# scripts/deploy.py — the one guarded deploy tool

`deploy.py` supersedes the dated one-off deploy scripts in this folder
(`deploy-uti-search-safe-cities-2026-06-12.py`, `deploy-mesa-search-safe-2026-06-11.py`,
`deploy-meta-pixel-strip-health-2026-06-11.py`, `deploy-discovery-audit-2026-06-10.py`,
`flush-discovery-audit-2026-06-10.py`, and friends). The old scripts are kept
for history and are still runnable, but new deploys should use `deploy.py`.

It runs the same proven pipeline every dated script reimplemented:

1. **Safety checks** on each local file (no GTM/GA/Ads/tracking.js/Meta
   markers in kitchen HTML; warns if "insurance" appears). Homepage PHP
   is the exception. Do not weaken the tool if a leftover file still has
   pixels — strip the file first.
2. **SFTP upload** (paramiko) of `landing-pages/{path}/index.html` to GoDaddy
   `html/{path}/index.html` — after downloading a timestamped backup of the
   existing remote file to `content-output/deploy-backups/<date>/`.
   Nothing is ever deleted, locally or remotely.
3. **Cache flush** — touches the matching WordPress stub via the REST API
   (no-op update → GoDaddy Varnish purge). Stub IDs come from the table in
   the script plus `scripts/page-ids-2026-04-22.json`; search-safe child
   pages flush their parent city stub. Brand-new URLs have nothing cached
   and are skipped with a note.
4. **Live verification** — clean public URL with no query string (200,
   doctype). A `?v=` / `?n=1` cache-bust can lie while patients still see
   an empty WordPress shell. If Playwright is installed, a mobile tracking
   run also checks zero Meta pixel requests per page.

Credentials load from `~/Desktop/Chris-HQ/.env` (python-dotenv if installed,
manual parse otherwise). Never hardcoded, never committed.

## The guard (non-negotiable)

- **Default is dry-run.** It prints the plan (local file → remote path,
  size + sha256) and exits. No SFTP connection, no WP request, no
  credentials loaded.
- `--live` requires the confirmation phrase `CHRIS APPROVED LIVE DEPLOY` —
  typed interactively at the prompt, or passed via
  `--confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY"` after Chris has
  explicitly approved. Anything else exits with code 2 and uploads nothing.

## Usage

```bash
# 1. Dry-run (default) — see exactly what would be uploaded, touch nothing
python3 scripts/deploy.py --pages uti-treatment/mesa-az/search-safe,uti-treatment/tempe-az/search-safe

# 2. Live deploy (only after Chris says yes) — backs up remote files first,
#    uploads, flushes cache stubs, verifies live URLs, prints a report
python3 scripts/deploy.py --pages uti-treatment/mesa-az/search-safe --live
#    ... then type: CHRIS APPROVED LIVE DEPLOY

# 3. Verify-only — no upload, just run the live tracking verification
python3 scripts/deploy.py --pages uti-treatment/mesa-az/search-safe --verify-only
```

For paid attribution specifically, verify the full browser path from paid
landing page -> SMS marker -> same-browser `/pay` handoff -> Stripe URL params:

```bash
node scripts/verify-paid-attribution-live.mjs
```

Big batches go in a manifest file (one page path per line, `#` comments OK):

```bash
python3 scripts/deploy.py --manifest content-output/manifests/june-batch.txt
```

Optional extras:

- `--remote-diff` — during dry-run, also connect read-only over SFTP and
  show whether each remote file differs (size/checksum). Off by default so
  a plain dry-run touches nothing at all.
- `--skip-verify` / `--skip-flush` — for the rare partial run.

## What deploy.py deliberately does NOT do

Variations that lived in individual dated scripts and are out of scope here:

- **mu-plugin route patching / WP stub creation** (`deploy-page.py` did this).
  deploy.py assumes the route and stub already exist — first-time page
  launches still need the mu-plugin entry added and a stub created.
- **Git-commit-driven file selection** (`deploy-discovery-audit-2026-06-10.py`
  derived its file list from a commit). Use an explicit `--pages` list or
  manifest instead.
- **IndexNow pings** — run `scripts/indexnow-submit.py` separately for
  indexable pages.
- **Sitemap-exclusion (faq-schema) patching** for noindex pages.
- **Non-landing-page code beyond a fixed allow-list.** Pages ship from
  `landing-pages/**/index.html`; new image/asset files ship with `--asset`;
  the homepage template, four mu-plugins, `npc-menu.js`, `llms*.txt` and the
  shared header/footer snippets ship with `--file` (below). Anything else
  (`tracking.js`, the route file, other mu-plugins, `wp-config.php`) is refused.
- **Page-specific forbidden-word lists** (the search-safe scripts blocked
  drug names). deploy.py enforces the universal guards (Meta pixel,
  "insurance" warning); campaign-specific wordlists stay in review.

## New asset files (`--asset`, added 2026-11-02)

For a page's new share card or picture, add `--asset` with the repo-relative
path under `assets/` (repeatable, or comma-separated):

```bash
python3 scripts/deploy.py --pages learn/ear-infection \
    --asset assets/img/share/learn-ear-infection-v2-1200x630.jpg            # dry-run plan
python3 scripts/deploy.py --pages learn/ear-infection \
    --asset assets/img/share/learn-ear-infection-v2-1200x630.jpg --remote-diff  # + read-only server check
python3 scripts/deploy.py --pages learn/ear-infection \
    --asset assets/img/share/learn-ear-infection-v2-1200x630.jpg \
    --live --confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY"
```

- Only paths under `assets/` in the repo; they go to `public_html/assets/...`
  over the same key-only SFTP session. Anything else (php/, landing-pages/,
  `..`, symlinks out of assets/) is refused.
- Same guards as pages: the counter, clean main == origin/main, and the
  confirmation phrase for `--live`. Dry-run prints the plan and touches nothing.
- **Assets go up first, and only as NEW files.** If the remote file already
  exists it is never overwritten: reported `matching` when its sha equals the
  kitchen copy, otherwise `SKIPPED`. A skipped or failed asset holds every
  page in that run (nothing else is uploaded; result ATTENTION NEEDED), since
  pages usually point at it. To replace an image, give it a new file name
  (e.g. `-v2`).
- Uploaded/matching assets are purged and their clean public URL sha is
  checked against the kitchen file exactly like pages (single-URL purge, then
  full-site fallback, STALE on mismatch).
- `--verify-only --asset ...` checks the public URL sha with no upload.
- Nothing is ever deleted.

## Allow-listed site files (`--file`, added 2026-11-02)

Chris, 2026-11-02 13:59 ET: "Add homepage/menu/footer/llms.txt upload to the
house tools with backups." `--file` overwrites one of these files **in place**:

| repo file | server path |
|---|---|
| `homepage/page-npcwoods-home.php` | `public_html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php` |
| `php/npcwoods-compliance-footer.php` | `public_html/wp-content/mu-plugins/npcwoods-compliance-footer.php` |
| `php/npcwoods-eeat.php` | `public_html/wp-content/mu-plugins/npcwoods-eeat.php` |
| `php/npcwoods-faq-schema.php` | `public_html/wp-content/mu-plugins/npcwoods-faq-schema.php` |
| `php/npcwoods-robots-extras.php` | `public_html/wp-content/mu-plugins/npcwoods-robots-extras.php` |
| `assets/js/npc-menu.js` | `public_html/assets/js/npc-menu.js` |
| `llms.txt`, `llms-full.txt` | `public_html/llms.txt`, `public_html/llms-full.txt` |
| `html/shared/footer-snippet.html`, `html/shared/header-snippet.html` | `public_html/shared/...` |

```bash
python3 scripts/deploy.py --file homepage/page-npcwoods-home.php                 # dry-run plan
python3 scripts/deploy.py --file homepage/page-npcwoods-home.php --remote-diff   # + read-only server check
python3 scripts/deploy.py --file homepage/page-npcwoods-home.php --live \
    --confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY"
python3 scripts/deploy.py --file llms.txt,llms-full.txt --live --confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY"
```

Rules the tool enforces:

- Anything not in the table is refused (no path rewriting, no traversal).
- `--file` runs alone (no `--pages`/`--asset` in the same run) and takes
  **one PHP file per run**: homepage template first, verify, then each mu-plugin.
- PHP must pass `php -l` before any server contact.
- The server file must already exist: it never creates files (so never a new
  mu-plugin, never a `copy 1.php`), never renames, never deletes.
- Before uploading a PHP file it reads every other `.php` in `mu-plugins/`
  and refuses if any of them defines a function the new file defines.
- A dated backup of the server copy is downloaded to
  `content-output/deploy-backups/<date>/` before the upload, and the uploaded
  server copy is read back and sha-checked.
- Same clean-main / HEAD == origin/main / kitchen-counter guard and the same
  live confirmation phrase as pages.
- After upload: exact-URL purge + live sha check for the public files
  (`npc-menu.js`, `llms*.txt`, snippets), and a full-site purge for anything
  that changes rendered pages (PHP, snippets). Then it renders the homepage
  (200, custom hero, same title, no PHP error text) and, for mu-plugins, a
  page WordPress renders itself (`/2026/`). If a render check fails, the backup
  it just took goes straight back, the site is purged again, and the run ends
  `ATTENTION NEEDED`.
- `--verify-only --file ...` re-runs the sha and render checks with no upload.

## One-page banned-word exceptions

`facts/practice.json` → `banned_word_allowed_phrases_by_page` maps one repo
page to exact sentences Chris approved on that page only. deploy.py requires
each sentence to appear **exactly once** on that page; any other banned word
on the page, or the same sentence on any other page, still blocks. There is
no bypass flag. Current entry (Chris, 2026-11-02 13:59 ET, "OK a one-time pass
past the lock"): `landing-pages/washington-uti-treatment/index.html` →
"NPCWoods doesn't take insurance, so there's nothing to file."

## Tests

```bash
python3 -m unittest tests/test_deploy_tool.py -v
```

Covers path resolution, manifest parsing, dry-run-makes-no-SFTP-calls,
backup path generation, stub resolution, the live-confirmation guard, and
`--asset` (assets/-only paths, new-only uploads, matching/skip reporting,
assets before pages, skipped asset holds pages, no remote deletes), `--file`
(allow-list, one PHP per run, php -l, no new files, duplicate-function refusal,
backup then overwrite, render failure restores the backup, purge + sha check),
and the one-page banned-word exception (exactly once, that page only).
