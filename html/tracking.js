/**
 * NPCWoods Tracking — Canonical lead-intent events
 *
 * This file should emit neutral site events only. Let GTM / GA4 / Google Ads
 * decide which downstream events count as conversions.
 */
(function () {
  'use strict';

  var EVENT_VALUE = 59;
  var ATTRIBUTION_TTL_MS = 90 * 24 * 60 * 60 * 1000;
  // These GA4 destinations were verified to emit sms_click on 2026-05-23.
  var GA4_EVENT_DESTINATIONS = ['G-EFFRQMG8TC', 'G-7HW238T9FM', 'G-0VCC0Z4FD7'];

  var params = new URLSearchParams(window.location.search);

  function cleanTag(value) {
    return String(value || '')
      .trim()
      .replace(/[^a-zA-Z0-9_.-]+/g, '-')
      .replace(/^[-_.]+|[-_.]+$/g, '')
      .slice(0, 80);
  }

  function cleanRef(value) {
    return String(value || '')
      .trim()
      .replace(/[^a-zA-Z0-9_.-]+/g, '')
      .slice(0, 180);
  }

  function storageGet(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || !parsed.expiresAt || Date.now() > parsed.expiresAt) {
        localStorage.removeItem(key);
        return null;
      }
      return parsed;
    } catch (e) {
      return null;
    }
  }

  function storageSet(key, value) {
    try {
      value.expiresAt = Date.now() + ATTRIBUTION_TTL_MS;
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {}
  }

  function inferReferrerSource() {
    if (!document.referrer) return {};
    try {
      var referrerHost = new URL(document.referrer).hostname.replace(/^www\./, '').toLowerCase();
      if (!referrerHost || referrerHost === window.location.hostname.replace(/^www\./, '').toLowerCase()) return {};

      var source = referrerHost.split('.')[0] || referrerHost;
      var medium = 'referral';
      if (/(^|\.)google\./.test(referrerHost)) {
        source = 'google';
        medium = 'organic';
      } else if (/(^|\.)bing\./.test(referrerHost)) {
        source = 'bing';
        medium = 'organic';
      } else if (/(facebook|fb|instagram|threads)\./.test(referrerHost)) {
        source = referrerHost.indexOf('instagram') !== -1 ? 'instagram' : 'facebook';
        medium = 'social';
      }
      return { source: source, medium: medium, referrer: referrerHost };
    } catch (e) {
      return {};
    }
  }

  function captureAttribution() {
    var referrer = inferReferrerSource();
    var clickId = cleanRef(params.get('gclid') || params.get('gbraid') || params.get('wbraid'));
    var clickIdType = params.get('gclid') ? 'gclid' : (params.get('gbraid') ? 'gbraid' : (params.get('wbraid') ? 'wbraid' : ''));
    var source = cleanTag(params.get('utm_source')) || (clickId ? 'google' : cleanTag(referrer.source));
    var medium = cleanTag(params.get('utm_medium')) || (clickId ? 'cpc' : cleanTag(referrer.medium));
    var campaign = cleanTag(params.get('utm_campaign'));
    var content = cleanTag(params.get('utm_content'));
    var term = cleanTag(params.get('utm_term'));

    var hasNewSignal = !!(clickId || source || medium || campaign || content || term || referrer.referrer);
    var firstTouch = storageGet('npc_attribution_first');
    var lastTouch = storageGet('npc_attribution_last');

    if (hasNewSignal) {
      var touch = {
        source: source || 'unknown',
        medium: medium || 'unknown',
        campaign: campaign || '',
        content: content || '',
        term: term || '',
        click_id: clickId,
        click_id_type: clickIdType,
        referrer: cleanTag(referrer.referrer),
        landing_path: window.location.pathname,
        captured_at: new Date().toISOString()
      };
      if (!firstTouch) {
        storageSet('npc_attribution_first', touch);
        firstTouch = touch;
      }
      storageSet('npc_attribution_last', touch);
      lastTouch = touch;
    }

    return lastTouch || firstTouch || {};
  }

  function touchValue(touch, key) {
    return touch && touch[key] ? String(touch[key]) : '';
  }

  // --- GCLID + UTM Capture ---
  // Store ad attribution for 90 days so SMS taps and later /pay/ visits keep a readable trail.
  var attribution = captureAttribution();
  var gclid = touchValue(attribution, 'click_id_type') === 'gclid' ? touchValue(attribution, 'click_id') : '';

  window.NPCWoodsAttribution = attribution;

  // --- UTM Source Detection ---
  var source = touchValue(attribution, 'source');
  var medium = touchValue(attribution, 'medium');
  var isFromGoogle = source.toLowerCase() === 'google' || !!touchValue(attribution, 'click_id');

  // --- SMS Link Enhancement ---
  // Ensure every sms: link has a ?body= and append attribution tags.
  //
  // Why: Many pages historically used bare href="sms:4806394722". In that case,
  // we still want a readable attribution trail (gclid/from Google/etc) to be
  // present in the prefilled SMS body.
  function enhanceSmsLinks() {
    var links = document.querySelectorAll('a[href^="sms:"]');
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var href = link.getAttribute('href') || '';
      if (!href) continue;

      var qmark = href.indexOf('?');
      var number = qmark === -1 ? href : href.slice(0, qmark);
      var queryStr = qmark === -1 ? '' : href.slice(qmark + 1);
      var bodyParams = new URLSearchParams(queryStr);
      var body = bodyParams.get('body') || '';

      // If the link has no body, add a sensible default so attribution tags
      // have a place to live.
      if (!body) {
        body = "Hi Chris, I'd like to start a $59 visit";
      }

      // Append attribution tags
      var tags = [];
      if (source && body.indexOf('(src:') === -1) tags.push('(src:' + cleanTag(source) + ')');
      if (medium && body.indexOf('(med:') === -1) tags.push('(med:' + cleanTag(medium) + ')');
      if (touchValue(attribution, 'campaign') && body.indexOf('(cmp:') === -1) tags.push('(cmp:' + cleanTag(touchValue(attribution, 'campaign')) + ')');
      if (touchValue(attribution, 'content') && body.indexOf('(ad:') === -1) tags.push('(ad:' + cleanTag(touchValue(attribution, 'content')) + ')');
      if (touchValue(attribution, 'click_id') && body.indexOf('(adref:') === -1) {
        tags.push('(adref:' + cleanTag(touchValue(attribution, 'click_id_type') || 'click') + ':' + cleanRef(touchValue(attribution, 'click_id')) + ')');
      }
      if (isFromGoogle && body.indexOf('(from Google)') === -1) tags.push('(from Google)');

      if (tags.length > 0) body = (body + ' ' + tags.join(' ')).trim();
      bodyParams.set('body', body);
      link.setAttribute('href', number + '?' + bodyParams.toString());
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceSmsLinks);
  } else {
    enhanceSmsLinks();
  }

  function safeInteractionLabel(target) {
    var href = target.getAttribute('href') || '';
    if (href.indexOf('sms:') === 0) return 'sms_cta_click';
    if (href.indexOf('tel:') === 0) return 'phone_cta_click';
    return 'cta_click';
  }

  function baseEventParams(target) {
    return {
      event_category: 'engagement',
      event_label: safeInteractionLabel(target),
      value: EVENT_VALUE,
      currency: 'USD',
      transport_type: 'beacon',
      page_path: window.location.pathname,
      gclid: gclid || '',
      traffic_source: source || '',
      traffic_medium: medium || '',
      traffic_campaign: touchValue(attribution, 'campaign')
    };
  }

  function sendGa4LeadIntentEvent(eventName, params) {
    if (typeof gtag !== 'function') return;

    for (var i = 0; i < GA4_EVENT_DESTINATIONS.length; i++) {
      var ga4Params = {};
      for (var key in params) {
        if (Object.prototype.hasOwnProperty.call(params, key)) {
          ga4Params[key] = params[key];
        }
      }
      ga4Params.send_to = GA4_EVENT_DESTINATIONS[i];
      gtag('event', eventName, ga4Params);
    }
  }

  // --- Desktop-to-Mobile SMS Bridge ---
  function isDesktopDevice() {
    var userAgentCheck = !/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    return userAgentCheck && window.innerWidth > 768;
  }

  var activeModal = null;

  function injectBridgeStyles() {
    if (document.getElementById('npc-sms-bridge-styles')) return;
    var style = document.createElement('style');
    style.id = 'npc-sms-bridge-styles';
    style.textContent = `
      .npc-sms-bridge-modal {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: 100000;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      }
      .npc-sms-bridge-modal.active {
        opacity: 1;
        pointer-events: auto;
      }
      .npc-sms-bridge-backdrop {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(26, 26, 46, 0.65);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
      }
      .npc-sms-bridge-card {
        position: relative;
        background: #FAF8F5;
        color: #2A2A2A;
        width: 90%;
        max-width: 440px;
        padding: 36px 32px;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.5);
        transform: translateY(20px);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 10;
        text-align: center;
      }
      .npc-sms-bridge-modal.active .npc-sms-bridge-card {
        transform: translateY(0);
      }
      .npc-sms-bridge-close {
        position: absolute;
        top: 16px;
        right: 18px;
        background: none;
        border: none;
        font-size: 24px;
        color: #8E8E9A;
        cursor: pointer;
        line-height: 1;
        padding: 4px;
        transition: color 0.2s;
      }
      .npc-sms-bridge-close:hover {
        color: #2A2A2A;
      }
      .npc-sms-bridge-title {
        font-family: 'DM Serif Display', serif;
        font-size: 24px;
        color: #2563EB;
        margin: 0 0 8px;
        font-weight: 400;
        line-height: 1.2;
      }
      .npc-sms-bridge-subtitle {
        font-size: 14px;
        color: #4A4A5A;
        line-height: 1.5;
        margin: 0 0 24px;
      }
      .npc-sms-bridge-qr-container {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 16px;
        display: inline-block;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        margin-bottom: 24px;
        border: 1px solid #E5E7EB;
      }
      .npc-sms-bridge-qr {
        display: block;
        width: 160px;
        height: 160px;
      }
      .npc-sms-bridge-phone-box {
        background: #EFF6FF;
        border: 1px solid #DBEAFE;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
      }
      .npc-sms-bridge-phone-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #2563EB;
        font-weight: 600;
        margin-bottom: 4px;
      }
      .npc-sms-bridge-phone-number {
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #1D4ED8;
      }
      .npc-sms-bridge-msg-box {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px 16px;
        text-align: left;
        margin-bottom: 24px;
        position: relative;
      }
      .npc-sms-bridge-msg-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #8E8E9A;
        font-weight: 600;
        margin-bottom: 4px;
      }
      .npc-sms-bridge-msg-text {
        font-size: 13px;
        color: #2A2A2A;
        line-height: 1.4;
        word-break: break-word;
        padding-right: 64px;
      }
      .npc-sms-bridge-copy-btn {
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        background: #2563EB;
        border: none;
        border-radius: 8px;
        color: #FFFFFF;
        cursor: pointer;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 600;
        transition: background 0.2s, transform 0.1s;
      }
      .npc-sms-bridge-copy-btn:hover {
        background: #1D4ED8;
      }
      .npc-sms-bridge-copy-btn:active {
        transform: translateY(-50%) scale(0.95);
      }
      .npc-sms-bridge-copy-btn.copied {
        background: #16A34A;
      }
      .npc-sms-bridge-footer {
        font-size: 11px;
        color: #8E8E9A;
        line-height: 1.4;
      }
    `;
    document.head.appendChild(style);
  }

  function showSmsBridgeModal(link) {
    injectBridgeStyles();
    
    var href = link.getAttribute('href') || '';
    if (!href) return;

    var qmark = href.indexOf('?');
    var number = qmark === -1 ? href.replace('sms:', '') : href.slice(0, qmark).replace('sms:', '');
    var queryStr = qmark === -1 ? '' : href.slice(qmark + 1);
    var bodyParams = new URLSearchParams(queryStr);
    var body = bodyParams.get('body') || "Hi Chris, I'd like to start a $59 visit";

    // Format phone number nicely for display: (480) 639-4722
    var formattedPhone = "(480) 639-4722";
    if (number.length === 10) {
      formattedPhone = '(' + number.slice(0,3) + ') ' + number.slice(3,6) + '-' + number.slice(6);
    } else if (number.length === 11 && number.indexOf('1') === 0) {
      formattedPhone = '(' + number.slice(1,4) + ') ' + number.slice(4,7) + '-' + number.slice(7);
    }

    var modalId = 'npcSmsBridgeModal';
    var modal = document.getElementById(modalId);
    if (!modal) {
      modal = document.createElement('div');
      modal.id = modalId;
      modal.className = 'npc-sms-bridge-modal';
      modal.innerHTML = `
        <div class="npc-sms-bridge-backdrop"></div>
        <div class="npc-sms-bridge-card">
          <button class="npc-sms-bridge-close" aria-label="Close modal">&times;</button>
          <h3 class="npc-sms-bridge-title">Prefer to text from your phone?</h3>
          <p class="npc-sms-bridge-subtitle">Scan this QR code with your camera to open Messages instantly, or text us manually below.</p>
          <div class="npc-sms-bridge-qr-container">
            <img class="npc-sms-bridge-qr" src="" alt="Scan to text">
          </div>
          <div class="npc-sms-bridge-phone-box">
            <div class="npc-sms-bridge-phone-label">Text Chris at</div>
            <div class="npc-sms-bridge-phone-number"></div>
          </div>
          <div class="npc-sms-bridge-msg-box">
            <div class="npc-sms-bridge-msg-label">Prefilled Message</div>
            <div class="npc-sms-bridge-msg-text"></div>
            <button class="npc-sms-bridge-copy-btn">Copy</button>
          </div>
          <div class="npc-sms-bridge-footer">
            🔒 HIPAA compliant setup. No personal info is stored or processed.
          </div>
        </div>
      `;
      document.body.appendChild(modal);

      var closeBtn = modal.querySelector('.npc-sms-bridge-close');
      var backdrop = modal.querySelector('.npc-sms-bridge-backdrop');
      closeBtn.addEventListener('click', closeSmsBridgeModal);
      backdrop.addEventListener('click', closeSmsBridgeModal);
    }

    var qrImg = modal.querySelector('.npc-sms-bridge-qr');
    var phoneNumEl = modal.querySelector('.npc-sms-bridge-phone-number');
    var msgTextEl = modal.querySelector('.npc-sms-bridge-msg-text');
    var copyBtn = modal.querySelector('.npc-sms-bridge-copy-btn');

    // Secure, anonymous QR code generation (no patient identifiers are ever sent)
    var qrData = href;
    qrImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=' + encodeURIComponent(qrData);
    phoneNumEl.textContent = formattedPhone;
    msgTextEl.textContent = body;

    copyBtn.className = 'npc-sms-bridge-copy-btn';
    copyBtn.textContent = 'Copy';
    copyBtn.onclick = function() {
      navigator.clipboard.writeText(body).then(function() {
        copyBtn.textContent = 'Copied!';
        copyBtn.className = 'npc-sms-bridge-copy-btn copied';
        setTimeout(function() {
          copyBtn.textContent = 'Copy';
          copyBtn.className = 'npc-sms-bridge-copy-btn';
        }, 2000);
      });
    };

    modal.classList.add('active');
    activeModal = modal;
  }

  function closeSmsBridgeModal() {
    if (activeModal) {
      activeModal.classList.remove('active');
      activeModal = null;
    }
  }

  // Handle ESC key to close modal
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeSmsBridgeModal();
    }
  });

  // --- CTA Click Event Tracking ---
  // Event delegation on document for all SMS and tel links
  document.addEventListener('click', function (e) {
    var target = e.target.closest('a[href^="sms:"], a[href^="tel:"]');
    if (!target) return;

    var href = target.getAttribute('href') || '';
    var isSmsClick = href.indexOf('sms:') === 0;
    
    // Desktop SMS click interception
    if (isSmsClick && isDesktopDevice()) {
      e.preventDefault();
      showSmsBridgeModal(target);
    }

    var eventName = isSmsClick ? 'sms_click' : 'phone_call_click';
    var eventParams = baseEventParams(target);

    if (typeof gtag === 'function') {
      // Use sendBeacon transport to prevent data loss on navigation.
      gtag('event', eventName, eventParams);
      sendGa4LeadIntentEvent(eventName, eventParams);
    }

    if (isSmsClick && typeof fbq === 'function') {
      fbq('track', 'Lead', {
        value: EVENT_VALUE,
        currency: 'USD'
      });
    }
  });

  // --- Mid-funnel engagement events (added 2026-04-21) ---
  // scroll_75: fires once per page view when user reaches 75% page depth.
  // time_on_page_30s: fires once at 30s after page load if still on page.
  // Both give GA4 attribution model mid-funnel touchpoints to credit,
  // so paid / organic channels aren't all single-touch.
  var scrolled75 = false;
  function checkScroll75() {
    if (scrolled75) return;
    var docHeight = document.documentElement.scrollHeight;
    if (docHeight <= 0) return;
    var viewBottom = (window.scrollY || window.pageYOffset || 0) + window.innerHeight;
    if (viewBottom / docHeight >= 0.75) {
      scrolled75 = true;
      window.removeEventListener('scroll', checkScroll75);
      if (typeof gtag === 'function') {
        gtag('event', 'scroll_75', {
          event_category: 'engagement',
          page_path: window.location.pathname,
          transport_type: 'beacon'
        });
      }
    }
  }
  window.addEventListener('scroll', checkScroll75, { passive: true });

  setTimeout(function () {
    if (typeof gtag === 'function') {
      gtag('event', 'time_on_page_30s', {
        event_category: 'engagement',
        page_path: window.location.pathname,
        transport_type: 'beacon'
      });
    }
  }, 30000);

  // --- Custom Engagement Listeners (pricing, faq, pharmacy) ---
  if (window.location.pathname.indexOf('/pharmacy') !== -1) {
    if (typeof gtag === 'function') {
      gtag('event', 'pharmacy_page_viewed', {
        event_category: 'engagement',
        page_path: window.location.pathname,
        trigger_type: 'page_view',
        transport_type: 'beacon'
      });
    }
  }

  document.addEventListener('click', function (e) {
    var faqTarget = e.target.closest('.faq-question');
    if (faqTarget) {
      var questionText = (faqTarget.textContent || faqTarget.innerText || '').trim();
      if (typeof gtag === 'function') {
        gtag('event', 'faq_expanded', {
          event_category: 'engagement',
          faq_question: questionText,
          page_path: window.location.pathname,
          transport_type: 'beacon'
        });
      }
    }

    var linkTarget = e.target.closest('a');
    if (linkTarget) {
      var href = linkTarget.getAttribute('href') || '';
      
      if (href.indexOf('pricing') !== -1) {
        if (typeof gtag === 'function') {
          gtag('event', 'pricing_viewed', {
            event_category: 'engagement',
            page_path: window.location.pathname,
            link_url: href,
            transport_type: 'beacon'
          });
        }
      }

      if (href.indexOf('/pharmacy') !== -1) {
        if (typeof gtag === 'function') {
          gtag('event', 'pharmacy_page_viewed', {
            event_category: 'engagement',
            page_path: window.location.pathname,
            link_url: href,
            trigger_type: 'click',
            transport_type: 'beacon'
          });
        }
      }
    }
  });
})();
