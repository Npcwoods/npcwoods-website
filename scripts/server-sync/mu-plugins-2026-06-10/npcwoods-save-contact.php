<?php
/**
 * Plugin Name: NPCWoods Save Contact
 * Description: Floating button on all pages — lets patients save Chris's contact info (vCard) to their phone
 * Version: 1.0
 * Author: ChrisOS
 */

add_action('wp_footer', 'npcwoods_save_contact_button', 90);

function npcwoods_save_contact_button() {
    $snippet_path = ABSPATH . 'contact-save-snippet.html';
    if (file_exists($snippet_path)) {
        readfile($snippet_path);
    } else {
        // Inline fallback if the snippet file isn't uploaded
        ?>
<!-- NPCWoods Contact Save -->
<style>
  .npc-save-wrap {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 998;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.4s ease, transform 0.4s ease;
    pointer-events: none;
  }
  .npc-save-wrap.npc-save-visible {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }
  .npc-save-wrap.npc-save-hidden {
    display: none !important;
  }
  .npc-save-btn {
    width: 56px;
    height: 56px;
    border-radius: 100px;
    background: #FFFFFF;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.12);
    transition: all 0.2s ease;
    position: relative;
    padding: 0;
  }
  .npc-save-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(37,99,235,0.25);
  }
  .npc-save-btn svg {
    width: 26px;
    height: 26px;
    color: #2563EB;
    flex-shrink: 0;
  }
  .npc-save-btn .npc-save-dot {
    position: absolute;
    top: 4px;
    right: 4px;
    width: 10px;
    height: 10px;
    background: #2563EB;
    border-radius: 50%;
    border: 2px solid #FFFFFF;
    animation: npc-save-pulse 2s infinite;
  }
  .npc-save-card {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 300px;
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.14);
    padding: 24px;
    opacity: 0;
    transform: scale(0.9) translateY(8px);
    transform-origin: bottom right;
    transition: opacity 0.25s ease, transform 0.25s ease;
    pointer-events: none;
    visibility: hidden;
  }
  .npc-save-card.npc-save-card-open {
    opacity: 1;
    transform: scale(1) translateY(0);
    pointer-events: auto;
    visibility: visible;
  }
  .npc-save-card-close {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 28px;
    height: 28px;
    border: none;
    background: #F3F4F6;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    transition: background 0.15s ease;
  }
  .npc-save-card-close:hover { background: #E5E7EB; }
  .npc-save-card-close svg { width: 14px; height: 14px; color: #6B7280; }
  .npc-save-card-profile { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
  .npc-save-card-avatar { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 2px solid #EFF6FF; }
  .npc-save-card-name { font-size: 0.95rem; font-weight: 600; color: #1A1A2E; line-height: 1.2; }
  .npc-save-card-title { font-size: 0.75rem; color: #6B7280; margin-top: 2px; }
  .npc-save-card-msg { font-size: 0.9rem; color: #4A4A5A; line-height: 1.5; margin-bottom: 16px; }
  .npc-save-card-msg strong { color: #1A1A2E; }
  .npc-save-card-dl {
    display: block;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: #FFFFFF;
    text-decoration: none;
    padding: 12px 24px;
    border-radius: 100px;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    box-sizing: border-box;
  }
  .npc-save-card-dl:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(37,99,235,0.4); }
  .npc-save-card-dl svg { width: 16px; height: 16px; vertical-align: -3px; margin-right: 6px; }
  .npc-save-card-hint { text-align: center; font-size: 0.7rem; color: #9CA3AF; margin-top: 10px; line-height: 1.4; }
  @keyframes npc-save-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
  @media (prefers-reduced-motion: reduce) {
    .npc-save-wrap, .npc-save-card, .npc-save-btn { transition: none; }
    .npc-save-btn .npc-save-dot { animation: none; }
  }
  @media (max-width: 640px) { .npc-save-wrap { bottom: 84px; right: 16px; } .npc-save-card { width: 280px; padding: 20px; } }
  @media (max-width: 360px) { .npc-save-card { width: 260px; right: -8px; } }
</style>

<div class="npc-save-wrap" id="npcSaveWrap">
  <button class="npc-save-btn" id="npcSaveBtn" aria-label="Save contact info">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" /></svg>
    <span class="npc-save-dot"></span>
  </button>
  <div class="npc-save-card" id="npcSaveCard">
    <button class="npc-save-card-close" id="npcSaveDismiss" aria-label="Dismiss">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" /></svg>
    </button>
    <div class="npc-save-card-profile">
      <img class="npc-save-card-avatar" src="https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png" alt="Chris Woods" width="48" height="48" loading="lazy">
      <div>
        <div class="npc-save-card-name">Chris Woods, NP</div>
        <div class="npc-save-card-title">NPCWoods Telemedicine</div>
      </div>
    </div>
    <div class="npc-save-card-msg"><strong>Not sick right now?</strong> Save my number for later — just search "sick guy" in your contacts when you need me.</div>
    <a class="npc-save-card-dl" id="npcSaveDownload" href="/chris-woods.vcf" download="Chris Woods - NPCWoods.vcf">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" /></svg>Save Contact
    </a>
    <div class="npc-save-card-hint">Saves to your phone contacts — search "sick guy" or "urgent care" anytime</div>
  </div>
</div>

<script>
(function() {
  var wrap = document.getElementById('npcSaveWrap');
  var btn = document.getElementById('npcSaveBtn');
  var card = document.getElementById('npcSaveCard');
  var dismiss = document.getElementById('npcSaveDismiss');
  var dl = document.getElementById('npcSaveDownload');
  if (!wrap || !btn || !card) return;
  try { if (sessionStorage.getItem('npc-contact-dismissed') === '1') { wrap.classList.add('npc-save-hidden'); return; } } catch(e) {}
  var hasSeenExpanded = false;
  try { hasSeenExpanded = sessionStorage.getItem('npc-contact-seen') === '1'; } catch(e) {}
  setTimeout(function() {
    wrap.classList.add('npc-save-visible');
    if (!hasSeenExpanded) {
      setTimeout(function() {
        card.classList.add('npc-save-card-open');
        btn.style.opacity = '0';
        btn.style.pointerEvents = 'none';
        setTimeout(function() {
          card.classList.remove('npc-save-card-open');
          btn.style.opacity = '1';
          btn.style.pointerEvents = 'auto';
          try { sessionStorage.setItem('npc-contact-seen', '1'); } catch(e) {}
        }, 5000);
      }, 200);
    }
  }, 3000);
  btn.addEventListener('click', function() {
    card.classList.add('npc-save-card-open');
    btn.style.opacity = '0';
    btn.style.pointerEvents = 'none';
  });
  dismiss.addEventListener('click', function() {
    card.classList.remove('npc-save-card-open');
    wrap.classList.remove('npc-save-visible');
    try { sessionStorage.setItem('npc-contact-dismissed', '1'); } catch(e) {}
    setTimeout(function() { wrap.classList.add('npc-save-hidden'); }, 400);
  });
  document.addEventListener('click', function(e) {
    if (card.classList.contains('npc-save-card-open') && !wrap.contains(e.target)) {
      card.classList.remove('npc-save-card-open');
      btn.style.opacity = '1';
      btn.style.pointerEvents = 'auto';
    }
  });
  dl.addEventListener('click', function() {
    if (typeof gtag === 'function') { gtag('event', 'generate_lead', { event_category: 'engagement', event_label: 'save_contact_vcard', value: 0 }); }
    if (typeof fbq === 'function') { fbq('track', 'Lead', { content_name: 'save_contact_vcard' }); }
  });
})();
</script>
<!-- END NPCWoods Contact Save -->
        <?php
    }
}
