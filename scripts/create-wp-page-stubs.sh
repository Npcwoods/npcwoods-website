#!/bin/bash
# ============================================================
# Create WordPress Page Stubs for Education Library
# ============================================================
# Creates empty WP pages at each /learn/ and /medications/ slug
# so WordPress sitemap and routing know these URLs exist.
# The mu-plugin intercepts the actual request and serves static HTML.
#
# USAGE:
#   1. Set WP credentials in .env or export them:
#      WP_USERNAME=your-username
#      WP_APP_PASSWORD=your-app-password
#   2. Run: bash scripts/create-wp-page-stubs.sh
# ============================================================

set -e

# Load .env if present
if [ -f "$(dirname "$0")/../.env" ]; then
    source "$(dirname "$0")/../.env"
fi

WP_URL="https://npcwoods.com/wp-json/wp/v2/pages"
AUTH="${WP_USERNAME}:${WP_APP_PASSWORD}"

if [ -z "$WP_USERNAME" ] || [ -z "$WP_APP_PASSWORD" ]; then
    echo "❌ WordPress credentials not set!"
    echo "Set WP_USERNAME and WP_APP_PASSWORD in .env or as environment variables."
    exit 1
fi

echo "📝 Creating WordPress page stubs for sitemap coverage..."
echo ""

# Function to create a WP page stub
create_page() {
    local title="$1"
    local slug="$2"
    local parent_id="$3"

    echo -n "  Creating: /$slug/ ... "

    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "$WP_URL" \
        -u "$AUTH" \
        -H "Content-Type: application/json" \
        -d "{
            \"title\": \"$title\",
            \"slug\": \"$slug\",
            \"status\": \"publish\",
            \"content\": \"<!-- This page is served by the npcwoods-education-pages mu-plugin -->\",
            \"parent\": $parent_id
        }")

    if [ "$response" = "201" ]; then
        echo "✅ Created"
    elif [ "$response" = "400" ]; then
        echo "⚠️  Already exists (skipped)"
    else
        echo "❌ HTTP $response"
    fi
}

# First, create the parent /learn/ page and get its ID
echo "Creating parent pages..."
LEARN_RESPONSE=$(curl -s -X POST "$WP_URL" \
    -u "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "After Your Visit — Patient Education Library",
        "slug": "learn",
        "status": "publish",
        "content": "<!-- Served by mu-plugin -->"
    }')

LEARN_ID=$(echo "$LEARN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',0))" 2>/dev/null || echo "0")
echo "  /learn/ page ID: $LEARN_ID"

MEDS_RESPONSE=$(curl -s -X POST "$WP_URL" \
    -u "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Medications Guide",
        "slug": "medications",
        "status": "publish",
        "content": "<!-- Served by mu-plugin -->"
    }')

MEDS_ID=$(echo "$MEDS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',0))" 2>/dev/null || echo "0")
echo "  /medications/ page ID: $MEDS_ID"
echo ""

# Condition education pages (children of /learn/)
echo "Creating condition education page stubs..."
create_page "Strep Throat: What to Know After Your Visit" "strep-throat" "${LEARN_ID:-0}"
create_page "UTI: What to Know After Your Visit" "uti" "${LEARN_ID:-0}"
create_page "Sinus Infection: What to Know After Your Visit" "sinus-infection" "${LEARN_ID:-0}"
create_page "Tooth Infection: What to Know After Your Visit" "tooth-infection" "${LEARN_ID:-0}"
create_page "Ear Infection: What to Know After Your Visit" "ear-infection" "${LEARN_ID:-0}"
create_page "Stomach Bug: What to Know After Your Visit" "stomach-bug" "${LEARN_ID:-0}"
create_page "Pink Eye: What to Know After Your Visit" "pink-eye" "${LEARN_ID:-0}"
create_page "Bronchitis: What to Know After Your Visit" "bronchitis" "${LEARN_ID:-0}"
create_page "Skin Infection: What to Know After Your Visit" "skin-infection" "${LEARN_ID:-0}"
create_page "Allergic Reaction: What to Know After Your Visit" "allergic-reaction" "${LEARN_ID:-0}"
create_page "Cold Sores: What to Know After Your Visit" "cold-sores" "${LEARN_ID:-0}"
create_page "Yeast Infection: What to Know After Your Visit" "yeast-infection" "${LEARN_ID:-0}"
create_page "Ingrown Toenail: What to Know After Your Visit" "ingrown-toenail" "${LEARN_ID:-0}"
create_page "COVID & Flu: What to Know After Your Visit" "covid-flu" "${LEARN_ID:-0}"
echo ""

# Drug reference pages (children of /medications/)
echo "Creating medication page stubs..."
create_page "Amoxicillin: Patient Guide" "amoxicillin" "${MEDS_ID:-0}"
create_page "Augmentin: Patient Guide" "augmentin" "${MEDS_ID:-0}"
create_page "Azithromycin: Patient Guide" "azithromycin" "${MEDS_ID:-0}"
create_page "Penicillin: Patient Guide" "penicillin" "${MEDS_ID:-0}"
create_page "Doxycycline: Patient Guide" "doxycycline" "${MEDS_ID:-0}"
create_page "Cephalexin: Patient Guide" "cephalexin" "${MEDS_ID:-0}"
create_page "Clindamycin: Patient Guide" "clindamycin" "${MEDS_ID:-0}"
create_page "Metronidazole: Patient Guide" "metronidazole" "${MEDS_ID:-0}"
create_page "Nitrofurantoin: Patient Guide" "nitrofurantoin" "${MEDS_ID:-0}"
create_page "TMP-SMX (Bactrim): Patient Guide" "tmp-smx" "${MEDS_ID:-0}"
create_page "Fluconazole: Patient Guide" "fluconazole" "${MEDS_ID:-0}"
create_page "Valacyclovir: Patient Guide" "valacyclovir" "${MEDS_ID:-0}"
create_page "Ondansetron: Patient Guide" "ondansetron" "${MEDS_ID:-0}"
create_page "Hydroxyzine: Patient Guide" "hydroxyzine" "${MEDS_ID:-0}"
create_page "Prednisone: Patient Guide" "prednisone" "${MEDS_ID:-0}"
create_page "Mupirocin: Patient Guide" "mupirocin" "${MEDS_ID:-0}"
create_page "Benzonatate: Patient Guide" "benzonatate" "${MEDS_ID:-0}"
create_page "Oseltamivir: Patient Guide" "oseltamivir" "${MEDS_ID:-0}"
create_page "Paxlovid: Patient Guide" "paxlovid" "${MEDS_ID:-0}"
create_page "Erythromycin Ophthalmic: Patient Guide" "erythromycin-ophthalmic" "${MEDS_ID:-0}"
create_page "Polytrim: Patient Guide" "polytrim" "${MEDS_ID:-0}"
echo ""

echo "✅ All page stubs created!"
echo ""
echo "These pages will appear in your WordPress sitemap."
echo "The mu-plugin serves the actual static HTML content."
