# Remove Site-wide Meta Pixel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the website's existing no-Meta-on-public-health-pages safeguard without changing page content, routes, payment behavior, or deploying anything.

**Architecture:** Remove the newly added Meta Pixel from all HTML/PHP source surfaces and make the WordPress runtime filter fail closed by stripping third-party tracking rather than inserting Meta. Preserve the new first-party-only checkout safeguard and content/route changes; update the old Google/GTM deployment and guardian expectations so they no longer require third-party trackers.

**Tech Stack:** Static HTML, WordPress mu-plugin PHP, Python `unittest`, existing search-safe page generator.

---

### Task 1: Lock the no-Meta public-source behavior in tests

**Files:**
- Modify: `tests/test_sitewide_meta_tracking.py`
- Test: `tests/test_sitewide_meta_tracking.py`

- [x] **Step 1: Add a failing scan asserting that public HTML and the homepage template do not contain a Meta Pixel initializer or loader.**

- [x] **Step 2: Run `python3 -m unittest tests.test_sitewide_meta_tracking` and confirm it fails because the current draft contains the Pixel.**

### Task 2: Restore source and runtime safeguards

**Files:**
- Modify: tracked HTML/PHP sources changed solely by the sitewide tracking replacement
- Modify: `php/npcwoods-tracking.php`
- Modify: `php/npcwoods-sitewide-meta-pixel.php`
- Modify: `scripts/replace_sitewide_tracking.py`

- [x] **Step 1: Remove the exact Meta block and legacy Google/GTM tracker blocks from public sources without restoring older Meta conversions or overwriting unrelated content changes.**

- [x] **Step 2: Remove the exact Meta block from untracked draft pages while leaving their copy, routes, and city data intact.**

- [x] **Step 3: Change both runtime plugins and the helper script so none can add a Meta Pixel.**

### Task 3: Regenerate derived city pages and verify contracts

**Files:**
- Modify: `landing-pages/uti-treatment/_search-safe-template/template.html`
- Regenerate: `landing-pages/uti-treatment/<city>/search-safe/index.html`
- Test: `tests/test_search_safe_template.py`
- Test: `tests/test_sitewide_meta_tracking.py`
- Test: `tests/test_glp1_page_compliance.py`

- [x] **Step 1: Regenerate search-safe city outputs only from the restored template and existing `cities.json`.**

- [x] **Step 2: Run the focused unit suite, PHP lint, and `git diff --check`; report any pre-existing or unrelated failures separately.**

### Task 4: Review the change boundary

**Files:**
- Review: `git diff --check`
- Review: `git status --short`

- [x] **Step 1: Confirm no Pixel loader, initializer, tracking beacon, or Meta response injector remains in deployable source.**

- [x] **Step 2: Confirm no deployment, commit, deletion, or source-content change outside the approved tracking cleanup occurred.**
