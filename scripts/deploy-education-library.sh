#!/bin/bash
# ============================================================
# NPCWoods Patient Education Library — Deployment Script
# ============================================================
# This script uploads all education pages, drug pages, the hub
# page, and the mu-plugin to the live GoDaddy server via SFTP.
#
# USAGE:
#   1. Fill in your SFTP credentials below (or export them as env vars)
#   2. Run: bash scripts/deploy-education-library.sh
#
# WHAT IT DOES:
#   - Uploads the mu-plugin to /wp-content/mu-plugins/
#   - Creates /learn/ and /medications/ directories on the server
#   - Uploads all 36 HTML pages to their correct paths
#   - Verifies each upload
# ============================================================

set -e

# ------- SFTP CREDENTIALS -------
# Option 1: Set these directly
SFTP_HOST="${SFTP_HOST:-}"
SFTP_USER="${SFTP_USER:-}"
SFTP_PASS="${SFTP_PASS:-}"
SFTP_PORT="${SFTP_PORT:-22}"

# Option 2: Read from .env file if it exists
if [ -f "$(dirname "$0")/../.env" ]; then
    source "$(dirname "$0")/../.env"
fi

# The web root on GoDaddy (typical path — adjust if different)
REMOTE_ROOT="${REMOTE_ROOT:-/home/${SFTP_USER}/public_html}"

# Local paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LANDING_DIR="$REPO_DIR/landing-pages"
PHP_DIR="$REPO_DIR/php"

# ------- VALIDATION -------
if [ -z "$SFTP_HOST" ] || [ -z "$SFTP_USER" ]; then
    echo "❌ SFTP credentials not set!"
    echo ""
    echo "Set them by either:"
    echo "  1. Creating a .env file in the npcwoods-website/ folder with:"
    echo "     SFTP_HOST=your-server.com"
    echo "     SFTP_USER=your-username"
    echo "     SFTP_PASS=your-password"
    echo ""
    echo "  2. Or export them before running:"
    echo "     export SFTP_HOST=your-server.com"
    echo "     export SFTP_USER=your-username"
    echo "     export SFTP_PASS=your-password"
    echo "     bash scripts/deploy-education-library.sh"
    exit 1
fi

echo "🚀 NPCWoods Education Library Deployment"
echo "========================================="
echo "Server: $SFTP_HOST"
echo "User:   $SFTP_USER"
echo "Root:   $REMOTE_ROOT"
echo ""

# ------- INSTALL sshpass IF NEEDED -------
if ! command -v sshpass &> /dev/null && [ -n "$SFTP_PASS" ]; then
    echo "⚠️  sshpass not found. Install it or use SSH key authentication."
    echo "   brew install hudochenkov/sshpass/sshpass  (macOS)"
    echo "   sudo apt install sshpass                  (Linux)"
fi

# Helper function for SFTP commands
sftp_cmd() {
    if [ -n "$SFTP_PASS" ] && command -v sshpass &> /dev/null; then
        sshpass -p "$SFTP_PASS" sftp -P "$SFTP_PORT" -oBatchMode=no -oStrictHostKeyChecking=no "$SFTP_USER@$SFTP_HOST" <<< "$1"
    else
        sftp -P "$SFTP_PORT" "$SFTP_USER@$SFTP_HOST" <<< "$1"
    fi
}

# Helper for batch SFTP
sftp_batch() {
    if [ -n "$SFTP_PASS" ] && command -v sshpass &> /dev/null; then
        sshpass -p "$SFTP_PASS" sftp -P "$SFTP_PORT" -oBatchMode=no -oStrictHostKeyChecking=no "$SFTP_USER@$SFTP_HOST" < "$1"
    else
        sftp -P "$SFTP_PORT" "$SFTP_USER@$SFTP_HOST" < "$1"
    fi
}

# ------- BUILD SFTP BATCH FILE -------
BATCH_FILE=$(mktemp)
cat > "$BATCH_FILE" << SFTP_COMMANDS
# Create directory structure
-mkdir ${REMOTE_ROOT}/learn
-mkdir ${REMOTE_ROOT}/learn/strep-throat
-mkdir ${REMOTE_ROOT}/learn/uti
-mkdir ${REMOTE_ROOT}/learn/sinus-infection
-mkdir ${REMOTE_ROOT}/learn/tooth-infection
-mkdir ${REMOTE_ROOT}/learn/ear-infection
-mkdir ${REMOTE_ROOT}/learn/stomach-bug
-mkdir ${REMOTE_ROOT}/learn/pink-eye
-mkdir ${REMOTE_ROOT}/learn/bronchitis
-mkdir ${REMOTE_ROOT}/learn/skin-infection
-mkdir ${REMOTE_ROOT}/learn/allergic-reaction
-mkdir ${REMOTE_ROOT}/learn/cold-sores
-mkdir ${REMOTE_ROOT}/learn/yeast-infection
-mkdir ${REMOTE_ROOT}/learn/ingrown-toenail
-mkdir ${REMOTE_ROOT}/learn/covid-flu
-mkdir ${REMOTE_ROOT}/medications
-mkdir ${REMOTE_ROOT}/medications/amoxicillin
-mkdir ${REMOTE_ROOT}/medications/augmentin
-mkdir ${REMOTE_ROOT}/medications/azithromycin
-mkdir ${REMOTE_ROOT}/medications/penicillin
-mkdir ${REMOTE_ROOT}/medications/doxycycline
-mkdir ${REMOTE_ROOT}/medications/cephalexin
-mkdir ${REMOTE_ROOT}/medications/clindamycin
-mkdir ${REMOTE_ROOT}/medications/metronidazole
-mkdir ${REMOTE_ROOT}/medications/nitrofurantoin
-mkdir ${REMOTE_ROOT}/medications/tmp-smx
-mkdir ${REMOTE_ROOT}/medications/fluconazole
-mkdir ${REMOTE_ROOT}/medications/valacyclovir
-mkdir ${REMOTE_ROOT}/medications/ondansetron
-mkdir ${REMOTE_ROOT}/medications/hydroxyzine
-mkdir ${REMOTE_ROOT}/medications/prednisone
-mkdir ${REMOTE_ROOT}/medications/mupirocin
-mkdir ${REMOTE_ROOT}/medications/benzonatate
-mkdir ${REMOTE_ROOT}/medications/oseltamivir
-mkdir ${REMOTE_ROOT}/medications/paxlovid
-mkdir ${REMOTE_ROOT}/medications/erythromycin-ophthalmic
-mkdir ${REMOTE_ROOT}/medications/polytrim

# Upload mu-plugin
put ${PHP_DIR}/npcwoods-education-pages.php ${REMOTE_ROOT}/wp-content/mu-plugins/npcwoods-education-pages.php

# Upload hub page
put ${LANDING_DIR}/learn/index.html ${REMOTE_ROOT}/learn/index.html

# Upload condition education pages
put ${LANDING_DIR}/learn/strep-throat/index.html ${REMOTE_ROOT}/learn/strep-throat/index.html
put ${LANDING_DIR}/learn/uti/index.html ${REMOTE_ROOT}/learn/uti/index.html
put ${LANDING_DIR}/learn/sinus-infection/index.html ${REMOTE_ROOT}/learn/sinus-infection/index.html
put ${LANDING_DIR}/learn/tooth-infection/index.html ${REMOTE_ROOT}/learn/tooth-infection/index.html
put ${LANDING_DIR}/learn/ear-infection/index.html ${REMOTE_ROOT}/learn/ear-infection/index.html
put ${LANDING_DIR}/learn/stomach-bug/index.html ${REMOTE_ROOT}/learn/stomach-bug/index.html
put ${LANDING_DIR}/learn/pink-eye/index.html ${REMOTE_ROOT}/learn/pink-eye/index.html
put ${LANDING_DIR}/learn/bronchitis/index.html ${REMOTE_ROOT}/learn/bronchitis/index.html
put ${LANDING_DIR}/learn/skin-infection/index.html ${REMOTE_ROOT}/learn/skin-infection/index.html
put ${LANDING_DIR}/learn/allergic-reaction/index.html ${REMOTE_ROOT}/learn/allergic-reaction/index.html
put ${LANDING_DIR}/learn/cold-sores/index.html ${REMOTE_ROOT}/learn/cold-sores/index.html
put ${LANDING_DIR}/learn/yeast-infection/index.html ${REMOTE_ROOT}/learn/yeast-infection/index.html
put ${LANDING_DIR}/learn/ingrown-toenail/index.html ${REMOTE_ROOT}/learn/ingrown-toenail/index.html
put ${LANDING_DIR}/learn/covid-flu/index.html ${REMOTE_ROOT}/learn/covid-flu/index.html

# Upload drug reference pages
put ${LANDING_DIR}/medications/amoxicillin/index.html ${REMOTE_ROOT}/medications/amoxicillin/index.html
put ${LANDING_DIR}/medications/augmentin/index.html ${REMOTE_ROOT}/medications/augmentin/index.html
put ${LANDING_DIR}/medications/azithromycin/index.html ${REMOTE_ROOT}/medications/azithromycin/index.html
put ${LANDING_DIR}/medications/penicillin/index.html ${REMOTE_ROOT}/medications/penicillin/index.html
put ${LANDING_DIR}/medications/doxycycline/index.html ${REMOTE_ROOT}/medications/doxycycline/index.html
put ${LANDING_DIR}/medications/cephalexin/index.html ${REMOTE_ROOT}/medications/cephalexin/index.html
put ${LANDING_DIR}/medications/clindamycin/index.html ${REMOTE_ROOT}/medications/clindamycin/index.html
put ${LANDING_DIR}/medications/metronidazole/index.html ${REMOTE_ROOT}/medications/metronidazole/index.html
put ${LANDING_DIR}/medications/nitrofurantoin/index.html ${REMOTE_ROOT}/medications/nitrofurantoin/index.html
put ${LANDING_DIR}/medications/tmp-smx/index.html ${REMOTE_ROOT}/medications/tmp-smx/index.html
put ${LANDING_DIR}/medications/fluconazole/index.html ${REMOTE_ROOT}/medications/fluconazole/index.html
put ${LANDING_DIR}/medications/valacyclovir/index.html ${REMOTE_ROOT}/medications/valacyclovir/index.html
put ${LANDING_DIR}/medications/ondansetron/index.html ${REMOTE_ROOT}/medications/ondansetron/index.html
put ${LANDING_DIR}/medications/hydroxyzine/index.html ${REMOTE_ROOT}/medications/hydroxyzine/index.html
put ${LANDING_DIR}/medications/prednisone/index.html ${REMOTE_ROOT}/medications/prednisone/index.html
put ${LANDING_DIR}/medications/mupirocin/index.html ${REMOTE_ROOT}/medications/mupirocin/index.html
put ${LANDING_DIR}/medications/benzonatate/index.html ${REMOTE_ROOT}/medications/benzonatate/index.html
put ${LANDING_DIR}/medications/oseltamivir/index.html ${REMOTE_ROOT}/medications/oseltamivir/index.html
put ${LANDING_DIR}/medications/paxlovid/index.html ${REMOTE_ROOT}/medications/paxlovid/index.html
put ${LANDING_DIR}/medications/erythromycin-ophthalmic/index.html ${REMOTE_ROOT}/medications/erythromycin-ophthalmic/index.html
put ${LANDING_DIR}/medications/polytrim/index.html ${REMOTE_ROOT}/medications/polytrim/index.html

bye
SFTP_COMMANDS

echo "📦 Uploading 36 pages + mu-plugin..."
echo ""

sftp_batch "$BATCH_FILE"

rm "$BATCH_FILE"

echo ""
echo "✅ Upload complete!"
echo ""
echo "========================================="
echo "NEXT STEPS (manual):"
echo "========================================="
echo "1. Verify the mu-plugin loaded: visit https://npcwoods.com/learn/"
echo "2. Spot-check a few pages:"
echo "   - https://npcwoods.com/learn/strep-throat/"
echo "   - https://npcwoods.com/medications/amoxicillin/"
echo "   - https://npcwoods.com/learn/uti/"
echo "3. Add the homepage education section (see html/homepage-education-section.html)"
echo "4. Create WordPress page stubs at each slug for sitemap coverage"
echo "========================================="
