# GLP-1 Explained: explainer page template (series v2)

One shared template for every page in the GLP-1 Explained series
(`https://npcwoods.com/learn/glp1/<slug>/`). It matches the hub's Hero A look:
dark editorial hero, big Inter type, orange "pop" word, Chris's cut-out, same
CTA and fine print, plus bold color blocks for each story step.

```
templates/glp1-explainer/          (kitchen repo copy; same files live at /workspace/glp1-series/templates/explainer/)
  build.py              builds pages/<slug>.py -> out/<slug>/index.html
  template.html         page skeleton with {{placeholders}}
  lib.py                block helpers: sec(), fig(), svg(), why(), tile(), grid(), cite(), icon()
  series.json           road map: every stop, label, URL (null = coming soon), CTA + fine print
  partials/
    explainer.css       all page CSS (inlined; scoped .gh-* hero and .ex-* body)
    site-header.html    shared NPCWoods nav (from live; no tracking scripts)
    site-footer.html    shared footer (13 states incl. Florida by telehealth registration)
  pages/
    _shared.py          shared sources (SRC), brand/compounded DISCLAIMER, ghost backgrounds
    how-they-work.py    stop 2
    side-effects.py     stop 3
    first-30-days.py    stop 4
```

## Make the next page (example: Dose Steps)

1. **series.json**: set the stop's `url` to `https://npcwoods.com/learn/glp1/dose-steps/` and
   tighten its `blurb`. The road-map strip, prev/next cards, and "you are here" state on
   every page come from this file, so rebuild all pages after editing it.
2. **pages/dose-steps.py**: copy `first-30-days.py` and edit the `PAGE` dict:
   - `title`, `description`, `crumb`, `pill`, `h1_top` + `h1_pop` (pop = the orange word), `sub`, two `sticker`s.
   - `ghost_svg`: add a new generator in `_shared.py`. Topic picture only: **no numbers, no weights.**
   - `lede` should link back to the last stop in words ("Last stop, you...").
   - `tldr` (4 lines), `sections` (use `sec(theme, id, kicker, h2, copy, figure, flip, below)`;
     themes: cream, white, night, orange, blue; alternate them), `recap` (4 cards), `faq` (3-4), `sources`.
   - Diagrams: `svg(id, title, desc, '0 0 480 H', body)`. Keep labels at 16px or larger in a 480-wide viewBox, and draw on white.
   - Cite with `cite(n)`. `n` is the 1-based position in the page's `sources` list.
3. `python3 build.py` (or `python3 build.py dose-steps`).
4. Checks before you push:
   - Reading grade about 4.5. Run `python3 /workspace/npcfix/fk2.py out/*/index.html` (box), or use textstat on the Mac.
   - Banned words: doctor, physician, MD, insurance, appointment (the footer's "No appointment" line is OK), "Text a Doctor", "Florida-licensed".
   - No weight-loss promises, no before/after, no "guaranteed". Use brand names with ®. Compounded drugs are "not FDA-approved".
   - No Google, Meta, or Ahrefs scripts. Nothing starts hidden (no opacity-0 fade-ins). No sideways scroll at 390px.
5. Deploy (same process every time):
   - Back up the live file over SFTP.
   - Upload `out/<slug>/index.html` to `html/learn/glp1/<slug>/index.html`.
   - Add the route to **both** maps in `html/wp-content/mu-plugins/npcwoods-glp1-pages.php` (`$path_map` and `$slug_map`), then run `php -l`. Never add a second mu-plugin with the same functions.
   - Create the WP stub page (slug `<slug>`, parent 1055, published) so Yoast lists it in page-sitemap.xml.
   - Add the page to `llms.txt`, the hub road map and ItemList, the `/learn/` cards, and the `/glp1-weight-loss/` "Explained Plainly" cards.
   - Purge the cache with `touch_stub` on the stubs you changed. Then verify live: 200, schema, no tracking, 390px.

## What every page gets automatically
- Hero A with page ghost, CTA `sms:4806394722` "Text Chris · $59 consult", and the standard fine print.
- A sticky-free road-map strip with the current stop highlighted, live stops linked, and coming-soon stops labeled, plus a "← Series hub" link.
- Breadcrumbs, a clinician byline, prev/next cards, and a back-to-hub link.
- JSON-LD: MedicalWebPage (author/reviewedBy Chris, lastReviewed, citations), BreadcrumbList, FAQPage.
- A self-canonical URL, `index, follow`, a skip link, alt text, and accessible SVG titles and descriptions.

Stub IDs: hub 1055, how-they-work 1056, side-effects 1057, first-30-days (see the deploy notes or `scripts/page-ids-2026-04-22.json`).
