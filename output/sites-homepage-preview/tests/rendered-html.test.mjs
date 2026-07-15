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

function textContent(markup) {
  return markup
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&(?:#39|apos);/gi, "'")
    .replace(/&quot;/gi, '"')
    .replace(/&amp;/gi, "&")
    .replace(/\s+/g, " ")
    .trim();
}

test("server-renders the finished Follow the Thread homepage", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  const title = html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? "";
  const headings = [...html.matchAll(/<h[1-6]\b[^>]*>([\s\S]*?)<\/h[1-6]>/gi)].map(
    ([, heading]) => textContent(heading),
  );
  const visibleText = textContent(html);

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
  assert.match(html, /href=["']sms:4806394722["']/i);
  assert.match(html, /<a\b[^>]*href=["']#main-content["'][^>]*>/i);
  assert.match(visibleText, /Real texts\. Real relief\./i);
  assert.match(visibleText, /Some symptoms need in-person care/i);
  assert.match(visibleText, /What happens when I text Chris/i);

  assert.doesNotMatch(html, /codex-preview/i);
  assert.doesNotMatch(html, /Your site is taking shape/i);
  assert.doesNotMatch(html, /react-loading-skeleton/i);
  assert.doesNotMatch(html, /\b(doctor|physician|appointment|insurance)\b/i);
});
