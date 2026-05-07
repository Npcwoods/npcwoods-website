#!/usr/bin/env python3
"""
Scrub the word 'doctor' from live npcwoods.com landing pages and templates.

Per-file context-aware replacements (no global find/replace — each page's
surrounding copy has its own tone). Idempotent: reads from a pristine
.pre-doctor-scrub.bak backup created on first run, so re-running always
starts from the same source.

Size-shrink guard: aborts per-file if the output shrinks by more than
30% vs the backup (per memory: feedback_safe_html_block_replace).

Does NOT deploy. SFTP upload is a separate step.

External URLs containing "doctor" in their path (e.g., doctor.webmd.com)
are intentionally left alone — the rule is about NPCWoods copy, not
third-party citations.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHRINK_GUARD = 0.70

# (relative path) -> [(old, new), ...]
REPLACEMENTS = {
    "landing-pages/montana-telemedicine/index.html": [
        ("one of the hardest places to see a doctor",
         "one of the hardest places to get seen"),
    ],
    "landing-pages/new-mexico-telemedicine/index.html": [
        ("Need a Doctor in New Mexico?<br><span>Text a Nurse Practitioner",
         "Need Care in New Mexico?<br><span>Text a Nurse Practitioner"),
    ],
    "landing-pages/oregon-telemedicine/index.html": [
        ("wait until Friday for a doctor's appointment",
         "wait until Friday for an appointment"),
    ],
    "landing-pages/colorado-telemedicine/index.html": [
        ("getting into a doctor can take days",
         "getting seen can take days"),
    ],
    "landing-pages/iowa-telemedicine/index.html": [
        # Hero H1 — keep emotional hit
        ("Your Town Doctor Retired<br>and Nobody Replaced Him?",
         "Your Family Clinic Closed<br>and Nobody Replaced It?"),
        # Body paragraph
        ("The family doctor retires, the clinic closes, and suddenly",
         "The family practice shuts down, and suddenly"),
    ],
    "landing-pages/utah-telemedicine/index.html": [
        ("Taking everybody to the doctor? That's a whole-day event",
         "Taking everybody in for a visit? That's a whole-day event"),
    ],
    "landing-pages/dental-pain/index.html": [
        # 6 refs — all variations of "primary care doctor" or "a doctor"
        ("primary care doctor.\"",
         "primary care provider.\""),
        ("Finding a primary care doctor takes weeks",
         "Finding a primary care provider takes weeks"),
        ("Let the primary care doctor handle systemic infections",
         "Let the primary care provider handle systemic infections"),
        ("You need to see your primary care doctor",
         "You need to see your primary care provider"),
        ("trying to find a doctor who can help",
         "trying to find a clinician who can help"),
        ("wait three months for a primary care doctor",
         "wait three months for a primary care provider"),
    ],
    "landing-pages/ed-treatment/index.html": [
        # FAQ question — both in JSON-LD schema and in visible HTML
        ("Can I really get ED treatment without going to a doctor's office?",
         "Can I really get ED treatment without an office visit?"),
    ],
    "landing-pages/faq/index.html": [
        ("random rotating doctor",
         "random rotating clinician"),
    ],
    "landing-pages/learn/cold-sores/index.html": [
        # Two occurrences — same phrasing, but one in JSON-LD and one in body
        ("your doctor may recommend daily antiviral therapy to reduce transmission.\"",
         "your clinician may recommend daily antiviral therapy to reduce transmission.\""),
        ("your doctor may recommend daily antiviral therapy to reduce transmission risk.",
         "your clinician may recommend daily antiviral therapy to reduce transmission risk."),
    ],
    "landing-pages/glp1-landing-page.html": [
        ("nurse screening questions for a doctor you'll never meet",
         "nurse screening questions for a clinician you'll never meet"),
    ],
    # credentials/index.html: only hits are inside doctor.webmd.com URLs.
    # External URL subdomain — not our copy. Intentionally skipped.
}


def ensure_backup(target: Path) -> Path:
    backup = target.with_suffix(target.suffix + ".pre-doctor-scrub.bak")
    if not backup.exists():
        shutil.copy2(target, backup)
        print(f"[backup] created {backup.name}")
    return backup


def scrub_file(rel_path: str, pairs, dry_run: bool) -> dict:
    target = REPO / rel_path
    if not target.exists():
        return {"path": rel_path, "status": "missing"}

    backup = ensure_backup(target)
    src = backup.read_text()

    # Verify every "old" is present in the pristine source.
    missing = [o for (o, _) in pairs if o not in src]
    if missing:
        return {
            "path": rel_path,
            "status": "pattern-not-found",
            "missing": missing,
        }

    out = src
    for old, new in pairs:
        out = out.replace(old, new)

    # Idempotence check: the output should contain no bare "doctor" that
    # wasn't already known-OK (external URL hosts). For our purposes we just
    # count any remaining "doctor" occurrences.
    remaining = _count_bare_doctor(out)
    # Shrink guard
    if len(out) < len(src) * SHRINK_GUARD:
        return {
            "path": rel_path,
            "status": "shrink-abort",
            "src_bytes": len(src),
            "out_bytes": len(out),
        }

    if dry_run:
        return {
            "path": rel_path,
            "status": "dry-run",
            "delta": len(out) - len(src),
            "remaining_doctor": remaining,
        }

    target.write_text(out)
    return {
        "path": rel_path,
        "status": "written",
        "delta": len(out) - len(src),
        "remaining_doctor": remaining,
    }


def _count_bare_doctor(text: str) -> int:
    """Count 'doctor' occurrences that are NOT inside a URL or a JSON URL field."""
    import re
    # Strip URLs and href values that mention doctor (external WebMD etc)
    stripped = re.sub(r'https?://[^\s"\'<>)]*doctor[^\s"\'<>)]*', '', text)
    return len(re.findall(r'\bdoctor\b', stripped, re.IGNORECASE))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would change without writing.")
    args = ap.parse_args()

    print(f"[scope] {len(REPLACEMENTS)} files, {sum(len(v) for v in REPLACEMENTS.values())} replacements\n")

    results = []
    for rel, pairs in REPLACEMENTS.items():
        r = scrub_file(rel, pairs, args.dry_run)
        results.append(r)
        status = r["status"]
        if status == "missing":
            print(f"[!] {rel} — MISSING on disk (skipped)")
        elif status == "pattern-not-found":
            print(f"[!] {rel} — patterns not found in pristine source (may already be scrubbed or file changed)")
            for m in r["missing"]:
                print(f"      missing: {m[:80]}...")
        elif status == "shrink-abort":
            print(f"[!] {rel} — SHRINK GUARD TRIPPED ({r['src_bytes']} -> {r['out_bytes']})")
        else:
            verb = "WOULD WRITE" if args.dry_run else "wrote"
            print(f"[ok] {rel} — {verb} (delta {r['delta']:+d} bytes; doctor-refs remaining: {r['remaining_doctor']})")

    # Summary
    ok = sum(1 for r in results if r["status"] in ("written", "dry-run"))
    bad = len(results) - ok
    print(f"\n[summary] {ok}/{len(results)} files scrubbed successfully; {bad} issue(s)")
    if bad:
        sys.exit(2)
    print("next: deploy modified landing pages via SFTP, then cache-bust verify")


if __name__ == "__main__":
    main()
