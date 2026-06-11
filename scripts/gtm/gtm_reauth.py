#!/usr/bin/env python3
"""
One-time GTM re-auth — mints a refresh token with Tag Manager EDIT + PUBLISH scope.

Why this exists:
  The existing GOOGLE_ADS_REFRESH_TOKEN only has tagmanager.readonly. Editing the
  Meta pixel tag needs edit + publish scope. We mint a SEPARATE token (GTM_REFRESH_TOKEN)
  on the same OAuth client so the Stripe -> Google Ads conversion bridge token is never
  touched. Follows the existing pattern in .env (one client, scope-specific tokens).

Prereq (Chris, one-time, in browser):
  Enable the Tag Manager API on the Cloud project:
  https://console.developers.google.com/apis/api/tagmanager.googleapis.com/overview?project=475686092388
  Click "Enable", wait ~1 min.

Run:
  gads-env/bin/python npcwoods-website/scripts/gtm/gtm_reauth.py

It opens a browser, you log in with the Google account that owns GTM-59QSWZRC,
grant access, and the new refresh token is written to ~/Desktop/Chris-HQ/.env
as GTM_REFRESH_TOKEN. Nothing goes live — this only grants API access.
"""
import os
import sys

ENV_PATH = os.path.expanduser("~/Desktop/Chris-HQ/.env")

# Edit container entities, create container versions, and publish a version.
# All three are needed for the full stage-and-publish flow.
SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish",
]


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


def upsert_env(path, key, value):
    """Add or replace KEY=value in .env, preserving everything else."""
    lines = []
    found = False
    with open(path) as fh:
        for line in fh:
            if line.strip().startswith(key + "="):
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.append(f"# GTM edit+publish token (minted by gtm_reauth.py; same OAuth client as Google Ads)\n")
        lines.append(f"{key}={value}\n")
    with open(path, "w") as fh:
        fh.writelines(lines)


def main():
    from google_auth_oauthlib.flow import InstalledAppFlow

    env = load_env(ENV_PATH)
    client_id = env.get("GOOGLE_ADS_CLIENT_ID")
    client_secret = env.get("GOOGLE_ADS_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit("Missing GOOGLE_ADS_CLIENT_ID / GOOGLE_ADS_CLIENT_SECRET in .env")

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    print("\nA browser window will open. Log in with the Google account that owns")
    print("GTM container GTM-59QSWZRC and approve the Tag Manager permissions.\n")
    creds = flow.run_local_server(
        port=0,
        access_type="offline",
        prompt="consent",
        include_granted_scopes="false",
    )

    if not creds.refresh_token:
        sys.exit("No refresh token returned. Re-run; ensure you click 'Allow' fully.")

    upsert_env(ENV_PATH, "GTM_REFRESH_TOKEN", creds.refresh_token)
    print("\n✅ Success. GTM_REFRESH_TOKEN written to .env")
    print("   Scopes granted:", " ".join(SCOPES))
    print("\nNext: run the audit (read-only):")
    print("   gads-env/bin/python npcwoods-website/scripts/gtm/gtm_meta_pixel_fix.py")


if __name__ == "__main__":
    main()
