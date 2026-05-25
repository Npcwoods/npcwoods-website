#!/usr/bin/env python3
"""Apply Receipt Hero pattern + anti-slop pass to UTI city pages.

Cities: surprise-az, scottsdale-az, albuquerque-nm
Pattern from: mocks audit 2026-05-01 variant C, applied to mesa-az earlier today.

Idempotent: reads from <file>.pre-receipt-2026-05-01.bak (creates on first run).
Reads pristine source per the splice-script lesson, never re-reads target.

Per-page steps:
  1. Backup pristine source on first run
  2. Read backup
  3. Strip em dashes (regex: collapse \\s*[—|&mdash;]\\s* -> ". ")
  4. Replace known stuck-phrase tics
  5. Replace <section class="hero" id="hero">...</section> with receipt hero
  6. Add Inter 800 + JetBrains Mono font import
  7. Inject Receipt Hero CSS before main </style>
  8. Validate: no banned words, size shrink < 30%
  9. Write to target
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP_SUFFIX = ".pre-receipt-2026-05-01.bak"

CITIES = [
    {
        "dir": "surprise-az",
        "city": "Surprise",
        "state": "AZ",
        "state_full": "Arizona",
        "verify_url": "https://www.azbn.gov/verify-a-license",
        "verify_text": "azbn.gov verifiable",
        "sms_body": "Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Surprise",
        "lede": "Urgent care on Bell Road is closed. Banner Del E. Webb's ER has a waiting room of people way sicker than you. Text us instead. Below is exactly what it costs and what happens, line by line.",
        "pharmacy_phrase": "your Surprise pharmacy",
    },
    {
        "dir": "scottsdale-az",
        "city": "Scottsdale",
        "state": "AZ",
        "state_full": "Arizona",
        "verify_url": "https://www.azbn.gov/verify-a-license",
        "verify_text": "azbn.gov verifiable",
        "sms_body": "Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Scottsdale",
        "lede": "Urgent care on Shea is closed. HonorHealth Osborn is a three-hour wait. Text us instead. Below is exactly what it costs and what happens, line by line.",
        "pharmacy_phrase": "your Scottsdale pharmacy",
    },
    {
        "dir": "albuquerque-nm",
        "city": "Albuquerque",
        "state": "NM",
        "state_full": "New Mexico",
        "verify_url": "https://npiregistry.cms.hhs.gov/provider-view/1285125468",
        "verify_text": "NPI verifiable",
        "sms_body": "Hi%2C%20I%20need%20help%20with%20a%20UTI%20in%20Albuquerque",
        "lede": "Don't sit in the UNM ER for three hours. Don't wait until your urgent care opens tomorrow. Text us instead. Below is exactly what it costs and what happens, line by line.",
        "pharmacy_phrase": "your Albuquerque pharmacy",
    },
]

# Known AI-tic phrases — any that don't match in a given file are silently skipped.
STUCK_REPS = [
    ("Three Texts. That's It.", "Three texts."),
    ("Three Texts.  That's It.", "Three texts."),
    ("Be Honest With Yourself: Is This Just a UTI?", "Is this actually a UTI?"),
    ("Be Honest With Yourself. Is This Just a UTI?", "Is this actually a UTI?"),
    ("Over 50 Five Star Ratings", "More than 50 five-star reviews"),
    ('<div class="hero-badge">$59 flat fee &bull; No paperwork, no hassle</div>',
     ''),  # hero badge dropped — receipt itself carries the price/no-strings message
    ('<span class="hero-price">$59 flat. no paperwork, no hassle.</span>', ''),
    ('<span class="hero-price">$59 flat &mdash; no paperwork, no hassle.</span>', ''),
]

HERO_RE = re.compile(r'<section class="hero"(?: id="hero")?>.*?</section>', re.DOTALL)

OLD_FONT_NOSCRIPT = (
    '  <noscript><link rel="stylesheet" '
    'href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700'
    '&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700'
    '&family=DM+Serif+Display:ital@0;1'
    '&family=Inter:wght@400;500;600;700&display=swap"></noscript>'
)

NEW_FONT_BLOCK = OLD_FONT_NOSCRIPT + (
    '\n  <!-- Receipt hero: Inter 800 + JetBrains Mono (audit 2026-05-01 variant C) -->'
    '\n  <link rel="stylesheet" '
    'href="https://fonts.googleapis.com/css2?family=Inter:wght@800'
    '&family=JetBrains+Mono:wght@400;500;600&display=swap">'
)

RECEIPT_CSS = """
    /* ===== RECEIPT HERO (audit 2026-05-01, variant C) ===== */
    .hero-receipt { background: var(--warm-white); padding: 5rem 2rem 6rem; border-bottom: 1px solid var(--border-light); }
    .hero-receipt-grid { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }
    .hero-receipt-copy h1 { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 800; font-size: clamp(2.4rem, 5vw, 3.6rem); line-height: 1.04; letter-spacing: -0.03em; color: var(--charcoal); margin: 0 0 1.5rem; }
    .hero-receipt-copy .lede { font-size: 1.1rem; color: var(--text-body); max-width: 46ch; margin: 0 0 2rem; line-height: 1.6; }
    .hero-receipt-cta { display: inline-flex; align-items: center; gap: 10px; background: var(--primary); color: #fff !important; font-weight: 600; font-size: 1rem; padding: 18px 32px; border-radius: 100px; text-decoration: none; box-shadow: 0 4px 16px rgba(37, 99, 235, 0.30); transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease; }
    .hero-receipt-cta:hover { background: var(--primary-hover); color: #fff !important; text-decoration: none; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(37, 99, 235, 0.40); }
    .receipt { background: var(--white); border: 1px solid var(--border-light); border-radius: 8px; padding: 2rem 1.75rem; box-shadow: 0 12px 36px rgba(0, 0, 0, 0.06); font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.92rem; color: var(--charcoal); line-height: 1.8; }
    .receipt-head { text-align: center; padding-bottom: 1.25rem; border-bottom: 1px dashed var(--border-light); margin-bottom: 1.25rem; font-size: 0.78rem; color: var(--text-muted); letter-spacing: 0.16em; text-transform: uppercase; }
    .receipt-row { display: flex; justify-content: space-between; align-items: baseline; padding: 4px 0; gap: 1rem; }
    .receipt-row .label { color: var(--text-body); }
    .receipt-row .val { color: var(--charcoal); font-weight: 600; font-variant-numeric: tabular-nums; text-align: right; }
    .receipt-rule { border: none; border-top: 1px dashed var(--border-light); margin: 0.875rem 0; }
    .receipt-total .label, .receipt-total .val { font-size: 1.05rem; font-weight: 700; color: var(--charcoal); }
    .receipt-foot { margin-top: 1.25rem; padding-top: 1.125rem; border-top: 1px dashed var(--border-light); font-size: 0.74rem; color: var(--text-muted); text-align: center; letter-spacing: 0.04em; line-height: 1.6; }
    .receipt-foot a { color: inherit; text-decoration: underline; }
    @media (max-width: 780px) {
      .hero-receipt-grid { grid-template-columns: 1fr; gap: 2.25rem; }
      .hero-receipt { padding: 3.5rem 1.5rem 4rem; }
      .receipt { padding: 1.5rem 1.25rem; }
      .hero-receipt-cta { width: 100%; justify-content: center; }
    }
"""

CSS_ANCHOR = """    /* Schema markup (hidden) */
    script[type="application/ld+json"] {
      display: none;
    }
  </style>"""

CSS_ANCHOR_NEW = (
    """    /* Schema markup (hidden) */
    script[type="application/ld+json"] {
      display: none;
    }
"""
    + RECEIPT_CSS
    + "  </style>"
)

BANNED = ["Text a Doctor", "text a doctor"]


def receipt_hero_html(c):
    return f"""<!-- ===== HERO SECTION (Receipt Hero, audit 2026-05-01 variant C) ===== -->
<section class="hero-receipt">
  <div class="hero-receipt-grid">
    <div class="hero-receipt-copy">
      <h1>Got a UTI in {c["city"]}? Here's the whole deal.</h1>
      <p class="lede">{c["lede"]}</p>
      <a href="sms:4806394722?body={c["sms_body"]}" class="hero-receipt-cta">Start my $59 visit &nbsp;&rarr;</a>
    </div>
    <div class="receipt" aria-label="What a UTI visit at NPCWoods costs and includes">
      <div class="receipt-head">NPCWoods Telemedicine &middot; UTI Visit &middot; {c["city"]} {c["state"]}</div>
      <div class="receipt-row"><span class="label">Visit, async, NP review</span><span class="val">$59.00</span></div>
      <div class="receipt-row"><span class="label">Co-pay</span><span class="val">$0.00</span></div>
      <div class="receipt-row"><span class="label">Membership fee</span><span class="val">$0.00</span></div>
      <div class="receipt-row"><span class="label">Surprise bills</span><span class="val">none</span></div>
      <hr class="receipt-rule">
      <div class="receipt-row"><span class="label">Reply, biz hours</span><span class="val">&lt; 1 hour</span></div>
      <div class="receipt-row"><span class="label">Reviewed by</span><span class="val">Chris Woods, NP</span></div>
      <div class="receipt-row"><span class="label">Script sent to</span><span class="val">{c["pharmacy_phrase"]}</span></div>
      <hr class="receipt-rule">
      <div class="receipt-row receipt-total"><span class="label">Total today</span><span class="val">$59.00</span></div>
      <div class="receipt-foot">
        Generic UTI antibiotic typically ~$8 with GoodRx, paid at the pharmacy.<br>
        Licensed in {c["state_full"]} &middot; NPI 1285125468 &middot; <a href="{c["verify_url"]}">{c["verify_text"]}</a>
      </div>
    </div>
  </div>
</section>"""


def transform(src, c):
    out = src

    # 1. Em dash strip (collapse surrounding whitespace)
    out = re.sub(r"\s*&mdash;\s*", ". ", out)
    out = re.sub(r"\s*—\s*", ". ", out)

    # 2. Stuck phrases — silently skip misses
    for old, new in STUCK_REPS:
        if old in out:
            out = out.replace(old, new)

    # 3. Hero swap
    new_hero = receipt_hero_html(c)
    out, n_hero = HERO_RE.subn(new_hero, out, count=1)
    if n_hero == 0:
        raise RuntimeError(f"hero block <section class=\"hero\" id=\"hero\"> not found")

    # 4. Font import
    if OLD_FONT_NOSCRIPT in out:
        out = out.replace(OLD_FONT_NOSCRIPT, NEW_FONT_BLOCK, 1)
    else:
        # Soft warning — most pages share this exact string
        print(f"[warn] {c['dir']}: noscript font link not found; JetBrains Mono not added", file=sys.stderr)

    # 5. Receipt CSS injection
    if CSS_ANCHOR in out:
        out = out.replace(CSS_ANCHOR, CSS_ANCHOR_NEW, 1)
    else:
        print(f"[warn] {c['dir']}: CSS anchor not found; receipt CSS not injected", file=sys.stderr)

    return out


def main():
    failures = []
    for c in CITIES:
        target = ROOT / "landing-pages" / "uti-treatment" / c["dir"] / "index.html"
        if not target.exists():
            print(f"[FAIL] {c['dir']}: target not found {target}", file=sys.stderr)
            failures.append(c["dir"])
            continue

        backup = target.parent / (target.name + BACKUP_SUFFIX)
        if not backup.exists():
            shutil.copy2(target, backup)
            print(f"[backup] created {backup.name}")

        src = backup.read_text()
        try:
            out = transform(src, c)
        except Exception as e:
            print(f"[FAIL] {c['dir']}: {e}", file=sys.stderr)
            failures.append(c["dir"])
            continue

        # Validation: banned words
        bad = next((w for w in BANNED if w in out), None)
        if bad:
            print(f"[FAIL] {c['dir']}: banned word present: {bad!r}", file=sys.stderr)
            failures.append(c["dir"])
            continue

        # Validation: size sanity
        size_before = len(src)
        size_after = len(out)
        shrink_pct = (size_before - size_after) / size_before * 100
        if shrink_pct > 30:
            print(f"[FAIL] {c['dir']}: shrink {shrink_pct:.1f}% > 30%", file=sys.stderr)
            failures.append(c["dir"])
            continue

        # Validation: receipt landed
        if "hero-receipt-grid" not in out or "receipt-row" not in out:
            print(f"[FAIL] {c['dir']}: receipt markers missing post-transform", file=sys.stderr)
            failures.append(c["dir"])
            continue

        target.write_text(out)
        em_count = out.count("&mdash;") + out.count("—")
        print(
            f"[ok] {c['dir']}: {size_before} -> {size_after} "
            f"({(size_after - size_before) / size_before * 100:+.1f}%), em-dashes remaining: {em_count}"
        )

    if failures:
        print(f"\n{len(failures)} failure(s): {failures}", file=sys.stderr)
        sys.exit(1)
    print("\nall city pages transformed successfully")


if __name__ == "__main__":
    main()
