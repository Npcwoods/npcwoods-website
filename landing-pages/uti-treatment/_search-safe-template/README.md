# Search-Safe UTI City Pages — Template System

The 8 search-safe city landing pages under `landing-pages/uti-treatment/<slug>/search-safe/index.html` are generated from a single template plus per-city data. They are LIVE and receiving paid ad traffic — never hand-edit the generated pages; edit the template or `cities.json` and regenerate.

## Files

| File | What it is |
|---|---|
| `template.html` | The single source of truth for page design and copy. Placeholders: `{{SLUG}}`, `{{CITY}}`, `{{STATE}}`, `{{ST}}`, `{{STATE_PAGE}}` |
| `cities.json` | One entry per city — the only thing that varies between pages |
| `../../../scripts/build-search-safe-pages.py` | The generator. Writes only `<slug>/search-safe/index.html` |
| `../../../tests/test_search_safe_template.py` | Proves regenerated output is byte-identical to the committed pages |

## Change the design or copy

1. Edit `template.html` (one file — the change applies to every city).
2. Regenerate all pages:
   ```bash
   python3 scripts/build-search-safe-pages.py
   ```
3. Run the guardrail checks and review the git diff:
   ```bash
   python3 -m unittest tests.test_search_safe_template
   git diff -- 'landing-pages/uti-treatment/*/search-safe/index.html'
   ```
   (After a deliberate template change, the byte-identity test fails until the regenerated pages are committed — that's the point: it forces the diff to be reviewed.)
4. Commit template + regenerated pages together.

## Add a new city

1. Add an entry to `cities.json`. Every field is required:
   - `slug` — URL slug, lowercase with hyphens (e.g. `peoria-az`). Becomes `/uti-treatment/<slug>/search-safe/`
   - `city` — display name (e.g. `Peoria`)
   - `state` — full state name (e.g. `Arizona`)
   - `state_abbr` — two-letter abbreviation (e.g. `AZ`)
   - `state_page` — the state page path on npcwoods.com, no slashes (e.g. `arizona-telemedicine`)
2. Build just that city:
   ```bash
   python3 scripts/build-search-safe-pages.py --city peoria-az
   ```
3. Update `EXPECTED_SLUGS` in `tests/test_search_safe_template.py`, then run the tests.
4. Commit `cities.json`, the test, and the new `index.html`.

The generator validates required tracking markers (GTM, GA4, Google Ads, `tracking.js`), the `noindex,follow` robots meta, and the canonical response-time wording, and rejects any forbidden terms before writing anything.

## Notes

- These are noindex paid landing pages — they stay out of the sitemap and Search Console, and the `noindex,follow` robots meta must remain in the template.
- `scripts/build-uti-search-safe-cities-2026-06-11.py` is the old dated build script that spliced the design from the live surprise-az page at runtime. It is **superseded** by this template system and kept only for history — don't run it.
- The generator only writes local files. **Deploys are a separate step**: they go through the guarded deploy flow (SFTP upload, mu-plugin routing, cache flush, Playwright verification) and require Chris's explicit approval before anything goes live.
