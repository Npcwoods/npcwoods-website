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
    var fbclid = cleanRef(params.get('fbclid'));
    var source = cleanTag(params.get('utm_source')) || (clickId ? 'google' : (fbclid ? 'facebook' : cleanTag(referrer.source)));
    var medium = cleanTag(params.get('utm_medium')) || (clickId ? 'cpc' : (fbclid ? 'paid_social' : cleanTag(referrer.medium)));
    var campaign = cleanTag(params.get('utm_campaign'));
    var content = cleanTag(params.get('utm_content'));
    var term = cleanTag(params.get('utm_term'));

    var hasNewSignal = !!(clickId || fbclid || source || medium || campaign || content || term || referrer.referrer);
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
        fbclid: fbclid,
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
  var fbclid = touchValue(attribution, 'fbclid');

  window.NPCWoodsAttribution = attribution;

  // --- UTM Source Detection ---
  var source = touchValue(attribution, 'source');
  var medium = touchValue(attribution, 'medium');
  var isFromGoogle = source.toLowerCase() === 'google' || !!touchValue(attribution, 'click_id');

  // --- sms_click_source derivation (added 2026-05-28) ---
  // Distinguishes paid vs organic at the conversion-event level so Google Ads, Facebook Ads,
  // and organic SMS clicks are cleanly separable in GA4 + Stripe/Spruce reconciliation.
  // Only paid-click identifiers count as paid — a referral from facebook.com without fbclid
  // is still organic (someone shared the link, no ad spend behind it).
  var smsClickSource = 'organic';
  if (gclid) {
    smsClickSource = 'google';
  } else if (fbclid) {
    smsClickSource = 'facebook';
  }

  function smsBodyForAttribution(existingBody) {
    var body = String(existingBody || '').trim();
    var strippedBody = body
      .replace(/\s*\((src|med|cmp|ad|from Google):?[^)]*\)/gi, '')
      .replace(/\s*\(adref:[^)]*\)/gi, '')
      .replace(/\s*\(from ad\)/gi, '')
      .replace(/\s+/g, ' ')
      .trim();
    var genericBody = !strippedBody
      || /^hi (chris|npcwoods),? i('d| would)? like to (start|ask about) a \$59/i.test(strippedBody)
      || /^hi,? i think i have a uti\.?$/i.test(strippedBody);

    if (!genericBody) {
      return strippedBody;
    }

    if (gclid || (source === 'google' && /^(cpc|paid|paid-search|ppc)$/i.test(medium))) {
      return 'Hi NPCWoods, I need help starting a $59 text visit.';
    }
    if (fbclid || (source === 'facebook' && /^(paid-social|paid_social|cpc|paid)$/i.test(medium))) {
      return 'Hi! I have a question and want to start a $59 text visit.';
    }
    if (source === 'facebook' || source === 'instagram' || source === 'threads') {
      return 'Hi Chris! I saw your page and need to start a $59 text visit.';
    }
    if (source === 'google' || source === 'bing') {
      return "Hi NPCWoods, I'd like to start a $59 text visit.";
    }
    return "Hi NPCWoods, I'd like to get started.";
  }

  function buildSmsHref(number, bodyParams, body) {
    bodyParams.delete('body');
    var extra = bodyParams.toString();
    return number + '?' + (extra ? extra + '&' : '') + 'body=' + encodeURIComponent(body);
  }

  // --- SMS Link Enhancement ---
  // Ensure every sms: link has a clean, human-looking ?body=.
  // Attribution stays in analytics event parameters; the patient-facing SMS
  // uses sentence families instead of raw source tags.
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
      var body = smsBodyForAttribution(bodyParams.get('body') || '');
      link.setAttribute('href', buildSmsHref(number, bodyParams, body));
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
      fbclid: fbclid || '',
      sms_click_source: smsClickSource,
      traffic_source: source || '',
      traffic_medium: medium || '',
      traffic_campaign: touchValue(attribution, 'campaign')
    };
  }

  // --- CTA Click Event Tracking ---
  // Event delegation on document for all SMS and tel links
  document.addEventListener('click', function (e) {
    var target = e.target.closest('a[href^="sms:"], a[href^="tel:"]');
    if (!target) return;

    var href = target.getAttribute('href') || '';
    var isSmsClick = href.indexOf('sms:') === 0;
    var eventName = isSmsClick ? 'sms_click' : 'phone_call_click';
    var eventParams = baseEventParams(target);

    if (typeof gtag === 'function') {
      // Single send to the page-configured destinations (GA4 G-EFFRQMG8TC +
      // Ads AW-610222919). Deduped 2026-06-10: removed the secondary send_to
      // loop that re-fired the same sms_click to unconfigured GA4 IDs.
      gtag('event', eventName, eventParams);
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
