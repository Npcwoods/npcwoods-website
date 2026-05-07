# Product

## Register

brand

## Users

**Primary — Patients in active symptom (~98% of revenue).** Adults 25–55 in the rural-leaning corridor of North Georgia and Western North Carolina, plus an Arizona growth target. They land on a page mid-symptom: burning during urination, sinus pressure that won't quit, sore throat, dental pain, ED concerns. They are usually on a phone, often in bad lighting, sometimes in pain or with a fussy kid in the room. They came from a Google search like "UTI doctor near me" or a Facebook post Chris filmed himself. They want **a script called in today** — not a video appointment, not a portal login, not a 20-minute intake form. The decision they make on this page is whether to text the number or close the tab.

**Secondary — Cost-shoppers without coverage.** People who would have driven to urgent care but bounced when they hit a $200 quote. They're suspicious of cheap healthcare ("what's the catch?") and need transparent proof: license numbers, real photos, real prices, real response-time claims.

**Job-to-be-done:** "Get me a real clinician's eyes on my problem and a script to my pharmacy in under an hour, for a price I can pay without thinking about it, without leaving my house."

## Product Purpose

NPCWoods.com sells **trust at a glance**. The product is not the visit — the product is the page that earns enough trust in the first 3 seconds to make a hurting person text a phone number. Every section, every word, every pixel either accelerates that text or gets in the way.

Success looks like:
1. Visitor lands → sees the price ($59), the person (Chris's actual face), and the action (text this number) — all without scrolling.
2. Visitor's specific anti-objection ("is this a real human?", "how fast?", "what if I'm in a different state?") is answered before they have to scroll past it.
3. Visitor texts. SMS click is the only conversion event that matters.

This site competes with Teladoc, Amwell, GoodRx Care, urgent care chains, and the Reddit thread the visitor is reading in the next tab. Its only edge is **personal**: a real Nurse Practitioner the visitor can see, named, with a license number they can verify.

## Brand Personality

**Three words: warm, transparent, decisive.**

- **Voice — "Southern-warm peer mentor with structured systems."** Casual-professional. "Y'all" and contractions are fine and welcome. Exclamation points are fine. The reader should feel like a knowledgeable friend is talking to them, not a hospital marketing team.
- **Tone shifts by surface.** Homepage is welcoming and reassuring. Condition pages are direct and confident ("Yes, we treat UTIs. Same day. $59. Text us."). State pages are local-specific and proud. Blog is conversational and educational, never preachy.
- **Authority comes from specificity, not titles.** Real photo. Real license numbers. Real turnaround times ("usually back to you within an hour during business hours"). Specific pharmacy partners.
- **Faith framing is allowed but never performative.** Stewardship, calling, family — fine where natural. Bible verses, prayer hands, "blessed" as a brand modifier — never.

**Voice markers to lean into:**
- Opens like "Hey y'all," "Here's the deal," "Pure transparency"
- "$59 flat fee," "no paperwork," "no hassle," "no surprise bills"
- "I believe in you" energy paired with "but you have to want this"
- Short sentences. Then medium ones. Then a question that makes you act.

**Voice markers to refuse:**
- LinkedIn-corporate ("leveraging," "world-class," "synergy," "platform")
- Hype-bro ("game-changer," "10x," "let's gooooo")
- Preachy religious ("blessed by God to bring you...")
- Generic AI marketing ("Discover the future of healthcare")
- Em dashes — replace with comma, colon, period, or parentheses

## Anti-references

This site should not look or read like:

- **Teladoc / Amwell / MDLive / Sesame** — corporate-clinical, navy-and-stethoscope, "platform-as-healthcare." Stock-photo doctors, abstract gradient blobs, "We connect you with a network of providers." That is what NPCWoods is the *alternative* to.
- **GoodRx / Costco Pharmacy comparison sites** — spammy multi-CTA pages, drug-name SEO bait, table-of-prices-from-every-pharmacy energy.
- **Hospital system landing pages (Mayo, Cleveland Clinic, Atrium)** — institutional gravity, white-coat photography, "Find a Doctor" search bars. NPCWoods is one Nurse Practitioner, not an institution.
- **Generic ConvertKit / Mailchimp / Webflow template landing pages** — gradient hero with floating phone mockup, "Used by 10,000+ teams," cards-with-icons feature grid, FAQ accordion at the bottom. AI-template smell.
- **Doctor-on-Demand-style "AI triage" tools** — chatbot avatars, "Symptom checker," "Tell us how you feel." NPCWoods does not have a chatbot, does not triage, and the visitor does not want one.

**Forbidden words on this site (zero exceptions):**
- "doctor," "physician," "MD" — Chris is a Nurse Practitioner. Use "Licensed Nurse Practitioner," "NP," or "clinician."
- "insurance" — triggers ad-platform flags and is not what NPCWoods sells. Use "$59 flat fee," "no paperwork," "no hidden fees," "no surprise bills."
- "Text a Doctor" — even when SEO research says it's open territory.
- "Board-certified" alone — corporate phrasing. **"Double board-certified" is OK** as Chris's specific credential.
- "appointment" — implies scheduling friction. Use "text us" or "start your visit."

## Design Principles

Five principles, in priority order. When two principles conflict, the higher one wins.

1. **Trust is the top of the funnel, not the bottom.** Price, real photo, license number, response-time claim, and the SMS CTA must all be visible above the fold on mobile. Trust signals do not "earn their place lower on the page" — they earn the page itself.

2. **Mobile is the only viewport that matters.** ~80%+ of traffic is a phone in a hand. Breakpoint planning starts at 360px and works up; never the reverse. Tap targets ≥44px. Every primary CTA must be reachable with one thumb without scrolling. Sticky text-us bar on every condition page.

3. **Specificity beats abstraction, every time.** "Same-day response" not "Fast care." "$59 flat fee" not "Affordable pricing." "Chris Woods, NP" not "A licensed clinician." If a sentence could appear unchanged on a Teladoc page, rewrite it until it can't.

4. **Peer, not provider.** The voice and visuals should feel like one person talking to one person. Cut anything that smells institutional: stock photography, abstract logos as content, "our team," white-coat tropes, hospital-blue gradients used as decoration.

5. **Visible plumbing where it builds trust; invisible plumbing everywhere else.** License numbers, NPI, real pharmacy partners, real turnaround times — show the wiring, it is the proof. But never expose the marketing wiring (no "Subscribe to our newsletter for tips!" boxes, no "We use cookies to improve your experience" theatrical banners). The visitor should feel a clinic, not a funnel.

## Accessibility & Inclusion

- **Target: WCAG 2.1 AA across all surfaces.** Color contrast ratios ≥4.5:1 for body text and ≥3:1 for large text. The site already declares `prefers-reduced-motion` overrides — keep that promise on every new component.
- **Mid-symptom usability is the real bar.** Patients are often in pain, distracted, on a low-brightness screen, with one thumb. Two-handed UI, hover-only states, or "click here" affordances that aren't obvious tap targets fail this audience faster than an a11y audit will catch.
- **Skip-link present** on every page (already on homepage at line 112). Keyboard-only navigation must reach the SMS CTA in ≤6 tab stops on every page.
- **Color independence.** Trust signals (verified, available, in-stock) cannot rely on green-vs-red alone — pair with icon and label.
- **Image alts.** Real medical content (medication names, conditions) needs descriptive alt text, not "image of pill bottle."
- **Reading level.** Body copy at ~6th–8th grade. Patients are often searching while symptomatic; the page is not the place to flex vocabulary.
