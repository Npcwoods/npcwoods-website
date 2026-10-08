"""2026-10-08 jobs: UTI CTR rewrite, /alternatives-to-teladoc/ launch, nav 13-state credentials."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LP = ROOT / "landing-pages"
FORBIDDEN_TRACKING = ("googletagmanager", "gtag(", "fbq('init", "fbevents.js", "google-analytics.com")


def _head(html):
    return html.split("</head>", 1)[0]


def test_uti_ctr_title_and_meta():
    html = (LP / "uti-treatment/how-fast-do-uti-antibiotics-work/index.html").read_text(encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
    desc = re.search(r'<meta name="description" content="([^"]+)"', html).group(1)
    assert len(title) <= 60 and "24" in title
    assert 120 <= len(desc) <= 160
    assert re.search(r'<meta property="og:title" content="%s"' % re.escape(title), html)
    assert re.search(r'<meta property="og:description" content="%s"' % re.escape(desc), html)
    assert "How fast do UTI antibiotics work?" in html  # H1 unchanged
    for bad in ("physician", "doctor", " MD", "insurance"):
        assert bad.lower() not in (title + desc).lower()


def test_teladoc_page_ready():
    html = (LP / "alternatives-to-teladoc/index.html").read_text(encoding="utf-8")
    head = _head(html)
    canon = re.findall(r'<link rel="canonical" href="([^"]+)"', head)
    assert canon == ["https://npcwoods.com/alternatives-to-teladoc/"]
    assert "noindex" not in head
    for bad in FORBIDDEN_TRACKING:
        assert bad not in html


def test_teladoc_in_sitemap_and_linked_from_faq():
    php = (ROOT / "php/npcwoods-sitemap-hygiene.php").read_text(encoding="utf-8")
    assert "'/alternatives-to-teladoc/'" in php
    faq = (LP / "faq/index.html").read_text(encoding="utf-8")
    assert 'href="https://npcwoods.com/alternatives-to-teladoc/"' in faq


def test_nav_credentials_13_states():
    files = [ROOT / "html/shared/header-snippet.html", LP / "learn/index.html", LP / "dental-abscess-treatment/index.html"]
    files += sorted((LP / "learn/dental-abscess").glob("**/index.html"))
    for f in files:
        t = f.read_text(encoding="utf-8")
        assert "11 state licenses" not in t, f
        assert "NPI, board cert, 13 states (FL by telehealth reg.)" in t, f
        assert "Florida-licensed" not in t, f
