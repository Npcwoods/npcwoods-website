#!/usr/bin/env python3
"""First-time live launch for /start-uti/ /start-sinus/ /start-dental/ /start-uri/.

Default is dry-run. Live requires:
  --execute --confirm-live-deploy "CHRIS APPROVED LIVE DEPLOY"
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
LIVE_CONFIRM = "CHRIS APPROVED LIVE DEPLOY"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
PAGES = [
    ("start-uti", "Start UTI (ads lander)"),
    ("start-sinus", "Start Sinus (ads lander)"),
    ("start-dental", "Start Dental (ads lander)"),
    ("start-uri", "Start URI (ads lander)"),
]
CLICK_PARENT = ("t", "Ads click log parent")
CLICK_CHILD = ("click", "Ads click ingest")


def load_env() -> dict:
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def wp_request(env, method, path, body=None):
    url = f"https://npcwoods.com/wp-json/wp/v2{path}"
    auth = base64.b64encode(f"{env['WP_USERNAME']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "User-Agent": UA,
    }
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()[:800]}


def get_or_create_stub(env, slug, title, parent=None):
    existing = wp_request(env, "GET", f"/pages?slug={slug}&status=publish,draft,private")
    if isinstance(existing, list) and existing:
        if parent:
            matches = [p for p in existing if p.get("parent") == parent]
            page = matches[0] if matches else existing[0]
        else:
            page = existing[0]
        print(f"  [stub] found {slug} id={page['id']}")
        return page["id"]
    payload = {
        "title": title,
        "slug": slug,
        "status": "publish",
        "content": "<!-- Served by npcwoods-paid-pages.php -->",
        "comment_status": "closed",
        "ping_status": "closed",
    }
    if parent:
        payload["parent"] = parent
    created = wp_request(env, "POST", "/pages", payload)
    if "id" not in created:
        raise SystemExit(f"  [stub] FAILED {slug}: {created}")
    print(f"  [stub] created {slug} id={created['id']}")
    return created["id"]


def touch_stub(env, page_id):
    wp_request(env, "POST", f"/pages/{page_id}", {"comment_status": "closed"})


def sftp_mkdirs(sftp, remote_dir: str) -> None:
    path = ""
    for part in remote_dir.split("/"):
        path = f"{path}/{part}" if path else part
        try:
            sftp.stat(path)
        except IOError:
            try:
                sftp.mkdir(path)
            except IOError:
                pass


def sftp_put(sftp, local: Path, remote: str) -> None:
    sftp_mkdirs(sftp, str(Path(remote).parent).replace("\\", "/"))
    sftp.put(str(local), remote)
    print(f"  [upload] {local.relative_to(ROOT)} -> {remote}")


def patch_faq_schema(ids: dict[str, int]) -> bool:
    path = ROOT / "php" / "npcwoods-faq-schema.php"
    text = path.read_text(encoding="utf-8")
    marker = "// Ads + HIPAA /start-* landers (noindexed)"
    if marker in text:
        print("  [patch] faq-schema already has Ads+HIPAA marker")
        return False
    block = (
        "        698,  // /uti-care/ paid Google + Facebook clone (noindexed)\n"
        f"        {marker}\n"
        f"        {ids['start-uti']},  // /start-uti/\n"
        f"        {ids['start-sinus']},  // /start-sinus/\n"
        f"        {ids['start-dental']},  // /start-dental/\n"
        f"        {ids['start-uri']},  // /start-uri/\n"
        f"        {ids['t']},  // /t/\n"
        f"        {ids['click']},  // /t/click/\n"
    )
    if "        698,  // /uti-care/ paid Google + Facebook clone (noindexed)\n" not in text:
        raise SystemExit("faq-schema insert point missing")
    path.write_text(
        text.replace(
            "        698,  // /uti-care/ paid Google + Facebook clone (noindexed)\n",
            block,
            1,
        ),
        encoding="utf-8",
    )
    print("  [patch] faq-schema sitemap exclusions added")
    return True


def verify_live() -> int:
    import ssl

    ctx = ssl.create_default_context()
    failed = 0
    checks = [
        ("https://npcwoods.com/start-uti/", "UTI treatment by text"),
        ("https://npcwoods.com/start-sinus/", "Day 5"),
        ("https://npcwoods.com/start-dental/", "Tooth throbbing"),
        ("https://npcwoods.com/start-uri/", "Can't shake this cold"),
        ("https://npcwoods.com/ads-click.js", "npc_gclid"),
    ]
    for url, needle in checks:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                body = resp.read().decode("utf-8", "replace")
                ok = resp.status == 200 and needle in body
                print(f"  [{'ok' if ok else 'FAIL'}] {resp.status} {url} needle={needle!r}")
                if not ok:
                    failed += 1
        except Exception as exc:
            print(f"  [FAIL] {url} {exc}")
            failed += 1
    return failed


def main(argv) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-live-deploy")
    args = parser.parse_args(argv[1:])

    print("Deploy plan:")
    for slug, _title in PAGES:
        print(f"  [up] landing-pages/{slug}/index.html -> html/{slug}/index.html")
    print("  [up] html/shared/ads-click.js -> html/ads-click.js")
    print("  [up] php/npcwoods-paid-pages.php -> html/wp-content/mu-plugins/npcwoods-paid-pages.php")
    print("  [up] php/npcwoods-faq-schema.php -> html/wp-content/mu-plugins/npcwoods-faq-schema.php")
    print("  [wp] stubs: start-uti start-sinus start-dental start-uri t/click")
    if not args.execute:
        print("[dry-run] nothing uploaded.")
        return 0
    if args.confirm_live_deploy != LIVE_CONFIRM:
        print(f"[blocked] need --confirm-live-deploy \"{LIVE_CONFIRM}\"", file=sys.stderr)
        return 2

    env = load_env()
    print("[1] WordPress stubs")
    ids = {}
    for slug, title in PAGES:
        ids[slug] = get_or_create_stub(env, slug, title)
    ids["t"] = get_or_create_stub(env, CLICK_PARENT[0], CLICK_PARENT[1])
    ids["click"] = get_or_create_stub(env, CLICK_CHILD[0], CLICK_CHILD[1], parent=ids["t"])
    print("[2] Patch sitemap exclusions")
    patch_faq_schema(ids)
    print("[3] SFTP upload")
    import paramiko

    transport = paramiko.Transport((env["SFTP_HOST"], int(env.get("SFTP_PORT") or 22)))
    transport.banner_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        for slug, _title in PAGES:
            sftp_put(sftp, ROOT / "landing-pages" / slug / "index.html", f"html/{slug}/index.html")
        sftp_put(sftp, ROOT / "html" / "shared" / "ads-click.js", "html/ads-click.js")
        sftp_put(sftp, ROOT / "php" / "npcwoods-paid-pages.php", "html/wp-content/mu-plugins/npcwoods-paid-pages.php")
        sftp_put(sftp, ROOT / "php" / "npcwoods-faq-schema.php", "html/wp-content/mu-plugins/npcwoods-faq-schema.php")
    finally:
        sftp.close()
        transport.close()
    print("[4] Touch stubs to flush Varnish")
    for page_id in ids.values():
        touch_stub(env, page_id)
    time.sleep(4)
    print("[5] Verify clean URLs")
    failed = verify_live()
    ids_path = ROOT / "content-output" / "reports" / "ads-hipaa-lookplate-2026-09-10" / "wp-stub-ids.json"
    ids_path.parent.mkdir(parents=True, exist_ok=True)
    ids_path.write_text(json.dumps(ids, indent=2), encoding="utf-8")
    print(f"[ok] stub ids -> {ids_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
