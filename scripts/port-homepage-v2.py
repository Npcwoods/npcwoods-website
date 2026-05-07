#!/usr/bin/env python3
"""Build the ported homepage PHP template + stage all upload assets.

Reads:
  - homepage-preview-v2.html  (approved preview, source of new main content)
  - homepage/page-npcwoods-home.php  (current production template)

Writes:
  - homepage/page-npcwoods-home.php  (SPLICED — replaces lines 2639-3812 with new main)
  - html/wp-content/uploads/2026/04/*.webp  (staged for SFTP)
  - html/wp-content/uploads/npc-data/*.json  (staged for SFTP)

Safe: does not touch <head>, nav, footer, tracking, JSON-LD, or footer JS.
"""
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / "homepage-preview-v2.html"
# Read from PRISTINE backup every run (script is idempotent this way).
# Writing to same target path is fine — backup is never touched.
PHP_SOURCE = ROOT / "backups" / "page-npcwoods-home-pre-mockup-port-2026-04-12.php"
PHP_TEMPLATE = ROOT / "homepage" / "page-npcwoods-home.php"
ASSETS_LOCAL = ROOT / "assets" / "homepage-v2"

# SFTP staging dirs (remote web root is `html/`)
STAGE_UPLOADS = ROOT / "html" / "wp-content" / "uploads" / "2026" / "04"
STAGE_DATA = ROOT / "html" / "wp-content" / "uploads" / "npc-data"

# WP media URL prefix for image src rewrites
WP_MEDIA_BASE = "/wp-content/uploads/2026/04"
WP_DATA_BASE = "/wp-content/uploads/npc-data"

# PHP splice boundaries (verified by inspection)
MAIN_START_LINE = 2639  # <main id="main">
MAIN_END_LINE = 3812    # </main>


def extract_preview_sections(preview_html: str) -> dict:
    """Pull out the pieces we need from the preview file."""
    out = {}

    # .home-v2 CSS block — everything from `.home-v2{` to the final `}` before </style>
    # The preview has one big <style> that includes .preview-notice, .home-v2 rules, .v2-ticker, and .preview-footer.
    # For production we want everything EXCEPT .preview-notice and .preview-footer.
    style_match = re.search(r"<style>(.*?)</style>", preview_html, re.DOTALL)
    if not style_match:
        raise RuntimeError("No <style> block found in preview")
    css = style_match.group(1)
    # Strip preview-only rules
    css = re.sub(r"/\*\s*=====\s*PREVIEW NOTICE BAR.*?=====\s*\*/.*?(?=/\*\s*=====\s*V2 HOMEPAGE STYLES)", "", css, flags=re.DOTALL)
    css = re.sub(r"\.preview-notice\{[^}]*\}", "", css)
    css = re.sub(r"\.preview-notice b\{[^}]*\}", "", css)
    css = re.sub(r"\.preview-footer\{[^}]*\}", "", css)
    css = re.sub(r"\.preview-footer b\{[^}]*\}", "", css)
    # Preview-only nav styles (.v2-nav) — keep OUT of production (prod has its own nav)
    css = re.sub(r"\.home-v2 nav\.v2-nav[^{]*\{[^}]*\}", "", css)
    css = re.sub(r"\.home-v2 nav\.v2-nav \.bar[^{]*\{[^}]*\}", "", css)
    css = re.sub(r"\.home-v2 nav\.v2-nav ul[^{]*\{[^}]*\}", "", css)
    css = re.sub(r"\.home-v2 nav\.v2-nav ul a[^{]*\{[^}]*\}", "", css)
    css = re.sub(r"\.home-v2 nav\.v2-nav ul a:hover\{[^}]*\}", "", css)
    # The @media rule contains a `.home-v2 nav.v2-nav ul{display:none}` — leave as dead selector (harmless)
    out["css"] = css.strip()

    # <main>...</main> content
    main_match = re.search(r"<main>(.*?)</main>", preview_html, re.DOTALL)
    if not main_match:
        raise RuntimeError("No <main> found in preview")
    main_html = main_match.group(1).strip()
    # Rewrite local asset paths to WP media URLs
    main_html = main_html.replace('src="assets/homepage-v2/', f'src="{WP_MEDIA_BASE}/')
    out["main_html"] = main_html

    # Activity ticker div
    ticker_match = re.search(r'(<div class="v2-ticker[^>]*>.*?</div>\s*</div>|<div class="v2-ticker[^>]*>.*?</div>)',
                             preview_html, re.DOTALL)
    # Simpler: find by id
    t2 = re.search(r'<div class="v2-ticker hide" id="ticker"[^>]*>.*?</div>', preview_html, re.DOTALL)
    if not t2:
        raise RuntimeError("Ticker div not found")
    out["ticker"] = t2.group(0)

    # Inline data scripts
    status_script = re.search(r'<script id="npc-status-data"[^>]*>[^<]*</script>', preview_html)
    activity_script = re.search(r'<script id="npc-activity-data"[^>]*>[^<]*</script>', preview_html)
    if not status_script or not activity_script:
        raise RuntimeError("Inline data scripts not found")
    out["status_script"] = status_script.group(0)
    out["activity_script"] = activity_script.group(0)

    # Main interactive <script> (IIFE) — the big one at the bottom (NOT the save-contact IIFE)
    # Find <script> blocks without an id attribute; pick the one containing "STATUS CHIP"
    scripts = re.findall(r"<script>(.*?)</script>", preview_html, re.DOTALL)
    main_script = None
    for s in scripts:
        if "STATUS CHIP" in s and "SAVINGS CALCULATOR" in s:
            main_script = s
            break
    if not main_script:
        raise RuntimeError("Main <script> block not found")
    # Also rewrite the texture.webp CSS reference — already inside our CSS
    out["main_script"] = main_script.strip()

    # Rewrite texture.webp path in CSS
    out["css"] = out["css"].replace(
        "url('assets/homepage-v2/texture.webp')",
        f"url('{WP_MEDIA_BASE}/texture.webp')"
    )

    # Contact-save-snippet block (the <style>, <div>, <script> for vCard)
    # Find marker: <!-- NPCWoods Contact Save (shared snippet...
    cs_match = re.search(
        r"<!-- NPCWoods Contact Save.*?</script>",
        preview_html, re.DOTALL
    )
    if not cs_match:
        raise RuntimeError("Contact save snippet not found")
    contact_snippet = cs_match.group(0)
    # Rewrite the local avatar path to WP media URL
    contact_snippet = contact_snippet.replace(
        'src="assets/homepage-v2/chris-400.webp"',
        f'src="{WP_MEDIA_BASE}/chris-400.webp"'
    )
    out["contact_snippet"] = contact_snippet

    return out


def build_new_main_block(sections: dict) -> str:
    """Assemble the production-ready <main> block."""
    parts = [
        '<!-- MAIN (v2 homepage port 2026-04-12) -->',
        '<main id="main">',
        '',
        '<style>',
        sections["css"],
        '</style>',
        '',
        f'<script>window.NPC_DATA_BASE = "{WP_DATA_BASE}";</script>',
        sections["status_script"],
        sections["activity_script"],
        '',
        '<div class="home-v2">',
        sections["main_html"],
        '</div><!-- /.home-v2 -->',
        '',
        sections["ticker"],
        '',
        '<script>',
        sections["main_script"],
        '</script>',
        '',
        '</main>',
    ]
    return "\n".join(parts)


def splice_php(php_lines: list, new_main: str, contact_snippet: str) -> list:
    """Rebuild PHP with new main + contact snippet (before </body>)."""
    # Keep lines 1..2638 (index 0..2637)  [MAIN_START_LINE - 1 = 2638 means index 2638, so slice [:2638]]
    pre = php_lines[:MAIN_START_LINE - 1]
    # Replace lines 2639..3812 with new_main
    # Keep lines 3813..end (index 3812..)
    post = php_lines[MAIN_END_LINE:]

    out_lines = pre + [new_main + "\n"] + post

    # Insert contact snippet right before </body>
    rebuilt = "".join(out_lines)
    if "<!-- NPCWoods Contact Save" in rebuilt:
        print("[warn] contact snippet already present in PHP — skipping re-insertion")
    else:
        rebuilt = rebuilt.replace("</body>", contact_snippet + "\n</body>", 1)

    return rebuilt


def stage_assets():
    """Copy WebP + JSON files into the html/wp-content/uploads/ structure for SFTP."""
    STAGE_UPLOADS.mkdir(parents=True, exist_ok=True)
    STAGE_DATA.mkdir(parents=True, exist_ok=True)

    webp_files = sorted(ASSETS_LOCAL.glob("*.webp"))
    for f in webp_files:
        dest = STAGE_UPLOADS / f.name
        shutil.copy2(f, dest)
        print(f"  staged: {dest.relative_to(ROOT)}")

    for name in ("status.json", "activity.json"):
        src = ASSETS_LOCAL / name
        dest = STAGE_DATA / name
        shutil.copy2(src, dest)
        print(f"  staged: {dest.relative_to(ROOT)}")


def main():
    print("Reading preview…")
    preview_html = PREVIEW.read_text(encoding="utf-8")
    sections = extract_preview_sections(preview_html)
    print(f"  css: {len(sections['css'])} chars")
    print(f"  main_html: {len(sections['main_html'])} chars")
    print(f"  main_script: {len(sections['main_script'])} chars")
    print(f"  contact_snippet: {len(sections['contact_snippet'])} chars")

    print("Reading pristine PHP template from backup…")
    php_text = PHP_SOURCE.read_text(encoding="utf-8")
    php_lines = php_text.splitlines(keepends=True)
    print(f"  {len(php_lines)} lines total (source: {PHP_SOURCE.relative_to(ROOT)})")
    # Sanity check: splice boundaries only valid on the pristine 4069-line original
    if len(php_lines) < 4000:
        raise RuntimeError(
            f"PHP source has {len(php_lines)} lines — expected ~4069. "
            "Splice boundaries would corrupt the file. Aborting."
        )

    print("Building new main block…")
    new_main = build_new_main_block(sections)

    print("Splicing PHP…")
    new_php = splice_php(php_lines, new_main, sections["contact_snippet"])

    out_path = PHP_TEMPLATE
    out_path.write_text(new_php, encoding="utf-8")
    print(f"  wrote: {out_path.relative_to(ROOT)} ({len(new_php)} bytes)")

    print("Staging upload assets…")
    stage_assets()

    # Guardrail grep
    print("Guardrail grep on new PHP…")
    for term in ("doctor", "Text a Doctor"):
        hits = [
            (i + 1, line.rstrip("\n"))
            for i, line in enumerate(new_php.splitlines())
            if term.lower() in line.lower()
        ]
        if hits:
            print(f"  [WARN] '{term}' found at {len(hits)} line(s):")
            for ln, content in hits[:5]:
                print(f"    L{ln}: {content[:100]}")
        else:
            print(f"  '{term}': 0 hits  ✓")
    # Insurance — only flag if not the cash-pay FAQ
    ins_hits = [
        (i + 1, line.rstrip("\n"))
        for i, line in enumerate(new_php.splitlines())
        if "insurance" in line.lower()
    ]
    print(f"  'insurance': {len(ins_hits)} hit(s)")
    for ln, content in ins_hits[:10]:
        print(f"    L{ln}: {content.strip()[:110]}")

    print("\nDone. Files to upload via SFTP:")
    print(f"  homepage/page-npcwoods-home.php")
    print(f"  html/wp-content/uploads/2026/04/*.webp")
    print(f"  html/wp-content/uploads/npc-data/*.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
