<?php
/**
 * Template Name: NPCWoods Homepage
 * Design v3 (2026-06-25): story-driven, photo-rich, Chris's voice. Real portrait anchors hero +
 * "Meet Chris". Scoped under #main.npc-redesign so it cannot disturb shared nav/footer (site.css)
 * or theme globals. Tracking (GA4/Ads/GTM/tracking.js) rides on wp_head()/wp_footer().
 * Reviews intentionally omitted until Chris supplies verified ones. Lifestyle/step images are
 * temporary stand-ins (wp-content/uploads/2026/06/) pending Chris's real photos.
 */
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#FBF7F0">
<title>NPCWoods Telemedicine: $59 Text-Based Urgent Care</title>
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://unpkg.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap" rel="stylesheet">
<?php if (function_exists('wp_head')) { wp_head(); } ?>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<?php
$npcwoods_header_rendered = false;
$npcwoods_header_candidates = array();
if (defined('ABSPATH')) {
  $npcwoods_header_candidates[] = rtrim(ABSPATH, '/\\') . '/shared/header-snippet.html';
}
$npcwoods_header_candidates[] = __DIR__ . '/../../../shared/header-snippet.html';
$npcwoods_header_candidates[] = __DIR__ . '/../../../../shared/header-snippet.html';
$npcwoods_header_candidates[] = __DIR__ . '/../shared/header-snippet.html';
foreach ($npcwoods_header_candidates as $npcwoods_header_path) {
  if (is_readable($npcwoods_header_path)) {
    readfile($npcwoods_header_path);
    $npcwoods_header_rendered = true;
    break;
  }
}
if (!$npcwoods_header_rendered):
?>
<nav class="npc-nav" aria-label="Primary navigation">
  <div class="npc-nav-inner">
    <a class="npc-nav-logo" href="/" aria-label="NPCWoods homepage">
      <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="" width="38" height="38">
      <span class="npc-nav-logo-text"><span class="npc-nav-logo-name">NPCWoods</span><span class="npc-nav-logo-tag">Telemedicine</span></span>
    </a>
    <a class="npc-nav-cta" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris &middot; $59</a>
  </div>
</nav>
<?php endif; ?>

<style id="npcwoods-home-redesign">
  /* ===== NPCWoods homepage v3 (story + photos) : scoped to #main.npc-redesign ===== */
  .skip-link { position: absolute; left: -9999px; top: 0; z-index: 2000; padding: 10px 16px; border-radius: 0 0 8px 8px; background: #1B1813; color: #FBF7F0; -webkit-text-fill-color: #FBF7F0; font-family: Inter, sans-serif; font-weight: 600; font-size: 14px; }
  .skip-link:focus { left: 14px; }

  #main.npc-redesign {
    --cream: #FBF7F0; --warm-white: #FDFAF5; --cream-2: #F1EBDF;
    --ink: #1C1A17; --body: #57524A; --muted: #8C867A; --eyebrow: #6E6A60;
    --dark: #1B1813; --dark-2: #221E18; --on-dark: #FBF7F0; --on-dark-muted: #A39B8C;
    --blue: #2563EB; --blue-deep: #1D4ED8; --lav: #A5B4FC;
    --green: #16A34A; --gold: #E0A106; --red: #C2413A;
    --hair: rgba(28,26,23,0.12); --hair-dark: rgba(251,247,240,0.15);
    --rmax: 1180px; --rgut: clamp(20px, 5vw, 56px);
    background: var(--cream); color: var(--ink);
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.5; overflow-x: hidden; -webkit-font-smoothing: antialiased;
  }
  body { background: #FBF7F0; }
  #main.npc-redesign * { box-sizing: border-box; }
  #main.npc-redesign :where(h1,h2,h3,h4,p,ul,li,figure) { margin: 0; padding: 0; }
  #main.npc-redesign a { color: inherit; text-decoration: none; -webkit-text-fill-color: currentColor; }
  #main.npc-redesign img { display: block; max-width: 100%; }
  #main.npc-redesign ::selection { background: var(--blue); color: #fff; }

  #main.npc-redesign .rwrap { width: min(var(--rmax), 100%); margin: 0 auto; padding-inline: var(--rgut); }
  #main.npc-redesign .rpad { padding-block: clamp(72px, 11vh, 144px); }
  #main.npc-redesign section { position: relative; }
  #main.npc-redesign .dark { background: var(--dark); color: var(--on-dark); -webkit-text-fill-color: var(--on-dark); }
  #main.npc-redesign .dark :where(h1,h2,h3,p,span,div,li) { color: var(--on-dark); -webkit-text-fill-color: var(--on-dark); }
  #main.npc-redesign .warm-white { background: var(--warm-white); }

  #main.npc-redesign .eyebrow { font-family: "JetBrains Mono", monospace; font-size: 11px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--eyebrow); -webkit-text-fill-color: var(--eyebrow); display: inline-flex; align-items: center; gap: 9px; }
  #main.npc-redesign .eyebrow::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--blue); }
  #main.npc-redesign .dark .eyebrow { color: var(--on-dark-muted); -webkit-text-fill-color: var(--on-dark-muted); }

  #main.npc-redesign h1, #main.npc-redesign h2, #main.npc-redesign h3 { font-weight: 600; letter-spacing: -0.03em; line-height: 1.03; text-wrap: balance; }
  #main.npc-redesign h1 { font-size: clamp(2.6rem, 6.4vw, 4.5rem); }
  #main.npc-redesign h2 { font-size: clamp(2rem, 4.5vw, 3.3rem); }
  #main.npc-redesign .em { color: var(--blue); -webkit-text-fill-color: var(--blue); }
  #main.npc-redesign .dark .em { color: var(--lav); -webkit-text-fill-color: var(--lav); }
  #main.npc-redesign .serif-accent { font-family: Newsreader, Georgia, serif; font-weight: 400; font-style: italic; letter-spacing: -0.01em; }
  #main.npc-redesign .lede { font-size: clamp(1.1rem, 2vw, 1.3rem); color: var(--body); -webkit-text-fill-color: var(--body); line-height: 1.5; font-weight: 400; }
  #main.npc-redesign .dark .lede { color: var(--on-dark-muted); -webkit-text-fill-color: var(--on-dark-muted); }

  #main.npc-redesign .rbtn { display: inline-flex; align-items: center; gap: 9px; font-size: 16px; font-weight: 600; padding: 16px 28px; border-radius: 100px; border: 1px solid transparent; transition: transform .2s, box-shadow .2s, background .2s; }
  #main.npc-redesign .rbtn-primary { background: var(--blue); color: #fff !important; -webkit-text-fill-color: #fff !important; box-shadow: 0 14px 34px rgba(37,99,235,.26); }
  #main.npc-redesign .rbtn-primary:hover { background: var(--blue-deep); transform: translateY(-2px); box-shadow: 0 18px 42px rgba(37,99,235,.34); }
  #main.npc-redesign .rbtn-ghost { background: transparent; color: var(--ink); -webkit-text-fill-color: var(--ink); border-color: var(--hair); }
  #main.npc-redesign .rbtn-ghost:hover { border-color: rgba(28,26,23,.42); transform: translateY(-2px); }
  #main.npc-redesign .dark .rbtn-ghost { color: var(--on-dark); -webkit-text-fill-color: var(--on-dark); border-color: rgba(251,247,240,.26); }

  /* HERO */
  #main.npc-redesign .rhero { min-height: calc(100svh - 64px); display: grid; place-items: center; background: radial-gradient(120% 80% at 82% 0%, rgba(99,102,241,.10), transparent 55%), linear-gradient(180deg, var(--warm-white), var(--cream) 70%); }
  #main.npc-redesign .hero-grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: clamp(24px,5vw,60px); align-items: center; padding-block: clamp(40px,7vh,80px); }
  #main.npc-redesign .hero-copy { display: grid; gap: 22px; justify-items: start; }
  #main.npc-redesign .hero-copy h1 { max-width: 13ch; }
  #main.npc-redesign .hero-copy .lede { max-width: 40ch; }
  #main.npc-redesign .hero-actions { display: flex; gap: 12px; flex-wrap: wrap; }
  #main.npc-redesign .hero-cred { font-family: "JetBrains Mono", monospace; font-size: 12px; letter-spacing: .07em; color: var(--eyebrow); -webkit-text-fill-color: var(--eyebrow); }
  #main.npc-redesign .hero-photo { position: relative; }
  #main.npc-redesign .hero-photo img { width: 100%; border-radius: 18px; box-shadow: 0 40px 90px rgba(28,26,23,.18); background: var(--cream-2); aspect-ratio: 4/5; object-fit: cover; object-position: center top; }
  #main.npc-redesign .hero-badge { position: absolute; left: -16px; bottom: 22px; background: #fff; border: 1px solid var(--hair); border-radius: 14px; padding: 12px 16px; box-shadow: 0 18px 40px rgba(28,26,23,.14); display: flex; align-items: center; gap: 10px; }
  #main.npc-redesign .hero-badge .price { font-size: 1.7rem; font-weight: 700; letter-spacing: -.04em; color: var(--blue); -webkit-text-fill-color: var(--blue); line-height: 1; }
  #main.npc-redesign .hero-badge .lbl { font-size: 12px; color: var(--body); -webkit-text-fill-color: var(--body); font-weight: 600; line-height: 1.25; }
  @media (max-width: 860px) { #main.npc-redesign .hero-grid { grid-template-columns: 1fr; padding-top: 40px; } #main.npc-redesign .hero-photo { order: -1; max-width: 340px; } #main.npc-redesign .hero-copy { justify-items: center; text-align: center; } #main.npc-redesign .hero-copy .lede { margin-inline: auto; } }

  /* PROBLEM */
  #main.npc-redesign .sec-head { display: grid; gap: 16px; max-width: 56ch; margin-bottom: clamp(36px,5vh,64px); }
  #main.npc-redesign .prob-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; }
  #main.npc-redesign .prob { padding: 26px 22px; border: 1px solid var(--hair); border-radius: 14px; background: var(--cream); display: grid; gap: 10px; align-content: start; }
  #main.npc-redesign .prob .x { width: 30px; height: 30px; border-radius: 8px; background: rgba(194,65,58,.1); color: var(--red); -webkit-text-fill-color: var(--red); display: grid; place-items: center; font-weight: 700; }
  #main.npc-redesign .prob h3 { font-size: 1.12rem; font-weight: 600; letter-spacing: -.01em; line-height: 1.15; }
  #main.npc-redesign .prob p { font-size: .92rem; color: var(--muted); -webkit-text-fill-color: var(--muted); }
  #main.npc-redesign .prob-foot { margin-top: 32px; font-size: clamp(1.2rem,2.4vw,1.7rem); font-weight: 500; letter-spacing: -.02em; }
  @media (max-width: 760px) { #main.npc-redesign .prob-grid { grid-template-columns: 1fr 1fr; } }

  /* MEET */
  #main.npc-redesign .meet { display: grid; grid-template-columns: .92fr 1.08fr; gap: clamp(28px,5vw,68px); align-items: center; }
  #main.npc-redesign .meet-photo img { width: 100%; border-radius: 18px; aspect-ratio: 4/5; object-fit: cover; object-position: center top; background: var(--cream-2); box-shadow: 0 36px 80px rgba(0,0,0,.34); }
  #main.npc-redesign .meet-copy { display: grid; gap: 18px; }
  #main.npc-redesign .meet-copy p { color: var(--on-dark-muted); -webkit-text-fill-color: var(--on-dark-muted); font-size: 1.06rem; line-height: 1.6; max-width: 52ch; }
  #main.npc-redesign .meet-copy .big { color: var(--on-dark); -webkit-text-fill-color: var(--on-dark); font-size: 1.2rem; }
  #main.npc-redesign .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
  #main.npc-redesign .chip { font-family: "JetBrains Mono", monospace; font-size: 11px; letter-spacing: .05em; text-transform: uppercase; padding: 8px 13px; border: 1px solid var(--hair-dark); border-radius: 100px; color: var(--on-dark); -webkit-text-fill-color: var(--on-dark); }
  @media (max-width: 820px) { #main.npc-redesign .meet { grid-template-columns: 1fr; } #main.npc-redesign .meet-photo { max-width: 400px; } }

  /* STEPS */
  #main.npc-redesign .steps { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }
  #main.npc-redesign .step { border: 1px solid var(--hair); border-radius: 16px; overflow: hidden; background: var(--warm-white); }
  #main.npc-redesign .step-img { aspect-ratio: 3/2; overflow: hidden; background: var(--cream-2); }
  #main.npc-redesign .step-img img { width: 100%; height: 100%; object-fit: cover; }
  #main.npc-redesign .step-body { padding: 22px 22px 26px; display: grid; gap: 8px; }
  #main.npc-redesign .step-num { font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--blue); -webkit-text-fill-color: var(--blue); }
  #main.npc-redesign .step h3 { font-size: 1.3rem; font-weight: 600; letter-spacing: -.02em; }
  #main.npc-redesign .step p { color: var(--body); -webkit-text-fill-color: var(--body); font-size: .98rem; }
  @media (max-width: 760px) { #main.npc-redesign .steps { grid-template-columns: 1fr; } }

  /* BAND */
  #main.npc-redesign .band { min-height: 54vh; display: grid; place-items: center; text-align: center; overflow: hidden; }
  #main.npc-redesign .band > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  #main.npc-redesign .band::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(27,24,19,.36), rgba(27,24,19,.55)); }
  #main.npc-redesign .band .rwrap { position: relative; z-index: 1; display: grid; gap: 12px; justify-items: center; }
  #main.npc-redesign .band h2 { color: #fff; -webkit-text-fill-color: #fff; max-width: 18ch; }
  #main.npc-redesign .band p { color: rgba(255,255,255,.92); -webkit-text-fill-color: rgba(255,255,255,.92); font-size: 1.1rem; max-width: 44ch; }

  /* PRICE */
  #main.npc-redesign .price-stage { display: grid; place-items: center; text-align: center; gap: 16px; }
  #main.npc-redesign .price-num { font-size: clamp(6rem,22vw,16rem); font-weight: 700; line-height: .82; letter-spacing: -.06em; color: var(--on-dark); -webkit-text-fill-color: var(--on-dark); }
  #main.npc-redesign .price-num .d { color: var(--lav); -webkit-text-fill-color: var(--lav); }
  #main.npc-redesign .price-copy { max-width: 46ch; }
  #main.npc-redesign .price-chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 6px; }

  /* STATES */
  #main.npc-redesign .states { display: flex; flex-wrap: wrap; gap: 9px; margin-top: 6px; }
  #main.npc-redesign .state { font-family: "JetBrains Mono", monospace; font-size: 13px; letter-spacing: .05em; padding: 9px 14px; border: 1px solid var(--hair); border-radius: 100px; color: var(--ink); -webkit-text-fill-color: var(--ink); display: inline-flex; gap: 8px; align-items: center; }
  #main.npc-redesign .state::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--green); }

  /* FINAL */
  #main.npc-redesign .final { text-align: center; }
  #main.npc-redesign .final .rwrap { display: grid; justify-items: center; gap: 22px; }
  #main.npc-redesign .final h2 { color: #fff; -webkit-text-fill-color: #fff; max-width: 14ch; }

  /* reveal */
  #main.npc-redesign .reveal { opacity: 0; transform: translateY(26px); transition: opacity .8s cubic-bezier(.16,1,.3,1), transform .8s cubic-bezier(.16,1,.3,1); }
  #main.npc-redesign .reveal.in { opacity: 1; transform: none; }
  #main.npc-redesign .d1 { transition-delay: .07s; } #main.npc-redesign .d2 { transition-delay: .14s; } #main.npc-redesign .d3 { transition-delay: .21s; }
  @media (prefers-reduced-motion: reduce) { #main.npc-redesign .reveal { opacity: 1; transform: none; transition: none; } }

  /* REVIEWS */
  #main.npc-redesign .rev-head { text-align: center; display: grid; gap: 14px; justify-items: center; margin-bottom: clamp(36px,5vh,64px); }
  #main.npc-redesign .rev-grid { columns: 3 290px; column-gap: 16px; }
  #main.npc-redesign .rev { break-inside: avoid; margin: 0 0 16px; padding: 24px; border: 1px solid var(--hair); border-radius: 16px; background: var(--cream); display: grid; gap: 12px; }
  #main.npc-redesign .stars { color: var(--gold); -webkit-text-fill-color: var(--gold); letter-spacing: 2px; font-size: .95rem; }
  #main.npc-redesign .rev p { font-size: 1.02rem; line-height: 1.5; color: var(--ink); -webkit-text-fill-color: var(--ink); }
  #main.npc-redesign .rev .who { font-family: "JetBrains Mono", monospace; font-size: 12px; letter-spacing: .05em; color: var(--muted); -webkit-text-fill-color: var(--muted); text-transform: uppercase; }

  /* keep shared widgets from intruding on the homepage */
  #npcSaveWrap { display: none !important; visibility: hidden !important; }
  #trustedsite-tm-image, [id^="trustedsite"], [id^="trustedbadge"], [class*="trustedsite"] { display: none !important; }
  body::after { content: none !important; display: none !important; }
</style>

<noscript><style>#main.npc-redesign .reveal { opacity: 1 !important; transform: none !important; }</style></noscript>

<main id="main" class="npc-redesign">

  <!-- HERO -->
  <header class="rhero" aria-labelledby="hero-title">
    <div class="rwrap hero-grid">
      <div class="hero-copy">
        <div class="eyebrow reveal">NPCWoods Telemedicine &middot; 11 states</div>
        <h1 id="hero-title" class="reveal d1">$59 text-based<br><span class="em">telemedicine.</span></h1>
        <p class="lede reveal d1">I'm Chris, a real Nurse Practitioner. Tell me what's going on and I'll get you sorted out. $59 flat, no waiting room, right from your couch.</p>
        <div class="hero-actions reveal d2">
          <a class="rbtn rbtn-primary" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now</a>
          <a class="rbtn rbtn-ghost" href="#how">See how it works</a>
        </div>
        <div class="hero-cred reveal d2">MSN, APRN, FNP-C &middot; Licensed in 11 states</div>
      </div>
      <div class="hero-photo reveal d2">
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, MSN, APRN, FNP-C, Nurse Practitioner" width="500" height="625" fetchpriority="high">
        <div class="hero-badge"><span class="price">$59</span><span class="lbl">flat fee<br>pay after care</span></div>
      </div>
    </div>
  </header>

  <!-- PROBLEM -->
  <section class="rpad" aria-labelledby="prob-h">
    <div class="rwrap">
      <div class="sec-head">
        <div class="eyebrow reveal">The old way</div>
        <h2 id="prob-h" class="reveal d1">Getting better<br>shouldn't be this hard.</h2>
        <p class="lede reveal d1">You feel awful, and the system makes you work for it. Here is what the waiting-room runaround actually costs you.</p>
      </div>
      <div class="prob-grid">
        <div class="prob reveal"><span class="x">&times;</span><h3>3-hour waits</h3><p>A half-day in an urgent care lobby for a 10-minute problem.</p></div>
        <div class="prob reveal d1"><span class="x">&times;</span><h3>$200 for a $20 fix</h3><p>Surprise bills for simple care you already knew you needed.</p></div>
        <div class="prob reveal d2"><span class="x">&times;</span><h3>No clinic close by</h3><p>The nearest option is far, closed, or booked out for days.</p></div>
        <div class="prob reveal d3"><span class="x">&times;</span><h3>Forms &amp; denials</h3><p>Portals, paperwork, and confusing fine print after the fact.</p></div>
      </div>
      <p class="prob-foot reveal">I built NPCWoods to skip <span class="em serif-accent">all of it.</span></p>
    </div>
  </section>

  <!-- MEET CHRIS -->
  <section id="chris" class="dark rpad" aria-labelledby="meet-h">
    <div class="rwrap meet">
      <div class="meet-photo reveal"><img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, Nurse Practitioner and founder of NPCWoods" width="500" height="625" loading="lazy"></div>
      <div class="meet-copy">
        <div class="eyebrow reveal">Meet your NP</div>
        <h2 id="meet-h" class="reveal d1">Hey, I'm Chris.</h2>
        <p class="big reveal d1">I spent years watching people lose a whole day and a couple hundred bucks over something I could sort out in ten minutes. That never sat right with me.</p>
        <p class="reveal d2">So I built the practice I would want for my own family: text a real Nurse Practitioner, get actually listened to, and pay one honest price. No runaround. No surprise bills. No pretending a chatbot is care. Faith and family keep me grounded, and they are why I treat every visit like it is someone I love.</p>
        <div class="chips reveal d2">
          <span class="chip">MSN, APRN, FNP-C</span>
          <span class="chip">Real clinician review</span>
          <span class="chip">Founder, NPCWoods</span>
        </div>
      </div>
    </div>
  </section>

  <!-- HOW IT WORKS -->
  <section id="how" class="warm-white rpad" aria-labelledby="how-h">
    <div class="rwrap">
      <div class="sec-head">
        <div class="eyebrow reveal">How it works</div>
        <h2 id="how-h" class="reveal d1">Three texts from<br>feeling better.</h2>
        <p class="lede reveal d1">Most visits wrap up in under an hour, from your first text to your prescription.</p>
      </div>
      <div class="steps">
        <article class="step reveal"><div class="step-img"><img src="https://npcwoods.com/wp-content/uploads/2026/06/npcwoods-step-text.webp" alt="Texting symptoms from home" loading="lazy"></div><div class="step-body"><span class="step-num">01</span><h3>Text me your symptoms</h3><p>In your own words. No 30-question form, no portal login, no app to download.</p></div></article>
        <article class="step reveal d1"><div class="step-img"><img src="https://npcwoods.com/wp-content/uploads/2026/06/npcwoods-step-review.webp" alt="Chris reviewing a visit" loading="lazy"></div><div class="step-body"><span class="step-num">02</span><h3>I actually read it</h3><p>I look at your history, ask what I need to, and build a plan for you. Not a template. Not a bot.</p></div></article>
        <article class="step reveal d2"><div class="step-img"><img src="https://npcwoods.com/wp-content/uploads/2026/06/npcwoods-step-pharmacy.webp" alt="Prescription ready at the pharmacy" loading="lazy"></div><div class="step-body"><span class="step-num">03</span><h3>Pick up and feel better</h3><p>I send your prescription to your pharmacy and a written plan to your inbox. That is it.</p></div></article>
      </div>
    </div>
  </section>

  <!-- BAND -->
  <section class="band" aria-label="Care from home">
    <img src="https://npcwoods.com/wp-content/uploads/2026/06/npcwoods-couch.jpg" alt="" loading="lazy">
    <div class="rwrap">
      <h2 class="reveal">No waiting room. No fluorescent lights.</h2>
      <p class="reveal d1">Just help, where you already are.</p>
    </div>
  </section>

  <!-- PRICE -->
  <section class="dark rpad" aria-labelledby="price-h">
    <div class="rwrap price-stage">
      <div class="eyebrow reveal">One price. One promise.</div>
      <div class="price-num reveal d1"><span class="d">$</span>59</div>
      <h2 id="price-h" class="reveal d1" style="font-size:clamp(1.6rem,3.6vw,2.6rem)">That's the whole thing.</h2>
      <p class="lede price-copy reveal d2">Pay after you're treated. And if I can't safely help you by text, I'll tell you straight up, and you don't pay a dime.</p>
      <div class="price-chips reveal d2">
        <span class="chip">Flat fee</span><span class="chip">No hidden fees</span><span class="chip">Pay after treated</span><span class="chip">HSA / FSA receipt on request</span>
      </div>
    </div>
  </section>

  <!-- REVIEWS -->
  <section class="rpad" aria-labelledby="rev-h">
    <div class="rwrap">
      <div class="rev-head">
        <div class="eyebrow reveal">Real people</div>
        <h2 id="rev-h" class="reveal d1">Real texts. Real relief.</h2>
      </div>
      <div class="rev-grid reveal d1">
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Very fast and convenient. I first messaged Chris at 10:08am and I was picking up my prescriptions from the pharmacy at 10:52am same day! Cannot recommend enough!"</p><div class="who">A. H.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"I texted Chris out of nowhere on a Sunday and he answered straight away, saw me in under an hour! You would be hard pressed to find such a high level of service, especially at lightning-quick speed. He got the medicine I needed refilled and helped me get new labs."</p><div class="who">B. P.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"My grandmother couldn't get a response from her primary care provider and was in so much pain. I texted Chris at 10pm and he responded within 15 minutes. When the pharmacy didn't have it, he called the store himself and we had the prescription within 20 minutes. I could not recommend him more!"</p><div class="who">M. D.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Chris texted me back within seconds and had my prescription over to the pharmacy within minutes. So simple and easy. Definitely beats sitting in a waiting room. Recommend 100%!"</p><div class="who">J. R.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"What a wonderful service to the community. Fast response time, no sitting in the waiting room or waiting hours for a call back. I highly recommend."</p><div class="who">J. D. Q.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Messaged Chris, he responded in a timely manner. Very professional. Easy to talk to about our concerns. It was nice to stay home and get quality care."</p><div class="who">T. P.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Great provider! Great response time! Very thorough!"</p><div class="who">K. K.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Chris was awesome and very professional! Would highly recommend to anyone!"</p><div class="who">Charles N.</div></div>
        <div class="rev"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"My visit was very pleasant. I was given multiple options that would benefit my diagnosis!"</p><div class="who">R. W.</div></div>
      </div>
    </div>
  </section>

  <!-- STATES -->
  <section class="warm-white rpad" aria-labelledby="st-h">
    <div class="rwrap">
      <div class="sec-head">
        <div class="eyebrow reveal">Where I can help</div>
        <h2 id="st-h" class="reveal d1">Licensed in 11 states.</h2>
      </div>
      <div class="states reveal d1">
        <span class="state">Arizona</span><span class="state">Colorado</span><span class="state">Georgia</span><span class="state">Idaho</span><span class="state">Iowa</span><span class="state">Montana</span><span class="state">Nevada</span><span class="state">New Mexico</span><span class="state">North Carolina</span><span class="state">Oregon</span><span class="state">Utah</span>
      </div>
    </div>
  </section>

  <!-- FINAL -->
  <section class="dark rpad final" aria-labelledby="f-h">
    <div class="rwrap">
      <div class="eyebrow reveal">Ready when you are</div>
      <h2 id="f-h" class="reveal d1">Text me.<br>I've <span class="em">got you.</span></h2>
      <p class="lede reveal d2">$59 flat. A real Nurse Practitioner. Right from your couch.</p>
      <a class="rbtn rbtn-primary reveal d2" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now</a>
    </div>
  </section>

</main>

<?php
$npcwoods_footer_rendered = false;
$npcwoods_footer_candidates = array();
if (defined('ABSPATH')) {
  $npcwoods_footer_candidates[] = rtrim(ABSPATH, '/\\') . '/shared/footer-snippet.html';
}
$npcwoods_footer_candidates[] = __DIR__ . '/../html/shared/footer-snippet.html';
$npcwoods_footer_candidates[] = __DIR__ . '/../../../shared/footer-snippet.html';
$npcwoods_footer_candidates[] = __DIR__ . '/../../../../shared/footer-snippet.html';
foreach ($npcwoods_footer_candidates as $npcwoods_footer_path) {
  if (is_readable($npcwoods_footer_path)) {
    $GLOBALS['npcwoods_shared_footer_rendered'] = true;
    readfile($npcwoods_footer_path);
    $npcwoods_footer_rendered = true;
    break;
  }
}
if (!$npcwoods_footer_rendered):
?>
<footer class="npc-site-footer" aria-label="Footer">
  <div class="npc-footer-inner"><p>$59 text-based urgent care with Chris Woods, MSN, APRN, FNP-C. Available in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, and UT.</p></div>
</footer>
<?php endif; ?>

<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script>
(function () {
  function init() {
    var root = document.querySelector('#main.npc-redesign');
    if (!root) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var lenis = null;
    try {
      if (window.Lenis && !reduce) {
        lenis = new window.Lenis({ duration: 1.1, smoothWheel: true });
        var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
        requestAnimationFrame(raf);
      }
    } catch (e) { lenis = null; }
    try {
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
        root.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
      } else { root.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); }); }
    } catch (e) { root.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); }); }
    try {
      root.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var id = a.getAttribute('href');
          if (id && id.length > 1) { var t = document.querySelector(id); if (t) { e.preventDefault(); lenis ? lenis.scrollTo(t, { offset: -70 }) : t.scrollIntoView({ behavior: 'smooth' }); } }
        });
      });
    } catch (e) {}
    setTimeout(function () { root.querySelectorAll('.reveal:not(.in)').forEach(function (el) { el.classList.add('in'); }); }, 2500);
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
})();
</script>
<?php if (function_exists('wp_footer')) { wp_footer(); } ?>
</body>
</html>
