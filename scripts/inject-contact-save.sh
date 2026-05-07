#!/usr/bin/env bash
#
# inject-contact-save.sh — Inject the "Save Contact" floating button into all NPCWoods HTML pages
#
# Usage: ./scripts/inject-contact-save.sh
# Safe to re-run — idempotent (skips already-injected pages)
#

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SNIPPET_FILE="$REPO_ROOT/html/shared/contact-save-snippet.html"

MARKER="NPCWoods Contact Save"

if [ ! -f "$SNIPPET_FILE" ]; then
  echo "ERROR: Snippet file not found: $SNIPPET_FILE"
  exit 1
fi

# Read the snippet content
SNIPPET_CONTENT=$(cat "$SNIPPET_FILE")

injected=0
skipped=0
errors=0

echo "Injecting contact save button into all HTML pages..."
echo ""

# Find all index.html files in landing-pages/ and html/
while IFS= read -r file; do
  # Skip shared snippets themselves
  if [[ "$file" == *"/shared/"* ]]; then
    continue
  fi

  # Skip if already injected
  if grep -q "$MARKER" "$file" 2>/dev/null; then
    echo "  SKIP: ${file#$REPO_ROOT/}"
    skipped=$((skipped + 1))
    continue
  fi

  # Check the file has a </body> tag to inject before
  if ! grep -q "</body>" "$file" 2>/dev/null; then
    echo "  ERROR (no </body>): ${file#$REPO_ROOT/}"
    errors=$((errors + 1))
    continue
  fi

  echo "  INJECT: ${file#$REPO_ROOT/}"

  python3 - "$file" <<PYEOF
import sys

filepath = sys.argv[1]
snippet = '''$SNIPPET_CONTENT'''

with open(filepath, 'r') as f:
    html = f.read()

# Insert before </body>
html = html.replace('</body>', snippet + '\n</body>', 1)

with open(filepath, 'w') as f:
    f.write(html)
PYEOF

  injected=$((injected + 1))

done < <(find "$REPO_ROOT/landing-pages" "$REPO_ROOT/html" -name "index.html" -type f 2>/dev/null)

echo ""
echo "Done."
echo "  Injected: $injected"
echo "  Skipped (already had it): $skipped"
echo "  Errors: $errors"
echo ""
echo "Next steps:"
echo "  1. Verify a few pages locally (open in browser)"
echo "  2. Upload chris-woods.vcf to server web root via SFTP"
echo "  3. Deploy all modified HTML pages via SFTP"
echo "  4. Deploy npcwoods-save-contact.php mu-plugin via SFTP"
