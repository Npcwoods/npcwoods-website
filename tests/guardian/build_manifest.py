#!/usr/bin/env python3
"""Build tests/guardian/manifest.json — the list of live marketing pages on npcwoods.com.

Sources of truth (all derived from this repo, never the live site):
  1. mu-plugin routing maps in php/*.php  (slug => html file, or /path/ => html file)
  2. Filesystem walk for */search-safe/ paid LPs (served directly by Apache,
     no mu-plugin routing needed because the real directory exists in the docroot)
  3. Manual core pages (homepage)

Refresh whenever pages are added:
    python3 tests/guardian/build_manifest.py

Output: tests/guardian/manifest.json with per-page metadata:
    url, local_source, exists_locally, is_health_page, is_paid_lp, kind, routed_by
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = Path(__file__).resolve().parent / "manifest.json"
BASE = "https://npcwoods.com"

# mu-plugin files that contain genuine page routing maps (slug/path => html file).
# Excludes redirects, schema, headers, tracking, payment-link etc. whose arrays
# are not routing tables.
ROUTING_PLUGINS = [
    "npcwoods-static-pages.php",
    "npcwoods-education-pages.php",
    "npcwoods-dental-pages.php",
    "npcwoods-pharmacy-pages.php",
    "npcwoods-paid-pages.php",
    "npcwoods-llmseo-pages.php",
    "npcwoods-ga-nc-pages.php",
    "npcwoods-glp1-pages.php",
    "npcwoods-about-pages.php",
    "npcwoods-affordable-arizona-page.php",
    "npcwoods-comparison-pages.php",
    "npcwoods-experience-page.php",
    "npcwoods-review-page.php",
]

# 'slug' => 'path/to/index.html'   or   '/full/path/' => 'path/to/index.html'
MAP_RE = re.compile(
    r"""['"](?P<key>/?[a-z0-9\-/]+?)['"]\s*=>\s*['"](?P<val>[a-z0-9\-/_.]+\.html)['"]""",
    re.IGNORECASE,
)

# URL substrings that mark a page as a health/condition/treatment/medication
# surface (zero Meta pixel tolerance — see memory/meta-pixel-removal.md).
HEALTH_MARKERS = (
    "uti",
    "sinus",
    "strep",
    "ear-infection",
    "tooth",
    "dental",
    "/learn/",
    "/medications/",
    "ed-treatment",
    "glp1",
    "yeast",
    "antibiotics",
    "/conditions/",
    "poison-ivy",
)

# WP slugs whose live URL differs from the slug used in the routing map key.
SLUG_URL_OVERRIDES = {
    "patient-experience": "/patient-experience/",
}


def classify_kind(url_path: str, is_paid: bool) -> str:
    if is_paid:
        return "paid-lp"
    if url_path == "/":
        return "core"
    if "/learn/" in url_path:
        return "education"
    if "/medications/" in url_path:
        return "medication"
    if "-telemedicine/" in url_path:
        return "state"
    if any(url_path.endswith(s) for s in ("-ga/", "-nc/", "-az/", "-nm/")):
        return "city"
    if is_health(url_path):
        return "condition"
    return "core"


def is_health(url_path: str) -> bool:
    p = url_path.lower()
    return any(m in p for m in HEALTH_MARKERS)


def resolve_local(val: str) -> Path | None:
    for base in ("landing-pages", "html"):
        candidate = REPO_ROOT / base / val
        if candidate.exists():
            return candidate.relative_to(REPO_ROOT)
    return None


def main() -> int:
    pages: dict[str, dict] = {}

    def add(url_path: str, local: str | None, routed_by: str) -> None:
        if not url_path.startswith("/"):
            url_path = "/" + url_path
        if not url_path.endswith("/"):
            url_path += "/"
        url = BASE + url_path
        if url in pages:
            return
        is_paid = "/search-safe/" in url_path or url_path == "/uti-care/"
        health = is_health(url_path)
        local_path = resolve_local(local) if local else None
        pages[url] = {
            "url": url,
            "local_source": str(local_path) if local_path else (local or None),
            "exists_locally": local_path is not None,
            "is_health_page": health,
            "is_paid_lp": is_paid,
            "kind": classify_kind(url_path, is_paid),
            "routed_by": routed_by,
        }

    # 1. Homepage + WP-native core pages not covered by routing maps
    add("/", "homepage/page-npcwoods-home.php", "manual:wordpress-template")
    pages[BASE + "/"]["exists_locally"] = (
        REPO_ROOT / "homepage/page-npcwoods-home.php"
    ).exists()
    add("/faq/", "faq/index.html", "npcwoods-faq-page.php")

    # 2. mu-plugin routing maps
    php_dir = REPO_ROOT / "php"
    for name in ROUTING_PLUGINS:
        php_file = php_dir / name
        if not php_file.exists():
            print(f"WARN: routing plugin missing: {php_file}", file=sys.stderr)
            continue
        text = php_file.read_text(encoding="utf-8", errors="replace")
        for m in MAP_RE.finditer(text):
            key, val = m.group("key"), m.group("val")
            if key.startswith("/"):
                url_path = key  # llmseo path-style routing
            elif name == "npcwoods-education-pages.php":
                # Education pages route by WP child-page slug but live under
                # /learn/* and /medications/* — the html file path mirrors the
                # live URL (verified live: /strep-throat/ 301s to /learn/strep-throat/).
                url_path = "/" + val.rsplit("/index.html", 1)[0] + "/"
            else:
                url_path = SLUG_URL_OVERRIDES.get(key, f"/{key}/")
            add(url_path, val, name)

    # 3. Paid search-safe LPs — served straight from the docroot, no routing map
    for f in sorted((REPO_ROOT / "landing-pages").rglob("search-safe/index.html")):
        rel = f.relative_to(REPO_ROOT / "landing-pages")
        url_path = "/" + str(rel.parent).replace("\\", "/") + "/"
        add(url_path, str(f.relative_to(REPO_ROOT)), "filesystem:docroot-static")
        pages[BASE + url_path]["local_source"] = str(f.relative_to(REPO_ROOT))
        pages[BASE + url_path]["exists_locally"] = True

    entries = sorted(pages.values(), key=lambda p: p["url"])
    summary = {
        "total": len(entries),
        "health_pages": sum(1 for p in entries if p["is_health_page"]),
        "paid_lps": sum(1 for p in entries if p["is_paid_lp"]),
        "other": sum(
            1 for p in entries if not p["is_health_page"] and not p["is_paid_lp"]
        ),
    }
    manifest = {
        "base_url": BASE,
        "generated_by": "tests/guardian/build_manifest.py",
        "summary": summary,
        "pages": entries,
    }
    OUT_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUT_PATH} — {summary['total']} pages "
        f"({summary['health_pages']} health, {summary['paid_lps']} paid LP, "
        f"{summary['other']} other)"
    )
    missing = [p["url"] for p in entries if not p["exists_locally"]]
    if missing:
        print(f"Pages routed on server but with no local source ({len(missing)}):")
        for u in missing:
            print(f"  - {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
