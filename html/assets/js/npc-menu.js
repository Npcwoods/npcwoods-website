/*
 * NPCWoods shared site menu — the ONE source for the header menu.
 * ================================================================
 * Builds the mobile/tablet slide-out panel and normalizes the desktop
 * "Conditions" / "States" dropdowns on every page that carries the
 * shared `.npc-nav` header. Pages used to paste their own copy of the
 * panel markup and drifted (different Florida links, credential lines,
 * subtitles). This file replaces any pasted panel at runtime, so edit
 * the MENU data below — not page HTML — to change menu links or copy.
 *
 * Loaded by /assets/js/site.js (§1) or directly:
 *   <script src="/assets/js/npc-menu.js?v=20261015" defer></script>
 * Safe to load twice (guarded). No tracking. No third-party requests.
 *
 * Copy rules: no medication names, no banned words. Credential line is
 * always "MSN, APRN, FNP-C, AGACNP-BC".
 * Last updated: 2026-10-15
 */
(function () {
  'use strict';
  if (window.__npcMenuLoaded) return;
  window.__npcMenuLoaded = true;

  var SITE = 'https://npcwoods.com';
  var SMS = 'sms:4806394722?body=Hi%20Chris%2C%20I%27d%20like%20to%20start%20a%20%2459%20visit';
  var HEADSHOT = SITE + '/wp-content/uploads/2026/04/chris-woods-headshot-160.webp';
  var CRED = 'MSN, APRN, FNP-C, AGACNP-BC';

  // ---- Menu data (single source) ------------------------------------
  var MENU = {
    care: [
      ['/how-it-works/', 'How it works', '3 simple steps to care'],
      ['/pricing/', 'Pricing', '$59 flat fee, one price, one promise'],
      ['/learn/', 'After your visit', 'Patient education library']
    ],
    conditions: [
      ['/uti-treatment/', 'UTI treatment'],
      ['/sinus-infection-treatment/', 'Sinus infection'],
      ['/dental-pain/', 'Dental pain'],
      ['/ear-infection-treatment/', 'Ear infection'],
      ['/ed-treatment/', 'ED treatment']
    ],
    allConditions: ['/conditions/', 'All conditions', 'Full list of what we treat'],
    states: [
      ['/arizona-telemedicine/', 'Arizona'],
      ['/colorado-telemedicine/', 'Colorado'],
      ['/georgia-telemedicine/', 'Georgia'],
      ['/idaho-telemedicine/', 'Idaho'],
      ['/iowa-telemedicine/', 'Iowa'],
      ['/montana-telemedicine/', 'Montana'],
      ['/nevada-telemedicine/', 'Nevada'],
      ['/new-mexico-telemedicine/', 'New Mexico'],
      ['/north-carolina-telemedicine/', 'North Carolina'],
      ['/oregon-telemedicine/', 'Oregon'],
      ['/utah-telemedicine/', 'Utah'],
      ['/washington-telemedicine/', 'Washington'],
      ['/florida-vacation-sick-text-visit/', 'Florida', '(telehealth reg.)']
    ],
    about: [
      ['/about/', 'About Chris', CRED + ', double board-certified'],
      ['/credentials/', 'Credentials', 'NPI, board cert, 12 states + FL telehealth reg.'],
      ['/blog/', 'Blog', 'Health tips &amp; insights']
    ]
  };

  // ---- Styles (travel with the script so CSS and JS never mismatch) --
  var CSS = [
    /* hamburger: 44px target, shown below 1024px */
    'html.npcm-ready .npc-nav .npc-nav-toggle{box-sizing:border-box;min-width:44px;min-height:44px;width:44px;height:44px;padding:0;align-items:center;justify-content:center;gap:5px;flex-direction:column;flex-shrink:0;border-radius:12px;cursor:pointer;-webkit-tap-highlight-color:transparent}',
    'html.npcm-ready .npc-nav .npc-nav-toggle:focus-visible{outline:3px solid #007AFF;outline-offset:2px}',
    '@media (max-width:1023px){html.npcm-ready .npc-nav .npc-nav-links{display:none!important}html.npcm-ready .npc-nav .npc-nav-toggle{display:flex!important}}',
    '@media (min-width:1024px){html.npcm-ready .npc-nav .npc-nav-toggle{display:none!important}}',
    '@media (min-width:1024px) and (max-width:1199px){html.npcm-ready .npc-nav .npc-nav-links{gap:2px}html.npcm-ready .npc-nav .npc-nav-links>li>a{padding:8px 10px}html.npcm-ready .npc-nav .npc-nav-cta{padding:10px 14px}}',
    'html.npcm-ready .npc-nav .npc-nav-links>li>a{white-space:nowrap}',
    'html.npcm-ready .npc-nav .npc-nav-logo{flex-shrink:0}',

    /* desktop dropdowns: card style */
    'html.npcm-ready .npc-nav .npc-nav-links>li.npcm-has-dd{position:relative}',
    'html.npcm-ready .npc-nav .npc-nav-links>li.npcm-has-dd>a .nav-arrow{display:inline-block;transition:transform .18s ease}',
    'html.npcm-ready .npc-nav .npc-nav-links>li.npcm-has-dd.npcm-dd-open>a .nav-arrow{transform:rotate(180deg)}',
    'html.npcm-ready .npc-nav .npc-nav-links>li>.npc-dropdown{display:block;position:absolute;top:calc(100% + 10px);left:-6px;margin:0;min-width:248px;padding:8px;box-sizing:border-box;background:#fff;border:1px solid rgba(15,23,42,.08);border-radius:16px;box-shadow:0 22px 48px -14px rgba(15,23,42,.28),0 4px 14px rgba(15,23,42,.06);opacity:0;visibility:hidden;transform:translateY(-6px);transition:opacity .16s ease,transform .16s ease,visibility 0s linear .16s;z-index:10003;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-align:left}',
    'html.npcm-ready .npc-nav .npc-nav-links>li>.npc-dropdown::before{content:"";position:absolute;left:0;right:0;top:-14px;height:14px}',
    'html.npcm-ready .npc-nav .npc-nav-links>li.npcm-dd-open>.npc-dropdown{opacity:1;visibility:visible;transform:none;transition-delay:0s}',
    'html.npcm-ready .npc-nav .npc-dropdown .npcm-dd-label{display:block;padding:8px 12px 6px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5B6170;-webkit-text-fill-color:#5B6170}',
    'html.npcm-ready .npc-nav .npc-dropdown a{display:flex;align-items:center;gap:6px;min-height:40px;padding:9px 12px;margin:0;border-radius:10px;font-size:14.5px;font-weight:500;line-height:1.25;color:#1A1A2E;-webkit-text-fill-color:#1A1A2E;text-decoration:none;background:transparent;white-space:nowrap;transition:background .12s ease,color .12s ease}',
    'html.npcm-ready .npc-nav .npc-dropdown a:hover,html.npcm-ready .npc-nav .npc-dropdown a:focus-visible{background:#EEF5FF;color:#0058C4;-webkit-text-fill-color:#0058C4}',
    'html.npcm-ready .npc-nav .npc-dropdown a:focus-visible{outline:2px solid #007AFF;outline-offset:-2px}',
    'html.npcm-ready .npc-nav .npc-dropdown a[aria-current="page"]{background:#F3F6FB;font-weight:600}',
    'html.npcm-ready .npc-nav .npc-dropdown a small{font-size:12px;font-weight:500;color:#5B6170;-webkit-text-fill-color:#5B6170}',
    'html.npcm-ready .npc-nav .npc-dropdown .npcm-dd-sep{height:1px;margin:6px 8px;background:#EEF0F4}',
    'html.npcm-ready .npc-nav .npc-dropdown a.npcm-dd-all{font-weight:600;color:#0058C4;-webkit-text-fill-color:#0058C4}',
    'html.npcm-ready .npc-nav .npc-nav-links>li>.npc-dropdown.npcm-dd-states{min-width:352px}',
    'html.npcm-ready .npc-nav .npc-dropdown .npcm-dd-grid{display:grid;grid-template-columns:1fr 1fr;gap:2px}',
    'html.npcm-ready .npc-nav .npc-dropdown .npcm-dd-grid a.npcm-wide{grid-column:1/-1}',

    /* overlay + panel */
    '.npcm-overlay{position:fixed;inset:0;z-index:2147483000;background:rgba(10,12,20,.46);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);opacity:0;visibility:hidden;transition:opacity .28s ease,visibility 0s linear .28s}',
    '.npcm-overlay.npcm-on{opacity:1;visibility:visible;transition-delay:0s}',
    '.npcm-panel{position:fixed;top:0;right:0;bottom:0;z-index:2147483001;width:min(400px,calc(100vw - 28px));height:100%;height:100dvh;display:flex;flex-direction:column;box-sizing:border-box;background:#fff;color:#1A1A2E;border-radius:22px 0 0 22px;box-shadow:-24px 0 60px -12px rgba(10,12,20,.35);transform:translateX(105%);visibility:hidden;transition:transform .32s cubic-bezier(.22,1,.36,1),visibility 0s linear .32s;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased;text-align:left;line-height:1.35;overscroll-behavior:contain}',
    '.npcm-panel.npcm-on{transform:none;visibility:visible;transition-delay:0s}',
    '.npcm-panel *,.npcm-panel *::before,.npcm-panel *::after{box-sizing:border-box}',
    '.npcm-panel a{text-decoration:none}',
    '.npcm-head{display:flex;align-items:center;gap:12px;padding:16px 14px 14px 18px;padding-top:max(16px,env(safe-area-inset-top));border-bottom:1px solid #EEF0F4;flex-shrink:0}',
    '.npcm-avatar{width:44px;height:44px;border-radius:50%;object-fit:cover;flex-shrink:0;box-shadow:0 0 0 2px #fff,0 0 0 3px #DCE6F5}',
    '.npcm-who{flex:1;min-width:0}',
    '.npcm-name{margin:0;font-size:16px;font-weight:700;color:#1A1A2E;-webkit-text-fill-color:#1A1A2E;line-height:1.2}',
    '.npcm-cred{margin-top:3px;font-size:12px;font-weight:500;color:#5B6170;-webkit-text-fill-color:#5B6170;letter-spacing:.01em}',
    '.npcm-close{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;min-width:48px;margin:0;padding:0;border:0;border-radius:14px;background:#F3F4F7;color:#1A1A2E;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:background .15s ease}',
    '.npcm-close:hover{background:#E8EBF0}',
    '.npcm-close svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round}',
    '.npcm-body{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;padding:6px 12px 16px}',
    '.npcm-sec{padding:12px 0 8px;border-top:1px solid #EEF0F4}',
    '.npcm-sec:first-child{border-top:0}',
    '.npcm-label{margin:0;padding:4px 8px 8px;font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#5B6170;-webkit-text-fill-color:#5B6170;line-height:1.2}',
    '.npcm-list{list-style:none;margin:0;padding:0}',
    '.npcm-list li{margin:0;padding:0}',
    '.npcm-row{display:flex;align-items:center;gap:10px;min-height:48px;padding:8px 10px;border-radius:12px;color:#1A1A2E;-webkit-text-fill-color:#1A1A2E;transition:background .12s ease}',
    '.npcm-row:hover,.npcm-row:active{background:#F2F7FF}',
    '.npcm-row[aria-current="page"]{background:#F3F6FB}',
    '.npcm-row-text{flex:1;min-width:0;display:flex;flex-direction:column}',
    '.npcm-row-t{font-size:16px;font-weight:600;line-height:1.25}',
    '.npcm-row-s{margin-top:2px;font-size:13px;font-weight:400;color:#5B6170;-webkit-text-fill-color:#5B6170;line-height:1.3}',
    '.npcm-chev{width:16px;height:16px;flex-shrink:0;stroke:#9AA3B2;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}',
    '.npcm-chips{list-style:none;margin:0;padding:0 2px;display:grid;grid-template-columns:1fr 1fr;gap:8px}',
    '.npcm-chips li{margin:0;padding:0;min-width:0}',
    '.npcm-chips li.npcm-wide{grid-column:1/-1}',
    '.npcm-chip{display:flex;align-items:center;gap:6px;min-height:44px;height:100%;padding:8px 12px;border-radius:12px;background:#F5F7FB;border:1px solid #E4E9F1;font-size:14px;font-weight:600;color:#1A1A2E;-webkit-text-fill-color:#1A1A2E;line-height:1.2;transition:background .12s ease,border-color .12s ease}',
    '.npcm-chip:hover,.npcm-chip:active{background:#EAF3FF;border-color:#BBD6FA}',
    '.npcm-chip[aria-current="page"]{background:#EAF3FF;border-color:#7FB2F5}',
    '.npcm-chip small{font-size:12px;font-weight:500;color:#5B6170;-webkit-text-fill-color:#5B6170}',
    '.npcm-foot{flex-shrink:0;padding:12px 16px;padding-bottom:max(14px,env(safe-area-inset-bottom));border-top:1px solid #EEF0F4;background:#fff;border-radius:0 0 0 22px}',
    '.npcm-cta{display:flex;align-items:center;justify-content:center;gap:10px;min-height:56px;width:100%;padding:12px 18px;border-radius:16px;background:#007AFF;color:#fff;-webkit-text-fill-color:#fff;font-size:19px;font-weight:700;letter-spacing:-.01em;box-shadow:0 10px 24px -8px rgba(0,122,255,.55);transition:background .15s ease,transform .15s ease}',
    '.npcm-cta:hover{background:#006AE0}',
    '.npcm-cta:active{transform:scale(.985)}',
    '.npcm-cta svg{width:20px;height:20px;stroke:#fff;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}',
    '.npcm-note{margin:8px 0 0;text-align:center;font-size:12.5px;color:#5B6170;-webkit-text-fill-color:#5B6170}',
    '.npcm-panel a:focus-visible,.npcm-panel button:focus-visible{outline:3px solid #007AFF;outline-offset:2px}',
    '.npcm-panel .npcm-cta:focus-visible{outline-color:#1A1A2E}',
    'html.npcm-locked,html.npcm-locked body{overflow:hidden!important;overscroll-behavior:none}',
    '@media (prefers-reduced-motion:reduce){.npcm-panel,.npcm-overlay,html.npcm-ready .npc-nav .npc-nav-links>li>.npc-dropdown,html.npcm-ready .npc-nav .nav-arrow{transition:none!important}html.npcm-ready .npc-nav .npc-nav-links>li>.npc-dropdown{transform:none}}'
  ].join('\n');

  // ---- helpers -------------------------------------------------------
  var CHEV = '<svg class="npcm-chev" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><polyline points="9 18 15 12 9 6"/></svg>';
  var XICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
  var MSG = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>';

  function norm(p) { return (p || '/').replace(/\/+$/, '') + '/'; }
  var HERE = norm(location.pathname);
  function cur(path) { return norm(path) === HERE ? ' aria-current="page"' : ''; }
  function url(path) { return SITE + path; }

  function rowHTML(item) {
    return '<li><a class="npcm-row" href="' + url(item[0]) + '"' + cur(item[0]) + '>' +
      '<span class="npcm-row-text"><span class="npcm-row-t">' + item[1] + '</span>' +
      (item[2] ? '<span class="npcm-row-s">' + item[2] + '</span>' : '') +
      '</span>' + CHEV + '</a></li>';
  }
  function section(label, id, inner) {
    return '<section class="npcm-sec" aria-labelledby="' + id + '"><h2 class="npcm-label" id="' + id + '">' + label + '</h2>' + inner + '</section>';
  }

  function panelHTML() {
    var conds = MENU.conditions.map(function (c) { return rowHTML(c); }).join('') + rowHTML(MENU.allConditions);
    var chips = MENU.states.map(function (s) {
      return '<li' + (s[2] ? ' class="npcm-wide"' : '') + '><a class="npcm-chip" href="' + url(s[0]) + '"' + cur(s[0]) + '>' +
        s[1] + (s[2] ? ' <small>' + s[2] + '</small>' : '') + '</a></li>';
    }).join('');
    return '' +
      '<div class="npcm-head">' +
        '<img class="npcm-avatar" src="' + HEADSHOT + '" alt="Chris Woods" width="44" height="44" decoding="async">' +
        '<div class="npcm-who"><p class="npcm-name" id="npcmTitle">Chris Woods</p><div class="npcm-cred">' + CRED + '</div></div>' +
        '<button type="button" class="npcm-close" aria-label="Close menu">' + XICON + '</button>' +
      '</div>' +
      '<nav class="npcm-body" aria-label="Site menu">' +
        section('Get care', 'npcmCare', '<ul class="npcm-list">' + MENU.care.map(rowHTML).join('') + '</ul>') +
        section('Conditions', 'npcmCond', '<ul class="npcm-list">' + conds + '</ul>') +
        section('States we serve', 'npcmStates', '<ul class="npcm-chips">' + chips + '</ul>') +
        section('About', 'npcmAbout', '<ul class="npcm-list">' + MENU.about.map(rowHTML).join('') + '</ul>') +
      '</nav>' +
      '<div class="npcm-foot">' +
        '<a class="npcm-cta" href="' + SMS + '">' + MSG + 'Text Chris · $59</a>' +
        '<p class="npcm-note">(480) 639-4722 · Not a chatbot</p>' +
      '</div>';
  }

  function ddConditionsHTML() {
    return '<span class="npcm-dd-label" aria-hidden="true">Conditions we treat</span>' +
      MENU.conditions.map(function (c) { return '<a href="' + url(c[0]) + '"' + cur(c[0]) + '>' + c[1] + '</a>'; }).join('') +
      '<div class="npcm-dd-sep" aria-hidden="true"></div>' +
      '<a class="npcm-dd-all" href="' + url(MENU.allConditions[0]) + '">View all conditions</a>';
  }
  function ddStatesHTML() {
    return '<span class="npcm-dd-label" aria-hidden="true">12 state licenses + FL telehealth reg.</span><div class="npcm-dd-grid">' +
      MENU.states.map(function (s) {
        return '<a' + (s[2] ? ' class="npcm-wide"' : '') + ' href="' + url(s[0]) + '"' + cur(s[0]) + '>' + s[1] + (s[2] ? ' <small>' + s[2] + '</small>' : '') + '</a>';
      }).join('') + '</div>';
  }

  function focusables(root) {
    return Array.prototype.filter.call(
      root.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])'),
      function (el) { return el.offsetWidth > 0 || el.offsetHeight > 0 || el.getClientRects().length > 0; });
  }

  // ---- init ----------------------------------------------------------
  function init() {
    var nav = document.querySelector('.npc-nav');
    if (!nav) return;

    if (!document.getElementById('npcm-css')) {
      var st = document.createElement('style');
      st.id = 'npcm-css';
      st.textContent = CSS;
      (document.head || document.documentElement).appendChild(st);
    }
    document.documentElement.classList.add('npcm-ready');

    // scroll shadow
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', (window.scrollY || window.pageYOffset) > 10);
    }, { passive: true });

    setupDropdowns(nav);
    setupPanel(nav);
  }

  // ---- desktop dropdowns ---------------------------------------------
  function setupDropdowns(nav) {
    var lis = nav.querySelectorAll('.npc-nav-links > li');
    var all = [];
    var lastPointer = 'mouse';
    var lastPointerAt = 0;
    document.addEventListener('pointerdown', function (e) { lastPointer = e.pointerType || 'mouse'; lastPointerAt = Date.now(); }, true);
    document.addEventListener('keydown', function () { lastPointerAt = 0; }, true);

    Array.prototype.forEach.call(lis, function (li, i) {
      var dd = li.querySelector('.npc-dropdown');
      var trig = li.querySelector('a');
      if (!dd || !trig) return;
      var label = (trig.textContent || '').trim().toLowerCase();
      if (label.indexOf('states') === 0) { dd.innerHTML = ddStatesHTML(); dd.classList.add('npcm-dd-states'); }
      else if (label.indexOf('conditions') === 0) { dd.innerHTML = ddConditionsHTML(); }
      li.classList.add('npcm-has-dd');
      dd.id = dd.id || ('npcmDD' + i);
      trig.setAttribute('aria-haspopup', 'true');
      trig.setAttribute('aria-expanded', 'false');
      trig.setAttribute('aria-controls', dd.id);
      var state = { li: li, dd: dd, trig: trig, toggleOnly: /^#/.test(trig.getAttribute('href') || '#'), t: null };
      all.push(state);

      function open() { closeAll(state); clearTimeout(state.t); li.classList.add('npcm-dd-open'); trig.setAttribute('aria-expanded', 'true'); }
      function close() { clearTimeout(state.t); li.classList.remove('npcm-dd-open'); trig.setAttribute('aria-expanded', 'false'); }
      state.open = open; state.close = close;

      li.addEventListener('mouseenter', function (e) { if (lastPointer === 'mouse') open(); });
      li.addEventListener('mouseleave', function () {
        if (lastPointer !== 'mouse') return;
        state.t = setTimeout(close, 140);
      });
      // Keyboard focus opens the menu; a tap/click focus is handled by the click below.
      li.addEventListener('focusin', function () { if (Date.now() - lastPointerAt > 700) open(); });
      li.addEventListener('focusout', function (e) {
        if (!li.contains(e.relatedTarget)) close();
      });
      trig.addEventListener('click', function (e) {
        var isOpen = li.classList.contains('npcm-dd-open');
        if (state.toggleOnly) {
          e.preventDefault();
          if (!isOpen) open();
          else if (lastPointer !== 'mouse' || e.detail === 0) close();
          return;
        }
        // Touch: first tap opens, second tap follows the link.
        if (lastPointer !== 'mouse' && !isOpen) { e.preventDefault(); open(); }
      });
      trig.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') {
          e.preventDefault(); open();
          var f = dd.querySelector('a'); if (f) f.focus();
        } else if ((e.key === ' ' || e.key === 'Spacebar') && state.toggleOnly) {
          e.preventDefault(); li.classList.contains('npcm-dd-open') ? close() : open();
        }
      });
      dd.addEventListener('keydown', function (e) {
        var items = Array.prototype.slice.call(dd.querySelectorAll('a'));
        var idx = items.indexOf(document.activeElement);
        if (e.key === 'ArrowDown') { e.preventDefault(); (items[idx + 1] || items[0]).focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); idx <= 0 ? trig.focus() : items[idx - 1].focus(); }
      });
    });

    function closeAll(except) { all.forEach(function (s) { if (s !== except) s.close(); }); }
    document.addEventListener('click', function (e) {
      all.forEach(function (s) { if (!s.li.contains(e.target)) s.close(); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      all.forEach(function (s) {
        if (s.li.classList.contains('npcm-dd-open')) {
          var hadFocus = s.li.contains(document.activeElement);
          s.close();
          if (hadFocus) {
            // keep it closed while focus sits on the trigger
            s.trig.focus();
            s.close();
          }
        }
      });
    });
  }

  // ---- slide-out panel -----------------------------------------------
  function setupPanel(nav) {
    var oldBtn = document.getElementById('npcHamburger') || nav.querySelector('.npc-nav-toggle');
    if (!oldBtn) return;

    // Drop pasted legacy panels so only this one exists.
    ['npcSlidePanel', 'npcOverlay'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el && el.parentNode) el.parentNode.removeChild(el);
    });

    // Clone the button to shed any legacy inline listeners.
    var btn = oldBtn.cloneNode(true);
    oldBtn.parentNode.replaceChild(btn, oldBtn);
    btn.id = 'npcHamburger';
    btn.type = 'button';
    btn.classList.remove('active');
    btn.setAttribute('aria-label', 'Open menu');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'npcMenu');
    btn.setAttribute('aria-haspopup', 'dialog');

    var overlay = document.createElement('div');
    overlay.className = 'npcm-overlay';
    overlay.id = 'npcmOverlay';
    overlay.setAttribute('aria-hidden', 'true');

    var panel = document.createElement('div');
    panel.className = 'npcm-panel';
    panel.id = 'npcMenu';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-labelledby', 'npcmTitle');
    panel.setAttribute('aria-hidden', 'true');
    panel.setAttribute('inert', '');
    panel.innerHTML = panelHTML();

    document.body.appendChild(overlay);
    document.body.appendChild(panel);

    var closeBtn = panel.querySelector('.npcm-close');
    var isOpen = false;

    function lock() {
      var sw = window.innerWidth - document.documentElement.clientWidth;
      document.documentElement.classList.add('npcm-locked');
      if (sw > 0) document.body.style.paddingRight = sw + 'px';
    }
    function unlock() {
      document.documentElement.classList.remove('npcm-locked');
      document.body.style.paddingRight = '';
    }

    function openMenu() {
      if (isOpen) return;
      isOpen = true;
      panel.removeAttribute('inert');
      panel.setAttribute('aria-hidden', 'false');
      panel.classList.add('npcm-on');
      overlay.classList.add('npcm-on');
      btn.setAttribute('aria-expanded', 'true');
      lock();
      // focus after the frame so the transition starts cleanly
      setTimeout(function () { try { closeBtn.focus({ preventScroll: true }); } catch (e) { closeBtn.focus(); } }, 30);
    }
    function closeMenu(restoreFocus) {
      if (!isOpen) return;
      isOpen = false;
      panel.classList.remove('npcm-on');
      overlay.classList.remove('npcm-on');
      panel.setAttribute('aria-hidden', 'true');
      panel.setAttribute('inert', '');
      btn.setAttribute('aria-expanded', 'false');
      unlock();
      if (restoreFocus !== false) { try { btn.focus({ preventScroll: true }); } catch (e) { btn.focus(); } }
    }
    window.npcMenu = { open: openMenu, close: closeMenu };

    btn.addEventListener('click', function (e) { e.preventDefault(); isOpen ? closeMenu() : openMenu(); });
    overlay.addEventListener('click', function () { closeMenu(); });
    closeBtn.addEventListener('click', function () { closeMenu(); });
    panel.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (a) closeMenu(false);
    });
    // Lock background scroll: overflow:hidden on <html>/<body> plus a
    // wheel/touch guard for browsers (iOS Safari) that still scroll the page.
    var body = panel.querySelector('.npcm-body');
    function guard(e) {
      if (!isOpen) return;
      if (body.contains(e.target) && body.scrollHeight > body.clientHeight) return;
      if (e.cancelable) e.preventDefault();
    }
    document.addEventListener('wheel', guard, { passive: false });
    document.addEventListener('touchmove', guard, { passive: false });

    document.addEventListener('keydown', function (e) {
      if (!isOpen) return;
      if (e.key === 'Escape' || e.key === 'Esc') { e.preventDefault(); closeMenu(); return; }
      if (e.key === 'Tab') {
        var f = focusables(panel);
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && (document.activeElement === first || !panel.contains(document.activeElement))) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && (document.activeElement === last || !panel.contains(document.activeElement))) { e.preventDefault(); first.focus(); }
      }
    });
    // Leaving the small-screen layout closes the panel.
    if (window.matchMedia) {
      var mq = window.matchMedia('(min-width: 1024px)');
      var onMQ = function (m) { if (m.matches) closeMenu(false); };
      if (mq.addEventListener) mq.addEventListener('change', onMQ); else if (mq.addListener) mq.addListener(onMQ);
    }
    // bfcache restore: never come back with the page locked
    window.addEventListener('pageshow', function () { if (!isOpen) unlock(); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
