# Pink Eye Treatment Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a Maven-informed, conversion-first pink-eye treatment landing page at `/pink-eye-treatment/` that is clinically cautious, compliant, and easy to use on a phone.

**Architecture:** Add one standalone HTML page served by the existing `npcwoods-static-pages.php` route map. The page will reuse the exact shared header, EEAT byline, footer, and tracking assets; new page-specific CSS will implement the warm evergreen, cream, editorial-italic visual treatment while retaining one clear $59 visit CTA.

**Tech Stack:** Static HTML/CSS/vanilla JavaScript, PHP MU-plugin routing, JSON-LD, Python `unittest`, guarded SFTP deploy script, Playwright.

---

### Task 1: Add a page-level regression and compliance test

**Files:**
- Create: `tests/test_pink_eye_treatment_page.py`
- Test: `tests/test_pink_eye_treatment_page.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing-pages/pink-eye-treatment/index.html"
ROUTER = ROOT / "php/npcwoods-static-pages.php"

class PinkEyeTreatmentPageTest(unittest.TestCase):
    def test_page_and_route_are_present_and_compliant(self):
        html = PAGE.read_text(encoding="utf-8")
        router = ROUTER.read_text(encoding="utf-8")
        self.assertIn('"pink-eye-treatment"', router)
        self.assertIn('href="https://npcwoods.com/pink-eye-treatment/"', html)
        self.assertIn('src="/tracking.js"', html)
        self.assertIn('application/ld+json', html)
        self.assertIn('Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT', html)
        self.assertNotRegex(html, re.compile(r'\\binsurance\\b|\\bdoctor\\b|\\bsubscription\\b', re.I))
```

- [ ] **Step 2: Run the focused test to confirm it fails before the page exists**

Run: `python3 -m unittest tests.test_pink_eye_treatment_page -v`

Expected: `FileNotFoundError` because the new page has not yet been created.

### Task 2: Create the mobile-first treatment page

**Files:**
- Create: `landing-pages/pink-eye-treatment/index.html`

- [ ] **Step 1: Build the document shell and search metadata**

```html
<title>Pink Eye Treatment Online | $59 Visit | NPCWoods</title>
<meta name="description" content="Get a clinician's guidance for pink eye by text. $59 flat fee, no video call, and clear next steps for eligible patients in 11 states.">
<link rel="canonical" href="https://npcwoods.com/pink-eye-treatment/">
```

- [ ] **Step 2: Paste the current shared header immediately after `<body>`, the EEAT byline after the hero, and the current shared footer before `</body>`**

```html
<!-- Shared components are copied verbatim from html/shared/. -->
```

- [ ] **Step 3: Add Maven-informed, original visual styling**

```css
:root { --forest:#013126; --forest-2:#035748; --cream:#ede9e3; --mint:#58eda2; --ink:#17352f; }
.hero { background:linear-gradient(120deg,var(--forest),#09261f); color:#fff; }
.display-accent { font-family:Georgia,serif; font-style:italic; }
.cta-primary { background:var(--mint); color:var(--forest); border-radius:999px; }
```

- [ ] **Step 4: Add the conversion and safety sections**

```html
<section id="symptoms"><h2>What your symptoms may suggest</h2><p>Explain watery, thick-discharge, and itchy-eye patterns without claiming a diagnosis.</p></section>
<section id="how-it-works"><h2>Three texts. Clear next steps.</h2><p>Start a $59 visit, answer a clinician's questions, and receive a clear next step.</p></section>
<aside class="red-flags">Eye pain, light sensitivity, blurred vision, intense redness, injury, or a contact-lens concern needs in-person eye care.</aside>
<section id="faq"><h2>Common questions</h2><p>Cover contacts, contagiousness, antibiotics, and when to seek in-person care.</p></section>
```

- [ ] **Step 5: Include `MedicalWebPage`, `MedicalCondition`, `FAQPage`, and `BreadcrumbList` JSON-LD; use citations to the CDC treatment and symptoms pages in the visible references.**

### Task 3: Register the static route and validate it locally

**Files:**
- Modify: `php/npcwoods-static-pages.php:13-16`
- Test: `tests/test_pink_eye_treatment_page.py`

- [ ] **Step 1: Add the exact static map entry**

```php
"pink-eye-treatment" => "pink-eye-treatment/index.html",
```

- [ ] **Step 2: Run the focused regression test**

Run: `python3 -m unittest tests.test_pink_eye_treatment_page -v`

Expected: `OK`.

- [ ] **Step 3: Run the deploy tool's safety tests**

Run: `python3 -m unittest tests.test_deploy_tool tests.test_sftp_upload_safety -v`

Expected: existing test expectations are preserved; no new failure is attributable to this page.

### Task 4: Dry-run, publish, and verify the live page

**Files:**
- Deploy: `landing-pages/pink-eye-treatment/index.html`
- Deploy: `php/npcwoods-static-pages.php`
- Create: `content-output/reports/pink-eye-treatment-verify-2026-08-09/verification-results.md`

- [ ] **Step 1: Run a read-only safety review of the local page and route**

Run: `python3 -m unittest tests.test_pink_eye_treatment_page tests.test_deploy_tool -v`

Expected: the new page passes its focused compliance contract and deploy-tool safety tests pass.

- [ ] **Step 2: Use the first-time-page deployment utility with the explicit user-provided live approval**

Run: `python3 scripts/deploy-page.py --local landing-pages/pink-eye-treatment/index.html --slug pink-eye-treatment --title "Pink Eye Treatment Online | NPCWoods"`

Expected: timestamped remote backups, static HTML upload, remote MU-plugin route patch, published WordPress route stub, cache flush, and a cache-busted HTTP check.

- [ ] **Step 3: Confirm the remote route is covered by `deploy-page.py`, then do not make a duplicate MU-plugin upload.**

```bash
python3 scripts/deploy-page.py --local landing-pages/pink-eye-treatment/index.html --slug pink-eye-treatment --title "Pink Eye Treatment Online | NPCWoods"
```

- [ ] **Step 4: Run browser verification at 375px and 1440px; confirm the hero, CTAs, tracking asset, schemas, headers/footers, absence of forbidden terms, and no mobile overlay. Save screenshots and the results report.**

- [ ] **Step 5: Commit and push only the page, route, test, plan, and verification artifacts**

```bash
git add landing-pages/pink-eye-treatment/index.html php/npcwoods-static-pages.php tests/test_pink_eye_treatment_page.py docs/superpowers/plans/2026-08-09-pink-eye-treatment-page.md content-output/reports/pink-eye-treatment-verify-2026-08-09
git commit -m "[landing-page] add pink eye treatment page"
git push -u origin feature/pink-eye-treatment-page
```
