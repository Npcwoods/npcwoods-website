---
name: NPCWoods Telemedicine
description: Trust-at-a-glance marketing surface for an async $59 telehealth practice; a one-Nurse-Practitioner peer voice in a category dominated by corporate platforms.
colors:
  white: "#FFFFFF"
  off-white: "#F7F8FA"
  warm-white: "#FDF8F4"
  text-primary: "#1A1A2E"
  text-body: "#4A4A5A"
  text-muted: "#8E8E9A"
  brand: "#2563EB"
  brand-light: "#EFF6FF"
  brand-soft: "#DBEAFE"
  brand-hover: "#1D4ED8"
  border: "#E5E7EB"
  border-hover: "#D1D5DB"
  success: "#16A34A"
  success-light: "#DCFCE7"
  gold: "#F59E0B"
typography:
  display:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(2.2rem, 6vw, 4rem)"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Inter, sans-serif"
    fontSize: "clamp(1.75rem, 4vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Inter, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Inter, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "Inter, sans-serif"
    fontSize: "0.65rem"
    fontWeight: 700
    letterSpacing: "0.1em"
  brand-mark:
    fontFamily: "'DM Serif Display', Georgia, serif"
    fontSize: "1.2rem"
    fontWeight: 400
    letterSpacing: "-0.3px"
rounded:
  sm: "4px"
  md: "8px"
  lg: "10px"
  xl: "12px"
  pill: "100px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "20px"
  xl: "32px"
  side-pad: "48px"
  side-pad-mobile: "20px"
  section-pad: "100px"
  section-pad-mobile: "64px"
  container-max: "1200px"
  nav-height: "72px"
components:
  button-primary:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.white}"
    rounded: "{rounded.pill}"
    padding: "16px 32px"
  button-primary-hover:
    backgroundColor: "{colors.brand-hover}"
    textColor: "{colors.white}"
    rounded: "{rounded.pill}"
    padding: "16px 32px"
  nav-cta:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.white}"
    rounded: "{rounded.xl}"
    padding: "10px 20px"
  card:
    backgroundColor: "{colors.white}"
    textColor: "{colors.text-body}"
    rounded: "{rounded.xl}"
    padding: "24px"
  pill-tag:
    backgroundColor: "{colors.brand-light}"
    textColor: "{colors.brand}"
    rounded: "{rounded.pill}"
    padding: "6px 14px"
  state-dot:
    backgroundColor: "{colors.success}"
    rounded: "{rounded.pill}"
    size: "7px"
---

# Design System: NPCWoods Telemedicine

## 1. Overview

**Creative North Star: "The Front Porch Clinic."**

This is not a hospital website. It is a clinic-as-front-porch — a real Nurse Practitioner waving you up the steps with the price written on the screen door. The aesthetic is warm-clean, not clinical-clean: white surfaces tinted toward off-white and warm-white, a single confident blue accent that does the work of both trust signal and CTA, and a sans-serif voice (Inter) that reads like a conversation, not a chart.

The system explicitly rejects the visual vocabulary of Teladoc / Amwell / MDLive / Sesame: navy-and-stethoscope palettes, white-coat hero photography, gradient-blob backgrounds, "platform" framing, and the cards-with-icons feature grid that signals "we are an institution." It also rejects the spammy multi-CTA energy of GoodRx-style comparison sites and the chatbot-avatar friction of "AI triage" tools. NPCWoods is one person. The interface should feel that way.

The system leans on **mass over decoration**: large headlines (Inter 800), generous section padding (100px desktop / 64px mobile), and pill-shaped primary CTAs that read like permission to text. Where Stitch-typical apps lean clinical-cool, this leans southern-warm.

**Key Characteristics:**
- **Single-accent palette.** One blue (`#2563EB`) carries the entire identity — CTA, link, focus ring, success state companion.
- **Tinted neutrals, not pure neutrals.** `#FFFFFF`, `#F7F8FA`, `#FDF8F4` — the warm-white is intentional warmth, not bug.
- **Pill CTAs everywhere.** 100px radius primary buttons. Anything that the visitor should tap reads as round.
- **Inter as a single voice.** One typeface, five weights (400/500/600/700/800), variable scale.
- **Trust comes from specificity.** Real photo, real phone number, real license counts — never abstract iconography pretending to be proof.

## 2. Colors: The One-Blue Palette

A single saturated blue carries the brand. Tinted near-whites carry the surface. Greens and golds appear only as state companions — never decorative.

### Primary
- **NPC Blue** (`#2563EB`): The single voice of the brand. Used for the primary CTA, all links in body copy, focus rings, the "phone-icon-glow" on call links, and the SMS-pulse dot. Never used as background fill on more than ~10% of any screen — its rarity is the point.
- **NPC Blue Hover** (`#1D4ED8`): Hover/active state for `brand`. Slightly deeper, never different hue.
- **NPC Blue Light** (`#EFF6FF`): The whisper of brand presence. Used for hover backgrounds on nav links, soft tints on dropdowns, and decorative pill tag fills.
- **NPC Blue Soft** (`#DBEAFE`): One step deeper than `brand-light` — used as ring/halo color on state dots and focus accents.

### Tertiary (state companions only — never decorative)
- **Trust Green** (`#16A34A`): "Available," "in-stock," "verified," "licensed in this state" dots. Always paired with a label or icon — never green alone.
- **Trust Green Light** (`#DCFCE7`): Halo/ring color around `success` dots; the soft chip fill behind a green checkmark.
- **Warm Gold** (`#F59E0B`): Reserved for review stars and premium-callout accents only. Never used as a CTA, never as link color.

### Neutral
- **Page White** (`#FFFFFF`): The default surface.
- **Off-White** (`#F7F8FA`): Section dividers, card hover-out states, scrollbar track.
- **Warm White** (`#FDF8F4`): Reserved for sections that need to feel softer-than-white (about, testimonials). Almost imperceptibly warm — that's the point.
- **Text Primary** (`#1A1A2E`): All headings, footer background, brand-mark text. Tinted toward blue-purple, never `#000`.
- **Text Body** (`#4A4A5A`): All body copy and nav-link text.
- **Text Muted** (`#8E8E9A`): Section labels, microcopy, sub-text under nav links.
- **Border** (`#E5E7EB`): Default 1px borders on cards, dropdowns, dividers.
- **Border Hover** (`#D1D5DB`): The 1-step-darker border on hovered cards or unselected toggles.

### Named Rules

**The One-Voice Rule.** The brand blue (`#2563EB`) is used on ≤10% of any given screen. Its rarity is the point — when the visitor sees blue, it should mean "tap me" or "this is verified." Never use brand blue as a section background fill.

**The Tinted-Neutral Rule.** No `#000000`, no `#FFFFFF` body text on `#FFFFFF` backgrounds, no untinted gray. Every neutral leans toward the brand hue. The warm-white (`#FDF8F4`) is the deliberately *warmer* variant — use it where the section needs to feel less institutional (testimonials, about, "thank you").

**The Trust-Color Rule.** Green (`#16A34A`) and gold (`#F59E0B`) are reserved for state and proof: licensed-here dots, available-now indicators, review stars. They are not part of the brand palette. Never use them on CTAs or section accents.

## 3. Typography: One Voice, Five Weights

**Display Font:** Inter (with `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` fallback)
**Body Font:** Inter (same)
**Brand-Mark Font (logo only):** DM Serif Display (with `Georgia, serif` fallback) — currently used for the nav-logo wordmark and slide-panel logo, nowhere else.

**Character:** Inter is the single voice — humanist sans, friendly enough to read like a conversation, technical enough to feel competent. The brand wordmark uses DM Serif Display as a quiet editorial counterweight, but only as a wordmark. Body copy never sets in serif.

### Hierarchy
- **Display** (800, `clamp(2.2rem, 6vw, 4rem)`, line-height 1.05, letter-spacing `-0.03em`): Hero headlines on every page. The visitor's first read.
- **Headline** (700, `clamp(1.75rem, 4vw, 2.5rem)`, line-height 1.15, letter-spacing `-0.02em`): Section openers ("How It Works", "What We Treat", "Pricing").
- **Title** (600, `1.25rem`): Card titles, FAQ question text, dropdown menu labels.
- **Body** (400, `1rem`, line-height 1.7): All paragraph copy. Cap line length at 65–75ch — never run a paragraph the full width of a 1200px container.
- **Label** (700, `0.65rem`, letter-spacing `0.1em`, uppercase): Section eyebrows, panel-section dividers, "STATES WE SERVE"-style microcopy.
- **Brand-Mark** (DM Serif Display, 400, `1.2rem`, letter-spacing `-0.3px`): Nav and panel logo wordmark only. Do not use for headlines or body.

### Named Rules

**The One-Family Rule.** Inter does the work. DM Serif Display is reserved for the wordmark. Do not introduce a third family for "editorial flair" or "headlines that pop" — the system already says enough with weight contrast (400 vs 800).

**The Preload-What-You-Use Rule.** Whatever family is referenced anywhere on the page must be in the `<link rel="preload">` block. Currently only Inter is preloaded — DM Serif Display falls back to Georgia silently on first paint. Either preload it or strip the references. Half-loaded type families are a craft tell.

## 4. Elevation

The system is **flat-by-default with intentional ambient lift on interactive elements**. Surfaces sit on the same plane unless a state demands otherwise; shadows appear as a *response* to interaction (hover, scroll, modal entrance), not as decoration.

### Shadow Vocabulary
- **Card-rest** (`box-shadow: 0 4px 16px rgba(0,0,0,0.04)`): Default ambient lift on cards and dropdowns. Barely visible — the lift comes from contrast, not the shadow.
- **Card-hover** (`box-shadow: 0 8px 30px rgba(0,0,0,0.08)`): Stepped-up shadow on hovered cards and open dropdowns.
- **Brand-glow** (`box-shadow: 0 4px 16px rgba(37,99,235,0.3)`): Reserved for primary CTAs — the brand-blue ambient glow signals "this is the one to tap."
- **Brand-glow-active** (`box-shadow: 0 8px 24px rgba(37,99,235,0.4)`): Hover state on primary CTA. Combined with `transform: translateY(-1px)`.
- **Nav-scrolled** (`box-shadow: 0 4px 24px rgba(0,0,0,0.06)`): Appears only after the user scrolls past the hero — the nav fades from transparent to solid with a soft drop.
- **Slide-panel** (`box-shadow: -12px 0 40px rgba(0,0,0,0.08)`): The mobile slide-out menu's edge shadow.

### Named Rules

**The Lift-on-Touch Rule.** Cards, CTAs, and nav links are flat at rest. They lift (shadow + 1–2px translate) only on hover/focus. Anything that lifts at rest is begging for attention it didn't earn.

**The No-Decorative-Glow Rule.** Brand-glow shadows are CTA-only. Do not put a colored glow on a non-interactive element to "make it pop."

## 5. Components

### Buttons

- **Shape:** Pill, fully rounded (`border-radius: 100px`). The pill is the language of "tap me." Square-cornered buttons are forbidden.
- **Primary:** Brand blue (`#2563EB`) fill, white text, 16px × 32px padding, Inter 600, 1rem. Has the brand-glow shadow at rest, lifts to brand-glow-active on hover with a 1px translate-up. Transition is `0.2s ease` — never bouncy.
- **Hover / Focus:** `:hover` deepens to `#1D4ED8` and lifts. `:focus-visible` paints a 2px brand outline at 2px offset. No squish on `:active`.
- **Nav CTA (compact variant):** Same blue, slightly smaller (`padding: 10px 20px`, `font-size: 0.85rem`), `12px` radius (rounded square, not full pill, because it sits in a 64px nav bar). Optional pulsing green-dot prefix to signal "live."
- **Ghost / Tertiary:** Not currently in the system. If introduced, must be a 1px border in `border` color with brand-blue text — never a gradient outline, never neon, never glassmorphic.

### Cards

- **Corner Style:** `12px` radius (`rounded.xl`). Feature cards, dropdowns, and slide-panel link tiles all share this radius. Pill cards (badge tags, state dots) are the exception.
- **Background:** Page white at rest; hovered cards may shift to `brand-light` (`#EFF6FF`) for nav-link tiles and dropdown hover. Never gradient backgrounds.
- **Shadow Strategy:** See Elevation. `card-rest` at rest, `card-hover` on hover.
- **Border:** 1px `border` (`#E5E7EB`) on dropdowns and slide-panel close buttons. Cards in body copy generally rely on shadow, not border.
- **Internal Padding:** `24px` default, scaled down to `12px` on dense list-item tiles (slide-panel links).

### Inputs / Fields

The current system has very few traditional form inputs because the primary action is `sms:` — there is no signup form on the homepage. When inputs are introduced (contact pages, pharmacy lookup): match button language. `12px` radius, 1px `border`, `text-primary` text color, 16px font-size minimum (anything smaller triggers iOS zoom and is forbidden by the Mobile-First rule). Focus state: 2px brand outline at 2px offset, never an inner glow.

### Navigation

- **Style:** Sticky white nav with a glassmorphic backdrop (`backdrop-filter: blur(20px)` over `rgba(255,255,255,0.92)`) — currently the only place glassmorphism appears in the system, and it is borderline. Consider replacing with a solid white plus a `card-hover` shadow on scroll.
- **Default state:** Transparent-tinted-white background, no shadow.
- **Scrolled state:** `.scrolled` class adds the `nav-scrolled` shadow.
- **Dropdowns:** White `#FFFFFF`, 12px radius, 1px border, `card-hover` shadow. Reveal on `:hover` and `:focus-within` (keyboard-accessible).
- **Mobile:** Hamburger button at ≥768px breakpoint opens a 400px-wide slide-out panel from the right with backdrop blur over the page. The panel is the showcase component of the system — multi-section, semantic, keyboard-trapped, animated entrances.

### Pill Tags

Distinctive component, used for "Same-day," "$59," "Real NP" badges throughout. Brand-light fill, brand text, fully rounded (100px), `0.875rem` font weight 600, `6px × 14px` padding. Functions as an anti-card: the pill is small enough to feel like an aside, big enough to read at a glance.

### State Dots

A tiny but signature component. `7px × 7px` circle, success-green fill (`#16A34A`), with a 2px halo of `success-light` (`#DCFCE7`). Indicates "licensed here," "available," "live." On hover, the dot shifts to brand-blue with a brand-soft halo — re-using color rather than adding a new semantic.

### Slide-Out Panel (Signature)

The mobile menu is the most distinctive custom component — a 400px right-anchored sheet with a sticky header, multi-section body (Navigate / States / Common Services / Get Care Now), staggered fade-in-from-right animation on entrance, and an SMS CTA pinned at the bottom. Treat this as the brand's most considered surface; new patterns should match its density and section-labeling rhythm.

## 6. Do's and Don'ts

### Do:
- **Do** keep the brand on ≤10% of any screen. The blue is rare on purpose — it should feel like the only place to tap.
- **Do** show the price (`$59`), the photo (Chris's actual face), and the SMS CTA above the mobile fold. PRODUCT.md calls this "trust at a glance" — the design must enforce it.
- **Do** preload every font family that's referenced anywhere on the page. Currently DM Serif Display is referenced but not preloaded — fix this.
- **Do** use Inter weight contrast (400 → 800) for hierarchy, not size alone. The display weight (800) is what makes the system feel decisive.
- **Do** pair every state color (green, gold) with a label or icon. Color alone fails the accessibility bar set in PRODUCT.md.
- **Do** lean on tinted near-whites (`#F7F8FA`, `#FDF8F4`) instead of pure white when a section needs to feel different. Don't reach for new colors.
- **Do** reuse the slide-out panel pattern on any future deep-nav surface. It's the system's most distinctive component.

### Don't:
- **Don't** introduce a third typeface for "editorial flair." Inter + DM Serif Display (wordmark only) is the rule. PRODUCT.md anti-references "generic ConvertKit / Mailchimp template landing pages" — those pages always reach for a third display font.
- **Don't** use gradient text (`background-clip: text`). Anywhere. The brand has weight contrast for emphasis.
- **Don't** use glassmorphism decoratively. The nav backdrop-blur is the one borderline use; do not extend the pattern to cards or hero panels. PRODUCT.md anti-references Teladoc / MDLive — those sites lean on glass.
- **Don't** use hospital-blue gradients (`linear-gradient(navy → cyan)`) as section backgrounds. PRODUCT.md anti-references "Mayo / Cleveland Clinic / Atrium" — that's their visual move.
- **Don't** use stock photography of doctors or smiling-patient-on-couch tableaux. Only Chris's actual face. Anything else dilutes the "Peer not provider" principle.
- **Don't** put the word "doctor," "physician," "MD," or "insurance" anywhere in markup, copy, or alt text. PRODUCT.md is unambiguous.
- **Don't** use side-stripe borders (`border-left: 4px solid <color>`) as a callout pattern. Use a full pill, a tinted card, or nothing.
- **Don't** use em dashes (—) in copy. Replace with comma, colon, period, or parentheses.
- **Don't** use the hero-metric SaaS template (big number + tiny label + supporting stats stacked). PRODUCT.md anti-references "ConvertKit / Mailchimp template landing pages" — that template is the giveaway.
- **Don't** add a chatbot avatar or "AI symptom checker" widget. PRODUCT.md anti-references "Doctor-on-Demand-style AI triage" — patients want a human, not an interface.
