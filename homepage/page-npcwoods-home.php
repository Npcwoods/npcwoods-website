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
<link rel="preconnect" href="https://unpkg.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700;8..60,800&display=swap" rel="stylesheet">
<style>
    :root {
      color-scheme: light;
      --ink: #111827;
      --body: #354052;
      --muted: #657286;
      --paper: #ffffff;
      --soft: #eef4fb;
      --blue: #0a74da;
      --navy: #07111f;
      --green: #18a36a;
      --amber: #d78a1f;
      --red: #c2413a;
      --line: rgba(15, 23, 42, 0.12);
      --line-dark: rgba(255, 255, 255, 0.16);
      --max: 1160px;
      --radius: 8px;
      --shadow: 0 18px 55px rgba(15, 23, 42, 0.11);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background: #f6f8fb;
      font-family: Inter, "DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
      touch-action: manipulation;
    }

    a { color: inherit; text-decoration: none; }
    img { display: block; max-width: 100%; }

    :focus-visible {
      outline: 3px solid rgba(10, 116, 218, 0.42);
      outline-offset: 4px;
    }

    .skip-link {
      position: absolute;
      left: 14px;
      top: -80px;
      z-index: 1000;
      padding: 10px 14px;
      border-radius: 0 0 var(--radius) var(--radius);
      background: var(--blue);
      color: #fff;
      font-weight: 900;
    }
    .skip-link:focus { top: 0; }

    .nav {
      position: sticky;
      top: 0;
      z-index: 50;
      border-bottom: 1px solid rgba(15, 23, 42, 0.08);
      background: rgba(246, 248, 251, 0.9);
      backdrop-filter: blur(18px);
    }

    .nav-inner {
      width: min(var(--max), calc(100% - 28px));
      min-height: 64px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 11px;
      font-weight: 900;
    }

    .brand img {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      object-fit: cover;
    }

    .brand span {
      display: block;
      font-size: 15px;
      line-height: 1;
    }

    .brand small {
      display: block;
      margin-top: 3px;
      color: var(--blue);
      font-size: 10px;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 22px;
      color: #3c4657;
      font-size: 14px;
      font-weight: 800;
    }

    .nav-links a:hover { color: var(--blue); }

    .btn {
      display: inline-flex;
      min-height: 46px;
      align-items: center;
      justify-content: center;
      gap: 9px;
      padding: 12px 18px;
      border: 0;
      border-radius: var(--radius);
      font-weight: 900;
      text-align: center;
      transition: transform 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease;
    }

    .btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 14px 30px rgba(10, 116, 218, 0.22);
    }

    .btn-primary {
      background: var(--blue);
      color: #fff;
    }

    .btn-secondary {
      border: 1px solid rgba(15, 23, 42, 0.14);
      background: #fff;
      color: var(--ink);
    }

    .hero {
      position: relative;
      overflow: hidden;
      background:
        linear-gradient(90deg, rgba(10, 116, 218, 0.09) 1px, transparent 1px),
        linear-gradient(180deg, rgba(10, 116, 218, 0.07) 1px, transparent 1px),
        linear-gradient(180deg, #f6f8fb 0%, #ffffff 100%);
      background-size: 64px 64px, 64px 64px, auto;
    }

    .hero-inner {
      width: min(var(--max), calc(100% - 28px));
      min-height: 720px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr 0.88fr;
      align-items: center;
      gap: 52px;
      padding: 74px 0 56px;
    }

    .kicker {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 18px;
      color: var(--blue);
      font-size: 13px;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .kicker::before {
      content: "";
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 0 5px rgba(24, 163, 106, 0.14);
    }

    h1,
    h2,
    h3,
    p {
      margin-top: 0;
    }

    h1 {
      max-width: 720px;
      margin-bottom: 22px;
      font-size: 76px;
      line-height: 0.95;
      letter-spacing: 0;
      text-wrap: balance;
    }

    .hero-lede {
      max-width: 650px;
      margin-bottom: 28px;
      color: var(--body);
      font-size: 22px;
      line-height: 1.35;
      font-weight: 750;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 22px;
    }

    .micro-row {
      display: flex;
      flex-wrap: wrap;
      gap: 9px;
    }

    .micro-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 8px 10px;
      border: 1px solid rgba(15, 23, 42, 0.1);
      border-radius: var(--radius);
      background: rgba(255, 255, 255, 0.86);
      color: #263247;
      font-size: 13px;
      font-weight: 850;
    }

    .visual-stack {
      display: grid;
      gap: 16px;
    }

    .phone-panel {
      position: relative;
      min-height: 520px;
      padding: 22px;
      border: 1px solid rgba(15, 23, 42, 0.12);
      border-radius: 14px;
      background: #fff;
      box-shadow: var(--shadow);
    }

    .phone-shell {
      width: min(310px, 100%);
      margin: 0 auto;
      border: 10px solid #0b1220;
      border-radius: 34px;
      background: #f8fafc;
      overflow: hidden;
      box-shadow: 0 24px 55px rgba(15, 23, 42, 0.24);
    }

    .phone-top {
      height: 42px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0b1220;
    }

    .phone-camera {
      width: 82px;
      height: 18px;
      border-radius: 999px;
      background: #020617;
    }

    .chat {
      display: grid;
      gap: 10px;
      padding: 16px;
    }

    .chat-head {
      display: flex;
      align-items: center;
      gap: 10px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(15, 23, 42, 0.08);
    }

    .chat-head img {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      object-fit: cover;
    }

    .chat-head strong,
    .chat-head span {
      display: block;
    }

    .chat-head span {
      color: var(--muted);
      font-size: 12px;
      font-weight: 750;
    }

    .bubble {
      max-width: 88%;
      padding: 10px 12px;
      border-radius: var(--radius);
      font-size: 14px;
      font-weight: 750;
      line-height: 1.35;
    }

    .bubble.patient {
      justify-self: end;
      background: var(--blue);
      color: #fff;
    }

    .bubble.np {
      justify-self: start;
      background: #e9eef5;
      color: #1d2738;
    }

    .next-card {
      display: grid;
      grid-template-columns: 42px 1fr;
      gap: 11px;
      align-items: center;
      margin-top: 4px;
      padding: 12px;
      border: 1px solid rgba(24, 163, 106, 0.22);
      border-radius: var(--radius);
      background: #f0fff7;
    }

    .next-card i {
      display: grid;
      place-items: center;
      width: 42px;
      height: 42px;
      border-radius: var(--radius);
      background: var(--green);
      color: #fff;
    }

    .next-card strong,
    .next-card span {
      display: block;
    }

    .next-card span {
      color: #32604c;
      font-size: 13px;
      font-weight: 800;
    }

    .route-card {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }

    .route-tile {
      min-height: 112px;
      padding: 14px;
      border: 1px solid rgba(15, 23, 42, 0.11);
      border-radius: var(--radius);
      background: #fff;
      box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
    }

    .route-tile i {
      color: var(--blue);
    }

    .route-tile strong {
      display: block;
      margin-top: 9px;
      font-size: 15px;
      line-height: 1.15;
    }

    .section {
      padding: 84px 0;
    }

    .section.dark {
      color: #fff;
      background:
        linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px),
        linear-gradient(180deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px),
        linear-gradient(180deg, #07111f 0%, #0d1828 100%);
      background-size: 72px 72px, 72px 72px, auto;
    }

    .section-inner {
      width: min(var(--max), calc(100% - 28px));
      margin: 0 auto;
    }

    .section-head {
      display: grid;
      grid-template-columns: 0.86fr 1fr;
      align-items: end;
      gap: 34px;
      margin-bottom: 34px;
    }

    .section h2 {
      margin-bottom: 0;
      font-size: 48px;
      line-height: 1.03;
      letter-spacing: 0;
      text-wrap: balance;
    }

    .section-copy {
      margin-bottom: 0;
      color: var(--body);
      font-size: 18px;
      font-weight: 750;
    }

    .dark .section-copy { color: #d8e1ef; }

    .proof-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }

    .proof-box {
      min-height: 122px;
      padding: 20px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper);
      box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
    }

    .proof-box strong {
      display: block;
      font-size: 34px;
      line-height: 1;
    }

    .proof-box span {
      display: block;
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 900;
      text-transform: uppercase;
    }

    .path {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }

    .path-step {
      min-height: 245px;
      display: grid;
      align-content: start;
      gap: 18px;
      padding: 22px;
      border: 1px solid var(--line-dark);
      border-radius: var(--radius);
      background: rgba(255, 255, 255, 0.09);
    }

    .icon-block {
      display: grid;
      place-items: center;
      width: 64px;
      height: 64px;
      border-radius: var(--radius);
      background: #fff;
      color: var(--blue);
    }

    .path-step h3 {
      margin-bottom: 0;
      color: #fff;
      font-size: 26px;
      line-height: 1.05;
      text-wrap: balance;
    }

    .path-step p {
      margin-bottom: 0;
      color: #dbe5f2;
      font-weight: 700;
    }

    .traffic {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
    }

    .signal {
      min-height: 280px;
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
    }

    .signal-top {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 18px;
    }

    .signal-light {
      width: 46px;
      height: 46px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: #fff;
    }

    .signal.green .signal-light { background: var(--green); }
    .signal.amber .signal-light { background: var(--amber); }
    .signal.red .signal-light { background: var(--red); }

    .signal h3 {
      margin-bottom: 0;
      font-size: 23px;
      line-height: 1.05;
    }

    .signal ul {
      display: grid;
      gap: 10px;
      margin: 0;
      padding: 0;
      list-style: none;
      color: var(--body);
      font-weight: 750;
    }

    .signal li {
      display: grid;
      grid-template-columns: 18px 1fr;
      gap: 8px;
    }

    .signal li::before {
      content: "";
      width: 8px;
      height: 8px;
      margin-top: 8px;
      border-radius: 50%;
      background: currentColor;
      opacity: 0.48;
    }

    .condition-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }

    .condition {
      min-height: 148px;
      display: grid;
      grid-template-columns: 50px 1fr;
      gap: 14px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
    }

    .condition i {
      display: grid;
      place-items: center;
      width: 50px;
      height: 50px;
      border-radius: var(--radius);
      background: var(--soft);
      color: var(--blue);
    }

    .condition strong {
      display: block;
      margin-bottom: 4px;
      font-size: 19px;
      line-height: 1.1;
    }

    .condition span {
      display: block;
      color: var(--muted);
      font-size: 14px;
      font-weight: 750;
    }

    .price-band {
      display: grid;
      grid-template-columns: 0.8fr 1fr;
      gap: 28px;
      align-items: center;
      padding: 34px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      box-shadow: var(--shadow);
    }

    .price-number {
      display: grid;
      place-items: center;
      min-height: 260px;
      border-radius: var(--radius);
      background:
        linear-gradient(135deg, rgba(10, 116, 218, 0.92), rgba(24, 163, 106, 0.86)),
        #0a74da;
      color: #fff;
      font-size: 92px;
      font-weight: 950;
    }

    .price-list {
      display: grid;
      gap: 12px;
      margin-top: 22px;
    }

    .price-item {
      display: grid;
      grid-template-columns: 42px 1fr;
      gap: 12px;
      align-items: center;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #f7fafc;
      font-weight: 850;
    }

    .price-item i {
      color: var(--green);
    }

    .trust {
      display: grid;
      grid-template-columns: 0.72fr 1fr;
      gap: 26px;
      align-items: stretch;
    }

    .portrait {
      overflow: hidden;
      border-radius: var(--radius);
      background: #d8e3ef;
      min-height: 420px;
    }

    .portrait img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .trust-copy {
      display: grid;
      align-content: center;
      padding: 34px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
    }

    .trust-copy h2 {
      margin-bottom: 16px;
    }

    .credential-row,
    .states {
      display: flex;
      flex-wrap: wrap;
      gap: 9px;
      margin-top: 20px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 8px 10px;
      border: 1px solid rgba(15, 23, 42, 0.12);
      border-radius: var(--radius);
      background: #fff;
      color: #263247;
      font-size: 13px;
      font-weight: 850;
    }

    .final {
      padding: 80px 0;
      color: #fff;
      background: var(--navy);
    }

    .final-inner {
      width: min(880px, calc(100% - 28px));
      margin: 0 auto;
      text-align: center;
    }

    .final h2 {
      margin-bottom: 18px;
      font-size: 52px;
      line-height: 1.02;
      text-wrap: balance;
    }

    .final p {
      max-width: 660px;
      margin: 0 auto 26px;
      color: #d7e1ef;
      font-size: 19px;
      font-weight: 760;
    }

    @media (max-width: 960px) {
      .hero-inner,
      .section-head,
      .price-band,
      .trust {
        grid-template-columns: 1fr;
      }

      .hero-inner {
        min-height: auto;
        padding-top: 46px;
      }

      .proof-grid,
      .path,
      .traffic,
      .condition-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    @media (max-width: 640px) {
      .nav-inner {
        min-height: 58px;
      }

      .brand small,
      .nav-links a:not(.btn) {
        display: none;
      }

      .nav-links {
        gap: 0;
      }

      .nav-links .btn {
        min-height: 40px;
        padding: 10px 12px;
        font-size: 13px;
      }

      h1 {
        font-size: 46px;
        line-height: 1.01;
      }

      .hero-lede {
        font-size: 18px;
      }

      .hero-actions,
      .hero-actions .btn {
        width: 100%;
      }

      .micro-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
      }

      .proof-grid,
      .path,
      .traffic,
      .condition-grid,
      .route-card {
        grid-template-columns: 1fr;
      }

      .section {
        padding: 62px 0;
      }

      .section h2,
      .final h2 {
        font-size: 36px;
      }

      .section-head {
        gap: 16px;
      }

      .phone-panel {
        padding: 14px;
      }

      .path-step,
      .signal,
      .price-band,
      .trust-copy {
        padding: 18px;
      }

      .price-number {
        min-height: 180px;
        font-size: 64px;
      }

      .portrait {
        min-height: 330px;
      }
    }

    :root {
      --shadow-soft: 0 24px 70px rgba(0, 0, 0, 0.1);
      --shadow-deep: 0 60px 120px rgba(0, 0, 0, 0.24);
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
      background-size: auto;
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
      min-height: auto;
      display: grid;
      grid-template-columns: 1.02fr 0.98fr;
      gap: 54px;
      align-items: center;
      padding: 0;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 22px;
      color: #0071e3;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .eyebrow i {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #18a36a;
      box-shadow: 0 0 0 6px rgba(25, 164, 99, 0.12);
    }

    .hero h1 {
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

    .hero .hero-actions {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      margin: 34px 0 0;
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
      background: #0071e3;
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
      color: #657286;
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
      padding-bottom: 0;
      border-bottom: 0;
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
      color: #18a36a;
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
      font-weight: 700;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
    }

    .bubble.me {
      margin-left: auto;
      border-bottom-right-radius: 6px;
      background: #0071e3;
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
      color: #657286;
      font-size: 12px;
      font-weight: 750;
    }

    .float-a { left: 0; top: 88px; }
    .float-b { right: 6px; bottom: 96px; }

    @media (max-width: 980px) {
      .hero {
        min-height: auto;
        padding-top: 58px;
      }

      .hero-inner {
        grid-template-columns: 1fr;
      }

      .stage {
        min-height: 590px;
        order: -1;
      }
    }

    @media (max-width: 640px) {
      .hero {
        padding: 34px 16px 38px;
      }

      .hero-inner {
        gap: 26px;
      }

      .hero h1 {
        font-size: clamp(55px, 15vw, 92px);
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

      .screen-content {
        padding: 52px 16px 18px;
      }

      .floating-card {
        padding: 13px 14px;
        border-radius: 18px;
        font-size: 13px;
      }

      .float-a { left: 4px; top: 46px; }
      .float-b { right: 0; bottom: 40px; }

      .hero .hero-actions {
        align-items: stretch;
      }

      .hero .button {
        width: 100%;
      }
    }
  </style>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://npcwoods.com/#medical-business",
      "name": "NPCWoods Telemedicine",
      "url": "https://npcwoods.com/",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "priceRange": "$59",
      "telephone": "+14806394722",
      "email": "cwoods@npcwoods.com",
      "founder": { "@id": "https://npcwoods.com/#chris-woods" },
      "employee": { "@id": "https://npcwoods.com/#chris-woods" },
      "areaServed": [
        {"@type": "State", "name": "Arizona"},
        {"@type": "State", "name": "Colorado"},
        {"@type": "State", "name": "Georgia"},
        {"@type": "State", "name": "Idaho"},
        {"@type": "State", "name": "Iowa"},
        {"@type": "State", "name": "Montana"},
        {"@type": "State", "name": "Nevada"},
        {"@type": "State", "name": "New Mexico"},
        {"@type": "State", "name": "North Carolina"},
        {"@type": "State", "name": "Oregon"},
        {"@type": "State", "name": "Utah"}
      ],
      "medicalSpecialty": "https://schema.org/FamilyPractice",
      "makesOffer": {
        "@type": "Offer",
        "name": "Async telemedicine visit",
        "price": "59.00",
        "priceCurrency": "USD"
      }
    },
    {
      "@type": "Person",
      "@id": "https://npcwoods.com/#chris-woods",
      "name": "Chris Woods",
      "honorificSuffix": "MSN, APRN, FNP-C",
      "jobTitle": "Licensed Nurse Practitioner",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "worksFor": { "@id": "https://npcwoods.com/#medical-business" },
      "identifier": {
        "@type": "PropertyValue",
        "propertyID": "NPI",
        "value": "1285125468"
      },
      "sameAs": [
        "https://npiregistry.cms.hhs.gov/provider-view/1285125468",
        "https://www.healthgrades.com/providers/christopher-woods-xynt5wl",
        "https://doctor.webmd.com/doctor/christopher-woods-7b55e933-62ef-4d7b-975c-9cfc40eb3ad8-overview"
      ]
    },
    {
      "@type": "Service",
      "@id": "https://npcwoods.com/#text-visit",
      "name": "$59 text-based urgent care visit",
      "provider": { "@id": "https://npcwoods.com/#medical-business" },
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
<?php endif; ?>

<style id="npcwoods-homepage-live-overrides">
#main .section.dark,
#main .final {
  color: #fff;
}

#main .section.dark h2,
#main .section.dark h3,
#main .section.dark .path-step h3,
#main .final h2 {
  color: #fff !important;
}

#main .section.dark .section-copy,
#main .section.dark .path-step p,
#main .final p {
  color: #dbe5f2 !important;
}

#main .section.dark .kicker,
#main .final .kicker {
  color: #35d99b !important;
}

#main .section.dark .icon-block {
  background: #fff;
  color: var(--blue);
}

#main .final .btn-primary {
  color: #fff !important;
}

#main .final .btn-secondary {
  color: var(--ink) !important;
}

/* The global save-contact prompt overlaps the homepage hero on small screens. */
#npcSaveWrap {
  display: none !important;
  visibility: hidden !important;
}
</style>

<main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-inner">
        <div class="hero-copy">
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

    <section class="section" aria-label="NPCWoods proof points">
      <div class="section-inner">
        <div class="proof-grid">
          <div class="proof-box"><strong>$59</strong><span>One visit fee</span></div>
          <div class="proof-box"><strong>Text</strong><span>Start on phone</span></div>
          <div class="proof-box"><strong>11</strong><span>Licensed states</span></div>
          <div class="proof-box"><strong>Chris</strong><span>Real clinician</span></div>
        </div>
      </div>
    </section>

    <section id="how" class="section dark" aria-labelledby="how-title">
      <div class="section-inner">
        <div class="section-head">
          <div>
            <div class="kicker">How it works</div>
            <h2 id="how-title">One simple path. Three clear steps.</h2>
          </div>
          <p class="section-copy">You can understand the visit at a glance, then read the details only if you want them.</p>
        </div>
        <div class="path">
          <article class="path-step">
            <div class="icon-block"><i data-lucide="message-square" aria-hidden="true"></i></div>
            <h3>1. Send a text</h3>
            <p>Tell NPCWoods what is going on, where you are located, and what you need help with.</p>
          </article>
          <article class="path-step">
            <div class="icon-block"><i data-lucide="stethoscope" aria-hidden="true"></i></div>
            <h3>2. Chris checks fit</h3>
            <p>Symptoms, red flags, state rules, and telemedicine fit are reviewed before the next step.</p>
          </article>
          <article class="path-step">
            <div class="icon-block"><i data-lucide="route" aria-hidden="true"></i></div>
            <h3>3. You get direction</h3>
            <p>Guidance, pharmacy coordination when appropriate, or a direct in-person recommendation.</p>
          </article>
        </div>
      </div>
    </section>

    <section id="fit" class="section" aria-labelledby="fit-title">
      <div class="section-inner">
        <div class="section-head">
          <div>
            <div class="kicker">Fit check</div>
            <h2 id="fit-title">A traffic light for what happens next.</h2>
          </div>
          <p class="section-copy">The first job is to decide whether text-based care makes sense. If symptoms sound unsafe, you will be pointed toward in-person care.</p>
        </div>
        <div class="traffic">
          <article class="signal green">
            <div class="signal-top">
              <div class="signal-light"><i data-lucide="check" aria-hidden="true"></i></div>
              <h3>Likely text fit</h3>
            </div>
            <ul>
              <li>Common, lower-risk concerns</li>
              <li>Clear symptom story</li>
              <li>You are in a licensed state</li>
              <li>No urgent red flags</li>
            </ul>
          </article>
          <article class="signal amber">
            <div class="signal-top">
              <div class="signal-light"><i data-lucide="search" aria-hidden="true"></i></div>
              <h3>Needs review</h3>
            </div>
            <ul>
              <li>Symptoms are not straightforward</li>
              <li>Timing or history matters</li>
              <li>Photo or detail may help</li>
              <li>Chris may ask follow-up questions</li>
            </ul>
          </article>
          <article class="signal red">
            <div class="signal-top">
              <div class="signal-light"><i data-lucide="triangle-alert" aria-hidden="true"></i></div>
              <h3>Go in person</h3>
            </div>
            <ul>
              <li>Severe or worsening symptoms</li>
              <li>Chest pain or trouble breathing</li>
              <li>Face, throat, or eye danger signs</li>
              <li>Telemedicine is not the right fit</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section id="conditions" class="section" aria-labelledby="conditions-title">
      <div class="section-inner">
        <div class="section-head">
          <div>
            <div class="kicker">Common lanes</div>
            <h2 id="conditions-title">Tap the problem. See the path.</h2>
          </div>
          <p class="section-copy">Short labels help you find the right starting point quickly.</p>
        </div>
        <div class="condition-grid">
          <a class="condition" href="/uti-treatment/">
            <i data-lucide="droplets" aria-hidden="true"></i>
            <span><strong>UTI symptoms</strong><span>Burning, urgency, bladder infection questions.</span></span>
          </a>
          <a class="condition" href="/sinus-infection-treatment/">
            <i data-lucide="wind" aria-hidden="true"></i>
            <span><strong>Sinus pressure</strong><span>Congestion, pressure, worsening symptoms.</span></span>
          </a>
          <a class="condition" href="/dental-pain/">
            <i data-lucide="shield-plus" aria-hidden="true"></i>
            <span><strong>Dental pain</strong><span>Bridge care before dental follow-up.</span></span>
          </a>
          <a class="condition" href="/learn/strep-throat/">
            <i data-lucide="thermometer" aria-hidden="true"></i>
            <span><strong>Sore throat</strong><span>Strep-like symptoms and red flags.</span></span>
          </a>
          <a class="condition" href="/learn/pink-eye/">
            <i data-lucide="eye" aria-hidden="true"></i>
            <span><strong>Pink eye</strong><span>Redness, drainage, contact-lens cautions.</span></span>
          </a>
          <a class="condition" href="/conditions/">
            <i data-lucide="layout-grid" aria-hidden="true"></i>
            <span><strong>More concerns</strong><span>Browse the larger care library.</span></span>
          </a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="price-title">
      <div class="section-inner">
        <div class="price-band">
          <div class="price-number" aria-label="$59">$59</div>
          <div>
            <div class="kicker">Simple pricing</div>
            <h2 id="price-title">One price before you start.</h2>
            <p class="section-copy">The visit fee is easy to see before you start, so there is no guessing.</p>
            <div class="price-list">
              <div class="price-item"><i data-lucide="check-circle-2" aria-hidden="true"></i><span>Flat visit fee</span></div>
              <div class="price-item"><i data-lucide="check-circle-2" aria-hidden="true"></i><span>No hidden fees</span></div>
              <div class="price-item"><i data-lucide="check-circle-2" aria-hidden="true"></i><span>No portal maze to start</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="trust-title">
      <div class="section-inner trust">
        <div class="portrait">
          <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-400.webp" alt="Chris Woods, MSN, APRN, FNP-C" width="400" height="400" loading="eager" decoding="async">
        </div>
        <div class="trust-copy">
          <div class="kicker">The human part</div>
          <h2 id="trust-title">Not an app pretending to care.</h2>
          <p class="section-copy">A real clinician reviews the visit and helps decide the safest next step.</p>
          <div class="credential-row" aria-label="Credentials and trust markers">
            <span class="chip"><i data-lucide="badge-check" aria-hidden="true"></i>MSN, APRN, FNP-C</span>
            <span class="chip"><i data-lucide="shield-check" aria-hidden="true"></i>Clinician review</span>
            <span class="chip"><i data-lucide="heart-pulse" aria-hidden="true"></i>Red flags matter</span>
          </div>
          <div class="states" aria-label="Licensed states">
            <span class="chip">AZ</span>
            <span class="chip">CO</span>
            <span class="chip">GA</span>
            <span class="chip">ID</span>
            <span class="chip">IA</span>
            <span class="chip">MT</span>
            <span class="chip">NV</span>
            <span class="chip">NM</span>
            <span class="chip">NC</span>
            <span class="chip">OR</span>
            <span class="chip">UT</span>
          </div>
        </div>
      </div>
    </section>

    <section class="final" aria-labelledby="final-title">
      <div class="final-inner">
        <div class="kicker">Ready when you are</div>
        <h2 id="final-title">Text first. Get clarity fast.</h2>
        <p>A $59 text visit with a real clinician, a fit check before the next step, and honest direction when in-person care makes more sense.</p>
        <div class="hero-actions" style="justify-content:center">
          <a class="btn btn-primary" href="sms:+14806394722?body=Hi%20NPCWoods%2C%20I%27d%20like%20to%20start%20a%20%2459%20text%20visit.">
            <i data-lucide="message-circle" aria-hidden="true"></i>
            Start my $59 visit
          </a>
          <a class="btn btn-secondary" href="/conditions/">
            <i data-lucide="layout-grid" aria-hidden="true"></i>
            Browse conditions
          </a>
        </div>
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
<?php endif; ?>

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

<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer></script>
<script>
(function () {
  function renderLucideIcons() {
    if (!window.lucide) { return; }
    window.lucide.createIcons({ attrs: { width: 22, height: 22, "stroke-width": 2.5 } });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderLucideIcons);
  } else {
    renderLucideIcons();
  }
})();
</script>
<?php if (function_exists('wp_footer')) { wp_footer(); } ?>
</body>
</html>
