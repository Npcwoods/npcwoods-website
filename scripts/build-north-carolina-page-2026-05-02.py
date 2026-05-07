#!/usr/bin/env python3
"""
build-north-carolina-page-2026-05-02.py

Composes /landing-pages/north-carolina-telemedicine/index.html from:
  - Arizona's index.html (structural skeleton — sections, schema scaffold, nav, footer)
  - Mesa UTI's receipt-hero block (Inter 800 + JetBrains Mono receipt card, Variant C)
  - NC content dictionary below

Pattern: idempotent. Always reads from Arizona's pristine source. Never reads its own output.
Per feedback_idempotent_batch_script_pattern + feedback_splice_script_idempotency.
"""

from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parent.parent
ARIZONA = REPO / "landing-pages/arizona-telemedicine/index.html"
MESA    = REPO / "landing-pages/uti-treatment/mesa-az/index.html"
OUT_DIR = REPO / "landing-pages/north-carolina-telemedicine"
OUT     = OUT_DIR / "index.html"

# ---------------------------------------------------------------------------
# NC CONTENT DICTIONARY
# ---------------------------------------------------------------------------
# Murphy / Western NC anchor (Chris's chosen voice). Cities are state-wide so
# anyone landing from Charlotte or Raleigh search still feels addressed,
# but the personal voice references Western NC (where Chris lives).
# ---------------------------------------------------------------------------

NC = {
    "title":           "Same-Day Telemedicine in North Carolina: $59 | NPCWoods",
    "meta_desc":       "North Carolina telemedicine for $59. Text a licensed nurse practitioner. No paperwork, no waiting room. Prescriptions sent to your local NC pharmacy.",
    "og_title":        "Same-Day Telemedicine in North Carolina: $59 | NPCWoods",
    "og_desc":         "Text a licensed nurse practitioner in North Carolina for $59. $59 flat fee. No paperwork. Prescriptions sent to your local pharmacy.",
    "canonical":       "https://npcwoods.com/north-carolina-telemedicine/",

    "schema_desc":     "Text-based telehealth visits in North Carolina for $59. $59 flat fee. No paperwork. Licensed nurse practitioner.",
    "breadcrumb_text": "North Carolina Telemedicine",

    # Western NC anchor (Chris lives in Murphy, far western tip of NC)
    "hero_h1":         "UTI, sinus, strep in North Carolina? Here's the whole deal.",
    "hero_lede":       "Mission ER waits for hours. Urgent care closes at 8. Text Chris instead. Below is exactly what it costs and what happens, line by line.",
    "hero_cta_sms":    "sms:4806394722?body=Hi%2C%20I%20need%20a%20visit%20%E2%80%94%20I%27m%20in%20North%20Carolina",
    "receipt_head":    "NPCWoods Telemedicine &middot; Text Visit &middot; North Carolina",
    "receipt_pharmacy_line": "your NC pharmacy",
    "receipt_foot":    ('Generic antibiotic typically ~$8&ndash;$12 with GoodRx, paid at the pharmacy.<br>'
                        'Licensed in North Carolina &middot; NPI 1285125468 &middot; '
                        '<a href="https://www.ncbon.com/licensure-listing/license-verification/">ncbon.com verifiable</a>'),

    # NC cities — population centers + Western NC anchor towns
    "cities": [
        ("Charlotte", "Charlotte"),
        ("Raleigh", "Raleigh"),
        ("Greensboro", "Greensboro"),
        ("Durham", "Durham"),
        ("Winston-Salem", "Winston-Salem"),
        ("Asheville", "Asheville"),
        ("Wilmington", "Wilmington"),
        ("Fayetteville", "Fayetteville"),
        ("Boone", "Boone"),
        ("Murphy", "Murphy"),
    ],

    # NC Board of Nursing
    "bon_url":  "https://www.ncbon.com/licensure-listing/license-verification/",
    "bon_name": "North Carolina Board of Nursing",
}

# ---------------------------------------------------------------------------
# Receipt-hero CSS — copied verbatim from Mesa, only token names rewritten
# to match Arizona's existing CSS variable namespace.
#   Mesa --primary       -> Arizona --brand
#   Mesa --primary-hover -> Arizona --brand-hover
#   Mesa --warm-white    -> Arizona --off-white
#   Mesa --charcoal      -> Arizona --text-primary
#   Mesa --border-light  -> Arizona --border
# (No new tokens needed — every reference resolves against Arizona's :root.)
# ---------------------------------------------------------------------------

RECEIPT_HERO_CSS = """
/* ===== RECEIPT HERO (audit 2026-05-01, variant C) ===== */
.hero-receipt {
  background: var(--off-white);
  padding: 5rem 2rem 6rem;
  border-bottom: 1px solid var(--border);
}
.hero-receipt-grid {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}
.hero-receipt-copy h1 {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-weight: 800;
  font-size: clamp(2.4rem, 5vw, 3.6rem);
  line-height: 1.04;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin: 0 0 1.5rem;
}
.hero-receipt-copy .lede {
  font-size: 1.1rem;
  color: var(--text-body);
  max-width: 46ch;
  margin: 0 0 2rem;
  line-height: 1.6;
}
.hero-receipt-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--brand);
  color: #fff !important;
  font-weight: 600;
  font-size: 1rem;
  padding: 18px 32px;
  border-radius: 100px;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.30);
  transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}
.hero-receipt-cta:hover {
  background: var(--brand-hover);
  color: #fff !important;
  text-decoration: none;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.40);
}
.receipt {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 2rem 1.75rem;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.06);
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.92rem;
  color: var(--text-primary);
  line-height: 1.8;
}
.receipt-head {
  text-align: center;
  padding-bottom: 1.25rem;
  border-bottom: 1px dashed var(--border);
  margin-bottom: 1.25rem;
  font-size: 0.78rem;
  color: var(--text-muted);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.receipt-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 4px 0;
  gap: 1rem;
}
.receipt-row .label { color: var(--text-body); }
.receipt-row .val {
  color: var(--text-primary);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  text-align: right;
}
.receipt-rule {
  border: none;
  border-top: 1px dashed var(--border);
  margin: 0.875rem 0;
}
.receipt-total .label,
.receipt-total .val {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}
.receipt-foot {
  margin-top: 1.25rem;
  padding-top: 1.125rem;
  border-top: 1px dashed var(--border);
  font-size: 0.74rem;
  color: var(--text-muted);
  text-align: center;
  letter-spacing: 0.04em;
  line-height: 1.6;
}
.receipt-foot a { color: inherit; text-decoration: underline; }
@media (max-width: 780px) {
  .hero-receipt-grid {
    grid-template-columns: 1fr;
    gap: 2.25rem;
  }
  .hero-receipt {
    padding: 3.5rem 1.5rem 4rem;
  }
  .receipt {
    padding: 1.5rem 1.25rem;
  }
  .hero-receipt-cta {
    width: 100%;
    justify-content: center;
  }
}
""".strip()


def receipt_hero_html() -> str:
    """The HTML markup that replaces Arizona's old <section class='hero'> block."""
    return f"""<!-- HERO (Receipt Hero, audit 2026-05-01 variant C) -->
<section class="hero-receipt">
  <div class="hero-receipt-grid">
    <div class="hero-receipt-copy">
      <h1>{NC['hero_h1']}</h1>
      <p class="lede">{NC['hero_lede']}</p>
      <a href="{NC['hero_cta_sms']}" class="hero-receipt-cta">Start my $59 visit &nbsp;&rarr;</a>
    </div>
    <div class="receipt" aria-label="What a text visit at NPCWoods costs and includes">
      <div class="receipt-head">{NC['receipt_head']}</div>
      <div class="receipt-row"><span class="label">Visit, async, NP review</span><span class="val">$59.00</span></div>
      <div class="receipt-row"><span class="label">Co-pay</span><span class="val">$0.00</span></div>
      <div class="receipt-row"><span class="label">Membership fee</span><span class="val">$0.00</span></div>
      <div class="receipt-row"><span class="label">Surprise bills</span><span class="val">none</span></div>
      <hr class="receipt-rule">
      <div class="receipt-row"><span class="label">Reply, biz hours</span><span class="val">&lt; 1 hour</span></div>
      <div class="receipt-row"><span class="label">Reviewed by</span><span class="val">Chris Woods, NP</span></div>
      <div class="receipt-row"><span class="label">Script sent to</span><span class="val">{NC['receipt_pharmacy_line']}</span></div>
      <hr class="receipt-rule">
      <div class="receipt-row receipt-total"><span class="label">Total today</span><span class="val">$59.00</span></div>
      <div class="receipt-foot">
        {NC['receipt_foot']}
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# TRANSFORMS
# ---------------------------------------------------------------------------

def update_head(html: str) -> str:
    # title
    html = re.sub(
        r"<title>[^<]*</title>",
        f"<title>{NC['title']}</title>",
        html, count=1,
    )
    # meta description (first occurrence — the one in <head>)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{NC["meta_desc"]}">',
        html, count=1,
    )
    # OG title / desc / url
    html = html.replace(
        '<meta property="og:title" content="Same-Day Telemedicine in Arizona: $59 | NPCWoods">',
        f'<meta property="og:title" content="{NC["og_title"]}">',
    )
    html = html.replace(
        '<meta property="og:description" content="Text a licensed nurse practitioner in Arizona for $59. $59 flat fee. No paperwork. Prescriptions sent to your local pharmacy.">',
        f'<meta property="og:description" content="{NC["og_desc"]}">',
    )
    html = html.replace(
        '<meta property="og:url" content="https://npcwoods.com/arizona-telemedicine/">',
        f'<meta property="og:url" content="{NC["canonical"]}">',
    )
    # canonical + cite-as
    html = html.replace(
        '<link rel="canonical" href="https://npcwoods.com/arizona-telemedicine/">',
        f'<link rel="canonical" href="{NC["canonical"]}">',
    )
    html = html.replace(
        '<link rel="cite-as" href="https://npcwoods.com/arizona-telemedicine/">',
        f'<link rel="cite-as" href="{NC["canonical"]}">',
    )

    # Add JetBrains Mono font right after the existing Inter font link.
    # Idempotency-safe: only inject if not already present.
    if "JetBrains+Mono" not in html:
        inter_line = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" media="print" onload="this.media=\'all\'">'
        jb_line = (
            '\n  <!-- Receipt hero monospace (variant C) -->\n'
            '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" media="print" onload="this.media=\'all\'">\n'
            '  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap"></noscript>'
        )
        if inter_line in html:
            html = html.replace(inter_line, inter_line + jb_line, 1)
        else:
            # Defensive fallback — bail loudly so we don't silently skip the font
            raise RuntimeError("Could not find Inter font link to anchor JetBrains Mono injection")

    return html


def update_schema(html: str) -> str:
    # MedicalBusiness schema
    html = html.replace(
        '"url": "https://npcwoods.com/arizona-telemedicine/",',
        f'"url": "{NC["canonical"]}",',
    )
    html = html.replace(
        '"description": "Text-based telehealth visits in Arizona for $59. $59 flat fee. No paperwork. Licensed nurse practitioner.",',
        f'"description": "{NC["schema_desc"]}",',
    )
    html = html.replace(
        '"areaServed": {\n    "@type": "State",\n    "name": "Arizona"\n  }',
        '"areaServed": {\n    "@type": "State",\n    "name": "North Carolina"\n  }',
    )
    # BreadcrumbList
    html = html.replace(
        '{"@type": "ListItem", "position": 2, "name": "Arizona Telemedicine", "item": "https://npcwoods.com/arizona-telemedicine/"}',
        f'{{"@type": "ListItem", "position": 2, "name": "{NC["breadcrumb_text"]}", "item": "{NC["canonical"]}"}}',
    )
    return html


def inject_receipt_hero_css(html: str) -> str:
    """Append receipt-hero CSS to the main <style> block. Idempotent — bails if already present."""
    if "RECEIPT HERO (audit 2026-05-01" in html:
        return html
    # Anchor: the line right before .npc-nav opens, which is the first ===== SITE NAV ===== marker.
    # Insert receipt-hero CSS just before it so it lives near the top of the global stylesheet.
    anchor = "/* ===== SITE NAV ===== */"
    if anchor not in html:
        raise RuntimeError("Could not find SITE NAV anchor to inject receipt-hero CSS")
    return html.replace(anchor, RECEIPT_HERO_CSS + "\n\n" + anchor, 1)


def replace_hero_section(html: str) -> str:
    """Replace Arizona's old <section class='hero'>...</section> with the receipt-hero markup."""
    pattern = re.compile(
        r"<!-- HERO -->\s*<section class=\"hero\">.*?</section>",
        re.DOTALL,
    )
    if not pattern.search(html):
        raise RuntimeError("Could not locate Arizona's old hero section to replace")
    return pattern.sub(receipt_hero_html(), html, count=1)


def replace_cities_grid(html: str) -> str:
    """Swap the Arizona cities grid for NC cities. Anchored on the cities <section> wrapper."""
    cities_html = "\n      ".join(
        f'<a href="{NC["canonical"]}" class="city-link">{label}</a>'
        for _, label in NC["cities"]
    )
    new_section = (
        f'<section class="cities fade-in">\n'
        f'  <div class="container">\n'
        f'    <div class="section-label">Cities We Serve</div>\n'
        f'    <h2 class="section-title">Telehealth across North Carolina</h2>\n'
        f'    <p style="text-align:center; margin-bottom: 32px; max-width: 540px; margin-left: auto; margin-right: auto;">'
        f'We serve patients across all of North Carolina, from the Outer Banks to the Smoky Mountains. '
        f'Chris lives in Murphy in the far west, so the Asheville/Boone/Hendersonville corridor gets a '
        f'little extra love. But whether you text from Charlotte, Raleigh, or anywhere else in the state, '
        f'you reach the same person.</p>\n'
        f'    <div class="city-grid">\n      {cities_html}\n    </div>\n'
        f'  </div>\n'
        f'</section>'
    )
    pattern = re.compile(
        r'<section class="cities fade-in">.*?</section>',
        re.DOTALL,
    )
    if not pattern.search(html):
        raise RuntimeError("Could not locate cities section to replace")
    return pattern.sub(new_section, html, count=1)


def update_cross_links(html: str) -> str:
    """In the 'Licensed in 11 states' grid, swap out 'North Carolina' (this page) and add 'Arizona'."""
    # Remove the NC self-link
    html = html.replace(
        '<a href="https://npcwoods.com/north-carolina-telemedicine/" class="cross-link">North Carolina</a>\n      ',
        '',
    )
    # Add Arizona link at the top of the cross-link grid (alphabetical order: comes first)
    html = html.replace(
        '<div class="cross-links-grid">\n      <a href="https://npcwoods.com/colorado-telemedicine/"',
        '<div class="cross-links-grid">\n      <a href="https://npcwoods.com/arizona-telemedicine/" class="cross-link">Arizona</a>\n      <a href="https://npcwoods.com/colorado-telemedicine/"',
    )
    return html


def update_body_copy(html: str) -> str:
    """Targeted text replacements for state name, board of nursing, pharmacy chains, etc."""

    # Breadcrumb visible text
    html = html.replace(
        "<a href=\"https://npcwoods.com/\">Home</a> &rsaquo; Arizona Telemedicine",
        f'<a href="https://npcwoods.com/">Home</a> &rsaquo; {NC["breadcrumb_text"]}',
    )

    # How It Works pharmacy mention — Arizona-specific chains -> NC chains
    html = html.replace(
        "any pharmacy in Arizona: CVS, Walgreens, Fry's, Costco, wherever is closest.",
        "any pharmacy in North Carolina: CVS, Walgreens, Walmart, Ingles (Western NC), Harris Teeter, wherever is closest.",
    )

    # "double board-certified Family Nurse Practitioner licensed in Arizona"
    html = html.replace(
        "double board-certified Family Nurse Practitioner licensed in Arizona",
        "double board-certified Family Nurse Practitioner licensed in North Carolina",
    )

    # CONDITIONS section header + intro paragraph
    html = html.replace(
        '<h2 class="section-title">Common conditions we treat in Arizona</h2>',
        '<h2 class="section-title">Common conditions we treat in North Carolina</h2>',
    )
    html = html.replace(
        "Living in Arizona means dealing with dry sinuses, heat-related illness, and those late-night infections that can't wait until morning. Whether you're a year-round resident or a snowbird spending the winter here, we've got you covered.",
        "Living in North Carolina means humid summers, fall allergens that flare sinuses, and those late-night infections that can't wait until morning. From the coast to the mountains, whether you're in Charlotte, Asheville, or Murphy, we've got you covered.",
    )

    # BOTTOM CTA
    html = html.replace(
        "Most Arizona patients hear back within a few hours.",
        "Most North Carolina patients hear back within a few hours.",
    )

    # HERO badge "Licensed in Arizona" — no longer present (we replaced the hero).
    # The Arizona Board of Nursing reference doesn't appear in Arizona's body
    # (it's not in the visible text), but we'll be defensive if it shows up later:
    html = html.replace(
        "https://www.azbn.gov/verify-a-license",
        NC["bon_url"],
    )
    html = html.replace("Arizona Board of Nursing", NC["bon_name"])

    # Footer "Affordable Care" link points to an Arizona-specific URL
    # (/affordable-telemedicine-arizona-no-insurance/). Remove that <li> from
    # the NC page footer — there's no NC equivalent yet, and pointing NC
    # visitors at an AZ-only page is jarring. The /pricing/ link the line
    # above it covers the same intent.
    html = re.sub(
        r'\s*<li><a href="https://npcwoods\.com/affordable-telemedicine-arizona-no-insurance/">[^<]*</a></li>',
        '',
        html, count=1,
    )

    # No catch-all "Arizona" -> "North Carolina" replacement here. Every body
    # mention of "Arizona" that should change has an explicit replacement above.
    # The remaining "Arizona" occurrences are nav/footer LINKS to the actual
    # Arizona page (e.g., the States dropdown, the cross-link grid) — those
    # must keep both their href AND their visible text. A blanket regex
    # quietly broke them on the first attempt; specificity wins.

    return html


def banned_word_check(html: str) -> list:
    """Return a list of banned-word violations in title and meta description (head only)."""
    # Extract <title> and the FIRST <meta name="description"> from <head>.
    head_match = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    head = head_match.group(1) if head_match else html[:5000]

    title_m = re.search(r"<title>([^<]*)</title>", head, re.IGNORECASE)
    desc_m  = re.search(r'<meta name="description" content="([^"]*)"', head, re.IGNORECASE)
    title = title_m.group(1) if title_m else ""
    desc  = desc_m.group(1) if desc_m else ""

    targets = {"title": title, "meta_description": desc}
    banned_in_head = [
        r"\bdoctor\b",
        r"\binsurance\b",
        r"\bappointment\b",
        r"text a doctor",
    ]
    # "board-certified" without preceding "double " — negative lookbehind
    banned_in_head.append(r"(?<!double )\bboard[- ]certified\b")

    violations = []
    for field, text in targets.items():
        for pat in banned_in_head:
            if re.search(pat, text, re.IGNORECASE):
                violations.append(f"{field} contains banned pattern /{pat}/: {text!r}")

    # Body-wide check: never the literal phrase "Text a Doctor" anywhere
    if re.search(r"text a doctor", html, re.IGNORECASE):
        violations.append('Body contains banned phrase "Text a Doctor"')
    # Body-wide check: never the word "doctor" anywhere on NPCWoods (per feedback_no_doctor)
    if re.search(r"\bdoctor\b", html, re.IGNORECASE):
        violations.append('Body contains the word "doctor" — banned site-wide on npcwoods.com')

    return violations


def main():
    if not ARIZONA.exists():
        print(f"[FATAL] Arizona source missing: {ARIZONA}", file=sys.stderr)
        sys.exit(2)
    if not MESA.exists():
        print(f"[FATAL] Mesa source missing: {MESA}", file=sys.stderr)
        sys.exit(2)

    print(f"[1/7] Reading Arizona source: {ARIZONA}")
    az = ARIZONA.read_text(encoding="utf-8")
    az_size = len(az)
    print(f"      Arizona: {az_size:,} bytes, {az.count(chr(10))} lines")

    print("[2/7] Updating <head> (title, meta, canonical, OG, fonts)")
    out = update_head(az)

    print("[3/7] Updating schema (MedicalBusiness, BreadcrumbList)")
    out = update_schema(out)

    print("[4/7] Injecting receipt-hero CSS into stylesheet")
    out = inject_receipt_hero_css(out)

    print("[5/7] Replacing old hero section with receipt-hero markup")
    out = replace_hero_section(out)

    print("[6/7] Localizing cities, cross-links, and body copy for NC")
    out = replace_cities_grid(out)
    out = update_cross_links(out)
    out = update_body_copy(out)

    # 30%-shrink guard (per feedback_safe_html_block_replace)
    out_size = len(out)
    if out_size < az_size * 0.70:
        print(f"[FATAL] Output is {out_size:,} bytes, Arizona was {az_size:,}.", file=sys.stderr)
        print(f"        Shrinkage > 30% — refusing to write.", file=sys.stderr)
        sys.exit(3)

    # Banned-word self-check
    print("[7/7] Banned-word self-check (title, meta, body)")
    violations = banned_word_check(out)
    if violations:
        print("[FATAL] Banned-word violations detected:", file=sys.stderr)
        for v in violations:
            print(f"        - {v}", file=sys.stderr)
        sys.exit(4)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding="utf-8")
    print(f"\n[OK] Wrote {OUT}")
    print(f"     {out_size:,} bytes, {out.count(chr(10))} lines")
    print(f"     Arizona was {az_size:,} bytes ({(out_size/az_size - 1)*100:+.1f}%)")
    print()
    print("Next steps:")
    print(f"  1. Open in browser:  open {OUT}")
    print(f"  2. Add route to:     php/npcwoods-static-pages.php")
    print(f"  3. Cache-bust verify after deploy:  curl 'https://npcwoods.com/north-carolina-telemedicine/?v=$(date +%s)'")


if __name__ == "__main__":
    main()
