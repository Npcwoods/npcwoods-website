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
<meta name="description" content="NPCWoods Telemedicine, $59 text-based urgent care from a licensed Nurse Practitioner. No hassle, no waiting rooms. Same-day response. Text (480) 639-4722.">
<meta name="theme-color" content="#2563EB">
<title>NPCWoods Telemedicine: $59 Online Urgent Care | No Hassle</title>
<link rel="canonical" href="https://npcwoods.com/">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://npcwoods.com/">
<meta property="og:title" content="NPCWoods Telemedicine – $59 Online Urgent Care">
<meta property="og:description" content="See a real Nurse Practitioner from home. $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.">
<meta property="og:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<meta property="og:site_name" content="NPCWoods Telemedicine">
<meta property="og:locale" content="en_US">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="NPCWoods Telemedicine – $59 Online Urgent Care">
<meta name="twitter:description" content="See a real Nurse Practitioner from home. $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.">
<meta name="twitter:image" content="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp">
<link rel="icon" type="image/jpeg" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="apple-touch-icon" href="https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://npcwoods.com">
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"></noscript>
<style>
/* ========================================
   CSS CUSTOM PROPERTIES
   ======================================== */
:root {
  --white: #FFFFFF;
  --off-white: #F7F8FA;
  --warm-white: #FDF8F4;
  --text-primary: #1A1A2E;
  --text-body: #4A4A5A;
  --text-muted: #8E8E9A;
  --brand: #2563EB;
  --brand-light: #EFF6FF;
  --brand-hover: #1D4ED8;
  --brand-soft: #DBEAFE;
  --border: #E5E7EB;
  --border-hover: #D1D5DB;
  --shadow: rgba(0,0,0,0.04);
  --shadow-hover: rgba(0,0,0,0.08);
  --success: #16A34A;
  --success-light: #DCFCE7;
  --gold: #F59E0B;
  --section-pad: 100px;
  --section-pad-mobile: 64px;
  --container-max: 1200px;
  --side-pad: 48px;
  --side-pad-mobile: 20px;
  --nav-height: 72px;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 2rem;
  --text-4xl: 2.5rem;
  --text-5xl: clamp(2.2rem, 6vw, 4rem);
}

/* ========================================
   RESET & BASE
   ======================================== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  scroll-behavior: smooth;
  scroll-padding-top: calc(var(--nav-height) + 16px);
  font-size: 16px;
}

body {
  background: var(--white);
  color: var(--text-body);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 400;
  line-height: 1.7;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

img { max-width: 100%; display: block; }
a { text-decoration: none; color: inherit; }

/* Focus Styles */
:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
  border-radius: 4px;
}
:focus:not(:focus-visible) { outline: none; }

/* Skip Link */
.skip-link {
  position: absolute;
  top: -100px;
  left: 16px;
  background: var(--brand);
  color: var(--white);
  padding: 12px 24px;
  border-radius: 0 0 8px 8px;
  font-weight: 600;
  z-index: 200;
  transition: top 0.2s;
}
.skip-link:focus { top: 0; }

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--off-white); }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #9CA3AF; }

/* ========================================
   SVG ICON SYSTEM (hidden sprite)
   ======================================== */

/* ========================================
   LAYOUT
   ======================================== */

section {
  padding: var(--section-pad) var(--side-pad);
}

/* ========================================
   TYPOGRAPHY
   ======================================== */
h1, h2, h3 {
  font-family: 'Inter', sans-serif;
  color: var(--text-primary);
  line-height: 1.15;
  letter-spacing: -0.02em;
}

h1 {
  font-size: var(--text-5xl);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.05;
}

h2 {
  font-size: clamp(1.75rem, 4vw, var(--text-4xl));
  font-weight: 700;
}

h3 {
  font-size: var(--text-xl);
  font-weight: 600;
}




/* ========================================
   BUTTONS
   ======================================== */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--brand);
  color: var(--white);
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: var(--text-base);
  padding: 16px 32px;
  border-radius: 100px;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
.btn-primary:hover {
  background: var(--brand-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(37,99,235,0.3);
}





/* ========================================
   BADGE
   ======================================== */

/* ========================================
   CARD
   ======================================== */

/* ========================================
   SCROLL REVEAL
   ======================================== */

/* Stagger children */

/* ========================================
   NAV (New slide-out panel)
   ======================================== */
/* ===== SITE NAV ===== */
.npc-nav {
  position: sticky;
  top: 0;
  z-index: 9999;
  background: #FFFFFF;
  border-bottom: 1px solid #E5E7EB;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.npc-nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}

.npc-nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #1A1A2E;
  font-weight: 700;
  font-size: 1rem;
}

.npc-nav-logo img {
  width: 32px;
  height: 32px;
  border-radius: 8px;
}

.npc-nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.npc-nav-links > li {
  position: relative;
}

.npc-nav-links > li > a {
  display: block;
  padding: 8px 14px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4A4A5A;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.15s, color 0.15s;
}

.npc-nav-links > li > a:hover {
  background: #EFF6FF;
  color: #2563EB;
}

/* Dropdown trigger arrow */
.npc-nav-links > li > a .nav-arrow {
  display: inline-block;
  margin-left: 4px;
  font-size: 0.65rem;
  transition: transform 0.2s;
}

/* Dropdown panel */
.npc-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 220px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  padding: 8px;
  margin-top: 4px;
  z-index: 10000;
}

.npc-nav-links > li:hover > .npc-dropdown,
.npc-nav-links > li:focus-within > .npc-dropdown {
  display: block;
}

.npc-dropdown a {
  display: block;
  padding: 8px 14px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #4A4A5A;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.15s;
}

.npc-dropdown a:hover {
  background: #EFF6FF;
  color: #2563EB;
}

/* CTA button in nav */
.npc-nav-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #2563EB;
  color: #FFFFFF !important;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 8px 18px;
  border-radius: 100px;
  text-decoration: none;
  transition: background 0.15s;
  white-space: nowrap;
}

.npc-nav-cta:hover {
  background: #1D4ED8;
  color: #FFFFFF !important;
}

/* Mobile hamburger button */
.npc-nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  cursor: pointer;
  padding: 10px;
  z-index: 10002;
  transition: all 0.2s;
}

.npc-nav-toggle:hover {
  background: #F7F8FA;
  border-color: #D1D5DB;
}

.npc-nav-toggle span {
  display: block;
  width: 18px;
  height: 2px;
  background: #1A1A2E;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center;
}

.npc-nav-toggle.active {
  border-color: #2563EB;
  background: #EFF6FF;
}

.npc-nav-toggle.active span { background: #2563EB; }
.npc-nav-toggle.active span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.npc-nav-toggle.active span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.npc-nav-toggle.active span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* ===== SLIDE-OUT PANEL ===== */
.npc-menu-overlay {
  position: fixed;
  inset: 0;
  background: rgba(26,26,46,0.3);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 9999;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s ease;
}

.npc-menu-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.npc-slide-panel {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  max-width: 92vw;
  height: 100vh;
  height: 100dvh;
  background: #FFFFFF;
  z-index: 10001;
  transition: right 0.4s cubic-bezier(0.32, 0.72, 0, 1);
  overflow-y: auto;
  overscroll-behavior: contain;
  box-shadow: -12px 0 40px rgba(0,0,0,0.08);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.npc-slide-panel.active {
  right: 0;
}

/* Panel header */
.npc-panel-header {
  position: sticky;
  top: 0;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 28px;
  border-bottom: 1px solid #E5E7EB;
  z-index: 2;
}

.npc-panel-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 1rem;
  color: #1A1A2E;
}

.npc-panel-logo img {
  height: 32px;
  width: 32px;
  border-radius: 8px;
}

.npc-panel-close {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8E8E9A;
  transition: all 0.2s;
}

.npc-panel-close:hover {
  background: #F7F8FA;
  border-color: #D1D5DB;
  color: #1A1A2E;
}

.npc-panel-close svg {
  width: 16px;
  height: 16px;
}

.npc-panel-body {
  padding: 8px 20px 120px;
}

/* Panel sections */
.npc-panel-section {
  margin-bottom: 8px;
}

.npc-panel-section-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #8E8E9A;
  padding: 16px 12px 8px;
}

/* Panel nav links */
.npc-panel-link {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border-radius: 12px;
  text-decoration: none;
  color: #1A1A2E;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.15s ease;
}

.npc-panel-link:hover {
  background: #EFF6FF;
}

.npc-panel-link-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #F7F8FA;
  border: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}

.npc-panel-link:hover .npc-panel-link-icon {
  background: #EFF6FF;
  border-color: #DBEAFE;
}

.npc-panel-link-icon svg {
  width: 18px;
  height: 18px;
  color: #2563EB;
}

.npc-panel-link-text {
  flex: 1;
}

.npc-panel-link-sub {
  font-size: 0.75rem;
  color: #8E8E9A;
  font-weight: 400;
  margin-top: 1px;
}

.npc-panel-link:hover .npc-panel-link-sub {
  color: #2563EB;
  opacity: 0.7;
}

.npc-panel-link-arrow {
  color: #D1D5DB;
  opacity: 0;
  transform: translateX(-4px);
  transition: all 0.2s;
}

.npc-panel-link:hover .npc-panel-link-arrow {
  opacity: 1;
  transform: translateX(0);
  color: #2563EB;
}

/* States grid */
.npc-states-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2px;
  padding: 0 4px;
}

.npc-state-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  text-decoration: none;
  color: #1A1A2E;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.15s ease;
}

.npc-state-link:hover {
  background: #EFF6FF;
  color: #2563EB;
}

.npc-state-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #16A34A;
  flex-shrink: 0;
  box-shadow: 0 0 0 2px #DCFCE7;
}

.npc-state-link:hover .npc-state-dot {
  background: #2563EB;
  box-shadow: 0 0 0 2px #DBEAFE;
}

/* Panel divider */
.npc-panel-divider {
  height: 1px;
  background: #E5E7EB;
  margin: 8px 12px 4px;
}

/* Panel CTA */
.npc-panel-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 15px;
  background: #2563EB;
  color: #FFFFFF;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 14px;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(37,99,235,0.3);
  margin: 4px 0;
}

.npc-panel-cta:hover {
  background: #1D4ED8;
  color: #FFFFFF;
  box-shadow: 0 6px 24px rgba(37,99,235,0.4);
  transform: translateY(-1px);
}

.npc-panel-cta svg {
  width: 20px;
  height: 20px;
}

/* Panel phone link */
.npc-panel-phone {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border-radius: 12px;
  text-decoration: none;
  color: #1A1A2E;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.15s;
  margin-top: 4px;
}

.npc-panel-phone:hover {
  background: #F7F8FA;
}

.npc-panel-phone-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #DCFCE7;
  border: 1px solid rgba(22,163,74,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.npc-panel-phone-icon svg {
  width: 18px;
  height: 18px;
  color: #16A34A;
}

/* Panel animations */
.npc-slide-panel.active .npc-panel-link,
.npc-slide-panel.active .npc-state-link,
.npc-slide-panel.active .npc-panel-cta,
.npc-slide-panel.active .npc-panel-phone {
  animation: npcFadeSlideIn 0.35s ease forwards;
  opacity: 0;
}

.npc-slide-panel.active .npc-panel-section:nth-child(1) .npc-panel-link:nth-child(2) { animation-delay: 0.06s; }
.npc-slide-panel.active .npc-panel-section:nth-child(1) .npc-panel-link:nth-child(3) { animation-delay: 0.09s; }
.npc-slide-panel.active .npc-panel-section:nth-child(1) .npc-panel-link:nth-child(4) { animation-delay: 0.12s; }
.npc-slide-panel.active .npc-panel-section:nth-child(1) .npc-panel-link:nth-child(5) { animation-delay: 0.15s; }
.npc-slide-panel.active .npc-panel-section:nth-child(1) .npc-panel-link:nth-child(6) { animation-delay: 0.18s; }

@keyframes npcFadeSlideIn {
  from { opacity: 0; transform: translateX(12px); }
  to { opacity: 1; transform: translateX(0); }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .npc-slide-panel,
  .npc-menu-overlay,
  .npc-nav-toggle span,
  .npc-panel-link,
  .npc-state-link,
  .npc-panel-cta,
  .npc-panel-phone {
    transition-duration: 0.1s !important;
    animation-duration: 0.01ms !important;
  }
}

@media (max-width: 768px) {
  .npc-nav-links { display: none; }
  .npc-nav-toggle { display: flex; }
}


/* Homepage-specific: nav transparent over hero, solid when scrolled */

/* ========================================
   HERO (Hims-style immersive)
   ======================================== */

/* SVG trend line behind photo */

/* Hero photo — large, bottom-anchored, centered */

/* Organized pill badges row under subtitle */

/* Text overlay on the gradient */

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.7); }
}



/* CTA buttons at bottom of viewport, over gradient */


/* ========================================
   SOCIAL PROOF BAR
   ======================================== */

/* ========================================
   PAIN POINTS
   ======================================== */







/* ========================================
   BEFORE / AFTER
   ======================================== */














/* Connector line between steps */



/* VS divider */

/* ========================================
   HOW IT WORKS
   ======================================== */







/* ========================================
   PRICING
   ======================================== */











/* ========================================
   CONDITIONS
   ======================================== */






/* ========================================
   ABOUT
   ======================================== */










/* ========================================
   SCROLLING REVIEWS BANNER
   ======================================== */
@keyframes scrollReviews{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
@media(max-width:768px){.reviews-banner{padding:36px 0 28px}.review-card{width:280px;padding:20px 22px}.reviews-banner-stars svg{width:20px;height:20px}}

/* ========================================
   TESTIMONIALS
   ======================================== */







/* ========================================
   FAQ
   ======================================== */








/* ========================================
   CTA SECTION
   ======================================== */





/* ========================================
   FOOTER
   ======================================== */
.site-footer {
  background: var(--text-primary);
  padding: 60px var(--side-pad) 40px;
}

.footer-grid {
  max-width: var(--container-max);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.footer-brand .nav-logo {
  color: var(--white);
  font-size: 1.2rem;
  display: block;
  margin-bottom: 12px;
}

.footer-brand p {
  font-size: var(--text-sm);
  color: rgba(255,255,255,0.5);
  line-height: 1.6;
}

.footer-links h4 {
  color: var(--white);
  font-size: var(--text-sm);
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: 0.03em;
}

.footer-links ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-links a {
  font-size: var(--text-sm);
  color: rgba(255,255,255,0.5);
  transition: color 0.2s;
}
.footer-links a:hover { color: var(--white); }

.footer-contact h4 {
  color: var(--white);
  font-size: var(--text-sm);
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: 0.03em;
}

.footer-contact p,
.footer-contact a {
  font-size: var(--text-sm);
  color: rgba(255,255,255,0.5);
  line-height: 1.8;
}
.footer-contact a:hover { color: var(--white); }
.footer-site { margin-top: 8px; }
.footer-logo-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid rgba(255,255,255,0.2); }

.footer-bottom {
  max-width: var(--container-max);
  margin: 0 auto;
  padding-top: 32px;
  border-top: 1px solid rgba(255,255,255,0.08);
  text-align: center;
}
.footer-bottom p {
  font-size: var(--text-xs);
  color: rgba(255,255,255,0.35);
  line-height: 1.6;
}

/* ========================================
   STICKY MOBILE CTA
   ======================================== */
.mobile-sticky-cta {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 90;
  padding: 12px 20px;
  background: var(--white);
  border-top: 1px solid var(--border);
  box-shadow: 0 -2px 10px rgba(0,0,0,0.06);
}
.mobile-sticky-cta .btn-primary {
  width: 100%;
  justify-content: center;
  padding: 14px 24px;
}

/* ========================================
   RESPONSIVE
   ======================================== */

/* Tablet */
@media (max-width: 1024px) {
  /* Old nav rules removed — new nav handles its own responsive */






  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

/* Mobile */
@media (max-width: 640px) {
  :root {
    --side-pad: 20px;
    --section-pad: 64px;
  }

  :root { --nav-height: 60px; }









  /* Show sticky mobile CTA */
  .mobile-sticky-cta { display: block; }

  /* Add bottom padding to body so footer isn't hidden behind sticky CTA */
  .site-footer { padding-bottom: 80px; }
}
</style>
<!-- NPCWoods Homepage Schema: MedicalBusiness + Person + Service -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://npcwoods.com/#medical-business",
      "name": "NPCWoods Telemedicine",
      "url": "https://npcwoods.com",
      "description": "Text-based asynchronous telemedicine from a double board-certified Nurse Practitioner. $59 flat fee per visit, no paperwork, no hidden fees. Same-day prescriptions for UTIs, sinus infections, strep throat, dental pain, ED, and 18+ conditions across 11 states.",
      "priceRange": "$59",
      "telephone": "+14806394722",
      "email": "cwoods@npcwoods.com",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "logo": "https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg",
      "medicalSpecialty": "FamilyPractice",
      "currenciesAccepted": "USD",
      "paymentAccepted": "Cash, Credit Card, Debit Card",
      "isAcceptingNewPatients": true,
      "founder": { "@id": "https://npcwoods.com/#chris-woods" },
      "employee": { "@id": "https://npcwoods.com/#chris-woods" },
      "areaServed": [
        { "@type": "State", "name": "Arizona" },
        { "@type": "State", "name": "Colorado" },
        { "@type": "State", "name": "Georgia" },
        { "@type": "State", "name": "Idaho" },
        { "@type": "State", "name": "Iowa" },
        { "@type": "State", "name": "Montana" },
        { "@type": "State", "name": "Nevada" },
        { "@type": "State", "name": "New Mexico" },
        { "@type": "State", "name": "North Carolina" },
        { "@type": "State", "name": "Oregon" },
        { "@type": "State", "name": "Utah" }
      ],
      "availableService": { "@id": "https://npcwoods.com/#telehealth-service" },
      "sameAs": [
        "https://www.facebook.com/npcwoods",
        "https://www.legitscript.com/websites/?checker_keywords=npcwoods.com",
        "https://share.google/XlmNvRT4vihOJ8KBH"
      ],
      "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "LegitScript Certified"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "53",
        "bestRating": "5"
      }
    },
    {
      "@type": "Person",
      "@id": "https://npcwoods.com/#chris-woods",
      "name": "Chris Woods",
      "givenName": "Chris",
      "familyName": "Woods",
      "jobTitle": "Licensed Nurse Practitioner",
      "description": "Chris Woods is a double board-certified Nurse Practitioner and the founder of NPCWoods Telemedicine. He personally reviews every patient case. No AI, no chatbot, no algorithm.",
      "url": "https://npcwoods.com/about/",
      "image": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp",
      "worksFor": { "@id": "https://npcwoods.com/#medical-business" },
      "hasCredential": [
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Master of Science in Nursing (MSN)"
        },
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Family Nurse Practitioner - Board Certified (FNP-C)"
        },
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Advanced Practice Registered Nurse (APRN)"
        }
      ],
      "knowsAbout": [
        "Urinary Tract Infections", "Sinus Infections", "Strep Throat",
        "Dental Pain", "Ear Infections", "Bronchitis", "Pink Eye",
        "Erectile Dysfunction", "Skin Infections", "Cold Sores",
        "Asynchronous Telemedicine", "Text-Based Healthcare"
      ]
    },
    {
      "@type": "MedicalService",
      "@id": "https://npcwoods.com/#telehealth-service",
      "name": "Asynchronous Text-Based Telemedicine Visit",
      "serviceType": "Telehealth Visit",
      "description": "Text-based urgent care visit with a double board-certified Nurse Practitioner. No video call required. Text your symptoms, get a diagnosis and prescription sent to your pharmacy, usually same day.",
      "provider": { "@id": "https://npcwoods.com/#chris-woods" },
      "areaServed": [
        { "@type": "State", "name": "Arizona" },
        { "@type": "State", "name": "Colorado" },
        { "@type": "State", "name": "Georgia" },
        { "@type": "State", "name": "Idaho" },
        { "@type": "State", "name": "Iowa" },
        { "@type": "State", "name": "Montana" },
        { "@type": "State", "name": "Nevada" },
        { "@type": "State", "name": "New Mexico" },
        { "@type": "State", "name": "North Carolina" },
        { "@type": "State", "name": "Oregon" },
        { "@type": "State", "name": "Utah" }
      ],
      "offers": {
        "@type": "Offer",
        "price": "59",
        "priceCurrency": "USD",
        "priceValidUntil": "2027-01-01",
        "availability": "https://schema.org/InStock",
        "url": "https://npcwoods.com/"
      },
      "termsOfService": "https://npcwoods.com/terms-of-service/",
      "availableChannel": {
        "@type": "ServiceChannel",
        "serviceUrl": "https://npcwoods.com/",
        "servicePhone": {
          "@type": "ContactPoint",
          "telephone": "+14806394722",
          "contactType": "patient care",
          "availableLanguage": "English"
        },
        "serviceSmsNumber": {
          "@type": "ContactPoint",
          "telephone": "+14806394722",
          "contactType": "patient care"
        }
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://npcwoods.com/#website",
      "name": "NPCWoods Telemedicine",
      "url": "https://npcwoods.com",
      "publisher": { "@id": "https://npcwoods.com/#medical-business" }
    },
    {
      "@type": "WebPage",
      "@id": "https://npcwoods.com/",
      "name": "NPCWoods Telemedicine: $59 Online Urgent Care",
      "description": "Text-based telemedicine from a double board-certified Nurse Practitioner. $59 flat fee. No paperwork, no hidden fees. Same-day prescriptions across 11 states.",
      "url": "https://npcwoods.com/",
      "isPartOf": { "@id": "https://npcwoods.com/#website" },
      "about": { "@id": "https://npcwoods.com/#medical-business" },
      "primaryImageOfPage": {
        "@type": "ImageObject",
        "url": "https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp"
      }
    }
  ]
}
</script>
<!-- NPCWoods Tracking: Ahrefs Analytics -->
<script src="https://analytics.ahrefs.com/analytics.js" data-key="1qFceGSHKP6yg4JlSdNJ4Q" async></script>
</head>
<body>
<!-- NPCWoods Tracking: GTM noscript -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-59QSWZRC"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<!-- ===== Core Web Vitals field reporter (sends LCP/CLS/INP/FCP/TTFB to GA4 via dataLayer) ===== -->
<script>
(function() {
  if (window.__npcCwvLoaded) return;
  window.__npcCwvLoaded = true;
  window.dataLayer = window.dataLayer || [];
  function report(metric) {
    try {
      window.dataLayer.push({
        event: 'web_vitals',
        metric_name: metric.name,
        metric_value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
        metric_rating: metric.rating,
        metric_id: metric.id,
        page_path: location.pathname
      });
    } catch (e) {}
  }
  function load() {
    var s = document.createElement('script');
    s.src = 'https://unpkg.com/web-vitals@4/dist/web-vitals.attribution.iife.js';
    s.async = true;
    s.onload = function() {
      if (!window.webVitals) return;
      window.webVitals.onLCP(report);
      window.webVitals.onCLS(report);
      window.webVitals.onINP(report);
      window.webVitals.onFCP(report);
      window.webVitals.onTTFB(report);
    };
    document.head.appendChild(s);
  }
  if ('requestIdleCallback' in window) {
    requestIdleCallback(load, { timeout: 3000 });
  } else {
    setTimeout(load, 2000);
  }
})();
</script>

<!-- Hidden SVG Sprite -->
<svg style="display:none" xmlns="http://www.w3.org/2000/svg">
  <symbol id="icon-check" viewBox="0 0 24 24">
    <path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-check-circle" viewBox="0 0 24 24">
    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" fill="currentColor"/>
  </symbol>
  <symbol id="icon-x" viewBox="0 0 24 24">
    <path d="M18 6L6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-phone" viewBox="0 0 24 24">
    <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.8 19.79 19.79 0 01.22 1.21 2 2 0 012.22 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 7.91a16 16 0 006.18 6.18l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-arrow-right" viewBox="0 0 24 24">
    <path d="M5 12h14M12 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-chevron-down" viewBox="0 0 24 24">
    <path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-star" viewBox="0 0 24 24">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="currentColor"/>
  </symbol>
  <!-- Condition icons -->
  <symbol id="icon-pill" viewBox="0 0 24 24">
    <path d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-droplet" viewBox="0 0 24 24">
    <path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-thermometer" viewBox="0 0 24 24">
    <path d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-ear" viewBox="0 0 24 24">
    <path d="M6 8.5a6.5 6.5 0 1113 0c0 4.5-3 6-3 9.5a3 3 0 01-6 0" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-shield" viewBox="0 0 24 24">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-leaf" viewBox="0 0 24 24">
    <path d="M11 20A7 7 0 019.8 6.9C15.5 4.9 17 3.5 17 3.5s1 3 1 7c0 4-2.5 6.5-5 8l-2 1.5z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-eye" viewBox="0 0 24 24">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  </symbol>
  <symbol id="icon-bandage" viewBox="0 0 24 24">
    <path d="M18 2l4 4-12 12-4-4L18 2zM2 18l4 4 2-2-4-4-2 2z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-refresh" viewBox="0 0 24 24">
    <path d="M23 4v6h-6M1 20v-6h6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <!-- Pain point icons -->
  <symbol id="icon-clock" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <path d="M12 6v6l4 2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-dollar" viewBox="0 0 24 24">
    <path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-map-pin" viewBox="0 0 24 24">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="12" cy="10" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  </symbol>
  <symbol id="icon-clipboard" viewBox="0 0 24 24">
    <path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1" fill="none" stroke="currentColor" stroke-width="1.5"/>
  </symbol>
</svg>

<!-- Skip to Content -->
<a href="#main" class="skip-link">Skip to content</a>

<!-- NAV -->
<!-- SVG icon definitions (hidden) -->
<svg style="display:none;">
  <defs>
    <symbol id="npc-icon-zap" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></symbol>
    <symbol id="npc-icon-heart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></symbol>
    <symbol id="npc-icon-user" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></symbol>
    <symbol id="npc-icon-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></symbol>
    <symbol id="npc-icon-help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></symbol>
    <symbol id="npc-icon-pill" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 1.5H8A6.5 6.5 0 001.5 8v8A6.5 6.5 0 008 22.5h8a6.5 6.5 0 006.5-6.5v-2.5"/><path d="M16 2l-6 6"/></symbol>
    <symbol id="npc-icon-list" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></symbol>
    <symbol id="npc-icon-message" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></symbol>
    <symbol id="npc-icon-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></symbol>
    <symbol id="npc-icon-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></symbol>
    <symbol id="npc-icon-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></symbol>
  </defs>
</svg>

<header>
<nav class="npc-nav" aria-label="Main navigation">
  <div class="npc-nav-inner">
    <a href="https://npcwoods.com" class="npc-nav-logo">
      <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="NPCWoods" width="32" height="32">
      NPCWoods
    </a>

    <ul class="npc-nav-links">
      <li>
        <a href="https://npcwoods.com/conditions/">Conditions <span class="nav-arrow">&#9662;</span></a>
        <div class="npc-dropdown">
          <a href="https://npcwoods.com/uti-treatment/">UTI Treatment</a>
          <a href="https://npcwoods.com/sinus-infection-treatment/">Sinus Infection</a>
          <a href="https://npcwoods.com/dental-pain/">Dental Pain</a>
          <a href="https://npcwoods.com/ear-infection/">Ear Infection</a>
          <a href="https://npcwoods.com/ed-treatment/">ED Treatment</a>
          <a href="https://npcwoods.com/conditions/">View All Conditions</a>
        </div>
      </li>
      <li>
        <a href="#how">How It Works</a>
      </li>
      <li>
        <a href="#coverage">States <span class="nav-arrow">&#9662;</span></a>
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
        </div>
      </li>
      <li>
        <a href="sms:4806394722" class="npc-nav-cta">$59 · Text Us</a>
      </li>
    </ul>

    <button class="npc-nav-toggle" id="npcHamburger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- Slide-out overlay -->
<div class="npc-menu-overlay" id="npcOverlay"></div>

<!-- Slide-out navigation panel -->
<div class="npc-slide-panel" id="npcSlidePanel" role="dialog" aria-label="Navigation menu">
  <div class="npc-panel-header">
    <div class="npc-panel-logo">
      <img src="https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp" alt="">
      NPCWoods
    </div>
    <button class="npc-panel-close" id="npcPanelClose" aria-label="Close menu">
      <svg><use href="#npc-icon-x"/></svg>
    </button>
  </div>
  <div class="npc-panel-body">

    <!-- Navigate -->
    <div class="npc-panel-section">
      <div class="npc-panel-section-label">Navigate</div>
      <a href="#how" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-zap"/></svg></div>
        <div class="npc-panel-link-text">How It Works<div class="npc-panel-link-sub">3 simple steps to care</div></div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/conditions/" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-heart"/></svg></div>
        <div class="npc-panel-link-text">Conditions We Treat<div class="npc-panel-link-sub">UTI, sinus, strep &amp; more</div></div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/about/" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-user"/></svg></div>
        <div class="npc-panel-link-text">About Chris<div class="npc-panel-link-sub">MSN, FNP-C · Double Board-Certified</div></div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/about/#licenses" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-shield"/></svg></div>
        <div class="npc-panel-link-text">Licenses &amp; Credentials<div class="npc-panel-link-sub">Verified in 11 states</div></div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/#faq" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-help"/></svg></div>
        <div class="npc-panel-link-text">FAQ<div class="npc-panel-link-sub">Common questions answered</div></div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
    </div>

    <div class="npc-panel-divider"></div>

    <!-- States We Serve -->
    <div class="npc-panel-section">
      <div class="npc-panel-section-label">States We Serve</div>
      <div class="npc-states-grid">
        <a href="https://npcwoods.com/arizona-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Arizona</a>
        <a href="https://npcwoods.com/colorado-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Colorado</a>
        <a href="https://npcwoods.com/georgia-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Georgia</a>
        <a href="https://npcwoods.com/idaho-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Idaho</a>
        <a href="https://npcwoods.com/iowa-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Iowa</a>
        <a href="https://npcwoods.com/montana-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Montana</a>
        <a href="https://npcwoods.com/nevada-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Nevada</a>
        <a href="https://npcwoods.com/new-mexico-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> New Mexico</a>
        <a href="https://npcwoods.com/north-carolina-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> North Carolina</a>
        <a href="https://npcwoods.com/oregon-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Oregon</a>
        <a href="https://npcwoods.com/utah-telemedicine/" class="npc-state-link"><span class="npc-state-dot"></span> Utah</a>
      </div>
    </div>

    <div class="npc-panel-divider"></div>

    <!-- Common Services -->
    <div class="npc-panel-section">
      <div class="npc-panel-section-label">Common Services</div>
      <a href="https://npcwoods.com/uti-treatment/" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-pill"/></svg></div>
        <div class="npc-panel-link-text">UTI Treatment</div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/sinus-infection-treatment/" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-heart"/></svg></div>
        <div class="npc-panel-link-text">Sinus Infection</div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/dental-pain/" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-heart"/></svg></div>
        <div class="npc-panel-link-text">Dental Pain Relief</div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
      <a href="https://npcwoods.com/conditions/" class="npc-panel-link">
        <div class="npc-panel-link-icon"><svg><use href="#npc-icon-list"/></svg></div>
        <div class="npc-panel-link-text">All Conditions<div class="npc-panel-link-sub">Full list of what we treat</div></div>
        <svg class="npc-panel-link-arrow" width="16" height="16"><use href="#npc-icon-chevron"/></svg>
      </a>
    </div>

    <div class="npc-panel-divider"></div>

    <!-- Get Care Now -->
    <div class="npc-panel-section">
      <div class="npc-panel-section-label">Get Care Now</div>
      <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="npc-panel-cta">
        <svg><use href="#npc-icon-message"/></svg>
        Text Chris · Start My $59 Visit
      </a>
      <a href="tel:4806394722" class="npc-panel-phone">
        <div class="npc-panel-phone-icon"><svg><use href="#npc-icon-phone"/></svg></div>
        <div class="npc-panel-link-text">Call (480) 639-4722<div class="npc-panel-link-sub">Available 7 days a week</div></div>
      </a>
    </div>

  </div>
</div>

<script>
(function() {
  var hamburger = document.getElementById('npcHamburger');
  var panel = document.getElementById('npcSlidePanel');
  var overlay = document.getElementById('npcOverlay');
  var panelClose = document.getElementById('npcPanelClose');
  if (!hamburger || !panel || !overlay || !panelClose) return;

  function openMenu() {
    panel.classList.add('active');
    overlay.classList.add('active');
    hamburger.classList.add('active');
    hamburger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    panelClose.focus();
  }

  function closeMenu() {
    panel.classList.remove('active');
    overlay.classList.remove('active');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    hamburger.focus();
  }

  hamburger.addEventListener('click', function() {
    panel.classList.contains('active') ? closeMenu() : openMenu();
  });

  overlay.addEventListener('click', closeMenu);
  panelClose.addEventListener('click', closeMenu);

  // Close on link click
  var links = panel.querySelectorAll('.npc-panel-link, .npc-state-link, .npc-panel-cta, .npc-panel-phone');
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', closeMenu);
  }

  // Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && panel.classList.contains('active')) closeMenu();
  });
})();
</script>
</header>


<!-- MAIN -->
<!-- MAIN (v2 homepage port 2026-04-12) -->
<main id="main">

<style>
/* ===== V2 HOMEPAGE STYLES (namespaced under .home-v2 for production isolation) ===== */

  /* Reset production styles that leak through non-namespaced selectors (.hero, .steps, .step, .stars) */
  .home-v2 section.hero{
    background:#FDF8F4 !important;
    min-height:auto !important;
    overflow:visible !important;
    display:block !important;
    flex-direction:initial !important;
    justify-content:initial !important;
  }
  .home-v2 section.steps{
    max-width:none !important;
    margin:0 !important;
    display:block !important;
    grid-template-columns:none !important;
    gap:0 !important;
    position:static !important;
  }
  .home-v2 .step{text-align:left !important}
  .home-v2 .stars{display:inline-block !important;gap:0 !important}

  /* Force production nav readable on the cream v2 hero (was transparent + white text, designed for the old blue hero) */
  .npc-nav{background:#FFFFFF !important;border-bottom:1px solid #E5E7EB !important}
  .npc-nav:not(.scrolled),
  .npc-nav a,
  .npc-nav .nav-link,
  .npc-nav .logo-text{color:#1A1A2E !important}
  .npc-nav .btn-primary,
  .npc-nav .nav-cta{background:#2563EB !important;color:#FFFFFF !important;border-color:#2563EB !important}

  .home-v2{
    --v2-cream:#FDF8F4;
    --v2-cream-2:#F5EFE7;
    --v2-paper:#FFFFFF;
    --v2-ink:#1A1A2E;
    --v2-ink-soft:#3B3B52;
    --v2-muted:#6B6B7B;
    --v2-line:#E6DED3;
    --v2-line-2:#EFE7DA;
    --v2-brand:#2563EB;
    --v2-brand-ink:#1D4ED8;
    --v2-brand-soft:#EFF6FF;
    --v2-coral:#C2614F;
    --v2-amber:#F59E0B;
    --v2-green:#16A34A;
    --v2-radius:14px;
    --v2-maxw:1220px;
    font-family:'Inter',ui-sans-serif,system-ui,sans-serif;
    background:var(--v2-cream);color:var(--v2-ink);
    font-size:17px;line-height:1.55;
  }
  .home-v2 *{box-sizing:border-box}
  .home-v2 a{color:var(--v2-brand);text-decoration:none}
  .home-v2 a:hover{color:var(--v2-brand-ink)}
  .home-v2 img{max-width:100%;display:block}
  .home-v2 .wrap{max-width:var(--v2-maxw);margin:0 auto;padding:0 28px}

  /* Preview-only nav (production will use the real site nav) */
  
  
  .home-v2 .logo{font-family:'Source Serif 4',Georgia,serif;font-weight:800;font-size:22px;letter-spacing:-.02em;color:var(--v2-ink)}
  .home-v2 .logo span{color:var(--v2-brand)}
  
  
  

  .home-v2 .btn{display:inline-block;padding:12px 22px;border-radius:10px;font-weight:600;font-size:15px;transition:transform .15s ease,box-shadow .15s ease,background .15s ease;border:1px solid transparent;cursor:pointer;text-decoration:none}
  .home-v2 .btn-primary{background:var(--v2-ink);color:var(--v2-cream);border-color:var(--v2-ink)}
  .home-v2 .btn-primary:hover{background:#000;color:#fff;transform:translateY(-1px);box-shadow:0 10px 24px -10px rgba(0,0,0,.45)}
  .home-v2 .btn-cta{background:var(--v2-brand);color:#fff;border:1px solid var(--v2-brand);padding:16px 28px;font-size:16px;border-radius:10px}
  .home-v2 .btn-cta:hover{background:var(--v2-brand-ink);color:#fff;transform:translateY(-1px);box-shadow:0 14px 30px -12px rgba(37,99,235,.55)}
  .home-v2 .btn-outline{background:transparent;color:var(--v2-ink);border:1px solid var(--v2-ink);padding:16px 28px;font-size:16px;border-radius:10px}
  .home-v2 .btn-outline:hover{background:var(--v2-ink);color:var(--v2-cream)}

  /* HERO */
  .home-v2 section.hero{padding:72px 0 80px;position:relative}
  .home-v2 .hero-grid{display:grid;grid-template-columns:1.15fr .95fr;gap:56px;align-items:center}
  .home-v2 .eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--v2-brand);margin-bottom:22px}
  .home-v2 .eyebrow .dot{width:8px;height:8px;border-radius:50%;background:var(--v2-brand);box-shadow:0 0 0 5px rgba(37,99,235,.15)}
  .home-v2 h1{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(44px,6vw,80px);line-height:1.03;letter-spacing:-.025em;margin:0 0 24px;color:var(--v2-ink)}
  .home-v2 h1 em{color:var(--v2-brand);font-weight:700;font-style:normal}
  .home-v2 .lede{font-size:20px;color:var(--v2-ink-soft);max-width:560px;margin:0 0 30px;line-height:1.5}
  .home-v2 .hero-cta{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-bottom:34px}

  .home-v2 .trust-row{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;padding-top:22px;border-top:1px solid var(--v2-line)}
  .home-v2 .trust-pill{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:#fff;border:1px solid var(--v2-line);font-size:13.5px;color:var(--v2-ink-soft);font-weight:500}
  .home-v2 .trust-pill svg{width:14px;height:14px;color:var(--v2-brand);flex:none}

  .home-v2 .cred-card{background:var(--v2-paper);border:1px solid var(--v2-line);border-radius:18px;box-shadow:0 28px 60px -32px rgba(26,26,46,.28),0 6px 16px -10px rgba(26,26,46,.12);padding:30px 30px 26px;position:relative}
  .home-v2 .cred-head{display:flex;gap:18px;align-items:center;margin-bottom:22px}
  .home-v2 .portrait-slot{width:96px;height:96px;flex:none;border-radius:50%;background:#F1EAE0;border:1px solid var(--v2-line);display:flex;align-items:center;justify-content:center;overflow:hidden}
  .home-v2 .portrait-slot img{width:100%;height:100%;object-fit:cover;object-position:center center}
  .home-v2 .cred-name{font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:22px;letter-spacing:-.01em;margin:0;color:var(--v2-ink)}
  .home-v2 .cred-title{font-size:14px;color:var(--v2-muted);margin-top:2px;line-height:1.4}
  .home-v2 .cred-title b{color:var(--v2-ink-soft);font-weight:600}
  .home-v2 .cred-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--v2-line-2);border:1px solid var(--v2-line-2);border-radius:12px;overflow:hidden;margin-bottom:18px}
  .home-v2 .cred-stat{background:#fff;padding:14px 16px}
  .home-v2 .cred-stat .n{font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:22px;letter-spacing:-.01em;color:var(--v2-ink);line-height:1.1}
  .home-v2 .cred-stat .l{font-size:12px;color:var(--v2-muted);margin-top:2px;letter-spacing:.02em}
  .home-v2 .cred-badges{display:flex;flex-wrap:wrap;gap:8px}
  .home-v2 .badge{display:inline-flex;align-items:center;gap:6px;padding:6px 10px;border-radius:8px;font-size:12px;font-weight:600;letter-spacing:.02em;background:var(--v2-brand-soft);color:var(--v2-brand-ink);border:1px solid #DBE8FF}
  .home-v2 .badge.gray{background:#F3EFE8;color:var(--v2-ink-soft);border-color:var(--v2-line)}
  .home-v2 .badge svg{width:12px;height:12px}
  .home-v2 .cred-foot{display:flex;justify-content:space-between;align-items:center;margin-top:18px;padding-top:14px;border-top:1px dashed var(--v2-line);font-size:12px;color:var(--v2-muted);gap:12px;flex-wrap:wrap}
  .home-v2 .cred-foot code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--v2-ink-soft)}

  /* MARQUEE */
  .home-v2 section.marquee{padding:20px 0;border-top:1px solid var(--v2-line);border-bottom:1px solid var(--v2-line);background:var(--v2-cream);overflow:hidden}
  .home-v2 .marq-inner{display:flex;gap:46px;animation:v2slide 50s linear infinite;white-space:nowrap;font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:20px;color:var(--v2-ink-soft)}
  .home-v2 .marq-inner span{display:inline-flex;align-items:center;gap:14px}
  .home-v2 .marq-inner span::after{content:"•";color:var(--v2-brand);font-size:14px;margin-left:14px}
  /* Eligibility — What we treat / What we refer */
  .home-v2 section.eligibility{padding:64px 0;border-top:1px solid var(--v2-line);border-bottom:1px solid var(--v2-line);background:var(--v2-cream)}
  .home-v2 .elig-head{text-align:center;max-width:620px;margin:0 auto 36px}
  .home-v2 .elig-head .kicker{display:inline-block;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--v2-brand);margin-bottom:14px}
  .home-v2 .elig-head h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(28px,3.6vw,40px);line-height:1.1;letter-spacing:-.02em;margin:0 0 12px;color:var(--v2-ink)}
  .home-v2 .elig-head p{color:var(--v2-ink-soft);font-size:16px;margin:0}
  .home-v2 .elig-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1040px;margin:0 auto}
  .home-v2 .elig-card{background:#fff;border:1px solid var(--v2-line);border-radius:var(--v2-radius);padding:28px 26px}
  .home-v2 .elig-card .elig-icon{width:36px;height:36px;border-radius:8px;display:inline-flex;align-items:center;justify-content:center;margin-bottom:14px}
  .home-v2 .elig-card.elig-treat .elig-icon{background:#E6F4EC;color:#16A34A}
  .home-v2 .elig-card.elig-refer .elig-icon{background:#F1EEFB;color:#5B4ED1}
  .home-v2 .elig-card h3{font-family:'Source Serif 4',Georgia,serif;font-size:22px;margin:0 0 4px;font-weight:600;letter-spacing:-.01em;color:var(--v2-ink)}
  .home-v2 .elig-card .elig-sub{color:var(--v2-muted);font-size:14px;margin:0 0 16px;line-height:1.5}
  .home-v2 .elig-card.elig-treat ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
  .home-v2 .elig-card.elig-treat ul li{background:#F5EFE7;border:1px solid #E6DED3;color:var(--v2-ink);padding:6px 12px;border-radius:999px;font-size:14px;font-weight:500}
  .home-v2 .elig-card.elig-refer ul{list-style:none;margin:0;padding:0}
  .home-v2 .elig-card.elig-refer ul li{padding:9px 0;border-bottom:1px dashed #E6DED3;color:var(--v2-ink-soft);font-size:14.5px;line-height:1.4}
  .home-v2 .elig-card.elig-refer ul li:last-child{border-bottom:0}
  @media (max-width:780px){
    .home-v2 .elig-grid{grid-template-columns:1fr}
  }
  @keyframes v2slide{from{transform:translateX(0)}to{transform:translateX(-50%)}}

  /* BROKEN / FIXED */
  .home-v2 section.broken{padding:104px 0}
  .home-v2 .section-head{max-width:780px;margin:0 auto 54px;text-align:center}
  .home-v2 .kicker{display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--v2-brand);margin-bottom:14px}
  .home-v2 .section-head h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(32px,4.4vw,52px);line-height:1.08;letter-spacing:-.02em;margin:0 0 16px;color:var(--v2-ink)}
  .home-v2 .section-head h2 em{color:var(--v2-brand);font-weight:700;font-style:normal}
  .home-v2 .section-head p{font-size:18px;color:var(--v2-ink-soft);margin:0}
  .home-v2 .broken-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .home-v2 .broken-card{background:#fff;border:1px solid var(--v2-line);border-radius:var(--v2-radius);padding:26px 22px;transition:transform .18s ease,box-shadow .18s ease}
  .home-v2 .broken-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px -22px rgba(26,26,46,.25)}
  .home-v2 .broken-card .x{width:34px;height:34px;border-radius:8px;background:#FBEDE8;color:var(--v2-coral);display:inline-flex;align-items:center;justify-content:center;font-weight:700;margin-bottom:14px;font-size:14px}
  .home-v2 .broken-card h3{font-family:'Source Serif 4',Georgia,serif;font-size:18px;margin:0 0 4px;font-weight:600;letter-spacing:-.01em}
  .home-v2 .broken-card .strike{color:var(--v2-muted);font-size:14px}

  /* SAVINGS CALCULATOR */
  .home-v2 section.savings{padding:110px 0;background:var(--v2-cream);border-top:1px solid var(--v2-line)}
  .home-v2 .calc-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:56px;max-width:1100px;margin:0 auto;align-items:center}
  .home-v2 .calc-controls{background:#fff;border:1px solid var(--v2-line);border-radius:16px;padding:32px 32px 28px;box-shadow:0 18px 46px -24px rgba(26,26,46,.18)}
  .home-v2 .calc-controls label{display:block;margin-bottom:24px}
  .home-v2 .calc-controls label:last-child{margin-bottom:0}
  .home-v2 .calc-controls .lbl{display:flex;justify-content:space-between;align-items:baseline;font-size:14px;color:var(--v2-ink-soft);font-weight:500;margin-bottom:10px;letter-spacing:.02em}
  .home-v2 .calc-controls .val{font-family:'Source Serif 4',serif;font-weight:700;font-size:20px;color:var(--v2-ink);letter-spacing:-.01em}
  .home-v2 .calc-controls input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:6px;border-radius:999px;background:linear-gradient(to right,var(--v2-brand) 0%,var(--v2-brand) var(--p,50%),var(--v2-line) var(--p,50%),var(--v2-line) 100%);outline:none;cursor:pointer}
  .home-v2 .calc-controls input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:22px;height:22px;border-radius:50%;background:#fff;border:2px solid var(--v2-brand);box-shadow:0 4px 14px -4px rgba(37,99,235,.45);cursor:pointer;transition:transform .1s ease}
  .home-v2 .calc-controls input[type=range]::-webkit-slider-thumb:active{transform:scale(1.12)}
  .home-v2 .calc-controls input[type=range]::-moz-range-thumb{width:22px;height:22px;border-radius:50%;background:#fff;border:2px solid var(--v2-brand);cursor:pointer}
  .home-v2 .calc-output{position:relative;padding:10px}
  .home-v2 .savings-amt{font-family:'Source Serif 4',serif;font-weight:800;font-size:clamp(56px,8vw,96px);line-height:1;letter-spacing:-.03em;color:var(--v2-brand);margin-bottom:6px}
  .home-v2 .savings-lbl{font-size:16px;color:var(--v2-ink-soft);margin-bottom:26px}
  .home-v2 .bars{display:flex;flex-direction:column;gap:12px;margin-bottom:26px}
  .home-v2 .bar{display:flex;align-items:center;gap:14px;font-size:14px}
  .home-v2 .bar-lbl{flex:none;width:120px;color:var(--v2-ink-soft);font-weight:500}
  .home-v2 .bar-track{flex:1;height:14px;background:var(--v2-cream-2);border-radius:999px;overflow:hidden;border:1px solid var(--v2-line)}
  .home-v2 .bar-fill{height:100%;border-radius:999px;width:0;transition:width .6s cubic-bezier(.2,.8,.2,1)}
  .home-v2 .bar.ur .bar-fill{background:var(--v2-coral)}
  .home-v2 .bar.vid .bar-fill{background:#D4AF37}
  .home-v2 .bar.npc .bar-fill{background:var(--v2-brand)}
  .home-v2 .bar-amt{flex:none;width:74px;text-align:right;font-family:'Source Serif 4',serif;font-weight:700;color:var(--v2-ink);font-variant-numeric:tabular-nums}
  .home-v2 .calc-output .cta-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}

  /* HOW IT WORKS */
  .home-v2 section.steps{padding:104px 0;background:var(--v2-cream-2);border-top:1px solid var(--v2-line);border-bottom:1px solid var(--v2-line)}
  .home-v2 .steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
  .home-v2 .step{background:#fff;border-radius:16px;overflow:hidden;border:1px solid var(--v2-line);transition:transform .2s ease,box-shadow .2s ease}
  .home-v2 .step:hover{transform:translateY(-3px);box-shadow:0 22px 46px -24px rgba(26,26,46,.28)}
  .home-v2 .step .photo{aspect-ratio:1/1;overflow:hidden;background:var(--v2-cream-2);position:relative}
  .home-v2 .step .photo img{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
  .home-v2 .step:hover .photo img{transform:scale(1.03)}
  .home-v2 .step .photo .num{position:absolute;left:18px;top:18px;width:40px;height:40px;border-radius:50%;background:var(--v2-ink);color:var(--v2-cream);display:flex;align-items:center;justify-content:center;font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:18px}
  .home-v2 .step .body{padding:26px 24px 28px}
  .home-v2 .step h3{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:21px;margin:0 0 8px;letter-spacing:-.01em}
  .home-v2 .step p{margin:0;color:var(--v2-ink-soft);font-size:15.5px}
  .home-v2 .step .time{display:inline-flex;align-items:center;gap:6px;margin-top:12px;font-size:13px;font-weight:600;color:var(--v2-brand);letter-spacing:.02em}

  /* MEET CHRIS */
  .home-v2 section.meet{padding:110px 0}
  .home-v2 .meet-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:center}
  .home-v2 .meet-portrait{position:relative;aspect-ratio:1/1;border-radius:18px;overflow:hidden;background:#F1EAE0;border:1px solid var(--v2-line);box-shadow:0 30px 70px -30px rgba(26,26,46,.3)}
  .home-v2 .meet-portrait img{width:100%;height:100%;object-fit:cover;object-position:center center}
  .home-v2 .meet h2{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(32px,4vw,48px);font-weight:600;letter-spacing:-.02em;line-height:1.08;margin:0 0 18px}
  .home-v2 .meet h2 em{color:var(--v2-brand);font-style:italic;font-weight:700}
  .home-v2 .meet p{color:var(--v2-ink-soft);font-size:17.5px;margin:0 0 18px;max-width:560px}
  .home-v2 .creds-list{margin:22px 0 26px;padding:0;list-style:none}
  .home-v2 .creds-list li{display:flex;gap:12px;align-items:flex-start;padding:9px 0;border-bottom:1px solid var(--v2-line);font-size:15.5px;color:var(--v2-ink)}
  .home-v2 .creds-list li:last-child{border-bottom:0}
  .home-v2 .creds-list li svg{width:18px;height:18px;color:var(--v2-brand);flex:none;margin-top:3px}
  .home-v2 .creds-list li b{font-weight:600;color:var(--v2-ink)}
  .home-v2 .creds-list li span{color:var(--v2-muted);margin-left:auto;font-size:13.5px}

  /* SMS DEMO */
  .home-v2 section.sms{padding:110px 0;background:var(--v2-cream-2);border-top:1px solid var(--v2-line);border-bottom:1px solid var(--v2-line)}
  .home-v2 .phone{max-width:440px;margin:0 auto;background:#fff;border-radius:32px;border:1px solid var(--v2-line);box-shadow:0 40px 80px -30px rgba(26,26,46,.35),0 10px 30px -15px rgba(26,26,46,.18);overflow:hidden}
  .home-v2 .phone-head{display:flex;align-items:center;gap:10px;padding:14px 18px;border-bottom:1px solid var(--v2-line);background:#F8F6F1}
  .home-v2 .phone-head .avatar{width:34px;height:34px;border-radius:50%;overflow:hidden;background:#F1EAE0;flex:none;border:1px solid var(--v2-line)}
  .home-v2 .phone-head .avatar img{width:100%;height:100%;object-fit:cover;object-position:center center}
  .home-v2 .phone-head .meta{font-size:14px;line-height:1.15}
  .home-v2 .phone-head .name{font-weight:700;color:var(--v2-ink)}
  .home-v2 .phone-head .sub{font-size:11.5px;color:var(--v2-green);font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .home-v2 .phone-head .sub::before{content:"•";color:var(--v2-green);margin-right:4px;font-size:18px;line-height:0;position:relative;top:2px}
  .home-v2 .phone-thread{min-height:320px;max-height:420px;overflow-y:auto;padding:22px 18px;background:#FFFDF9;display:flex;flex-direction:column;gap:10px}
  .home-v2 .msg{max-width:78%;padding:10px 14px;border-radius:18px;font-size:14.5px;line-height:1.4;word-wrap:break-word}
  .home-v2 .msg.me{align-self:flex-end;background:var(--v2-brand);color:#fff;border-bottom-right-radius:6px}
  .home-v2 .msg.np{align-self:flex-start;background:#F1EDE5;color:var(--v2-ink);border-bottom-left-radius:6px}
  .home-v2 .msg.np.typing{color:var(--v2-muted);font-style:italic}
  .home-v2 .msg.np.typing::after{content:"";display:inline-block;width:1px;height:14px;background:var(--v2-ink);margin-left:3px;vertical-align:middle;animation:v2blink 1s infinite}
  @keyframes v2blink{0%,49%{opacity:1}50%,100%{opacity:0}}
  .home-v2 .phone-input{display:flex;gap:8px;padding:12px 14px;border-top:1px solid var(--v2-line);background:#fff}
  .home-v2 .phone-input input{flex:1;border:1px solid var(--v2-line);border-radius:22px;padding:10px 16px;font-size:14.5px;font-family:inherit;background:#F8F6F1;outline:none}
  .home-v2 .phone-input input:focus{border-color:var(--v2-brand);background:#fff}
  .home-v2 .phone-input button{background:var(--v2-brand);color:#fff;border:none;border-radius:22px;padding:10px 18px;font-weight:600;font-size:14px;cursor:pointer;transition:background .15s ease}
  .home-v2 .phone-input button:hover{background:var(--v2-brand-ink)}
  .home-v2 .phone-input button:disabled{background:var(--v2-muted);cursor:not-allowed}
  .home-v2 .phone-suggest{padding:10px 16px 16px;font-size:13px;color:var(--v2-muted);display:flex;gap:6px;flex-wrap:wrap;align-items:center;background:#fff}
  .home-v2 .phone-suggest .chip{background:var(--v2-cream-2);border:1px solid var(--v2-line);color:var(--v2-ink-soft);border-radius:999px;padding:5px 11px;font-size:12.5px;cursor:pointer;transition:background .15s ease,color .15s ease;font-family:inherit}
  .home-v2 .phone-suggest .chip:hover{background:var(--v2-brand);color:#fff;border-color:var(--v2-brand)}

  /* COVERAGE */
  .home-v2 section.coverage{padding:100px 0;background:var(--v2-cream)}
  .home-v2 .map-wrap{max-width:880px;margin:0 auto;position:relative}
  .home-v2 .tile-map{display:grid;grid-template-columns:repeat(11,1fr);grid-template-rows:repeat(8,auto);gap:6px;margin:32px auto 36px;max-width:680px}
  .home-v2 .tile{aspect-ratio:1/1;border-radius:8px;background:#F1EAE0;color:#B0A995;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;letter-spacing:.02em;cursor:default;transition:transform .15s ease,background .15s ease,color .15s ease,box-shadow .15s ease;border:1px solid transparent;user-select:none}
  .home-v2 .tile:hover{background:#E6DED3;color:var(--v2-ink-soft);transform:scale(1.08);z-index:2;position:relative}
  .home-v2 .tile.lic{background:var(--v2-brand);color:#fff;box-shadow:0 4px 12px -4px rgba(37,99,235,.5)}
  .home-v2 .tile.lic:hover{background:var(--v2-brand-ink);transform:scale(1.12)}
  .home-v2 .map-legend{display:flex;justify-content:center;gap:28px;margin-bottom:18px;font-size:13.5px;color:var(--v2-ink-soft)}
  .home-v2 .map-legend span{display:inline-flex;align-items:center;gap:8px}
  .home-v2 .map-legend i{width:14px;height:14px;border-radius:4px;display:inline-block}
  .home-v2 .map-legend i.lic{background:var(--v2-brand)}
  .home-v2 .map-legend i.un{background:#F1EAE0;border:1px solid #D9CEB9}
  .home-v2 .tile-tip{position:absolute;pointer-events:none;background:var(--v2-ink);color:var(--v2-cream);padding:10px 14px;border-radius:10px;font-size:13px;line-height:1.35;transform:translate(-50%,-100%) translateY(-12px);white-space:nowrap;box-shadow:0 10px 30px -8px rgba(0,0,0,.5);opacity:0;transition:opacity .12s ease;z-index:30}
  .home-v2 .tile-tip.show{opacity:1}
  .home-v2 .tile-tip b{color:#fff}
  .home-v2 .tile-tip .t-sub{color:#9EC2FF;font-size:12px;margin-top:3px;display:block}
  .home-v2 .tile-tip.unlic .t-sub{color:#B0A995}
  .home-v2 .tile-tip::after{content:"";position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);border:6px solid transparent;border-top-color:var(--v2-ink)}

  /* PRICING */
  .home-v2 section.price{padding:110px 0;background:var(--v2-cream-2);border-top:1px solid var(--v2-line);border-bottom:1px solid var(--v2-line)}
  .home-v2 .price-wrap{max-width:980px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
  .home-v2 .price-card{background:#fff;border:1px solid var(--v2-line);border-radius:16px;padding:38px 36px;box-shadow:0 26px 60px -28px rgba(26,26,46,.28)}
  .home-v2 .price-card .big{font-family:'Source Serif 4',Georgia,serif;font-weight:800;font-size:92px;line-height:.9;letter-spacing:-.035em;color:var(--v2-ink)}
  .home-v2 .price-card .big small{font-size:32px;font-weight:600;vertical-align:top;margin-right:6px;color:var(--v2-muted)}
  .home-v2 .price-card h3{font-family:'Source Serif 4',Georgia,serif;font-size:20px;font-weight:600;margin:8px 0 18px;letter-spacing:-.01em}
  .home-v2 .price-card ul{list-style:none;padding:0;margin:0 0 6px}
  .home-v2 .price-card li{display:flex;gap:10px;align-items:flex-start;padding:8px 0;font-size:15.5px;color:var(--v2-ink-soft)}
  .home-v2 .price-card li::before{content:"✓";color:var(--v2-brand);font-weight:700;margin-top:1px}
  .home-v2 .price-copy h2{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(32px,4vw,48px);font-weight:600;line-height:1.06;letter-spacing:-.02em;margin:0 0 16px}
  .home-v2 .price-copy h2 em{color:var(--v2-brand);font-style:italic;font-weight:700}
  .home-v2 .price-copy p{color:var(--v2-ink-soft);font-size:17px;margin:0 0 22px}
  .home-v2 .micro{font-size:13.5px;color:var(--v2-muted);margin-top:14px}
  .home-v2 .hero-refund{max-width:560px;margin-top:-12px;margin-bottom:22px;line-height:1.5}

  /* TESTIMONIALS */
  .home-v2 section.testi{padding:110px 0;position:relative;color:var(--v2-cream);overflow:hidden;background:var(--v2-ink)}
  .home-v2 section.testi::before{content:"";position:absolute;inset:0;background-image:url('/wp-content/uploads/2026/04/texture.webp');background-size:cover;background-position:center;opacity:.14;filter:grayscale(.35)}
  .home-v2 .testi .wrap{position:relative}
  .home-v2 .testi .kicker{color:var(--v2-amber)}
  .home-v2 .testi h2{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(32px,4.4vw,56px);font-weight:600;letter-spacing:-.02em;line-height:1.06;margin:0 0 40px;max-width:820px}
  .home-v2 .testi h2 em{color:#A8C4FF;font-style:italic;font-weight:700}
  .home-v2 .quote-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
  .home-v2 .quote{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:var(--v2-radius);padding:26px 24px;backdrop-filter:blur(6px)}
  .home-v2 .quote .stars{color:var(--v2-amber);margin-bottom:12px;letter-spacing:2px;font-size:14px}
  .home-v2 .quote p{font-family:'Source Serif 4',Georgia,serif;font-size:17.5px;font-weight:500;line-height:1.45;margin:0 0 16px;color:#F5EDE2}
  .home-v2 .quote .who{font-size:13px;color:#C7C9D9;letter-spacing:.04em}

  /* COMPLIANCE */
  .home-v2 section.compliance{padding:46px 0;background:var(--v2-cream);border-bottom:1px solid var(--v2-line)}
  .home-v2 .comp-row{display:flex;flex-wrap:wrap;gap:28px 44px;justify-content:center;align-items:center}
  .home-v2 .comp-item{display:inline-flex;align-items:center;gap:12px;font-size:14px;color:var(--v2-ink-soft)}
  .home-v2 .comp-item .ic{width:34px;height:34px;border-radius:8px;background:#fff;border:1px solid var(--v2-line);display:flex;align-items:center;justify-content:center;color:var(--v2-brand)}
  .home-v2 .comp-item .ic svg{width:18px;height:18px}
  .home-v2 .comp-item b{color:var(--v2-ink);font-weight:700;margin-right:4px}

  /* FAQ */
  .home-v2 section.faq-v2{padding:104px 0}
  .home-v2 .faq-v2-wrap{max-width:840px;margin:0 auto}
  .home-v2 .faq-v2-item{border-bottom:1px solid var(--v2-line);padding:20px 0}
  .home-v2 .faq-v2-item summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:20px;font-family:'Source Serif 4',Georgia,serif;font-size:21px;font-weight:600;color:var(--v2-ink);letter-spacing:-.01em;cursor:pointer}
  .home-v2 .faq-v2-item summary::-webkit-details-marker{display:none}
  .home-v2 .faq-v2-item summary::after{content:"+";font-family:'Inter';font-weight:400;font-size:26px;color:var(--v2-brand);transition:transform .2s ease}
  .home-v2 .faq-v2-item[open] summary::after{transform:rotate(45deg)}
  .home-v2 .faq-v2-item p{color:var(--v2-ink-soft);font-size:16.5px;margin:14px 0 4px;max-width:760px}

  /* FINAL CTA */
  .home-v2 section.final{padding:110px 0 124px;text-align:center}
  .home-v2 .final h2{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:clamp(36px,5vw,68px);letter-spacing:-.025em;line-height:1.05;margin:0 0 18px}
  .home-v2 .final h2 em{color:var(--v2-brand);font-style:italic;font-weight:700}
  .home-v2 .final p{font-size:19px;color:var(--v2-ink-soft);max-width:620px;margin:0 auto 30px}
  .home-v2 .final .btn-cta{font-size:17px;padding:18px 34px}
  .home-v2 .final .ps{margin-top:20px;font-size:14px;color:var(--v2-muted)}

  /* STATUS CHIP */
  .home-v2 .status-chip{display:inline-flex;align-items:center;gap:9px;padding:8px 14px;border-radius:999px;background:#fff;border:1px solid var(--v2-line);font-size:13.5px;font-weight:500;color:var(--v2-ink-soft);transition:background .2s ease}
  .home-v2 .status-chip .status-dot{width:9px;height:9px;border-radius:50%;background:#9CA3AF;box-shadow:0 0 0 4px rgba(0,0,0,.05);flex:none}
  .home-v2 .status-chip.online .status-dot{background:var(--v2-green);box-shadow:0 0 0 4px rgba(22,163,74,.16);animation:v2pulse 2s ease-in-out infinite}
  .home-v2 .status-chip.offline{color:var(--v2-muted)}
  @keyframes v2pulse{0%,100%{box-shadow:0 0 0 4px rgba(22,163,74,.16)}50%{box-shadow:0 0 0 7px rgba(22,163,74,.08)}}

  /* ACTIVITY TICKER */
  .v2-ticker{position:fixed;left:22px;bottom:22px;z-index:40;display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #E6DED3;border-radius:999px;padding:10px 16px 10px 14px;box-shadow:0 14px 40px -16px rgba(26,26,46,.35),0 4px 10px -4px rgba(26,26,46,.15);font-size:13.5px;color:#3B3B52;max-width:340px;transform:translateY(24px);opacity:0;transition:transform .3s ease,opacity .3s ease;font-family:'Inter',system-ui,sans-serif}
  .v2-ticker.show{transform:translateY(0);opacity:1}
  .v2-ticker.hide{display:none}
  .v2-ticker .tk-dot{width:8px;height:8px;border-radius:50%;background:#16A34A;flex:none;box-shadow:0 0 0 4px rgba(22,163,74,.18);animation:v2pulse 2s ease-in-out infinite}
  .v2-ticker .tk-text{flex:1;line-height:1.35}
  .v2-ticker .tk-text b{color:#1A1A2E;font-weight:600}
  .v2-ticker .tk-close{background:none;border:none;color:#6B6B7B;font-size:18px;line-height:1;cursor:pointer;padding:2px 6px;border-radius:6px;margin-left:4px}
  .v2-ticker .tk-close:hover{background:#F5EFE7;color:#1A1A2E}

  @media (prefers-reduced-motion:reduce){
    .v2-ticker .tk-dot,.home-v2 .status-chip.online .status-dot{animation:none}
    .home-v2 .msg.np.typing::after{animation:none;opacity:1}
    .home-v2 .bar-fill{transition:none}
  }

  /* Responsive */
  @media (max-width:960px){
    .home-v2 .hero-grid{grid-template-columns:1fr;gap:40px}
    .home-v2 .broken-grid{grid-template-columns:repeat(2,1fr)}
    .home-v2 .steps-grid{grid-template-columns:1fr}
    .home-v2 .meet-grid{grid-template-columns:1fr;gap:36px}
    .home-v2 .price-wrap{grid-template-columns:1fr;gap:36px}
    .home-v2 .quote-grid{grid-template-columns:1fr}
    
    .home-v2 .calc-grid{grid-template-columns:1fr;gap:34px}
    .v2-ticker{left:12px;right:12px;bottom:12px;max-width:none}
    .home-v2 .tile-map{max-width:100%}
  }

  /* Preview-only placeholder footer */
</style>

<script>window.NPC_DATA_BASE = "/wp-content/uploads/npc-data";</script>
<script id="npc-status-data" type="application/json">{"online":true,"avgMinutes":14,"offlineNote":"Back in the morning · avg 22 min","hoursNote":"8am–9pm Mountain"}</script>
<script id="npc-activity-data" type="application/json">[{"cond":"UTI","city":"Phoenix, AZ","min":4},{"cond":"Sinus infection","city":"Salt Lake City, UT","min":12},{"cond":"Strep throat","city":"Reno, NV","min":7},{"cond":"Pink eye","city":"Boise, ID","min":18},{"cond":"Dental pain","city":"Raleigh, NC","min":9},{"cond":"UTI","city":"Tucson, AZ","min":22},{"cond":"Cold sore","city":"Missoula, MT","min":14},{"cond":"Ear infection","city":"Des Moines, IA","min":11},{"cond":"Sinus infection","city":"Atlanta, GA","min":6},{"cond":"Skin infection","city":"Albuquerque, NM","min":19}]</script>

<div class="home-v2">
<!-- HERO -->
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <div class="eyebrow"><span class="dot"></span> Async telemedicine · 11 states</div>
      <h1>Real healthcare.<br>A real clinician.<br><em>$59, same day.</em></h1>
      <p class="lede">Text your symptoms to a double board-certified Nurse Practitioner. Get evaluated, treated, and prescribed, without a waiting room, a video call, or an appointment.</p>
      <div class="hero-cta">
        <a href="#cta" class="btn btn-cta">Text your symptoms · $59 →</a>
        <a href="#how" class="btn btn-outline">How it works</a>
        <span class="status-chip" id="statusChip">
          <span class="status-dot"></span>
          <span class="status-text">Checking status…</span>
        </span>
      </div>
      <p class="micro hero-refund">If we can't safely treat you with a text visit, you won't be charged. Don't be shy — shoot us a text!</p>
      <div class="trust-row">
        <span class="trust-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg> Double board-certified NP</span>
        <span class="trust-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg> 50+ five-star reviews</span>
        <span class="trust-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/></svg> HIPAA-compliant &amp; encrypted</span>
        <span class="trust-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Under 30-min response</span>
      </div>
    </div>
    <aside class="cred-card" aria-label="About your clinician">
      <div class="cred-head">
        <div class="portrait-slot" id="heroPortrait">
          <img src="/wp-content/uploads/2026/04/chris-400.webp" alt="Chris Woods, FNP-C" width="400" height="400" fetchpriority="high" decoding="async">
        </div>
        <div>
          <p class="cred-name">Chris Woods, MSN, APRN, FNP-C</p>
          <p class="cred-title"><b>Double Board-Certified</b> Family Nurse Practitioner<br>Founder, NPCWoods Telemedicine</p>
        </div>
      </div>
      <div class="cred-stats">
        <a class="cred-stat cred-stat-link" href="https://share.google/XlmNvRT4vihOJ8KBH" rel="noopener" style="text-decoration:none;color:inherit;display:block;"><div class="n">50+</div><div class="l">Five-star reviews &rsaquo;</div></a>
        <div class="cred-stat"><div class="n">11</div><div class="l">States licensed</div></div>
        <div class="cred-stat"><div class="n">&lt;30<span style="font-size:13px">min</span></div><div class="l">Avg response</div></div>
        <div class="cred-stat"><div class="n">$59</div><div class="l">Flat · every visit</div></div>
      </div>
      <div class="cred-badges">
        <span class="badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg> LegitScript Certified</span>
        <span class="badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/></svg> HIPAA-Compliant</span>
        <span class="badge gray">FNP-C · APRN · MSN</span>
      </div>
      <div class="cred-foot">
        <span>Every visit personally reviewed by Chris · no AI, no chatbots</span>
        <code>NPI 1285125468</code>
      </div>
    </aside>
  </div>
</section>

<!-- ELIGIBILITY -->
<section class="eligibility" aria-labelledby="elig-heading">
  <div class="wrap">
    <div class="elig-head">
      <div class="kicker">An honest match</div>
      <h2 id="elig-heading">What we treat. What we don't.</h2>
      <p>So you don't waste a $59 visit on something we'd just refer out.</p>
    </div>
    <div class="elig-grid">
      <div class="elig-card elig-treat">
        <div class="elig-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
        </div>
        <h3>We treat</h3>
        <p class="elig-sub">Common acute conditions, by text — same day.</p>
        <ul>
          <li>UTI</li>
          <li>Sinus infection</li>
          <li>Strep throat</li>
          <li>Pink eye</li>
          <li>Cold sores</li>
          <li>Ear infection</li>
          <li>Skin infection</li>
          <li>Dental pain</li>
          <li>Bronchitis</li>
          <li>Yeast infection</li>
          <li>Ingrown toenail</li>
          <li>GLP-1 weight loss</li>
          <li>ED treatment</li>
        </ul>
      </div>
      <div class="elig-card elig-refer">
        <div class="elig-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
        </div>
        <h3>We refer out</h3>
        <p class="elig-sub">Some things need hands-on care. We'll point you the right direction.</p>
        <ul>
          <li>Chest pain or trouble breathing</li>
          <li>Broken bones or head injuries</li>
          <li>Pregnancy complications</li>
          <li>Kids under 2</li>
          <li>Severe abdominal pain</li>
          <li>Anything that needs labs or imaging</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- BROKEN / FIXED -->
<section class="broken">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">The old way</div>
      <h2>Healthcare is broken.<br>We <em>fixed it</em> for $59.</h2>
      <p>Four things the waiting-room system gets wrong, and what you get instead.</p>
    </div>
    <div class="broken-grid">
      <div class="broken-card"><div class="x">✕</div><h3>3-hour urgent care waits</h3><div class="strike">Half your day, gone.</div></div>
      <div class="broken-card"><div class="x">✕</div><h3>$200+ for a $20 antibiotic</h3><div class="strike">Surprise bills, weeks later.</div></div>
      <div class="broken-card"><div class="x">✕</div><h3>No clinic nearby</h3><div class="strike">Or the only one closed at 5pm.</div></div>
      <div class="broken-card"><div class="x">✕</div><h3>Paperwork &amp; denials</h3><div class="strike">Fight the plan to get care.</div></div>
    </div>
  </div>
</section>

<!-- SAVINGS CALCULATOR -->
<section class="savings" id="savings">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Run the math</div>
      <h2>What would this have <em>cost you?</em></h2>
      <p>Drag the sliders. We'll show what urgent care would have charged for the same care.</p>
    </div>
    <div class="calc-grid">
      <div class="calc-controls">
        <label>
          <span class="lbl"><span>Visits per year</span><span class="val" id="svVisitsV">4</span></span>
          <input type="range" min="1" max="12" value="4" id="svVisits">
        </label>
        <label>
          <span class="lbl"><span>Family members</span><span class="val" id="svFamV">2</span></span>
          <input type="range" min="1" max="6" value="2" id="svFam">
        </label>
        <label>
          <span class="lbl"><span>Avg urgent-care bill</span><span class="val" id="svBillV">$180</span></span>
          <input type="range" min="50" max="500" step="10" value="180" id="svBill">
        </label>
      </div>
      <div class="calc-output">
        <div class="savings-amt" id="savingsAmt">$0</div>
        <div class="savings-lbl">You'd save this year vs. urgent care</div>
        <div class="bars">
          <div class="bar ur"><span class="bar-lbl">Urgent care</span><span class="bar-track"><span class="bar-fill" id="barUC"></span></span><span class="bar-amt" id="amtUC">$0</span></div>
          <div class="bar vid"><span class="bar-lbl">Video telehealth</span><span class="bar-track"><span class="bar-fill" id="barVid"></span></span><span class="bar-amt" id="amtVid">$0</span></div>
          <div class="bar npc"><span class="bar-lbl">NPCWoods</span><span class="bar-track"><span class="bar-fill" id="barNPC"></span></span><span class="bar-amt" id="amtNPC">$0</span></div>
        </div>
        <div class="cta-row"><a href="#cta" class="btn btn-cta">Start saving · $59 →</a></div>
      </div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="steps" id="how">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">How it works</div>
      <h2>Three steps. <em>No waiting room.</em></h2>
      <p>From first text to prescription, most visits wrap up in under an hour.</p>
    </div>
    <div class="steps-grid">
      <article class="step">
        <div class="photo"><img src="/wp-content/uploads/2026/04/step_text.webp" alt="Messaging thread on a phone" loading="lazy" decoding="async" width="800" height="800"><div class="num">1</div></div>
        <div class="body"><h3>Text your symptoms</h3><p>Tell us what's going on in your own words. No form fatigue, no 30-question intake.</p><div class="time">⏱ 90 seconds</div></div>
      </article>
      <article class="step">
        <div class="photo"><img src="/wp-content/uploads/2026/04/step_review.webp" alt="Clinician reviewing notes at a desk" loading="lazy" decoding="async" width="800" height="800"><div class="num">2</div></div>
        <div class="body"><h3>A real NP reviews</h3><p>Double board-certified. Reads your history, asks any follow-ups, builds a plan for you, not a template.</p><div class="time">⏱ under 30 min</div></div>
      </article>
      <article class="step">
        <div class="photo"><img src="/wp-content/uploads/2026/04/step_pharmacy.webp" alt="Prescription at a pharmacy counter" loading="lazy" decoding="async" width="800" height="800"><div class="num">3</div></div>
        <div class="body"><h3>Pick up &amp; feel better</h3><p>Prescription sent to your pharmacy of choice. Written follow-up plan in your inbox.</p><div class="time">⏱ same day</div></div>
      </article>
    </div>
  </div>
</section>

<!-- MEET CHRIS -->
<section class="meet" id="meet">
  <div class="wrap meet-grid">
    <div class="meet-portrait" id="meetPortrait">
      <img src="/wp-content/uploads/2026/04/chris-1000.webp" alt="Chris Woods, MSN, APRN, FNP-C, founder of NPCWoods Telemedicine" loading="lazy" decoding="async" width="768" height="768">
    </div>
    <div>
      <div class="kicker">Meet your clinician</div>
      <h2>Not a provider mill.<br><em>A person who shows up.</em></h2>
      <p>Chris Woods, MSN, APRN, FNP-C, is a double board-certified Family Nurse Practitioner and the founder of NPCWoods Telemedicine. He personally reviews every patient case. No AI, no chatbots, no handoffs to someone you've never met.</p>
      <ul class="creds-list">
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>Double Board-Certified Family Nurse Practitioner</b> (FNP-C)</div></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>Advanced Practice Registered Nurse</b> (APRN)</div></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>Master of Science in Nursing</b> (MSN)</div></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>Licensed in 11 states</b><span>AZ · CO · GA · ID · IA · MT · NV · NM · NC · OR · UT</span></div></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><div><b>LegitScript Certified</b> · HIPAA-compliant practice<span>NPI 1285125468</span></div></li>
      </ul>
      <a href="#cta" class="btn btn-cta">Start a visit →</a>
    </div>
  </div>
</section>

<!-- SMS DEMO -->
<section class="sms" id="demo">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Try it</div>
      <h2>See what a visit <em>feels like.</em></h2>
      <p>Type a symptom. Chris's response streams back, same as a real visit.</p>
    </div>
    <div class="phone">
      <div class="phone-head">
        <div class="avatar"><img src="/wp-content/uploads/2026/04/chris-400.webp" alt="" loading="lazy" decoding="async" width="400" height="400"></div>
        <div class="meta">
          <div class="name">Chris Woods, FNP-C</div>
          <div class="sub">Online</div>
        </div>
      </div>
      <div class="phone-thread" id="smsThread" aria-live="polite">
        <div class="msg np">Hey, I'm Chris. Tell me what's going on and I'll take a look.</div>
      </div>
      <div class="phone-input">
        <input id="smsInput" type="text" placeholder="Describe your symptoms…" autocomplete="off">
        <button id="smsSend" type="button">Send</button>
      </div>
      <div class="phone-suggest">
        <span>Try:</span>
        <button class="chip" data-sym="uti" type="button">burning when I pee</button>
        <button class="chip" data-sym="sinus" type="button">sinus pressure 5 days</button>
        <button class="chip" data-sym="strep" type="button">sore throat + fever</button>
      </div>
    </div>
  </div>
</section>

<!-- COVERAGE TILE MAP -->
<section class="coverage" id="coverage">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Where Chris is licensed</div>
      <h2>Licensed in <em>11 states.</em> More on the way.</h2>
      <p>Hover any state for details. Blue means we can treat you today.</p>
    </div>
    <div class="map-wrap">
      <div class="map-legend">
        <span><i class="lic"></i> Licensed today</span>
        <span><i class="un"></i> Not yet licensed</span>
      </div>
      <div class="tile-map" id="tileMap"></div>
      <div class="tile-tip" id="tileTip" role="tooltip"></div>
    </div>
  </div>
</section>

<!-- PRICING -->
<section class="price" id="price">
  <div class="wrap price-wrap">
    <div class="price-copy">
      <div class="kicker">One price. One promise.</div>
      <h2>$59. That's it.<br><em>No billing.</em> No surprises.</h2>
      <p>One flat fee per visit. Pay after you're treated. HSA/FSA receipt on request.</p>
      <a href="#cta" class="btn btn-cta">Start a visit →</a>
    </div>
    <div class="price-card">
      <div class="big"><small>$</small>59</div>
      <h3>Per visit · flat fee</h3>
      <ul>
        <li>Evaluation by a double board-certified NP</li>
        <li>Same-day prescription if appropriate</li>
        <li>Written plan &amp; follow-up included</li>
        <li>HSA/FSA receipt on request</li>
        <li>No subscription · pay as you need us</li>
      </ul>
    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="testi">
  <div class="wrap">
    <div class="kicker">Why patients stay</div>
    <h2>Care that actually<br><em>shows up for you.</em></h2>
    <style>
      .quote .who{display:flex;flex-wrap:wrap;align-items:center;gap:8px;}
      .quote .via-google{display:inline-flex;align-items:center;gap:5px;font-size:.72rem;color:#5f6368;background:#fff;border:1px solid #e8eaed;padding:2px 9px;border-radius:100px;font-weight:500;letter-spacing:.01em;white-space:nowrap;}
      .quote .via-google svg{width:12px;height:12px;flex-shrink:0;}
      .testi-cta-row{display:flex;justify-content:center;margin-top:32px;}
      .btn-gbp-reviews{display:inline-flex;align-items:center;gap:10px;background:#fff;color:#202124;border:1px solid #dadce0;padding:12px 22px;border-radius:100px;font-weight:600;font-size:.95rem;text-decoration:none;transition:box-shadow .15s,border-color .15s,transform .15s;font-family:inherit;}
      .btn-gbp-reviews:hover{box-shadow:0 1px 3px rgba(60,64,67,.15);border-color:#bdc1c6;transform:translateY(-1px);}
      .btn-gbp-reviews svg{width:18px;height:18px;flex-shrink:0;}
      .btn-gbp-reviews .arrow{font-size:1.1em;color:#5f6368;}
    </style>
    <div class="quote-grid">
      <div class="quote"><div class="stars">★★★★★</div><p>"Texted my symptoms at 9pm. Prescription at my pharmacy by 9am. I've never had healthcare be this easy."</p><div class="who"><span>Sarah K. · Phoenix, AZ</span><span class="via-google" aria-label="via Google"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.83z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.83c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>via Google</span></div></div>
      <div class="quote"><div class="stars">★★★★★</div><p>"I expected a chatbot. Got a real NP who read my history and asked good questions. Worth ten times $59."</p><div class="who"><span>Marcus T. · Salt Lake City, UT</span><span class="via-google" aria-label="via Google"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.83z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.83c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>via Google</span></div></div>
      <div class="quote"><div class="stars">★★★★★</div><p>"Urgent care would've been 4 hours and $300. This was 40 minutes and $59. I'm not going back."</p><div class="who"><span>Rachel D. · Reno, NV</span><span class="via-google" aria-label="via Google"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.83z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.83c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>via Google</span></div></div>
    </div>
    <!-- TODO:REINSTATEMENT_GBP_CTA — flip script removes the inline style and swaps #gbp-pending for the real GBP URL when the profile is publicly visible again -->
    <div class="testi-cta-row" data-gbp-cta="true">
      <a class="btn-gbp-reviews" href="https://share.google/XlmNvRT4vihOJ8KBH" rel="noopener" data-gbp-href="true">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.83z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.83c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
        <span>Read all 50+ reviews on Google</span>
        <span class="arrow" aria-hidden="true">→</span>
      </a>
    </div>
  </div>
</section>

<!-- COMPLIANCE STRIP -->
<section class="compliance" aria-label="Credentials and compliance">
  <div class="wrap comp-row">
    <div class="comp-item"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg></div><span><b>LegitScript Certified</b> telemedicine provider</span></div>
    <div class="comp-item"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/></svg></div><span><b>HIPAA-compliant</b> &amp; end-to-end encrypted</span></div>
    <div class="comp-item"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg></div><span><b>Double Board-Certified NP</b> · FNP-C · APRN</span></div>
    <div class="comp-item"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h10M7 13h10M7 17h6"/></svg></div><span><b>NPI</b> 1285125468</span></div>
  </div>
</section>

<!-- FAQ (v2 namespaced to avoid colliding with production .faq-item JS) -->
<section class="faq-v2" id="faq">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Straight answers</div>
      <h2>Got questions? <em>We've got answers.</em></h2>
    </div>
    <div class="faq-v2-wrap">
      <details class="faq-v2-item" open>
        <summary>How fast will I hear back?</summary>
        <p>Most visits get a first response in under 30 minutes during operating hours. If it's after hours, we pick up first thing in the morning.</p>
      </details>
      <details class="faq-v2-item">
        <summary>Is $59 the total cost? Any hidden fees or co-pays?</summary>
        <p>We're a flat-fee cash-pay practice. $59 per visit, no billing. Many patients find that's less than a typical co-pay. We'll send a receipt you can submit to HSA/FSA.</p>
      </details>
      <details class="faq-v2-item">
        <summary>What can you treat?</summary>
        <p>18+ conditions including UTIs, sinus infections, strep throat, pink eye, dental pain, skin infections, cold sores, and more. If we can't safely treat you remotely, we'll tell you up front and refund the visit.</p>
      </details>
      <details class="faq-v2-item">
        <summary>Which states are you licensed in?</summary>
        <p>Arizona, Colorado, Georgia, Idaho, Iowa, Montana, Nevada, New Mexico, North Carolina, Oregon, and Utah.</p>
      </details>
      <details class="faq-v2-item">
        <summary>Is it really just one person reviewing my case?</summary>
        <p>Yes. Every case is read and reviewed by Chris Woods, FNP-C. No AI triage, no rotating roster of contract clinicians, no chatbots pretending to be people.</p>
      </details>
      <details class="faq-v2-item">
        <summary>Is my information private?</summary>
        <p>All messaging runs through a HIPAA-compliant, end-to-end encrypted platform. Your health information stays between you and Chris.</p>
      </details>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="final" id="cta">
  <div class="wrap">
    <h2>Care that<br><em>shows up for you.</em></h2>
    <p>Start a visit now. Text your symptoms and a real NP will be with you in under 30 minutes.</p>
    <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn btn-cta">Text your symptoms · $59 →</a>
    <div class="ps">No forms. No waiting room. No surprises.</div>
  </div>
</section>
</div><!-- /.home-v2 -->

<div class="v2-ticker hide" id="ticker" aria-live="polite" role="status">
  <span class="tk-dot"></span>
  <span class="tk-text">·</span>
  <button class="tk-close" id="tkClose" aria-label="Dismiss">×</button>
</div>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function readInlineData(elId, fetchPath) {
    const el = document.getElementById(elId);
    if (el) {
      try { return Promise.resolve(JSON.parse(el.textContent)); }
      catch(e) { /* fall through */ }
    }
    return fetch(fetchPath).then(r => r.json());
  }

  /* STATUS CHIP */
  readInlineData('npc-status-data', (window.NPC_DATA_BASE || 'assets/homepage-v2') + '/status.json').then(s => {
    const chip = $('statusChip'), txt = chip.querySelector('.status-text');
    if (s.online) {
      chip.classList.add('online');
      txt.textContent = `Chris is online · avg ${s.avgMinutes} min today`;
      const statN = document.querySelectorAll('.cred-stat .n')[2];
      if (statN) statN.innerHTML = `${s.avgMinutes}<span style="font-size:13px">min</span>`;
    } else {
      chip.classList.add('offline');
      txt.textContent = s.offlineNote || 'Back in the morning';
    }
  }).catch(() => {
    $('statusChip').querySelector('.status-text').textContent = 'Avg response under 30 min';
  });

  /* SAVINGS CALCULATOR */
  const NPC_FEE = 59, VIDEO_FEE = 89;
  const visits = $('svVisits'), fam = $('svFam'), bill = $('svBill');
  const visitsV = $('svVisitsV'), famV = $('svFamV'), billV = $('svBillV');
  const savingsAmt = $('savingsAmt');
  const barUC = $('barUC'), barVid = $('barVid'), barNPC = $('barNPC');
  const amtUC = $('amtUC'), amtVid = $('amtVid'), amtNPC = $('amtNPC');

  function setFill(el, val, max) { el.style.width = Math.max(2, (val/max)*100) + '%'; }
  function setRangeBg(el) {
    const min = +el.min, max = +el.max, v = +el.value;
    el.style.setProperty('--p', ((v-min)/(max-min)*100) + '%');
  }
  function animateNum(el, from, to, dur = 500, prefix = '$') {
    if (reduce) { el.textContent = prefix + to.toLocaleString(); return; }
    const t0 = performance.now();
    function tick(t) {
      const p = Math.min(1, (t-t0)/dur);
      const eased = 1 - Math.pow(1-p, 3);
      el.textContent = prefix + Math.round(from + (to-from)*eased).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  let prev = { save:0, uc:0, vid:0, npc:0 };
  function calc() {
    const v = +visits.value, f = +fam.value, b = +bill.value;
    visitsV.textContent = v;
    famV.textContent = f;
    billV.textContent = '$' + b;
    [visits, fam, bill].forEach(setRangeBg);
    const totalVisits = v * f;
    const uc = totalVisits * b;
    const vid = totalVisits * VIDEO_FEE;
    const npc = totalVisits * NPC_FEE;
    const save = Math.max(0, uc - npc);
    const max = Math.max(uc, vid, npc, 100);
    setFill(barUC, uc, max);
    setFill(barVid, vid, max);
    setFill(barNPC, npc, max);
    animateNum(savingsAmt, prev.save, save, 500);
    animateNum(amtUC, prev.uc, uc, 400);
    animateNum(amtVid, prev.vid, vid, 400);
    animateNum(amtNPC, prev.npc, npc, 400);
    prev = { save, uc, vid, npc };
  }
  [visits, fam, bill].forEach(el => el.addEventListener('input', calc));
  calc();

  /* SMS DEMO */
  const SCRIPTS = {
    uti: [
      "Sorry you're dealing with that. Burning with urination is a classic UTI sign, especially with urgency or more frequent trips.",
      "A few quick questions: any back pain, fever, or blood in the urine? Any history of kidney problems?",
      "Assuming none of those, I'd start a 5-day course of Macrobid. I'll send it to your pharmacy now. If you're not feeling better in 48 hrs, message me back and we'll adjust."
    ],
    sinus: [
      "Five days of facial pressure usually tells me we've crossed from viral into bacterial territory.",
      "Any fever, thick colored drainage, or tooth/jaw pain? Any allergies history?",
      "If yes to those, I'll send amoxicillin-clavulanate plus a saline rinse protocol. We'll check in at 48 hrs to make sure it's working."
    ],
    strep: [
      "Sore throat plus fever together raises my suspicion for strep. Any cough, runny nose, or body aches? A cough usually argues against strep.",
      "Without a cough and given the fever, I'm comfortable treating empirically. Amoxicillin 500mg twice daily × 10 days, sent to your pharmacy.",
      "If you're not significantly better in 48 hrs we'll need to re-evaluate in person."
    ],
    eye: [
      "Is it one eye or both? Is the drainage watery or thick/yellow? Any vision changes or pain?",
      "Thick drainage usually = bacterial conjunctivitis. I'll send erythromycin ophthalmic ointment and go over warm-compress technique."
    ],
    cold: [
      "Cold sores respond best if we hit them in the first 48 hrs. When did you first notice it?",
      "Starting valacyclovir 2g twice in one day will cut duration roughly in half. Sending the script now."
    ],
    default: [
      "Thanks, a few quick questions so I can help: how long has this been going on, and on a 1 to 10 scale how bad is it right now?",
      "Any fever, and any conditions or medications I should know about?",
      "Based on what you're describing I think we can handle this remotely. Once I hear back on those, I'll build a plan and send any prescription to your pharmacy."
    ]
  };
  function classify(input) {
    const s = input.toLowerCase();
    if (/(burn|pee|urin|uti|bladder)/.test(s)) return 'uti';
    if (/(sinus|congest|pressure|face|stuffy)/.test(s)) return 'sinus';
    if (/(throat|strep|swallow)/.test(s)) return 'strep';
    if (/(eye|pink ?eye|conjuncti)/.test(s)) return 'eye';
    if (/(cold sore|herpes|lip|blister)/.test(s)) return 'cold';
    return 'default';
  }
  const thread = $('smsThread'), input = $('smsInput'), sendBtn = $('smsSend');
  let busy = false;
  function append(cls, text) {
    const m = document.createElement('div');
    m.className = 'msg ' + cls;
    m.textContent = text;
    thread.appendChild(m);
    thread.scrollTop = thread.scrollHeight;
    return m;
  }
  function appendTyping() {
    const m = document.createElement('div');
    m.className = 'msg np typing';
    m.textContent = 'Chris is typing';
    thread.appendChild(m);
    thread.scrollTop = thread.scrollHeight;
    return m;
  }
  function stream(el, text, speed = 22) {
    return new Promise(resolve => {
      if (reduce) { el.textContent = text; resolve(); return; }
      let i = 0;
      el.textContent = '';
      (function tick() {
        if (i >= text.length) return resolve();
        el.textContent += text[i++];
        thread.scrollTop = thread.scrollHeight;
        setTimeout(tick, speed + (text[i-1] === '.' ? 120 : text[i-1] === ',' ? 60 : 0));
      })();
    });
  }
  function showVisitCTA() {
    if (thread.querySelector('.final-cta-msg')) return;
    const m = document.createElement('div');
    m.className = 'msg np final-cta-msg';
    m.innerHTML = 'Want me to handle this for real? <a href="#cta" style="color:var(--v2-brand);font-weight:700;text-decoration:underline">Start a visit · $59 →</a>';
    thread.appendChild(m);
    thread.scrollTop = thread.scrollHeight;
  }
  async function handleSend(text) {
    if (busy || !text.trim()) return;
    busy = true; sendBtn.disabled = true;
    append('me', text.trim());
    input.value = '';
    const script = SCRIPTS[classify(text)];
    for (let i = 0; i < script.length; i++) {
      const typing = appendTyping();
      await new Promise(r => setTimeout(r, reduce ? 200 : 900 + Math.random() * 600));
      typing.classList.remove('typing');
      await stream(typing, script[i]);
      await new Promise(r => setTimeout(r, reduce ? 100 : 400));
    }
    showVisitCTA();
    busy = false; sendBtn.disabled = false;
    input.focus();
  }
  sendBtn.addEventListener('click', () => handleSend(input.value));
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') handleSend(input.value); });
  document.querySelectorAll('.phone-suggest .chip').forEach(c => {
    c.addEventListener('click', () => handleSend(c.textContent));
  });

  /* COVERAGE TILE MAP */
  const LIC = new Set(['AZ','CO','GA','ID','IA','MT','NV','NM','NC','OR','UT']);
  const AVG = {AZ:11,CO:14,GA:18,ID:16,IA:21,MT:19,NV:9,NM:17,NC:22,OR:13,UT:12};
  const STATES = [
    ["ME","Maine",11,1],
    ["AK","Alaska",1,2],["VT","Vermont",10,2],["NH","New Hampshire",11,2],
    ["WA","Washington",2,3],["MT","Montana",4,3],["ND","N. Dakota",5,3],["MN","Minnesota",6,3],["WI","Wisconsin",8,3],["MI","Michigan",9,3],["NY","New York",10,3],["MA","Massachusetts",11,3],
    ["OR","Oregon",2,4],["ID","Idaho",3,4],["WY","Wyoming",4,4],["SD","S. Dakota",5,4],["IA","Iowa",6,4],["IL","Illinois",7,4],["IN","Indiana",8,4],["OH","Ohio",9,4],["PA","Pennsylvania",10,4],["CT","Connecticut",11,4],
    ["NV","Nevada",2,5],["UT","Utah",3,5],["CO","Colorado",4,5],["NE","Nebraska",5,5],["MO","Missouri",6,5],["KY","Kentucky",7,5],["WV","W. Virginia",8,5],["VA","Virginia",9,5],["NJ","New Jersey",10,5],["RI","Rhode Island",11,5],
    ["CA","California",2,6],["AZ","Arizona",3,6],["NM","New Mexico",4,6],["KS","Kansas",5,6],["AR","Arkansas",6,6],["TN","Tennessee",7,6],["NC","N. Carolina",8,6],["MD","Maryland",9,6],["DE","Delaware",10,6],
    ["HI","Hawaii",1,7],["OK","Oklahoma",5,7],["LA","Louisiana",6,7],["MS","Mississippi",7,7],["AL","Alabama",8,7],["SC","S. Carolina",9,7],["DC","D.C.",10,7],
    ["TX","Texas",5,8],["GA","Georgia",8,8],["FL","Florida",9,8]
  ];
  const mapEl = $('tileMap'), tip = $('tileTip');
  STATES.forEach(([a,n,c,r]) => {
    const t = document.createElement('div');
    t.className = 'tile' + (LIC.has(a) ? ' lic' : '');
    t.textContent = a;
    t.style.gridColumn = c;
    t.style.gridRow = r;
    t.dataset.name = n;
    t.dataset.abbr = a;
    mapEl.appendChild(t);
  });
  function showTip(ev) {
    const t = ev.currentTarget;
    const a = t.dataset.abbr, n = t.dataset.name, lic = LIC.has(a);
    tip.innerHTML = `<b>${n}</b><span class="t-sub">${lic ? `Licensed ✓ · avg ${AVG[a]} min response` : 'Coming soon'}</span>`;
    tip.classList.toggle('unlic', !lic);
    const r = t.getBoundingClientRect();
    const pr = mapEl.parentElement.getBoundingClientRect();
    tip.style.left = (r.left - pr.left + r.width/2) + 'px';
    tip.style.top = (r.top - pr.top) + 'px';
    tip.classList.add('show');
  }
  function hideTip() { tip.classList.remove('show'); }
  mapEl.querySelectorAll('.tile').forEach(t => {
    t.addEventListener('mouseenter', showTip);
    t.addEventListener('mouseleave', hideTip);
    t.addEventListener('focus', showTip);
    t.addEventListener('blur', hideTip);
    t.tabIndex = 0;
  });

  /* ACTIVITY TICKER — show ONCE per browser session, then stay hidden */
  readInlineData('npc-activity-data', (window.NPC_DATA_BASE || 'assets/homepage-v2') + '/activity.json').then(list => {
    if (!list.length) return;
    try { if (sessionStorage.getItem('npc-ticker-shown') === '1') return; } catch(e) {}
    const ticker = $('ticker'), txt = ticker.querySelector('.tk-text');
    const pick = list[Math.floor(Math.random() * list.length)];
    txt.innerHTML = `<b>${pick.cond}</b> treated · ${pick.city} · ${pick.min} min ago`;
    let dismissed = false;
    function hideTicker() {
      ticker.classList.remove('show');
      setTimeout(() => ticker.classList.add('hide'), 400);
      try { sessionStorage.setItem('npc-ticker-shown', '1'); } catch(e) {}
    }
    setTimeout(() => {
      if (dismissed) return;
      ticker.classList.remove('hide');
      requestAnimationFrame(() => ticker.classList.add('show'));
    }, 2500);
    setTimeout(() => { if (!dismissed) hideTicker(); }, 14000);
    $('tkClose').addEventListener('click', () => {
      dismissed = true;
      hideTicker();
    });
  }).catch(() => {});
})();
</script>

</main>

<!-- FOOTER -->
<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <img src="https://npcwoods.com/wp-content/uploads/2026/03/chris-headshot.jpg" alt="Chris Woods, MSN, FNP-C" class="footer-logo-img"><br><strong style="color:#fff;font-size:1rem;">Chris Woods, MSN, FNP-C</strong>
      <p>Telemedicine that shows up. $59 flat-fee visits from a licensed nurse practitioner.</p>
    </div>
    <div class="footer-links">
      <h4>Quick Links</h4>
      <ul>
        <li><a href="#how">How It Works</a></li>
        <li><a href="/conditions/">Conditions We Treat</a></li>
        <li><a href="/about/">About Chris</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
      <h4 style="margin-top:16px;">Legal</h4>
      <ul>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-service/">Terms of Service</a></li>
        <li><a href="/medical-disclaimer/">Medical Disclaimer</a></li>
      </ul>
    </div>
    <div class="footer-contact">
      <h4>Contact</h4>
      <p>Text or call anytime:</p>
      <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit">(480) 639-4722</a>
      <p><a href="mailto:cwoods@npcwoods.com" style="color:rgba(255,255,255,0.8);">cwoods@npcwoods.com</a></p>
      <p class="footer-site">npcwoods.com</p>
    </div>
  </div>
  <div style="text-align:center;padding:12px 20px 0;font-size:12px;color:rgba(255,255,255,0.5);border-top:1px solid rgba(255,255,255,0.1);margin:0 20px;">
    <p style="margin:0 0 4px;"><strong>NPCWoods Telemedicine, PLLC</strong> &middot; Chris Woods, MSN, FNP-C &middot; NPI: 1285125468</p>
    <p style="margin:0 0 4px;">AZ: 320600 | CO: C-APN.0103723-C-NP | GA: APRN-NP319386 | ID: 1671854 | IA: A183070 | MT: APRN-260601 | NV: 886822 | NM: 82936 | NC: 5010551 | OR: 10043494 | UT: 14202514-4405</p>
    <p style="margin:0 0 4px;">Telehealth service &middot; Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT</p>
  </div>
  <div style="text-align:center;padding:10px 20px;font-size:11px;color:rgba(255,255,255,0.4);max-width:600px;margin:0 auto;">
    <p style="margin:0 0 6px;"><strong style="color:#ff6b6b;">This site does not provide emergency medical services.</strong> If you are experiencing a medical emergency, call 911 immediately.</p>
    <p style="margin:0;">Telehealth services are not a substitute for in-person medical care when clinically indicated. Individual results may vary.</p>
  </div>
  <div style="text-align:center; margin-bottom:15px;"><a href="https://www.legitscript.com/websites/?checker_keywords=npcwoods.com" target="_blank" title="Verify LegitScript Approval for www.npcwoods.com"><img src="https://static.legitscript.com/seals/45807860.png" alt="Verify Approval for www.npcwoods.com" width="73" height="79" /></a></div>
  <div class="footer-bottom">
    <p>&copy; 2026 NPCWoods Telemedicine, PLLC &middot; <span style="background:rgba(37,99,235,0.3);padding:2px 8px;border-radius:3px;font-size:11px;">HIPAA COMPLIANT</span></p>
  </div>
</footer>

<!-- STICKY MOBILE CTA -->
<div class="mobile-sticky-cta" id="mobileCta">
  <a href="sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit" class="btn-primary">Start My $59 Visit</a>
</div>

<!-- STRUCTURED DATA — BreadcrumbList -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://npcwoods.com"
    }
  ]
}
</script>

<!-- STRUCTURED DATA — FAQPage -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is it safe to text my medical symptoms?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Chris is a licensed nurse practitioner, and every conversation is protected by HIPAA, the same federal privacy law that covers any clinic visit. Your messages are handled on a HIPAA-compliant platform and encrypted so your health information stays between you and Chris. Chris personally reviews and responds to every message; there is no AI triage, no call center, and no third-party handling. Your information is never shared, sold, or used for advertising."
      }
    },
    {
      "@type": "Question",
      "name": "Is this legal? Can an NP prescribe without seeing me in person?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Arizona law permits licensed NPs to evaluate and prescribe via telemedicine for many common conditions. Chris operates fully within state and federal telehealth guidelines."
      }
    },
    {
      "@type": "Question",
      "name": "Is NPCWoods just a pill mill?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Chris evaluates every case on its clinical merits. If antibiotics aren't warranted, he'll tell you honestly and explain why. He declines to prescribe when it's not appropriate, and he'll never just send you a script to get paid. The $59 covers a real clinical evaluation, not a rubber stamp."
      }
    },
    {
      "@type": "Question",
      "name": "What if I need labs or imaging?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Chris can order labs or imaging if needed and refer you to the right in-person facility. He'll always be transparent about what he can and can't handle remotely."
      }
    },
    {
      "@type": "Question",
      "name": "How do I pay?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Payment is collected securely after your visit. We accept all major credit/debit cards. No upfront payment required to start a conversation. HSA/FSA receipts available."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to file any paperwork?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We are a cash-pay practice. Many patients find $59 is less than their copay. We can provide a receipt for HSA/FSA reimbursement."
      }
    },
    {
      "@type": "Question",
      "name": "What states do you serve?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "NPCWoods currently serves patients in Arizona, Colorado, Georgia, Idaho, Iowa, Montana, Nevada, New Mexico, North Carolina, Oregon, and Utah."
      }
    },
    {
      "@type": "Question",
      "name": "What if the prescription doesn't work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Chris follows up with every patient the next day. If your symptoms aren't improving, he'll reassess your case and adjust your treatment plan, whether that means a different medication, a different dose, or a referral for in-person care. There's no extra charge for follow-up adjustments."
      }
    },
    {
      "@type": "Question",
      "name": "What if you can't treat my condition?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Then Chris will tell you directly and honestly. Some conditions need labs, imaging, or hands-on evaluation that can't be done over text. If that's your situation, he'll explain why and point you to the right next step. You won't be charged for a visit where he can't help."
      }
    }
  ]
}
</script>


<script>

// ========================================
// NAV — Scroll shadow
// ========================================
}, { passive: true });

// Hamburger menu JS is now inline in the header snippet above


// ========================================
// FAQ ACCORDION
// ========================================
// ========================================
// STICKY MOBILE CTA — Show after hero
// ========================================
const mobileCta = document.getElementById('mobileCta');
const heroEl = document.querySelector('.hero');

if (mobileCta && heroEl) {
  const ctaObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      mobileCta.style.transform = entry.isIntersecting ? 'translateY(100%)' : 'translateY(0)';
    });
  }, { threshold: 0 });

  mobileCta.style.transition = 'transform 0.3s ease';
  mobileCta.style.transform = 'translateY(100%)';
  ctaObserver.observe(heroEl);
}
</script>
<!-- NPCWoods Tracking: tracking.js -->
<script src="/tracking.js"></script>
<!-- NPCWoods Contact Save (shared snippet from html/shared/contact-save-snippet.html) -->
<style>
  .npc-save-wrap{position:fixed;bottom:24px;right:24px;z-index:998;font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;opacity:0;transform:translateY(16px);transition:opacity .4s ease,transform .4s ease;pointer-events:none}
  .npc-save-wrap.npc-save-visible{opacity:1;transform:translateY(0);pointer-events:auto}
  .npc-save-wrap.npc-save-hidden{display:none!important}
  .npc-save-btn{width:56px;height:56px;border-radius:100px;background:#FFF;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 24px rgba(0,0,0,.12);transition:all .2s ease;position:relative;padding:0}
  .npc-save-btn:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(37,99,235,.25)}
  .npc-save-btn svg{width:26px;height:26px;color:#2563EB;flex-shrink:0}
  .npc-save-btn .npc-save-dot{position:absolute;top:4px;right:4px;width:10px;height:10px;background:#2563EB;border-radius:50%;border:2px solid #FFF;animation:npc-save-pulse 2s infinite}
  .npc-save-card{position:absolute;bottom:0;right:0;width:300px;background:#FFF;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,.14);padding:24px;opacity:0;transform:scale(.9) translateY(8px);transform-origin:bottom right;transition:opacity .25s ease,transform .25s ease;pointer-events:none;visibility:hidden}
  .npc-save-card.npc-save-card-open{opacity:1;transform:scale(1) translateY(0);pointer-events:auto;visibility:visible}
  .npc-save-card-close{position:absolute;top:12px;right:12px;width:28px;height:28px;border:none;background:#F3F4F6;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;transition:background .15s ease}
  .npc-save-card-close:hover{background:#E5E7EB}
  .npc-save-card-close svg{width:14px;height:14px;color:#6B7280}
  .npc-save-card-profile{display:flex;align-items:center;gap:12px;margin-bottom:12px}
  .npc-save-card-avatar{width:48px;height:48px;border-radius:50%;object-fit:cover;flex-shrink:0;border:2px solid #EFF6FF}
  .npc-save-card-name{font-size:.95rem;font-weight:600;color:#1A1A2E;line-height:1.2}
  .npc-save-card-title{font-size:.75rem;color:#6B7280;margin-top:2px}
  .npc-save-card-msg{font-size:.9rem;color:#4A4A5A;line-height:1.5;margin-bottom:16px}
  .npc-save-card-msg strong{color:#1A1A2E}
  .npc-save-card-dl{display:block;width:100%;text-align:center;background:linear-gradient(135deg,#2563EB 0%,#1D4ED8 100%);color:#FFF;text-decoration:none;padding:12px 24px;border-radius:100px;font-size:.9rem;font-weight:600;letter-spacing:.01em;transition:all .2s ease;box-shadow:0 4px 12px rgba(37,99,235,.3);box-sizing:border-box}
  .npc-save-card-dl:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(37,99,235,.4)}
  .npc-save-card-dl svg{width:16px;height:16px;vertical-align:-3px;margin-right:6px}
  .npc-save-card-hint{text-align:center;font-size:.7rem;color:#9CA3AF;margin-top:10px;line-height:1.4}
  @keyframes npc-save-pulse{0%,100%{opacity:1}50%{opacity:.4}}
  @media (prefers-reduced-motion:reduce){.npc-save-wrap,.npc-save-card,.npc-save-btn{transition:none}.npc-save-btn .npc-save-dot{animation:none}}
  @media (max-width:640px){.npc-save-wrap{bottom:84px;right:16px}.npc-save-card{width:280px;padding:20px}}
  @media (max-width:360px){.npc-save-card{width:260px;right:-8px}}
</style>
<div class="npc-save-wrap" id="npcSaveWrap">
  <button class="npc-save-btn" id="npcSaveBtn" aria-label="Save contact info">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"/></svg>
    <span class="npc-save-dot"></span>
  </button>
  <div class="npc-save-card" id="npcSaveCard">
    <button class="npc-save-card-close" id="npcSaveDismiss" aria-label="Dismiss">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/></svg>
    </button>
    <div class="npc-save-card-profile">
      <img class="npc-save-card-avatar" src="/wp-content/uploads/2026/04/chris-400.webp" alt="Chris Woods" width="48" height="48" loading="lazy">
      <div>
        <div class="npc-save-card-name">Chris Woods, NP</div>
        <div class="npc-save-card-title">NPCWoods Telemedicine</div>
      </div>
    </div>
    <div class="npc-save-card-msg"><strong>Not sick right now?</strong> Save my number for later. Just search "sick guy" in your contacts when you need me.</div>
    <a class="npc-save-card-dl" id="npcSaveDownload" href="/chris-woods.vcf" download="Chris Woods - NPCWoods.vcf">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"/></svg>Save Contact
    </a>
    <div class="npc-save-card-hint">Saves to your phone contacts. Search "sick guy" or "urgent care" anytime</div>
  </div>
</div>
<script>
(function(){
  var wrap=document.getElementById('npcSaveWrap'),btn=document.getElementById('npcSaveBtn'),card=document.getElementById('npcSaveCard'),dismiss=document.getElementById('npcSaveDismiss'),dl=document.getElementById('npcSaveDownload');
  if(!wrap||!btn||!card)return;
  try{if(sessionStorage.getItem('npc-contact-dismissed')==='1'){wrap.classList.add('npc-save-hidden');return}}catch(e){}
  var hasSeenExpanded=false;try{hasSeenExpanded=sessionStorage.getItem('npc-contact-seen')==='1'}catch(e){}
  setTimeout(function(){
    wrap.classList.add('npc-save-visible');
    if(!hasSeenExpanded){
      setTimeout(function(){
        card.classList.add('npc-save-card-open');btn.style.opacity='0';btn.style.pointerEvents='none';
        setTimeout(function(){
          card.classList.remove('npc-save-card-open');btn.style.opacity='1';btn.style.pointerEvents='auto';
          try{sessionStorage.setItem('npc-contact-seen','1')}catch(e){}
        },5000);
      },200);
    }
  },3000);
  btn.addEventListener('click',function(){card.classList.add('npc-save-card-open');btn.style.opacity='0';btn.style.pointerEvents='none'});
  dismiss.addEventListener('click',function(){card.classList.remove('npc-save-card-open');wrap.classList.remove('npc-save-visible');try{sessionStorage.setItem('npc-contact-dismissed','1')}catch(e){}setTimeout(function(){wrap.classList.add('npc-save-hidden')},400)});
  document.addEventListener('click',function(e){if(card.classList.contains('npc-save-card-open')&&!wrap.contains(e.target)){card.classList.remove('npc-save-card-open');btn.style.opacity='1';btn.style.pointerEvents='auto'}});
  dl.addEventListener('click',function(){if(typeof gtag==='function'){gtag('event','generate_lead',{event_category:'engagement',event_label:'save_contact_vcard',value:0})}if(typeof fbq==='function'){fbq('track','Lead',{content_name:'save_contact_vcard'})}});
})();
</script>

<!-- NPCWoods CWV: GTM relocated to end of <body> by cwv-batch-fixes.py -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-59QSWZRC');</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EFFRQMG8TC"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-EFFRQMG8TC');
gtag('config', 'AW-610222919');
</script>
</body>
</html>
