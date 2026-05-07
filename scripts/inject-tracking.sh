#!/usr/bin/env bash
#
# inject-tracking.sh — Inject GTM + GA4 + Meta Pixel + tracking.js into all NPCWoods HTML pages
#
# Usage: ./scripts/inject-tracking.sh
# Safe to re-run — idempotent (skips already-injected pages)
#

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Tracking IDs — update these as needed
GTM_ID="GTM-59QSWZRC"
GA4_ID="G-EFFRQMG8TC"
ADS_ID="AW-610222919"
FB_PIXEL_ID="1558261907814968"

MARKER="NPCWoods Tracking"

injected=0
skipped=0

# Find all index.html files
while IFS= read -r file; do
  # Skip if already injected
  if grep -q "$MARKER" "$file" 2>/dev/null; then
    echo "  SKIP: $file"
    skipped=$((skipped + 1))
    continue
  fi

  echo "  INJECT: $file"

  python3 - "$file" "$GTM_ID" "$GA4_ID" "$ADS_ID" "$FB_PIXEL_ID" <<'PYEOF'
import sys, re

filepath = sys.argv[1]
gtm_id = sys.argv[2]
ga4_id = sys.argv[3]
ads_id = sys.argv[4]
fb_pixel_id = sys.argv[5]

with open(filepath, 'r') as f:
    html = f.read()

# GTM head snippet
head_snippet = f"""<!-- NPCWoods Tracking: GTM -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{gtm_id}');</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{ga4_id}');
gtag('config', '{ads_id}');
</script>
<!-- NPCWoods Tracking: Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{fb_pixel_id}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={fb_pixel_id}&ev=PageView&noscript=1"/></noscript>"""

# GTM noscript (after <body>)
body_snippet = f"""<!-- NPCWoods Tracking: GTM noscript -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>"""

# Canonical site event layer (before </body>)
js_snippet = """<!-- NPCWoods Tracking: tracking.js -->
<script src="/tracking.js"></script>"""

# 1. Insert after <head...>
html = re.sub(r'(<head[^>]*>)', r'\1\n' + head_snippet, html, count=1)

# 2. Insert after <body...>
html = re.sub(r'(<body[^>]*>)', r'\1\n' + body_snippet, html, count=1)

# 3. Insert before </body>
html = html.replace('</body>', js_snippet + '\n</body>', 1)

with open(filepath, 'w') as f:
    f.write(html)
PYEOF

  injected=$((injected + 1))

done < <(find "$REPO_ROOT/landing-pages" "$REPO_ROOT/html" -name "index.html" -type f 2>/dev/null)

echo ""
echo "Done. Injected: $injected, Skipped: $skipped"
echo ""
echo "Next steps:"
echo "  1. Re-run this script after creating new static pages"
echo "  2. Deploy via SFTP"
echo "  3. Keep conversion logic in GTM / GA4, not inline page code"
