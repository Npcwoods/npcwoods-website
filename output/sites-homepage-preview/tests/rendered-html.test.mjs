import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

function withoutNonVisibleContent(markup) {
  return markup
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/<(script|style|template)\b[^>]*>[\s\S]*?<\/\1\s*>/gi, " ");
}

function decodeEntities(value) {
  const namedEntities = {
    amp: "&",
    apos: "'",
    gt: ">",
    ldquo: "\u201c",
    lt: "<",
    mdash: "\u2014",
    nbsp: " ",
    ndash: "\u2013",
    quot: '"',
    rdquo: "\u201d",
    rsquo: "\u2019",
  };

  return value
    .replace(/&#(\d+);/g, (entity, decimal) => {
      const codePoint = Number.parseInt(decimal, 10);
      return Number.isSafeInteger(codePoint) && codePoint <= 0x10ffff
        ? String.fromCodePoint(codePoint)
        : entity;
    })
    .replace(/&#x([\da-f]+);/gi, (entity, hexadecimal) => {
      const codePoint = Number.parseInt(hexadecimal, 16);
      return Number.isSafeInteger(codePoint) && codePoint <= 0x10ffff
        ? String.fromCodePoint(codePoint)
        : entity;
    })
    .replace(/&([a-z][a-z\d]+);/gi, (entity, name) =>
      Object.hasOwn(namedEntities, name.toLowerCase())
        ? namedEntities[name.toLowerCase()]
        : entity,
    );
}

function textContent(markup) {
  return decodeEntities(withoutNonVisibleContent(markup).replace(/<[^>]+>/g, " "))
    .replace(/\s+/g, " ")
    .trim();
}

function userFacingAttributeText(markup) {
  const visibleMarkup = withoutNonVisibleContent(markup);
  const values = [];
  const openingTags = visibleMarkup.matchAll(
    /<([a-z][\w:-]*)\b(?:[^>"']|"[^"]*"|'[^']*')*>/gi,
  );

  for (const match of openingTags) {
    const [openingTag, tagName] = match;
    const userFacingAttributes = openingTag.matchAll(
      /[\t\n\f\r ]+(?:aria-label|alt|title|placeholder)\s*=\s*(["'])(.*?)\1/gi,
    );
    for (const attribute of userFacingAttributes) values.push(attribute[2]);

    if (tagName.toLowerCase() === "meta") {
      const content = openingTag.match(
        /[\t\n\f\r ]+content\s*=\s*(["'])(.*?)\1/i,
      )?.[2];
      if (content !== undefined) values.push(content);
    }
  }

  return decodeEntities(values.join(" ")).replace(/\s+/g, " ").trim();
}

test("extracts decoded user-facing HTML without hidden runtime content", () => {
  const markup = `
    <meta content="NPCWoods &#35;1">
    <main aria-label="Text &#67;hris" title="Real &amp; local"
      data-title="doctor" data-alt="physician"
      data-placeholder="appointment" data-aria-label="insurance">
      &#82;&#x65;al relief &#x1f44b;
      <img alt="Chris &quot;Woods&quot;">
      <input placeholder="Tell us what&#x27;s going on">
    </main>
    <script>doctor</script>
    <style>.insurance { color: red; }</style>
    <template>appointment</template>
    <!-- physician -->
  `;
  const userFacingText = `${textContent(markup)} ${userFacingAttributeText(markup)}`;

  assert.match(userFacingText, /Real relief 👋/);
  assert.match(userFacingText, /NPCWoods #1/);
  assert.match(userFacingText, /Text Chris/);
  assert.match(userFacingText, /Real & local/);
  assert.match(userFacingText, /Chris "Woods"/);
  assert.match(userFacingText, /Tell us what's going on/);
  assert.doesNotMatch(
    userFacingText,
    /\b(doctor|physician|appointment|insurance)\b/i,
  );
});

test("server-renders the finished Follow the Thread homepage", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  const visibleMarkup = withoutNonVisibleContent(html);
  const title =
    visibleMarkup.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? "";
  const headings = [
    ...visibleMarkup.matchAll(/<h[1-6]\b[^>]*>([\s\S]*?)<\/h[1-6]>/gi),
  ].map(([, heading]) => textContent(heading));
  const visibleText = textContent(html);
  const userFacingText = `${visibleText} ${userFacingAttributeText(html)}`;

  assert.match(textContent(title), /^NPCWoods Telemedicine/i);
  assert.deepEqual(
    headings.filter((heading) =>
      [
        "I feel awful",
        "I don’t have time for the runaround",
        "A real person can help me",
        "This is actually simple",
        "I know exactly what to do next",
      ].includes(heading),
    ),
    [
      "I feel awful",
      "I don’t have time for the runaround",
      "A real person can help me",
      "This is actually simple",
      "I know exactly what to do next",
    ],
  );
  assert.match(visibleText, /\$59 flat fee/i);
  assert.match(visibleText, /licensed in 11 states/i);
  assert.match(
    visibleText,
    /usually back to you within an hour during business hours/i,
  );
  assert.match(visibleMarkup, /href=["']sms:4806394722["']/i);
  assert.match(visibleMarkup, /<a\b[^>]*href=["']#main-content["'][^>]*>/i);
  assert.match(
    visibleMarkup,
    /<[a-z][^>]*\bid=["']main-content["'][^>]*>/i,
  );
  assert.match(visibleText, /Real texts\. Real relief\./i);
  assert.match(visibleText, /Some symptoms need in-person care/i);
  assert.match(visibleText, /What happens when I text Chris/i);

  assert.doesNotMatch(html, /codex-preview/i);
  assert.doesNotMatch(html, /react-loading-skeleton/i);
  assert.doesNotMatch(userFacingText, /Your site is taking shape/i);
  assert.doesNotMatch(userFacingText, /Codex is working/i);
  assert.doesNotMatch(userFacingText, /Codex is building the first version/i);
  assert.doesNotMatch(
    userFacingText,
    /\b(doctor|physician|appointment|insurance)\b/i,
  );
});
