#!/usr/bin/env python3
"""Remove every `Pharmacy Info` / `Pharmacy Partners` nav/footer `<li>` and
mobile slide-out panel link from every page on the site.

Handles three structural forms of the same nav surface:
  1. Single-line <li>...</li> with optional inline styles / attributes — covers
     every footer Quick Links block and the minified footer variants on state
     pages (e.g. nevada-telemedicine).
  2. Multi-line 3-line <li> block (classic desktop header nav).
  3. The /how-it-works/ mobile slide-out panel card — same conceptual nav entry
     but uses a different markup (<a class="npc-panel-link">).

Idempotent: runs on string/regex match. No-ops if nothing to do. Writes a
`.pharmacy-bak` sidecar on first change per file (never overwrites).

Per feedback_splice_script_idempotency.md: uses content matching (regex), not
line-number slicing, so re-runs are always safe.

Body-content cross-links (class="cross-link", class="link-card") on state and
condition pages are NOT touched by this script — those are body content and
need a separate decision.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "html", ROOT / "landing-pages", ROOT / "blog"]
EXTRA_FILES = [ROOT / "homepage" / "page-npcwoods-home.php"]

# Skip these trees / files entirely.
SKIP_CONTAINS = (
    "/automation-output/",
    "/backups/",
    "/mockups/",
    "/_archive/",
)


# Form 1: single-line <li> (optionally with attributes/styles) wrapping the
# pharmacy link. Consumes any leading indentation and trailing newline so we
# don't leave blank-line gaps. Works even when multiple <li>s are on ONE line
# (minified footer) because the pattern doesn't require `\n` anchors.
SINGLE_LI_RE = re.compile(
    r'(?:^[ \t]*)?<li[^>]*><a[^>]*href="https://npcwoods\.com/pharmacy(?:-partners)?/"[^>]*>Pharmacy (?:Info|Partners)</a></li>\n?',
    re.MULTILINE,
)

# Form 2: multi-line 3-line <li> block — header nav style.
MULTI_LI_RE = re.compile(
    r'[ \t]*<li>[ \t]*\n'
    r'[ \t]*<a[^>]*href="https://npcwoods\.com/pharmacy(?:-partners)?/"[^>]*>Pharmacy (?:Info|Partners)</a>[ \t]*\n'
    r'[ \t]*</li>[ \t]*\n'
)

# Form 3: /how-it-works/ mobile slide-out panel link.
PANEL_RE = re.compile(
    r'[ \t]*<a href="https://npcwoods\.com/pharmacy/" class="npc-panel-link">[ \t]*\n'
    r'[ \t]*<div class="npc-panel-link-icon">[^<]*</div>[ \t]*\n'
    r'[ \t]*<div class="npc-panel-link-text">Pharmacy Info<div class="npc-panel-link-sub">[^<]*</div></div>[ \t]*\n'
    r'[ \t]*<span class="npc-panel-link-arrow">[^<]*</span>[ \t]*\n'
    r'[ \t]*</a>[ \t]*\n'
)


def scrub(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError, PermissionError):
        return "skipped"

    new_text = MULTI_LI_RE.sub("", text)
    new_text = PANEL_RE.sub("", new_text)
    new_text = SINGLE_LI_RE.sub("", new_text)

    if new_text == text:
        return "noop"

    bak = path.with_suffix(path.suffix + ".pharmacy-bak")
    if not bak.exists():
        bak.write_text(text, encoding="utf-8")
    path.write_text(new_text, encoding="utf-8")
    return "cleaned"


def iter_targets():
    for root in SCAN_DIRS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            name = p.name
            if name.endswith((".bak", ".pharmacy-bak", ".synced.bak", ".meta-bak", ".cwv-bak")):
                continue
            if p.suffix not in {".html", ".php"}:
                continue
            if any(s in str(p) for s in SKIP_CONTAINS):
                continue
            yield p
    for p in EXTRA_FILES:
        if p.exists():
            yield p


def main() -> int:
    cleaned = 0
    noop = 0
    skipped = 0
    for path in iter_targets():
        result = scrub(path)
        if result == "cleaned":
            cleaned += 1
            print(f"[clean] {path.relative_to(ROOT)}")
        elif result == "skipped":
            skipped += 1
        else:
            noop += 1

    print()
    print(f"  cleaned: {cleaned}")
    print(f"  noop:    {noop}")
    print(f"  skipped: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
