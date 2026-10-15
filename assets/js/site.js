/*
 * NPCWoods Site-Wide JavaScript
 * ==============================
 * Shared scripts for navigation, Core Web Vitals reporting,
 * save-contact widget, and fade-in animations.
 *
 * Usage: <script src="/assets/js/site.js" defer></script>
 *
 * Last updated: 2026-10-15 (menu moved to /assets/js/npc-menu.js)
 */


/* ============================================================
 * 1. NAVIGATION (Hamburger menu, slide-out panel, scroll shadow)
 * ============================================================ */

/* The header menu (hamburger slide-out panel + desktop dropdowns) lives in
 * ONE file: /assets/js/npc-menu.js. It renders the panel from a single
 * data list, so pasted page copies can no longer drift. Bump MENU_VER
 * when npc-menu.js changes (the versioned URL dodges the 31-day cache). */
(function() {
  var MENU_VER = '20261015';
  if (window.__npcMenuLoaded || !document.querySelector('.npc-nav')) return;
  var s = document.createElement('script');
  s.src = '/assets/js/npc-menu.js?v=' + MENU_VER;
  s.async = false;
  s.onerror = legacyNav;  // network hiccup: keep the pasted panel working
  (document.head || document.body).appendChild(s);

  function legacyNav() {
    var hamburger = document.getElementById('npcHamburger');
    var panel = document.getElementById('npcSlidePanel');
    var overlay = document.getElementById('npcOverlay');
    var panelClose = document.getElementById('npcPanelClose');
    if (!hamburger || !panel || !overlay || !panelClose) return;
    function openMenu() {
      panel.classList.add('active'); overlay.classList.add('active'); hamburger.classList.add('active');
      hamburger.setAttribute('aria-expanded', 'true');
      document.documentElement.style.overflow = 'hidden'; document.body.style.overflow = 'hidden';
      panelClose.focus();
    }
    function closeMenu() {
      panel.classList.remove('active'); overlay.classList.remove('active'); hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
      document.documentElement.style.overflow = ''; document.body.style.overflow = '';
      hamburger.focus();
    }
    hamburger.addEventListener('click', function() { panel.classList.contains('active') ? closeMenu() : openMenu(); });
    overlay.addEventListener('click', closeMenu);
    panelClose.addEventListener('click', closeMenu);
    document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && panel.classList.contains('active')) closeMenu(); });
  }
})();


/* ============================================================
 * 1.5 MOBILE NAV CTA ("Text · $59" pill in the top bar)
 * ------------------------------------------------------------
 * The desktop nav links (including the CTA) are hidden under
 * 1024px, leaving phones with no persistent way to text. Static
 * pages carry pasted copies of the header snippet, so the pill
 * is injected here instead of editing ~80 HTML files. The
 * matchMedia guard keeps it off desktop even if site.css is
 * served stale from cache. tracking.js enhances the sms: href
 * on DOMContentLoaded, after deferred scripts run.
 * ============================================================ */

(function() {
  if (!window.matchMedia || !window.matchMedia('(max-width: 1023px)').matches) return;
  var inner = document.querySelector('.npc-nav-inner');
  if (!inner || inner.querySelector('.npc-nav-cta-mobile')) return;
  var toggle = inner.querySelector('.npc-nav-toggle');
  if (!toggle) return;

  var cta = document.createElement('a');
  cta.className = 'npc-nav-cta-mobile';
  cta.setAttribute('href', 'sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit');
  cta.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>Text · $59';
  inner.insertBefore(cta, toggle);
})();


/* ============================================================
 * 2. SAVE CONTACT FLOATING WIDGET
 * ============================================================ */

(function() {
  var booted = false;
  function bootSaveContact() {
    if (booted) return;
    booted = true;
    bootSaveContactInner();
  }
  function scheduleSaveContact() {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(function () { bootSaveContact(); }, { timeout: 4000 });
    } else {
      setTimeout(bootSaveContact, 2500);
    }
  }
  if (document.readyState === 'complete') scheduleSaveContact();
  else window.addEventListener('load', scheduleSaveContact);

  function bootSaveContactInner() {
  var wrap = document.getElementById('npcSaveWrap');
  var btn = document.getElementById('npcSaveBtn');
  var card = document.getElementById('npcSaveCard');
  var dismiss = document.getElementById('npcSaveDismiss');
  var dl = document.getElementById('npcSaveDownload');

  if (!wrap || !btn || !card) return;

  // Check if dismissed this session
  try {
    if (sessionStorage.getItem('npc-contact-dismissed') === '1') {
      wrap.classList.add('npc-save-hidden');
      return;
    }
  } catch(e) {}

  var hasSeenExpanded = false;
  try { hasSeenExpanded = sessionStorage.getItem('npc-contact-seen') === '1'; } catch(e) {}

  // Show after 3 second delay
  setTimeout(function() {
    wrap.classList.add('npc-save-visible');

    // Auto-expand on first view, stay collapsed on subsequent pages
    if (!hasSeenExpanded) {
      setTimeout(function() {
        card.classList.add('npc-save-card-open');
        btn.style.opacity = '0';
        btn.style.pointerEvents = 'none';
        // Auto-collapse after 5 seconds
        setTimeout(function() {
          card.classList.remove('npc-save-card-open');
          btn.style.opacity = '1';
          btn.style.pointerEvents = 'auto';
          try { sessionStorage.setItem('npc-contact-seen', '1'); } catch(e) {}
        }, 5000);
      }, 200);
    }
  }, 3000);

  // Toggle on click
  btn.addEventListener('click', function() {
    card.classList.add('npc-save-card-open');
    btn.style.opacity = '0';
    btn.style.pointerEvents = 'none';
  });

  // Dismiss
  dismiss.addEventListener('click', function() {
    card.classList.remove('npc-save-card-open');
    wrap.classList.remove('npc-save-visible');
    try { sessionStorage.setItem('npc-contact-dismissed', '1'); } catch(e) {}
    setTimeout(function() { wrap.classList.add('npc-save-hidden'); }, 400);
  });

  // Close card when clicking outside
  document.addEventListener('click', function(e) {
    if (card.classList.contains('npc-save-card-open') && !wrap.contains(e.target)) {
      card.classList.remove('npc-save-card-open');
      btn.style.opacity = '1';
      btn.style.pointerEvents = 'auto';
    }
  });
  }

})();


/* ============================================================
 * 3. FADE-IN ANIMATION OBSERVER
 * ============================================================ */

(function() {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(function(el) { observer.observe(el); });
})();
