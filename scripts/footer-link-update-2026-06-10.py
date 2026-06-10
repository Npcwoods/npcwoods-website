#!/usr/bin/env python3
"""Footer link update — 2026-06-10.

Propagates the html/shared/footer-snippet.html link fixes to every page
that contains a pasted copy of the shared footer:

  1. Cold & Flu      -> /learn/covid-flu/      (was /conditions/)
  2. Allergies       -> /learn/allergic-reaction/ (was /conditions/)
  3. Skin Rashes     -> /learn/skin-infection/ (was /conditions/)
  4. Remove duplicate "Simple Pricing" link (keep "Pricing, $59")
  5. Add Strep Throat, Poison Ivy, GLP-1 Weight Loss to Conditions column
  6. Add FAQ after "Pricing, $59" in Quick Links
  7. Add Patient Education + Medications after Credentials in Quick Links

Per-file policy: ALL anchors must be present (and the inserted links must
not already exist) or the file is left completely untouched ("bailed").
Skips: .bak files, _archive/, html/shared/footer-snippet.html (source of
truth, already edited), landing-pages/sitemap/index.html (owned by another
agent).
"""
import os
import sys

ROOT = "/Users/macmini/Desktop/Chris-HQ/npcwoods-website"
SCAN_DIRS = ["landing-pages", "html"]

FOOTER_MARKER = "npc-site-footer"

# (old, new) exact-string replacements
REPLACEMENTS = [
    ('<li><a href="https://npcwoods.com/conditions/">Cold &amp; Flu</a></li>',
     '<li><a href="https://npcwoods.com/learn/covid-flu/">Cold &amp; Flu</a></li>'),
    ('<li><a href="https://npcwoods.com/conditions/">Allergies</a></li>',
     '<li><a href="https://npcwoods.com/learn/allergic-reaction/">Allergies</a></li>'),
    ('<li><a href="https://npcwoods.com/conditions/">Skin Rashes</a></li>',
     '<li><a href="https://npcwoods.com/learn/skin-infection/">Skin Rashes</a></li>'),
    # de-dupe pricing: remove the whole "Simple Pricing" line incl. newline
    ('          <li><a href="https://npcwoods.com/pricing/">Simple Pricing</a></li>\n',
     ''),
    # conditions column additions, inserted before "View All"
    ('          <li><a href="https://npcwoods.com/conditions/">View All &rarr;</a></li>',
     '          <li><a href="https://npcwoods.com/strep-throat-treatment/">Strep Throat</a></li>\n'
     '          <li><a href="https://npcwoods.com/poison-ivy/">Poison Ivy</a></li>\n'
     '          <li><a href="https://npcwoods.com/glp1-weight-loss/">GLP-1 Weight Loss</a></li>\n'
     '          <li><a href="https://npcwoods.com/conditions/">View All &rarr;</a></li>'),
    # quick links: FAQ after Pricing, $59
    ('          <li><a href="https://npcwoods.com/pricing/">Pricing, $59</a></li>',
     '          <li><a href="https://npcwoods.com/pricing/">Pricing, $59</a></li>\n'
     '          <li><a href="https://npcwoods.com/faq/">FAQ</a></li>'),
    # quick links: Patient Education + Medications after Credentials
    ('          <li><a href="https://npcwoods.com/credentials/">Credentials &amp; Licenses</a></li>',
     '          <li><a href="https://npcwoods.com/credentials/">Credentials &amp; Licenses</a></li>\n'
     '          <li><a href="https://npcwoods.com/learn/">Patient Education</a></li>\n'
     '          <li><a href="https://npcwoods.com/medications/">Medications</a></li>'),
]

# If any of these are already present, the page was already updated — skip it.
ALREADY_DONE_SENTINELS = [
    '<li><a href="https://npcwoods.com/poison-ivy/">Poison Ivy</a></li>',
    '<li><a href="https://npcwoods.com/faq/">FAQ</a></li>',
    '<li><a href="https://npcwoods.com/learn/">Patient Education</a></li>',
]

SKIP_PATHS = [
    os.path.join(ROOT, "landing-pages", "sitemap", "index.html"),
    os.path.join(ROOT, "html", "shared", "footer-snippet.html"),
]


def main():
    modified, skipped, bailed = [], [], []

    for d in SCAN_DIRS:
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, d)):
            if "_archive" in dirpath.split(os.sep):
                continue
            for fn in sorted(filenames):
                if not fn.endswith(".html"):
                    continue
                path = os.path.join(dirpath, fn)
                if ".bak" in fn or path in SKIP_PATHS:
                    skipped.append(path)
                    continue
                with open(path, encoding="utf-8") as f:
                    s = f.read()
                if FOOTER_MARKER not in s:
                    skipped.append(path)
                    continue
                if any(t in s for t in ALREADY_DONE_SENTINELS):
                    bailed.append((path, "already contains new footer links"))
                    continue
                missing = [old for old, _ in REPLACEMENTS if old not in s]
                if missing:
                    bailed.append((path, f"{len(missing)} anchor(s) not found"))
                    continue
                multi = [old for old, _ in REPLACEMENTS if s.count(old) != 1]
                if multi:
                    bailed.append((path, f"{len(multi)} anchor(s) not unique"))
                    continue
                for old, new in REPLACEMENTS:
                    s = s.replace(old, new)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(s)
                modified.append(path)

    print(f"MODIFIED: {len(modified)}")
    print(f"SKIPPED (no footer / .bak / excluded): {len(skipped)}")
    print(f"BAILED (anchor mismatch, left untouched): {len(bailed)}")
    for p, why in bailed:
        print(f"  BAIL {os.path.relpath(p, ROOT)} — {why}")
    if "--list" in sys.argv:
        for p in modified:
            print(f"  MOD  {os.path.relpath(p, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
