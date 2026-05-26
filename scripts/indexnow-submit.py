#!/usr/bin/env python3
"""IndexNow URL submission for npcwoods.com.

IndexNow lets us push fresh URLs directly to Bing, Yandex, Naver, Seznam, and
Microsoft Bing-powered search. Bing has near-zero index of npcwoods.com per the
2026-04-23 audit — this is the highest-leverage indexing action available
without GSC OAuth.

First-run flow:
  1. Generate a 32-char hex key (or reuse an existing one stored in .env as INDEXNOW_KEY)
  2. SFTP-upload <key>.txt to html/<key>.txt containing just the key string
  3. POST to api.indexnow.org/indexnow with the URL list

Subsequent runs reuse the same key.
"""
import argparse
import json
import secrets
import sys
from pathlib import Path

import paramiko
import requests

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT.parent / ".env"
HOST = "npcwoods.com"

URLS_TO_SUBMIT = [
    "https://npcwoods.com/pricing/",
    "https://npcwoods.com/credentials/",
    "https://npcwoods.com/",
    "https://npcwoods.com/about/",
    "https://npcwoods.com/faq/",
    "https://npcwoods.com/how-it-works/",
    "https://npcwoods.com/conditions/",
    "https://npcwoods.com/uti-treatment/",
    "https://npcwoods.com/sinus-infection-treatment/",
    "https://npcwoods.com/dental-pain/",
    "https://npcwoods.com/ed-treatment/",
    "https://npcwoods.com/arizona-telemedicine/",
    "https://npcwoods.com/nevada-telemedicine/",
    "https://npcwoods.com/new-mexico-telemedicine/",
    "https://npcwoods.com/utah-telemedicine/",
    "https://npcwoods.com/iowa-telemedicine/",
    "https://npcwoods.com/montana-telemedicine/",
    "https://npcwoods.com/llms.txt",
    "https://npcwoods.com/llms-full.txt",
    # 2026-05-02 — newly enriched / title-aligned (FAQ schema + query-aligned titles)
    "https://npcwoods.com/uti-treatment/mesa-az/",
    "https://npcwoods.com/uti-treatment/surprise-az/",
    "https://npcwoods.com/strep-throat-treatment/",
]


def load_env():
    env = {}
    for raw in ENV_PATH.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def append_to_env(key: str, value: str):
    """Append a new key=value to .env if not present."""
    text = ENV_PATH.read_text()
    if f"{key}=" in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    text += f"{key}={value}\n"
    ENV_PATH.write_text(text)
    print(f"[env] appended {key} to .env")


def resolve_path_to_url(path_str: str) -> str | None:
    """Resolve a public URL or local repository file path to a public npcwoods.com URL."""
    if path_str.startswith("http://") or path_str.startswith("https://"):
        url = path_str
        if url.startswith("http://"):
            url = "https://" + url[7:]
        # Normalize index.html or index.php endings
        if url.endswith("/index.html"):
            url = url[:-10]
        elif url.endswith("/index.php"):
            url = url[:-9]
        elif url.endswith("index.html"):
            url = url[:-10]
        return url

    # Resolve local path relative to root
    try:
        p = Path(path_str).resolve()
    except Exception:
        return None

    # Ensure path is relative to the repo ROOT
    try:
        p.relative_to(ROOT)
    except ValueError:
        try:
            # Try relative to ROOT if passed as a relative path
            p = (ROOT / path_str).resolve()
            p.relative_to(ROOT)
        except ValueError:
            return None

    rel = p.relative_to(ROOT).as_posix()
    if rel == "homepage/page-npcwoods-home.php":
        return "https://npcwoods.com/"
    if rel.startswith("homepage/"):
        return None
    if rel.startswith("landing-pages/"):
        slug = rel[len("landing-pages/"):]
        if slug.endswith("index.html"):
            slug = slug[:-10]
        if slug and not slug.endswith("/"):
            if "." not in slug.split("/")[-1]:
                slug += "/"
        return f"https://npcwoods.com/{slug}"
    if rel.startswith("html/"):
        slug = rel[len("html/"):]
        if slug.endswith("index.html"):
            slug = slug[:-10]
        if slug and not slug.endswith("/"):
            if "." not in slug.split("/")[-1]:
                slug += "/"
        return f"https://npcwoods.com/{slug}"
    return None


def upload_key_file(env, key: str) -> bool:
    """Check if the key is already live. If not, upload it via SFTP and verify."""
    verify_url = f"https://{HOST}/{key}.txt"
    
    # Optimization Check: If the key is already retrievable over HTTPS, bypass SFTP
    try:
        r = requests.get(verify_url, timeout=5)
        if r.status_code == 200 and r.text.strip() == key:
            print(f"[ok] key file already live at {verify_url} (skipped SFTP upload)")
            return True
    except Exception:
        pass

    remote = f"html/{key}.txt"
    local = ROOT / f"_indexnow-key-{key[:8]}.txt"
    local.write_text(key, encoding="utf-8")

    print(f"[sftp] uploading IndexNow key file -> {remote}")
    transport = paramiko.Transport((env["SFTP_HOST"], int(env["SFTP_PORT"])))
    transport.banner_timeout = 60
    transport.auth_timeout = 60
    transport.connect(username=env["SFTP_USERNAME"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.put(str(local), remote)
    finally:
        sftp.close()
        transport.close()
        local.unlink()

    # Verify the key file is publicly retrievable after upload
    r = requests.get(verify_url, timeout=30)
    if r.status_code != 200 or r.text.strip() != key:
        print(f"[err] key file not retrievable from {verify_url} (status={r.status_code})")
        return False
    print(f"[ok] key file live at {verify_url}")
    return True


def submit_urls(key: str, urls: list[str]) -> bool:
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }
    print(f"\n[indexnow] submitting {len(urls)} URLs to api.indexnow.org")
    for u in urls[:5]:
        print(f"  - {u}")
    if len(urls) > 5:
        print(f"  ... +{len(urls) - 5} more")

    r = requests.post(
        "https://api.indexnow.org/indexnow",
        json=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    print(f"[indexnow] response: {r.status_code}")
    if r.text:
        print(f"[indexnow] body: {r.text[:200]}")
    # 200 OK or 202 Accepted are both success per spec
    return r.status_code in (200, 202)


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow (Bing + partners).")
    parser.add_argument("targets", nargs="*", help="Optional specific URLs or local paths to submit. If omitted, submits the default set.")
    args = parser.parse_args(argv)

    urls = []
    if args.targets:
        for t in args.targets:
            url = resolve_path_to_url(t)
            if url:
                urls.append(url)
            else:
                print(f"[skip] cannot resolve to a public URL: {t}")
        # Remove duplicates while keeping order
        seen = set()
        urls = [x for x in urls if not (x in seen or seen.add(x))]
        if not urls:
            print("[abort] no valid URLs resolved from targets")
            return 1
    else:
        urls = URLS_TO_SUBMIT

    env = load_env()
    key = env.get("INDEXNOW_KEY")
    if not key:
        key = secrets.token_hex(16)  # 32-char hex
        print(f"[gen] new IndexNow key: {key}")
        append_to_env("INDEXNOW_KEY", key)

    if not upload_key_file(env, key):
        print("[abort] key file verification failed — IndexNow submission would be rejected")
        return 2

    ok = submit_urls(key, urls)
    if ok:
        print(f"\n[done] {len(urls)} URLs submitted to IndexNow (Bing + partners). Indexing happens within hours.")
        return 0
    print("\n[warn] IndexNow returned non-success status")
    return 1


if __name__ == "__main__":
    sys.exit(main())
