<?php
/**
 * Template Name: NPCWoods Homepage
 */
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="NPCWoods Telemedicine offers $59 text-based urgent care from a licensed Nurse Practitioner. No waiting room, no hidden fees, and clear next steps from home.">
<meta name="theme-color" content="#f5f5f7">
<title>NPCWoods Telemedicine: $59 Text-Based Urgent Care</title>
<link rel="canonical" href="https://npcwoods.com/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://npcwoods.com/">
<meta property="og:title" content="NPCWoods Telemedicine - $59 Text-Based Urgent Care">
<meta property="og:description" content="A simple text visit with a licensed Nurse Practitioner. $59 flat fee, clear next steps, and care from home.">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="NPCWoods Telemedicine - $59 Text-Based Urgent Care">
<meta name="twitter:description" content="A simple text visit with a licensed Nurse Practitioner. $59 flat fee, clear next steps, and care from home.">
<meta name="twitter:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700;8..60,800&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #f5f5f7;
  --panel: #ffffff;
  --ink: #111114;
  --body: #3f4148;
  --muted: #6e6e73;
  --line: rgba(0, 0, 0, 0.1);
  --line-soft: rgba(255, 255, 255, 0.16);
  --blue: #0071e3;
  --blue-bright: #2997ff;
  --green: #19a463;
  --orange: #f5a524;
  --red: #e5484d;
  --deep: #05060a;
  --deep-2: #151720;
  --radius: 28px;
  --max: 1200px;
  --shadow-soft: 0 24px 70px rgba(0, 0, 0, 0.1);
  --shadow-deep: 0 60px 120px rgba(0, 0, 0, 0.24);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.45;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

a { color: inherit; text-decoration: none; }
img { display: block; max-width: 100%; }
button, input, textarea { font: inherit; }

:focus-visible {
  outline: 3px solid rgba(0, 113, 227, 0.5);
  outline-offset: 4px;
}

.skip-link {
  position: absolute;
  left: 16px;
  top: -80px;
  z-index: 1000;
  padding: 12px 16px;
  border-radius: 0 0 14px 14px;
  background: var(--blue);
  color: #fff;
  font-weight: 800;
}
.skip-link:focus { top: 0; }

.nav {
  position: sticky;
  top: 0;
  z-index: 50;
  height: 56px;
  display: flex;
  justify-content: center;
  background: rgba(245, 245, 247, 0.78);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(22px);
}

.nav-inner {
  width: min(var(--max), 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0 22px;
  font-size: 13px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-width: max-content;
  color: #1d1d1f;
  font-size: 15px;
  font-weight: 900;
}

.brand img {
  width: 28px;
  height: 28px;
  border-radius: 9px;
  object-fit: cover;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 28px;
  color: #424245;
  font-weight: 650;
}

.nav-links a:hover { color: var(--blue); }

.nav-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 34px;
  padding: 8px 15px;
  border-radius: 999px;
  background: var(--blue);
  color: #fff;
  font-weight: 800;
  box-shadow: 0 10px 24px rgba(0, 113, 227, 0.24);
}

.hero {
  min-height: calc(100svh - 56px);
  display: grid;
  place-items: center;
  position: relative;
  overflow: hidden;
  padding: 78px 22px 54px;
  background:
    radial-gradient(circle at 50% 0%, rgba(0, 113, 227, 0.2), transparent 34%),
    linear-gradient(180deg, #fbfbfd 0%, #f5f5f7 56%, #edf3fb 100%);
}

.hero::before {
  content: "";
  position: absolute;
  inset: auto -12% -28% -12%;
  height: 48%;
  background: radial-gradient(ellipse at center, rgba(0, 113, 227, 0.22), transparent 65%);
  filter: blur(34px);
}

.hero-inner {
  position: relative;
  z-index: 1;
  width: min(var(--max), 100%);
  display: grid;
  grid-template-columns: 1.02fr 0.98fr;
  gap: 54px;
  align-items: center;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 22px;
  color: var(--blue);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.eyebrow i {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 0 6px rgba(25, 164, 99, 0.12);
}

h1, h2, h3, p { margin-top: 0; }

h1 {
  margin-bottom: 0;
  max-width: 790px;
  font-size: clamp(58px, 8.8vw, 118px);
  line-height: 0.91;
  letter-spacing: -0.065em;
  font-weight: 900;
}

.blue-word {
  background: linear-gradient(100deg, #0071e3, #5e5ce6 48%, #111114);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.07em;
}

.lede {
  max-width: 590px;
  margin: 26px 0 0;
  color: #424245;
  font-size: clamp(20px, 2.1vw, 28px);
  line-height: 1.24;
  letter-spacing: -0.025em;
  font-weight: 650;
}

.hero-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 34px;
}

.button {
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 22px;
  border-radius: 999px;
  font-size: 16px;
  font-weight: 850;
  transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}

.button.primary {
  background: var(--blue);
  color: #fff;
  box-shadow: 0 22px 44px rgba(0, 113, 227, 0.24);
}

.button.secondary {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #1d1d1f;
}

.button:hover { transform: translateY(-2px); }
.hero-fineprint {
  margin-top: 18px;
  color: var(--muted);
  font-size: 14px;
  font-weight: 700;
}

.stage {
  position: relative;
  min-height: 650px;
  display: grid;
  place-items: center;
  perspective: 1200px;
}

.halo {
  position: absolute;
  width: 620px;
  height: 620px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 113, 227, 0.18), rgba(255, 255, 255, 0.04) 46%, transparent 68%);
}

.iphone {
  width: min(360px, 76vw);
  aspect-ratio: 9 / 18.6;
  padding: 13px;
  border-radius: 54px;
  background: linear-gradient(145deg, #16181f, #e9ecf3 32%, #101116 62%, #ffffff);
  box-shadow: var(--shadow-deep), 0 18px 44px rgba(0, 113, 227, 0.15);
  transform: rotateY(-14deg) rotateX(5deg) rotateZ(1deg);
  animation: floatPhone 7s ease-in-out infinite;
}

@keyframes floatPhone {
  0%, 100% { transform: rotateY(-14deg) rotateX(5deg) rotateZ(1deg) translateY(0); }
  50% { transform: rotateY(-9deg) rotateX(7deg) rotateZ(1deg) translateY(-14px); }
}

.screen {
  position: relative;
  height: 100%;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.52);
  border-radius: 43px;
  background: #f7f8fb;
}

.island {
  position: absolute;
  top: 11px;
  left: 50%;
  z-index: 4;
  width: 104px;
  height: 30px;
  border-radius: 999px;
  background: #07070a;
  transform: translateX(-50%);
}

.screen-content { padding: 58px 20px 22px; }
.chat-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 22px;
}

.chat-head img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
}

.chat-head b { display: block; color: #1d1d1f; }
.chat-head span {
  display: block;
  color: var(--green);
  font-size: 12px;
  font-weight: 850;
}

.bubble {
  width: fit-content;
  max-width: 88%;
  margin: 10px 0;
  padding: 12px 14px;
  border-radius: 19px;
  font-size: 14px;
  line-height: 1.35;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
}

.bubble.me {
  margin-left: auto;
  border-bottom-right-radius: 6px;
  background: var(--blue);
  color: #fff;
}

.bubble.np {
  border-bottom-left-radius: 6px;
  background: #fff;
  color: #1d1d1f;
}

.reply-card {
  margin-top: 18px;
  padding: 18px;
  border-radius: 24px;
  background: #111114;
  color: #fff;
  box-shadow: 0 20px 44px rgba(0, 0, 0, 0.2);
}

.reply-card .small {
  color: #9ecaff;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.reply-card strong {
  display: block;
  margin: 8px 0 6px;
  font-size: 23px;
  line-height: 1.02;
  letter-spacing: -0.04em;
}

.reply-card p {
  margin: 0;
  color: #c7c7ce;
  font-size: 12px;
}

.floating-card {
  position: absolute;
  padding: 18px 20px;
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(20px);
  color: #1d1d1f;
  font-weight: 850;
}

.floating-card span {
  display: block;
  margin-top: 2px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 750;
}

.float-a { left: 0; top: 88px; }
.float-b { right: 6px; bottom: 96px; }

.proof {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  width: min(var(--max), calc(100% - 44px));
  margin: -20px auto 0;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 26px 80px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(24px);
}

.proof-item {
  min-height: 132px;
  padding: 28px;
  border-right: 1px solid rgba(0, 0, 0, 0.07);
}
.proof-item:last-child { border-right: 0; }
.proof-item strong {
  display: block;
  color: #1d1d1f;
  font-size: clamp(32px, 4vw, 54px);
  line-height: 1;
  letter-spacing: -0.06em;
}
.proof-item span {
  display: block;
  margin-top: 10px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 800;
}

.section {
  padding: 110px 22px;
}

.section-inner {
  width: min(var(--max), 100%);
  margin: 0 auto;
}

.section-kicker {
  margin-bottom: 14px;
  color: var(--blue);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.section-title {
  max-width: 920px;
  margin-bottom: 18px;
  color: #1d1d1f;
  font-size: clamp(42px, 6vw, 86px);
  line-height: 0.96;
  letter-spacing: -0.06em;
  font-weight: 900;
}

.section-copy {
  max-width: 700px;
  margin-bottom: 0;
  color: #51545c;
  font-size: clamp(18px, 2vw, 24px);
  line-height: 1.35;
  letter-spacing: -0.02em;
  font-weight: 600;
}

.dark {
  overflow: hidden;
  background:
    radial-gradient(circle at 22% 0%, rgba(41, 151, 255, 0.2), transparent 28%),
    linear-gradient(180deg, #05060a 0%, #11131a 100%);
  color: #fff;
}

.dark .section-kicker { color: #7cc0ff; }
.dark .section-title { color: #fff; }
.dark .section-copy { color: #c7c7ce; }

.experience-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-top: 56px;
}

.glass-panel {
  min-height: 430px;
  padding: 34px;
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.24);
  backdrop-filter: blur(24px);
}

.glass-panel h3 {
  margin-bottom: 14px;
  color: #fff;
  font-size: 31px;
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.glass-panel p {
  margin-bottom: 0;
  color: #c7c7ce;
  font-size: 16px;
  font-weight: 600;
}

.timeline {
  display: grid;
  gap: 15px;
  margin-top: 28px;
}

.step {
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 14px;
  align-items: start;
  padding: 16px;
  border: 1px solid var(--line-soft);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.07);
}

.step-number {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: #fff;
  color: #111114;
  font-weight: 900;
}

.step b {
  display: block;
  margin-bottom: 3px;
  color: #fff;
}

.step span {
  color: #b7bac5;
  font-size: 14px;
  font-weight: 600;
}

.price-reveal {
  position: relative;
  display: grid;
  place-items: center;
  min-height: 680px;
  overflow: hidden;
  border-radius: 38px;
  background: #030405;
  box-shadow: var(--shadow-deep);
}

.price-reveal::before {
  content: "";
  position: absolute;
  width: 860px;
  height: 860px;
  border-radius: 50%;
  background:
    radial-gradient(circle, rgba(41, 151, 255, 0.34), transparent 55%),
    conic-gradient(from 180deg, rgba(0, 113, 227, 0.55), rgba(255, 255, 255, 0), rgba(25, 164, 99, 0.34), rgba(0, 113, 227, 0.55));
  filter: blur(24px);
  animation: slowSpin 18s linear infinite;
}

@keyframes slowSpin {
  to { transform: rotate(360deg); }
}

.price-content {
  position: relative;
  z-index: 1;
  max-width: 780px;
  padding: 52px 26px;
  text-align: center;
  color: #fff;
}

.price-number {
  display: block;
  margin-bottom: 18px;
  font-size: clamp(104px, 18vw, 230px);
  line-height: 0.8;
  letter-spacing: -0.09em;
  font-weight: 900;
}

.price-content h2 {
  margin: 0 auto 16px;
  max-width: 720px;
  color: #fff;
  font-size: clamp(34px, 5vw, 72px);
  line-height: 0.98;
  letter-spacing: -0.055em;
}

.price-content p {
  max-width: 610px;
  margin: 0 auto 30px;
  color: #d7d7df;
  font-size: 20px;
  font-weight: 650;
}

.conditions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-top: 54px;
}

.condition-card {
  min-height: 210px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 25px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.05);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.condition-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 28px 70px rgba(0, 0, 0, 0.09);
}

.condition-card strong {
  display: block;
  color: #1d1d1f;
  font-size: 26px;
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.condition-card span {
  display: block;
  margin-top: 11px;
  color: var(--muted);
  font-weight: 650;
}

.card-link {
  margin-top: 24px;
  color: var(--blue);
  font-weight: 850;
}

.trust-layout {
  display: grid;
  grid-template-columns: 0.86fr 1.14fr;
  gap: 28px;
  align-items: stretch;
  margin-top: 56px;
}

.portrait-card,
.quote-card {
  overflow: hidden;
  border-radius: var(--radius);
  background: #fff;
  box-shadow: var(--shadow-soft);
}

.portrait-card {
  min-height: 620px;
  display: flex;
  flex-direction: column;
}

.portrait-card img {
  width: 100%;
  height: 470px;
  object-fit: cover;
  object-position: center top;
}

.portrait-copy {
  padding: 28px;
}

.portrait-copy b {
  display: block;
  color: #1d1d1f;
  font-size: 28px;
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.portrait-copy span {
  display: block;
  margin-top: 8px;
  color: var(--muted);
  font-weight: 700;
}

.quote-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 48px;
}

.quote-card blockquote {
  margin: 0;
  color: #1d1d1f;
  font-family: "Source Serif 4", Georgia, serif;
  font-size: clamp(34px, 4vw, 58px);
  line-height: 1.04;
  letter-spacing: -0.045em;
  font-weight: 800;
}

.quote-card p {
  margin: 24px 0 0;
  color: var(--muted);
  font-size: 17px;
  font-weight: 650;
}

.state-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 42px;
}

.state-strip a {
  display: inline-flex;
  min-height: 38px;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 999px;
  background: #fff;
  color: #33343b;
  font-size: 14px;
  font-weight: 800;
}

.state-strip a:hover {
  border-color: rgba(0, 113, 227, 0.28);
  color: var(--blue);
}

.final {
  min-height: 760px;
  display: grid;
  place-items: center;
  position: relative;
  overflow: hidden;
  padding: 110px 22px 90px;
  background:
    radial-gradient(circle at 50% 12%, rgba(0, 113, 227, 0.2), transparent 35%),
    linear-gradient(180deg, #f5f5f7 0%, #fff 100%);
}

.final-card {
  width: min(960px, 100%);
  padding: 60px 34px;
  border: 1px solid rgba(255, 255, 255, 0.82);
  border-radius: 42px;
  background: rgba(255, 255, 255, 0.76);
  box-shadow: 0 40px 110px rgba(0, 0, 0, 0.11);
  backdrop-filter: blur(24px);
  text-align: center;
}

.final-card h2 {
  margin: 0 auto 18px;
  max-width: 780px;
  color: #1d1d1f;
  font-size: clamp(48px, 7vw, 96px);
  line-height: 0.94;
  letter-spacing: -0.065em;
  font-weight: 900;
}

.final-card p {
  max-width: 620px;
  margin: 0 auto 32px;
  color: #51545c;
  font-size: 21px;
  line-height: 1.35;
  font-weight: 650;
}

.footer {
  padding: 58px 22px;
  background: #111114;
  color: #d7d7df;
}

.footer-inner {
  width: min(var(--max), 100%);
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 0.8fr;
  gap: 32px;
  margin: 0 auto;
}

.footer h2,
.footer h3 {
  color: #fff;
  margin: 0 0 14px;
}

.footer p {
  max-width: 520px;
  margin-bottom: 0;
  color: #a7aab5;
}

.footer a {
  display: block;
  margin: 8px 0;
  color: #d7d7df;
  font-weight: 650;
}

.footer a:hover { color: #fff; }

.reveal {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.reveal.in-view {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
}

@media (max-width: 980px) {
  .nav-links a:not(.nav-cta) { display: none; }
  .hero {
    min-height: auto;
    padding-top: 58px;
  }
  .hero-inner,
  .experience-grid,
  .trust-layout {
    grid-template-columns: 1fr;
  }
  .stage {
    min-height: 590px;
    order: -1;
  }
  h1 {
    font-size: clamp(55px, 15vw, 92px);
  }
  .proof {
    grid-template-columns: repeat(2, 1fr);
  }
  .proof-item:nth-child(2) { border-right: 0; }
  .proof-item:nth-child(1),
  .proof-item:nth-child(2) { border-bottom: 1px solid rgba(0, 0, 0, 0.07); }
  .conditions-grid {
    grid-template-columns: 1fr 1fr;
  }
  .footer-inner {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .nav-inner { padding: 0 14px; }
  .brand span { display: none; }
  .nav-cta {
    min-height: 32px;
    padding: 7px 12px;
    font-size: 12px;
  }
  .hero {
    padding: 34px 16px 38px;
  }
  .hero-inner {
    gap: 26px;
  }
  .stage {
    min-height: 460px;
  }
  .iphone {
    width: min(292px, 76vw);
    border-radius: 44px;
  }
  .screen {
    border-radius: 34px;
  }
  .screen-content { padding: 52px 16px 18px; }
  .floating-card {
    padding: 13px 14px;
    border-radius: 18px;
    font-size: 13px;
  }
  .float-a { left: 4px; top: 46px; }
  .float-b { right: 0; bottom: 40px; }
  .hero-actions {
    align-items: stretch;
  }
  .button {
    width: 100%;
  }
  .proof {
    width: calc(100% - 28px);
    grid-template-columns: 1fr;
    margin-top: 0;
  }
  .proof-item {
    min-height: 112px;
    border-right: 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.07);
    padding: 24px;
  }
  .proof-item:last-child { border-bottom: 0; }
  .section {
    padding: 76px 16px;
  }
  .section-title {
    font-size: clamp(39px, 13vw, 62px);
  }
  .section-copy {
    font-size: 18px;
  }
  .experience-grid,
  .conditions-grid,
  .trust-layout {
    gap: 16px;
    margin-top: 34px;
  }
  .glass-panel {
    min-height: auto;
    padding: 24px;
  }
  .price-reveal {
    min-height: 560px;
    border-radius: 28px;
  }
  .price-number {
    font-size: clamp(94px, 30vw, 150px);
  }
  .conditions-grid {
    grid-template-columns: 1fr;
  }
  .portrait-card {
    min-height: auto;
  }
  .portrait-card img {
    height: 350px;
  }
  .quote-card {
    padding: 30px;
  }
  .quote-card blockquote {
    font-size: 34px;
  }
  .final {
    min-height: auto;
    padding: 80px 16px;
  }
  .final-card {
    padding: 42px 22px;
    border-radius: 30px;
  }
  .final-card h2 {
    font-size: clamp(42px, 14vw, 66px);
  }
}
</style>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://npcwoods.com/#organization",
      "name": "NPCWoods Telemedicine",
      "url": "https://npcwoods.com/",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "priceRange": "$59",
      "telephone": "+1-480-639-4722",
      "founder": { "@id": "https://npcwoods.com/#chris-woods" },
      "areaServed": ["Arizona", "Colorado", "Georgia", "Idaho", "Iowa", "Montana", "Nevada", "New Mexico", "North Carolina", "Oregon", "Utah"],
      "medicalSpecialty": "PrimaryCare"
    },
    {
      "@type": "Person",
      "@id": "https://npcwoods.com/#chris-woods",
      "name": "Chris Woods",
      "jobTitle": "MSN, APRN, FNP-C",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "worksFor": { "@id": "https://npcwoods.com/#organization" }
    },
    {
      "@type": "Service",
      "@id": "https://npcwoods.com/#text-visit",
      "name": "$59 text-based urgent care visit",
      "provider": { "@id": "https://npcwoods.com/#organization" },
      "offers": {
        "@type": "Offer",
        "price": "59",
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock"
      }
    }
  ]
}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<nav class="nav" aria-label="Primary navigation">
  <div class="nav-inner">
    <a class="brand" href="/" aria-label="NPCWoods homepage">
      <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="" width="28" height="28">
      <span>NPCWoods</span>
    </a>
    <div class="nav-links">
      <a href="#how">How it works</a>
      <a href="#conditions">Conditions</a>
      <a href="#states">States</a>
      <a href="#trust">Chris</a>
      <a class="nav-cta" href="sms:+14806394722?body=Hi%20NPCWoods%2C%20I%27d%20like%20to%20start%20a%20%2459%20text%20visit.">Start visit</a>
    </div>
  </div>
</nav>

<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-inner">
      <div class="hero-copy reveal in-view">
        <div class="eyebrow"><i></i> Text-based urgent care</div>
        <h1 id="hero-title">Urgent care, reimagined for <span class="blue-word">your phone.</span></h1>
        <p class="lede">A $59 text visit with Chris Woods, MSN, APRN, FNP-C. Clear next steps from home, without the waiting room spiral.</p>
        <div class="hero-actions">
          <a class="button primary" href="sms:+14806394722?body=Hi%20NPCWoods%2C%20I%27d%20like%20to%20start%20a%20%2459%20text%20visit.">Start my $59 visit</a>
          <a class="button secondary" href="#how">See how it works</a>
        </div>
        <div class="hero-fineprint">Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, and UT.</div>
      </div>

      <div class="stage" aria-hidden="true">
        <div class="halo"></div>
        <div class="floating-card float-a">$59 flat fee<span>No hidden fees</span></div>
        <div class="iphone">
          <div class="screen">
            <div class="island"></div>
            <div class="screen-content">
              <div class="chat-head">
                <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-400.webp" alt="" width="42" height="42">
                <div><b>Chris at NPCWoods</b><span>Usually replies by text</span></div>
              </div>
              <div class="bubble me">Burning when I pee. Can I do this from home?</div>
              <div class="bubble np">Yes. Text me what is going on and I will walk you through the next step.</div>
              <div class="bubble me">How much?</div>
              <div class="bubble np">$59 flat fee. I will tell you if this needs in-person care instead.</div>
              <div class="reply-card">
                <div class="small">Visit ready</div>
                <strong>Simple, human care.</strong>
                <p>Text first. Clear guidance. Pharmacy path when appropriate.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="floating-card float-b">Secure text flow<span>Built for real life</span></div>
      </div>
    </div>
  </section>

  <section class="proof" aria-label="NPCWoods quick proof">
    <div class="proof-item"><strong>$59</strong><span>Flat visit fee</span></div>
    <div class="proof-item"><strong>11</strong><span>States served</span></div>
    <div class="proof-item"><strong>50+</strong><span>Common concerns</span></div>
    <div class="proof-item"><strong>NPI</strong><span>Real clinician care</span></div>
  </section>

  <section id="how" class="section dark">
    <div class="section-inner">
      <div class="section-kicker reveal">The new patient experience</div>
      <h2 class="section-title reveal">It feels too simple because healthcare usually is not.</h2>
      <p class="section-copy reveal">NPCWoods is designed around the part patients actually need first: a fast, clear answer from a real clinician about what to do next.</p>

      <div class="experience-grid">
        <article class="glass-panel reveal">
          <h3>Your visit starts as a text.</h3>
          <p>No portal maze. No mystery price. You send the concern, Chris reviews the situation, and you get a practical path forward.</p>
          <div class="timeline">
            <div class="step">
              <div class="step-number">1</div>
              <div><b>Send a text</b><span>Tell us symptoms, state, and what you need help with.</span></div>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <div><b>Clinician review</b><span>Chris checks fit, red flags, and whether telemedicine makes sense.</span></div>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <div><b>Clear next step</b><span>You get guidance, follow-up instructions, or pharmacy coordination when appropriate.</span></div>
            </div>
          </div>
        </article>

        <article class="glass-panel reveal">
          <h3>Built to lower friction, not lower standards.</h3>
          <p>Some problems need in-person care. The job is not to force everything through a text visit. The job is to get you pointed in the right direction quickly and honestly.</p>
          <div class="timeline">
            <div class="step">
              <div class="step-number">A</div>
              <div><b>Red flags matter</b><span>If symptoms sound unsafe for telemedicine, you will be told directly.</span></div>
            </div>
            <div class="step">
              <div class="step-number">B</div>
              <div><b>Medication is not automatic</b><span>Prescriptions depend on state rules, history, symptoms, and clinical fit.</span></div>
            </div>
            <div class="step">
              <div class="step-number">C</div>
              <div><b>Simple does not mean casual</b><span>This is licensed clinical care, just stripped of the usual clutter.</span></div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="price-title">
    <div class="section-inner">
      <div class="price-reveal reveal">
        <div class="price-content">
          <span class="price-number">$59</span>
          <h2 id="price-title">One clear price before you start.</h2>
          <p>No surprise bills. No confusing checkout story. Just a flat visit fee for text-based urgent care when NPCWoods is an appropriate fit.</p>
          <a class="button primary" href="sms:+14806394722?body=Hi%20NPCWoods%2C%20I%27d%20like%20to%20start%20a%20%2459%20text%20visit.">Text NPCWoods</a>
        </div>
      </div>
    </div>
  </section>

  <section id="conditions" class="section" aria-labelledby="conditions-title">
    <div class="section-inner">
      <div class="section-kicker reveal">Common visit lanes</div>
      <h2 id="conditions-title" class="section-title reveal">The stuff that usually derails a normal day.</h2>
      <p class="section-copy reveal">These pages help patients understand whether a text visit may fit and when symptoms should be handled in person.</p>

      <div class="conditions-grid">
        <a class="condition-card reveal" href="/uti-treatment/">
          <div><strong>UTI symptoms</strong><span>Burning, urgency, and bladder infection questions.</span></div>
          <div class="card-link">Explore UTI care</div>
        </a>
        <a class="condition-card reveal" href="/sinus-infection-treatment/">
          <div><strong>Sinus infection</strong><span>Congestion, pressure, worsening symptoms, and timing.</span></div>
          <div class="card-link">Explore sinus care</div>
        </a>
        <a class="condition-card reveal" href="/dental-pain/">
          <div><strong>Dental pain</strong><span>Tooth infection concerns and bridge care before dental follow-up.</span></div>
          <div class="card-link">Explore dental care</div>
        </a>
        <a class="condition-card reveal" href="/learn/strep-throat/">
          <div><strong>Sore throat</strong><span>Strep-like symptoms, red flags, and next-step guidance.</span></div>
          <div class="card-link">Read throat guide</div>
        </a>
        <a class="condition-card reveal" href="/learn/pink-eye/">
          <div><strong>Pink eye</strong><span>Eye redness, drainage, contact-lens cautions, and care guidance.</span></div>
          <div class="card-link">Read eye guide</div>
        </a>
        <a class="condition-card reveal" href="/conditions/">
          <div><strong>More conditions</strong><span>See the broader NPCWoods care library and patient education pages.</span></div>
          <div class="card-link">View all conditions</div>
        </a>
      </div>
    </div>
  </section>

  <section id="trust" class="section" aria-labelledby="trust-title">
    <div class="section-inner">
      <div class="section-kicker reveal">The human part</div>
      <h2 id="trust-title" class="section-title reveal">It is not an app pretending to care.</h2>
      <p class="section-copy reveal">NPCWoods works because there is a real clinician on the other side, using telemedicine for problems where speed and clarity matter.</p>

      <div class="trust-layout">
        <article class="portrait-card reveal">
          <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-400.webp" alt="Chris Woods, MSN, APRN, FNP-C" width="400" height="400" decoding="async">
          <div class="portrait-copy">
            <b>Chris Woods, MSN, APRN, FNP-C</b>
            <span>Founder of NPCWoods Telemedicine</span>
          </div>
        </article>

        <article class="quote-card reveal">
          <blockquote>"The goal is not to make healthcare feel flashy. The goal is to make it finally feel clear."</blockquote>
          <p>That is the whole design principle: modern enough to feel effortless, grounded enough to feel safe, and human enough to trust.</p>
        </article>
      </div>
    </div>
  </section>

  <section id="states" class="section" aria-labelledby="states-title">
    <div class="section-inner">
      <div class="section-kicker reveal">Where NPCWoods can help</div>
      <h2 id="states-title" class="section-title reveal">Licensed across 11 states.</h2>
      <p class="section-copy reveal">Text-based urgent care is available for patients physically located in the states below at the time of the visit.</p>
      <div class="state-strip reveal" aria-label="State landing pages">
        <a href="/arizona-telemedicine/">AZ - Arizona</a>
        <a href="/colorado-telemedicine/">CO - Colorado</a>
        <a href="/georgia-telemedicine/">GA - Georgia</a>
        <a href="/idaho-telemedicine/">ID - Idaho</a>
        <a href="/iowa-telemedicine/">IA - Iowa</a>
        <a href="/montana-telemedicine/">MT - Montana</a>
        <a href="/nevada-telemedicine/">NV - Nevada</a>
        <a href="/new-mexico-telemedicine/">NM - New Mexico</a>
        <a href="/north-carolina-telemedicine/">NC - North Carolina</a>
        <a href="/oregon-telemedicine/">OR - Oregon</a>
        <a href="/utah-telemedicine/">UT - Utah</a>
      </div>
    </div>
  </section>

  <section class="final" aria-labelledby="final-title">
    <div class="final-card reveal">
      <h2 id="final-title">This is what urgent care should feel like.</h2>
      <p>A simple text visit, a clear $59 fee, and a real clinician helping you decide the next right move.</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="button primary" href="sms:+14806394722?body=Hi%20NPCWoods%2C%20I%27d%20like%20to%20start%20a%20%2459%20text%20visit.">Start my $59 visit</a>
        <a class="button secondary" href="/conditions/">Browse conditions</a>
      </div>
    </div>
  </section>
</main>

<footer class="footer" aria-label="Footer">
  <div class="footer-inner">
    <div>
      <h2>NPCWoods Telemedicine</h2>
      <p>$59 text-based urgent care with Chris Woods, MSN, APRN, FNP-C. Available in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, and UT.</p>
    </div>
    <div>
      <h3>Care</h3>
      <a href="/conditions/">Conditions</a>
      <a href="/uti-treatment/">UTI treatment</a>
      <a href="/sinus-infection-treatment/">Sinus infection</a>
      <a href="/dental-pain/">Dental pain</a>
    </div>
    <div>
      <h3>Info</h3>
      <a href="/experience/">Patient experience</a>
      <a href="/pharmacy/">Pharmacy info</a>
      <a href="/learn/">After your visit</a>
      <a href="/sitemap/">Sitemap</a>
    </div>
  </div>
</footer>

<script>
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (item) { item.classList.add('in-view'); });
    return;
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });
  items.forEach(function (item) { observer.observe(item); });
})();
</script>
<!-- NPCWoods Tracking: tracking.js -->
<script src="/tracking.js"></script>
</body>
</html>
