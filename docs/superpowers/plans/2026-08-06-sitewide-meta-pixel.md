# Site-wide Meta Pixel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Pixel `1428464038973925` fire once on every HTML page while removing Google and prior Meta tracking.

**Architecture:** A single response filter in the existing tracking mu-plugin strips active third-party tracking snippets from the final HTML response and inserts Chris’s exact Meta code above `</head>`. That intercepts WordPress and static `readfile()` pages alike.

**Tech Stack:** PHP mu-plugin, Python `unittest`, PHP CLI, Playwright CLI, GoDaddy SFTP helper.

---

### Task 1: Lock the response contract with a regression test

**Files:**

- Create: `tests/test_sitewide_meta_tracking.py`
- Test: `tests/test_sitewide_meta_tracking.py`

- [ ] **Step 1: Write the failing test**

```python
def test_filter_replaces_google_and_legacy_meta_tracking_with_requested_pixel(self):
    transformed = transform(SAMPLE_DOCUMENT)
    self.assertIn("fbq('init', '1428464038973925');", transformed)
    self.assertEqual(transformed.count('connect.facebook.net/en_US/fbevents.js'), 1)
    self.assertNotIn('1558261907814968', transformed)
    self.assertNotIn('googletagmanager.com', transformed)
    self.assertNotIn('google-analytics.com', transformed)
    self.assertNotIn('/tracking.js', transformed)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_sitewide_meta_tracking -v`

Expected: FAIL because `npcwoods_tracking_rewrite_document()` does not exist.

### Task 2: Implement the one-site response filter

**Files:**

- Modify: `php/npcwoods-tracking.php`
- Test: `tests/test_sitewide_meta_tracking.py`

- [ ] **Step 1: Add the exact Pixel snippet and HTML response rewrite function**

```php
$html = preg_replace('/<script\b[^>]*>.*?googletagmanager\.com.*?<\/script>/is', '', $html);
$html = preg_replace('/<\/head\s*>/i', NPCWOODS_META_PIXEL_SNIPPET . "\n</head>", $html, 1);
```

- [ ] **Step 2: Start the output buffer before static route handlers**

```php
add_action('template_redirect', 'npcwoods_start_tracking_rewrite', 0);
function npcwoods_start_tracking_rewrite() {
    if (!is_admin()) ob_start('npcwoods_tracking_rewrite_document');
}
```

- [ ] **Step 3: Run test to verify it passes**

Run: `python3 -m unittest tests.test_sitewide_meta_tracking -v`

Expected: PASS.

- [ ] **Step 4: Check plugin syntax**

Run: `php -l php/npcwoods-tracking.php`

Expected: `No syntax errors detected`.

### Task 3: Prepare the unsent team email

**Files:**

- Create: `content-output/drafts/meta-pixel-payment-thank-you-email.md`

- [ ] **Step 1: Write the draft**

```text
Subject: Quick check: Meta Pixel on payment + thank-you pages

We’ve installed the new Meta PageView Pixel site-wide. Before we leave it on the payment and thank-you pages long-term, can you confirm whether you want it there or prefer those two pages excluded?

Please reply with: keep on both / exclude payment / exclude thank-you / exclude both.
```

### Task 4: Deploy and verify

**Files:**

- Modify: `php/npcwoods-tracking.php`

- [ ] **Step 1: Show the dry-run upload plan**

Run: `python3 scripts/sftp-upload.py php/npcwoods-tracking.php`

Expected: one upload target at `html/wp-content/mu-plugins/npcwoods-tracking.php` and no upload.

- [ ] **Step 2: Upload after the explicit approval in this thread**

Run: `python3 scripts/sftp-upload.py --execute --confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY" php/npcwoods-tracking.php`

Expected: one uploaded plugin and no secret values printed.

- [ ] **Step 3: Verify the live response and browser network on `/`, `/uti-treatment/`, `/pay/`, and `/thank-you/`**

Run: Playwright CLI at desktop and mobile sizes, inspecting network requests and response content.

Expected: each page has exactly one request for `fbevents.js`, uses ID `1428464038973925`, and has no Google/GTM/GA or prior Pixel requests.
