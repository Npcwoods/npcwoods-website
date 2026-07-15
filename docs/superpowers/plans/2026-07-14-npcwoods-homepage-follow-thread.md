# NPCWoods “Follow the Thread” Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and privately host an isolated, mobile-first NPCWoods homepage preview whose five-chapter visitor journey is connected by one scroll-driven visual thread.

**Architecture:** Keep the live WordPress homepage untouched. Implement the preview inside `output/sites-homepage-preview/` as one semantic Vinext/React route. Server-render all content, isolate scroll behavior in one client component, use GSAP ScrollTrigger only for progressive enhancement, and fall back to a complete static document when JavaScript or motion is unavailable.

**Tech Stack:** Vinext, React 19, TypeScript, CSS, GSAP ScrollTrigger, Node test runner, Cloudflare-compatible Sites hosting.

---

## File Map

- Create `output/sites-homepage-preview/app/homepage-content.ts`: typed, non-patient marketing copy and review data.
- Create `output/sites-homepage-preview/app/components/HomepageContent.tsx`: semantic five-chapter page and supporting proof.
- Create `output/sites-homepage-preview/app/components/FollowThread.tsx`: the only client-side scroll controller.
- Create `output/sites-homepage-preview/app/components/ThreadPath.tsx`: decorative thread markup with accessible hiding.
- Modify `output/sites-homepage-preview/app/page.tsx`: semantic five-chapter page plus supporting proof.
- Modify `output/sites-homepage-preview/app/layout.tsx`: finished metadata, fonts, and social metadata.
- Replace `output/sites-homepage-preview/app/globals.css`: complete responsive visual and motion system.
- Replace `output/sites-homepage-preview/tests/rendered-html.test.mjs`: final-page server-rendering contract.
- Create `output/sites-homepage-preview/tests/source-contract.test.mjs`: motion, accessibility, and starter-removal contract.
- Create `output/sites-homepage-preview/public/og.png`: bespoke social preview matching the finished page.
- Move `output/sites-homepage-preview/app/_sites-preview/` into `output/sites-homepage-preview/archive/starter/`: preserve the starter without shipping or importing it.
- Modify `output/sites-homepage-preview/package.json` and `package-lock.json`: add GSAP, remove the skeleton package, and run both test files.

## Task 1: Replace the Starter Contract With Finished-Homepage Tests

**Files:**
- Replace: `output/sites-homepage-preview/tests/rendered-html.test.mjs`
- Create: `output/sites-homepage-preview/tests/source-contract.test.mjs`
- Modify: `output/sites-homepage-preview/package.json`

- [ ] **Step 1: Write the failing rendered HTML test**

Replace `tests/rendered-html.test.mjs` with:

```js
import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the finished Follow the Thread homepage", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();

  assert.match(html, /<title>NPCWoods Telemedicine[^<]*<\/title>/i);
  assert.match(html, /I feel awful/i);
  assert.match(html, /I don.t have time for the runaround/i);
  assert.match(html, /A real person can help me/i);
  assert.match(html, /This is actually simple/i);
  assert.match(html, /I know exactly what to do next/i);
  assert.match(html, /\$59 flat fee/i);
  assert.match(html, /licensed in 11 states/i);
  assert.match(html, /usually back to you within an hour during business hours/i);
  assert.match(html, /href=["']sms:4806394722/i);
  assert.match(html, /href=["']#main-content["']/i);
  assert.match(html, /Real texts\. Real relief\./i);
  assert.match(html, /Some symptoms need in-person care/i);
  assert.match(html, /What happens when I text Chris/i);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape|react-loading-skeleton/i);
  assert.doesNotMatch(html, /\bdoctor\b|\bphysician\b|\bappointment\b/i);
});
```

- [ ] **Step 2: Write the failing source contract test**

Create `tests/source-contract.test.mjs`:

```js
import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const read = (path) => readFile(new URL(path, root), "utf8");

test("isolates motion and preserves a reduced-motion fallback", async () => {
  const [controller, css] = await Promise.all([
    read("app/components/FollowThread.tsx"),
    read("app/globals.css"),
  ]);
  assert.match(controller, /gsap\/ScrollTrigger/);
  assert.match(controller, /gsap\.matchMedia/);
  assert.match(controller, /prefers-reduced-motion:\s*reduce/);
  assert.match(controller, /revert\(\)/);
  assert.match(css, /@media\s*\(prefers-reduced-motion:\s*reduce\)/);
  assert.match(css, /\.thread-path/);
  assert.match(css, /\.mobile-text-bar/);
});

test("removes all disposable starter artifacts", async () => {
  const [page, layout, pkg] = await Promise.all([
    read("app/page.tsx"),
    read("app/layout.tsx"),
    read("package.json"),
  ]);
  assert.doesNotMatch(page, /SkeletonPreview|_sites-preview/);
  assert.doesNotMatch(layout, /Starter Project|codex-preview/);
  assert.doesNotMatch(pkg, /react-loading-skeleton/);
  await assert.rejects(access(new URL("app/_sites-preview", root)));
  await access(new URL("archive/starter/SkeletonPreview.tsx", root));
  await access(new URL("archive/starter/preview.css", root));
});
```

- [ ] **Step 3: Update the test script**

Change the package script to:

```json
"test": "npm run build && node --test tests/*.test.mjs"
```

- [ ] **Step 4: Run the tests and confirm the new contract fails**

Run: `npm test`

Expected: FAIL because the starter still renders and `app/components/FollowThread.tsx` does not exist.

- [ ] **Step 5: Commit the failing contract**

```bash
git add output/sites-homepage-preview/tests output/sites-homepage-preview/package.json
git commit -m "[homepage] define cinematic preview contract"
```

## Task 2: Create the Typed Content Model and Semantic Page

**Files:**
- Create: `output/sites-homepage-preview/app/homepage-content.ts`
- Create: `output/sites-homepage-preview/app/components/HomepageContent.tsx`
- Create: `output/sites-homepage-preview/app/components/ThreadPath.tsx`
- Replace: `output/sites-homepage-preview/app/page.tsx`
- Modify: `output/sites-homepage-preview/app/layout.tsx`
- Move: `output/sites-homepage-preview/app/_sites-preview/SkeletonPreview.tsx` → `output/sites-homepage-preview/archive/starter/SkeletonPreview.tsx`
- Move: `output/sites-homepage-preview/app/_sites-preview/preview.css` → `output/sites-homepage-preview/archive/starter/preview.css`
- Modify: `output/sites-homepage-preview/package.json`
- Modify: `output/sites-homepage-preview/package-lock.json`

- [ ] **Step 1: Add the typed content model**

Create `app/homepage-content.ts`:

```ts
export const smsHref =
  "sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit";

export const chapters = [
  { id: "hook", number: "01", title: "I feel awful.", body: "I need help today, without losing the rest of my day." },
  { id: "friction", number: "02", title: "I don’t have time for the runaround.", body: "No driving across town. No waiting room. No pile of forms." },
  { id: "guide", number: "03", title: "A real person can help me.", body: "Text Chris Woods, NP, and tell him what’s going on in your own words." },
  { id: "conversation", number: "04", title: "This is actually simple.", body: "You explain the problem. Chris reviews it. You get clear next steps." },
  { id: "resolution", number: "05", title: "I know exactly what to do next.", body: "$59 flat fee. A real Nurse Practitioner. Right from home." },
] as const;

export const reviews = [
  { quote: "Very fast and convenient. I first messaged Chris at 10:08am and I was picking up my prescriptions from the pharmacy at 10:52am same day!", name: "A. H." },
  { quote: "Chris texted me back within seconds and had my prescription over to the pharmacy within minutes. So simple and easy.", name: "J. R." },
  { quote: "Messaged Chris, he responded in a timely manner. Very professional. Easy to talk to about our concerns.", name: "T. P." },
] as const;

export const states = ["Arizona", "Colorado", "Georgia", "Idaho", "Iowa", "Montana", "Nevada", "New Mexico", "North Carolina", "Oregon", "Utah"] as const;

export const faqs = [
  { question: "What happens when I text Chris?", answer: "Tell Chris what is going on in your own words. He will review it, ask what he needs to know, and explain the safest next step." },
  { question: "What does a visit cost?", answer: "$59 flat fee. No hidden fees and no subscription." },
  { question: "What if text-based care is not the safe fit?", answer: "Chris will tell you plainly when you need in-person or emergency care." },
] as const;
```

- [ ] **Step 2: Add the decorative thread component**

Create `app/components/ThreadPath.tsx`:

```tsx
export function ThreadPath() {
  return (
    <div className="thread-layer" aria-hidden="true">
      <div className="thread-path" />
      <div className="thread-progress" />
    </div>
  );
}
```

- [ ] **Step 3: Create the semantic server-rendered content component**

Create `app/components/HomepageContent.tsx` with:

```tsx
import Image from "next/image";
import { ThreadPath } from "./ThreadPath";
import { chapters, faqs, reviews, smsHref, states } from "../homepage-content";

export function HomepageContent() {
  return (
    <>
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <nav className="site-nav" aria-label="Primary navigation">
        <a className="brand" href="#top">NPCWoods <span>Telemedicine</span></a>
        <a className="nav-cta" href={smsHref}>Text Chris · $59</a>
      </nav>
      <main id="main-content">
        <div id="top" />
        <ThreadPath />
        <section className="chapter chapter-hook" data-chapter="hook" aria-labelledby="hook-title">
          <div className="chapter-copy">
            <p className="eyebrow">Straightforward care, from a real person</p>
            <h1 id="hook-title">{chapters[0].title}</h1>
            <p className="lede">{chapters[0].body}</p>
            <div className="hero-actions"><a className="button button-primary" href={smsHref}>Text Chris now</a><a className="button button-quiet" href="#friction">Follow the journey</a></div>
            <ul className="trust-list"><li>$59 flat fee</li><li>Licensed in 11 states</li><li>Usually back to you within an hour during business hours</li></ul>
          </div>
          <figure className="hero-portrait">
            <Image src="/chris-1000.webp" alt="Chris Woods, NP" width={1000} height={1250} priority />
            <figcaption>Chris Woods, MSN, APRN, FNP-C</figcaption>
          </figure>
        </section>

        <section id="friction" className="chapter chapter-friction" data-chapter="friction" aria-labelledby="friction-title"><div className="chapter-copy"><p className="chapter-number">02</p><h2 id="friction-title">{chapters[1].title}</h2><p>{chapters[1].body}</p><div className="obstacles"><span>Drive</span><span>Wait</span><span>Forms</span></div></div></section>
        <section className="chapter chapter-guide" data-chapter="guide" aria-labelledby="guide-title"><figure><Image src="/chris-1000.webp" alt="Chris Woods, Nurse Practitioner" width={1000} height={1250} /></figure><div className="chapter-copy"><p className="chapter-number">03</p><h2 id="guide-title">{chapters[2].title}</h2><p>{chapters[2].body}</p><blockquote><span className="guide-thread-tail" aria-hidden="true" />Just text me.</blockquote></div></section>
        <section className="chapter chapter-conversation" data-chapter="conversation" aria-labelledby="conversation-title"><div className="conversation-stage"><div className="chapter-copy"><p className="chapter-number">04</p><h2 id="conversation-title">{chapters[3].title}</h2><p>{chapters[3].body}</p></div><ol className="message-list"><li className="message visitor">Here’s what’s going on…</li><li className="message chris">I’ve got it. Let me review this.</li><li className="message chris">Here are your next steps.</li></ol></div></section>
        <section className="chapter chapter-resolution" data-chapter="resolution" aria-labelledby="resolution-title"><div className="chapter-copy"><p className="chapter-number">05</p><h2 id="resolution-title">{chapters[4].title}</h2><p>{chapters[4].body}</p><div className="resolution-ring"><a className="button button-primary" href={smsHref}>Text Chris now</a></div></div></section>

        <section className="proof-section" aria-labelledby="reviews-title"><p className="eyebrow">Real people</p><h2 id="reviews-title">Real texts. Real relief.</h2><div className="review-grid">{reviews.map((review) => <figure className="review" key={review.name}><blockquote>“{review.quote}”</blockquote><figcaption>{review.name}</figcaption></figure>)}</div></section>
        <section className="states-section" aria-labelledby="states-title"><p className="eyebrow">Where Chris can help</p><h2 id="states-title">Licensed in 11 states.</h2><ul className="state-list">{states.map((state) => <li key={state}>{state}</li>)}</ul></section>
        <section className="safety-section" aria-labelledby="safety-title"><p className="eyebrow">Straight answers</p><h2 id="safety-title">Some symptoms need in-person care.</h2><p>Chris will tell you plainly when text-based care is not the safe fit. If symptoms may be life-threatening, call 911 or seek emergency care now.</p></section>
        <section className="faq-section" aria-labelledby="faq-title"><p className="eyebrow">Common questions</p><h2 id="faq-title">Before you text.</h2><div className="faq-list">{faqs.map((faq) => <details key={faq.question}><summary>{faq.question}</summary><p>{faq.answer}</p></details>)}</div></section>
        <section className="final-section" aria-labelledby="final-title"><h2 id="final-title">Feeling rough? Just text me.</h2><p>$59 flat fee. No hidden fees.</p><a className="button button-primary" href={smsHref}>Text Chris now</a></section>
      </main>
      <a className="mobile-text-bar" href={smsHref}>Text Chris now · $59</a>
    </>
  );
}
```

- [ ] **Step 4: Replace the starter page with the finished content component**

Replace `app/page.tsx` with:

```tsx
import { HomepageContent } from "./components/HomepageContent";

export default function Home() {
  return <HomepageContent />;
}
```

- [ ] **Step 5: Finish metadata**

Set `app/layout.tsx` metadata to:

```ts
export const metadata: Metadata = {
  title: "NPCWoods Telemedicine | $59 Text-Based Care with Chris Woods, NP",
  description: "$59 text-based telemedicine with Chris Woods, NP. Straightforward care from home in 11 states.",
  icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
};
```

- [ ] **Step 6: Archive the starter and update dependencies**

Run:

```bash
mkdir -p archive/starter
mv app/_sites-preview/SkeletonPreview.tsx archive/starter/SkeletonPreview.tsx
mv app/_sites-preview/preview.css archive/starter/preview.css
rmdir app/_sites-preview
npm uninstall react-loading-skeleton
```

Expected: the starter files are preserved under `archive/starter/`, the imported starter directory is gone, and `react-loading-skeleton` is absent from both package files.

- [ ] **Step 7: Copy approved portrait assets**

Run:

```bash
cp ../../assets/homepage-v2/chris-1000.webp public/chris-1000.webp
cp ../../assets/homepage-v2/chris-400.webp public/chris-400.webp
```

- [ ] **Step 8: Commit the semantic page**

```bash
git add output/sites-homepage-preview
git commit -m "[homepage] add semantic visitor journey"
```

## Task 3: Build the Responsive Visual System

**Files:**
- Replace: `output/sites-homepage-preview/app/globals.css`

- [ ] **Step 1: Add the foundation and chapter layout**

Replace starter CSS with exact design tokens and structural rules:

```css
@import "tailwindcss";
:root{--pressure:#1b201d;--cream:#f7f2e8;--paper:#fffdf8;--cobalt:#2855c7;--cobalt-deep:#183f9e;--clay:#bd5a42;--green:#1c8a5c;--ink:#203128;--muted:#647068;--hair:rgba(32,49,40,.15);--gutter:clamp(20px,5vw,64px);--max:1180px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--font-geist-sans),Arial,sans-serif;overflow-x:hidden}a{color:inherit}.skip-link{position:fixed;left:16px;top:-80px;z-index:100;background:var(--paper);padding:12px 16px;border-radius:0 0 10px 10px}.skip-link:focus{top:0}
.site-nav{height:68px;display:flex;align-items:center;justify-content:space-between;padding:0 var(--gutter);position:relative;z-index:20;background:rgba(247,242,232,.9);backdrop-filter:blur(16px);border-bottom:1px solid var(--hair)}.brand{text-decoration:none;font-weight:800}.brand span{display:block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.nav-cta,.button{min-height:48px;display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:12px 22px;text-decoration:none;font-weight:800}.nav-cta,.button-primary{background:var(--cobalt);color:#fff;box-shadow:0 8px 0 var(--cobalt-deep)}.button-quiet{border:1px solid var(--hair);background:rgba(255,255,255,.55)}
main{position:relative}.chapter,.proof-section,.states-section,.safety-section,.faq-section,.final-section{width:min(var(--max),100%);margin:0 auto;padding:clamp(72px,10vw,140px) var(--gutter);position:relative}.chapter{min-height:100svh;display:grid;align-items:center}.chapter-copy{position:relative;z-index:3;max-width:650px}.eyebrow,.chapter-number{font:700 11px/1.2 var(--font-geist-mono),monospace;letter-spacing:.15em;text-transform:uppercase;color:var(--muted)}h1,h2{font-family:Georgia,serif;letter-spacing:-.05em;line-height:.94;margin:.2em 0}h1{font-size:clamp(3.7rem,9vw,8.3rem)}h2{font-size:clamp(2.8rem,7vw,6rem)}.lede,.chapter-copy>p{font-size:clamp(1.05rem,2vw,1.35rem);line-height:1.55}.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin:30px 0}.trust-list{display:flex;gap:12px;flex-wrap:wrap;list-style:none;padding:0}.trust-list li{padding:8px 11px;background:rgba(255,255,255,.72);border:1px solid var(--hair);border-radius:999px;font-size:12px;font-weight:700}
.chapter-hook{grid-template-columns:1.05fr .95fr;gap:clamp(28px,6vw,80px)}.hero-portrait img,.chapter-guide img{display:block;width:100%;height:auto;border-radius:45% 45% 18px 18px}.hero-portrait figcaption{font:700 11px var(--font-geist-mono);margin-top:10px}.chapter-friction{background:var(--pressure);color:#fff;width:100%;max-width:none}.chapter-friction .chapter-copy{width:min(var(--max),100%);margin:auto}.obstacles{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.obstacles span{padding:24px 30px;border:1px solid rgba(255,255,255,.2);border-radius:16px}.chapter-guide{grid-template-columns:.85fr 1.15fr;gap:clamp(30px,6vw,90px)}.chapter-guide figure{margin:0}.chapter-guide blockquote{font:italic 600 clamp(2rem,5vw,4.5rem) Georgia,serif;color:var(--cobalt);margin:30px 0}.chapter-conversation{min-height:260svh}.conversation-stage{position:sticky;top:0;min-height:100svh;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:40px}.message-list{list-style:none;padding:0;display:grid;gap:12px}.message{max-width:82%;padding:17px 20px;border-radius:20px;background:#fff;box-shadow:0 14px 35px rgba(32,49,40,.12)}.message.chris{margin-left:auto;background:var(--cobalt);color:#fff}.chapter-resolution{text-align:center;place-items:center}.chapter-resolution .chapter-copy{display:grid;justify-items:center}.resolution-ring{width:min(390px,90vw);aspect-ratio:1;border:5px solid var(--green);border-radius:50%;display:grid;place-items:center;margin-top:30px}.review-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.review{margin:0;padding:24px;background:var(--paper);border:1px solid var(--hair);border-radius:18px}.review blockquote{margin:0 0 14px;line-height:1.55}.state-list{display:flex;gap:9px;flex-wrap:wrap;list-style:none;padding:0}.state-list li{padding:9px 13px;background:var(--paper);border:1px solid var(--hair);border-radius:999px}.safety-section{background:#f0e4d7;border-radius:28px}.safety-section>p:last-child{max-width:68ch;line-height:1.6}.faq-list{display:grid;gap:10px}.faq-list details{background:var(--paper);border:1px solid var(--hair);border-radius:16px;padding:18px 20px}.faq-list summary{cursor:pointer;font-weight:800}.faq-list p{color:var(--muted);line-height:1.55}.final-section{text-align:center;background:var(--pressure);color:#fff;width:100%;max-width:none}.mobile-text-bar{display:none}
```

- [ ] **Step 2: Add the mobile and accessibility rules**

Append:

```css
@media(max-width:760px){.site-nav{height:60px}.nav-cta{display:none}.chapter{min-height:auto;padding-top:86px;padding-bottom:92px}.chapter-hook,.chapter-guide,.conversation-stage{grid-template-columns:1fr}.hero-portrait{order:-1;margin:0 auto;max-width:290px}.hero-actions .button{width:100%}.trust-list{display:grid}.chapter-conversation{min-height:210svh}.conversation-stage{align-content:center;padding:72px 0}.review-grid{grid-template-columns:1fr}.mobile-text-bar{display:flex;position:fixed;z-index:50;left:12px;right:12px;bottom:12px;min-height:54px;align-items:center;justify-content:center;background:var(--cobalt);color:#fff;border-radius:999px;text-decoration:none;font-weight:800;box-shadow:0 8px 24px rgba(24,63,158,.35)}.final-section{padding-bottom:110px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}.chapter-conversation{min-height:auto}.conversation-stage{position:relative;min-height:auto}.message{opacity:1!important;transform:none!important}.thread-progress{transform:scaleY(1)!important}.guide-thread-tail{transform:scaleX(1)!important}}
:focus-visible{outline:3px solid #d9a441;outline-offset:4px}
```

- [ ] **Step 3: Run the rendered contract**

Run: `npm test`

Expected: rendered content test passes; motion source test still fails because the controller is not present.

- [ ] **Step 4: Commit the visual foundation**

```bash
git add output/sites-homepage-preview/app/globals.css
git commit -m "[homepage] add responsive cinematic visual system"
```

## Task 4: Implement the Living Thread and Scroll Controller

**Files:**
- Create: `output/sites-homepage-preview/app/components/FollowThread.tsx`
- Modify: `output/sites-homepage-preview/app/page.tsx`
- Modify: `output/sites-homepage-preview/package.json`
- Modify: `output/sites-homepage-preview/package-lock.json`
- Modify: `output/sites-homepage-preview/app/globals.css`

- [ ] **Step 1: Install GSAP**

Run: `npm install gsap`

Expected: `gsap` appears in dependencies and the lockfile changes.

- [ ] **Step 2: Create the scoped controller**

Create `app/components/FollowThread.tsx`:

```tsx
"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function FollowThread({ children }: { children: React.ReactNode }) {
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;

    const mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: reduce)", () => {
      root.dataset.motion = "reduced";
      gsap.set(root.querySelectorAll(".message,.obstacles span"), { clearProps: "all" });
    });
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      root.dataset.motion = "full";
      gsap.fromTo(".thread-progress", { scaleY: 0 }, { scaleY: 1, ease: "none", scrollTrigger: { trigger: root, start: "top top", end: "bottom bottom", scrub: 0.4 } });
      gsap.to(".obstacles span", { xPercent: (index) => index % 2 ? 35 : -35, opacity: 0.25, stagger: 0.08, scrollTrigger: { trigger: ".chapter-friction", start: "top 45%", end: "bottom 45%", scrub: true } });
      gsap.from(".chapter-guide figure", { yPercent: 14, scale: 0.9, opacity: 0, scrollTrigger: { trigger: ".chapter-guide", start: "top 75%", end: "center 55%", scrub: true } });
      gsap.fromTo(".guide-thread-tail", { scaleX: 0 }, { scaleX: 1, ease: "none", scrollTrigger: { trigger: ".chapter-guide", start: "top 70%", end: "center 50%", scrub: true } });
      gsap.from(".message", { y: 50, opacity: 0, stagger: 0.35, scrollTrigger: { trigger: ".chapter-conversation", start: "top top", end: "bottom bottom", scrub: true } });
      gsap.from(".resolution-ring", { scale: 0.65, rotate: -18, opacity: 0, scrollTrigger: { trigger: ".chapter-resolution", start: "top 75%", end: "center 55%", scrub: true } });
    });

    return () => mm.revert();
  }, []);

  return <div ref={rootRef}>{children}</div>;
}
```

- [ ] **Step 3: Wrap the page**

Import the controller and wrap all page output:

```tsx
import { FollowThread } from "./components/FollowThread";
import { HomepageContent } from "./components/HomepageContent";

export default function Home() {
  return <FollowThread><HomepageContent /></FollowThread>;
}
```

- [ ] **Step 4: Add the thread geometry**

Append to `globals.css`:

```css
.thread-layer{position:absolute;z-index:2;left:clamp(22px,4vw,54px);top:20px;bottom:20px;width:16px;pointer-events:none}.thread-path,.thread-progress{position:absolute;inset:0 auto 0 5px;width:5px;border-radius:999px;transform-origin:top}.thread-path{background:rgba(32,49,40,.12)}.thread-progress{background:linear-gradient(to bottom,var(--clay) 0 20%,var(--cobalt) 42% 80%,var(--green) 100%);box-shadow:0 0 0 7px rgba(40,85,199,.05)}.chapter-guide blockquote{position:relative}.guide-thread-tail{position:absolute;right:calc(100% + 16px);top:50%;width:clamp(36px,8vw,110px);height:5px;border-radius:999px;background:var(--cobalt);transform-origin:right}
@media(min-width:1000px){.thread-layer{left:50%;transform:translateX(-50%);margin-left:-590px}}
```

- [ ] **Step 5: Run tests**

Run: `npm test`

Expected: both test files pass.

- [ ] **Step 6: Commit the scroll experience**

```bash
git add output/sites-homepage-preview
git commit -m "[homepage] animate the visitor journey thread"
```

## Task 5: Add the Social Preview and Final Metadata

**Files:**
- Create: `output/sites-homepage-preview/public/og.png`
- Modify: `output/sites-homepage-preview/app/layout.tsx`
- Modify: `output/sites-homepage-preview/tests/source-contract.test.mjs`

- [ ] **Step 1: Add a failing social metadata contract**

Append to `tests/source-contract.test.mjs`:

```js
test("ships a bespoke social card and metadata", async () => {
  const [layout] = await Promise.all([read("app/layout.tsx")]);
  await access(new URL("public/og.png", root));
  assert.match(layout, /openGraph/);
  assert.match(layout, /twitter/);
  assert.match(layout, /x-forwarded-host/);
  assert.match(layout, /metadataBase/);
  assert.match(layout, /\/og\.png/);
});
```

- [ ] **Step 2: Generate one cohesive social card**

Use one image generation request with this exact creative brief:

```text
Create a complete 1200×630 social preview image for NPCWoods Telemedicine. Use the finished homepage’s warm cream, ink, cobalt, clay, and green palette. Feature Chris Woods, NP, as a real approachable guide and a single living thread moving from tangled clay to confident cobalt and calm green. Include the exact readable text: “Feeling rough? Just text me.” and “$59 flat fee”. Premium editorial typography, warm human tone, high legibility in small link previews, no stock clinical scene, no device mockup, no unrelated logos, no watermark.
```

Inspect the result. Save it as `public/og.png` only if both required text strings are correct and legible. Retry once if unusable; otherwise omit social image metadata.

- [ ] **Step 3: Add host-derived social metadata**

Import `headers` from `next/headers`, remove the static `metadata` export, and add:

```ts
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const incoming = await headers();
  const host = incoming.get("x-forwarded-host") ?? incoming.get("host") ?? "localhost:3000";
  const protocol = incoming.get("x-forwarded-proto") ?? (host.startsWith("localhost") ? "http" : "https");
  const metadataBase = new URL(`${protocol}://${host}`);
  const socialImage = new URL("/og.png", metadataBase).toString();

  return {
    metadataBase,
    title: "NPCWoods Telemedicine | $59 Text-Based Care with Chris Woods, NP",
    description: "$59 text-based telemedicine with Chris Woods, NP. Straightforward care from home in 11 states.",
    icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
    openGraph: {
      title: "Feeling rough? Just text me.",
      description: "$59 text-based telemedicine with Chris Woods, NP.",
      images: [{ url: socialImage, width: 1200, height: 630, alt: "NPCWoods Telemedicine, $59 flat fee" }],
    },
    twitter: {
      card: "summary_large_image",
      title: "Feeling rough? Just text me.",
      description: "$59 text-based telemedicine with Chris Woods, NP.",
      images: [socialImage],
    },
  };
}
```

- [ ] **Step 4: Run tests and commit**

Run: `npm test`

Expected: PASS.

```bash
git add output/sites-homepage-preview/public/og.png output/sites-homepage-preview/app/layout.tsx output/sites-homepage-preview/tests/source-contract.test.mjs
git commit -m "[homepage] add cinematic social preview"
```

## Task 6: Validate the Private Preview

**Files:**
- Verify only: `output/sites-homepage-preview/`
- Verify untouched: `homepage/page-npcwoods-home.php`

- [ ] **Step 1: Run the complete automated suite**

Run: `npm test`

Expected: build succeeds and all tests pass.

- [ ] **Step 2: Run lint**

Run: `npm run lint`

Expected: zero lint errors.

- [ ] **Step 3: Check the forbidden-marketing-word contract in rendered output**

Run:

```bash
rg -ni '\b(doctor|physician|appointment|insurance)\b' dist/client dist/server || true
```

Expected: no visitor-facing matches. Dependency or source-map matches must be inspected and excluded from the conclusion.

- [ ] **Step 4: Confirm the live homepage file was not changed by preview work**

Run:

```bash
git hash-object homepage/page-npcwoods-home.php
```

Expected exactly: `eb81b99ebbced5b0f4a83428c4eb05c436eed8e5`. A different hash means the live homepage source changed after the approved design and must be investigated before continuing.

- [ ] **Step 5: Verify phone, desktop, keyboard, and reduced motion**

Use the retained local preview and inspect:

- 360×800 phone layout
- 1440×900 desktop layout
- Keyboard path to the primary SMS action within six tab stops
- Visible skip link and focus states
- Reduced-motion static layout
- No horizontal overflow
- Sticky conversation releases normally

Expected: all checks pass. Fix and rerun build if any fail.

- [ ] **Step 6: Commit validation fixes, if any**

```bash
git add output/sites-homepage-preview
git commit -m "[homepage] finish private preview validation"
```

## Task 7: Save and Publish the Owner-Only Sites Preview

**Files:**
- Modify: `output/sites-homepage-preview/.openai/hosting.json`
- Package: temporary Sites deployment archive

- [ ] **Step 1: Reuse the successful build**

Do not rebuild unless source changed after Task 6.

- [ ] **Step 2: Create the Sites project once**

Use title `NPCWoods Homepage — Follow the Thread`, description `Private cinematic homepage concept for Chris review`, and an available slug beginning with `npcwoods-follow-thread`.

Persist only the returned opaque `project_id` in `.openai/hosting.json`.

- [ ] **Step 3: Commit and push the exact validated source state**

Commit only the preview files and hosting metadata. Push with the short-lived per-command Sites credential. Never persist the token.

- [ ] **Step 4: Package and save one version**

Use the Sites packaging helper against `output/sites-homepage-preview/`, then save one version using the pushed branch-head SHA and exact archive.

- [ ] **Step 5: Deploy owner-only**

Use the verified owner-only private deployment method. Do not call the shared/public deployment method without a new explicit approval from Chris.

- [ ] **Step 6: Poll to completion**

Poll the deployment status until it succeeds or fails. On success, open the exact returned URL in Codex and deliver it as the primary artifact.

- [ ] **Step 7: Final handoff**

Report:

- The private Sites URL
- That the live NPCWoods homepage was not changed
- The key verified behaviors: mobile layout, reduced motion, keyboard path, and successful build
- That any future production change still requires separate explicit approval
