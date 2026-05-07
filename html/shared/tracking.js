/**
 * NPCWoods Tracking — Canonical lead-intent events
 *
 * This file should emit neutral site events only. Let GTM / GA4 / Google Ads
 * decide which downstream events count as conversions.
 */
(function () {
  'use strict';

  var EVENT_VALUE = 59;

  // --- GCLID Capture ---
  // Grab gclid from URL and store in sessionStorage
  var params = new URLSearchParams(window.location.search);
  var gclid = params.get('gclid');
  if (gclid) {
    try { sessionStorage.setItem('npc_gclid', gclid); } catch (e) {}
  } else {
    try { gclid = sessionStorage.getItem('npc_gclid'); } catch (e) {}
  }

  // --- UTM Source Detection ---
  var utmSource = params.get('utm_source') || '';
  var isFromGoogle = utmSource.toLowerCase() === 'google' || !!gclid;

  // --- SMS Link Enhancement ---
  // Append attribution info to SMS body text on all sms: links
  function enhanceSmsLinks() {
    var links = document.querySelectorAll('a[href^="sms:"]');
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var href = link.getAttribute('href');

      // Only modify links that have a ?body= parameter
      if (href.indexOf('?body=') === -1 && href.indexOf('&body=') === -1) continue;

      // Parse the existing body
      var parts = href.split('?');
      if (parts.length < 2) continue;
      var number = parts[0];
      var queryStr = parts.slice(1).join('?');
      var bodyParams = new URLSearchParams(queryStr);
      var body = bodyParams.get('body') || '';

      // Append attribution tags
      var tags = [];
      if (gclid) tags.push('(gclid:' + gclid + ')');
      if (isFromGoogle) tags.push('(from Google)');

      if (tags.length > 0) {
        body = body + ' ' + tags.join(' ');
        bodyParams.set('body', body);
        link.setAttribute('href', number + '?' + bodyParams.toString());
      }
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceSmsLinks);
  } else {
    enhanceSmsLinks();
  }

  function baseEventParams(target) {
    return {
      event_category: 'engagement',
      event_label: target.getAttribute('href'),
      value: EVENT_VALUE,
      currency: 'USD',
      transport_type: 'beacon',
      page_path: window.location.pathname,
      gclid: gclid || ''
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

    if (typeof gtag === 'function') {
      // Use sendBeacon transport to prevent data loss on navigation.
      gtag('event', eventName, baseEventParams(target));
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
})();
