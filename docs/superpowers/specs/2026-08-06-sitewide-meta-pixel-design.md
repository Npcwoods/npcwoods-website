# Site-wide Meta Pixel Design

## Goal

Send one Meta `PageView` to Pixel `1428464038973925` on every HTML page of NPCWoods.com, including `/pay/` and `/thank-you/`, while stopping all other Google and Meta tracking from loading.

## Decision

Use the existing `php/npcwoods-tracking.php` mu-plugin as one response-level filter. It runs before the static-page route handlers, so it covers both WordPress-rendered pages and the static HTML pages served with `readfile()`.

Three approaches were considered:

1. Edit the 111 source files containing Google tags. This would be laborious, easy to miss on future pages, and would not remove tags injected by WordPress plugins.
2. Configure a tag manager. This would retain Google code and would not install Chris’s exact Meta snippet.
3. Filter every HTML response, remove active Google/Meta tags, and insert the exact snippet immediately before `</head>`. This is the selected approach because it covers the two page systems at one control point.

## Behavior

- The filter removes active Google Tag Manager, Google Analytics, Google Ads, Meta Pixel, Meta no-op blocks, and `/tracking.js` script tags before delivery.
- It preserves unrelated resources such as Google Fonts and Ahrefs analytics.
- It injects the exact supplied Meta snippet once, immediately before the closing `</head>` tag.
- It does not alter JSON, REST, or other non-HTML responses that have no `</head>` tag.
- A PHP-backed regression test feeds representative WordPress/static markup through the actual filter and verifies the required Pixel remains while legacy Google/Meta markers do not.

## Verification

1. Run the focused regression test and PHP syntax check.
2. Run the full Python suite; separately report the existing unrelated failures if they remain.
3. Dry-run then upload the one mu-plugin after Chris’s explicit approval in this thread.
4. Use real-browser network evidence on the homepage, a condition page, `/pay/`, and `/thank-you/` to prove one `fbevents.js` request and no Google/legacy-Meta tracking requests.

## Email Draft

Create, but do not send, a short team email asking whether the new site-wide PageView Pixel should remain on `/pay/` and `/thank-you/`.
