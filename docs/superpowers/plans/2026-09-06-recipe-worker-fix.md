# Website recipe and worker repair

> Execution: inline, using writing-plans, test-driven-development, and verification-before-completion. Chris requested the repairs after the source assessment. No GitHub save, preview publication, production push, or scheduled-worker installation is authorized by this implementation request.

**Goal:** Agree on one executable website policy, verify the real clean page, and return an honest, checked preview from the worker.

**Architecture:** Keep WordPress/GoDaddy and the existing Python publishing tool. Share the static-page tracking policy between the generator, publisher, and Guardian. Keep the homepage's existing separate policy intact. Repair the Node worker's existing allowlisted workflow, approval boundary, and result delivery.

**Tech stack:** Python standard library + existing requests/Playwright; Node standard library; existing Vercel CLI for explicitly approved preview publication.

## Requirements and evidence

- [x] Add regression tests before implementation: real local HTTP responses must detect clean-URL shells, redirects, incorrect title/H1, thin responses, and forbidden tracking. A successful cache-busting response cannot rescue a failed clean URL.
- [x] Centralize static-page tracker markers in `scripts/website_policy.py`. The generator, publisher, Guardian, and source checker must use them. Use the existing `replace_sitewide_tracking.py` transformation to repair affected local HTML, preserving the homepage and unrelated edits.
- [x] Repair the eight-city recipe: required paid marker/noindex/response copy remain; requiring a forbidden tracking script is removed. Regeneration must agree with all eight saved pages without losing city-specific content.
- [x] Change `scripts/deploy.py` to compare the ordinary response with local title/H1 and expected size; browser checks must inspect the same clean address, reject forbidden network traffic, and record screenshots. Missing browser verification must not report full success.
- [x] Make `scripts/check-website-recipes.py` a read-only local check for tracker drift and generated-page drift. Refresh active website instructions to reference this check and the shared policy rather than contradictory historical requirements.
- [x] Repair preview preparation: immutable per-task output, no destructive directory replacement, exact requested routes, no PHP leakage or tracking in public preview output, and a structured manifest of routes and hashes.
- [ ] Repair the worker: validate the workspace and page scope; keep local preparation separate from explicitly approved preview publication; wait for the preview to finish; verify each returned page; return structured review results through the task endpoint; forward production confirmation only for an approved task; never overlap polling executions.
- [x] Scope decision: no editing-runner selection was received. Codex remains the chef for editing tickets; this repair handles prepared pages, checks, approvals, and preview delivery. No new freeform editing runner is claimed.
- [ ] Verify targeted Python tests and the complete worker test suite, then run real local HTTP/browser fixtures for the critical boundaries. Record any external runtime checks still awaiting an authorized activation.
- [ ] Review and transfer only this task's changes to the original kitchen after checking original-file hashes. Preserve the 12 pre-existing local changes. No commit or push.

## Decisions

Shared policy is preferable to weakening the guard: current source tests and GL-011 explicitly preserve tracking restrictions. A local fixture isolates verifier defects from hosting/cache behavior. Native phone access remains the recommended operator interface; this repair does not invent a new dashboard.

## Validation commands

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_deploy_tool tests.test_clean_page_verification tests.test_website_policy tests.test_search_safe_template tests.test_guardian_tracking`

`python3 scripts/check-website-recipes.py`

`node --test test/*.test.js` in the worker kitchen.

## Local website evidence

77 targeted Python tests passed, including real Chrome phone/desktop fixtures. The read-only drift check passed 162 public documents, eight city recipes, and seven active instruction files. All 158 cleaned HTML files retain their visible text, links, and allowed scripts. Preview snapshot races and verification bypasses have regression coverage. No live clinic or public preview was contacted.
