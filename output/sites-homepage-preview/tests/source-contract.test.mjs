import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

test("source includes the cinematic thread and reduced-motion contracts", async () => {
  const [followThread, globals] = await Promise.all([
    readFile(new URL("app/components/FollowThread.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);

  assert.match(followThread, /gsap\/ScrollTrigger/);
  assert.match(followThread, /gsap\.matchMedia/);
  assert.match(followThread, /prefers-reduced-motion:\s*reduce/);
  assert.match(followThread, /\.revert\(\);/);

  assert.match(globals, /@media\s*\([^)]*prefers-reduced-motion:\s*reduce[^)]*\)/);
  assert.match(globals, /\.thread-path\b/);
  assert.match(globals, /\.mobile-text-bar\b/);
});

test("starter preview is removed from runtime source and retained in the archive", async () => {
  const [page, layout, packageJson] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/layout.tsx", projectRoot), "utf8"),
    readFile(new URL("package.json", projectRoot), "utf8"),
  ]);
  const runtimeSource = [page, layout, packageJson].join("\n");

  assert.doesNotMatch(
    runtimeSource,
    /codex-preview|Your site is taking shape|Codex is working|SkeletonPreview|_sites-preview|react-loading-skeleton|Starter Project|site-creator-vinext-starter/i,
  );
  await assert.rejects(access(new URL("app/_sites-preview", projectRoot)), {
    code: "ENOENT",
  });
  await access(new URL("archive/starter/SkeletonPreview.tsx", projectRoot));
  await access(new URL("archive/starter/preview.css", projectRoot));
});
