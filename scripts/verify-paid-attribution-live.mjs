#!/usr/bin/env node
/**
 * Live paid-attribution verifier for NPCWoods paid landing pages.
 *
 * This is read-only with respect to money: it follows the browser redirect
 * only to the Stripe Checkout URL and inspects query params. It never
 * completes a payment.
 */
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(__filename), '..');
const FIXED_HQ_ROOT = '/Users/macmini/Desktop/Chris-HQ';
const HQ_ROOT = fs.existsSync(FIXED_HQ_ROOT) ? FIXED_HQ_ROOT : path.resolve(REPO_ROOT, '..');
const SITE = 'https://npcwoods.com';
const DEFAULT_TIMEOUT_MS = 60000;
const META_PIXEL_MARKERS = [
  'connect.facebook.net',
  'facebook.com/tr',
  'fbq("init"',
  "fbq('init'",
];

const DEFAULT_CASES = [
  {
    name: 'mesa-search-safe',
    url: `${SITE}/uti-treatment/mesa-az/search-safe/`,
    payState: 'AZ',
  },
  {
    name: 'uti-care-wnc-ga',
    url: `${SITE}/uti-care/`,
    payState: 'NC',
  },
];

function timestamp(now = new Date()) {
  return now.toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
}

function safeFileName(value) {
  return String(value || 'case')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_.-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80) || 'case';
}

function addClickId(rawUrl, clickId) {
  const url = new URL(rawUrl);
  url.searchParams.set('gclid', clickId);
  return url.toString();
}

function smsBodyFromHref(href) {
  const qmark = String(href || '').indexOf('?');
  if (qmark === -1) return '';
  return new URLSearchParams(String(href).slice(qmark + 1)).get('body') || '';
}

function expectedStripeReference(clickId) {
  return `google-cpc-manual-payment-gclid-${clickId}`;
}

function playwrightCliPath() {
  const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
  return process.env.PWCLI || path.join(codexHome, 'skills/playwright/scripts/playwright_cli.sh');
}

function parseCase(raw) {
  const parts = String(raw || '').split('|');
  if (parts.length < 2 || parts.length > 3) {
    throw new Error(`Invalid --case ${raw}. Use name|url or name|url|state.`);
  }
  return {
    name: parts[0].trim(),
    url: parts[1].trim(),
    payState: (parts[2] || 'AZ').trim(),
  };
}

function parseArgs(argv) {
  const args = {
    cases: [],
    headed: false,
    selfTest: false,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    outDir: '',
    clickPrefix: 'LIVE_VERIFY_ATTRIBUTION',
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--headed') {
      args.headed = true;
    } else if (arg === '--self-test') {
      args.selfTest = true;
    } else if (arg === '--case') {
      args.cases.push(parseCase(argv[++i]));
    } else if (arg === '--out-dir') {
      args.outDir = argv[++i];
    } else if (arg === '--timeout-ms') {
      args.timeoutMs = Number(argv[++i]);
    } else if (arg === '--click-prefix') {
      args.clickPrefix = argv[++i];
    } else if (arg === '--help' || arg === '-h') {
      args.help = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (!args.cases.length) args.cases = DEFAULT_CASES;
  if (!Number.isFinite(args.timeoutMs) || args.timeoutMs < 1000) {
    throw new Error('--timeout-ms must be a number >= 1000');
  }
  return args;
}

function usage() {
  return `Usage:
  node scripts/verify-paid-attribution-live.mjs
  node scripts/verify-paid-attribution-live.mjs --case "mesa|https://npcwoods.com/uti-treatment/mesa-az/search-safe/|AZ"

Checks each paid page for:
  - window.NPCWoodsPaidSurface === true
  - Google/CPC attribution capture from gclid
  - SMS body paid marker (->)
  - no Meta pixel markers
  - same-browser /pay handoff to Stripe with google-cpc client_reference_id
`;
}

function runSelfTest() {
  assert.equal(safeFileName('Mesa Search Safe!'), 'mesa-search-safe');
  assert.equal(
    addClickId('https://npcwoods.com/uti-care/?x=1', 'ABC123'),
    'https://npcwoods.com/uti-care/?x=1&gclid=ABC123',
  );
  assert.equal(smsBodyFromHref('sms:4806394722?body=Hi%20there%20-%3E'), 'Hi there ->');
  assert.equal(
    expectedStripeReference('CLICK123'),
    'google-cpc-manual-payment-gclid-CLICK123',
  );
  assert.deepEqual(parseCase('mesa|https://npcwoods.com/x/|AZ'), {
    name: 'mesa',
    url: 'https://npcwoods.com/x/',
    payState: 'AZ',
  });
  console.log('ok verify-paid-attribution-live self-test');
}

function parseCliJson(raw) {
  const text = String(raw || '').trim();
  const parsed = JSON.parse(text);
  return typeof parsed === 'string' ? JSON.parse(parsed) : parsed;
}

function runPwCli(session, cliArgs, options = {}) {
  const pwcli = playwrightCliPath();
  if (!fs.existsSync(pwcli)) {
    throw new Error(`Playwright CLI wrapper not found at ${pwcli}. Set PWCLI to the wrapper path.`);
  }
  return execFileSync(
    pwcli,
    ['--session', session, ...cliArgs],
    {
      cwd: REPO_ROOT,
      encoding: 'utf8',
      stdio: options.stdio || ['ignore', 'pipe', 'pipe'],
      timeout: options.timeoutMs || 120000,
    },
  );
}

function verifyCase(testCase, args, outDir) {
  const clickId = `${args.clickPrefix}_${safeFileName(testCase.name).toUpperCase()}_${timestamp()}`;
  const landingUrl = addClickId(testCase.url, clickId);
  const payUrl = `${new URL(testCase.url).origin}/pay/`;
  const session = `paid-attr-${process.pid}-${safeFileName(testCase.name)}-${Date.now()}`;
  const codePath = path.join(os.tmpdir(), `${session}.js`);
  const code = `async page => {
    const testCase = ${JSON.stringify(testCase)};
    const landingUrl = ${JSON.stringify(landingUrl)};
    const payUrl = ${JSON.stringify(payUrl)};
    const clickId = ${JSON.stringify(clickId)};
    const outDir = ${JSON.stringify(outDir)};
    const timeoutMs = ${JSON.stringify(args.timeoutMs)};
    const metaPixelMarkers = ${JSON.stringify(META_PIXEL_MARKERS)};
    const result = {
      ok: false,
      name: testCase.name,
      landingUrl,
      clickId,
      screenshots: []
    };

    function decodePart(value) {
      try {
        return decodeURIComponent(String(value || '').replace(/\\+/g, ' '));
      } catch (_error) {
        return String(value || '');
      }
    }

    function queryParamsFromUrl(raw) {
      const text = String(raw || '');
      const qmark = text.indexOf('?');
      if (qmark === -1) return {};
      const hash = text.indexOf('#', qmark);
      const query = text.slice(qmark + 1, hash === -1 ? undefined : hash);
      const out = {};
      for (const piece of query.split('&')) {
        if (!piece) continue;
        const equals = piece.indexOf('=');
        const key = decodePart(equals === -1 ? piece : piece.slice(0, equals));
        const value = decodePart(equals === -1 ? '' : piece.slice(equals + 1));
        if (key) out[key] = value;
      }
      return out;
    }

    function smsBodyFromHref(href) {
      const qmark = String(href || '').indexOf('?');
      if (qmark === -1) return '';
      return queryParamsFromUrl(String(href).slice(qmark)).body || '';
    }

    function expectedStripeReference(id) {
      return 'google-cpc-manual-payment-gclid-' + id;
    }

    function check(condition, message) {
      if (!condition) throw new Error(message);
    }

    try {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(landingUrl, { waitUntil: 'networkidle', timeout: timeoutMs });
      await page.waitForSelector('a[href^="sms:"]', { timeout: timeoutMs });

      const landingShot = outDir + '/' + testCase.name.replace(/[^a-zA-Z0-9_.-]+/g, '-').toLowerCase() + '-landing-mobile.png';
      await page.screenshot({ path: landingShot, fullPage: true });
      result.screenshots.push(landingShot);

      const state = await page.evaluate(() => {
        const scripts = Array.from(document.scripts).map(script => script.src || '');
        const sms = document.querySelector('a[href^="sms:"]');
        return {
          title: document.title,
          paidSurface: window.NPCWoodsPaidSurface === true,
          attribution: window.NPCWoodsAttribution || {},
          trackingScripts: scripts.filter(src => src.includes('/tracking.js')),
          smsHref: sms ? sms.getAttribute('href') || '' : '',
          html: document.documentElement.outerHTML,
        };
      });

      const smsBody = smsBodyFromHref(state.smsHref);
      const foundMetaMarkers = metaPixelMarkers.filter(marker =>
        state.html.toLowerCase().includes(marker.toLowerCase())
      );

      check(state.paidSurface === true, 'paid surface marker missing');
      check(state.attribution.source === 'google', 'landing source should be google');
      check(state.attribution.medium === 'cpc', 'landing medium should be cpc');
      check(state.attribution.click_id === clickId, 'landing click_id should match gclid');
      check(state.attribution.click_id_type === 'gclid', 'landing click_id_type should be gclid');
      check(state.trackingScripts.length > 0, 'tracking.js script missing');
      check(smsBody.includes('->'), 'SMS body missing paid marker');
      check(foundMetaMarkers.length === 0, 'Meta pixel marker present: ' + foundMetaMarkers.join(', '));

      await page.goto(payUrl, {
        waitUntil: 'domcontentloaded',
        timeout: timeoutMs,
      });
      await page.selectOption('#stateSelect', testCase.payState);
      await page.check('#chkLocation');
      await page.check('#chkFee');
      await page.check('#chkTerms');

      const stripeWait = page.waitForURL(url => String(url).startsWith('https://buy.stripe.com/'), {
        timeout: timeoutMs,
      });
      await page.click('#btnSubmit');
      await stripeWait;

      const stripeUrl = page.url();
      const stripeParams = queryParamsFromUrl(stripeUrl);
      check(stripeParams.utm_source === 'google', 'Stripe utm_source should be google');
      check(stripeParams.utm_medium === 'cpc', 'Stripe utm_medium should be cpc');
      check(stripeParams.gclid === clickId, 'Stripe gclid should match landing gclid');
      check(
        stripeParams.client_reference_id === expectedStripeReference(clickId),
        'Stripe client_reference_id should preserve Google click proof'
      );

      Object.assign(result, {
        ok: true,
        title: state.title,
        paidSurface: state.paidSurface,
        attribution: state.attribution,
        trackingScripts: state.trackingScripts,
        smsBody,
        stripeUrl,
        stripeParams,
      });
    } catch (error) {
      result.error = error && error.stack ? error.stack : String(error);
    }
    return JSON.stringify(result);
  }`;

  fs.writeFileSync(codePath, `${code}\n`);
  try {
    runPwCli(session, args.headed ? ['open', 'about:blank', '--headed'] : ['open', 'about:blank']);
    const raw = runPwCli(session, ['--raw', 'run-code', `--filename=${codePath}`], {
      timeoutMs: args.timeoutMs + 60000,
    });
    return parseCliJson(raw);
  } catch (error) {
    return {
      ok: false,
      name: testCase.name,
      landingUrl,
      clickId,
      error: error && error.stderr ? String(error.stderr) : (error && error.stack ? error.stack : String(error)),
      screenshots: [],
    };
  } finally {
    try {
      runPwCli(session, ['close'], { timeoutMs: 30000 });
    } catch (_error) {}
    try {
      fs.unlinkSync(codePath);
    } catch (_error) {}
  }
}

function writeReport(results, outDir) {
  const reportPath = path.join(outDir, 'verification-results.md');
  const lines = [
    '# Paid Attribution Live Verification',
    '',
    `Generated: ${new Date().toISOString()}`,
    '',
    'This proof stops at the Stripe Checkout URL. No payment was completed.',
    '',
    '| Case | Result | Landing URL | SMS body | Stripe client_reference_id | Screenshots |',
    '|---|---|---|---|---|---|',
  ];

  for (const result of results) {
    const smsBody = result.smsBody || '';
    const ref = result.stripeParams ? result.stripeParams.client_reference_id || '' : '';
    const shots = (result.screenshots || []).join('<br>') || 'none';
    lines.push(
      `| \`${result.name}\` | ${result.ok ? 'PASS' : 'FAIL'} | ${result.landingUrl} | ${smsBody.replaceAll('|', '\\|')} | ${ref.replaceAll('|', '\\|')} | ${shots.replaceAll('|', '\\|')} |`,
    );
  }

  const failures = results.filter((result) => !result.ok);
  if (failures.length) {
    lines.push('', '## Failures', '');
    for (const failure of failures) {
      lines.push(`### ${failure.name}`, '', '```text', failure.error || 'unknown error', '```', '');
    }
  }

  fs.writeFileSync(reportPath, `${lines.join('\n')}\n`);
  return reportPath;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return 0;
  }
  if (args.selfTest) {
    runSelfTest();
    return 0;
  }

  const outDir = args.outDir || path.join(
    HQ_ROOT,
    'content-output',
    'reports',
    `paid-attribution-live-verify-${timestamp().replace(/Z$/, '')}`,
  );
  fs.mkdirSync(outDir, { recursive: true });

  const results = [];
  for (const testCase of args.cases) {
    console.log(`[verify] ${testCase.name}: ${testCase.url}`);
    const result = verifyCase(testCase, args, outDir);
    results.push(result);
    console.log(`  ${result.ok ? 'PASS' : 'FAIL'} ${result.ok ? result.stripeParams.client_reference_id : result.error.split('\n')[0]}`);
  }

  const reportPath = writeReport(results, outDir);
  console.log(`[proof] ${reportPath}`);
  return results.every((result) => result.ok) ? 0 : 1;
}

main()
  .then((code) => {
    process.exitCode = code;
  })
  .catch((error) => {
    console.error(error && error.stack ? error.stack : error);
    process.exitCode = 1;
  });
