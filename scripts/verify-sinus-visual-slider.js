#!/usr/bin/env node
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.goto('http://127.0.0.1:8766/sinus-infection-treatment/', { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#visual-guide-title');

  const title = await page.locator('#visual-guide-title').innerText();
  const hero = await page.locator('h1').first().innerText();
  const decisions = await page.locator('.decision-row').count();
  const slides = await page.locator('.visual-slide').count();
  const images = await page.locator('.visual-slide img').count();
  if (!hero.includes('Day 5-7 and still getting worse?')) throw new Error(`short hero missing: ${hero}`);
  if (!title.includes('See which story matches yours.')) throw new Error('visual guide title missing');
  if (decisions !== 4) throw new Error(`expected 4 decision rows, saw ${decisions}`);
  if (slides !== 5) throw new Error(`expected 5 slides, saw ${slides}`);
  if (images !== 5) throw new Error(`expected 5 images, saw ${images}`);

  await page.locator('[data-visual-next]').click();
  await page.waitForTimeout(550);
  const counter = await page.locator('[data-visual-counter]').innerText();
  if (!counter.includes('2 / 5')) throw new Error(`next button did not advance slider: ${counter}`);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (overflow > 1) throw new Error(`horizontal overflow: ${overflow}px`);

  await browser.close();
  console.log(JSON.stringify({ hero, title, decisions, slides, images, counter, overflow }, null, 2));
}

main().catch(async (error) => {
  console.error(error);
  process.exit(1);
});
