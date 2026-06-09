# Smart Content Integration Guide

> Where to add `data-npc-personalize` attributes in each landing page, based on the actual DOM structure found in the codebase.

---

## Quick Reference

| Attribute Value | What It Targets | API Field |
|---|---|---|
| `headline` | Hero `<h1>` | `data.headline` |
| `subheadline` | Hero subtitle `<p>` | `data.subheadline` |
| `trust-badge` | One trust pill in the hero | `data.trust_badge` |
| `social-proof` | Testimonial/social proof block | `data.social_proof` |
| `cta-text` | SMS CTA button text (multiple) | `data.cta_text` |

SMS body (`data.sms_body`) is applied automatically to ALL `a[href^="sms:"]` links on the page — no attribute needed.

---

## Page Pattern A: City-Specific Pages

Used by: `/uti-treatment/mesa-az/`, `/uti-treatment/scottsdale-az/`, and all city-level pages.

These pages use `.hero-inner` as the hero container, `.hero-sub` for the subtitle, `.cta-btn` for CTA buttons with SVG icons inside, and `.hero-trust > .pill` for trust pills.

### Before (current HTML)

```html
<section class="hero">
  <div class="hero-inner">
    <span class="hero-badge">
      <span class="hero-dot"></span>
      Licensed in Arizona · Same-day reply
    </span>
    <h1>UTI in Mesa? Text us and pick up your antibiotics <span>today.</span></h1>
    <p class="hero-sub">Burning, urgency, can't stop running to the bathroom...</p>
    <div class="hero-price">$59 flat · no hidden fees</div>
    <div class="hero-cta-row">
      <a href="sms:4806394722?body=..." class="cta-btn">
        <svg>...</svg>
        Text (480) 639-4722
      </a>
      <a href="#how-it-works" class="cta-btn-outline">How it works</a>
    </div>
    <div class="hero-trust">
      <span class="pill"><svg>...</svg> Licensed in AZ</span>
      <span class="pill"><svg>...</svg> Reply in under 1 hour</span>
      <span class="pill"><svg>...</svg> 50+ five-star reviews</span>
    </div>
  </div>
</section>
```

### After (with data attributes added)

```html
<section class="hero">
  <div class="hero-inner">
    <span class="hero-badge">
      <span class="hero-dot"></span>
      Licensed in Arizona · Same-day reply
    </span>
    <h1 data-npc-personalize="headline">UTI in Mesa? Text us and pick up your antibiotics <span>today.</span></h1>
    <p class="hero-sub" data-npc-personalize="subheadline">Burning, urgency, can't stop running to the bathroom...</p>
    <div class="hero-price">$59 flat · no hidden fees</div>
    <div class="hero-cta-row">
      <a href="sms:4806394722?body=..." class="cta-btn" data-npc-personalize="cta-text">
        <svg>...</svg>
        Text (480) 639-4722
      </a>
      <a href="#how-it-works" class="cta-btn-outline">How it works</a>
    </div>
    <div class="hero-trust">
      <span class="pill"><svg>...</svg> Licensed in AZ</span>
      <span class="pill"><svg>...</svg> Reply in under 1 hour</span>
      <span class="pill" data-npc-personalize="trust-badge"><svg>...</svg> 50+ five-star reviews</span>
    </div>
  </div>
</section>
```

### Also tag the final CTA section

```html
<section class="final-cta">
  <div class="final-cta-content">
    ...
    <div class="final-cta-buttons">
      <a href="sms:..." class="cta-btn" data-npc-personalize="cta-text">
        <svg>...</svg>
        Text (480) 639-4722
      </a>
      ...
    </div>
  </div>
</section>
```

### Optionally tag the mobile floating CTA

```html
<div class="mobile-floating-cta">
  <a href="sms:..." data-npc-personalize="cta-text">
    <svg>...</svg>
    Text Chris · $59
  </a>
</div>
```

Note: The mobile CTA text is typically shorter ("Text Chris · $59") and may not need personalization. If you want it personalized, add the attribute. If you prefer it to stay generic, leave it untagged.

### Where to add social-proof

Pattern A pages don't currently have a dedicated social-proof element. To enable it, add a new element in the hero section (after hero-trust) or in the scenario section:

```html
<!-- Option 1: Inside hero, after hero-trust -->
<div class="hero-trust">...</div>
<div data-npc-personalize="social-proof" style="margin-top: 20px; font-size: 0.95rem; color: var(--text-body); max-width: 580px; margin-left: auto; margin-right: auto; text-align: center; font-style: italic;"></div>

<!-- Option 2: As a standalone block between hero and scenario -->
<div data-npc-personalize="social-proof" class="container-narrow" style="padding: 20px 0; text-align: center; font-style: italic; color: var(--text-body);"></div>
```

The social-proof element starts empty and only gets content if the API returns a match. If no match, the empty div is invisible.

---

## Page Pattern B: Condition Hub Pages

Used by: `/strep-throat-treatment/`, `/dental-pain/`, `/ear-infection-treatment/`

These pages use `.hero-content` as the hero container, a plain `<p>` for the subtitle (no `.hero-sub` class), and `.hero-cta` for the CTA button (no SVG icon inside).

### Before

```html
<section class="hero">
  <div class="hero-content">
    <div class="hero-badge">$59 Flat. No Paperwork, No Waiting Room</div>
    <h1>Sore Throat That Won't Quit? Get Strep Antibiotics Sent to Your Pharmacy.</h1>
    <p>$59 flat, no paperwork, no hassle. No appointment. No video call...</p>
    <a href="sms:..." class="hero-cta">Text Us Now: (480) 639-4722</a>
  </div>
</section>
```

### After

```html
<section class="hero">
  <div class="hero-content">
    <div class="hero-badge">$59 Flat. No Paperwork, No Waiting Room</div>
    <h1 data-npc-personalize="headline">Sore Throat That Won't Quit? Get Strep Antibiotics Sent to Your Pharmacy.</h1>
    <p data-npc-personalize="subheadline">$59 flat, no paperwork, no hassle. No appointment. No video call...</p>
    <a href="sms:..." class="hero-cta" data-npc-personalize="cta-text">Text Us Now: (480) 639-4722</a>
  </div>
</section>
```

For Pattern B, the CTA has no SVG icon — the script's fallback logic handles this: when there are no child elements, it sets `textContent` directly on the `<a>`.

---

## Page Pattern C: Sinus Infection Page

The sinus page uses a different hero layout with `.hero-lede` instead of `.hero-sub`. Apply:

```html
<h1 data-npc-personalize="headline">Day 5-7 and still getting worse?</h1>
<p class="hero-lede" data-npc-personalize="subheadline">Text Chris your sinus pattern...</p>
```

---

## Adding the Script Tag

Add the script tag to each landing page HTML, right after the existing `tracking.js` line, before `</body>`:

```html
<!-- NPCWoods Tracking -->
<script src="/tracking.js?v=20260528-no-phi"></script>

<!-- NPCWoods Smart Content: dynamic headlines + social proof from Railway -->
<script src="/smart-content.js?v=20260531"></script>
```

The `?v=` query string is for cache-busting on updates. Bump the version when you deploy a new version of the script.

---

## Condition Map Reference

The script's `conditionMap` maps URL path segments to API condition keys. Here are all current condition pages:

| URL Path Segment | API Condition Key | Page |
|---|---|---|
| `uti-treatment` | `uti` | UTI hub + city pages |
| `uti-treatment-online` | `uti` | UTI comparison page |
| `sinus-infection-treatment` | `sinus` | Sinus hub |
| `strep-throat-treatment` | `strep` | Strep hub |
| `dental-pain` | `dental` | Dental hub |
| `ear-infection-treatment` | `ear-infection` | Ear infection hub |
| `ed-treatment` | `ed` | ED hub |
| `glp1-weight-loss` | `glp1` | GLP-1 hub |
| `poison-ivy` | `poison-ivy` | Poison ivy hub |

When adding a new condition page to the site, also add its slug to the `conditionMap` in `smart-content.js`.

---

## Rollout Order

Per the build plan, roll out one page at a time:

1. Add `data-npc-personalize` attributes to `/uti-treatment/mesa-az/` (Pattern A)
2. Add `<script src="/smart-content.js?v=20260531"></script>` after tracking.js
3. SFTP upload the modified HTML + the new smart-content.js to server root
4. Touch the WP page stub to bust GoDaddy cache
5. Verify with Playwright (with and without UTM params)
6. Monitor for 48 hours
7. Roll out to remaining pages

---

## What NOT to Tag

These elements should NOT get `data-npc-personalize` attributes:

- **Price elements** (`.hero-price`, "$59 flat") — price is always $59 and should never be dynamic
- **"How it works" links** — structural navigation, not content
- **Phone number links** (`tel:`) — always the same number
- **Footer content** — shared across all pages, not personalized
- **Header/nav** — shared component, not personalized
- **Schema/JSON-LD** — structured data stays static (matches the page's canonical content)

---

*Created: 2026-05-31 | Companion to smart-content.js and railway-smart-backend-plan.md*
