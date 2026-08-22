#!/usr/bin/env python3
"""Install site Meta Pixel 1428464038973925 before </head> on public HTML."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOTS = ("html", "landing-pages", "blog")
SKIP_PARTS = {"_archive", "content-output", "output", "node_modules", ".git"}
PIXEL_ID = "1428464038973925"
SNIPPET = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1428464038973925');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1428464038973925&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
"""
HEAD_CLOSE_RE = re.compile(r"</head\s*>", re.IGNORECASE)


def target_paths() -> list[Path]:
    paths: list[Path] = []
    for source_root in SOURCE_ROOTS:
        base = ROOT / source_root
        if not base.exists():
            continue
        for path in base.rglob("*.html"):
            if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
                continue
            text = path.read_text(encoding="utf-8")
            if "<html" not in text.lower() or not HEAD_CLOSE_RE.search(text):
                continue
            paths.append(path)
    return sorted(paths)


def transform(html: str) -> str:
    if PIXEL_ID in html:
        return html
    return HEAD_CLOSE_RE.sub(SNIPPET + "</head>", html, count=1)


def main() -> None:
    changed = 0
    for path in target_paths():
        original = path.read_text(encoding="utf-8")
        updated = transform(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[up] {path.relative_to(ROOT)}")
    print(f"updated {changed} files")


if __name__ == "__main__":
    main()
