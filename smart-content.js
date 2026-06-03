/**
 * NPCWoods Smart Content — Personalization Snippet
 * Version: 1.0.0 | 2026-05-31
 *
 * ┌─────────────────────────────────────────────────────┐
 * │ HIPAA COMPLIANCE STATEMENT                          │
 * ├─────────────────────────────────────────────────────┤
 * │ This script sends ONLY marketing data to the API:   │
 * │  - city slug       (from URL path, e.g. "mesa")     │
 * │  - condition slug  (from URL path, e.g. "uti")      │
 * │  - utm_source, utm_medium, utm_campaign             │
 * │  - page path       (e.g. "/uti-treatment/mesa-az/") │
 * │                                                     │
 * │ This script NEVER sends:                            │
 * │  - Patient names, phone numbers, or contact info    │
 * │  - SMS message content or clinical data             │
 * │  - Cookies, localStorage, or session identifiers    │
 * │  - IP addresses, fingerprints, or device info       │
 * │  - Any data from Spruce, Stripe, or clinical systems│
 * │  - Any personally identifiable information (PII)    │
 * └─────────────────────────────────────────────────────┘
 *
 * LOAD ORDER: Must load AFTER tracking.js, which sets
 * window.NPCWoodsAttribution with parsed UTM data.
 *
 * FAILURE BEHAVIOR: On ANY failure — network error, timeout,
 * bad JSON, matched:false, missing DOM elements — the static
 * page stays untouched. Railway is additive only.
 */
(function () {
  'use strict';

  // ====================================================================
  // CONFIGURATION
  // Change API_BASE when the Railway URL or custom domain changes.
  // ====================================================================
  var API_BASE = 'https://npc-smart-backend-production.up.railway.app';
  var TIMEOUT_MS = 2000;   // 2-second hard cutoff — if Railway is slow, bail
  var DEBUG = false;        // flip to true for console logging in dev

  // ====================================================================
  // CONDITION MAP
  // Every condition landing-page slug -> API condition key.
  // Update this list whenever a new condition page is added to the site.
  // ====================================================================
  var conditionMap = {
    'uti-treatment':               'uti',
    'uti-treatment-online':        'uti',
    'sinus-infection-treatment':   'sinus',
    'strep-throat-treatment':      'strep',
    'dental-pain':                 'dental',
    'ear-infection-treatment':     'ear-infection',
    'ed-treatment':                'ed',
    'glp1-weight-loss':            'glp1',
    'poison-ivy':                  'poison-ivy'
  };

  // ====================================================================
  // PATH EXTRACTION
  // Infer city and condition from the URL path.
  //   /uti-treatment/mesa-az/   -> condition = "uti",  city = "mesa"
  //   /dental-pain/             -> condition = "dental", city = null
  //   /arizona-telemedicine/    -> condition = null,    city = null
  // ====================================================================
  function extractFromPath(path) {
    var result = { city: null, condition: null };
    var segments = path.replace(/^\/|\/$/g, '').split('/');

    // First segment: condition slug lookup
    if (segments[0] && conditionMap[segments[0]]) {
      result.condition = conditionMap[segments[0]];
    }

    // Second segment: city slug — strip the two-letter state suffix
    //   "mesa-az"         -> "mesa"
    //   "albuquerque-nm"  -> "albuquerque"
    //   "murphy-nc"       -> "murphy"
    if (segments[1]) {
      result.city = segments[1].replace(/-[a-z]{2}$/, '');
    }

    return result;
  }

  // ====================================================================
  // QUERY STRING BUILDER (ES5-safe, no URLSearchParams dependency)
  // ====================================================================
  function buildQS(params) {
    var parts = [];
    for (var key in params) {
      if (params.hasOwnProperty(key) && params[key]) {
        parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(params[key]));
      }
    }
    return parts.length ? '?' + parts.join('&') : '';
  }

  function cleanSlug(value) {
    if (!value) return null;
    value = String(value).toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 50);
    return value || null;
  }

  function getQueryValue(name) {
    var query = window.location.search || '';
    if (query.charAt(0) === '?') query = query.slice(1);
    if (!query) return null;

    var parts = query.split('&');
    for (var i = 0; i < parts.length; i++) {
      var pair = parts[i].split('=');
      if (decodeURIComponent(pair[0] || '') === name) {
        return cleanSlug(decodeURIComponent((pair[1] || '').replace(/\+/g, ' ')));
      }
    }
    return null;
  }

  // ====================================================================
  // BUILD API URL
  // Combines path-derived slugs + tracking.js attribution into a
  // single GET request to the Railway personalization endpoint.
  // ====================================================================
  function buildApiUrl() {
    var path = window.location.pathname;
    var info = extractFromPath(path);

    info.city = getQueryValue('npc_city') || getQueryValue('city') || info.city;
    info.condition = getQueryValue('npc_condition') || getQueryValue('condition') || info.condition;

    // Read attribution from tracking.js (already parsed and stored)
    var attr = window.NPCWoodsAttribution || {};

    var q = {};
    if (info.city)       q.city      = info.city;
    if (info.condition)  q.condition = info.condition;
    if (attr.source)     q.source    = attr.source;
    if (attr.medium)     q.medium    = attr.medium;
    if (attr.campaign)   q.campaign  = attr.campaign;
    q.page = path;

    return API_BASE + '/api/personalize' + buildQS(q);
  }

  // ====================================================================
  // DOM HELPERS
  // ====================================================================
  function getEl(attrValue) {
    return document.querySelector('[data-npc-personalize="' + attrValue + '"]');
  }

  // ====================================================================
  // APPLY PERSONALIZATION
  // Swap Railway-provided content into DOM elements tagged with
  // data-npc-personalize attributes. If any element is missing,
  // that swap silently skips — no errors, no side effects.
  // ====================================================================
  function applyPersonalization(data) {
    if (!data || !data.meta || !data.meta.matched) {
      if (DEBUG) console.log('[NPC-Smart] No match — static page stays.');
      return;
    }

    // --- Headline (textContent, no HTML) ---
    var headlineEl = getEl('headline');
    if (headlineEl && data.headline) {
      headlineEl.textContent = data.headline;
    }

    // --- Sub-headline (textContent) ---
    var subEl = getEl('subheadline');
    if (subEl && data.subheadline) {
      subEl.textContent = data.subheadline;
    }

    // --- Trust badge (textContent) ---
    var badgeEl = getEl('trust-badge');
    if (badgeEl && data.trust_badge) {
      badgeEl.textContent = data.trust_badge;
    }

    // --- Social proof (innerHTML — may contain quotes/formatting) ---
    var proofEl = getEl('social-proof');
    if (proofEl && data.social_proof) {
      proofEl.innerHTML = data.social_proof;
    }

    // --- CTA button text ---
    // Multiple CTAs may exist (hero, final, mobile floating).
    // Each may contain an SVG icon child — we swap ONLY the text node,
    // leaving icons intact.
    if (data.cta_text) {
      var ctaEls = document.querySelectorAll('[data-npc-personalize="cta-text"]');
      for (var i = 0; i < ctaEls.length; i++) {
        var swapped = false;
        var nodes = ctaEls[i].childNodes;
        for (var j = 0; j < nodes.length; j++) {
          // nodeType 3 = Text node
          if (nodes[j].nodeType === 3 && nodes[j].textContent.trim()) {
            nodes[j].textContent = ' ' + data.cta_text + ' ';
            swapped = true;
            break;
          }
        }
        // Fallback: no SVG icon, just a plain text link (e.g. hero-cta)
        if (!swapped && ctaEls[i].children.length === 0) {
          ctaEls[i].textContent = data.cta_text;
        }
      }
    }

    // --- SMS body ---
    // Update the ?body= parameter in EVERY sms: link on the page.
    // This covers hero CTA, final CTA, mobile floating CTA, inline links.
    // Note: tracking.js enhanceSmsLinks() runs earlier on DOMContentLoaded;
    // our overwrite here is more specific (city + condition) and wins.
    if (data.sms_body) {
      var smsLinks = document.querySelectorAll('a[href^="sms:"]');
      for (var k = 0; k < smsLinks.length; k++) {
        var href = smsLinks[k].getAttribute('href') || '';
        var qmark = href.indexOf('?');
        var number = qmark === -1 ? href : href.slice(0, qmark);
        smsLinks[k].setAttribute(
          'href',
          number + '?body=' + encodeURIComponent(data.sms_body)
        );
      }
    }

    if (DEBUG) console.log('[NPC-Smart] Applied:', data.meta);
  }

  // ====================================================================
  // MAIN FETCH
  // Call Railway, apply on success, do nothing on any failure.
  // ====================================================================
  function fetchAndApply() {
    // Guard: bail if fetch API is not available (very old browsers)
    if (typeof fetch === 'undefined') {
      if (DEBUG) console.log('[NPC-Smart] fetch unavailable — skipping.');
      return;
    }

    var url = buildApiUrl();
    if (DEBUG) console.log('[NPC-Smart] Fetching:', url);

    // AbortController for timeout (with graceful fallback)
    var controller = (typeof AbortController !== 'undefined')
      ? new AbortController()
      : null;
    var signal = controller ? controller.signal : undefined;
    var timer = null;
    var timedOut = false;

    if (controller) {
      timer = setTimeout(function () { controller.abort(); }, TIMEOUT_MS);
    } else {
      // Browsers without AbortController: ignore late responses
      timer = setTimeout(function () { timedOut = true; }, TIMEOUT_MS);
    }

    fetch(url, {
      method: 'GET',
      signal: signal,
      headers: { 'Accept': 'application/json' }
    })
      .then(function (res) {
        clearTimeout(timer);
        if (timedOut) return;
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        if (timedOut) return;
        if (data) applyPersonalization(data);
      })
      .catch(function (err) {
        clearTimeout(timer);
        // Silent failure — the static page is already perfect
        if (DEBUG) console.warn('[NPC-Smart] Skipped:', err.message);
      });
  }

  // ====================================================================
  // INITIALIZATION
  // Wait for DOM ready + 50ms to ensure tracking.js has set
  // window.NPCWoodsAttribution before we read it.
  // ====================================================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(fetchAndApply, 50);
    });
  } else {
    setTimeout(fetchAndApply, 50);
  }

})();
