#!/usr/bin/env python3
"""Deploy 404 cleanup mu-plugin + verify configured redirects.

Flow:
  1. Pre-deploy guardrail — grep plugin for banned words (doctor, insurance)
  2. SFTP upload php/npcwoods-redirects-404-cleanup.php → html/wp-content/mu-plugins/
  3. POST to WP homepage stub (id=63) to trigger Varnish purge
  4. Sleep 30s for cache propagation
  5. Cache-busted curl each source URL, confirm 301 + correct Location

Idempotent: re-running just re-uploads the same plugin + re-verifies.

Usage:
    python3 scripts/deploy-404-cleanup-2026-04-22.py [--dry-run]
"""
import base64
import json
import ssl
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path("/Users/chriswoods/Desktop/Chris-HQ/.env")
PLUGIN_LOCAL = ROOT / "php" / "npcwoods-redirects-404-cleanup.php"
PLUGIN_REMOTE = "html/wp-content/mu-plugins/npcwoods-redirects-404-cleanup.php"
HOMEPAGE_STUB_ID = 63
SITE = "https://npcwoods.com"
BANNED = ["doctor", "insurance"]
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# (source_slug, expected_target) — must match the array inside the mu-plugin.
REDIRECTS = [
    ("/phoenix-az-strep/",               "/strep-throat-ear-infection/"),
    ("/chandler-az-strep/",              "/strep-throat-ear-infection/"),
    ("/tempe-az-strep/",                 "/strep-throat-ear-infection/"),
    ("/glendale-az-strep/",              "/strep-throat-ear-infection/"),
    ("/surprise-az-strep/",              "/strep-throat-ear-infection/"),
    ("/tucson-az-strep/",                "/strep-throat-ear-infection/"),
    ("/peoria-az-strep/",                "/strep-throat-ear-infection/"),
    ("/mesa-az-strep/",                  "/strep-throat-ear-infection/"),
    ("/phoenix-uti-treatment/",          "/uti-treatment/"),
    ("/phoenix-sinus-infection/",        "/sinus-infection-treatment/"),
    ("/mesa-sinus-infection/",           "/sinus-infection-treatment/"),
    ("/scottsdale-sinus-infection/",     "/sinus-infection-treatment/"),
    ("/tucson-sinus-infection/",         "/sinus-infection-treatment/"),
    ("/surprise-sinus-infection/",       "/sinus-infection-treatment/"),
    ("/tucson-az-sinus/",                "/sinus-infection-treatment/"),
    ("/mesa-telemedicine/",              "/arizona-telemedicine/"),
    ("/scottsdale-telemedicine/",        "/arizona-telemedicine/"),
    ("/gilbert-telemedicine/",           "/arizona-telemedicine/"),
    ("/glendale-az-telemedicine/",       "/arizona-telemedicine/"),
    ("/tempe-telemedicine/",             "/arizona-telemedicine/"),
    ("/chandler-telemedicine/",          "/arizona-telemedicine/"),
    ("/surprise-telemedicine/",          "/arizona-telemedicine/"),
    ("/peoria-az-telemedicine/",         "/arizona-telemedicine/"),
    ("/santa-fe-uti-treatment/",         "/uti-treatment/"),
    ("/rio-rancho-uti-treatment/",       "/uti-treatment/"),
    ("/farmington-uti-treatment/",       "/uti-treatment/"),
    ("/albuquerque-sinus-infection/",    "/sinus-infection-treatment/"),
    ("/santa-fe-sinus-infection/",       "/sinus-infection-treatment/"),
    ("/rio-rancho-sinus-infection/",     "/sinus-infection-treatment/"),
    ("/las-cruces-sinus-infection/",     "/sinus-infection-treatment/"),
    ("/farmington-sinus-infection/",     "/sinus-infection-treatment/"),
    ("/santa-fe-telemedicine/",          "/new-mexico-telemedicine/"),
    ("/rio-rancho-telemedicine/",        "/new-mexico-telemedicine/"),
    ("/farmington-telemedicine/",        "/new-mexico-telemedicine/"),
    ("/las-cruces-telemedicine/",        "/new-mexico-telemedicine/"),
    ("/roswell-telemedicine/",           "/new-mexico-telemedicine/"),
    ("/dalton-uti-treatment/",           "/uti-treatment/"),
    ("/gainesville-ga-uti-treatment/",   "/uti-treatment/"),
    ("/augusta-uti-treatment/",          "/uti-treatment/"),
    ("/athens-uti-treatment/",           "/uti-treatment/"),
    ("/atlanta-sinus-infection/",        "/sinus-infection-treatment/"),
    ("/dalton-sinus-infection/",         "/sinus-infection-treatment/"),
    ("/augusta-sinus-infection/",        "/sinus-infection-treatment/"),
    ("/athens-sinus-infection/",         "/sinus-infection-treatment/"),
    ("/gainesville-ga-sinus-infection/", "/sinus-infection-treatment/"),
    ("/charlotte-uti-treatment/",        "/uti-treatment/"),
    ("/asheville-uti-treatment/",        "/uti-treatment/"),
    ("/hickory-uti-treatment/",          "/uti-treatment/"),
    ("/hendersonville-uti-treatment/",   "/uti-treatment/"),
    ("/boone-uti-treatment/",            "/uti-treatment/"),
    ("/charlotte-sinus-infection/",      "/sinus-infection-treatment/"),
    ("/hickory-sinus-infection/",        "/sinus-infection-treatment/"),
    ("/hendersonville-sinus-infection/", "/sinus-infection-treatment/"),
    ("/conditions/skin-infections/",     "/learn/skin-infection/"),
    ("/learn/respiratory-infection/",    "/learn/bronchitis/"),
    ("/learn/cold-flu/",                 "/learn/covid-flu/"),
    ("/learn/hives/",                    "/learn/allergic-reaction/"),
    ("/learn/acne/",                     "/learn/skin-infection/"),
    ("/learn/abscesses/",                "/dental-pain/"),
]


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def guardrail():
    text = PLUGIN_LOCAL.read_text(encoding="utf-8").lower()
    hits = [w for w in BANNED if w in text]
    # Whitelist: "Cache-Control: no-cache" is fine; "uri-" isn't a banned word
    # We're looking for the literal tokens "doctor" / "insurance" as content words
    # but our plugin has only URL paths and PHP header() — nothing that would use
    # these naturally. If hit, block.
    if hits:
        print(f"[GUARDRAIL FAIL] banned words found in plugin: {hits}")
        sys.exit(2)
    print("[guardrail] OK — no banned words in mu-plugin")


def sftp_upload(env):
    try:
        import paramiko
    except ImportError:
        print("paramiko not installed. pip3 install paramiko")
        sys.exit(2)
    transport = paramiko.Transport((env["SFTP_HOST"], int(env.get("SFTP_PORT", "22"))))
    transport.banner_timeout = 30
    transport.auth_timeout = 30
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.put(str(PLUGIN_LOCAL), PLUGIN_REMOTE)
        stat = sftp.stat(PLUGIN_REMOTE)
        print(f"[sftp] uploaded → {PLUGIN_REMOTE} ({stat.st_size} bytes)")
    finally:
        sftp.close()
        transport.close()


def wp_varnish_purge(env):
    """POST a no-op update to the homepage stub to force Varnish invalidation.

    On GoDaddy MWP, touching a page via REST fires the auto-purge hook.
    We send a harmless field update that WordPress accepts without changing content.
    """
    url = f"{SITE}/wp-json/wp/v2/pages/{HOMEPAGE_STUB_ID}"
    auth = base64.b64encode(
        f'{env["WP_USERNAME"]}:{env["WP_APP_PASSWORD"]}'.encode()
    ).decode()
    body = json.dumps({"meta": {"_npcwoods_cache_bust": str(int(time.time()))}}).encode()
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            print(f"[wp-purge] stub {HOMEPAGE_STUB_ID} touched — modified={data.get('modified','?')}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:200]
        print(f"[wp-purge] HTTP {e.code} on stub {HOMEPAGE_STUB_ID}: {body}")


def verify_redirect(source, expected):
    """Cache-busted HEAD request. Expect 301 + Location matching expected target."""
    url = f"{SITE}{source}?v={int(time.time())}"
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    # Don't follow redirects — we want to inspect the 301 response itself.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        resp = opener.open(req, timeout=15)
        status = resp.status
        location = resp.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        status = e.code
        location = e.headers.get("Location", "") if e.headers else ""
    # Normalize location: may be absolute (home_url()) or relative
    loc_path = location.replace(SITE, "") if location.startswith(SITE) else location
    ok = status == 301 and loc_path.rstrip("/") == expected.rstrip("/")
    return status, loc_path, ok


def verify_all():
    print()
    print("=" * 76)
    print(f"Verifying {len(REDIRECTS)} redirects (cache-busted)")
    print("=" * 76)
    passes = 0
    fails = []
    for source, expected in REDIRECTS:
        status, loc, ok = verify_redirect(source, expected)
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] {status}  {source:40s} → {loc}")
        if ok:
            passes += 1
        else:
            fails.append((source, expected, status, loc))
    print()
    print(f"  {passes} / {len(REDIRECTS)} redirects PASS")
    if fails:
        print()
        print("  Failures:")
        for source, expected, status, loc in fails:
            print(f"    {source}  expected 301→{expected}  got {status}→{loc}")
        return False
    return True


def main(argv):
    dry_run = "--dry-run" in argv
    print(f"[deploy-404-cleanup] plugin: {PLUGIN_LOCAL.relative_to(ROOT)}")
    print(f"[deploy-404-cleanup] remote: {PLUGIN_REMOTE}")
    print(f"[deploy-404-cleanup] dry-run: {dry_run}")
    print()

    guardrail()

    if dry_run:
        print("[dry-run] skipping SFTP + WP REST + verification")
        return 0

    env = load_env()
    for key in ("SFTP_HOST", "SFTP_USERNAME", "SFTP_PASSWORD", "WP_USERNAME", "WP_APP_PASSWORD"):
        if not env.get(key):
            print(f"[fatal] missing {key} in .env")
            return 2

    sftp_upload(env)
    wp_varnish_purge(env)

    print("[sleep] 30s for Varnish/edge propagation...")
    time.sleep(30)

    ok = verify_all()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
