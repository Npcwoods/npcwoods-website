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


def test_teladoc_uses_current_site_shell():
    html = (LP / "alternatives-to-teladoc/index.html").read_text(encoding="utf-8")
    assert (ROOT / "html/shared/header-snippet.html").read_text(encoding="utf-8").strip() in html
    assert (ROOT / "html/shared/footer-snippet.html").read_text(encoding="utf-8").strip() in html
    assert "11 state licenses" not in html


STALE_FOOTER_LINE = "Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT<br>"
CURRENT_FOOTER_LINE = (
    "Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT, WA, plus Florida by "
    "telehealth registration (TPAN3355). 13 states served.<br>"
)


def test_footer_licensing_line_13_states():
    """Site Audit P1: /learn/, /dental-abscess-treatment/ and the dental-abscess
    series still showed the 11-state footer line live."""
    files = [ROOT / "html/shared/footer-snippet.html", LP / "learn/index.html", LP / "dental-abscess-treatment/index.html"]
    files += sorted((LP / "learn/dental-abscess").glob("**/index.html"))
    assert len(files) == 13
    for f in files:
        t = f.read_text(encoding="utf-8")
        assert STALE_FOOTER_LINE not in t, f
        assert t.count(CURRENT_FOOTER_LINE) == 1, f
        assert "Florida-licensed" not in t, f


def test_learn_meta_pixel_left_exactly_as_live():
    """/learn/ carries the site Meta pixel live (Chris is deciding separately).
    This pin keeps a footer/copy commit from silently adding or removing it.
    If Chris decides to change it, update this test in that same commit."""
    t = (LP / "learn/index.html").read_text(encoding="utf-8")
    assert t.count("fbq('init', '1428464038973925');") == 1
    assert t.count("https://www.facebook.com/tr?id=1428464038973925&ev=PageView&noscript=1") == 1
