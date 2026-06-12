#!/usr/bin/env python3
"""
GTM Meta-pixel health-page fix for container GTM-59QSWZRC.

Goal: stop the GTM-injected Meta pixel (ID 1558261907814968) from firing on UTI
health-condition pages, while keeping it live on non-health pages (homepage,
thank-you) for Meta ads. We do this the clean GTM way: a firing EXCEPTION
(blocking trigger) on the Meta tag, matching the health-page URL paths. No tag
deletion — flip-the-switch reversible.

Three modes, safe by default:
  (no flags)            AUDIT — read-only. Finds the Meta tag(s), prints their
                        firing/blocking triggers and the planned change. Changes nothing.
  --apply               Enables the {{Page Path}} built-in var, creates/reuses the
                        block trigger, attaches it as an exception to the Meta tag(s),
                        and creates a new container VERSION. NOT published — still a draft.
  --apply --publish     Same as --apply, then PUBLISHES the version live.
                        ^ This is the only mode that changes the live site. Chris's yes required.

Usage:
  gads-env/bin/python npcwoods-website/scripts/gtm/gtm_meta_pixel_fix.py            # audit
  gads-env/bin/python npcwoods-website/scripts/gtm/gtm_meta_pixel_fix.py --apply    # stage (draft)
  gads-env/bin/python npcwoods-website/scripts/gtm/gtm_meta_pixel_fix.py --apply --publish  # go live
"""
import argparse
import json
import os
import sys

ENV_PATH = os.path.expanduser("~/Desktop/Chris-HQ/.env")

# Pages where Meta must NOT fire (no BAA with Meta). Covers ALL health-condition
# surfaces: the whole UTI family (hub + city + condition subpages + arizona +
# uti-care + uti-treatment-online) and the non-UTI condition pages. Longer slugs
# are listed before their prefixes so the (/|$) boundary resolves correctly.
# Non-health pages (geo/state, how-it-works, pharmacy, thank-you, homepage) are
# intentionally excluded so Meta ads keep working there.
BLOCK_REGEX = (
    r"^/(arizona-uti-treatment|uti-treatment-online|uti-treatment|uti-care|"
    r"dental-pain|ear-infection-treatment|ed-treatment|glp1-weight-loss|"
    r"sinus-infection-treatment|strep-throat-treatment|conditions|"
    r"learn|medications)(/|$)"
)
TRIGGER_NAME = "Block — UTI / Health Pages (no Meta BAA)"
META_PIXEL_ID = "1558261907814968"
VERSION_NAME = "Scope Meta pixel off health + education pages"
VERSION_NOTES = (
    "Extends the firing exception so the Meta pixel (1558261907814968) does not "
    "fire on health-condition pages OR the /learn/* and /medications/* education "
    "pages. No BAA with Meta; health pages must not send PageView. Pixel remains "
    "live on non-health pages."
)

# Substrings that identify a Meta/Facebook pixel tag when found in its JSON.
META_MARKERS = ["1558261907814968", "connect.facebook.net", "fbevents", "fbq("]


def load_env(path):
    env = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def build_service(env):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    rt = env.get("GTM_REFRESH_TOKEN")
    if not rt:
        sys.exit(
            "Missing GTM_REFRESH_TOKEN in .env.\n"
            "Run the one-time re-auth first:\n"
            "  gads-env/bin/python npcwoods-website/scripts/gtm/gtm_reauth.py"
        )
    creds = Credentials(
        token=None,
        refresh_token=rt,
        client_id=env["GOOGLE_ADS_CLIENT_ID"],
        client_secret=env["GOOGLE_ADS_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("tagmanager", "v2", credentials=creds, cache_discovery=False)


def find_container(svc, public_id):
    accounts = svc.accounts().list().execute().get("account", [])
    for acct in accounts:
        conts = (
            svc.accounts()
            .containers()
            .list(parent=acct["path"])
            .execute()
            .get("container", [])
        )
        for c in conts:
            if c.get("publicId") == public_id:
                return acct, c
    sys.exit(f"Container {public_id} not found under any accessible account.")


def default_workspace(svc, container_path):
    wss = (
        svc.accounts()
        .containers()
        .workspaces()
        .list(parent=container_path)
        .execute()
        .get("workspace", [])
    )
    if not wss:
        sys.exit("No workspaces found in container.")
    for ws in wss:
        if ws.get("name", "").lower() == "default workspace":
            return ws
    return wss[0]


def is_meta_tag(tag):
    blob = json.dumps(tag).lower()
    return any(m.lower() in blob for m in META_MARKERS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="stage the fix in a draft version")
    ap.add_argument("--publish", action="store_true", help="publish the version live (requires --apply)")
    ap.add_argument("--json", action="store_true", help="dump matched tag JSON")
    args = ap.parse_args()
    if args.publish and not args.apply:
        sys.exit("--publish requires --apply (nothing to publish otherwise).")

    env = load_env(ENV_PATH)
    public_id = env.get("GTM_ID", "GTM-59QSWZRC")
    svc = build_service(env)

    acct, container = find_container(svc, public_id)
    print(f"Account : {acct.get('name')} ({acct.get('accountId')})")
    print(f"Container: {container.get('name')} / {public_id} ({container.get('containerId')})")

    ws = default_workspace(svc, container["path"])
    ws_path = ws["path"]
    print(f"Workspace: {ws.get('name')} ({ws.get('workspaceId')})\n")

    tags = svc.accounts().containers().workspaces().tags().list(parent=ws_path).execute().get("tag", [])
    triggers = svc.accounts().containers().workspaces().triggers().list(parent=ws_path).execute().get("trigger", [])
    trig_by_id = {t["triggerId"]: t for t in triggers}

    meta_tags = [t for t in tags if is_meta_tag(t)]
    if not meta_tags:
        print("No Meta/Facebook pixel tag found in this workspace. Nothing to do.")
        return

    print(f"Found {len(meta_tags)} Meta/Facebook pixel tag(s):")
    for t in meta_tags:
        fires = [trig_by_id.get(i, {}).get("name", i) for i in t.get("firingTriggerId", [])]
        blocks = [trig_by_id.get(i, {}).get("name", i) for i in t.get("blockingTriggerId", [])]
        print(f"  • [{t['tagId']}] {t.get('name')}  (type={t.get('type')})")
        print(f"      fires on : {fires or '—'}")
        print(f"      exceptions: {blocks or '—'}")
        if args.json:
            print(json.dumps(t, indent=2))

    print(f"\nPlanned exception trigger: '{TRIGGER_NAME}'")
    print(f"  condition: Page Path matches RegEx  {BLOCK_REGEX}")

    if not args.apply:
        print("\n[AUDIT ONLY] No changes made. Re-run with --apply to stage (draft, not live).")
        return

    # ---- mutation path (draft version; not live unless --publish) ----
    tm = svc.accounts().containers().workspaces()

    # 1. Ensure {{Page Path}} built-in variable is enabled (idempotent).
    try:
        tm.built_in_variables().create(parent=ws_path, type="pagePath").execute()
        print("\nEnabled built-in variable: Page Path")
    except Exception as e:
        if "already exists" in str(e).lower() or "409" in str(e):
            print("\nBuilt-in variable Page Path already enabled.")
        else:
            print(f"\nNote enabling Page Path var: {e}")

    # 2. Create or update the block trigger.
    # It MUST be a Custom Event trigger matching {{_event}} = .* so the exception
    # is active on EVERY event (page view, DOM ready, custom events). The Meta tags
    # fire on DOM Ready + Custom Event; a Page View exception would never apply at
    # those moments and the tags would still fire. Plus the Page Path condition to
    # scope it to the health pages.
    desired = {
        "name": TRIGGER_NAME,
        "type": "customEvent",
        "customEventFilter": [
            {
                "type": "matchRegex",
                "parameter": [
                    {"type": "template", "key": "arg0", "value": "{{_event}}"},
                    {"type": "template", "key": "arg1", "value": ".*"},
                ],
            }
        ],
        "filter": [
            {
                "type": "matchRegex",
                "parameter": [
                    {"type": "template", "key": "arg0", "value": "{{Page Path}}"},
                    {"type": "template", "key": "arg1", "value": BLOCK_REGEX},
                ],
            }
        ],
    }
    existing = next((t for t in triggers if t.get("name") == TRIGGER_NAME), None)
    if existing:
        block_trigger = tm.triggers().update(path=existing["path"], body=desired).execute()
        print(f"Updated block trigger [{block_trigger['triggerId']}] -> Custom Event(.*) + Page Path.")
    else:
        block_trigger = tm.triggers().create(parent=ws_path, body=desired).execute()
        print(f"Created block trigger [{block_trigger['triggerId']}].")
    block_id = block_trigger["triggerId"]

    # 3. Attach as a firing exception on each Meta tag (idempotent).
    for t in meta_tags:
        existing = t.get("blockingTriggerId", [])
        if block_id in existing:
            print(f"Tag [{t['tagId']}] already has the exception. Skipping.")
            continue
        t["blockingTriggerId"] = existing + [block_id]
        tm.tags().update(path=t["path"], body=t).execute()
        print(f"Attached exception to tag [{t['tagId']}] {t.get('name')}.")

    # 4. Create a version (draft snapshot). This does NOT go live by itself.
    resp = tm.create_version(
        path=ws_path, body={"name": VERSION_NAME, "notes": VERSION_NOTES}
    ).execute()
    version = resp.get("containerVersion", {})
    vid = version.get("containerVersionId")
    vpath = version.get("path")
    print(f"\nCreated container version {vid} (DRAFT — not live).")

    if not args.publish:
        print("\n[STAGED] Draft version created but NOT published. Live site unchanged.")
        print("To go live (needs Chris's yes): re-run with  --apply --publish")
        return

    # 5. Publish live.
    svc.accounts().containers().versions().publish(path=vpath).execute()
    print(f"\n✅ PUBLISHED version {vid} LIVE. Meta pixel now skips UTI health pages.")


if __name__ == "__main__":
    main()
