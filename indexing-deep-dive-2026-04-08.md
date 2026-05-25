# NPCWoods Indexing Deep Dive

Date: 2026-04-08
Domain: `https://npcwoods.com`

## Executive Summary

This is not a "Google cannot crawl the site" problem.

Google can reach the domain, fetch `robots.txt`, read the XML sitemaps, and at least some education pages are already indexed. The indexing problem is a quality and URL-governance problem: Google is being shown duplicate, conflicting, and legacy URLs on a relatively new domain.

## What Is Working

- `robots.txt` is open and points to `https://npcwoods.com/sitemap_index.xml`
- `sitemap_index.xml` is live and references both `page-sitemap.xml` and `post-sitemap.xml`
- Key page types return `200`
- Education pages like `/learn/skin-infection/` are already appearing in Google search results

## Root Causes Found

### 1. Duplicate WordPress page is still live and indexable

Legacy page:
- `/patient-experience-2/`
- WordPress page ID `310`

Problem:
- Returns `200`
- Self-canonicalizes to `/patient-experience-2/`
- Appears in `page-sitemap.xml`

Impact:
- Duplicate quality signal against `/patient-experience/`

### 2. Same slug is published as both a page and a post

Conflicting URL:
- `/telehealth-vs-urgent-care/`

Objects:
- WordPress page ID `433`
- WordPress post ID `436`

Problem:
- The live URL renders the static landing page
- The post is also published with the exact same slug and URL
- The URL appears in both `page-sitemap.xml` and `post-sitemap.xml`
- The blog archive links to that same conflicting URL

Impact:
- Mixed signals about what the canonical document actually is
- Duplicate sitemap pollution on a small domain

### 3. Intended redirects are still serving 200 pages

Legacy URLs still live:
- `/experience/`
- `/how-it-works/`

Problem:
- Repo comments describe these as redirect/legacy behavior
- Live responses currently return `200`
- `/experience/` appears to be served directly from a static file path, not cleanly redirected

Impact:
- More duplicate or near-duplicate experience/process content

### 4. Sitemap hygiene is still imperfect

Confirmed issues:
- Homepage appears twice in `page-sitemap.xml`
- `/patient-experience-2/` was still sitemap-eligible before local cleanup
- Cross-sitemap duplication exists for `/telehealth-vs-urgent-care/`

Impact:
- Lowers trust in sitemap quality
- Makes crawl prioritization harder on a young domain

### 5. Important discovery is intentionally constrained

Current strategy:
- City pages are deliberately excluded from the XML sitemap

This is not inherently wrong, but it means:
- Google has to discover those pages through internal links alone
- Some city pages may stay in "discovered" or "crawled, not indexed" longer than expected

## Why Indexing Feels "Stuck"

On a young domain, Google is conservative.

When the site sends signals like:
- duplicate URLs
- page/post slug collisions
- legacy pages still indexable
- redirect-intended pages still live
- sitemap inconsistencies

Google often slows down trust and selective indexing instead of indexing everything quickly.

That matches what is happening here.

## Safe Cleanup Order

### Immediate

1. Remove the duplicate legacy page from sitemap eligibility
   - Done locally in `php/npcwoods-faq-schema.php`
   - Added page ID `310`

2. Fix the page/post slug collision
   - Keep only one owner for `/telehealth-vs-urgent-care/`
   - Either:
     - keep the static landing page and rename the blog post slug
     - or keep the blog post and move the landing page to a unique slug

3. Unpublish or redirect `/patient-experience-2/`
   - Best outcome: draft it or 301 it to `/patient-experience/`

### Next

4. Decide canonical experience/process URLs
   - `/patient-experience/`
   - `/how-it-works/`
   - `/experience/`

5. Ensure only the intended URLs return `200`
   - Everything else should 301 or disappear from indexing

6. Regenerate or re-check the XML sitemap after cleanup

### After Cleanup

7. In Google Search Console:
   - resubmit sitemap
   - inspect the top canonical URLs
   - request indexing for the fixed pages

## Local Repo Changes Made

1. Added legacy page ID `310` to sitemap exclusions in:
- `php/npcwoods-faq-schema.php`

2. Added slug-collision guidance and corrected active static-route docs in:
- `CLAUDE.md`

## Live Cleanup Performed

Date: 2026-04-08

1. WordPress page `310` (`/patient-experience-2/`) changed from `publish` to `draft`
2. WordPress post `436` (`/telehealth-vs-urgent-care/`) changed from `publish` to `draft`

Date: 2026-04-09

3. Deployed a real static redirect for `/experience/` to `/patient-experience/`
4. Updated sitemap exclusions so the homepage no longer appears twice in `page-sitemap.xml`
5. Re-allowed the intentional `/how-it-works/` page in the sitemap
6. Resubmitted `https://npcwoods.com/sitemap_index.xml` in Google Search Console under `sc-domain:npcwoods.com`

## Post-Cleanup Verification

- `wp-json/wp/v2/pages?slug=patient-experience-2` now returns no published result
- `wp-json/wp/v2/posts?slug=telehealth-vs-urgent-care` now returns no published result
- `post-sitemap.xml` no longer includes `/telehealth-vs-urgent-care/`
- `page-sitemap.xml` still includes the intended landing page `/telehealth-vs-urgent-care/`
- `page-sitemap.xml` no longer shows `/patient-experience-2/`
- `/experience/?nocache=1` now returns `301` to `/patient-experience/`
- `/how-it-works/?nocache=1` returns `200` and is now present in `page-sitemap.xml`
- `page-sitemap.xml?nocache=1` now contains only one homepage entry
- Search Console accepted the sitemap submission on `2026-04-09T04:43:08.121Z`
- Search Console currently shows the sitemap index as `isPending: true`, which is normal immediately after resubmission

## Remaining Follow-Up

1. Wait for Search Console to re-fetch the sitemap index and refresh `lastDownloaded`
2. Inspect the canonical URLs in GSC once the pending sitemap finishes processing
3. Optional content cleanup: update old internal links that still point to `/experience/` so they link directly to `/patient-experience/`
4. Optional sitemap cleanup: investigate the existing `author-sitemap.xml` error shown in Search Console

## Recommended Production Decisions

### Best default path

- Keep `/telehealth-vs-urgent-care/` as the static landing page
- Rename blog post `436` to a unique slug
- Draft or redirect page `310`
- Decide whether `/experience/` should redirect to `/patient-experience/` or be retired entirely

## Bottom Line

The site is crawlable.

The main problem is that Google is being asked to trust too many competing versions of similar content on a young domain. Clean up the legacy page, fix the slug collision, and tighten the experience/process URL set. That should improve indexation much more than publishing more pages into the current mess.
