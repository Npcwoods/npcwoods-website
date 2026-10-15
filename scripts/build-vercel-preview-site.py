#!/usr/bin/env python3
"""Build a sanitized static site for Vercel preview review.

This does not deploy anything. It copies only reviewable public website files
into an ignored output directory so agents do not upload the full repo,
private drafts, scripts, backups, or credentials to Vercel.

Usage:
    python3 scripts/build-vercel-preview-site.py
    python3 scripts/build-vercel-preview-site.py --page pricing --page uti-care
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from replace_sitewide_tracking import transform
from website_policy import headings, tracker_markers

DEFAULT_OUTPUT = ROOT / "content-output" / "previews" / ("review-" + uuid.uuid4().hex[:12])

PUBLIC_HTML_ROOTS = ("landing-pages", "html")
SKIP_HTML_DIRS = {"shared", "wp-content", "review"}
SUPPORT_FILES = ("smart-content.js", "llms.txt", "llms-full.txt")


@dataclass(frozen=True)
class PageCopy:
    source: Path
    destination: Path
    route: str


def parse_args() -> argparse.Namespace:
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
        "--include-live-tracking",
        action="store_true",
        help="Copy production tracking.js instead of the preview no-op stub. Not the default.",
    )
    parser.add_argument("--json", action="store_true", help="Emit structured preview manifest metadata")
    return parser.parse_args()


def ensure_safe_output(path: Path) -> Path:
    output = path.resolve()
    allowed_root = (ROOT / "content-output" / "previews").resolve()
    if allowed_root not in output.parents and output != allowed_root:
        raise SystemExit(f"[blocked] output must be inside {allowed_root}")
    return output


def clean_output(output: Path) -> None:
    if output.exists():
        raise SystemExit("[blocked] preview output already exists; choose a new task directory")
    output.mkdir(parents=True, exist_ok=False)


def strip_php_template_header(html: str) -> str:
    return re.sub(r"<\?(?:php|=)?.*?\?>", "", html, flags=re.DOTALL)


def route_for_index(root_name: str, source: Path) -> str | None:
    rel = source.relative_to(ROOT / root_name)
    if rel.name != "index.html":
        return None
    if any(part in SKIP_HTML_DIRS for part in rel.parts[:-1]):
        return None
    route_parts = rel.parts[:-1]
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


def copy_text_page(item: PageCopy, output: Path) -> str:
    source_bytes = item.source.read_bytes()
    text = source_bytes.decode("utf-8", errors="replace")
    if item.source.suffix == ".php":
        text = strip_php_template_header(text)
    text = transform(text)
    if "<?" in text or tracker_markers(text):
        raise SystemExit(f"[blocked] unsanitized preview: {item.route}")
    destination = output / item.destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    return hashlib.sha256(source_bytes).hexdigest()


def copy_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    allowed = {".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".avif",
               ".woff", ".woff2", ".ttf", ".ico", ".mp4", ".webm", ".gif"}
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if path.is_symlink():
            raise SystemExit(f"[blocked] symlink in preview assets: {rel}")
        if any(part.startswith(".") for part in rel.parts):
            continue
        if path.is_file() and path.suffix.lower() in allowed:
            dest = destination / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


def write_tracking_stub(output: Path) -> None:
    (output / "tracking.js").write_text(
        """/* NPCWoods Vercel preview: production tracking disabled. */
(function () {
  window.NPCWoodsAttribution = window.NPCWoodsAttribution || {};
  window.gtag = window.gtag || function () {
    if (window.console && console.debug) {
      console.debug("[npcwoods-preview] gtag suppressed", arguments);
    }
  };
  if (window.console && console.info) {
    console.info("[npcwoods-preview] tracking.js is a no-op in review previews");
  }
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
                ],
            }
        ],
        "rewrites": [
            {"source": "/:path((?!.*\\.).*)", "destination": "/:path/index.html"}
        ],
    }
    (output / "vercel.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (output / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")


def write_readme(output: Path, pages: list[PageCopy], live_tracking: bool) -> None:
    page_lines = "\n".join(f"- {page.route} <- {page.source.relative_to(ROOT)}" for page in pages)
    tracking = "production tracking copied" if live_tracking else "production tracking disabled with no-op stub"
    (output / "README.md").write_text(
        f"""# NPCWoods Vercel Review Preview

Generated by `scripts/build-vercel-preview-site.py`.

- Purpose: phone-reviewable Vercel preview only
- Review URL: use the latest Vercel deployment URL; create a temporary share link if Vercel Authentication protects it
- Indexing: blocked by `robots.txt` and `X-Robots-Tag`
- Tracking: {tracking}
- Live deploy: no GoDaddy, WordPress, SFTP, DNS, or production route changed

## Pages

{page_lines}

## Deploy Command

```bash
vercel deploy {output} --yes
```
""",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    if args.include_live_tracking:
        raise SystemExit("[blocked] review previews never include live tracking")
    output = ensure_safe_output(Path(args.output))
    page_filters = {page.strip("/").strip() for page in args.page if page.strip("/").strip()}

    pages = collect_pages(page_filters)
    matched = {page.route.strip("/") or "home" for page in pages}
    missing = page_filters - matched
    if not pages or missing:
        raise SystemExit("[fatal] requested preview routes missing: " + ", ".join(sorted(missing)))
    for page in pages:
        if not page.source.resolve().is_relative_to(ROOT.resolve()):
            raise SystemExit("[blocked] source outside website kitchen")

    clean_output(output)

    source_hashes = {page.route: copy_text_page(page, output) for page in pages}

    copy_tree(ROOT / "assets", output / "assets")
    copy_tree(ROOT / "landing-pages" / "trust-video" / "assets", output / "trust-video" / "assets")
    copy_tree(ROOT / "html" / "wp-content" / "uploads" / "npc-data", output / "wp-content" / "uploads" / "npc-data")

    for filename in SUPPORT_FILES:
        source = ROOT / filename
        if source.exists():
            shutil.copy2(source, output / filename)

    if args.include_live_tracking:
        source = ROOT / "html" / "tracking.js"
        if source.exists():
            shutil.copy2(source, output / "tracking.js")
        else:
            write_tracking_stub(output)
    else:
        write_tracking_stub(output)

    write_vercel_config(output)
    write_readme(output, pages, args.include_live_tracking)

    records = []
    for page in pages:
        preview = output / page.destination
        values = headings(preview.read_text())
        if any(len(values[tag]) != 1 or not values[tag][0] for tag in ("title", "h1")):
            raise SystemExit(f"[blocked] preview needs one title and h1: {page.route}")
        records.append({"route": page.route, "source": str(page.source.relative_to(ROOT)),
                        "destination": str(page.destination),
                        "source_sha256": source_hashes[page.route],
                        "preview_sha256": hashlib.sha256(preview.read_bytes()).hexdigest(),
                        "title": values["title"][0], "h1": values["h1"][0]})
    manifest = output / "preview-manifest.json"
    result = {"schema_version": 1, "output": str(output), "manifest": str(manifest), "pages": records}
    manifest.write_text(json.dumps(result, indent=2) + "\n")
    if args.json:
        print(json.dumps(result))
    else:
        print(f"[prepared] {output}; {len(records)} pages; not published")
        print(f"[manifest] {manifest}")
        print(f"[next, only after preview approval] vercel deploy {output} --yes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
