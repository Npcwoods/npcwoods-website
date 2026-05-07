#!/usr/bin/env python3
"""
Impeccable clarify pass — 2026-04-30

Reads each target file from its pre-impeccable backup, applies ordered
(old, new) replacements, writes the result to the live file. Idempotent
because we always read from the pristine backup, never the live file.

Targets:
  1. homepage/page-npcwoods-home.php — em-dash sweep + 3 bare "Board Certified"
  2. landing-pages/arizona-telemedicine/index.html — em-dash sweep + 1 bare "board-certified"

CSS/JS/HTML comments containing em-dashes are intentionally NOT replaced —
they are not user-facing.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # npcwoods-website/
BAK_SUFFIX = ".pre-impeccable-2026-04-30.bak"


def apply(path: Path, replacements: list[tuple[str, str]], strict: bool = True) -> int:
    """Read from <path><BAK_SUFFIX>, apply replacements in order, write to <path>."""
    bak = path.with_suffix(path.suffix + BAK_SUFFIX) if False else Path(str(path) + BAK_SUFFIX)
    if not bak.exists():
        sys.exit(f"FATAL: backup missing — {bak}")
    src = bak.read_text(encoding="utf-8")
    out = src
    misses = 0
    for old, new in replacements:
        if old not in out:
            misses += 1
            print(f"  MISS  in {path.name}: {old[:80]!r}")
            if strict:
                continue
        else:
            count = out.count(old)
            out = out.replace(old, new)
            print(f"  ok ({count}×) {old[:60]!r}  →  {new[:60]!r}")
    path.write_text(out, encoding="utf-8")
    return misses


# -----------------------------------------------------------------------------
# 1. HOMEPAGE — homepage/page-npcwoods-home.php
# -----------------------------------------------------------------------------
HOMEPAGE = ROOT / "homepage" / "page-npcwoods-home.php"

homepage_edits: list[tuple[str, str]] = [
    # ---- Meta tags (4) -------------------------------------------------------
    (
        '<meta name="description" content="NPCWoods Telemedicine — $59 text-based urgent care from a licensed Nurse Practitioner. No hassle, no waiting rooms. Same-day response. Text (480) 639-4722.">',
        '<meta name="description" content="NPCWoods Telemedicine, $59 text-based urgent care from a licensed Nurse Practitioner. No hassle, no waiting rooms. Same-day response. Text (480) 639-4722.">',
    ),
    (
        '<title>NPCWoods Telemedicine — $59 Online Urgent Care | No Hassle</title>',
        '<title>NPCWoods Telemedicine: $59 Online Urgent Care | No Hassle</title>',
    ),
    (
        '<meta property="og:description" content="See a real Nurse Practitioner from home — $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.">',
        '<meta property="og:description" content="See a real Nurse Practitioner from home. $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.">',
    ),
    (
        '<meta name="twitter:description" content="See a real Nurse Practitioner from home — $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.">',
        '<meta name="twitter:description" content="See a real Nurse Practitioner from home. $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.">',
    ),
    # ---- Schema.org descriptions (4) -----------------------------------------
    (
        '"description": "Text-based asynchronous telemedicine from a double board-certified Nurse Practitioner. $59 flat fee per visit — no paperwork, no hidden fees. Same-day prescriptions for UTIs, sinus infections, strep throat, dental pain, ED, and 18+ conditions across 11 states.",',
        '"description": "Text-based asynchronous telemedicine from a double board-certified Nurse Practitioner. $59 flat fee per visit, no paperwork, no hidden fees. Same-day prescriptions for UTIs, sinus infections, strep throat, dental pain, ED, and 18+ conditions across 11 states.",',
    ),
    (
        '"description": "Chris Woods is a double board-certified Nurse Practitioner and the founder of NPCWoods Telemedicine. He personally reviews every patient case — no AI, no chatbot, no algorithm.",',
        '"description": "Chris Woods is a double board-certified Nurse Practitioner and the founder of NPCWoods Telemedicine. He personally reviews every patient case. No AI, no chatbot, no algorithm.",',
    ),
    (
        '"description": "Text-based urgent care visit with a double board-certified Nurse Practitioner. No video call required. Text your symptoms, get a diagnosis and prescription sent to your pharmacy — usually same day.",',
        '"description": "Text-based urgent care visit with a double board-certified Nurse Practitioner. No video call required. Text your symptoms, get a diagnosis and prescription sent to your pharmacy, usually same day.",',
    ),
    (
        '"name": "NPCWoods Telemedicine — $59 Online Urgent Care",',
        '"name": "NPCWoods Telemedicine: $59 Online Urgent Care",',
    ),
    # ---- Nav + slide-panel CTA labels (3) ------------------------------------
    (
        '<a href="sms:4806394722" class="npc-nav-cta">$59 &mdash; Text Us</a>',
        '<a href="sms:4806394722" class="npc-nav-cta">$59 · Text Us</a>',
    ),
    (
        '<div class="npc-panel-link-text">About Chris<div class="npc-panel-link-sub">MSN, FNP-C &mdash; Board Certified</div></div>',
        '<div class="npc-panel-link-text">About Chris<div class="npc-panel-link-sub">MSN, FNP-C · Double Board-Certified</div></div>',
    ),
    (
        '        Text Chris &mdash; Start My $59 Visit',
        '        Text Chris · Start My $59 Visit',
    ),
    # ---- Hero lede (1) -------------------------------------------------------
    (
        '<p class="lede">Text your symptoms to a double board-certified Nurse Practitioner. Get evaluated, treated, and prescribed — without a waiting room, a video call, or an appointment.</p>',
        '<p class="lede">Text your symptoms to a double board-certified Nurse Practitioner. Get evaluated, treated, and prescribed, without a waiting room, a video call, or an appointment.</p>',
    ),
    # ---- "Healthcare is broken" intro (1) ------------------------------------
    (
        "<p>Four things the waiting-room system gets wrong — and what you get instead.</p>",
        "<p>Four things the waiting-room system gets wrong, and what you get instead.</p>",
    ),
    # ---- "Three steps" cards (2) --------------------------------------------
    (
        "<div class=\"body\"><h3>Text your symptoms</h3><p>Tell us what's going on in your own words — no form fatigue, no 30-question intake.</p><div class=\"time\">⏱ 90 seconds</div></div>",
        "<div class=\"body\"><h3>Text your symptoms</h3><p>Tell us what's going on in your own words. No form fatigue, no 30-question intake.</p><div class=\"time\">⏱ 90 seconds</div></div>",
    ),
    (
        '<div class="body"><h3>A real NP reviews</h3><p>Double board-certified. Reads your history, asks any follow-ups, builds a plan for you — not a template.</p><div class="time">⏱ under 30 min</div></div>',
        '<div class="body"><h3>A real NP reviews</h3><p>Double board-certified. Reads your history, asks any follow-ups, builds a plan for you, not a template.</p><div class="time">⏱ under 30 min</div></div>',
    ),
    # ---- Image alt text (1) --------------------------------------------------
    (
        'alt="Chris Woods, MSN, APRN, FNP-C — founder of NPCWoods Telemedicine"',
        'alt="Chris Woods, MSN, APRN, FNP-C, founder of NPCWoods Telemedicine"',
    ),
    # ---- About-Chris bio (1) -------------------------------------------------
    (
        "<p>Chris Woods, MSN, APRN, FNP-C, is a double board-certified Family Nurse Practitioner and the founder of NPCWoods Telemedicine. He personally reviews every patient case — no AI, no chatbots, no handoffs to someone you've never met.</p>",
        "<p>Chris Woods, MSN, APRN, FNP-C, is a double board-certified Family Nurse Practitioner and the founder of NPCWoods Telemedicine. He personally reviews every patient case. No AI, no chatbots, no handoffs to someone you've never met.</p>",
    ),
    # ---- Bare "Board Certified" credential bullet (1) ------------------------
    (
        '<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>Family Nurse Practitioner — Board Certified</b> (FNP-C)</div></li>',
        '<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>Double Board-Certified Family Nurse Practitioner</b> (FNP-C)</div></li>',
    ),
    # ---- Simulator caption + bubble (2) -------------------------------------
    (
        "<p>Type a symptom. Chris's response streams back — same as a real visit.</p>",
        "<p>Type a symptom. Chris's response streams back, same as a real visit.</p>",
    ),
    (
        "<div class=\"msg np\">Hey — I'm Chris. Tell me what's going on and I'll take a look.</div>",
        "<div class=\"msg np\">Hey, I'm Chris. Tell me what's going on and I'll take a look.</div>",
    ),
    # ---- Bare "board-certified" in pricing-section bullets (1) --------------
    (
        "<li>Evaluation by a board-certified NP</li>",
        "<li>Evaluation by a double board-certified NP</li>",
    ),
    # ---- Testimonial attributions (3) ----------------------------------------
    (
        '<span>— Sarah K. · Phoenix, AZ</span>',
        '<span>Sarah K. · Phoenix, AZ</span>',
    ),
    (
        '<span>— Marcus T. · Salt Lake City, UT</span>',
        '<span>Marcus T. · Salt Lake City, UT</span>',
    ),
    (
        '<span>— Rachel D. · Reno, NV</span>',
        '<span>Rachel D. · Reno, NV</span>',
    ),
    # ---- FAQ visible answers (2) ---------------------------------------------
    (
        "<p>We're a flat-fee cash-pay practice — $59 per visit, no billing. Many patients find that's less than a typical co-pay. We'll send a receipt you can submit to HSA/FSA.</p>",
        "<p>We're a flat-fee cash-pay practice. $59 per visit, no billing. Many patients find that's less than a typical co-pay. We'll send a receipt you can submit to HSA/FSA.</p>",
    ),
    (
        "<p>Yes. Every case is read and reviewed by Chris Woods, FNP-C — no AI triage, no rotating roster of contract clinicians, no chatbots pretending to be people.</p>",
        "<p>Yes. Every case is read and reviewed by Chris Woods, FNP-C. No AI triage, no rotating roster of contract clinicians, no chatbots pretending to be people.</p>",
    ),
    # ---- Tk text divider (1) — was just an em-dash glyph -------------------
    (
        '<span class="tk-text">—</span>',
        '<span class="tk-text">·</span>',
    ),
    # ---- Symptom-simulator bot replies (3) ----------------------------------
    (
        '"Sorry you\'re dealing with that — burning with urination is a classic UTI sign, especially with urgency or more frequent trips.",',
        '"Sorry you\'re dealing with that. Burning with urination is a classic UTI sign, especially with urgency or more frequent trips.",',
    ),
    (
        '"Cold sores respond best if we hit them in the first 48 hrs — when did you first notice it?",',
        '"Cold sores respond best if we hit them in the first 48 hrs. When did you first notice it?",',
    ),
    (
        '"Thanks — a few quick questions so I can help: how long has this been going on, and on a 1–10 scale how bad is it right now?",',
        '"Thanks, a few quick questions so I can help: how long has this been going on, and on a 1 to 10 scale how bad is it right now?",',
    ),
    # ---- FAQ JSON-LD answer text (2) -----------------------------------------
    (
        '"text": "Yes. Chris is a licensed nurse practitioner, and every conversation is protected by HIPAA — the same federal privacy law that covers any clinic visit. Your messages are handled on a HIPAA-compliant platform and encrypted so your health information stays between you and Chris. Chris personally reviews and responds to every message; there is no AI triage, no call center, and no third-party handling. Your information is never shared, sold, or used for advertising."',
        '"text": "Yes. Chris is a licensed nurse practitioner, and every conversation is protected by HIPAA, the same federal privacy law that covers any clinic visit. Your messages are handled on a HIPAA-compliant platform and encrypted so your health information stays between you and Chris. Chris personally reviews and responds to every message; there is no AI triage, no call center, and no third-party handling. Your information is never shared, sold, or used for advertising."',
    ),
    (
        '"text": "Chris follows up with every patient the next day. If your symptoms aren\'t improving, he\'ll reassess your case and adjust your treatment plan — whether that means a different medication, a different dose, or a referral for in-person care. There\'s no extra charge for follow-up adjustments."',
        '"text": "Chris follows up with every patient the next day. If your symptoms aren\'t improving, he\'ll reassess your case and adjust your treatment plan, whether that means a different medication, a different dose, or a referral for in-person care. There\'s no extra charge for follow-up adjustments."',
    ),
    # ---- "Save my number" save-card copy (2) --------------------------------
    (
        "<div class=\"npc-save-card-msg\"><strong>Not sick right now?</strong> Save my number for later — just search \"sick guy\" in your contacts when you need me.</div>",
        "<div class=\"npc-save-card-msg\"><strong>Not sick right now?</strong> Save my number for later. Just search \"sick guy\" in your contacts when you need me.</div>",
    ),
    (
        "<div class=\"npc-save-card-hint\">Saves to your phone contacts — search \"sick guy\" or \"urgent care\" anytime</div>",
        "<div class=\"npc-save-card-hint\">Saves to your phone contacts. Search \"sick guy\" or \"urgent care\" anytime</div>",
    ),
]

# -----------------------------------------------------------------------------
# 2. ARIZONA — landing-pages/arizona-telemedicine/index.html
# -----------------------------------------------------------------------------
ARIZONA = ROOT / "landing-pages" / "arizona-telemedicine" / "index.html"

arizona_edits: list[tuple[str, str]] = [
    # ---- Meta + title + og (3) ----------------------------------------------
    (
        '<meta name="description" content="Arizona telemedicine for $59. Text a licensed nurse practitioner — no appointment, no waiting room. Prescriptions sent to your local AZ pharmacy.">',
        '<meta name="description" content="Arizona telemedicine for $59. Text a licensed nurse practitioner. No appointment, no waiting room. Prescriptions sent to your local AZ pharmacy.">',
    ),
    (
        '<title>Same-Day Telemedicine in Arizona — $59 | NPCWoods</title>',
        '<title>Same-Day Telemedicine in Arizona: $59 | NPCWoods</title>',
    ),
    (
        '<meta property="og:title" content="Same-Day Telemedicine in Arizona — $59 | NPCWoods">',
        '<meta property="og:title" content="Same-Day Telemedicine in Arizona: $59 | NPCWoods">',
    ),
    # ---- Nav + slide-panel CTAs (4) ------------------------------------------
    (
        '          $59 &mdash; Text Chris Now',
        '          $59 · Text Chris Now',
    ),
    (
        '<div class="npc-panel-link-text">Pricing<div class="npc-panel-link-sub">$59 flat fee &mdash; one price, one promise</div></div>',
        '<div class="npc-panel-link-text">Pricing<div class="npc-panel-link-sub">$59 flat fee · one price, one promise</div></div>',
    ),
    (
        '<div class="npc-panel-link-text">About Chris<div class="npc-panel-link-sub">MSN, APRN, FNP-C &mdash; double board-certified</div></div>',
        '<div class="npc-panel-link-text">About Chris<div class="npc-panel-link-sub">MSN, APRN, FNP-C · double board-certified</div></div>',
    ),
    (
        '        Text Chris &mdash; Start My $59 Visit',
        '        Text Chris · Start My $59 Visit',
    ),
    # ---- Hero (3) ------------------------------------------------------------
    (
        '<h1>Sick in the Arizona Heat?<br><span>Get Treated by Text &mdash; $59</span></h1>',
        '<h1>Sick in the Arizona Heat?<br><span>Get Treated by Text · $59</span></h1>',
    ),
    (
        '<p class="hero-sub">$59 flat — no paperwork, no hassle. No appointment. No waiting room. Text a real nurse practitioner from anywhere in Arizona &mdash; whether you\'re dealing with the desert heat in Phoenix or up late in Tucson.</p>',
        '<p class="hero-sub">$59 flat. No paperwork, no hassle. No appointment. No waiting room. Text a real nurse practitioner from anywhere in Arizona, whether you\'re dealing with the desert heat in Phoenix or up late in Tucson.</p>',
    ),
    (
        '<div class="hero-price">$59 per visit &mdash; that\'s it</div>',
        '<div class="hero-price">$59 per visit · that\'s it</div>',
    ),
    # ---- How-it-works steps (3) ----------------------------------------------
    (
        "<p>Tap the button to send a text message. Tell us what's going on &mdash; UTI, sinus pressure, ear pain, whatever it is. We'll ask a few follow-up questions to understand your situation.</p>",
        "<p>Tap the button to send a text message. Tell us what's going on: UTI, sinus pressure, ear pain, whatever it is. We'll ask a few follow-up questions to understand your situation.</p>",
    ),
    # FIX P0: bare "board-certified" → "double board-certified" + em-dash sweep
    (
        "<p>Chris Woods, a board-certified Family Nurse Practitioner licensed in Arizona, personally reviews your symptoms and creates a treatment plan. No video call required &mdash; everything happens by text.</p>",
        "<p>Chris Woods, a double board-certified Family Nurse Practitioner licensed in Arizona, personally reviews your symptoms and creates a treatment plan. No video call required. Everything happens by text.</p>",
    ),
    (
        "<p>If you need medication, your prescription is sent electronically to any pharmacy in Arizona &mdash; CVS, Walgreens, Fry's, Costco, wherever is closest. Usually ready within 1&ndash;2 hours.</p>",
        "<p>If you need medication, your prescription is sent electronically to any pharmacy in Arizona: CVS, Walgreens, Fry's, Costco, wherever is closest. Usually ready within 1&ndash;2 hours.</p>",
    ),
    # ---- Footer brand line (1) -----------------------------------------------
    (
        '<p>Text-based telehealth visits — $59 flat, no paperwork, no hassle. No appointment. Just text us what\'s going on and a licensed nurse practitioner will take care of you.</p>',
        '<p>Text-based telehealth visits. $59 flat, no paperwork, no hassle. No appointment. Just text us what\'s going on and a licensed nurse practitioner will take care of you.</p>',
    ),
    # ---- Footer pricing link (1) ---------------------------------------------
    (
        '<li><a href="https://npcwoods.com/pricing/">Pricing &mdash; $59</a></li>',
        '<li><a href="https://npcwoods.com/pricing/">Pricing · $59</a></li>',
    ),
    # ---- Reviewed-by line (1) ------------------------------------------------
    (
        'Reviewed by Chris Woods, MSN, APRN, FNP-C &mdash; Double Board-Certified Nurse Practitioner<br>',
        'Reviewed by Chris Woods, MSN, APRN, FNP-C · Double Board-Certified Nurse Practitioner<br>',
    ),
    # ---- Save-card copy (2) --------------------------------------------------
    (
        "<div class=\"npc-save-card-msg\"><strong>Not sick right now?</strong> Save my number for later — just search \"sick guy\" in your contacts when you need me.</div>",
        "<div class=\"npc-save-card-msg\"><strong>Not sick right now?</strong> Save my number for later. Just search \"sick guy\" in your contacts when you need me.</div>",
    ),
    (
        "<div class=\"npc-save-card-hint\">Saves to your phone contacts — search \"sick guy\" or \"urgent care\" anytime</div>",
        "<div class=\"npc-save-card-hint\">Saves to your phone contacts. Search \"sick guy\" or \"urgent care\" anytime</div>",
    ),
]

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
def main():
    print(f"\n=== Homepage ({HOMEPAGE.name}) ===")
    misses_h = apply(HOMEPAGE, homepage_edits)

    print(f"\n=== Arizona ({ARIZONA.name}) ===")
    misses_a = apply(ARIZONA, arizona_edits)

    total_misses = misses_h + misses_a
    print(f"\n=== Done. Total misses: {total_misses} ===")
    return 1 if total_misses else 0


if __name__ == "__main__":
    sys.exit(main())
