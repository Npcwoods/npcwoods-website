#!/usr/bin/env bash
set -euo pipefail

repo="$(git rev-parse --show-toplevel)"
hook="$repo/.git/hooks/post-commit"

cat > "$hook" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

repo="$(git rev-parse --show-toplevel)"
cd "$repo"

if [ "${NPCWOODS_AUTO_PREVIEW:-1}" = "0" ]; then
  exit 0
fi

mkdir -p automation-output/previews
{
  echo
  echo "=== $(date -u '+%Y-%m-%d %H:%M:%S UTC') post-commit preview ==="
  python3 scripts/preview-url.py --deploy --open
} 2>&1 | tee -a automation-output/previews/post-commit.log || true
HOOK

chmod +x "$hook"
echo "Installed post-commit preview hook at $hook"
echo "Disable for one commit with: NPCWOODS_AUTO_PREVIEW=0 git commit ..."
