# Website recipes — current operating contract

Updated 2026-09-06 from local source and regression tests. This describes the kitchen tools; it does not claim any local change is live.

## One executable tracking policy

`scripts/website_policy.py` owns the static-page policy. The publisher, eight-city generator, and Site Guardian consume it. Static public HTML must not load Meta, GTM, GA4, Google Ads, DoubleClick, or `/tracking.js`. Preserve the existing approved Ahrefs behavior. The PHP homepage has a separate existing policy and is outside static-page repair. Never infer permission to add a tracker from an old page or a retired skill example.

Run the read-only drift check before cooking and again before a review:

```sh
python3 scripts/check-website-recipes.py --hq-root /Users/macmini/Desktop/Chris-HQ
python3 scripts/build-search-safe-pages.py --check
```

These check local source and recipes; neither contacts the live site. The first also catches retired tracking instructions in the active HQ skills. Fix the originating recipe and regenerate affected pages; do not weaken a guard just to get a green result. No source cleanup goes live without Chris's explicit approval.

## Page proof

`scripts/deploy.py --pages <slug> --verify-only` checks the ordinary address without a query string. The response must be HTTP 200, remain at that address, match the local title and H1, contain a substantial body relative to the local source, and satisfy the shared tracking policy. A cache-busting alternate cannot override a failure.

Full success also requires the clean address to pass mobile and desktop browser checks, with screenshots. Missing Playwright or a browser is a failure to complete verification, never a full pass. Redirect-only routes and first-time WordPress routing/stub creation remain separate, explicit work.

Browser runtime setup (local environment only): create a dedicated Python environment, install `scripts/requirements-verification.txt`, then run `python -m playwright install chromium`. The worker's `WEBSITE_PYTHON` points to that interpreter. Alternatively, when Chrome is installed, set `NPCWOODS_BROWSER_CHANNEL=chrome`. Installing or scheduling a background worker remains a separate approved action.

## Preview handoff

Build into a new output directory for each ticket. A build never overwrites an older preview, publishes, or creates a review-ready URL by itself.

```sh
python3 scripts/build-vercel-preview-site.py --page <slug> --json
```

The last JSON line names the bundle and `preview-manifest.json`, which records exact routes, title/H1, and source/preview hashes. The bundle excludes credentials/server code and strips production tracking from preview pages. An explicitly approved preview publication runs Vercel against this bundle only, waits for readiness, then checks it:

```sh
python3 scripts/verify-preview.py --manifest <bundle>/preview-manifest.json --base-url <preview-origin> --json
```

Chris gets the verified page URL, checks, and outstanding approval state. An authentication wall, missing page, stale bundle, or failed browser check is not a review-ready result.

## Approval and scope

Local preparation, preview publication, GitHub saves, production pushes, and scheduling are distinct actions. An approved preview is not approval to change npcwoods.com. The worker requires an approved production task plus an exact page-to-source-hash map. The publisher checks that map before loading credentials and uploads the exact bytes checked in its plan. A later local edit needs a new review.

Use the current tools above. Dated scripts, old shift reports, and historical status notes are evidence of past work, not alternate current recipes. Keep AGENTS.md and CLAUDE.md pointers aligned.
