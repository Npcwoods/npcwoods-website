# NPCWoods Homepage: “Follow the Thread” Design

**Status:** Approved visual design, pending written-spec review  
**Date:** 2026-07-14  
**Surface:** Private Sites preview only  
**Production rule:** Do not modify or publish the live NPCWoods homepage without Chris’s separate, explicit approval.

## Objective

Create an immersive, mobile-first NPCWoods homepage that tells one simple visitor journey through controlled cinematic scrolling. The visitor is the main character. Chris is the trusted guide. The experience must build trust and make texting Chris feel like the obvious next step without hijacking scroll behavior or hiding essential information behind animation.

## Success Criteria

1. The visitor understands the offer, price, person, availability, and primary action in the first viewport.
2. The homepage feels like one continuous story rather than a stack of unrelated website sections.
3. A single animated thread visibly connects all five story chapters and changes form to match each chapter.
4. The experience remains fast, legible, and complete on a 360-pixel-wide phone.
5. A visitor using reduced-motion settings receives the same content and narrative in a polished static layout.
6. The private preview does not change, publish, or deploy the live WordPress homepage.

## Approved Narrative

The homepage follows one visitor from discomfort to decisive action:

1. **I feel awful.** The visitor lands inside their current emotional state.
2. **I do not have time for the runaround.** Familiar care friction is acknowledged briefly.
3. **A real person can help me.** Chris appears as the guide and trust becomes personal.
4. **This is actually simple.** The text-based visit unfolds in three clear beats.
5. **I know exactly what to do next.** The story resolves into one calm, unmistakable text action.

The emotional arc is pressure → recognition → trust → simplicity → relief.

## Approved Cinematic Device: Follow the Thread

One living line acts as the visual narrator across the entire story.

### Chapter 1: Tangled Beginning

- The thread begins as a slightly tangled warm-clay line behind the visitor-first headline.
- The first viewport still shows Chris Woods, NP; the $59 flat fee; response-time language; 11-state availability; and “Text Chris now.”
- The composition feels compressed but remains readable and calm enough for a symptomatic visitor.

### Chapter 2: Clearing Friction

- Three brief obstacles represent driving, waiting, and forms.
- As the visitor scrolls, the thread straightens and passes each obstacle.
- The obstacles drift away from the thread instead of forcing the visitor through a long negative section.

### Chapter 3: Meeting the Guide

- Chris’s real portrait becomes prominent.
- The thread curves around the portrait and becomes the tail of one message: “Just text me.”
- Chris is framed as the person who helps the visitor move forward, not as the story’s hero.

### Chapter 4: One Simple Conversation

- A short pinned sequence shows three beats:
  1. The visitor describes what is going on.
  2. Chris reviews the information and asks what he needs to know.
  3. The visitor receives clear next steps.
- The thread connects the three conversation beats.
- The copy must not imply that every visitor receives a prescription or guarantee a particular response time or outcome.

### Chapter 5: Calm Resolution

- Movement slows and then stops.
- The thread forms a complete ring around the primary “Text Chris now” action.
- The $59 flat fee and core trust proof appear again.
- The final scene is spacious, still, and decisive.

## Supporting Content After the Story

After the cinematic five-chapter journey, the homepage transitions into a calmer editorial layout containing:

- Real reviews already approved for the homepage
- The 11 licensed states
- Scope and safety boundaries
- Chris’s credentials and direct-care positioning
- Frequently asked questions
- A final text action

This proof content supports the decision without interrupting the narrative climax.

## Visual Language

### Palette

- Pressure ink: `#1B201D`
- Warm cream: `#F7F2E8`
- Paper: `#FFFDF8`
- Trust cobalt: `#2855C7`
- Deep cobalt: `#183F9E`
- Tangled-thread clay: `#BD5A42`
- Resolution green: `#1C8A5C`
- Body ink: `#203128`
- Muted copy: `#647068`

The thread changes from clay to cobalt to green as the visitor moves from discomfort to resolution. Color is always paired with shape, position, and text so meaning never depends on color alone.

### Typography

- Editorial serif for emotional visitor statements and major chapter headlines.
- Highly legible sans-serif for explanations, navigation, trust proof, buttons, and supporting content.
- Short sentences, large mobile type, and a sixth- to eighth-grade reading level.

### Photography

- Use Chris’s approved real portrait assets.
- Avoid stock clinical photography, fake device mockups, and generic abstract healthcare imagery.
- Photography gains prominence only when Chris enters as the guide.

## Interaction and Motion

- Preserve natural browser scrolling at all times.
- Use one short sticky chapter for the three-beat conversation; do not create long pinned sections.
- Drive thread progress from scroll position so motion follows the visitor’s thumb and never auto-plays.
- Use parallax only for secondary depth layers, never for essential text.
- Keep hover behavior supplemental; all primary behavior must work by touch and keyboard.
- When `prefers-reduced-motion: reduce` is active, disable scrubbing, parallax, and transforms. Render the thread and chapters in their final static positions.

## Responsive Behavior

### Phone, Primary Design Target

- Start layout decisions at 360 pixels wide.
- Run the thread down the left edge of the chapter stack.
- Use shorter pinned distances and fewer depth layers.
- Keep the primary text action thumb-ready and at least 44 pixels tall.
- Ensure the first-screen action is reachable within six keyboard tab stops.
- Prevent decorative motion from covering headlines, proof, or actions.

### Desktop

- Allow the thread to curve across the canvas and connect larger spatial compositions.
- Use expanded photography and additional depth without changing the chapter order.
- Preserve the same copy, trust hierarchy, and action path as mobile.

## Technical Architecture for the Private Preview

The first implementation will live only in the isolated Sites preview project at `output/sites-homepage-preview/`. It will not replace or edit `homepage/page-npcwoods-home.php`.

The preview will use:

- A single homepage route with semantic chapter sections
- One client-side scroll controller responsible only for thread progress and chapter motion
- CSS custom properties for palette, thread state, and responsive spacing
- A lightweight scroll animation layer using GSAP ScrollTrigger with scoped timelines and media-query variants
- Native `position: sticky` for layout, with GSAP limited to progress and transforms
- Existing approved NPCWoods photography copied into the preview’s public assets
- Static supporting proof content with no persistence, forms, authentication, uploads, or patient information

The animation controller will initialize only after the page content exists. If JavaScript fails, all sections remain visible in normal document flow with the thread in a static final state.

## Content Rules

- Price is always `$59 flat fee` with no subscription framing.
- Use “Chris Woods, NP,” “Nurse Practitioner,” “provider,” or “clinician” where appropriate.
- Never use forbidden title or payment-trigger wording from the project guidance.
- Do not promise a prescription, guaranteed treatment, or a guaranteed completion time.
- Response-time language must preserve its qualifier, such as “usually back to you within an hour during business hours.”
- No patient information or realistic patient records may appear in the preview.

## Accessibility and Failure Handling

- Meet WCAG 2.1 AA color contrast.
- Include a skip link and semantic headings in order.
- Keep all essential content in the DOM and visible without animation.
- Provide descriptive image alternatives for meaningful photography.
- Use visible keyboard focus states.
- If motion initialization fails, remove pinned behavior and render a normal stacked page.
- If an image fails, preserve layout and show the visitor-facing text and action without obstruction.

## Performance Budget

- No autoplay video, WebGL, 3D engine, or large background animation.
- Use responsive WebP photography and explicit image dimensions.
- Avoid layout-changing animation; animate transforms and opacity only.
- Load the animation layer only on the homepage preview.
- Keep the mobile experience simpler than desktop rather than attempting visual parity at the cost of smoothness.

## Verification

Before the private preview is presented as complete:

1. Run the production build successfully.
2. Verify the five chapter headings, trust proof, price, and primary text actions are present in the rendered output.
3. Verify the page at phone and desktop sizes.
4. Verify keyboard navigation, visible focus, skip link, and reduced-motion behavior.
5. Verify the conversation section does not imply guaranteed medication or outcomes.
6. Confirm the live WordPress homepage file remains unchanged by this preview work.
7. Publish only to an owner-only private Sites URL after the build is validated.

## Out of Scope

- Replacing or deploying the production WordPress homepage
- Changing the existing SMS workflow or phone number
- Collecting visitor or patient information
- Authentication, accounts, persistent records, uploads, or payments
- Publishing a public Sites URL
- Creating a custom domain

## Approval Boundary

Approval of this design authorizes creation of the isolated private preview only. It does not authorize changes to NPCWoods.com or any public deployment.
