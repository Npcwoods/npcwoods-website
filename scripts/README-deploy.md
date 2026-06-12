# scripts/deploy.py — the one guarded deploy tool

`deploy.py` supersedes the dated one-off deploy scripts in this folder
(`deploy-uti-search-safe-cities-2026-06-12.py`, `deploy-mesa-search-safe-2026-06-11.py`,
`deploy-meta-pixel-strip-health-2026-06-11.py`, `deploy-discovery-audit-2026-06-10.py`,
`flush-discovery-audit-2026-06-10.py`, and friends). The old scripts are kept
for history and are still runnable, but new deploys should use `deploy.py`.

It runs the same proven pipeline every dated script reimplemented:

1. **Safety checks** on each local file (no Meta pixel markers, warns if
   GTM/tracking.js missing or "insurance" appears).
2. **SFTP upload** (paramiko) of `landing-pages/{path}/index.html` to GoDaddy
   `html/{path}/index.html` — after downloading a timestamped backup of the
   existing remote file to `content-output/deploy-backups/<date>/`.
   Nothing is ever deleted, locally or remotely.
3. **Cache flush** — touches the matching WordPress stub via the REST API
   (no-op update → GoDaddy Varnish purge). Stub IDs come from the table in
   the script plus `scripts/page-ids-2026-04-22.json`; search-safe child
   pages flush their parent city stub. Brand-new URLs have nothing cached
   and are skipped with a note.
4. **Live verification** — cache-busted HTTP check (200, doctype, GTM,
   tracking.js), and if Playwright is installed, a full mobile tracking run
   (GTM + GA4 requests fire, zero Meta pixel requests) per page.

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
- **Non-landing-page assets** (mu-plugins, `tracking.js`, `llms.txt`).
  deploy.py only ships `landing-pages/**/index.html`.
- **Page-specific forbidden-word lists** (the search-safe scripts blocked
  drug names). deploy.py enforces the universal guards (Meta pixel,
  "insurance" warning); campaign-specific wordlists stay in review.

## Tests

```bash
python3 -m unittest tests/test_deploy_tool.py -v
```

Covers path resolution, manifest parsing, dry-run-makes-no-SFTP-calls,
backup path generation, stub resolution, and the live-confirmation guard.
