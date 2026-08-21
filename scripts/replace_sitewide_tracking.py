#!/usr/bin/env python3
"""Remove third-party tracking from public website sources.

The public site contains static HTML pages that bypass WordPress hooks. This
script removes the retired Meta Pixel and legacy third-party tracking from
every locally served HTML page plus the homepage PHP template. It is
idempotent and defaults to a no-write preview; use --apply to write.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOTS = ("html", "landing-pages", "blog")
SKIP_PARTS = {"_archive", "content-output", "output", "node_modules", ".git"}
HOMEPAGE_TEMPLATE = Path("homepage/page-npcwoods-home.php")
LEGACY_TRACKING_ASSETS = (Path("html/tracking.js"), Path("html/shared/tracking.js"))

INERT_LEGACY_TRACKING_ASSET = """/**
 * Legacy tracking disabled.
 *
 * Public pages do not load third-party tracking.
 */
(function () {
  'use strict';
})();
"""

META_BLOCK_RE = re.compile(
    r"[ \t]*<!-- Meta Pixel Code -->.*?<!-- End Meta Pixel Code -->\n?", re.IGNORECASE | re.DOTALL
)
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.IGNORECASE | re.DOTALL)
NOSCRIPT_RE = re.compile(r"<noscript\b[^>]*>.*?</noscript\s*>", re.IGNORECASE | re.DOTALL)
LINK_RE = re.compile(r"<link\b[^>]*>", re.IGNORECASE | re.DOTALL)
PIXEL_IMAGE_RE = re.compile(
    r"<img\b[^>]*\bsrc\s*=\s*(['\"])\s*https?://(?:www\.)?facebook\.com/tr(?:[/?])[^'\"]*\1[^>]*>",
    re.IGNORECASE,
)
HEAD_CLOSE_RE = re.compile(r"</head\s*>", re.IGNORECASE)

TRACKER_MARKERS = re.compile(
    r"googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|"
    r"(?:^|[^\w])gtag\s*\(|(?:^|[^\w])dataLayer\s*=|"
    r"connect\.facebook\.net/en_US/fbevents\.js|facebook\.com/tr|(?:^|[^\w])fbq\s*\(|window\.fbq\s*=|"
    r"(?:^|[/'\"])tracking\.js(?:[?'\"]|$)",
    re.IGNORECASE,
)


def is_tracking_script(match: re.Match[str]) -> bool:
    return bool(TRACKER_MARKERS.search(match.group(0)))


def is_tracking_noscript(match: re.Match[str]) -> bool:
    return bool(TRACKER_MARKERS.search(match.group(0)) or "facebook.com/tr" in match.group(0).lower())


def is_tracking_link(match: re.Match[str]) -> bool:
    return bool(TRACKER_MARKERS.search(match.group(0)))


def transform(html: str) -> str:
    """Return public HTML with no active Meta or legacy third-party tracker."""
    if not HEAD_CLOSE_RE.search(html):
        return html

    html = META_BLOCK_RE.sub("", html)
    html = SCRIPT_RE.sub(lambda match: "" if is_tracking_script(match) else match.group(0), html)
    html = NOSCRIPT_RE.sub(lambda match: "" if is_tracking_noscript(match) else match.group(0), html)
    html = LINK_RE.sub(lambda match: "" if is_tracking_link(match) else match.group(0), html)
    html = PIXEL_IMAGE_RE.sub("", html)
    return html


def target_paths(root: Path = ROOT) -> list[Path]:
    paths: list[Path] = []
    for source_root in SOURCE_ROOTS:
        base = root / source_root
        if not base.exists():
            continue
        for path in base.rglob("*.html"):
            if any(part in SKIP_PARTS for part in path.relative_to(root).parts):
                continue
            text = path.read_text(encoding="utf-8")
            if "<html" not in text.lower() or "</head" not in text.lower():
                continue
            paths.append(path)
    homepage = root / HOMEPAGE_TEMPLATE
    if homepage.exists():
        paths.append(homepage)
    return sorted(set(paths))


def verify(path: Path, html: str) -> None:
    forbidden = (
        "1558261907814968",
        "1428464038973925",
        "connect.facebook.net",
        "facebook.com/tr",
        "fbq(",
        "googletagmanager.com",
        "gtag/js?id=",
        "google-analytics.com",
        "googleadservices.com",
        "doubleclick.net",
        "window.fbq = function",
    )
    for marker in forbidden:
        if marker in html:
            raise RuntimeError(f"{path}: legacy tracking marker remains: {marker}")
    if re.search(r"<script\b[^>]*\bsrc\s*=\s*(['\"])[^'\"]*/tracking\.js[^'\"]*\1", html, re.IGNORECASE):
        raise RuntimeError(f"{path}: legacy tracking.js script remains")


def verify_legacy_tracking_asset(path: Path, source: str) -> None:
    if re.search(r"\b(?:gtag|fbq)\s*\(", source):
        raise RuntimeError(f"{path}: outbound tracking call remains")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes (default is a preview)")
    args = parser.parse_args()

    changed = 0
    unchanged = 0
    for path in target_paths():
        original = path.read_text(encoding="utf-8")
        updated = transform(original)
        verify(path, updated)
        if updated == original:
            unchanged += 1
            continue
        changed += 1
        if args.apply:
            path.write_text(updated, encoding="utf-8")

    for relative_path in LEGACY_TRACKING_ASSETS:
        path = ROOT / relative_path
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = INERT_LEGACY_TRACKING_ASSET
        verify_legacy_tracking_asset(path, updated)
        if updated == original:
            unchanged += 1
            continue
        changed += 1
        if args.apply:
            path.write_text(updated, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"{mode}: {changed} page sources need changes, {unchanged} already match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
