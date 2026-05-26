#!/bin/bash
# Deploy script: Shared CSS/JS Extraction
# Run from: ~/Desktop/Chris-HQ/npcwoods-website/
# Usage: bash scripts/deploy-css-js-extraction.sh

set -e

echo "=== Step 1: Clean git lock files ==="
rm -f .git/index.lock
rm -f .git/objects/maintenance.lock
find .git/objects -name "tmp_obj_*" -delete 2>/dev/null || true
echo "Done."

echo ""
echo "=== Step 2: Stage all changes ==="
git add assets/css/site.css assets/js/site.js scripts/extract-shared-css-js.py
git add html/shared/header-snippet.html html/shared/footer-snippet.html html/shared/contact-save-snippet.html
git add -A
echo "Staged $(git diff --cached --name-only | wc -l | tr -d ' ') files"

echo ""
echo "=== Step 3: Commit ==="
git commit -m "[perf] Extract shared CSS/JS into external files

- Created assets/css/site.css (nav, footer, reviews, save-contact CSS)
- Created assets/js/site.js (nav, CWV reporter, save-contact, fade-in JS)
- Removed ~1.8MB of duplicated inline CSS/JS across 79 pages
- Updated shared snippets to reference external files
- Added migration script: scripts/extract-shared-css-js.py"
echo "Committed."

echo ""
echo "=== Step 4: Push to origin/main ==="
git push origin main
echo "Pushed."

echo ""
echo "=== Done! Ready for SFTP deploy. ==="
