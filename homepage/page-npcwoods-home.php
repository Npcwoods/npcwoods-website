<?php
/**
 * Template Name: NPCWoods Homepage
 * Hybrid V3 Homelander. Public URL: https://npcwoods.com/
 * UTI-look plate: approved preview body. 13 states: 12 NP licenses (incl. Washington)
 * plus Florida by out-of-state telehealth registration (TPAN3355).
 * 2026-10-06: Meta Pixel REMOVED (HIPAA hard rule: no tracking tags). Do not re-add.
 * 2026-10-06: GA4 / Google tag REMOVED (HIPAA hard rule: no Google tags on the site).
 * Do not re-add any Google tag here.
 * Do not enqueue TT4 / wp-block-library on this template.
 */
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#05060a" />
  <title>NPCWoods Telemedicine: $59 Text-Based Urgent Care</title>
  <link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg" />
  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/dm-serif-display-400.woff2" crossorigin />
  <link rel="preload" as="image" href="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" imagesrcset="https://npcwoods.com/wp-content/uploads/2026/04/chris-400.webp 400w, https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp 1000w" imagesizes="(max-width:860px) 92vw, 520px" fetchpriority="high" />
<?php if (function_exists('wp_head')) { wp_head(); } ?>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<!-- Live shared site CSS (nav/footer). Not the Twenty Twenty-Four stylesheet. -->
<link rel="stylesheet" href="https://npcwoods.com/assets/css/site.css">
<style>
/* === UTI page visual system (copied from live /uti-treatment/ inline CSS) === */

:root {
  --bg: #05060a;
  --panel: #0d0e14;
  --panel-2: #111318;
  --panel-3: #161820;
  --ink: #ffffff;
  --body: #c7c7ce;
  --muted: #6e6e73;
  --line: rgba(255,255,255,0.08);
  --blue: #0071e3;
  --blue-bright: #2997ff;
  --green: #19a463;
  --orange: #f5a524;
  --red: #e5484d;
  --radius: 20px;
  --max: 1120px;
}

*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  background:var(--bg);
  color:var(--ink);
  font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;
  line-height:1.5;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}

/* ── NAV ── */
.nav{
  position:sticky;top:0;z-index:50;
  height:52px;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 32px;
  background:rgba(5,6,10,0.82);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--line);
}
.nav-logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px}
.nav-logo img{width:32px;height:32px;border-radius:8px}
.nav-cta{
  background:var(--blue);color:#fff;
  border-radius:999px;padding:7px 16px;
  font-size:13px;font-weight:700;
  transition:opacity .15s;
}
.nav-cta:hover{opacity:.85}

/* ── HERO ── */
.hero{
  position:relative;
  min-height:92vh;
  display:flex;align-items:center;justify-content:center;
  padding:80px 24px 60px;
  background:var(--bg);
  overflow:hidden;
}
.hero::before{
  content:'';
  position:absolute;
  top:-20%;left:50%;transform:translateX(-50%);
  width:900px;height:700px;
  background:radial-gradient(ellipse at center, rgba(0,113,227,0.28) 0%, transparent 65%);
  filter:blur(60px);
  pointer-events:none;
}
.hero::after{
  content:'';
  position:absolute;
  bottom:0;left:0;right:0;height:200px;
  background:linear-gradient(to bottom,transparent,var(--bg));
  pointer-events:none;
}
.hero-inner{
  position:relative;z-index:1;
  text-align:center;
  max-width:760px;
  margin:0 auto;
}
.hero-kicker{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,0.07);
  border:1px solid rgba(255,255,255,0.12);
  border-radius:999px;
  padding:6px 16px;
  font-size:12px;font-weight:600;
  letter-spacing:0.06em;text-transform:uppercase;
  color:rgba(255,255,255,0.7);
  margin-bottom:28px;
}
.hero-dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(25,164,99,.2)}
.hero h1{
  font-size:clamp(42px,7.5vw,96px);
  font-weight:800;
  line-height:1.0;
  letter-spacing:-0.065em;
  background:linear-gradient(120deg,#ffffff 0%,#a8d4ff 50%,#c8d8f0 100%);
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;
  margin-bottom:20px;
}
.hero-sub{
  font-size:clamp(16px,2vw,20px);
  color:var(--body);
  line-height:1.55;
  letter-spacing:-0.015em;
  max-width:560px;margin:0 auto 36px;
}
.hero-actions{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;margin-bottom:28px}
.btn-primary{
  background:var(--blue);color:#fff;
  border-radius:999px;padding:14px 28px;
  font-size:15px;font-weight:700;
  letter-spacing:-0.01em;
  transition:transform .15s,box-shadow .15s;
  box-shadow:0 0 0 0 rgba(0,113,227,.4);
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 8px 30px rgba(0,113,227,.35)}
.btn-ghost{
  background:rgba(255,255,255,0.07);
  border:1px solid rgba(255,255,255,0.15);
  color:#fff;
  border-radius:999px;padding:14px 28px;
  font-size:15px;font-weight:600;
  transition:background .15s;
}
.btn-ghost:hover{background:rgba(255,255,255,0.12)}
.hero-trust{
  display:flex;align-items:center;justify-content:center;gap:20px;
  font-size:12px;color:var(--muted);flex-wrap:wrap;
}
.hero-trust span{display:flex;align-items:center;gap:5px}

/* ── STATS BAND ── */
.stats-band{
  background:var(--panel);
  border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);
  padding:32px 24px;
}
.stats-inner{
  max-width:var(--max);margin:0 auto;
  display:grid;grid-template-columns:repeat(3,1fr);
  gap:24px;
}
.stat{text-align:center}
.stat-n{
  font-size:clamp(36px,5vw,56px);
  font-weight:900;
  letter-spacing:-0.06em;
  background:linear-gradient(120deg,#fff,var(--blue-bright));
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;
  line-height:1;
  margin-bottom:6px;
}
.stat-l{font-size:13px;color:var(--muted);font-weight:500;letter-spacing:0.02em}

/* ── REVIEWS ── */
.reviews{
  background:var(--panel-2);
  padding:56px 0;
  overflow:hidden;
}
.reviews-head{text-align:center;padding:0 24px;margin-bottom:28px}
.reviews-head h2{font-size:clamp(22px,3vw,32px);font-weight:800;letter-spacing:-0.04em;margin-bottom:4px}
.reviews-head p{color:var(--muted);font-size:14px}
.stars-row{display:inline-flex;gap:3px;margin-bottom:6px}
.stars-row svg{width:18px;height:18px;fill:#f59e0b}
.scroll-mask{
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
}
.scroll-track{
  display:flex;gap:16px;width:max-content;
  animation:scrollR 50s linear infinite;
}
.scroll-track:hover{animation-play-state:paused}
@keyframes scrollR{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.rcard{
  flex-shrink:0;width:300px;
  background:var(--panel-3);
  border:1px solid var(--line);
  border-radius:16px;
  padding:20px 22px;
}
.rcard-text{font-size:13px;color:var(--body);line-height:1.6;font-style:italic;margin-bottom:14px;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.rcard-foot{display:flex;justify-content:space-between;align-items:center}
.rcard-author{font-size:12px;font-weight:700;color:#fff}
.rcard-source{font-size:10px;font-weight:700;color:var(--blue-bright);background:rgba(41,151,255,.12);border-radius:999px;padding:3px 9px}

/* ── SECTION WRAPPER ── */
.section{padding:80px 24px}
.section-inner{max-width:var(--max);margin:0 auto}
.section-kicker{
  display:inline-block;
  font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:0.1em;
  color:var(--blue-bright);
  margin-bottom:12px;
}
.section-title{
  font-size:clamp(28px,4vw,48px);
  font-weight:800;
  letter-spacing:-0.05em;
  line-height:1.08;
  margin-bottom:16px;
}
.section-body{
  font-size:16px;color:var(--body);
  line-height:1.65;max-width:640px;
  margin-bottom:40px;
}
.alt-bg{background:var(--panel)}
.alt-bg-2{background:var(--panel-2)}

/* ── HOW IT WORKS — BENTO ── */
.bento{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:16px;
}
.bento-card{
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:var(--radius);
  padding:28px 24px;
  transition:border-color .2s,transform .2s;
}
.bento-card:hover{border-color:rgba(0,113,227,.35);transform:translateY(-2px)}
.step-num{
  width:36px;height:36px;
  border-radius:50%;
  background:var(--blue);
  color:#fff;
  font-size:16px;font-weight:800;
  display:flex;align-items:center;justify-content:center;
  margin-bottom:16px;
}
.bento-card h3{
  font-size:18px;font-weight:800;
  letter-spacing:-0.03em;
  margin-bottom:10px;
}
.bento-card p{font-size:14px;color:var(--body);line-height:1.6}
.bento-card a{color:var(--blue-bright)}

/* ── WHAT IS A UTI ── */
.symptom-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:12px;
  margin-top:24px;
}
.symptom-card{
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:14px;
  padding:16px 18px;
  display:flex;gap:12px;align-items:flex-start;
}
.symptom-icon{
  width:28px;height:28px;
  background:rgba(0,113,227,.15);
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;
  font-size:14px;
}
.symptom-card strong{display:block;font-size:13px;font-weight:700;margin-bottom:2px}
.symptom-card span{font-size:12px;color:var(--muted)}

/* ── COMPARISON TABLE ── */
.compare-table{
  width:100%;border-collapse:collapse;
  border-radius:16px;overflow:hidden;
  border:1px solid var(--line);
  font-size:14px;
}
.compare-table th{
  background:var(--panel-3);
  padding:12px 16px;
  text-align:left;
  font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:0.08em;
  color:var(--muted);
  border-bottom:1px solid var(--line);
}
.compare-table td{
  padding:14px 16px;
  color:var(--body);
  border-bottom:1px solid rgba(255,255,255,0.04);
  vertical-align:top;
}
.compare-table tr:last-child td{border-bottom:none}
.compare-table tr:nth-child(even) td{background:rgba(255,255,255,0.02)}
.compare-table td:first-child{font-weight:700;color:#fff}
.treat-us{color:var(--green)!important;font-weight:600!important}
.treat-er{color:var(--muted)!important}
.table-wrap{overflow-x:auto;border-radius:16px}

/* ── DRUG CARDS ── */
.drug-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:14px;
}
.drug-card{
  background:rgba(255,255,255,0.04);
  border:1px solid var(--line);
  border-radius:var(--radius);
  padding:22px 20px;
  backdrop-filter:blur(12px);
  transition:border-color .2s,background .2s;
  text-decoration:none;color:inherit;
  display:block;
}
.drug-card:hover{border-color:rgba(0,113,227,.4);background:rgba(0,113,227,.06)}
.drug-badge{
  font-size:10px;font-weight:700;
  text-transform:uppercase;letter-spacing:0.1em;
  margin-bottom:8px;
}
.badge-blue{color:var(--blue-bright)}
.badge-orange{color:var(--orange)}
.badge-purple{color:#a78bfa}
.badge-green{color:var(--green)}
.drug-card h3{
  font-family:'DM Serif Display',serif;
  font-size:18px;color:#fff;
  margin-bottom:3px;
}
.drug-card .brand{font-size:11px;color:var(--muted);font-style:italic;margin-bottom:10px}
.drug-card p{font-size:13px;color:var(--body);line-height:1.55}

/* ── ER WARNING ── */
.er-box{
  background:rgba(229,72,77,.08);
  border:1px solid rgba(229,72,77,.25);
  border-radius:var(--radius);
  padding:28px 32px;
  max-width:740px;margin:24px auto 0;
}
.er-box h3{
  font-size:16px;font-weight:700;
  color:#ff6b70;margin-bottom:14px;
  display:flex;align-items:center;gap:8px;
}
.er-box ul{list-style:none;padding:0}
.er-box li{
  padding:8px 0;
  border-bottom:1px solid rgba(229,72,77,.12);
  font-size:14px;color:var(--body);
  padding-left:20px;position:relative;
}
.er-box li::before{content:'→';position:absolute;left:0;color:#ff6b70;font-weight:700}
.er-box li:last-child{border-bottom:none}

/* ── WHO IT'S FOR ── */
.fit-grid{
  display:grid;grid-template-columns:1fr 1fr;
  gap:16px;margin-top:24px;
}
.fit-good{
  background:rgba(25,164,99,.07);
  border:1px solid rgba(25,164,99,.2);
  border-radius:var(--radius);padding:24px;
}
.fit-bad{
  background:rgba(229,72,77,.07);
  border:1px solid rgba(229,72,77,.2);
  border-radius:var(--radius);padding:24px;
}
.fit-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px}
.fit-good .fit-label{color:var(--green)}
.fit-bad .fit-label{color:#ff6b70}
.fit-list{list-style:none;padding:0}
.fit-list li{
  font-size:13px;color:var(--body);
  padding:6px 0 6px 22px;
  position:relative;
  border-bottom:1px solid rgba(255,255,255,0.04);
}
.fit-list li:last-child{border-bottom:none}
.fit-good .fit-list li::before{content:'✓';position:absolute;left:0;color:var(--green);font-weight:700}
.fit-bad .fit-list li::before{content:'✗';position:absolute;left:0;color:#ff6b70;font-weight:700}

/* ── FAQ ── */
.faq-list{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:10px}
.faq-item{
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:14px;
  overflow:hidden;
  transition:border-color .2s;
}
.faq-item.open{border-color:rgba(0,113,227,.3)}
.faq-q{
  padding:18px 20px;
  font-size:15px;font-weight:600;
  cursor:pointer;
  display:flex;justify-content:space-between;align-items:center;
  gap:12px;
  color:#fff;
  user-select:none;
}
.faq-q::after{
  content:'+';
  font-size:20px;font-weight:300;
  color:var(--muted);
  flex-shrink:0;
  transition:transform .2s;
}
.faq-item.open .faq-q::after{transform:rotate(45deg);color:var(--blue-bright)}
.faq-a{
  max-height:0;overflow:hidden;
  transition:max-height .3s ease,padding .3s;
  padding:0 20px;
}
.faq-item.open .faq-a{max-height:800px;padding-bottom:18px}
.faq-a p{font-size:14px;color:var(--body);line-height:1.65}
.faq-a strong{color:#fff}

/* ── STATES ── */
.states-pills{
  display:flex;flex-wrap:wrap;justify-content:center;
  gap:10px;margin-top:24px;
}
.state-pill{
  padding:8px 18px;
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:999px;
  font-size:14px;font-weight:500;
  color:var(--body);
  transition:border-color .15s,color .15s,background .15s;
}
.state-pill:hover{border-color:var(--blue);color:#fff;background:rgba(0,113,227,.1)}

/* ── SPOKE GUIDES ── */
.guides-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:14px;
  margin-top:24px;
}
.guide-card{
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:14px;
  padding:18px 20px;
  transition:border-color .2s,transform .2s;
  text-decoration:none;color:inherit;
  display:block;
}
.guide-card:hover{border-color:rgba(0,113,227,.35);transform:translateY(-2px)}
.guide-card strong{display:block;font-size:13px;font-weight:700;color:var(--blue-bright);margin-bottom:6px}
.guide-card span{font-size:12px;color:var(--muted);line-height:1.5}

/* ── CROSS LINKS ── */
.cross-wrap{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:24px}
.cross-link{
  padding:8px 16px;
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:999px;
  font-size:13px;color:var(--body);
  transition:color .15s,border-color .15s;
}
.cross-link:hover{color:#fff;border-color:rgba(255,255,255,.25)}

/* ── BOTTOM CTA ── */
.bottom-cta{
  background:linear-gradient(160deg,#0a1628 0%,#05060a 50%,#0d1a30 100%);
  border-top:1px solid var(--line);
  padding:80px 24px;
  text-align:center;
  position:relative;overflow:hidden;
}
.bottom-cta::before{
  content:'';
  position:absolute;top:-40%;left:50%;transform:translateX(-50%);
  width:600px;height:400px;
  background:radial-gradient(ellipse,rgba(0,113,227,.2),transparent 65%);
  filter:blur(40px);pointer-events:none;
}
.bottom-cta-inner{position:relative;z-index:1;max-width:600px;margin:0 auto}
.bottom-cta h2{
  font-size:clamp(32px,5vw,56px);
  font-weight:800;letter-spacing:-0.055em;
  margin-bottom:16px;
  background:linear-gradient(120deg,#fff,#a8d4ff);
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;
}
.bottom-cta p{font-size:16px;color:var(--body);margin-bottom:32px;line-height:1.6}
.bottom-trust-line{
  font-size:12px;color:var(--muted);
  margin-top:20px;
  display:flex;align-items:center;justify-content:center;
  gap:16px;flex-wrap:wrap;
}

/* ── CLINICIAN LINE ── */
.clinician-line{
  text-align:center;
  padding:20px 24px;
  font-size:12px;
  color:var(--muted);
  border-top:1px solid var(--line);
  background:var(--bg);
}

/* ── FOOTER ── */
.footer{
  background:#030406;
  border-top:1px solid var(--line);
  padding:56px 24px 32px;
  color:var(--muted);
  font-size:13px;
}
.footer-inner{max-width:var(--max);margin:0 auto}
.footer-grid{
  display:grid;
  grid-template-columns:1.4fr 1fr 1fr 1fr;
  gap:40px;
  margin-bottom:40px;
}
.footer-brand p{color:var(--muted);font-size:13px;line-height:1.65;max-width:260px;margin:10px 0 16px}
.footer-brand-name{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:700;color:#fff}
.footer-brand-name img{width:32px;height:32px;border-radius:8px}
.footer-col h4{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#fff;margin-bottom:14px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:8px}
.footer-col a{color:var(--muted);transition:color .15s}
.footer-col a:hover{color:#fff}
.footer-cta{
  display:inline-block;
  background:var(--blue);color:#fff;
  border-radius:999px;padding:9px 20px;
  font-size:13px;font-weight:700;
}
.footer-divider{border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 20px}
.footer-bottom{
  display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:12px;
  font-size:11px;color:rgba(255,255,255,0.25);
}
.footer-bottom a{color:rgba(255,255,255,0.25);transition:color .15s}
.footer-bottom a:hover{color:rgba(255,255,255,0.55)}

/* ── RESPONSIVE ── */
@media(max-width:900px){
  .bento{grid-template-columns:1fr}
  .stats-inner{grid-template-columns:repeat(3,1fr)}
  .fit-grid{grid-template-columns:1fr}
  .footer-grid{grid-template-columns:1fr 1fr;gap:28px}
}
@media(max-width:600px){
  .stats-inner{grid-template-columns:1fr}
  .symptom-grid{grid-template-columns:1fr}
  .footer-grid{grid-template-columns:1fr}
  .hero h1{letter-spacing:-0.04em}
  .section{padding:56px 20px}
  .nav{padding:0 16px}
}

/* ── LIGHT SECTIONS ── */
.section-light,
.section-white {
  --panel: #ffffff;
  --panel-2: #f0f0f5;
  --panel-3: #e8e8ed;
  --ink: #111114;
  --body: #3d3d3f;
  --muted: #6e6e73;
  --line: rgba(0,0,0,0.09);
  color: #111114;
}
.section-light { background: #f5f5f7; }
.section-white { background: #ffffff; }

.section-light .section-kicker,
.section-white .section-kicker { color: var(--blue); }

.section-light .faq-q,
.section-white .faq-q { color: #111114; }
.section-light .faq-item.open .faq-q::after,
.section-white .faq-item.open .faq-q::after { color: var(--blue); }
.section-light .faq-a strong,
.section-white .faq-a strong { color: #111114; }

.section-light .guide-card strong,
.section-white .guide-card strong { color: var(--blue); }

.section-light .state-pill:hover,
.section-white .state-pill:hover {
  background: rgba(0,113,227,.08);
  color: #0071e3;
  border-color: rgba(0,113,227,.3);
}
.section-light .cross-link:hover,
.section-white .cross-link:hover { color: #111114; border-color: rgba(0,0,0,.22); }

.section-light .compare-table th,
.section-white .compare-table th { background: #e8e8ed; color: #111114; }
.section-light .compare-table td,
.section-white .compare-table td,
.section-light .compare-table td:first-child,
.section-white .compare-table td:first-child { color: #111114; }
.section-light .compare-table .treat-us,
.section-white .compare-table .treat-us { color: var(--green) !important; }
.section-light .compare-table .treat-er,
.section-white .compare-table .treat-er { color: #6e6e73 !important; }
.section-light .compare-table tr:nth-child(even) td,
.section-white .compare-table tr:nth-child(even) td { background: rgba(0,0,0,.015); }

.section-light .er-box,
.section-white .er-box { background: rgba(229,72,77,.04); }

.section-light .fit-good,
.section-white .fit-good { background: rgba(25,164,99,.05); }
.section-light .fit-bad,
.section-white .fit-bad { background: rgba(229,72,77,.05); }

/* Treat-maybe badge for "sometimes we can help" */
.treat-maybe { color: var(--orange) !important; font-weight: 600 !important; }
.treat-us-also { color: var(--green) !important; font-weight: 600 !important; }

/* ── DARK-TO-LIGHT TRANSITIONS ── */
.dark-to-light {
  position:relative;z-index:2;
  clip-path:polygon(0 56px,100% 0,100% 100%,0 100%);
  margin-top:-56px;
  padding-top:calc(80px + 56px);
}
@media(max-width:600px){
  .dark-to-light{clip-path:polygon(0 32px,100% 0,100% 100%,0 100%);margin-top:-32px;padding-top:calc(56px + 32px)}
}

/* ── BLUE POP ── */
.section-light .section-kicker,
.section-white .section-kicker {
  background:rgba(0,113,227,.1);
  border:1px solid rgba(0,113,227,.22);
  border-radius:999px;
  padding:4px 14px;
}
.section-light .bento-card,
.section-white .bento-card {
  border-left:3px solid var(--blue);
}
.section-light .bento-card:hover,
.section-white .bento-card:hover {
  box-shadow:0 8px 32px rgba(0,113,227,.1);
}
.section-light .step-num,
.section-white .step-num {
  box-shadow:0 0 0 6px rgba(0,113,227,.12);
}
.section-light .guide-card,
.section-white .guide-card {
  border-top:2px solid var(--blue);
}
.section-light .guide-card:hover,
.section-white .guide-card:hover {
  box-shadow:0 4px 20px rgba(0,113,227,.1);
}

/* ── PHONE MOCKUP ── */
.hero-split {
  display:grid;
  grid-template-columns:1fr auto;
  gap:64px;
  align-items:center;
  text-align:left;
  max-width:1060px;
}
.hero-split .hero-actions{justify-content:flex-start}
.hero-split .hero-trust{justify-content:flex-start}

.phone-float {
  display:flex;align-items:center;justify-content:center;
  animation:float 6s ease-in-out infinite;
  filter:drop-shadow(0 40px 60px rgba(0,113,227,.35));
}
.phone-frame {
  width:264px;
  background:#18181c;
  border-radius:46px;
  padding:10px;
  box-shadow:
    0 0 0 1px rgba(255,255,255,.12),
    0 0 0 10px rgba(255,255,255,.03),
    inset 0 0 0 1px rgba(0,0,0,.6);
}
.phone-notch {
  width:88px;height:22px;
  background:#18181c;
  border-radius:0 0 14px 14px;
  margin:0 auto 6px;
}
.phone-screen {
  background:#000;
  border-radius:36px;
  overflow:hidden;
  display:flex;flex-direction:column;
}
.imsg-header {
  background:rgba(24,24,28,.96);
  backdrop-filter:blur(10px);
  padding:10px 14px 8px;
  display:flex;align-items:center;gap:10px;
  border-bottom:1px solid rgba(255,255,255,.07);
}
.imsg-avatar {
  width:34px;height:34px;
  border-radius:50%;object-fit:cover;
  border:1.5px solid rgba(0,113,227,.7);
  flex-shrink:0;
}
.imsg-name{font-size:12px;font-weight:700;color:#fff;line-height:1.2}
.imsg-status{font-size:10px;color:var(--green);font-weight:500}
.imsg-body {
  padding:12px 10px 16px;
  display:flex;flex-direction:column;gap:7px;
}
.imsg-bubble {
  max-width:80%;padding:8px 12px;
  border-radius:18px;
  font-size:11.5px;line-height:1.5;
}
.imsg-bubble.user {
  background:var(--blue);color:#fff;
  align-self:flex-end;border-bottom-right-radius:4px;
}
.imsg-bubble.chris {
  background:#2c2c2e;color:#e5e5ea;
  align-self:flex-start;border-bottom-left-radius:4px;
}
.imsg-rx {
  align-self:flex-start;
  background:rgba(25,164,99,.15);
  border:1px solid rgba(25,164,99,.35);
  border-radius:12px;
  padding:7px 12px;
  font-size:11px;font-weight:600;color:#19a463;
  display:flex;align-items:center;gap:6px;
}
.imsg-time{font-size:10px;color:#6e6e73;text-align:center}

.chris-avatar {
  width:52px;height:52px;border-radius:50%;
  object-fit:cover;
  border:2px solid var(--blue);
  margin-bottom:12px;display:block;
}

@media(max-width:900px){
  .hero-split{grid-template-columns:1fr;text-align:center}
  .hero-split .hero-actions,.hero-split .hero-trust{justify-content:center}
  .phone-float{display:none}
}

/* ── REDUCED MOTION ── */
@media(prefers-reduced-motion:reduce){
  .scroll-track{animation:none}
  *{transition-duration:.01ms!important;animation-duration:.01ms!important}
}

/* ── DESKTOP QR + PHONE CTA (sms: links fail on desktop) ── */
.npc-qr-cta{display:none}
@media(min-width:769px){
  .npc-sms-cta{display:none!important}
  .npc-qr-cta{
    display:inline-flex;align-items:center;gap:18px;
    padding:16px 20px;border-radius:var(--radius);
    background:var(--panel-3);
    border:1px solid var(--line);
    box-shadow:0 8px 30px rgba(0,0,0,.35);
    text-align:left;
  }
  .npc-qr-code{
    width:118px;height:118px;padding:8px;border-radius:14px;background:#fff;flex-shrink:0;
  }
  .npc-qr-code img,.npc-qr-code canvas{display:block;width:100%!important;height:100%!important}
  .npc-qr-meta{display:flex;flex-direction:column;gap:3px}
  .npc-qr-label{color:var(--blue-bright);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
  .npc-qr-phone{color:#fff;font-size:26px;font-weight:800;letter-spacing:-0.03em;line-height:1.05}
  .npc-qr-sub{color:var(--muted);font-size:13px;font-weight:600}
}

/* ── NPC WOODS vs BIG TELEHEALTH ── */
.vs-section{padding:52px 24px;background:var(--panel);border-bottom:1px solid var(--line)}
.vs-inner{max-width:720px;margin:0 auto}
.vs-head{text-align:center;margin-bottom:26px}
.vs-head .section-kicker{margin-bottom:10px}
.vs-head h2{font-size:clamp(24px,4vw,40px);font-weight:800;letter-spacing:-0.045em;margin-bottom:8px}
.vs-head p{color:var(--muted);font-size:14px}
.vs-grid{
  display:grid;grid-template-columns:1.1fr 1fr 1fr;
  border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;
  background:var(--panel-2);box-shadow:0 12px 40px rgba(0,0,0,.35);
}
.vs-cell{padding:13px 14px;border-bottom:1px solid var(--line);font-size:14px;display:flex;align-items:center;line-height:1.35}
.vs-grid > .vs-cell:nth-last-child(-n+3){border-bottom:none}
.vs-corner{background:var(--panel-3)}
.vs-us-head,.vs-them-head{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;justify-content:center;text-align:center}
.vs-us-head{background:var(--blue);color:#fff}
.vs-them-head{background:var(--panel-3);color:var(--body)}
.vs-feature{font-weight:700;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:0.05em;background:var(--panel-3)}
.vs-us{background:rgba(0,113,227,.10);color:#fff;font-weight:700}
.vs-them{color:var(--muted)}
.vs-check{color:var(--green);margin-right:7px;font-weight:800;flex-shrink:0}
@media(max-width:600px){
  .vs-section{padding:40px 16px}
  .vs-cell{padding:11px 9px;font-size:12px}
  .vs-feature{font-size:10px}
  .vs-us-head,.vs-them-head{font-size:10px}
  .vs-check{margin-right:4px}
}

/* Phoenix-style site header on dark gold plates — light bar, always on top of the hero */
.npc-nav{
  position:sticky;top:0;z-index:10000;
  background:#ffffff !important;
  border-bottom:1px solid #e5e7eb;
}
.npc-nav-inner{height:64px}
.npc-nav-logo-name,
.npc-nav-links > li > a:not(.npc-nav-cta){
  color:#1A1A2E !important;
  -webkit-text-fill-color:#1A1A2E !important;
}
.npc-nav-logo-tag{
  color:#2563EB !important;
  -webkit-text-fill-color:#2563EB !important;
}
.npc-nav-links > li > a.npc-nav-cta,
.npc-nav-cta,
.npc-nav-cta-mobile{
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
}
.npc-nav-cta svg,
.npc-nav-cta-mobile svg{
  stroke:#FFFFFF !important;
  color:#FFFFFF !important;
}
.npc-nav-toggle span{background:#1A1A2E !important}
.hero{padding-top:28px}



/* === Preview-only extras for homepage content in UTI rhythm === */

/* Meet Chris (homepage content in UTI rhythm) */
.meet-section{
  background:var(--panel-2);
  padding:72px 24px;
  border-top:1px solid var(--line);
}
.meet-inner{
  max-width:var(--max);margin:0 auto;
  display:grid;grid-template-columns:minmax(0,0.9fr) minmax(0,1.1fr);
  gap:48px;align-items:center;
}
.meet-photo{
  width:100%;border-radius:20px;display:block;
  box-shadow:0 24px 60px rgba(0,0,0,.45);
  aspect-ratio:4/5;object-fit:cover;object-position:center top;
}
.meet-section .section-kicker{margin-bottom:10px}
.meet-section h2{
  font-family:'DM Serif Display',serif;
  font-size:clamp(2rem,4vw,3rem);
  color:#fff;margin:0 0 18px;font-weight:400;letter-spacing:-0.02em;
}
.meet-section p{
  color:var(--body);font-size:1.05rem;line-height:1.65;margin:0 0 14px;
}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 16px}
.chip{
  display:inline-flex;align-items:center;
  padding:6px 12px;border-radius:999px;
  background:rgba(255,255,255,.06);border:1px solid var(--line);
  color:#fff;font-size:12px;font-weight:600;letter-spacing:0.02em;
}
.meet-links{display:flex;gap:18px;flex-wrap:wrap}
.meet-links a{color:var(--blue-bright);font-weight:600;font-size:14px;text-decoration:none}
.meet-links a:hover{text-decoration:underline}

/* States pills */
.states-section{
  background:var(--bg);padding:72px 24px;border-top:1px solid var(--line);
}
.states-inner{max-width:var(--max);margin:0 auto;text-align:center}
.states-pills{
  display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:28px;
}
.state-pill{
  display:inline-flex;padding:10px 16px;border-radius:999px;
  background:var(--panel);border:1px solid var(--line);
  color:#fff;font-size:14px;font-weight:600;text-decoration:none;
  transition:border-color .15s, background .15s;
}
.state-pill:hover{border-color:var(--blue);background:rgba(0,113,227,.12)}

/* Treat grid */
.treat-section{
  background:var(--panel);padding:72px 24px;border-top:1px solid var(--line);
}
.treat-inner{max-width:var(--max);margin:0 auto}
.treat-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
  gap:10px;margin-top:28px;
}
.treat{
  display:flex;align-items:center;justify-content:center;text-align:center;
  padding:16px 12px;border-radius:14px;
  background:var(--panel-2);border:1px solid var(--line);
  color:#fff;font-size:14px;font-weight:600;text-decoration:none;
  transition:border-color .15s, transform .15s;
}
.treat small{display:block;font-weight:500;color:var(--muted);font-size:11px;margin-top:4px}
.treat:hover{border-color:var(--blue);transform:translateY(-1px)}

/* Pain / old way as light cards in dark theme */
.pain-section{
  background:var(--panel-2);padding:72px 24px;border-top:1px solid var(--line);
}
.pain-inner{max-width:var(--max);margin:0 auto}
.pain-list{
  display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:16px;margin-top:28px;
}
.pain{
  display:flex;gap:14px;padding:20px;border-radius:16px;
  background:var(--panel);border:1px solid var(--line);
}
.pain .x{
  flex:0 0 28px;height:28px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:rgba(239,68,68,.15);color:#f87171;font-weight:800;
}
.pain h3{color:#fff;font-size:16px;margin:0 0 6px}
.pain p{color:var(--body);font-size:14px;margin:0;line-height:1.5}
.quote-block{
  margin-top:28px;text-align:center;
  font-family:'DM Serif Display',serif;
  font-size:clamp(1.25rem,2.5vw,1.75rem);color:#fff;
}

/* Price block */
.price-block{
  background:var(--bg);padding:64px 24px;text-align:center;border-top:1px solid var(--line);
}
.price-block .big{
  font-size:clamp(56px,10vw,96px);font-weight:900;letter-spacing:-0.06em;
  background:linear-gradient(120deg,#fff,var(--blue-bright));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  line-height:1;margin-bottom:8px;
}
.price-block h2{
  font-family:'DM Serif Display',serif;color:#fff;
  font-size:clamp(1.75rem,3vw,2.5rem);margin:0 0 12px;font-weight:400;
}
.price-block p{color:var(--body);max-width:42ch;margin:0 auto 24px;line-height:1.6}

/* Safety note */
.safety-wrap{max-width:var(--max);margin:0 auto;padding:0 24px 48px}
.safety{
  padding:18px 20px;border-radius:14px;
  background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.25);
  color:var(--body);font-size:14px;line-height:1.55;
}
.safety b{color:#fff;display:block;margin-bottom:4px}

/* Override light homepage leftovers */
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif}
a{color:inherit}

@media (max-width:860px){
  .meet-inner{grid-template-columns:1fr;gap:28px}
  .meet-photo{max-width:360px;margin:0 auto}
  .pain-list{grid-template-columns:1fr}
}

#npcSaveWrap, body::after { display: none !important; content: none !important; }
</style>
<body>
<!-- ===== Sticky header / nav (UTI page pattern) ===== -->
<nav class="npc-nav" aria-label="Main navigation">
  <div class="npc-nav-inner">
    <a href="https://npcwoods.com" class="npc-nav-logo">
      <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="NPCWoods" width="38" height="38">
      <div class="npc-nav-logo-text">
        <span class="npc-nav-logo-name">NPCWoods</span>
        <span class="npc-nav-logo-tag">Telemedicine</span>
      </div>
    </a>

    <ul class="npc-nav-links">
      <li>
        <a href="https://npcwoods.com/conditions/">Conditions <span class="nav-arrow">&#9662;</span></a>
        <div class="npc-dropdown">
          <a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a>
          <a href="https://npcwoods.com/sinus-infection-treatment/">Sinus Infection</a>
          <a href="https://npcwoods.com/dental-pain/">Dental Pain</a>
          <a href="https://npcwoods.com/ear-infection-treatment/">Ear Infection</a>
          <a href="https://npcwoods.com/ed-treatment/">ED Treatment</a>
          <a href="https://npcwoods.com/conditions/">View All Conditions</a>
        </div>
      </li>
      <li><a href="https://npcwoods.com/how-it-works/">How It Works</a></li>
      <li><a href="https://npcwoods.com/pricing/">Pricing</a></li>
      <li>
        <a href="#states">States <span class="nav-arrow">&#9662;</span></a>
        <div class="npc-dropdown">
          <a href="https://npcwoods.com/arizona-telemedicine/">Arizona</a>
          <a href="https://npcwoods.com/colorado-telemedicine/">Colorado</a>
          <a href="https://npcwoods.com/georgia-telemedicine/">Georgia</a>
          <a href="https://npcwoods.com/idaho-telemedicine/">Idaho</a>
          <a href="https://npcwoods.com/iowa-telemedicine/">Iowa</a>
          <a href="https://npcwoods.com/montana-telemedicine/">Montana</a>
          <a href="https://npcwoods.com/nevada-telemedicine/">Nevada</a>
          <a href="https://npcwoods.com/new-mexico-telemedicine/">New Mexico</a>
          <a href="https://npcwoods.com/north-carolina-telemedicine/">North Carolina</a>
          <a href="https://npcwoods.com/oregon-telemedicine/">Oregon</a>
          <a href="https://npcwoods.com/utah-telemedicine/">Utah</a>
          <a href="https://npcwoods.com/washington-telemedicine/">Washington</a>
        </div>
      </li>
      <li><a href="https://npcwoods.com/blog/">Blog</a></li>
      <li><a href="https://npcwoods.com/credentials/">Credentials</a></li>
      <li>
        <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="npc-nav-cta">
          <span class="npc-cta-dot"></span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
          $59. Text Chris Now
        </a>
      </li>
    </ul>

    <button class="npc-nav-toggle" id="npcHamburger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<main>

<!-- HERO: UTI split layout + homepage messaging (no antibiotics / drug names) -->
<section class="hero">
  <div class="hero-inner hero-split">
    <div class="hero-text">
      <div class="hero-kicker">
        <span class="hero-dot"></span>
        $59 Flat &nbsp;·&nbsp; No Waiting Room &nbsp;·&nbsp; Pay After Care
      </div>
      <h1>You feel awful. The system makes you work for it.</h1>
      <p class="hero-sub">A half-day in a waiting room for a ten-minute problem. Or you text me from the couch. Same problem. Different day. Text a double board-certified Nurse Practitioner. No video. No app. No chatbot.</p>
      <div class="hero-actions">
        <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary npc-sms-cta">Text Chris Now: (480) 639-4722</a>
        <a href="#how-it-works" class="btn-ghost">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>🔒 HIPAA-Compliant</span>
        <span>⭐ 50+ Five-Star Reviews</span>
        <span>📱 No video · Just text</span>
      </div>
    </div>
    <div class="phone-float">
      <div class="phone-frame">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <div class="imsg-header">
            <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="imsg-avatar" alt="Chris">
            <div>
              <div class="imsg-name">Chris @ NPCWoods</div>
              <div class="imsg-status">● Available now</div>
            </div>
          </div>
          <div class="imsg-body">
            <div class="imsg-time">Today 10:08 AM</div>
            <div class="imsg-bubble user">Hey Chris — sinus pressure + sore throat since yesterday. Can you help?</div>
            <div class="imsg-bubble chris">Hey! Happy to take a look. Any fever? How long have you felt like this?</div>
            <div class="imsg-bubble user">Low fever last night. Started ~36 hours ago. No trouble breathing.</div>
            <div class="imsg-bubble chris">Got it. Plan coming your way — Rx to your pharmacy + written instructions.</div>
            <div class="imsg-rx">✓ Care plan sent · pharmacy notified</div>
            <div class="imsg-time" style="margin-top:4px">10:52 AM</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ATF answer (homepage facts, UTI rhythm) -->
<div class="npc-atf-answer" data-npc-aeo="atf-answer">
  <p>
    <strong>NPCWoods</strong> is a $59 text visit with Chris Woods, MSN, APRN, FNP-C, a licensed Nurse Practitioner.
    Text <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>.
    No video. No app. No chatbot. You must be physically in a licensed state at the time of the visit.
    A prescription is not promised. You only pay if he can treat you.
  </p>
</div>

<!-- STATS BAND -->
<div class="stats-band">
  <div class="stats-inner">
    <div class="stat"><div class="stat-n">$59</div><div class="stat-l">Flat fee, no surprises</div></div>
    <div class="stat"><div class="stat-n">Pay after</div><div class="stat-l">Only if he can treat you</div></div>
    <div class="stat"><div class="stat-n">Same day</div><div class="stat-l">Usually hours, not days</div></div>
  </div>
</div>

<!-- OLD WAY / pain (homepage content) -->
<section class="pain-section">
  <div class="pain-inner">
    <span class="section-kicker">Why people text instead</span>
    <h2 class="section-title" style="color:#fff;font-family:'DM Serif Display',serif;font-size:clamp(1.75rem,3.5vw,2.5rem);font-weight:400;margin:8px 0 8px">The old way is the expensive part.</h2>
    <p class="section-body" style="color:var(--body);max-width:50ch">Not the medicine. Not the visit. The runaround.</p>
    <div class="pain-list">
      <article class="pain"><div class="x">×</div><div><h3>3-hour waits</h3><p>A half-day in an urgent care lobby for something I can sort out in a few texts.</p></div></article>
      <article class="pain"><div class="x">×</div><div><h3>$200 for a $20 fix</h3><p>Surprise bills for simple care you already knew you needed.</p></div></article>
      <article class="pain"><div class="x">×</div><div><h3>No clinic close by</h3><p>The nearest option is far, closed, or booked out for days.</p></div></article>
      <article class="pain"><div class="x">×</div><div><h3>Forms and denials</h3><p>Portals, paperwork, and fine print after the fact.</p></div></article>
    </div>
    <div class="quote-block"><p>I built the practice I would want for my own family.</p></div>
  </div>
</section>

<!-- COMPARISON: NPCWoods vs Big Telehealth (homepage rows; NOT UTI differential) -->
<section class="vs" id="compare">
  <div class="vs-inner">
    <div class="vs-head">
      <span class="section-kicker">The honest comparison</span>
      <h2>NPCWoods vs. Big Telehealth</h2>
      <p>A real NP in your messages. None of the games.</p>
    </div>
    <div class="vs-grid">
      <div class="vs-cell vs-corner"></div>
      <div class="vs-cell vs-us-head">NPCWoods</div>
      <div class="vs-cell vs-them-head">Big Telehealth</div>

      <div class="vs-cell vs-feature">Price</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>$59 flat fee</div>
      <div class="vs-cell vs-them">Membership plus visit fees</div>

      <div class="vs-cell vs-feature">Who reads it</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>Chris Woods, NP</div>
      <div class="vs-cell vs-them">Call center or algorithm</div>

      <div class="vs-cell vs-feature">App</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>None. Just text</div>
      <div class="vs-cell vs-them">Download required</div>

      <div class="vs-cell vs-feature">Pay</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>After you're treated</div>
      <div class="vs-cell vs-them">Up front, then extras</div>

      <div class="vs-cell vs-feature">Waiting room</div>
      <div class="vs-cell vs-us"><span class="vs-check">✓</span>None — from your couch</div>
      <div class="vs-cell vs-them">Lobby or video queue</div>
    </div>
  </div>
</section>

<!-- SCROLLING REVIEWS (real quotes already on npcwoods.com) -->
<section class="reviews">
  <div class="reviews-head">
    <div class="stars-row">
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
    </div>
    <h2>50+ Five-Star Reviews</h2>
    <p>Real patients. Real reviews. From Facebook &amp; Google.</p>
  </div>
  <div class="scroll-mask">
    <div class="scroll-track">
      <div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Chris texted me back within seconds and had my prescription over to the pharmacy within minutes..so simple and easy definitely beats sitting in a waiting room. Recommend 100%!"</p><div class="rcard-foot"><span class="rcard-author">J.R.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Very fast and convenient. I first messaged Chris at 10:08am and I was picking up my prescriptions from the pharmacy at 10:52am same day! Cannot recommend enough!!!!"</p><div class="rcard-foot"><span class="rcard-author">A.H.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Fast, easy, no waiting, very professional. I recommend him to everyone."</p><div class="rcard-foot"><span class="rcard-author">D.C.D.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Messaged Chris he responded in a timely manner. Very professional. Easy to talk to about our concerns. It was nice to be able to stay at home and get quality care."</p><div class="rcard-foot"><span class="rcard-author">T.P.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"I had a great experience with NPCWoods Telemed Clinic! Chris was incredibly efficient and genuinely helpful. He made the whole process quick and stress-free."</p><div class="rcard-foot"><span class="rcard-author">H.P.W.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Literally cannot recommend enough! My daughter had the worst cough ever and it was so bad on a Saturday night after midnight, I text Chris, he replied immediately."</p><div class="rcard-foot"><span class="rcard-author">A.A.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"I texted Chris out of nowhere on a Sunday and he answered straight away. Lightning-quick."</p><div class="rcard-foot"><span class="rcard-author">B.P.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"I texted Chris at 10pm and he responded within 15 minutes. When the pharmacy didn’t have it, he called the store himself."</p><div class="rcard-foot"><span class="rcard-author">M.D.</span><span class="rcard-source">Facebook</span></div></div>
      <!-- Duplicate for infinite scroll -->
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Chris texted me back within seconds and had my prescription over to the pharmacy within minutes..so simple and easy definitely beats sitting in a waiting room. Recommend 100%!"</p><div class="rcard-foot"><span class="rcard-author">J.R.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Very fast and convenient. I first messaged Chris at 10:08am and I was picking up my prescriptions from the pharmacy at 10:52am same day! Cannot recommend enough!!!!"</p><div class="rcard-foot"><span class="rcard-author">A.H.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Fast, easy, no waiting, very professional. I recommend him to everyone."</p><div class="rcard-foot"><span class="rcard-author">D.C.D.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Messaged Chris he responded in a timely manner. Very professional. Easy to talk to about our concerns. It was nice to be able to stay at home and get quality care."</p><div class="rcard-foot"><span class="rcard-author">T.P.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"I had a great experience with NPCWoods Telemed Clinic! Chris was incredibly efficient and genuinely helpful. He made the whole process quick and stress-free."</p><div class="rcard-foot"><span class="rcard-author">H.P.W.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"Literally cannot recommend enough! My daughter had the worst cough ever and it was so bad on a Saturday night after midnight, I text Chris, he replied immediately."</p><div class="rcard-foot"><span class="rcard-author">A.A.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"I texted Chris out of nowhere on a Sunday and he answered straight away. Lightning-quick."</p><div class="rcard-foot"><span class="rcard-author">B.P.</span><span class="rcard-source">Facebook</span></div></div>
<div class="rcard"><div class="stars-row" style="margin-bottom:10px"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div><p class="rcard-text">"I texted Chris at 10pm and he responded within 15 minutes. When the pharmacy didn’t have it, he called the store himself."</p><div class="rcard-foot"><span class="rcard-author">M.D.</span><span class="rcard-source">Facebook</span></div></div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS (homepage content, UTI section rhythm) -->
<section id="how-it-works" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">How it works</span>
    <h2 class="section-title">Three texts from feeling better.</h2>
    <p class="section-body">Usually within a few hours — first text to the pharmacy. No app, no portal, no video call — just text.</p>
    <div class="bento">
      <div class="bento-card">
        <div class="step-num">1</div>
        <h3>Text me your symptoms</h3>
        <p>In your own words. No 30-question form. No portal. No app. Text <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">2</div>
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="chris-avatar" alt="Chris Woods NP">
        <h3>I actually read it</h3>
        <p>I look at your history, ask what I need, and build a plan for you. Not a template. Not a bot.</p>
      </div>
      <div class="bento-card">
        <div class="step-num">3</div>
        <h3>Pick up and feel better</h3>
        <p>Sent to your pharmacy. Written plan to your inbox. That is it.</p>
      </div>
    </div>
  </div>
</section>

<!-- PRICE BLOCK -->
<div class="price-block">
  <div class="big">$59</div>
  <h2>That’s the whole thing.</h2>
  <p>Pay after you’re treated. If I can’t safely help you by text, I’ll tell you straight up — and you don’t pay a dime.</p>
  <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary npc-sms-cta">Text Chris now</a>
</div>

<!-- MEET CHRIS + real photo -->
<section class="meet-section" id="chris">
  <div class="meet-inner">
    <img class="meet-photo" src="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, MSN, APRN, FNP-C, Nurse Practitioner" width="1000" height="1250" loading="lazy">
    <div>
      <span class="section-kicker">Meet your NP</span>
      <h2>Hey, I'm Chris.</h2>
      <p>I spent years watching people lose a whole day and a couple hundred bucks over something I could sort out in a few texts. That never sat right with me.</p>
      <p>So I built the practice I would want for my own family. Text a real Nurse Practitioner, get actually listened to, and pay one honest price.</p>
      <p>No runaround. No surprise bills. No pretending a chatbot is care. Faith and family keep me grounded, and they are why I treat every visit like it is someone I love.</p>
      <div class="chips">
        <span class="chip">MSN, APRN, FNP-C</span>
        <span class="chip">Double board-certified</span>
        <span class="chip">NPI 1285125468</span>
        <span class="chip">Real clinician review</span>
      </div>
      <div class="meet-links">
        <a href="https://npcwoods.com/credentials/">Credentials</a>
        <a href="https://npcwoods.com/services/">What I treat</a>
      </div>
    </div>
  </div>
</section>

<!-- COMMON VISITS (homepage) -->
<section class="treat-section">
  <div class="treat-inner">
    <span class="section-kicker">What I treat by text</span>
    <h2 class="section-title" style="color:#fff;font-family:'DM Serif Display',serif;font-size:clamp(1.75rem,3.5vw,2.5rem);font-weight:400;margin:8px 0 8px">Common $59 visits.</h2>
    <p style="color:var(--body);max-width:50ch;margin:0">If it is safe to handle by text, I will. If it is not, I will say so and you do not pay.</p>
    <div class="treat-grid">
      <a class="treat" href="https://npcwoods.com/uti-treatment/">UTI</a>
      <a class="treat" href="https://npcwoods.com/sinus-infection-treatment/">Sinus infection</a>
      <a class="treat" href="https://npcwoods.com/strep-throat-treatment/">Strep throat</a>
      <a class="treat" href="https://npcwoods.com/ear-infection-treatment/">Ear infection</a>
      <a class="treat" href="https://npcwoods.com/pink-eye-treatment/">Pink eye</a>
      <a class="treat" href="https://npcwoods.com/learn/bronchitis/">Bronchitis / cough</a>
      <a class="treat" href="https://npcwoods.com/learn/skin-infection/">Skin infection</a>
      <a class="treat" href="https://npcwoods.com/dental-pain/">Tooth infection <small>bridge only, dentist still required</small></a>
      <a class="treat" href="https://npcwoods.com/learn/stomach-bug/">Stomach bug</a>
      <a class="treat" href="https://npcwoods.com/learn/cold-sores/">Cold sores</a>
      <a class="treat" href="https://npcwoods.com/learn/covid-flu/">COVID / flu</a>
      <a class="treat" href="https://npcwoods.com/learn/allergic-reaction/">Allergies</a>
      <a class="treat" href="https://npcwoods.com/learn/acid-reflux/">Acid reflux</a>
      <a class="treat" href="https://npcwoods.com/learn/acne/">Acne</a>
      <a class="treat" href="https://npcwoods.com/yeast-infection-treatment/">Yeast infection</a>
      <a class="treat" href="https://npcwoods.com/learn/ingrown-toenail/">Ingrown toenail</a>
      <a class="treat" href="https://npcwoods.com/poison-ivy/">Poison ivy</a>
      <a class="treat" href="https://npcwoods.com/ed-treatment/">ED</a>
      <a class="treat" href="https://npcwoods.com/services/">Medication refills</a>
      <a class="treat" href="https://npcwoods.com/glp1-weight-loss/">GLP-1 consult <small>fit and safety, drug cost separate</small></a>
      <a class="treat" href="https://npcwoods.com/learn/glp1/">GLP-1, explained <small>how they work, side effects</small></a>
    </div>
  </div>
</section>

<!-- STATES -->
<section class="states-section" id="states">
  <div class="states-inner">
    <span class="section-kicker">Where I can help</span>
    <h2 class="section-title" style="color:#fff;font-family:'DM Serif Display',serif;font-size:clamp(1.75rem,3.5vw,2.5rem);font-weight:400;margin:8px 0 8px">Serving 13 states.</h2>
    <p style="color:var(--body);max-width:50ch;margin:0 auto">12 state NP licenses, plus Florida by telehealth registration. You have to be physically in one of these states at the time of the visit.</p>
    <div class="states-pills">
        <a class="state-pill" href="https://npcwoods.com/arizona-telemedicine/">Arizona</a>
        <a class="state-pill" href="https://npcwoods.com/colorado-telemedicine/">Colorado</a>
        <a class="state-pill" href="https://npcwoods.com/georgia-telemedicine/">Georgia</a>
        <a class="state-pill" href="https://npcwoods.com/idaho-telemedicine/">Idaho</a>
        <a class="state-pill" href="https://npcwoods.com/iowa-telemedicine/">Iowa</a>
        <a class="state-pill" href="https://npcwoods.com/montana-telemedicine/">Montana</a>
        <a class="state-pill" href="https://npcwoods.com/nevada-telemedicine/">Nevada</a>
        <a class="state-pill" href="https://npcwoods.com/new-mexico-telemedicine/">New Mexico</a>
        <a class="state-pill" href="https://npcwoods.com/north-carolina-telemedicine/">North Carolina</a>
        <a class="state-pill" href="https://npcwoods.com/oregon-telemedicine/">Oregon</a>
        <a class="state-pill" href="https://npcwoods.com/utah-telemedicine/">Utah</a>
        <a class="state-pill" href="https://npcwoods.com/washington-telemedicine/">Washington</a>
        <a class="state-pill" href="https://npcwoods.com/florida-vacation-sick-text-visit/">Florida <small style="font-weight:500;opacity:.75;margin-left:4px">telehealth reg.</small></a>
    </div>
    <p style="color:var(--muted);font-size:14px;margin-top:22px">Licensed in Arizona, Colorado, Georgia, Idaho, Iowa, Montana, Nevada, New Mexico, North Carolina, Oregon, Utah, and Washington. Florida by Out-of-State Telehealth Provider registration (TPAN3355).</p>
    <h3 style="color:#fff;font-family:'DM Serif Display',serif;font-size:clamp(1.25rem,2.6vw,1.6rem);font-weight:400;margin:40px 0 6px">Rural shortage areas</h3>
    <p style="color:var(--body);max-width:56ch;margin:0 auto">Long drive to the nearest clinic? These counties have few local options. A $59 text works the same there.</p>
    <div class="states-pills">
        <a class="state-pill" href="https://npcwoods.com/colfax-county-text-visit/">Colfax County, NM</a>
        <a class="state-pill" href="https://npcwoods.com/humboldt-county-text-visit/">Humboldt County, NV</a>
        <a class="state-pill" href="https://npcwoods.com/emery-county-text-visit/">Emery County, UT</a>
        <a class="state-pill" href="https://npcwoods.com/park-county-text-visit/">Park County, CO</a>
        <a class="state-pill" href="https://npcwoods.com/winnebago-county-text-visit/">Winnebago County, IA</a>
    </div>
  </div>
</section>

<div class="safety-wrap">
  <div class="safety">
    <b>Emergencies</b>
    <p>Text care is not for chest pain, trouble breathing, severe allergic reaction, or anything that feels life-threatening. Call 911 or go to the nearest emergency room.</p>
  </div>
</div>

<!-- BOTTOM TEXT CTA (UTI rhythm + homepage voice) -->
<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>Text me. I’ve got you.</h2>
    <p>$59 flat. A real Nurse Practitioner. Right from your couch. No video. Pay after care.</p>
    <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary npc-sms-cta" style="font-size:16px;padding:16px 32px">Text Chris Now: (480) 639-4722</a>
    <div class="bottom-trust-line">
      <span>🔒 HIPAA-Compliant &amp; Secure</span>
      <span>📱 No video · Just text</span>
      <span>💊 Sent same-day to your local pharmacy</span>
    </div>
    <p style="margin-top:18px;color:var(--muted);font-size:13px">Chris Woods, MSN, APRN, FNP-C · Not a chatbot · Pay after care</p>
  </div>
</section>

</main>

<a class="mobile-cta" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now · $59</a>

<script>
/* Minimal sticky-nav hamburger (matches UTI/shared behavior enough for preview) */
(function(){
  var btn = document.getElementById('npcHamburger');
  var nav = document.querySelector('.npc-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function(){
    var open = nav.classList.toggle('npc-nav-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
</script>
<?php
$GLOBALS['npcwoods_shared_footer_rendered'] = true;
$npcwoods_footer = defined('ABSPATH') ? ABSPATH . 'shared/footer-snippet.html' : '';
if ($npcwoods_footer && is_readable($npcwoods_footer)) {
    readfile($npcwoods_footer);
} else {
?>
<footer class="npc-site-footer">
  <div class="npc-footer-inner">
    <div class="npc-footer-grid">
      <div class="npc-footer-brand">
        <div class="npc-footer-brand-name">
          <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="NPCWoods" width="36" height="36">
          NPCWoods Telemedicine
        </div>
        <p>Text-based telehealth visits, $59 flat, no paperwork, no hassle. No appointment. Just text us what's going on and a licensed nurse practitioner will take care of you.</p>
        <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="npc-footer-cta">Text (480) 639-4722</a>
      </div>
      <div class="npc-footer-col">
        <h4>Conditions We Treat</h4>
        <ul>
          <li><a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a></li>
          <li><a href="https://npcwoods.com/sinus-infection-treatment/">Sinus Infection</a></li>
          <li><a href="https://npcwoods.com/dental-pain/">Dental Pain</a></li>
          <li><a href="https://npcwoods.com/ear-infection-treatment/">Ear Infection</a></li>
          <li><a href="https://npcwoods.com/learn/covid-flu/">Cold &amp; Flu</a></li>
          <li><a href="https://npcwoods.com/learn/allergic-reaction/">Allergies</a></li>
          <li><a href="https://npcwoods.com/learn/skin-infection/">Skin Rashes</a></li>
          <li><a href="https://npcwoods.com/ed-treatment/">ED Treatment</a></li>
          <li><a href="https://npcwoods.com/strep-throat-treatment/">Strep Throat</a></li>
          <li><a href="https://npcwoods.com/poison-ivy/">Poison Ivy</a></li>
          <li><a href="https://npcwoods.com/glp1-weight-loss/">GLP-1 Weight Loss</a></li>
          <li><a href="https://npcwoods.com/conditions/">View All &rarr;</a></li>
        </ul>
      </div>
      <div class="npc-footer-col">
        <h4>States We Serve</h4>
        <ul>
          <li><a href="https://npcwoods.com/arizona-telemedicine/">Arizona</a></li>
          <li><a href="https://npcwoods.com/georgia-telemedicine/">Georgia</a></li>
          <li><a href="https://npcwoods.com/north-carolina-telemedicine/">North Carolina</a></li>
          <li><a href="https://npcwoods.com/new-mexico-telemedicine/">New Mexico</a></li>
          <li><a href="https://npcwoods.com/colorado-telemedicine/">Colorado</a></li>
          <li><a href="https://npcwoods.com/idaho-telemedicine/">Idaho</a></li>
          <li><a href="https://npcwoods.com/iowa-telemedicine/">Iowa</a></li>
          <li><a href="https://npcwoods.com/montana-telemedicine/">Montana</a></li>
          <li><a href="https://npcwoods.com/nevada-telemedicine/">Nevada</a></li>
          <li><a href="https://npcwoods.com/oregon-telemedicine/">Oregon</a></li>
          <li><a href="https://npcwoods.com/utah-telemedicine/">Utah</a></li>
          <li><a href="https://npcwoods.com/washington-telemedicine/">Washington</a></li>
          <li><a href="https://flhealthsource.gov/telehealth/" target="_blank" rel="noopener">Florida</a></li>
        </ul>
      </div>
      <div class="npc-footer-col">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="https://npcwoods.com/">Home</a></li>
          <li><a href="https://npcwoods.com/how-it-works/">How It Works</a></li>
          <li><a href="https://npcwoods.com/pricing/">Pricing, $59</a></li>
          <li><a href="https://npcwoods.com/faq/">FAQ</a></li>
          <li><a href="https://npcwoods.com/credentials/">Credentials &amp; Licenses</a></li>
          <li><a href="https://npcwoods.com/learn/">Patient Education</a></li>
          <li><a href="https://npcwoods.com/medications/">Medications</a></li>
          <li><a href="https://npcwoods.com/blog/">Blog</a></li>
          <li><a href="https://npcwoods.com/sitemap/">Site Map</a></li>
        </ul>
      </div>
    </div>
    <hr class="npc-footer-divider">
    <div class="npc-footer-bottom">
      <span>&copy; 2026 NPCWoods Telehealth. All rights reserved.</span>
      <span><a href="https://npcwoods.com">npcwoods.com</a></span>
    </div>
    <div class="npc-footer-trust">
      <a href="https://www.legitscript.com/websites/?checker_keywords=npcwoods.com" target="_blank" title="Verify LegitScript Approval for www.npcwoods.com" style="display:inline-block; margin-bottom:12px;">
        <img src="/assets/img/legitscript-seal.png" alt="Verify Approval for www.npcwoods.com" width="73" height="79" loading="lazy" decoding="async" />
      </a><br>
      Reviewed by Chris Woods, MSN, APRN, FNP-C. Double Board-Certified Nurse Practitioner<br>
      Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT, WA, plus Florida by telehealth registration (TPAN3355). 13 states served.<br>
      NPI: 1285125468 &bull; Mailing address: 3550 N Goldwater Blvd #1119, Scottsdale, AZ 85251 &bull; Phone: (480) 639-4722<br>
      <a href="https://npcwoods.com/about/">About Chris</a> &bull; <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">Verify NPI</a> &bull; <a href="https://npcwoods.com/medical-disclaimer/">Medical Disclaimer</a> &bull; <a href="https://npcwoods.com/privacy-policy/">Privacy Policy</a> &bull; <a href="https://npcwoods.com/notice-of-privacy-practices/">Notice of Privacy Practices</a> &bull; <a href="https://npcwoods.com/terms-of-service/">Terms of Service</a> &bull; <span class="npc-footer-hipaa-badge">HIPAA Compliant</span>
      <p class="npc-footer-emergency">Text-based telehealth is not for emergencies. If you have chest pain, trouble breathing, or other emergency symptoms, call 911.</p>
    </div>
  </div>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "@id": "https://npcwoods.com/#medical-business",
    "name": "NPCWoods",
    "alternateName": "NPCWoods Telemedicine",
    "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
    "telephone": "+14806394722",
    "url": "https://npcwoods.com",
    "logo": "https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg",
    "priceRange": "$59",
    "sameAs": [
      "https://share.google/XlmNvRT4vihOJ8KBH",
      "https://www.facebook.com/npcwoods",
      "https://www.legitscript.com/websites/?checker_keywords=npcwoods.com"
    ],
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "3550 N Goldwater Blvd #1119",
      "addressLocality": "Scottsdale",
      "addressRegion": "AZ",
      "postalCode": "85251",
      "addressCountry": "US"
    }
  }
  </script>
</footer>
<?php } ?>
<?php if (function_exists('wp_footer')) { wp_footer(); } ?>
</body>
</html>
