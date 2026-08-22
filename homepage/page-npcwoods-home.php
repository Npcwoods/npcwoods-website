<?php
/**
 * Template Name: NPCWoods Homepage
 * Pocket refresh 2026-08-21: urgent care in your pocket.
 * Tracking via wp_head()/wp_footer(). Do not enqueue TT4 / wp-block-library on this template.
 */
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#05060a">
<title>NPCWoods Telemedicine: $59 Text-Based Urgent Care</title>
<link rel="canonical" href="https://npcwoods.com/">
<meta property="og:title" content="NPCWoods Telemedicine: $59 Text-Based Urgent Care">
<meta property="og:description" content="Urgent care in your pocket. Text a real Nurse Practitioner. $59 flat. No waiting room. No app.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://npcwoods.com/">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp">
<meta name="description" content="Urgent care in your pocket. Text Chris Woods, a real Nurse Practitioner. $59 flat. Licensed in 11 states. No waiting room. No app.">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"MedicalBusiness","@id":"https://npcwoods.com/#medical-business","name":"NPCWoods Telemedicine","description":"Text-based urgent care with a licensed Nurse Practitioner. $59 flat fee. Licensed in 11 states.","telephone":"+14806394722","url":"https://npcwoods.com/","priceRange":"$59","areaServed":[{"@type":"State","name":"Arizona"},{"@type":"State","name":"Colorado"},{"@type":"State","name":"Georgia"},{"@type":"State","name":"Idaho"},{"@type":"State","name":"Iowa"},{"@type":"State","name":"Montana"},{"@type":"State","name":"Nevada"},{"@type":"State","name":"New Mexico"},{"@type":"State","name":"North Carolina"},{"@type":"State","name":"Oregon"},{"@type":"State","name":"Utah"}],"medicalSpecialty":"https://schema.org/FamilyPractice"}
</script>
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://www.googletagmanager.com">
<?php if (function_exists('wp_head')) { wp_head(); } ?>
<style>
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
  --red: #e5484d;
  --radius: 20px;
  --max: 1120px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  background:var(--bg);color:var(--ink);
  font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;
  line-height:1.5;-webkit-font-smoothing:antialiased;overflow-x:hidden;
}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
.skip-link{position:absolute;left:-9999px;top:0;z-index:2000;padding:10px 16px;background:#fff;color:#000;font-weight:700}
.skip-link:focus{left:14px}
.nav{
  position:sticky;top:0;z-index:50;height:56px;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 32px;
  background:transparent;
  border-bottom:1px solid transparent;
  transition:background .35s ease,border-color .35s ease,box-shadow .35s ease,height .35s ease;
}
.nav.is-scrolled{
  height:52px;
  background:rgba(5,6,10,0.72);
  backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);
  border-bottom-color:var(--line);
  box-shadow:0 10px 30px rgba(0,0,0,.28);
}
.nav-logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px}
.nav-logo img{width:32px;height:32px;border-radius:8px;object-fit:cover}
.nav-tag{display:block;font-size:11px;font-weight:500;color:var(--muted);letter-spacing:0}
.nav-cta{
  position:relative;overflow:hidden;
  background:var(--blue);color:#fff!important;-webkit-text-fill-color:#fff!important;
  border-radius:999px;padding:7px 16px;font-size:13px;font-weight:700;
  transition:box-shadow .25s ease,transform .2s ease;
}
.nav-cta::after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(105deg,transparent 30%,rgba(255,255,255,.28) 50%,transparent 70%);
  transform:translateX(-120%);
  transition:transform .6s ease;
}
.nav-cta:hover{box-shadow:0 0 0 3px rgba(0,113,227,.22),0 8px 24px rgba(0,113,227,.5);transform:translateY(-1px)}
.nav-cta:hover::after{transform:translateX(120%)}

.hero{
  position:relative;min-height:92vh;
  display:flex;align-items:center;justify-content:center;
  padding:80px 24px 60px;background:var(--bg);overflow:hidden;
}
.hero::before{
  content:'';position:absolute;top:-20%;left:50%;transform:translateX(-50%);
  width:900px;height:700px;
  background:radial-gradient(ellipse at center, rgba(0,113,227,0.28) 0%, transparent 65%);
  filter:blur(60px);pointer-events:none;
}
.hero::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:200px;
  background:linear-gradient(to bottom,transparent,var(--bg));pointer-events:none;
}
.hero-inner{position:relative;z-index:1;max-width:760px;margin:0 auto;text-align:center}
.hero-kicker{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
  border-radius:999px;padding:6px 16px;
  font-size:12px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;
  color:rgba(255,255,255,0.7);margin-bottom:28px;
}
.hero-dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(25,164,99,.2)}
.hero h1{
  font-size:clamp(42px,7.5vw,84px);font-weight:800;line-height:1.0;letter-spacing:-0.065em;
  color:#f4f8ff;margin-bottom:20px;
}
.pocket-word{
  background:linear-gradient(90deg,#ffffff 0%,#a8d4ff 35%,#2997ff 50%,#a8d4ff 65%,#ffffff 100%);
  background-size:220% 100%;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  animation:pocketSweep 4.8s ease-in-out infinite;
}
@keyframes pocketSweep{0%,100%{background-position:100% 0}50%{background-position:0 0}}
.text-caret{
  display:inline-block;width:2px;height:.62em;margin-left:4px;vertical-align:-1px;
  background:#2997ff;border-radius:1px;animation:blink 1.15s steps(1) infinite;
}
@keyframes blink{0%,50%{opacity:1}50.01%,100%{opacity:0}}
.hero-sub{
  font-size:clamp(16px,2vw,20px);color:var(--body);line-height:1.55;letter-spacing:-0.015em;
  max-width:560px;margin:0 auto 36px;
}
.hero-actions{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;margin-bottom:28px}
.btn-primary{
  background:var(--blue);color:#fff!important;-webkit-text-fill-color:#fff!important;
  border-radius:999px;padding:14px 28px;font-size:15px;font-weight:700;
  box-shadow:0 8px 30px rgba(0,113,227,.35);
  transition:box-shadow .4s ease,transform .2s ease;
}
.btn-primary.is-ready{animation:ctaGlow 2.6s ease-in-out infinite}
@keyframes ctaGlow{
  0%,100%{box-shadow:0 8px 30px rgba(0,113,227,.35)}
  50%{box-shadow:0 10px 42px rgba(0,113,227,.7),0 0 0 5px rgba(0,113,227,.14)}
}
.btn-ghost{
  background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);
  color:#fff;border-radius:999px;padding:14px 28px;font-size:15px;font-weight:600;
}
.hero-trust{display:flex;align-items:center;justify-content:center;gap:20px;font-size:12px;color:var(--muted);flex-wrap:wrap}

.hero-split{
  display:grid;grid-template-columns:1fr auto;gap:48px;align-items:center;
  text-align:left;max-width:1100px;
}
.hero-split .hero-sub{margin-left:0}
.hero-split .hero-actions,.hero-split .hero-trust{justify-content:flex-start}

.hero-visual{position:relative;width:min(380px,42vw);flex-shrink:0}
.hero-face-wrap{
  border-radius:28px;overflow:hidden;
  box-shadow:
    0 0 0 1px rgba(255,255,255,.14),
    0 0 48px rgba(41,151,255,.32),
    0 40px 90px rgba(0,0,0,.5);
  opacity:0;transform:translateY(12px);
  transition:opacity .9s ease,transform .9s ease;
}
.hero-visual.is-in .hero-face-wrap{opacity:1;transform:none}
.hero-face{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center 10%}
.hero-visual .phone-float{
  position:absolute;right:-18%;bottom:-8%;
  opacity:0;transform:translateY(36px);
  transition:opacity .7s ease,transform .7s cubic-bezier(.16,1,.3,1);
  animation:none;
}
.hero-visual.is-in .phone-float{opacity:1;transform:none}
.hero-visual.is-in .phone-float.is-settled{animation:float 6s ease-in-out infinite}
.hero-visual .phone-frame{width:214px}

.phone-float{display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 40px 60px rgba(0,113,227,.35))}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.phone-frame{
  width:214px;background:#1c1c1e;border-radius:40px;padding:8px;
  box-shadow:0 0 0 1px rgba(255,255,255,.14),0 0 0 8px rgba(255,255,255,.03),inset 0 0 0 1px rgba(0,0,0,.55);
}
.phone-notch{width:78px;height:22px;background:#1c1c1e;border-radius:14px;margin:7px auto 6px}
.phone-screen{background:#000;border-radius:32px;overflow:hidden;display:flex;flex-direction:column;aspect-ratio:9/19.4;height:auto}
.imsg-header{background:rgba(24,24,28,.96);padding:10px 14px 8px;display:flex;align-items:center;gap:10px;border-bottom:1px solid rgba(255,255,255,.07)}
.imsg-avatar{width:34px;height:34px;border-radius:50%;object-fit:cover;border:1.5px solid rgba(0,113,227,.7)}
.imsg-name{font-size:12px;font-weight:700;color:#fff;line-height:1.2}
.imsg-status{font-size:10px;color:var(--green);font-weight:500;display:flex;align-items:center;gap:6px}
.live-dot{
  width:7px;height:7px;border-radius:50%;background:var(--green);flex-shrink:0;
  box-shadow:0 0 0 0 rgba(25,164,99,.45);
  animation:heartbeat 2.2s ease-out infinite;
}
@keyframes heartbeat{
  0%{box-shadow:0 0 0 0 rgba(25,164,99,.42)}
  70%{box-shadow:0 0 0 7px rgba(25,164,99,0)}
  100%{box-shadow:0 0 0 0 rgba(25,164,99,0)}
}
.imsg-body{padding:10px 9px 14px;display:flex;flex-direction:column;gap:7px;flex:1;min-height:0}
.imsg-line{opacity:0;transform:translateY(10px);transition:opacity .45s ease,transform .45s ease}
.imsg-line.is-in{opacity:1;transform:none}
.imsg-bubble{max-width:80%;padding:8px 12px;border-radius:18px;font-size:11.5px;line-height:1.5}
.imsg-bubble.user{background:var(--blue);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.imsg-bubble.chris{background:#2c2c2e;color:#e5e5ea;align-self:flex-start;border-bottom-left-radius:4px}
.imsg-rx{align-self:flex-start;background:rgba(25,164,99,.15);border:1px solid rgba(25,164,99,.35);border-radius:12px;padding:7px 12px;font-size:11px;font-weight:600;color:#19a463}
.imsg-time{font-size:10px;color:#6e6e73;text-align:center}

.stats-band{background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:32px 24px}
.stats-inner{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.stat{text-align:center}
.stat-n{font-size:clamp(28px,4vw,48px);font-weight:900;letter-spacing:-0.06em;background:linear-gradient(120deg,#fff,var(--blue-bright));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;line-height:1;margin-bottom:6px}
.stat-l{font-size:13px;color:var(--muted);font-weight:500}

.reviews{background:var(--panel-2);padding:56px 0;overflow:hidden}
.reviews-head{text-align:center;padding:0 24px;margin-bottom:28px}
.reviews-head h2{font-size:clamp(22px,3vw,32px);font-weight:800;letter-spacing:-0.04em;margin-bottom:4px}
.reviews-head p{color:var(--muted);font-size:14px}
.stars-row{display:inline-flex;gap:3px;margin-bottom:6px}
.stars-row svg{width:18px;height:18px;fill:#f59e0b}
.scroll-mask{-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.scroll-track{display:flex;gap:16px;width:max-content;animation:scrollR 50s linear infinite}
.scroll-track:hover{animation-play-state:paused}
@keyframes scrollR{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.rcard{flex-shrink:0;width:300px;background:var(--panel-3);border:1px solid var(--line);border-radius:16px;padding:20px 22px}
.rcard-text{font-size:13px;color:var(--body);line-height:1.6;font-style:italic;margin-bottom:14px}
.rcard-foot{display:flex;justify-content:space-between;align-items:center}
.rcard-author{font-size:12px;font-weight:700;color:#fff}
.rcard-source{font-size:10px;font-weight:700;color:var(--blue-bright);background:rgba(41,151,255,.12);border-radius:999px;padding:3px 9px}

.section{padding:80px 24px}
.section-inner{max-width:var(--max);margin:0 auto}
.section-kicker{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--blue-bright);margin-bottom:12px}
.section-title{font-size:clamp(28px,4vw,48px);font-weight:800;letter-spacing:-0.05em;line-height:1.08;margin-bottom:16px}
.section-body{font-size:16px;color:var(--body);line-height:1.65;max-width:640px;margin-bottom:40px}
.center{text-align:center}
.center .section-body{margin-left:auto;margin-right:auto}
.alt-bg{background:var(--panel)}

.bento{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.bento-card{background:var(--panel-2);border:1px solid var(--line);border-radius:var(--radius);padding:28px 24px}
.step-num{width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;font-size:16px;font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.bento-card h3{font-size:18px;font-weight:800;letter-spacing:-0.03em;margin-bottom:10px}
.bento-card p{font-size:14px;color:var(--body);line-height:1.6}
.bento-card a{color:var(--blue-bright)}
.chris-avatar{width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid var(--blue);margin-bottom:12px}

.prob-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.prob{background:var(--panel-2);border:1px solid var(--line);border-radius:16px;padding:22px 18px}
.prob .x{width:28px;height:28px;border-radius:8px;background:rgba(229,72,77,.12);color:var(--red);display:grid;place-items:center;font-weight:800;margin-bottom:10px}
.prob h3{font-size:15px;font-weight:700;margin-bottom:6px}
.prob p{font-size:13px;color:var(--muted)}

.meet{display:grid;grid-template-columns:.8fr 1.2fr;gap:40px;align-items:center}
.meet img{width:100%;border-radius:24px;aspect-ratio:4/5;object-fit:cover;object-position:center top;box-shadow:0 30px 80px rgba(0,113,227,.2)}
.meet p{color:var(--body);font-size:16px;line-height:1.65;margin-bottom:14px;max-width:48ch}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.chip{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:8px 12px;border:1px solid var(--line);border-radius:999px;color:var(--body)}

.treat-grid,.states-pills{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.treat,.state-pill{
  padding:10px 16px;background:var(--panel-2);border:1px solid var(--line);
  border-radius:999px;font-size:14px;font-weight:500;color:var(--body);
}
.treat small{display:block;font-size:11px;color:var(--muted);font-weight:400}

.vs-section{padding:52px 24px;background:var(--panel);border-bottom:1px solid var(--line)}
.vs-inner{max-width:720px;margin:0 auto}
.vs-head{text-align:center;margin-bottom:26px}
.vs-head h2{font-size:clamp(24px,4vw,40px);font-weight:800;letter-spacing:-0.045em;margin-bottom:8px}
.vs-head p{color:var(--muted);font-size:14px}
.vs-grid{display:grid;grid-template-columns:1.1fr 1fr 1fr;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--panel-2)}
.vs-cell{padding:13px 14px;border-bottom:1px solid var(--line);font-size:14px;display:flex;align-items:center;line-height:1.35}
.vs-grid > .vs-cell:nth-last-child(-n+3){border-bottom:none}
.vs-corner{background:var(--panel-3)}
.vs-us-head,.vs-them-head{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;justify-content:center;text-align:center}
.vs-us-head{background:var(--blue);color:#fff}
.vs-them-head{background:var(--panel-3);color:var(--body)}
.vs-feature{font-weight:700;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:0.05em;background:var(--panel-3)}
.vs-us{background:rgba(0,113,227,.10);color:#fff;font-weight:700}
.vs-them{color:var(--muted)}
.vs-check{color:var(--green);margin-right:7px;font-weight:800}

.bottom-cta{background:linear-gradient(160deg,#0a1628 0%,#05060a 50%,#0d1a30 100%);border-top:1px solid var(--line);padding:80px 24px;text-align:center;position:relative;overflow:hidden}
.bottom-cta::before{content:'';position:absolute;top:-40%;left:50%;transform:translateX(-50%);width:600px;height:400px;background:radial-gradient(ellipse,rgba(0,113,227,.2),transparent 65%);filter:blur(40px);pointer-events:none}
.bottom-cta-inner{position:relative;z-index:1;max-width:600px;margin:0 auto}
.bottom-cta h2{font-size:clamp(32px,5vw,56px);font-weight:800;letter-spacing:-0.055em;margin-bottom:16px;background:linear-gradient(120deg,#fff,#a8d4ff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.bottom-cta p{font-size:16px;color:var(--body);margin-bottom:32px;line-height:1.6}
.bottom-trust-line{font-size:12px;color:var(--muted);margin-top:20px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap}

.er-note{font-size:13px;color:var(--muted);text-align:center;padding:20px 24px 100px;border-top:1px solid var(--line)}
.mobile-cta{
  display:none;position:fixed;left:12px;right:12px;bottom:12px;z-index:50;
  background:var(--blue);color:#fff!important;-webkit-text-fill-color:#fff!important;
  text-align:center;padding:16px;border-radius:100px;font-weight:700;
  box-shadow:0 12px 32px rgba(0,113,227,.4);
}
.section-light,.section-white{
  --panel:#ffffff;--panel-2:#f0f0f5;--panel-3:#e8e8ed;
  --ink:#111114;--body:#3d3d3f;--muted:#6e6e73;--line:rgba(0,0,0,0.09);
  color:#111114;
}
.section-light{background:#f5f5f7}
.section-white{background:#ffffff}
.section-light .section-kicker,.section-white .section-kicker{
  color:var(--blue);background:rgba(0,113,227,.1);border:1px solid rgba(0,113,227,.22);
  border-radius:999px;padding:4px 14px;
}
.section-light .bento-card,.section-white .bento-card{border-left:3px solid var(--blue)}
.section-light .step-num,.section-white .step-num{box-shadow:0 0 0 6px rgba(0,113,227,.12)}
.section-light .chip,.section-white .chip,
.section-light .treat,.section-white .treat,
.section-light .state-pill,.section-white .state-pill{
  background:#fff;border-color:rgba(0,0,0,.1);color:#3d3d3f;
}
.section-light .prob,.section-white .prob{background:#fff}
.dark-to-light{
  position:relative;z-index:2;
  clip-path:polygon(0 56px,100% 0,100% 100%,0 100%);
  margin-top:-56px;padding-top:calc(80px + 56px);
}

#npcSaveWrap{display:none!important}
body.npc-redesign .npc-nav{display:none!important}
#trustedsite-tm-image,[id^="trustedsite"],[id^="trustedbadge"],[class*="trustedsite"]{display:none!important}
html{background:#05060a!important}
body.npc-redesign{background:#05060a!important}
body.npc-redesign nav.nav{background:rgba(5,6,10,.88)!important;color:#fff!important;backdrop-filter:blur(18px)}
body.npc-redesign nav.nav.is-scrolled{background:rgba(5,6,10,.94)!important}
body.npc-redesign .nav-logo,body.npc-redesign .nav-logo span{color:#fff!important}
body.npc-redesign .nav-tag{color:rgba(255,255,255,.72)!important}
body::after{content:none!important;display:none!important}

@media(max-width:900px){
  .hero{min-height:auto;padding:36px 20px 130px}
  .hero h1{font-size:clamp(34px,10vw,46px)}
  .hero-sub{margin-bottom:20px}
  .hero-split{grid-template-columns:1fr;text-align:center}
  .hero-split .hero-sub{margin-inline:auto}
  .hero-split .hero-actions,.hero-split .hero-trust{justify-content:center}
  .hero-visual{width:min(280px,78vw);margin:20px auto 0}
  .hero-visual .phone-float{right:-12%;bottom:-6%}
  .hero-visual .phone-frame{width:152px}
  .dark-to-light{clip-path:polygon(0 32px,100% 0,100% 100%,0 100%);margin-top:-32px;padding-top:calc(56px + 32px)}
  .bento,.prob-grid,.meet,.stats-inner,.vs-grid{grid-template-columns:1fr}
  .vs-grid{grid-template-columns:1.1fr 1fr 1fr}
  .nav{padding:0 16px}
  .nav-tag{max-width:16ch}
  .mobile-cta{display:block}
}
@media(max-width:600px){
  .stats-inner{grid-template-columns:1fr 1fr}
  .prob-grid{grid-template-columns:1fr 1fr}
  .vs-cell{padding:11px 9px;font-size:12px}
  .section{padding:56px 20px}
}
@media(prefers-reduced-motion:reduce){
  .scroll-track,.phone-float,.pocket-word,.text-caret,.live-dot,.btn-primary.is-ready,.nav-cta::after{animation:none}
  .hero-face-wrap,.hero-visual .phone-float,.imsg-line{opacity:1;transform:none;transition:none}
}
</style>
</head>
<body class="npc-redesign">
<style>
body.npc-redesign .npc-nav, body.npc-redesign header.wp-block-template-part, body.npc-redesign .wp-site-blocks > header { display:none !important; }
body.npc-redesign .npc-site-footer { display:none !important; }
</style>
<a class="skip-link" href="#main">Skip to content</a>

<nav class="nav" aria-label="Primary">
  <a class="nav-logo" href="#">
    <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="" width="32" height="32">
    <span>NPCWoods<span class="nav-tag">Urgent care in your pocket</span></span>
  </a>
  <a class="nav-cta" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris · $59</a>
</nav>

<main id="main">

<section class="hero">
  <div class="hero-inner hero-split">
    <div>
      <div class="hero-kicker"><span class="hero-dot"></span> $59 flat · Real NP · 11 states</div>
      <h1>Urgent care in your <span class="pocket-word">pocket</span><span class="text-caret" aria-hidden="true"></span>.</h1>
      <p class="hero-sub">I'm Chris, a real Nurse Practitioner. Tell me what's going on and I'll get you sorted out. $59 flat. No waiting room. No app. Just a text.</p>
      <div class="hero-actions">
        <a class="btn-primary" id="hero-cta" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now</a>
        <a class="btn-ghost" href="#how">See how it works</a>
      </div>
      <div class="hero-trust">
        <span>MSN, APRN, FNP-C</span>
        <span>Double board-certified</span>
        <span>Pay after care</span>
      </div>
    </div>
    <div class="hero-visual" id="hero-visual">
      <div class="hero-face-wrap" id="hero-face-wrap">
      <img class="hero-face" src="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, MSN, APRN, FNP-C, Nurse Practitioner" width="500" height="625" fetchpriority="high">
      </div>
    <div class="phone-float" id="phone-float" aria-hidden="true">
      <div class="phone-frame">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <div class="imsg-header">
            <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="imsg-avatar" alt="">
            <div>
              <div class="imsg-name">Chris @ NPCWoods</div>
              <div class="imsg-status"><span class="live-dot" aria-hidden="true"></span> Available now</div>
            </div>
          </div>
          <div class="imsg-body">
            <div class="imsg-line imsg-time">Today 10:08 AM</div>
            <div class="imsg-line imsg-bubble user">Hey Chris, burning when I pee. Started this morning.</div>
            <div class="imsg-line imsg-bubble chris">I've got you. Any fever, back pain, or blood?</div>
            <div class="imsg-line imsg-bubble user">No fever. Just the burning.</div>
            <div class="imsg-line imsg-rx">✓ Plan sent. Pickup 10:52 AM</div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</section>

<div class="stats-band">
  <div class="stats-inner">
    <div class="stat"><div class="stat-n">$59</div><div class="stat-l">Flat fee, no surprises</div></div>
    <div class="stat"><div class="stat-n">11</div><div class="stat-l">Licensed states</div></div>
    <div class="stat"><div class="stat-n">Real NP</div><div class="stat-l">Chris reads every text</div></div>
    <div class="stat"><div class="stat-n">After</div><div class="stat-l">Pay after you're treated</div></div>
  </div>
</div>

<section class="reviews" aria-labelledby="rev-h">
  <div class="reviews-head">
    <div class="stars-row" aria-hidden="true">
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
    </div>
    <h2 id="rev-h">Real texts. Real relief.</h2>
    <p>Same people. Same quotes. Now they show up first.</p>
  </div>
  <div class="scroll-mask">
    <div class="scroll-track">
      <div class="rcard"><p class="rcard-text">"Very fast and convenient. I first messaged Chris at 10:08am and I was picking up my prescriptions from the pharmacy at 10:52am same day! Cannot recommend enough!"</p><div class="rcard-foot"><span class="rcard-author">A. H.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"Chris texted me back within seconds and had my prescription over to the pharmacy within minutes. So simple and easy. Definitely beats sitting in a waiting room."</p><div class="rcard-foot"><span class="rcard-author">J. R.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"I texted Chris out of nowhere on a Sunday and he answered straight away, saw me in under an hour!"</p><div class="rcard-foot"><span class="rcard-author">B. P.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"My grandmother couldn't get a response from her primary care provider. I texted Chris at 10pm and he responded within 15 minutes."</p><div class="rcard-foot"><span class="rcard-author">M. D.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"What a wonderful service to the community. Fast response time, no sitting in the waiting room."</p><div class="rcard-foot"><span class="rcard-author">J. D. Q.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"Messaged Chris, he responded in a timely manner. Very professional. It was nice to stay home and get quality care."</p><div class="rcard-foot"><span class="rcard-author">T. P.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"Very fast and convenient. I first messaged Chris at 10:08am and I was picking up my prescriptions from the pharmacy at 10:52am same day! Cannot recommend enough!"</p><div class="rcard-foot"><span class="rcard-author">A. H.</span><span class="rcard-source">Facebook</span></div></div>
      <div class="rcard"><p class="rcard-text">"Chris texted me back within seconds and had my prescription over to the pharmacy within minutes. So simple and easy. Definitely beats sitting in a waiting room."</p><div class="rcard-foot"><span class="rcard-author">J. R.</span><span class="rcard-source">Facebook</span></div></div>
    </div>
  </div>
</section>

<section id="how" class="section section-light dark-to-light">
  <div class="section-inner">
    <span class="section-kicker">The visit in your pocket</span>
    <h2 class="section-title">Three texts. That's it.</h2>
    <p class="section-body">Most visits wrap up in under an hour, from your first text to your prescription. No 30-question form. No portal. No app.</p>
    <div class="bento">
      <article class="bento-card">
        <div class="step-num">1</div>
        <h3>Text me your symptoms</h3>
        <p>In your own words. No 30-question form, no portal login, no app to download.</p>
      </article>
      <article class="bento-card">
        <div class="step-num">2</div>
        <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" class="chris-avatar" alt="Chris Woods, NP">
        <h3>I actually read it</h3>
        <p>I look at your history, ask what I need to, and build a plan for you. Not a template. Not a bot.</p>
      </article>
      <article class="bento-card">
        <div class="step-num">3</div>
        <h3>Pick up and feel better</h3>
        <p>I send your prescription to your pharmacy and a written plan to your inbox. That is it.</p>
      </article>
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:20px;text-align:center">Text-based telehealth is not for emergencies. If you have chest pain, trouble breathing, or other emergency symptoms, call 911.</p>
  </div>
</section>

<section class="section alt-bg">
  <div class="section-inner">
    <span class="section-kicker">The old way</span>
    <h2 class="section-title">Getting better shouldn't be this hard.</h2>
    <p class="section-body">You feel awful, and the system makes you work for it.</p>
    <div class="prob-grid">
      <div class="prob"><span class="x">&times;</span><h3>3-hour waits</h3><p>A half-day in an urgent care lobby for a 10-minute problem.</p></div>
      <div class="prob"><span class="x">&times;</span><h3>$200 for a $20 fix</h3><p>Surprise bills for simple care you already knew you needed.</p></div>
      <div class="prob"><span class="x">&times;</span><h3>No clinic close by</h3><p>The nearest option is far, closed, or booked out for days.</p></div>
      <div class="prob"><span class="x">&times;</span><h3>Forms &amp; denials</h3><p>Portals, paperwork, and confusing fine print after the fact.</p></div>
    </div>
    <p class="section-body" style="margin:28px 0 0;max-width:none">I built NPCWoods so you'd have urgent care in your pocket.</p>
  </div>
</section>

<section class="section section-white" id="chris">
  <div class="section-inner meet">
    <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, MSN, APRN, FNP-C, Nurse Practitioner">
    <div>
      <span class="section-kicker">Meet your NP</span>
      <h2 class="section-title">Hey, I'm Chris.</h2>
      <p>I spent years watching people lose a whole day and a couple hundred bucks over something I could sort out in ten minutes. That never sat right with me.</p>
      <p>So I built the practice I would want for my own family: urgent care in your pocket. Text a real Nurse Practitioner, get actually listened to, and pay one honest price.</p>
      <p>No runaround. No surprise bills. No pretending a chatbot is care. Faith and family keep me grounded, and they are why I treat every visit like it is someone I love.</p>
      <div class="chips">
        <span class="chip">MSN, APRN, FNP-C</span>
        <span class="chip">Double board-certified</span>
        <span class="chip">NPI 1285125468</span>
        <span class="chip">Real clinician review</span>
      </div>
    </div>
  </div>
</section>

<section class="vs-section" aria-label="NPCWoods compared to big telehealth">
  <div class="vs-inner">
    <div class="vs-head">
      <span class="section-kicker">The honest comparison</span>
      <h2>NPCWoods vs. big telehealth</h2>
      <p>A real NP in your messages. None of the games.</p>
    </div>
    <div class="vs-grid">
      <div class="vs-cell vs-corner"></div>
      <div class="vs-cell vs-us-head">NPCWoods</div>
      <div class="vs-cell vs-them-head">Big telehealth</div>
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
    </div>
  </div>
</section>

<section class="section section-light dark-to-light center">
  <div class="section-inner">
    <span class="section-kicker">One price. One promise.</span>
    <h2 class="section-title">That's the whole thing. $59.</h2>
    <p class="section-body">Pay after you're treated. And if I can't safely help you by text, I'll tell you straight up, and you don't pay a dime.</p>
    <div class="chips" style="justify-content:center">
      <span class="chip">Flat fee</span><span class="chip">No hidden fees</span><span class="chip">Pay after treated</span><span class="chip">HSA / FSA receipt on request</span>
    </div>
  </div>
</section>

<section class="section section-white center">
  <div class="section-inner">
    <span class="section-kicker">What I treat by text</span>
    <h2 class="section-title">Common $59 visits.</h2>
    <p class="section-body">If it is safe to handle by text, I will. If it is not, I will say so and you do not pay.</p>
    <div class="treat-grid">
      <span class="treat">UTI</span>
      <span class="treat">Sinus infection</span>
      <span class="treat">Strep throat</span>
      <span class="treat">Ear infection</span>
      <span class="treat">Pink eye</span>
      <span class="treat">Bronchitis / cough</span>
      <span class="treat">Skin infection</span>
      <span class="treat">Tooth infection <small>bridge only, dentist still required</small></span>
      <span class="treat">Stomach bug</span>
      <span class="treat">Cold sores</span>
      <span class="treat">COVID / flu</span>
      <span class="treat">Allergies</span>
      <span class="treat">Acid reflux</span>
      <span class="treat">Acne</span>
      <span class="treat">Yeast infection</span>
      <span class="treat">Ingrown toenail</span>
      <span class="treat">Poison ivy</span>
      <span class="treat">ED</span>
      <span class="treat">Medication refills</span>
      <span class="treat">GLP-1 consult <small>fit and safety, drug cost separate</small></span>
    </div>
  </div>
</section>

<section class="section section-light center">
  <div class="section-inner">
    <span class="section-kicker">Where I can help</span>
    <h2 class="section-title">Licensed in 11 states.</h2>
    <p class="section-body">You have to be physically in one of these states at the time of the visit.</p>
    <div class="states-pills">
      <span class="state-pill">Arizona</span><span class="state-pill">Colorado</span><span class="state-pill">Georgia</span><span class="state-pill">Idaho</span><span class="state-pill">Iowa</span><span class="state-pill">Montana</span><span class="state-pill">Nevada</span><span class="state-pill">New Mexico</span><span class="state-pill">North Carolina</span><span class="state-pill">Oregon</span><span class="state-pill">Utah</span>
    </div>
  </div>
</section>

<section class="bottom-cta">
  <div class="bottom-cta-inner">
    <h2>Text me. It's already in your hand!</h2>
    <p>$59 flat. A real Nurse Practitioner. No waiting room. No app.</p>
    <a class="btn-primary" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" style="font-size:16px;padding:16px 32px">Text Chris now</a>
    <div class="bottom-trust-line">
      <span>HIPAA-compliant</span>
      <span>HSA / FSA receipt on request</span>
      <span>Pay after care</span>
    </div>
  </div>
</section>

<p class="er-note">$59 text-based urgent care with Chris Woods, MSN, APRN, FNP-C. Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, and UT.<br>Text-based telehealth is not for emergencies. If you have chest pain, trouble breathing, or other emergency symptoms, call 911.</p>
</main>

<a class="mobile-cta" href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">Text Chris now · $59</a>
<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nav = document.querySelector('.nav');
  var visual = document.getElementById('hero-visual');
  var faceWrap = document.getElementById('hero-face-wrap');
  var phone = document.getElementById('phone-float');
  var cta = document.getElementById('hero-cta');
  var lines = document.querySelectorAll('.imsg-line');

  function onScroll() {
    if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 40);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  function showAll() {
    if (visual) visual.classList.add('is-in');
    if (phone) phone.classList.add('is-settled');
    lines.forEach(function (el) { el.classList.add('is-in'); });
    if (cta) cta.classList.add('is-ready');
  }

  if (reduce) {
    showAll();
    return;
  }

  if (visual) visual.classList.add('is-in');
  window.setTimeout(function () {
    if (phone) phone.classList.add('is-settled');
  }, 720);

  var times = [520, 1280, 2100, 2920, 3600];
  lines.forEach(function (el, i) {
    window.setTimeout(function () { el.classList.add('is-in'); }, times[i] || 400);
  });
  window.setTimeout(function () {
    if (cta) cta.classList.add('is-ready');
  }, 4100);

  var hero = document.querySelector('.hero');
  if (!hero || !visual) return;
  var mx = 0, my = 0, sx = 0, sy = 0;
  function paint() {
    visual.style.transform = 'translate(' + (mx * -8 + sx) + 'px,' + (my * -6 + sy) + 'px)';
  }
  hero.addEventListener('mousemove', function (e) {
    var r = hero.getBoundingClientRect();
    mx = (e.clientX - r.left) / r.width - 0.5;
    my = (e.clientY - r.top) / r.height - 0.5;
    paint();
  });
  window.addEventListener('scroll', function () {
    var y = Math.min(1, Math.max(0, window.scrollY / 420));
    sy = y * -16;
    sx = y * -5;
    paint();
  }, { passive: true });
})();
</script>
<?php if (function_exists('wp_footer')) { wp_footer(); } ?>
</body>
</html>
