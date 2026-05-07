#!/usr/bin/env python3
"""
Mesa UTI em-dash sweep — 2026-04-30 (followup pass)

The first clarify script handled homepage + Arizona. This sweep covers
the Mesa UTI page, which has em-dashes in meta tags + body copy + JSON-LD
that were not part of the original audit's per-line list.

Reads from the live file (post-distill), applies idempotent replacements,
writes back. Each (old, new) pair is unique substring matching — second
run is a no-op because the em-dash glyph is gone after the first pass.

Backup safety: a .pre-impeccable-2026-04-30.bak of the pristine pre-edit
file already exists. This script does not create a new backup; the .bak
captured before any impeccable edit is still the canonical rollback.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MESA = ROOT / "landing-pages" / "uti-treatment" / "mesa-az" / "index.html"

mesa_edits: list[tuple[str, str]] = [
    # ---- Meta tags (4) -------------------------------------------------------
    (
        "<title>UTI Treatment in Mesa, AZ — $59 Online | NPCWoods</title>",
        "<title>UTI Treatment in Mesa, AZ: $59 Online | NPCWoods</title>",
    ),
    (
        '<meta name="description" content="UTI symptoms in Mesa? Text a Licensed Nurse Practitioner — antibiotics sent to your Mesa pharmacy same day. $59 flat, no waiting room.">',
        '<meta name="description" content="UTI symptoms in Mesa? Text a Licensed Nurse Practitioner. Antibiotics sent to your Mesa pharmacy same day. $59 flat, no waiting room.">',
    ),
    (
        '<meta property="og:title" content="UTI at 10pm in Mesa? Get Antibiotics Without Leaving Home — $59">',
        '<meta property="og:title" content="UTI at 10pm in Mesa? Get Antibiotics Without Leaving Home: $59">',
    ),
    (
        '<meta property="og:description" content="Text a real nurse practitioner. Get UTI antibiotics sent to your Mesa pharmacy. $59 flat fee — affordable telemedicine.">',
        '<meta property="og:description" content="Text a real nurse practitioner. Get UTI antibiotics sent to your Mesa pharmacy. $59 flat fee, affordable telemedicine.">',
    ),
    # ---- JSON-LD FAQ answers (2) --------------------------------------------
    (
        '"text": "Chris will ask follow-up questions to figure out what\'s going on. If it\'s something he can treat via text, he will. If it\'s something that needs in-person care, he\'ll tell you straight up — no charge for the honesty."',
        '"text": "Chris will ask follow-up questions to figure out what\'s going on. If it\'s something he can treat via text, he will. If it\'s something that needs in-person care, he\'ll tell you straight up. No charge for the honesty."',
    ),
    (
        '"text": "Most people hear back within a few hours. If antibiotics are appropriate, your prescription gets sent electronically to a pharmacy near you in Mesa — Community Clinical Pharmacy on S Vineyard, Fry\'s, wherever is closest. Many people pick up same-day."',
        '"text": "Most people hear back within a few hours. If antibiotics are appropriate, your prescription gets sent electronically to a pharmacy near you in Mesa: Community Clinical Pharmacy on S Vineyard, Fry\'s, wherever is closest. Many people pick up same-day."',
    ),
    # ---- Shared header CTA labels on Mesa (4) -------------------------------
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
    # ---- Body content em-dashes (long-form copy) ----------------------------
    (
        "<p>The urgent care on Southern closed hours ago. The ER at Banner Desert is a three-hour wait. Just text us what's going on — $59, prescription to your Mesa pharmacy, done.</p>",
        "<p>The urgent care on Southern closed hours ago. The ER at Banner Desert is a three-hour wait. Just text us what's going on. $59, prescription to your Mesa pharmacy, done.</p>",
    ),
    (
        "<p>It's 9pm on a Friday. You just got back from catching the Cubs at Sloan Park — great game, but you've been holding it since the 5th inning because the lines were ridiculous. Now you're home, and every single trip to the bathroom feels like fire. You've been four times in the last hour. You know exactly what this is.</p>",
        "<p>It's 9pm on a Friday. You just got back from catching the Cubs at Sloan Park (great game, but you've been holding it since the 5th inning because the lines were ridiculous). Now you're home, and every single trip to the bathroom feels like fire. You've been four times in the last hour. You know exactly what this is.</p>",
    ),
    (
        "<p>Here's what you do instead: you text <a href=\"sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Mesa\">(480) 639-4722</a> while you're still sitting on your couch. You tell Chris — a real <a href=\"https://npcwoods.com/how-it-works/\">nurse practitioner</a>, not a chatbot — what's going on. He asks a couple follow-up questions. If it's a straightforward UTI (and let's be honest, you've had one before, you know the drill), he sends a prescription to Community Clinical Pharmacy (a local independent pharmacy) over on S Vineyard. You pick it up tomorrow morning on your way to the Superstition Freeway. Done. $59. $59 flat — no paperwork, no hassle.</p>",
        "<p>Here's what you do instead: you text <a href=\"sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Mesa\">(480) 639-4722</a> while you're still sitting on your couch. You tell Chris (a real <a href=\"https://npcwoods.com/how-it-works/\">nurse practitioner</a>, not a chatbot) what's going on. He asks a couple follow-up questions. If it's a straightforward UTI (and let's be honest, you've had one before, you know the drill), he sends a prescription to Community Clinical Pharmacy (a local independent pharmacy) over on S Vineyard. You pick it up tomorrow morning on your way to the Superstition Freeway. Done. $59. $59 flat. No paperwork, no hassle.</p>",
    ),
    (
        "<p><strong>NPCWoods Telemedicine</strong> treats UTIs in Mesa, Arizona for <strong>$59</strong> via text message. $59 flat — no paperwork, no hassle. No appointment — just text <a href=\"sms:4806394722\">(480) 639-4722</a>, describe your symptoms, and Chris Woods, a licensed nurse practitioner, will respond same-day. Prescriptions sent directly to your Mesa pharmacy.</p>",
        "<p><strong>NPCWoods Telemedicine</strong> treats UTIs in Mesa, Arizona for <strong>$59</strong> via text message. $59 flat. No paperwork, no hassle. No appointment. Just text <a href=\"sms:4806394722\">(480) 639-4722</a>, describe your symptoms, and Chris Woods, a licensed nurse practitioner, will respond same-day. Prescriptions sent directly to your Mesa pharmacy.</p>",
    ),
    (
        "<p>Chris — a real nurse practitioner licensed in Arizona — will text back. He might ask when it started, if you've had UTIs before, or if anything else is going on. Think of it like texting a friend who happens to know medicine. Except this friend can actually write you a prescription.</p>",
        "<p>Chris (a real nurse practitioner licensed in Arizona) will text back. He might ask when it started, if you've had UTIs before, or if anything else is going on. Think of it like texting a friend who happens to know medicine. Except this friend can actually write you a prescription.</p>",
    ),
    (
        "<p>Community Clinical Pharmacy on S Vineyard has been in Mesa since 1980. Or Fry's on Power Road if that's your route. The prescription shows up electronically — you just walk in and pick it up.</p>",
        "<p>Community Clinical Pharmacy on S Vineyard has been in Mesa since 1980. Or Fry's on Power Road if that's your route. The prescription shows up electronically. You just walk in and pick it up.</p>",
    ),
    (
        "<p>Chris Woods is a real nurse practitioner — <a href=\"https://npcwoods.com/arizona-telemedicine/\">licensed in Arizona</a>, not a chatbot, not a call center. He reads your text himself and responds personally. The East Valley has a million telehealth options that route you to some random provider in another state who's juggling 40 patients at once. This isn't that. This is one NP who actually reads your text and treats you like a person, not a ticket number. Verify Chris's credentials on the <a href=\"https://www.azbn.gov/verify-a-license\">Arizona Board of Nursing</a>.</p>",
        "<p>Chris Woods is a real nurse practitioner, <a href=\"https://npcwoods.com/arizona-telemedicine/\">licensed in Arizona</a>, not a chatbot, not a call center. He reads your text himself and responds personally. The East Valley has a million telehealth options that route you to some random provider in another state who's juggling 40 patients at once. This isn't that. This is one NP who actually reads your text and treats you like a person, not a ticket number. Verify Chris's credentials on the <a href=\"https://www.azbn.gov/verify-a-license\">Arizona Board of Nursing</a>.</p>",
    ),
    (
        "<h2>Be Honest With Yourself — Is This Just a UTI?</h2>",
        "<h2>Be Honest With Yourself: Is This Just a UTI?</h2>",
    ),
    (
        "<li>You've got a fever over 101&deg;F AND pain in your back or side — that's kidney territory, and you might need IV antibiotics</li>",
        "<li>You've got a fever over 101&deg;F AND pain in your back or side. That's kidney territory, and you might need IV antibiotics</li>",
    ),
    (
        "<li>You can't keep water down — because you can't take oral antibiotics if you're throwing up</li>",
        "<li>You can't keep water down. (You can't take oral antibiotics if you're throwing up.)</li>",
    ),
    (
        "<p>Banner Desert on Dobson or Mountain Vista on Crismon — whichever's closer. Don't mess around with kidney stuff.</p>",
        "<p>Banner Desert on Dobson or Mountain Vista on Crismon, whichever's closer. Don't mess around with kidney stuff.</p>",
    ),
    (
        "<p>Yes. For uncomplicated UTIs — the kind where it burns when you pee, you're going constantly, and you know the feeling — a text-based visit with a nurse practitioner is clinically supported. Chris takes a thorough history via text, and if antibiotics are the right call, he sends the prescription electronically. No video call, no driving anywhere.</p>",
        "<p>Yes. For uncomplicated UTIs (the kind where it burns when you pee, you're going constantly, and you know the feeling), a text-based visit with a nurse practitioner is clinically supported. Chris takes a thorough history via text, and if antibiotics are the right call, he sends the prescription electronically. No video call, no driving anywhere.</p>",
    ),
    (
        '<p>The $59 covers the visit. Meds are separate, but most generic UTI antibiotics — like nitrofurantoin or trimethoprim-sulfamethoxazole — run under $10 with <a href="https://www.goodrx.com/">GoodRx</a> at pharmacies in Mesa. So you\'re looking at under $70 total, start to finish.</p>',
        '<p>The $59 covers the visit. Meds are separate, but most generic UTI antibiotics (like nitrofurantoin or trimethoprim-sulfamethoxazole) run under $10 with <a href="https://www.goodrx.com/">GoodRx</a> at pharmacies in Mesa. So you\'re looking at under $70 total, start to finish.</p>',
    ),
    (
        '<p>That\'s literally who this is built for. $59 flat, no hidden fees, no surprise bills. A lot of folks in the East Valley — especially people working jobs that don\'t offer benefits — use <a href="https://npcwoods.com/">NPCWoods</a> specifically because it\'s affordable and simple.</p>',
        '<p>That\'s literally who this is built for. $59 flat, no hidden fees, no surprise bills. A lot of folks in the East Valley (especially people working jobs that don\'t offer benefits) use <a href="https://npcwoods.com/">NPCWoods</a> specifically because it\'s affordable and simple.</p>',
    ),
    (
        '<p>UTIs aren\'t the only thing we handle. NPCWoods treats <a href="https://npcwoods.com/sinus-infection-treatment/">sinus infections</a>, <a href="https://npcwoods.com/dental-pain/">dental pain</a>, <a href="https://npcwoods.com/ear-infection/">ear infections</a>, and <a href="https://npcwoods.com/conditions/">50+ other conditions</a> — all by text, all for $59. <a href="https://npcwoods.com/how-it-works/">See how a visit works</a>.</p>',
        '<p>UTIs aren\'t the only thing we handle. NPCWoods treats <a href="https://npcwoods.com/sinus-infection-treatment/">sinus infections</a>, <a href="https://npcwoods.com/dental-pain/">dental pain</a>, <a href="https://npcwoods.com/ear-infection/">ear infections</a>, and <a href="https://npcwoods.com/conditions/">50+ other conditions</a>, all by text, all for $59. <a href="https://npcwoods.com/how-it-works/">See how a visit works</a>.</p>',
    ),
    (
        '<p>Text <a href="sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Mesa" style="color: rgba(255,255,255,0.95); text-decoration: underline;">(480) 639-4722</a>. Tell us what\'s going on. $59 flat — no paperwork, no hassle.</p>',
        '<p>Text <a href="sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Mesa" style="color: rgba(255,255,255,0.95); text-decoration: underline;">(480) 639-4722</a>. Tell us what\'s going on. $59 flat. No paperwork, no hassle.</p>',
    ),
    (
        '<div class="signature-close">— Chris</div>',
        '<div class="signature-close">Chris</div>',
    ),
    # ---- Footer (matches Arizona pattern, 1) --------------------------------
    (
        "<p>Text-based telehealth visits — $59 flat, no paperwork, no hassle. No appointment. Just text us what's going on and a licensed nurse practitioner will take care of you.</p>",
        "<p>Text-based telehealth visits. $59 flat, no paperwork, no hassle. No appointment. Just text us what's going on and a licensed nurse practitioner will take care of you.</p>",
    ),
    (
        '<li><a href="https://npcwoods.com/pricing/">Pricing &mdash; $59</a></li>',
        '<li><a href="https://npcwoods.com/pricing/">Pricing · $59</a></li>',
    ),
    (
        'Reviewed by Chris Woods, MSN, APRN, FNP-C &mdash; Double Board-Certified Nurse Practitioner<br>',
        'Reviewed by Chris Woods, MSN, APRN, FNP-C · Double Board-Certified Nurse Practitioner<br>',
    ),
    # ---- Sticky mobile bottom CTA (1) ---------------------------------------
    (
        '<a href="sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Mesa">$59 — Text Chris Now</a>',
        '<a href="sms:4806394722?body=Hi%2C%20I%20think%20I%20have%20a%20UTI%20in%20Mesa">$59 · Text Chris Now</a>',
    ),
]


def main():
    src = MESA.read_text(encoding="utf-8")
    out = src
    misses = 0
    print(f"=== Mesa em-dash sweep ({MESA.name}) ===")
    for old, new in mesa_edits:
        if old not in out:
            misses += 1
            print(f"  MISS  {old[:80]!r}")
        else:
            count = out.count(old)
            out = out.replace(old, new)
            print(f"  ok ({count}×) {old[:60]!r}")
    MESA.write_text(out, encoding="utf-8")
    print(f"=== Done. Total misses: {misses} ===")
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
