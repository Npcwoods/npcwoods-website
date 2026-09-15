/* NPCWoods first-party ads click helper.
   Stores gclid/gbraid/wbraid in first-party cookies only.
   On SMS tap: mints a random 6-char ref, rewrites the $59 body, POSTs
   {gclid,gbraid,wbraid,ref,ts} to /t/click. No Google. No Meta. No diagnosis. */
(function () {
  'use strict';
  if (window.NPCWoodsAdsClickReady) return;
  window.NPCWoodsAdsClickReady = true;
  window.NPCWoodsPaidSurface = true;

  var COOKIE_MAX_AGE = 90 * 24 * 60 * 60;
  var REF_CHARS = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
  var SMS_PREFIX = "Hi Chris, I'd like to start a $59 visit. Ref: ";

  function params() {
    try {
      return new URLSearchParams(window.location.search || '');
    } catch (e) {
      return new URLSearchParams();
    }
  }

  function cleanId(value) {
    return String(value || '').trim().replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 180);
  }

  function cookieSecure() {
    return window.location.protocol === 'https:' ? '; Secure' : '';
  }

  function writeCookie(name, value) {
    if (!value) return;
    document.cookie =
      name +
      '=' +
      value +
      '; Max-Age=' +
      COOKIE_MAX_AGE +
      '; Path=/; SameSite=Lax' +
      cookieSecure();
  }

  function readCookie(name) {
    var parts = String(document.cookie || '').split(';');
    var prefix = name + '=';
    for (var i = 0; i < parts.length; i++) {
      var part = parts[i].trim();
      if (part.indexOf(prefix) === 0) return cleanId(part.slice(prefix.length));
    }
    return '';
  }

  function mintRef() {
    var out = '';
    for (var i = 0; i < 6; i++) {
      out += REF_CHARS.charAt(Math.floor(Math.random() * REF_CHARS.length));
    }
    return out;
  }

  function captureClickIds() {
    var q = params();
    var gclid = cleanId(q.get('gclid'));
    var gbraid = cleanId(q.get('gbraid'));
    var wbraid = cleanId(q.get('wbraid'));
    writeCookie('npc_gclid', gclid);
    writeCookie('npc_gbraid', gbraid);
    writeCookie('npc_wbraid', wbraid);
    return {
      gclid: gclid || readCookie('npc_gclid'),
      gbraid: gbraid || readCookie('npc_gbraid'),
      wbraid: wbraid || readCookie('npc_wbraid'),
    };
  }

  function smsLinks() {
    return document.querySelectorAll('a[href^="sms:"]');
  }

  function rewriteHref(link, ref) {
    var body = SMS_PREFIX + ref;
    var href = 'sms:+14806394722?body=' + encodeURIComponent(body);
    link.href = href;
    link.setAttribute && link.setAttribute('href', href);
    return body;
  }

  function postClick(payload) {
    if (typeof fetch !== 'function') return;
    try {
      fetch('/t/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true,
      }).catch(function () {});
    } catch (e) {}
  }

  function onSmsClick(link) {
    var ids = captureClickIds();
    var ref = mintRef();
    rewriteHref(link, ref);
    postClick({
      gclid: ids.gclid || '',
      gbraid: ids.gbraid || '',
      wbraid: ids.wbraid || '',
      ref: ref,
      ts: Date.now(),
    });
  }

  function bind() {
    captureClickIds();
    var links = smsLinks();
    for (var i = 0; i < links.length; i++) {
      (function (link) {
        if (link._npcAdsBound) return;
        link._npcAdsBound = true;
        link.addEventListener('click', function () {
          onSmsClick(link);
        });
      })(links[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();
