#!/usr/bin/env python3
"""Verify the local Ahrefs crawl-waste cleanup before deployment.

Default mode is local-only: it checks redirect mappings and source hrefs.
Use --live after Chris approves deployment to check live HTTP status/Location.
"""
from __future__ import annotations

import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://npcwoods.com"

REDIRECT_FILES = [
    ROOT / "php" / "npcwoods-redirects.php",
    ROOT / "php" / "npcwoods-redirects-404-cleanup.php",
]

SAMPLED_REDIRECTS = {
    "/tucson-az-sinus/": "/sinus-infection-treatment/",
    "/glendale-az-strep/": "/strep-throat-ear-infection/",
    "/gilbert-telemedicine/": "/arizona-telemedicine/",
    "/surprise-az-strep/": "/strep-throat-ear-infection/",
    "/learn/hives/": "/learn/allergic-reaction/",
    "/scottsdale-telemedicine/": "/arizona-telemedicine/",
    "/tucson-az-strep/": "/strep-throat-ear-infection/",
    "/glendale-az-telemedicine/": "/arizona-telemedicine/",
    "/learn/acne/": "/learn/skin-infection/",
    "/tempe-telemedicine/": "/arizona-telemedicine/",
}

CHAIN_REDIRECTS = {
    "/phoenix-telemedicine/": "/arizona-telemedicine/",
    "/home/phoenix-telemedicine/": "/arizona-telemedicine/",
}

SOURCE_HREF_BLOCKLIST = {
    "landing-pages/arizona-telemedicine/index.html": [
        "/mesa-telemedicine/",
        "/scottsdale-telemedicine/",
        "/surprise-telemedicine/",
        "/phoenix-telemedicine/",
        "/tucson-telemedicine/",
        "/chandler-telemedicine/",
        "/gilbert-telemedicine/",
        "/glendale-az-telemedicine/",
        "/tempe-telemedicine/",
        "/peoria-az-telemedicine/",
    ],
    "landing-pages/sinus-infection-treatment/index.html": [
        "/mesa-sinus-infection/",
        "/scottsdale-sinus-infection/",
        "/surprise-sinus-infection/",
        "/phoenix-sinus-infection/",
        "/tucson-sinus-infection/",
    ],
    "landing-pages/medications/augmentin/index.html": [
        "/learn/respiratory-infection/",
    ],
    "landing-pages/medications/clindamycin/index.html": [
        "/learn/abscesses/",
        "/learn/acne/",
        "/learn/respiratory-infection/",
    ],
    "landing-pages/medications/prednisone/index.html": [
        "/learn/hives/",
    ],
    "landing-pages/learn/sinus-infection/index.html": [
        "/learn/cold-flu/",
    ],
    "blog/no-insurance-no-problem.html": [
        "/experience/",
    ],
    "llms.txt": [
        "/experience/",
    ],
    "llms-full.txt": [
        "/experience/",
    ],
    "automation-output/daily-blog/drafts/post-5-telehealth-safe-legitimate-wp-body.html": [
        "/experience/",
    ],
}

LIVE_SOURCE_BLOCKLIST = {
    "/": ["/experience/", "https://npcwoods.com/experience/"],
    "/blog/": ["/experience/", "https://npcwoods.com/experience/"],
    "/arizona-telemedicine/": SOURCE_HREF_BLOCKLIST["landing-pages/arizona-telemedicine/index.html"],
    "/sinus-infection-treatment/": SOURCE_HREF_BLOCKLIST[
        "landing-pages/sinus-infection-treatment/index.html"
    ],
    "/medications/augmentin/": SOURCE_HREF_BLOCKLIST[
        "landing-pages/medications/augmentin/index.html"
    ],
    "/medications/clindamycin/": SOURCE_HREF_BLOCKLIST[
        "landing-pages/medications/clindamycin/index.html"
    ],
    "/medications/prednisone/": SOURCE_HREF_BLOCKLIST[
        "landing-pages/medications/prednisone/index.html"
    ],
    "/learn/sinus-infection/": SOURCE_HREF_BLOCKLIST[
        "landing-pages/learn/sinus-infection/index.html"
    ],
    "/llms.txt": SOURCE_HREF_BLOCKLIST["llms.txt"],
    "/llms-full.txt": SOURCE_HREF_BLOCKLIST["llms-full.txt"],
}


def parse_redirects() -> dict[str, str]:
    redirects: dict[str, str] = {}
    pattern = re.compile(r'"([^"]+)"\s*=>\s*"([^"]+)"')
    for path in REDIRECT_FILES:
        text = path.read_text(encoding="utf-8")
        redirects.update(pattern.findall(text))
    return redirects


def verify_local_redirects() -> list[str]:
    redirects = parse_redirects()
    failures: list[str] = []
    for source, expected in {**SAMPLED_REDIRECTS, **CHAIN_REDIRECTS}.items():
        actual = redirects.get(source)
        if actual != expected:
            failures.append(f"{source} expected {expected}, got {actual or 'missing'}")
    return failures


def verify_source_hrefs() -> list[str]:
    failures: list[str] = []
    for rel, blocked_hrefs in SOURCE_HREF_BLOCKLIST.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for href in blocked_hrefs:
            if href in text:
                failures.append(f"{rel} still contains {href}")
    return failures


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def live_check(source: str, expected: str) -> tuple[int, str, bool]:
    url = f"{SITE}{source}?v={int(time.time())}"
    req = urllib.request.Request(url, headers={"User-Agent": "NPCWoods crawl cleanup verifier"})
    opener = urllib.request.build_opener(NoRedirect)
    try:
        resp = opener.open(req, timeout=20)
        status = resp.status
        location = resp.headers.get("Location", "")
    except urllib.error.HTTPError as exc:
        status = exc.code
        location = exc.headers.get("Location", "") if exc.headers else ""
    loc_path = location.replace(SITE, "") if location.startswith(SITE) else location
    ok = status in (200, 301) and (status == 200 or loc_path.rstrip("/") == expected.rstrip("/"))
    return status, loc_path, ok


def verify_live() -> list[str]:
    failures: list[str] = []
    for source, expected in {**SAMPLED_REDIRECTS, **CHAIN_REDIRECTS}.items():
        status, loc_path, ok = live_check(source, expected)
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {status} {source} -> {loc_path or '(no Location)'}")
        if not ok:
            failures.append(f"{source} expected 200 or 301->{expected}, got {status}->{loc_path}")
    for source, blocked_hrefs in LIVE_SOURCE_BLOCKLIST.items():
        url = f"{SITE}{source}?v={int(time.time())}"
        req = urllib.request.Request(url, headers={"User-Agent": "NPCWoods crawl cleanup verifier"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                status = resp.status
                text = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            status = exc.code
            text = exc.read().decode("utf-8", errors="replace")
        hits = [href for href in blocked_hrefs if href in text]
        marker = "PASS" if status == 200 and not hits else "FAIL"
        print(f"[{marker}] {status} {source} stale-hrefs={len(hits)}")
        if status != 200 or hits:
            failures.append(f"{source} expected 200 and no stale hrefs, got {status} hits={hits}")
    return failures


def main() -> int:
    failures = verify_local_redirects() + verify_source_hrefs()

    if "--live" in sys.argv:
        failures += verify_live()

    if failures:
        print("\nFAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: local redirect mappings and source href checks are clean.")
    if "--live" not in sys.argv:
        print("Live HTTP checks skipped. Run with --live after deployment approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
