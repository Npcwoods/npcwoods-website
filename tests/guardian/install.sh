#!/bin/zsh
# Install the nightly site guardian as a launchd agent (daily ~6:05am).
#
# DO NOT run this without Chris's yes — nothing is scheduled until this runs.
#
# TCC workaround (same as the git-hygiene / drift-check monitors): launchd
# cannot read ~/Desktop paths, so everything the job needs is staged under
# ~/.local/npcwoods/site-guardian/ with its own venv. Reports go to
# ~/.local/npcwoods/reports/guardian-reports/latest.md (atomic temp+rename).
#
# Re-run this script any time guardian.py or manifest.json changes
# (e.g. after `python3 tests/guardian/build_manifest.py`).
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST_DIR="$HOME/.local/npcwoods/site-guardian"
REPORT_DIR="$HOME/.local/npcwoods/reports/guardian-reports"
PLIST_NAME="com.npcwoods.site-guardian.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "==> Staging guardian under $DEST_DIR (launchd cannot read ~/Desktop)"
mkdir -p "$DEST_DIR" "$REPORT_DIR"
cp "$SRC_DIR/guardian.py" "$DEST_DIR/guardian.py"
cp "$SRC_DIR/manifest.json" "$DEST_DIR/manifest.json"

if [ ! -x "$DEST_DIR/venv/bin/python3" ]; then
  echo "==> Creating venv (requests + playwright, no credentials needed)"
  python3 -m venv "$DEST_DIR/venv"
fi
"$DEST_DIR/venv/bin/pip" install --quiet --upgrade requests playwright
"$DEST_DIR/venv/bin/playwright" install chromium

echo "==> Installing $PLIST_DEST"
mkdir -p "$HOME/Library/LaunchAgents"
cp "$SRC_DIR/$PLIST_NAME" "$PLIST_DEST"

echo "==> Loading launchd job"
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"
launchctl list | grep com.npcwoods.site-guardian || true

echo ""
echo "Installed. Runs daily at 6:05am."
echo "Morning report: $REPORT_DIR/latest.md"
echo "Trigger a run now with: launchctl start com.npcwoods.site-guardian"
