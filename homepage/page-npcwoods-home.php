<?php
/**
 * Template Name: NPCWoods Homepage
 * Scroll plate live 2026-09-07. Chris: push the npcwoods scroll plate live.
 * Approved Meta Pixels live in this template after wp_head():
 * 1558261907814968 (ads) and 1428464038973925 (site).
 * Do not enqueue TT4 / wp-block-library on this template.
 */
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#F6F3EE" />
  <title>NPCWoods Telemedicine: $59 Text-Based Urgent Care</title>
  <link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg" />
  <link rel="preload" as="image" href="https://npcwoods.com/wp-content/uploads/2026/04/chris-400.webp" imagesrcset="https://npcwoods.com/wp-content/uploads/2026/04/chris-400.webp 400w, https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp 1000w" imagesizes="(max-width:900px) 100vw, 520px" fetchpriority="high" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<?php if (function_exists('wp_head')) { wp_head(); } ?>
<!-- Meta Pixel Code: load after idle or first tap so phones stay snappy. -->
<script>
(function () {
  var loaded = false;
  function loadPixel() {
    if (loaded) return;
    loaded = true;
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '1558261907814968');
    fbq('init', '1428464038973925');
    fbq('track', 'PageView');
  }
  function fireContact() {
    loadPixel();
    if (typeof fbq !== 'function') return;
    fbq('track', 'Contact');
    fbq('trackCustom', 'ContactSent');
  }
  function schedulePixel() {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(function () { loadPixel(); }, { timeout: 8000 });
    } else {
      setTimeout(loadPixel, 8000);
    }
  }
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {
    window.addEventListener(ev, loadPixel, { once: true, passive: true });
  });
  if (document.readyState === 'complete') schedulePixel();
  else window.addEventListener('load', schedulePixel);
  document.addEventListener('click', function (e) {
    var t = e.target;
    var a = t && t.closest ? t.closest('a[href^="sms:"]') : null;
    if (a) fireContact();
  });
})();
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1558261907814968&ev=PageView&noscript=1"
/></noscript>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1428464038973925&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
  <style>
    :root {
      --ink: #1A1A2E;
      --muted: #5B5B6B;
      --blue: #2563EB;
      --blue-dark: #1D4ED8;
      --cream: #F6F3EE;
      --white: #FFFFFF;
      --line: rgba(26, 26, 46, 0.08);
      --shadow: 0 20px 50px rgba(26, 26, 46, 0.12);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: Inter, system-ui, sans-serif;
      color: var(--ink);
      background: var(--cream);
      -webkit-font-smoothing: antialiased;
      line-height: 1.5;
    }
    img { max-width: 100%; display: block; }
    a { color: inherit; }
    #npcSaveWrap, body::after { display: none !important; content: none !important; }
    .skip-link{position:absolute;left:-9999px;top:0;z-index:2000;padding:10px 16px;background:#fff;color:#000;font-weight:700}
    .skip-link:focus{left:14px}
    .nav {
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 18px;
      background: rgba(246, 243, 238, 0.86);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--line);
    }
    .brand { display: flex; align-items: center; gap: 10px; text-decoration: none; }
    .brand img { width: 38px; height: 38px; border-radius: 10px; object-fit: cover; }
    .brand-name { font-family: "DM Serif Display", serif; font-size: 1.15rem; line-height: 1; }
    .brand-tag {
      font-family: "DM Sans", sans-serif;
      font-size: 0.62rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--blue);
      margin-top: 3px;
    }
    .nav-cta {
      display: inline-flex;
      align-items: center;
      background: linear-gradient(135deg, var(--blue), var(--blue-dark));
      color: #fff !important;
      -webkit-text-fill-color: #fff;
      text-decoration: none;
      font-family: "DM Sans", sans-serif;
      font-weight: 600;
      font-size: 0.86rem;
      padding: 10px 16px;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.28);
    }
    .wrap { max-width: 720px; margin: 0 auto; padding: 0 20px; }
    .hero { padding: 36px 20px 20px; text-align: left; }
    .eyebrow {
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--blue);
      margin-bottom: 14px;
    }
    h1 {
      font-family: "DM Serif Display", serif;
      font-size: clamp(2.15rem, 8vw, 3.4rem);
      line-height: 1.05;
      letter-spacing: -0.02em;
      font-weight: 400;
    }
    h1 em { font-style: italic; color: var(--blue); }
    .lede { margin-top: 16px; font-size: 1.08rem; color: var(--muted); max-width: 34rem; }
    .photo-stage { padding: 12px 16px 8px; }
    .photo-card {
      position: relative;
      border-radius: 22px;
      overflow: hidden;
      box-shadow: var(--shadow);
      background: #d8d4ce;
    }
    .photo-card img {
      width: 100%;
      aspect-ratio: 4 / 5;
      object-fit: cover;
      object-position: 50% 18%;
    }
    .price-pill {
      position: absolute;
      left: 14px;
      bottom: 14px;
      background: #fff;
      border-radius: 16px;
      padding: 10px 14px;
      display: flex;
      align-items: baseline;
      gap: 8px;
      box-shadow: 0 10px 24px rgba(0,0,0,0.12);
    }
    .price-pill strong {
      font-family: "DM Serif Display", serif;
      font-size: 1.6rem;
      color: var(--blue);
      line-height: 1;
    }
    .price-pill span { font-size: 0.78rem; color: var(--muted); line-height: 1.2; }
    section { padding: 56px 0 8px; }
    h2 {
      font-family: "DM Serif Display", serif;
      font-size: clamp(1.7rem, 6vw, 2.4rem);
      line-height: 1.12;
      letter-spacing: -0.02em;
    }
    .section-copy { margin-top: 12px; color: var(--muted); font-size: 1.05rem; }
    .pain-list { margin-top: 28px; display: grid; gap: 12px; }
    .pain {
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 16px 16px 16px 18px;
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 12px;
      align-items: start;
    }
    .x {
      width: 22px;
      height: 22px;
      border-radius: 999px;
      background: #F3E8E8;
      color: #B42318;
      display: grid;
      place-items: center;
      font-size: 0.8rem;
      font-weight: 700;
      margin-top: 2px;
    }
    .pain h3 { font-size: 1rem; margin-bottom: 2px; }
    .pain p { color: var(--muted); font-size: 0.92rem; }
    .quote-block { margin-top: 28px; padding: 4px 0 0; }
    .quote-block p {
      font-family: "DM Serif Display", serif;
      font-size: 1.35rem;
      line-height: 1.3;
    }
    .steps { margin-top: 28px; display: grid; gap: 14px; }
    .step {
      background: #fff;
      border-radius: 18px;
      padding: 18px 18px 18px 16px;
      border: 1px solid var(--line);
      display: grid;
      grid-template-columns: 42px 1fr;
      gap: 12px;
    }
    .num {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: #EFF6FF;
      color: var(--blue);
      display: grid;
      place-items: center;
      font-family: "DM Sans", sans-serif;
      font-weight: 700;
    }
    .step h3 { font-size: 1.05rem; margin-bottom: 4px; }
    .step p { color: var(--muted); font-size: 0.95rem; }
    .price-block {
      margin: 36px 16px 0;
      background: var(--ink);
      color: #fff;
      border-radius: 24px;
      padding: 32px 24px;
      text-align: center;
    }
    .price-block .big {
      font-family: "DM Serif Display", serif;
      font-size: 4.2rem;
      line-height: 1;
    }
    .price-block h2 { color: #fff; margin-top: 8px; }
    .price-block p { color: rgba(255,255,255,0.78); margin-top: 10px; }
    .cta-row { display: flex; flex-direction: column; gap: 10px; margin-top: 22px; }
    .btn {
      display: inline-flex;
      justify-content: center;
      align-items: center;
      text-decoration: none;
      border-radius: 14px;
      padding: 14px 18px;
      font-family: "DM Sans", sans-serif;
      font-weight: 650;
      font-size: 1rem;
    }
    .btn-primary {
      background: linear-gradient(135deg, var(--blue), var(--blue-dark));
      color: #fff !important;
      -webkit-text-fill-color: #fff;
      box-shadow: 0 8px 22px rgba(37,99,235,0.35);
    }
    .btn-light { background: #fff; color: var(--ink); border: 1px solid var(--line); }
    .reviews { margin-top: 28px; display: grid; gap: 12px; }
    .review {
      background: #fff;
      border-radius: 16px;
      padding: 16px;
      border: 1px solid var(--line);
    }
    .stars { color: #E2A03A; letter-spacing: 1px; font-size: 0.85rem; margin-bottom: 6px; }
    .review p { font-size: 0.95rem; }
    .review cite { display: block; margin-top: 8px; color: var(--muted); font-style: normal; font-size: 0.82rem; }
    .states { margin-top: 18px; color: var(--muted); font-size: 0.95rem; }
    .safety {
      max-width: 720px;
      margin: 40px auto 0;
      padding: 22px 20px;
      border: 2px solid #fda29b;
      background: #fff1f0;
      border-radius: 20px;
    }
    .safety b { display: block; color: #b42318; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; }
    .safety p { color: #7a271a; margin-top: 8px; }
    .finale { padding: 48px 20px 80px; text-align: center; }
    .finale h2 { margin-bottom: 10px; }
    .finale .lede { margin: 0 auto 22px; }
    .fine { margin-top: 18px; font-size: 0.82rem; color: var(--muted); }
    .reveal { opacity: 0; transform: translateY(18px); animation: up 0.7s ease forwards; }
    .d1 { animation-delay: 0.05s; }
    .d2 { animation-delay: 0.14s; }
    .d3 { animation-delay: 0.22s; }
    @keyframes up { to { opacity: 1; transform: none; } }
    @media (prefers-reduced-motion: reduce) {
      .reveal { opacity: 1; transform: none; animation: none; }
    }
    @media (min-width: 860px) {
      .hero-grid {
        max-width: 1080px;
        margin: 0 auto;
        padding: 48px 28px 20px;
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 48px;
        align-items: center;
      }
      .photo-stage { padding: 0; }
      .photo-card img { aspect-ratio: 4 / 5; max-height: 640px; }
      .cta-row { flex-direction: row; justify-content: center; }
      .btn { min-width: 220px; }
    }
  </style>
</head>
<body class="npc-redesign">
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="nav">
    <a class="brand" href="https://npcwoods.com/">
      <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="Chris Woods, NP" width="38" height="38" />
      <span>
        <span class="brand-name">NPCWoods</span>
        <span class="brand-tag">Telemedicine</span>
      </span>
    </a>
    <a class="nav-cta" href="sms:+14806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">$59. Text Chris</a>
  </header>
  <main id="main">
  <div class="hero-grid">
    <section class="hero">
      <p class="eyebrow reveal">NPCWoods · 11 states</p>
      <h1 class="reveal d1">You feel awful.<br>The system makes you <em>work</em> for it.</h1>
      <p class="lede reveal d2">A half-day in a waiting room for a ten-minute problem. Or you text me from the couch. Same problem. Different day.</p>
    </section>
    <div class="photo-stage reveal d3">
      <div class="photo-card">
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, Nurse Practitioner" width="1000" height="1250" />
        <div class="price-pill">
          <strong>$59</strong>
          <span>flat fee<br>pay after care</span>
        </div>
      </div>
    </div>
  </div>
  <section>
    <div class="wrap">
      <h2>The old way is the expensive part.</h2>
      <p class="section-copy">Not the medicine. Not the visit. The runaround.</p>
      <div class="pain-list">
        <article class="pain"><div class="x">×</div><div><h3>3-hour waits</h3><p>A half-day in an urgent care lobby for something I can sort out in a few texts.</p></div></article>
        <article class="pain"><div class="x">×</div><div><h3>$200 for a $20 fix</h3><p>Surprise bills for simple care you already knew you needed.</p></div></article>
        <article class="pain"><div class="x">×</div><div><h3>No clinic close by</h3><p>The nearest option is far, closed, or booked out for days.</p></div></article>
        <article class="pain"><div class="x">×</div><div><h3>Forms and denials</h3><p>Portals, paperwork, and fine print after the fact.</p></div></article>
      </div>
      <div class="quote-block"><p>I built the practice I would want for my own family.</p></div>
    </div>
  </section>
  <section>
    <div class="wrap">
      <p class="eyebrow">How it works</p>
      <h2>Three texts from feeling better.</h2>
      <p class="section-copy">Usually within a few hours — first text to the pharmacy.</p>
      <div class="steps">
        <article class="step"><div class="num">01</div><div><h3>Text me your symptoms</h3><p>In your own words. No 30-question form. No portal. No app.</p></div></article>
        <article class="step"><div class="num">02</div><div><h3>I actually read it</h3><p>I look at your history, ask what I need, and build a plan for you. Not a template. Not a bot.</p></div></article>
        <article class="step"><div class="num">03</div><div><h3>Pick up and feel better</h3><p>Sent to your pharmacy. Written plan to your inbox. That is it.</p></div></article>
      </div>
    </div>
  </section>
  <div class="price-block">
    <div class="big">$59</div>
    <h2>That’s the whole thing.</h2>
    <p>Pay after you’re treated. If I can’t safely help you by text, I’ll tell you straight up — and you don’t pay a dime.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="sms:+14806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now</a>
    </div>
  </div>
  <section>
    <div class="wrap">
      <h2>Real texts. Real relief.</h2>
      <div class="reviews">
        <article class="review"><div class="stars">★★★★★</div><p>“I first messaged Chris at 10:08am and I was picking up my prescriptions at 10:52am same day.”</p><cite>A. H.</cite></article>
        <article class="review"><div class="stars">★★★★★</div><p>“I texted Chris out of nowhere on a Sunday and he answered straight away. Lightning-quick.”</p><cite>B. P.</cite></article>
        <article class="review"><div class="stars">★★★★★</div><p>“I texted Chris at 10pm and he responded within 15 minutes. When the pharmacy didn’t have it, he called the store himself.”</p><cite>M. D.</cite></article>
      </div>
      <p class="states">Licensed in Arizona, Colorado, Georgia, Idaho, Iowa, Montana, Nevada, New Mexico, North Carolina, Oregon, and Utah.</p>
    </div>
  </section>
  <div class="wrap">
    <div class="safety">
      <b>Emergencies</b>
      <p>Text care is not for chest pain, trouble breathing, severe allergic reaction, or anything that feels life-threatening. Call 911 or go to the nearest emergency room.</p>
    </div>
  </div>
  <section class="finale">
    <h2>Text me. I’ve got you.</h2>
    <p class="lede">$59 flat. A real Nurse Practitioner. Right from your couch.</p>
    <div class="cta-row" style="max-width: 420px; margin-left: auto; margin-right: auto;">
      <a class="btn btn-primary" href="sms:+14806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now</a>
      <a class="btn btn-light" href="https://npcwoods.com/chris-woods.vcf">Save my number as “sick guy”</a>
    </div>
    <p class="fine">Chris Woods, MSN, APRN, FNP-C · Not a chatbot · Pay after care</p>
  </section>
  </main>
<?php if (function_exists('wp_footer')) { wp_footer(); } ?>
</body>
</html>
