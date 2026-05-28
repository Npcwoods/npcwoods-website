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
  var GA4_EVENT_DESTINATIONS = ['G-7HW238T9FM', 'G-0VCC0Z4FD7'];

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
