#!/usr/bin/env python3
"""
NPCWoods CSS/JS Extraction Migration Script
=============================================
Removes duplicated inline <style> and <script> blocks from all HTML pages
and replaces them with references to external files:
  - /assets/css/site.css  (nav, footer, reviews, save-contact CSS)
  - /assets/js/site.js    (nav, CWV, save-contact, fade-in JS)

Usage:
    python3 scripts/extract-shared-css-js.py [--dry-run]

Safety:
    - Only processes files in html/, landing-pages/, blog/ directories
    - Skips backups, automation-output, content-output, mockups, scripts
    - Uses signature-based matching (not exact content) to handle
      minified vs formatted variants
    - Never removes page-specific CSS/JS
    - Reports everything it does
"""

import os
import re
import sys
import hashlib
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv

# Repo root (script lives in scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories to process
TARGET_DIRS = ['html', 'landing-pages', 'blog']

# Directories to skip
SKIP_DIRS = {
    '.backups', 'backups', 'automation-output', 'content-output',
    'mockups', 'scripts', 'node_modules', 'shared'  # shared snippets already updated
}

# The CSS <link> tag to inject (if not already present)
CSS_LINK = '<link rel="stylesheet" href="/assets/css/site.css">'

# The JS <script> tag to inject (if not already present)
JS_SCRIPT = '<script src="/assets/js/site.js" defer></script>'


def has_real_css_link(content):
    """Return True only when the page has an actual site.css link tag."""
    return re.search(
        r'<link\b[^>]*href=["\'][^"\']*/assets/css/site\.css(?:\?[^"\']*)?["\'][^>]*>',
        content,
        re.IGNORECASE,
    ) is not None


def has_real_js_script(content):
    """Return True only when the page has an actual site.js script tag."""
    return re.search(
        r'<script\b[^>]*src=["\'][^"\']*/assets/js/site\.js(?:\?[^"\']*)?["\'][^>]*>',
        content,
        re.IGNORECASE,
    ) is not None


def find_html_files():
    """Find all HTML files in target directories, excluding skipped dirs."""
    files = []
    for d in TARGET_DIRS:
        dir_path = REPO_ROOT / d
        if not dir_path.exists():
            continue
        for root, dirs, filenames in os.walk(dir_path):
            # Skip excluded directories
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for f in filenames:
                if f.endswith('.html'):
                    files.append(Path(root) / f)
    return sorted(files)


def remove_nav_css(content):
    """Remove the nav/header CSS <style> block.
    Signature: contains '.npc-nav' and '.npc-slide-panel' in the same block.
    """
    def replacer(m):
        body = m.group(1)
        if '.npc-nav' in body and '.npc-slide-panel' in body:
            return '<!-- nav CSS: now in /assets/css/site.css -->'
        return m.group(0)

    return re.sub(r'<style[^>]*>(.*?)</style>', replacer, content, flags=re.DOTALL)


def remove_footer_css(content):
    """Remove the footer CSS <style> block.
    Signature: contains '.npc-site-footer' or '.npc-footer-inner' but NOT
    other major components (nav, save, reviews).
    """
    def replacer(m):
        body = m.group(1)
        # Must have footer classes
        if not ('.npc-site-footer' in body or '.npc-footer-inner' in body):
            return m.group(0)
        # Must NOT also contain nav or save (those are separate blocks or page-specific)
        if '.npc-nav' in body or '.npc-save-wrap' in body:
            return m.group(0)
        # Only remove if it's a standalone footer CSS block (< 5000 chars)
        # Larger blocks are page-specific CSS that happens to include footer styles
        if len(body.strip()) > 5000:
            return m.group(0)
        return '<!-- footer CSS: now in /assets/css/site.css -->'

    return re.sub(r'<style[^>]*>(.*?)</style>', replacer, content, flags=re.DOTALL)


def remove_reviews_css(content):
    """Remove the scrolling reviews banner CSS <style> block.
    Signature: contains 'SCROLLING REVIEWS BANNER' or '.reviews-banner' as the
    primary content (not mixed with other components).
    """
    def replacer(m):
        body = m.group(1)
        if '.reviews-banner' in body and '.npc-nav' not in body and '.npc-site-footer' not in body:
            # Must be primarily reviews CSS (< 4000 chars)
            if len(body.strip()) < 4000:
                return '<!-- reviews CSS: now in /assets/css/site.css -->'
        return m.group(0)

    return re.sub(r'<style[^>]*>(.*?)</style>', replacer, content, flags=re.DOTALL)


def remove_save_contact_css(content):
    """Remove the save-contact floating widget CSS <style> block.
    Signature: contains '.npc-save-wrap' as a standalone block.
    """
    def replacer(m):
        body = m.group(1)
        if '.npc-save-wrap' in body and '.npc-nav' not in body and '.npc-site-footer' not in body:
            if len(body.strip()) < 8000:
                return '<!-- save-contact CSS: now in /assets/css/site.css -->'
        return m.group(0)

    return re.sub(r'<style[^>]*>(.*?)</style>', replacer, content, flags=re.DOTALL)


def remove_nav_js(content):
    """Remove the nav/hamburger menu JS <script> block.
    Signature: IIFE containing 'npcHamburger' and 'npcSlidePanel'.
    """
    pattern = r'<script>\s*\(function\(\)\s*\{[^}]*?npcHamburger.*?\}\)\(\);\s*</script>'
    return re.sub(pattern, '<!-- nav JS: now in /assets/js/site.js -->', content, flags=re.DOTALL)


def remove_cwv_js(content):
    """Remove the Core Web Vitals reporter JS <script> block.
    Signature: IIFE containing '__npcCwvLoaded'.
    """
    # Match the CWV block and its preceding comment if present
    pattern = r'(?:<!-- =+ Core Web Vitals.*?-->\s*)?<script>\s*\(function\(\)\s*\{\s*if\s*\(window\.__npcCwvLoaded\).*?\}\)\(\);\s*</script>'
    return re.sub(pattern, '<!-- CWV JS: now in /assets/js/site.js -->', content, flags=re.DOTALL)


def remove_save_contact_js(content):
    """Remove the save-contact widget JS <script> block.
    Signature: IIFE containing 'npcSaveWrap' and 'npcSaveBtn'.
    """
    pattern = r'<script>\s*\(function\(\)\s*\{[^}]*?npcSaveWrap.*?\}\)\(\);\s*</script>'
    return re.sub(pattern, '<!-- save-contact JS: now in /assets/js/site.js -->', content, flags=re.DOTALL)


def remove_fadein_js(content):
    """Remove the fade-in IntersectionObserver JS <script> block.
    Signature: IIFE containing 'IntersectionObserver' and '.fade-in'.
    """
    pattern = r"<script>\s*\(function\(\)\s*\{[^}]*?IntersectionObserver.*?\.fade-in.*?\}\)\(\);\s*</script>"
    return re.sub(pattern, '<!-- fade-in JS: now in /assets/js/site.js -->', content, flags=re.DOTALL)


def inject_css_link(content):
    """Add the CSS <link> tag if not already present.
    Injects right after <body> or the first element after <body>.
    """
    if has_real_css_link(content):
        return content  # Already has it

    body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
    if body_match:
        insert_pos = body_match.end()
        return content[:insert_pos] + '\n' + CSS_LINK + content[insert_pos:]

    # Fallback: inject after the SVG icon defs block
    svg_end = content.find('</svg>', content.find('<svg style="display:none">'))
    if svg_end > 0:
        insert_pos = svg_end + len('</svg>')
        return content[:insert_pos] + '\n\n' + CSS_LINK + content[insert_pos:]

    return content  # Can't find injection point


def inject_js_script(content):
    """Add the JS <script> tag if not already present.
    Injects right before </body>.
    """
    if has_real_js_script(content):
        return content  # Already has it

    # Inject before </body>
    body_close = content.rfind('</body>')
    if body_close > 0:
        return content[:body_close] + JS_SCRIPT + '\n' + content[body_close:]

    # Fallback: inject before </html>
    html_close = content.rfind('</html>')
    if html_close > 0:
        return content[:html_close] + JS_SCRIPT + '\n' + content[html_close:]

    return content  # Can't find injection point


def ensure_shared_assets(content, stats):
    """Inject shared CSS/JS when removals happened or marker comments remain."""
    needs_css = bool(stats) or (
        '/assets/css/site.css' in content and not has_real_css_link(content)
    )
    needs_js = bool(stats) or (
        '/assets/js/site.js' in content and not has_real_js_script(content)
    )

    if needs_css and not has_real_css_link(content):
        updated = inject_css_link(content)
        if updated != content:
            content = updated
            stats['css_link'] = True

    if needs_js and not has_real_js_script(content):
        updated = inject_js_script(content)
        if updated != content:
            content = updated
            stats['js_script'] = True

    return content, stats


def clean_empty_comments(content):
    """Remove consecutive HTML comment lines left by the removals."""
    # Collapse multiple consecutive comment-only lines
    content = re.sub(r'(<!-- [a-z].*?site\.(css|js) -->\n){2,}',
                     lambda m: m.group().split('\n')[0] + '\n', content)
    # Remove excessive blank lines (3+ → 2)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    return content


def process_file(filepath):
    """Process a single HTML file. Returns (changed, stats_dict)."""
    original = filepath.read_text(encoding='utf-8')
    content = original
    stats = {}

    # Track what we remove
    orig_len = len(content)

    # Remove shared CSS blocks
    content = remove_nav_css(content)
    if len(content) < len(original):
        stats['nav_css'] = True

    prev = len(content)
    content = remove_footer_css(content)
    if len(content) < prev:
        stats['footer_css'] = True

    prev = len(content)
    content = remove_reviews_css(content)
    if len(content) < prev:
        stats['reviews_css'] = True

    prev = len(content)
    content = remove_save_contact_css(content)
    if len(content) < prev:
        stats['save_css'] = True

    # Remove shared JS blocks
    prev = len(content)
    content = remove_nav_js(content)
    if len(content) < prev:
        stats['nav_js'] = True

    prev = len(content)
    content = remove_cwv_js(content)
    if len(content) < prev:
        stats['cwv_js'] = True

    prev = len(content)
    content = remove_save_contact_js(content)
    if len(content) < prev:
        stats['save_js'] = True

    prev = len(content)
    content = remove_fadein_js(content)
    if len(content) < prev:
        stats['fadein_js'] = True

    content, stats = ensure_shared_assets(content, stats)

    # Clean up
    content = clean_empty_comments(content)

    changed = content != original
    if changed:
        stats['bytes_saved'] = orig_len - len(content)

    if changed and not DRY_RUN:
        filepath.write_text(content, encoding='utf-8')

    return changed, stats


def main():
    if DRY_RUN:
        print("=== DRY RUN MODE (no files will be modified) ===\n")

    files = find_html_files()
    print(f"Found {len(files)} HTML files to process\n")

    changed_count = 0
    skipped_count = 0
    total_saved = 0
    all_stats = {}

    for f in files:
        rel = f.relative_to(REPO_ROOT)
        changed, stats = process_file(f)

        if changed:
            changed_count += 1
            saved = stats.get('bytes_saved', 0)
            total_saved += saved
            removed = [k for k in stats if k != 'bytes_saved']
            print(f"  {'[DRY] ' if DRY_RUN else ''}UPDATED {rel}")
            print(f"         Removed: {', '.join(removed)}")
            print(f"         Saved: {saved:,} bytes ({saved/1024:.1f} KB)")
            for k in removed:
                all_stats[k] = all_stats.get(k, 0) + 1
        else:
            skipped_count += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY {'(DRY RUN)' if DRY_RUN else ''}")
    print(f"{'='*60}")
    print(f"Files processed:  {len(files)}")
    print(f"Files changed:    {changed_count}")
    print(f"Files skipped:    {skipped_count}")
    print(f"Total bytes saved: {total_saved:,} ({total_saved/1024:.1f} KB)")
    print(f"\nBlocks removed:")
    for k, v in sorted(all_stats.items()):
        print(f"  {k}: {v} pages")


if __name__ == '__main__':
    main()
