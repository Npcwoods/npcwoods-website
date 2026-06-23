const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const root = path.resolve(__dirname, '..');
const trackingFiles = [
  'html/shared/tracking.js',
  'html/tracking.js',
];

function runCase(script, { search = '', referrer = '', initialBody = "Hi Chris, I'd like to start a $59 visit", paidSurface = false }) {
  const link = {
    href: 'sms:4806394722?body=' + encodeURIComponent(initialBody),
    getAttribute(name) {
      return name === 'href' ? this.href : '';
    },
    setAttribute(name, value) {
      if (name === 'href') this.href = value;
    },
  };
  const localStore = new Map();
  const context = {
    URL,
    URLSearchParams,
    Date,
    String,
    RegExp,
    encodeURIComponent,
    localStorage: {
      getItem(key) {
        return localStore.has(key) ? localStore.get(key) : null;
      },
      setItem(key, value) {
        localStore.set(key, value);
      },
      removeItem(key) {
        localStore.delete(key);
      },
    },
    window: {
      location: {
        search,
        pathname: '/uti-care/',
        hostname: 'npcwoods.com',
      },
      addEventListener() {},
      removeEventListener() {},
      scrollY: 0,
      pageYOffset: 0,
      innerHeight: 900,
    },
    document: {
      referrer,
      readyState: 'complete',
      documentElement: { scrollHeight: 2000 },
      querySelectorAll(selector) {
        return selector === 'a[href^="sms:"]' ? [link] : [];
      },
      addEventListener() {},
    },
    setTimeout() {},
  };
  if (paidSurface) {
    context.window.NPCWoodsPaidSurface = true;
  }
  context.window.window = context.window;
  context.window.document = context.document;
  context.window.localStorage = context.localStorage;
  context.globalThis = context.window;

  vm.runInNewContext(script, context);
  const body = new URL(link.href).searchParams.get('body');
  return { href: link.href, body };
}

const cases = [
  {
    name: 'google paid',
    input: { search: '?gclid=TEST_GCLID' },
    expected: 'Hi NPCWoods, I need help starting a $59 text visit.',
  },
  {
    name: 'facebook paid',
    input: { search: '?fbclid=TEST_FBCLID' },
    expected: 'Hi! I have a question and want to start a $59 text visit.',
  },
  {
    name: 'google organic',
    input: { referrer: 'https://www.google.com/search?q=npcwoods' },
    expected: "Hi NPCWoods, I'd like to start a $59 text visit.",
  },
  {
    name: 'facebook organic',
    input: { referrer: 'https://www.facebook.com/' },
    expected: 'Hi Chris! I saw your page and need to start a $59 text visit.',
  },
  {
    name: 'unknown direct',
    input: { initialBody: '' },
    expected: "Hi NPCWoods, I'd like to get started.",
  },
  {
    name: 'custom body is preserved without tags',
    input: { search: '?gclid=TEST_GCLID', initialBody: 'Hi Chris, I used the Arizona UTI checker and have a safety question. (src:google) (med:cpc) (from Google)' },
    expected: 'Hi Chris, I used the Arizona UTI checker and have a safety question.',
  },
  {
    name: 'ad UTI body becomes clean source sentence',
    input: { search: '?gclid=TEST_GCLID', initialBody: 'Hi, I think I have a UTI (from ad)' },
    expected: 'Hi NPCWoods, I need help starting a $59 text visit.',
  },
  {
    name: 'paid surface appends marker to rewritten google body',
    input: { search: '?gclid=TEST_GCLID', paidSurface: true },
    expected: 'Hi NPCWoods, I need help starting a $59 text visit. ->',
  },
  {
    name: 'paid surface appends marker to direct default body',
    input: { initialBody: '', paidSurface: true },
    expected: "Hi NPCWoods, I'd like to get started. ->",
  },
  {
    name: 'paid surface does not duplicate marker',
    input: { search: '?gclid=TEST_GCLID', paidSurface: true, initialBody: 'Hi NPCWoods, I need help starting a $59 text visit. ->' },
    expected: 'Hi NPCWoods, I need help starting a $59 text visit. ->',
  },
  {
    name: 'organic surface does not append marker',
    input: { search: '?gclid=TEST_GCLID', paidSurface: false },
    expected: 'Hi NPCWoods, I need help starting a $59 text visit.',
  },
];

for (const relPath of trackingFiles) {
  const script = fs.readFileSync(path.join(root, relPath), 'utf8');
  for (const testCase of cases) {
    const result = runCase(script, testCase.input);
    const label = `${relPath}: ${testCase.name}`;
    assert.strictEqual(result.body, testCase.expected, label);
    assert(!result.href.includes('(src:'), label + ' leaked src tag');
    assert(!result.href.includes('(med:'), label + ' leaked med tag');
    assert(!result.href.includes('(from%20Google)'), label + ' leaked Google tag');
    assert(!result.href.includes('+'), label + ' encoded spaces as pluses');
  }
}

console.log(`ok ${cases.length * trackingFiles.length} sms body sentence cases`);
