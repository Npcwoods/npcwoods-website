#!/usr/bin/env python3
"""Build a sanitized static site for Vercel preview review.

This does not deploy anything. It copies only reviewable public website files
into an ignored output directory so agents do not upload the full repo,
private drafts, scripts, backups, or credentials to Vercel.

Usage:
    python3 scripts/build-vercel-preview-site.py
    python3 scripts/build-vercel-preview-site.py --page pricing --page uti-care
    python3 scripts/build-vercel-preview-site.py --export-root /path/to/npcwoods-website-export
"""

from __future__ import annotations

import argparse
from html import escape
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "content-output" / "previews" / "vercel-review-site"
DEFAULT_EXPORT_ROOT = Path("/Users/macmini/.buzz/REPOS/npcwoods-website-export")

PUBLIC_HTML_ROOTS = ("landing-pages", "html")
SKIP_HTML_DIRS = {"shared", "wp-content", "review"}
SUPPORT_FILES = ("smart-content.js", "llms.txt", "llms-full.txt")

PREVIEW_SCRIPT_MARKERS = (
    "googletagmanager.com",
    "google-analytics.com",
    "connect.facebook.net",
    "facebook.com/tr",
    "gtm-",
    "gtag(",
    "fbq(",
    "datalayer",
)

PREVIEW_PAYMENT_MARKERS = (
    "buy.stripe.com",
    "checkout.stripe.com",
    "stripebaseurl",
    "window.location.replace(finalurl",
)

PREVIEW_REDIRECT_MARKERS = (
    "window.location.replace(",
    "window.location.assign(",
    "location.replace(",
    "location.assign(",
)


@dataclass(frozen=True)
class PageCopy:
    source: Path
    destination: Path
    route: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a sanitized Vercel preview directory from NPCWoods website source."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output directory. Must live inside npcwoods-website/content-output/previews/.",
    )
    parser.add_argument(
        "--page",
        action="append",
        default=[],
        help=(
            "Limit output to one route slug, e.g. pricing, uti-treatment/mesa-az, "
            "learn/strep-throat. Can be passed multiple times."
        ),
    )
    parser.add_argument(
        "--export-root",
        default=str(DEFAULT_EXPORT_ROOT),
        help=(
            "Read-only staging export containing blog/<slug>/index.html and "
            "assets/uploads/. Missing roots are skipped."
        ),
    )
    return parser.parse_args(argv)


def ensure_safe_output(path: Path) -> Path:
    output = path.resolve()
    allowed_root = (ROOT / "content-output" / "previews").resolve()
    if allowed_root not in output.parents and output != allowed_root:
        raise SystemExit(f"[blocked] output must be inside {allowed_root}")
    return output


def clean_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)


def strip_php_template_header(html: str) -> str:
    return re.sub(r"^\s*<\?php.*?\?>\s*", "", html, flags=re.DOTALL)


def shared_snippet(name: str) -> str:
    for candidate in (
        ROOT / "html" / "shared" / name,
        ROOT / "shared" / name,
    ):
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8", errors="replace")
    return ""


def render_static_homepage(source: Path) -> str:
    """Render the PHP-only homepage into a browser-deliverable HTML document."""

    text = strip_php_template_header(source.read_text(encoding="utf-8", errors="replace"))
    text = re.sub(
        r"<\?php\s*if\s*\(function_exists\(['\"]wp_head['\"]\)\)\s*\{\s*wp_head\(\);\s*\}\s*\?>",
        "",
        text,
        flags=re.I,
    )

    header_block = re.compile(
        r"<\?php\s*\$npcwoods_header_rendered\b.*?<\?php\s*endif\s*;\s*\?>",
        re.I | re.S,
    )
    footer_block = re.compile(
        r"<\?php\s*\$npcwoods_footer_rendered\b.*?<\?php\s*endif\s*;\s*\?>",
        re.I | re.S,
    )
    text = header_block.sub(shared_snippet("header-snippet.html"), text, count=1)
    text = footer_block.sub(shared_snippet("footer-snippet.html"), text, count=1)
    text = re.sub(
        r"<\?php\s*if\s*\(function_exists\(['\"]wp_footer['\"]\)\)\s*\{\s*wp_footer\(\);\s*\}\s*\?>",
        "",
        text,
        flags=re.I,
    )
    if "<?php" in text:
        raise ValueError(f"unhandled PHP remains in static homepage source: {source}")
    return text


def route_for_index(root_name: str, source: Path) -> str | None:
    rel = source.relative_to(ROOT / root_name)
    if rel.name != "index.html":
        return None
    if any(part in SKIP_HTML_DIRS for part in rel.parts[:-1]):
        return None
    route_parts = rel.parts[:-1]
    # WordPress serves this standalone source at the public page slug; the
    # legacy /experience/ path is handled by the 301 map.
    if root_name == "html" and route_parts == ("experience",):
        return "patient-experience"
    return "/".join(route_parts)


def collect_pages(page_filters: set[str]) -> list[PageCopy]:
    pages: list[PageCopy] = []
    seen_routes: set[str] = set()

    homepage = ROOT / "homepage" / "page-npcwoods-home.php"
    if homepage.exists() and (not page_filters or "" in page_filters or "home" in page_filters):
        pages.append(PageCopy(source=homepage, destination=Path("index.html"), route="/"))
        seen_routes.add("")

    for root_name in PUBLIC_HTML_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for source in sorted(root.rglob("index.html")):
            route = route_for_index(root_name, source)
            if route is None:
                continue
            if page_filters and route not in page_filters:
                continue
            if route in seen_routes:
                print(f"[skip] duplicate route {route}: {source.relative_to(ROOT)}")
                continue
            seen_routes.add(route)
            pages.append(PageCopy(source=source, destination=Path(route) / "index.html", route=f"/{route}/"))

    return pages


def script_is_json(script_attrs: str) -> bool:
    script_type = re.search(r"\btype\s*=\s*[\"']([^\"']+)", script_attrs, re.I)
    return bool(script_type and script_type.group(1).lower() in {"application/ld+json", "application/json"})


def script_has_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def sanitize_preview_html(html: str, output: Path | None = None, localize_assets: bool = False) -> str:
    """Remove executable production tracking/payment blocks from review HTML.

    JSON-LD is data, not executable tracking, so it is retained. Site-wide
    navigation JavaScript remains available when it does not contain a known
    production marker. Asset localization is intentionally limited to files
    that exist in the generated preview; normal external links are untouched.
    """

    script_pattern = re.compile(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script\s*>", re.I | re.S)

    def replace_script(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        block = match.group(0)
        src_match = re.search(r"\bsrc\s*=\s*[\"']([^\"']+)", attrs, re.I)
        src = src_match.group(1) if src_match else ""

        if script_is_json(attrs):
            return block
        if script_has_marker(block, PREVIEW_PAYMENT_MARKERS):
            return "<!-- preview: live payment navigation disabled -->"
        if script_has_marker(block, PREVIEW_REDIRECT_MARKERS):
            return "<!-- preview: live redirect navigation disabled -->"
        if src and "tracking.js" in src.lower():
            rewritten_attrs = re.sub(
                r"(\bsrc\s*=\s*[\"'])[^\"']*tracking\.js(?:\?[^\"']*)?([\"'])",
                r"\1/tracking.js\2",
                attrs,
                flags=re.I,
            )
            return f"<script{rewritten_attrs}>{body}</script>"
        if script_has_marker(block, PREVIEW_SCRIPT_MARKERS):
            return "<!-- preview: production analytics script disabled -->"
        return block

    html = script_pattern.sub(replace_script, html)
    noscript_pattern = re.compile(r"<noscript\b[^>]*>.*?</noscript\s*>", re.I | re.S)
    html = noscript_pattern.sub(
        lambda match: "<!-- preview: production tag iframe disabled -->"
        if script_has_marker(match.group(0), PREVIEW_SCRIPT_MARKERS)
        else match.group(0),
        html,
    )
    html = re.sub(
        r"<link\b[^>]+(?:googletagmanager\.com|google-analytics\.com|connect\.facebook\.net|facebook\.com)[^>]*>",
        "<!-- preview: production analytics preconnect disabled -->",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<meta\b[^>]+\bhttp-equiv\s*=\s*[\"']refresh[\"'][^>]*>",
        "<!-- preview: live meta refresh disabled -->",
        html,
        flags=re.I,
    )

    if localize_assets and output is not None:
        html = localize_export_asset_urls(html, output)
    return html


def localize_export_asset_urls(html: str, output: Path) -> str:
    """Localize only present npcwoods.com asset URLs in exported HTML."""

    # One exported post contains a doubled domain in the upload path. Normalize
    # that known export artifact before checking the copied asset path.
    html = html.replace(
        "https://npcwoods.com/wp-content/uploads/2026/06/https://npcwoods.com/wp-content/uploads/",
        "https://npcwoods.com/wp-content/uploads/",
    )
    asset_pattern = re.compile(
        r"https://npcwoods\.com/(?P<kind>wp-content/uploads|assets)/(?P<path>[A-Za-z0-9._~!$&'()*+,;=@%/-]+)",
        re.I,
    )

    def replace_asset(match: re.Match[str]) -> str:
        kind = match.group("kind")
        relative_path = Path(match.group("path"))
        destination = output / kind / relative_path
        if not destination.is_file():
            return match.group(0)
        return f"/{kind}/{relative_path.as_posix()}"

    # Structured data must retain absolute public URLs. Localize markup between
    # script blocks, but never rewrite JSON-LD or other script contents.
    script_pattern = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.I | re.S)
    pieces: list[str] = []
    cursor = 0
    for script_match in script_pattern.finditer(html):
        pieces.append(asset_pattern.sub(replace_asset, html[cursor : script_match.start()]))
        pieces.append(script_match.group(0))
        cursor = script_match.end()
    pieces.append(asset_pattern.sub(replace_asset, html[cursor:]))
    return "".join(pieces)


def copy_text_page(item: PageCopy, output: Path, exported: bool = False) -> None:
    if item.route == "/" and item.source.suffix == ".php":
        text = render_static_homepage(item.source)
    else:
        text = item.source.read_text(encoding="utf-8", errors="replace")
    if item.source.suffix == ".php" and item.route != "/":
        text = strip_php_template_header(text)
    text = sanitize_preview_html(
        text,
        output=output,
        localize_assets=exported or item.route == "/",
    )
    destination = output / item.destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def copy_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            ".git",
            ".vercel",
            ".DS_Store",
            "__pycache__",
            "*.bak",
            "*.bak-*",
            "*.bak.*",
            "*.pyc",
            "*.log",
        ),
    )


def collect_export_pages(export_root: Path, page_filters: set[str]) -> list[PageCopy]:
    """Map export blog/<slug>/index.html to the live root-level post URL."""

    blog_root = export_root / "blog"
    if not blog_root.exists():
        return []

    pages: list[PageCopy] = []
    for source in sorted(blog_root.rglob("index.html")):
        relative = source.relative_to(blog_root)
        route_parts = relative.parts[:-1]
        if not route_parts:
            continue
        route = "/".join(route_parts)
        if page_filters and route not in page_filters:
            continue
        pages.append(PageCopy(source=source, destination=Path(route) / "index.html", route=f"/{route}/"))
    return pages


def collect_export_content_pages(export_root: Path, page_filters: set[str]) -> list[PageCopy]:
    """Map exported pages/<path>/index.html to their live route paths."""

    pages_root = export_root / "pages"
    if not pages_root.exists():
        return []

    pages: list[PageCopy] = []
    for source in sorted(pages_root.rglob("index.html")):
        relative = source.relative_to(pages_root)
        route_parts = relative.parts[:-1]
        route = "/".join(route_parts)
        if page_filters and route not in page_filters and not (not route and "home" in page_filters):
            continue
        destination = Path("index.html") if not route else Path(route) / "index.html"
        pages.append(PageCopy(source=source, destination=destination, route=f"/{route}/" if route else "/"))
    return pages


def copy_export_assets(export_root: Path, output: Path) -> None:
    copy_tree(export_root / "assets" / "uploads", output / "wp-content" / "uploads")


def export_post_metadata(page: PageCopy) -> tuple[str, str, str]:
    """Read stable archive fields from an exported post without rewriting it."""

    text = page.source.read_text(encoding="utf-8", errors="replace")
    title_match = re.search(r"<title\b[^>]*>(.*?)</title\s*>", text, re.I | re.S)
    date_match = re.search(
        r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']+)',
        text,
        re.I,
    )
    canonical_match = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)',
        text,
        re.I,
    )
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else page.route.strip("/")
    published = date_match.group(1).strip() if date_match else ""
    canonical = canonical_match.group(1).strip() if canonical_match else f"https://npcwoods.com{page.route}"
    return title, published, canonical


def write_blog_archive(export_pages: list[PageCopy], output: Path) -> None:
    """Generate the static /blog/ archive and paginated archive pages."""

    if not export_pages:
        return
    posts = []
    for page in export_pages:
        title, published, _canonical = export_post_metadata(page)
        posts.append((published, page.route, title))
    posts.sort(key=lambda item: (item[0], item[1]), reverse=True)

    page_size = 20
    total_pages = (len(posts) + page_size - 1) // page_size
    header = shared_snippet("header-snippet.html")
    footer = shared_snippet("footer-snippet.html")
    for page_number in range(total_pages):
        route = "/blog/" if page_number == 0 else f"/blog/page/{page_number + 1}/"
        canonical = f"https://npcwoods.com{route}"
        cards = []
        for published, post_route, title in posts[page_number * page_size : (page_number + 1) * page_size]:
            date = escape(published[:10]) if published else ""
            date_markup = f'<time datetime="{date}">{date}</time>' if date else ""
            cards.append(
                f'<article class="blog-archive-card"><h2><a href="{escape(post_route)}">{escape(title)}</a></h2>{date_markup}</article>'
            )
        previous = ""
        if page_number == 1:
            previous = '<link rel="prev" href="https://npcwoods.com/blog/">'
        elif page_number > 1:
            previous = f'<link rel="prev" href="https://npcwoods.com/blog/page/{page_number}/">'
        next_link = (
            ""
            if page_number + 1 >= total_pages
            else f'<link rel="next" href="https://npcwoods.com/blog/page/{page_number + 2}/">'
        )
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NPCWoods Telemedicine Blog</title>
  <meta name="description" content="Practical telemedicine and urgent-care guidance from NPCWoods Telemedicine.">
  <link rel="canonical" href="{canonical}">
  {previous}
  {next_link}
  <style>
    .blog-archive-main {{ max-width: 960px; margin: 0 auto; padding: 48px 20px 80px; font-family: Inter, system-ui, sans-serif; }}
    .blog-archive-main h1 {{ margin: 0 0 12px; font-size: clamp(2rem, 5vw, 3.4rem); }}
    .blog-archive-intro {{ color: #57524A; margin: 0 0 32px; max-width: 55ch; }}
    .blog-archive-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .blog-archive-card {{ border: 1px solid #e3e3ea; border-radius: 14px; padding: 22px; background: #fff; }}
    .blog-archive-card h2 {{ margin: 0 0 12px; font-size: 1.15rem; line-height: 1.3; }}
    .blog-archive-card a {{ color: #2563EB; text-decoration: none; }}
    .blog-archive-card time {{ color: #6b7280; font-size: .9rem; }}
  </style>
</head>
<body>
{header}
<main class="blog-archive-main">
  <h1>NPCWoods Telemedicine Blog</h1>
  <p class="blog-archive-intro">Clear, practical guidance for common health questions, text-based care, and knowing when to get checked.</p>
  <section class="blog-archive-grid" aria-label="Blog posts">
    {"".join(cards)}
  </section>
</main>
{footer}
</body>
</html>
"""
        destination = output / route.strip("/") / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            sanitize_preview_html(html, output=output, localize_assets=True),
            encoding="utf-8",
        )


def write_tracking_stub(output: Path) -> None:
    (output / "tracking.js").write_text(
        """/* NPCWoods Vercel preview: production tracking disabled. */
(function () {
  window.__NPCWOODS_PREVIEW__ = true;
  window.dataLayer = window.dataLayer || [];
  window.NPCWoodsAttribution = window.NPCWoodsAttribution || {};
  window.gtag = window.gtag || function () {
    return undefined;
  };
  window.fbq = window.fbq || function () { return undefined; };
  window._fbq = window._fbq || window.fbq;
})();
""",
        encoding="utf-8",
    )


def write_vercel_config(output: Path) -> None:
    config = {
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Robots-Tag", "value": "noindex, nofollow, noarchive"},
                    {"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"},
                    {
                        "key": "Content-Security-Policy",
                        "value": (
                            "default-src 'self' https: data:; script-src 'self'; "
                            "connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'self'"
                        ),
                    },
                ],
            }
        ],
        "rewrites": [
            {"source": "/:path((?!.*\\.).*)", "destination": "/:path/index.html"}
        ],
    }
    migration_draft = ROOT / "vercel.migration.draft.json"
    if migration_draft.is_file():
        draft = json.loads(migration_draft.read_text(encoding="utf-8"))
        config["redirects"] = draft.get("redirects", [])
    (output / "vercel.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (output / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")


def write_readme(output: Path, pages: list[PageCopy]) -> None:
    def source_label(page: PageCopy) -> str:
        try:
            return str(page.source.relative_to(ROOT))
        except ValueError:
            return str(page.source)

    page_lines = "\n".join(f"- {page.route} <- {source_label(page)}" for page in pages)
    (output / "README.md").write_text(
        f"""# NPCWoods Vercel Review Preview

Generated by `scripts/build-vercel-preview-site.py`.

- Purpose: phone-reviewable Vercel preview only
- Review URL: use the latest Vercel deployment URL; create a temporary share link if Vercel Authentication protects it
- Indexing: blocked by `robots.txt` and `X-Robots-Tag`
- Tracking: production tracking disabled with a no-op stub
- Live deploy: no GoDaddy, WordPress, SFTP, DNS, or production route changed

## Pages

{page_lines}

## Deploy Command

```bash
vercel deploy content-output/previews/vercel-review-site -y --no-wait
```
""",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = ensure_safe_output(Path(args.output))
    page_filters = {page.strip("/").strip() for page in args.page if page.strip("/").strip()}

    pages = collect_pages(page_filters)
    export_root = Path(args.export_root).expanduser()
    export_pages = collect_export_pages(export_root, page_filters) if export_root.is_dir() else []
    export_content_pages = (
        collect_export_content_pages(export_root, page_filters) if export_root.is_dir() else []
    )
    if export_content_pages or export_pages:
        pages.extend(export_content_pages)
        pages.extend(export_pages)
    if not pages:
        raise SystemExit("[fatal] no pages matched the requested filters")

    clean_output(output)

    copy_tree(ROOT / "assets", output / "assets")
    copy_tree(ROOT / "landing-pages" / "trust-video" / "assets", output / "trust-video" / "assets")
    copy_tree(ROOT / "html" / "wp-content" / "uploads" / "npc-data", output / "wp-content" / "uploads" / "npc-data")
    copy_export_assets(export_root, output)

    exported_pages = set(export_pages + export_content_pages)
    for page in pages:
        copy_text_page(page, output, exported=page in exported_pages)
    write_blog_archive(export_pages, output)

    for filename in SUPPORT_FILES:
        source = ROOT / filename
        if source.exists():
            shutil.copy2(source, output / filename)

    write_tracking_stub(output)

    write_vercel_config(output)
    write_readme(output, pages)

    print(f"[ok] built Vercel review preview: {output}")
    print(f"[ok] pages: {len(pages)}")
    print("[next] vercel deploy content-output/previews/vercel-review-site -y --no-wait")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
