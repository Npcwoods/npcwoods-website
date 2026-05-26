/*
 * NPCWoods Site-Wide JavaScript
 * ==============================
 * Shared scripts for navigation, Core Web Vitals reporting,
 * save-contact widget, and fade-in animations.
 *
 * Usage: <script src="/assets/js/site.js" defer></script>
 *
 * Last updated: May 2026
 */


/* ============================================================
 * 1. NAVIGATION (Hamburger menu, slide-out panel, scroll shadow)
 * ============================================================ */

(function() {
  var hamburger = document.getElementById('npcHamburger');
  var panel = document.getElementById('npcSlidePanel');
  var overlay = document.getElementById('npcOverlay');
  var panelClose = document.getElementById('npcPanelClose');
  var nav = document.querySelector('.npc-nav');
  if (!hamburger || !panel || !overlay || !panelClose) return;

  // Scroll shadow effect
  if (nav) {
    window.addEventListener('scroll', function() {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

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


/* ============================================================
 * 2. CORE WEB VITALS REPORTER (sends LCP/CLS/INP/FCP/TTFB to GA4)
 * ============================================================ */

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


/* ============================================================
 * 3. SAVE CONTACT FLOATING WIDGET
 * ============================================================ */

(function() {
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

  // Track download
  dl.addEventListener('click', function() {
    // Google Analytics / Ads
    if (typeof gtag === 'function') {
      gtag('event', 'generate_lead', {
        event_category: 'engagement',
        event_label: 'save_contact_vcard',
        value: 0
      });
    }
    // Facebook Pixel
    if (typeof fbq === 'function') {
      fbq('track', 'Lead', { content_name: 'save_contact_vcard' });
    }
  });
})();


/* ============================================================
 * 4. FADE-IN ANIMATION OBSERVER
 * ============================================================ */

(function() {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(function(el) { observer.observe(el); });
})();
