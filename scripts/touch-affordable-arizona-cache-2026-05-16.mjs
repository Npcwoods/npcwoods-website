import { Buffer } from "node:buffer";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const envText = readFileSync(resolve(root, ".env"), "utf8");
const env = {};

for (const rawLine of envText.split(/\r?\n/)) {
  const line = rawLine.trim();
  if (!line || line.startsWith("#") || !line.includes("=")) continue;
  const index = line.indexOf("=");
  const key = line.slice(0, index).trim();
  let value = line.slice(index + 1).trim();
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    value = value.slice(1, -1);
  }
  env[key] = value;
}

for (const key of ["WP_USERNAME", "WP_APP_PASSWORD"]) {
  if (!env[key]) {
    console.error(`[fatal] missing ${key} in root .env`);
    process.exit(2);
  }
}

const pageId = 198;
const userAgent =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36";
const auth = Buffer.from(`${env.WP_USERNAME}:${env.WP_APP_PASSWORD}`).toString(
  "base64",
);
const base = `https://npcwoods.com/wp-json/wp/v2/pages/${pageId}`;

async function wpJson(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Basic ${auth}`,
      "Content-Type": "application/json",
      "User-Agent": userAgent,
      ...(options.headers || {}),
    },
  });

  const text = await response.text();
  let body = {};
  if (text) {
    body = JSON.parse(text);
  }

  if (!response.ok) {
    throw new Error(
      `WordPress REST ${response.status}: ${body.message || response.statusText}`,
    );
  }

  return body;
}

const current = await wpJson(
  `${base}?context=edit&_fields=id,slug,status,title,content,modified`,
);

const payload = {
  title: current.title?.raw || current.title?.rendered || "",
  content: current.content?.raw || current.content?.rendered || "",
  status: current.status || "publish",
};

const updated = await wpJson(`${base}?_fields=id,slug,status,modified`, {
  method: "POST",
  body: JSON.stringify(payload),
});

console.log(
  JSON.stringify(
    {
      touched: true,
      id: updated.id,
      slug: updated.slug,
      status: updated.status,
      modified: updated.modified,
    },
    null,
    2,
  ),
);
