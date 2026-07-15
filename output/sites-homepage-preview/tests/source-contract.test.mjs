import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function blockAfter(source, marker) {
  const match = marker.exec(source);
  assert.ok(match, `Expected ${marker} in source`);
  const openingBrace = source.indexOf("{", match.index + match[0].length);
  assert.notEqual(openingBrace, -1, `Expected a block after ${marker}`);

  let depth = 0;
  for (let index = openingBrace; index < source.length; index += 1) {
    if (source[index] === "{") depth += 1;
    if (source[index] === "}") depth -= 1;
    if (depth === 0) return source.slice(openingBrace + 1, index);
  }

  assert.fail(`Expected a closing brace after ${marker}`);
}

test("source includes the cinematic thread and reduced-motion contracts", async () => {
  const [followThread, globals] = await Promise.all([
    readFile(new URL("app/components/FollowThread.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);

  assert.match(followThread, /from\s+["']gsap\/ScrollTrigger["']/);
  assert.match(followThread, /gsap\.registerPlugin\(ScrollTrigger\)/);

  const matchMediaDeclaration = followThread.match(
    /\bconst\s+([A-Za-z_$][\w$]*)\s*=\s*gsap\.matchMedia\(\)\s*;/,
  );
  assert.ok(matchMediaDeclaration, "Expected a named gsap.matchMedia instance");
  const matchMediaName = escapeRegExp(matchMediaDeclaration[1]);
  assert.match(
    followThread,
    new RegExp(
      `\\b${matchMediaName}\\.add\\(\\s*\\{[\\s\\S]*?\\bcompact\\s*:\\s*["']\\(max-width:\\s*760px\\)["']`,
    ),
    "Expected the responsive breakpoint to be owned by gsap.matchMedia",
  );
  assert.doesNotMatch(
    followThread,
    /window\.matchMedia\(/,
    "Expected responsive motion to rebuild instead of sampling the viewport once",
  );
  const reducedMotionRegistration = new RegExp(
    `\\b${matchMediaName}\\.add\\(\\s*["']\\(prefers-reduced-motion:\\s*reduce\\)["']\\s*,`,
  );
  const reducedMotionCallback = blockAfter(
    followThread,
    reducedMotionRegistration,
  );
  assert.match(
    reducedMotionCallback,
    /\broot\.dataset\.motion\s*=\s*["']reduced["']\s*;/,
  );
  assert.match(
    reducedMotionCallback,
    /\bgsap\.set\([\s\S]*?\{[\s\S]*?\bclearProps\s*:\s*["']all["']/,
  );
  assert.match(
    followThread,
    new RegExp(
      `return\\s*\\(\\)\\s*=>\\s*(?:\\{\\s*)?${matchMediaName}\\.revert\\(\\)\\s*;?`,
    ),
  );

  const reducedMotionCss = blockAfter(
    globals,
    /@media\s*\([^)]*prefers-reduced-motion:\s*reduce[^)]*\)/,
  );
  assert.match(
    reducedMotionCss,
    /\banimation-duration\s*:\s*0?\.01ms\s*!important\s*;/,
  );
  assert.match(
    reducedMotionCss,
    /\btransition-duration\s*:\s*0?\.01ms\s*!important\s*;/,
  );
  const staticThreadPath = blockAfter(
    reducedMotionCss,
    /\.thread-path\b[^,{]*/,
  );
  assert.match(staticThreadPath, /\btransform\s*:\s*none\s*!important\s*;/);
  const staticMobileTextBar = blockAfter(
    reducedMotionCss,
    /\.mobile-text-bar\b[^,{]*/,
  );
  assert.match(staticMobileTextBar, /\btransform\s*:\s*none\s*!important\s*;/);

  const threadPathRule = blockAfter(globals, /\.thread-path\b[^,{]*/);
  assert.match(threadPathRule, /\bstroke(?:-[\w-]+)?\s*:/);

  const mobileTextBarRule = blockAfter(globals, /\.mobile-text-bar\b[^,{]*/);
  assert.match(mobileTextBarRule, /\bposition\s*:\s*fixed\b/);
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
    /codex-preview|Your site is taking shape|Codex is working|Codex is building the first version|SkeletonPreview|_sites-preview|react-loading-skeleton|Starter Project|site-creator-vinext-starter/i,
  );
  await assert.rejects(access(new URL("app/_sites-preview", projectRoot)), {
    code: "ENOENT",
  });
  await access(new URL("archive/starter/SkeletonPreview.tsx", projectRoot));
  await access(new URL("archive/starter/preview.css", projectRoot));
});

test("thread is contained by the full story and uses one continuous SVG gradient", async () => {
  const [homepage, threadPath, globals] = await Promise.all([
    readFile(new URL("app/components/HomepageContent.tsx", projectRoot), "utf8"),
    readFile(new URL("app/components/ThreadPath.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);

  assert.match(
    homepage,
    /<main\b[^>]*>[\s\S]*?<ThreadPath\s*\/>/,
    "Expected the thread to be a descendant of the full-height main story",
  );
  assert.match(threadPath, /<linearGradient\b[^>]*\bid=["']thread-story-gradient["']/);
  assert.match(threadPath, /stopColor=["']#bd5a42["']/);
  assert.match(threadPath, /stopColor=["']#2855c7["']/);
  assert.match(threadPath, /stopColor=["']#1c8a5c["']/);
  assert.match(
    threadPath,
    /<path[\s\S]*?className=["']thread-progress["'][\s\S]*?stroke=["']url\(#thread-story-gradient\)["']/,
  );

  const threadLayerRule = blockAfter(globals, /\.thread-layer\b[^,{]*/);
  assert.match(threadLayerRule, /\btop\s*:\s*0\s*;/);
  assert.match(threadLayerRule, /\bheight\s*:\s*100%\s*;/);
  assert.match(
    threadLayerRule,
    /\bleft\s*:\s*max\([^;]*\bvar\(--gutter\)/,
    "Expected the desktop thread to be positioned inside the outer gutter",
  );
  assert.match(threadLayerRule, /\bpointer-events\s*:\s*none\s*;/);
  assert.doesNotMatch(threadLayerRule, /\bbottom\s*:/);

  const elevatedContentRule = blockAfter(globals, /\.chapter\s*>\s*\*[^,{]*/);
  assert.match(
    elevatedContentRule,
    /\bz-index\s*:\s*3\s*;/,
    "Expected essential section content to paint above the decorative thread",
  );

  const threadProgressRule = blockAfter(globals, /\.thread-progress\b[^,{]*/);
  assert.doesNotMatch(threadProgressRule, /\bbackground(?:-image)?\s*:/);
  assert.doesNotMatch(threadProgressRule, /\bstroke-dasharray\s*:/);
  assert.doesNotMatch(globals, /\.thread-layer::before/);
});
