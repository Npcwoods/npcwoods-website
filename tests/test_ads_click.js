const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const scriptPath = path.resolve(__dirname, '../html/shared/ads-click.js');

function run({ search = '', protocol = 'https:', fetchImpl }) {
  const posts = [];
  const cookies = [];
  const links = [];

  function makeSmsLink() {
    const link = {
      href: 'sms:+14806394722?body=' + encodeURIComponent("Hi Chris, I'd like to start a $59 visit"),
      className: 'cta',
      addEventListener(type, fn) {
        if (type === 'click') this._onClick = fn;
      },
      click() {
        if (this._onClick) this._onClick({ preventDefault() {} });
      },
    };
    links.push(link);
    return link;
  }

  makeSmsLink();

  const context = {
    URL,
    URLSearchParams,
    Date,
    Math,
    JSON,
    encodeURIComponent,
    console,
    fetch: fetchImpl || (async (url, opts) => {
      posts.push({ url, opts });
      return { ok: true };
    }),
    window: {
      location: {
        search,
        protocol,
        hostname: 'npcwoods.com',
        pathname: '/start-uti/',
        href: 'https://npcwoods.com/start-uti/' + search,
      },
      addEventListener(type, fn) {
        if (type === 'DOMContentLoaded') fn();
      },
    },
    document: {
      cookie: '',
      readyState: 'complete',
      querySelectorAll(selector) {
        return selector.includes('sms:') ? links : [];
      },
      addEventListener() {},
    },
  };
  Object.defineProperty(context.document, 'cookie', {
    get() {
      return cookies.map((c) => c.split(';')[0]).join('; ');
    },
    set(value) {
      cookies.push(String(value));
    },
  });
  context.window.window = context.window;
  context.window.document = context.document;
  context.document.cookie;
  context.globalThis = context.window;

  const code = fs.readFileSync(scriptPath, 'utf8');
  vm.runInNewContext(code, context);
  return { context, posts, cookies, links };
}

const cases = [
  {
    name: 'stores gclid in a first-party cookie',
    run() {
      const { cookies } = run({ search: '?gclid=TESTGCLID123' });
      const joined = cookies.join('\n');
      assert(joined.includes('npc_gclid=TESTGCLID123'), joined);
      assert(joined.includes('Max-Age=7776000'), joined);
      assert(joined.includes('SameSite=Lax'), joined);
      assert(joined.includes('Secure'), joined);
      assert(!joined.toLowerCase().includes('uti'), 'cookie leaked condition');
      assert(!joined.includes('/start-uti'), 'cookie leaked path');
    },
  },
  {
    name: 'sms click mints a 6-char ref and $59 body',
    run() {
      const { links, posts } = run({ search: '?gclid=TESTGCLID123' });
      links[0].click();
      const body = new URL(links[0].href).searchParams.get('body');
      const match = body.match(/^Hi Chris, I'd like to start a \$59 visit\. Ref: ([A-Z0-9]{6})$/);
      assert(match, body);
      assert.strictEqual(posts.length, 1);
      const payload = JSON.parse(posts[0].opts.body);
      assert.strictEqual(payload.gclid, 'TESTGCLID123');
      assert.strictEqual(payload.ref, match[1]);
      assert.ok(payload.ts);
      assert.strictEqual(Object.keys(payload).sort().join(','), 'gbraid,gclid,ref,ts,wbraid');
      assert(!JSON.stringify(payload).toLowerCase().includes('uti'));
      assert(!JSON.stringify(payload).includes('480'));
      assert(!JSON.stringify(payload).includes('/start-uti'));
    },
  },
  {
    name: 'does not post a diagnosis or phone',
    run() {
      const { links, posts } = run({ search: '?gclid=AAA&gbraid=BBB&wbraid=CCC' });
      links[0].click();
      const payload = JSON.parse(posts[0].opts.body);
      assert.strictEqual(payload.gclid, 'AAA');
      assert.strictEqual(payload.gbraid, 'BBB');
      assert.strictEqual(payload.wbraid, 'CCC');
    },
  },
];

for (const testCase of cases) {
  testCase.run();
  console.log('ok', testCase.name);
}
console.log(`ok ${cases.length} ads-click cases`);
