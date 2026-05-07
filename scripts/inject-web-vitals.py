#!/usr/bin/env python3
"""Inject the Core Web Vitals reporter into any page that has the header but
didn't get updated by sync-header-snippet.py (no opening marker).

Idempotent: uses __npcCwvLoaded as the guard — re-running won't duplicate.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "html", ROOT / "landing-pages"]
END_MARKER = "<!-- ===== END SITE HEADER ===== -->"
GUARD = "__npcCwvLoaded"

BLOCK = """
<!-- ===== Core Web Vitals field reporter (sends LCP/CLS/INP/FCP/TTFB to GA4 via dataLayer) ===== -->
<script>
(function() {
  if (window.__npcCwvLoaded) return;
  window.__npcCwvLoaded = true;
  window.dataLayer = window.dataLayer || [];
  function report(metric) {
    try {
      window.dataLayer.push({
        event: 'web_vitals',
        metric_name: metric.name,
        metric_value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
        metric_rating: metric.rating,
        metric_id: metric.id,
        page_path: location.pathname
      });
    } catch (e) {}
  }
  function load() {
    var s = document.createElement('script');
    s.src = 'https://unpkg.com/web-vitals@4/dist/web-vitals.attribution.iife.js';
    s.async = true;
    s.onload = function() {
      if (!window.webVitals) return;
      window.webVitals.onLCP(report);
      window.webVitals.onCLS(report);
      window.webVitals.onINP(report);
      window.webVitals.onFCP(report);
      window.webVitals.onTTFB(report);
    };
    document.head.appendChild(s);
  }
  if ('requestIdleCallback' in window) {
    requestIdleCallback(load, { timeout: 3000 });
  } else {
    setTimeout(load, 2000);
  }
})();
</script>
"""


def main() -> int:
    injected = 0
    already = 0
    no_marker = 0

    targets = []
    for root in SCAN_DIRS:
        for html in root.rglob("index.html"):
            if html.name.endswith(".bak"):
                continue
            targets.append(html)

    for path in sorted(targets):
        text = path.read_text(encoding="utf-8")
        if END_MARKER not in text:
            no_marker += 1
            continue
        if GUARD in text:
            already += 1
            continue
        new_text = text.replace(END_MARKER, BLOCK.strip() + "\n" + END_MARKER, 1)
        path.write_text(new_text, encoding="utf-8")
        injected += 1
        print(f"[inject] {path.relative_to(ROOT)}")

    print()
    print(f"  injected:   {injected}")
    print(f"  already:    {already}")
    print(f"  no marker:  {no_marker}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
