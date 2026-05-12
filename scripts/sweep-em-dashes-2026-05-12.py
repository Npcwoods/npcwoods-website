#!/usr/bin/env python3
"""
Scoped em-dash sweep for NPCWoods static HTML/PHP pages.

Replaces em-dashes (—, &mdash;, &#8212;) with contextual punctuation:
- Inside <title> and og:title/twitter:title meta content → ' | '
- Elsewhere in body text → contextual: '. ' if followed by clause-starter, ', ' otherwise

Hard rules:
- Skip content inside <script>...</script> (covers JSON-LD)
- Skip content inside <style>...</style>
- Skip files in protected dirs (.git, backups, automation-output, mockups, scripts/wp-backups)
- Skip .bak files and obvious test/scratch files
- Fail-fast on corruption signatures from prior bad sweeps

Creates *.em-dash-bak-v2 backups before modifying.

Usage:
    /usr/bin/python3 scripts/sweep-em-dashes-2026-05-12.py [--dry-run]
"""

import re, os, sys, shutil

REPO_ROOT = "/Users/chriswoods/Desktop/Chris-HQ/npcwoods-website"

# What to exclude
EXCLUDED_DIRS = [
    "/.git/", "/backups/", "/automation-output/", "/mockups/",
    "/scripts/wp-backups/", "/scripts/.backups/", "/assets/homepage-v2/",
]
EXCLUDED_PATTERNS = [
    ".bak", "test-strep-throat-landing-page", "test-uti-landing-page",
    "LESSONS-TO-APPEND", "seo-fixes-checklist", "indexing-deep-dive",
    "homepage-preview", "homepage-updates-draft", "homepage-backup",
]
# Skip PHP for this sweep — risky, lower priority, do separately
EXCLUDE_PHP = True

# Protected ranges (do not modify em-dashes inside these)
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)

# Title contexts (use pipe replacement instead of comma/period)
TITLE_TAG_RE = re.compile(r"(<title[^>]*>)(.*?)(</title>)", re.DOTALL | re.IGNORECASE)
# meta property/name="(og:|twitter:|)title" with content
META_TITLE_RE = re.compile(
    r'(<meta\b[^>]*?(?:property|name)\s*=\s*["\'](?:og:|twitter:)?title["\'][^>]*?content\s*=\s*["\'])([^"\']*)(["\'])',
    re.IGNORECASE,
)

# Em-dash pattern (consumes adjacent whitespace so we control spacing on both sides)
EMDASH_RE = re.compile(r"\s*(?:—|&mdash;|&#8212;)\s*")

# Words that, when they come immediately after the em-dash, suggest a new clause/sentence → use period
CLAUSE_STARTERS_RE = re.compile(
    r"^(?:It|Treatment|Antibiotics|Chris|This|No|Most|Some|Many|All|We|You|I|My|Our|"
    r"That|Here|Just|Same|Real|Safe|Yes|Sometimes|Often|Usually|Every|Whether|These|"
    r"Those|Plus|Also|And|But|So|Or|Now|Then|Today|First|Second|Third|Last|After|"
    r"Before|During|When|If|Once|Antibiotic|Take|Drink|Stop|Call|Text|Email|Visit|Read|"
    r"Need|Want|Don|Get|Make|See|Look|Find|Use|Try|Let|Order|Skip|Talk|Reviewed|"
    r"Licensed|MSN|APRN|FNP|Double|Bare|Plain|Regular|Same|Real|Sent|Picked|Common|"
    r"Brand|Generic|Symptoms|Side|Dosing|Resistance|Bacterial|Viral|Safety|Pregnancy|"
    r"Allergies|Children|Adults|Pediatric|Each|Per|Both|Either|Neither|"
    r"Start|Open|Close|Tap|Click|Send|Receive|Sign|Login|Submit|Confirm|Cancel|Continue|"
    r"Back|Next|Yes|No|Maybe|Whenever|Wherever|However|Therefore|Thus|Hence|Meanwhile|"
    r"Board|Certified|Nurse|Practitioner|Doctor|Patient|Provider|Pharmacy|Pharmacist|"
    r"Within|Around|About|Above|Below|Outside|Inside|Total|Free|Easy|Quick|Fast|Slow|"
    r"Step|Stage|Phase|Day|Week|Month|Year|Hour|Minute|Second|Morning|Evening|Night|"
    r"Available|Open|Closed|Active|Inactive|Pending|Complete|Done|Ready|Set|Go)\b"
)

# Corruption signatures to detect post-write
CORRUPTION_SIGS = [
    "DM Sanssection", "isDM Sanssect", "in-personian",
    "no-simple pricing", "Do I need simple pricing",
]


def replace_in_title_chunks(text: str) -> str:
    """Replace em-dashes inside <title> and og:title meta with ' | '."""
    def title_tag_repl(m):
        return m.group(1) + EMDASH_RE.sub(" | ", m.group(2)) + m.group(3)

    def meta_title_repl(m):
        return m.group(1) + EMDASH_RE.sub(" | ", m.group(2)) + m.group(3)

    text = TITLE_TAG_RE.sub(title_tag_repl, text)
    text = META_TITLE_RE.sub(meta_title_repl, text)
    return text


def replace_in_body(text: str) -> str:
    """Replace remaining em-dashes contextually (period before clause-starter, else comma)."""
    out = []
    last = 0
    for m in EMDASH_RE.finditer(text):
        out.append(text[last:m.start()])
        after = text[m.end():m.end() + 60]
        stripped = after.lstrip()
        word_match = re.match(r"[A-Z][A-Za-z]*", stripped)
        if word_match and CLAUSE_STARTERS_RE.match(word_match.group()):
            out.append(". ")
        else:
            out.append(", ")
        last = m.end()
    out.append(text[last:])
    return "".join(out)


def process_file(path: str, dry_run: bool = False):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_em = content.count("—") + content.count("&mdash;") + content.count("&#8212;")
    if orig_em == 0:
        return None

    # Identify protected ranges (script + style)
    protected_spans = []
    for regex in (SCRIPT_RE, STYLE_RE):
        for m in regex.finditer(content):
            protected_spans.append((m.start(), m.end()))
    protected_spans.sort()

    # Merge overlapping spans defensively
    merged = []
    for s, e in protected_spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    protected_spans = merged

    # Build interleaved chunks
    chunks = []
    last = 0
    for s, e in protected_spans:
        if s > last:
            chunks.append(("text", content[last:s]))
        chunks.append(("protected", content[s:e]))
        last = e
    if last < len(content):
        chunks.append(("text", content[last:]))

    # Process text chunks
    new_parts = []
    for kind, chunk in chunks:
        if kind == "protected":
            new_parts.append(chunk)
        else:
            # Title-first (pipe), then body (comma/period)
            chunk = replace_in_title_chunks(chunk)
            chunk = replace_in_body(chunk)
            new_parts.append(chunk)
    new_content = "".join(new_parts)

    # Validate: no corruption introduced
    for sig in CORRUPTION_SIGS:
        if sig in new_content and sig not in content:
            raise RuntimeError(f"Corruption signature introduced in {path}: {sig}")

    new_em = new_content.count("—") + new_content.count("&mdash;") + new_content.count("&#8212;")
    if new_em > orig_em:
        raise RuntimeError(f"Em-dash count increased in {path}: {orig_em} -> {new_em}")

    if dry_run:
        return (orig_em, new_em, len(content), len(new_content), False)

    # Backup
    backup = path + ".em-dash-bak-v2"
    if not os.path.exists(backup):
        shutil.copy2(path, backup)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return (orig_em, new_em, len(content), len(new_content), True)


def find_candidates() -> list[str]:
    candidates = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip excluded dirs
        rel = root.replace(REPO_ROOT, "")
        if any(d in (rel + "/") for d in EXCLUDED_DIRS):
            continue
        for f in files:
            if not (f.endswith(".html") or (not EXCLUDE_PHP and f.endswith(".php"))):
                continue
            if any(p in f for p in EXCLUDED_PATTERNS):
                continue
            full = os.path.join(root, f)
            # Quick em-dash presence check
            try:
                with open(full, "r", encoding="utf-8") as fh:
                    c = fh.read()
            except Exception:
                continue
            if "—" in c or "&mdash;" in c or "&#8212;" in c:
                candidates.append(full)
    return sorted(candidates)


def main():
    dry_run = "--dry-run" in sys.argv
    candidates = find_candidates()
    print(f"Found {len(candidates)} candidate HTML files with em-dashes.")
    print(f"Dry-run: {dry_run}")
    print()

    total_orig = 0
    total_new = 0
    modified = []
    errors = []
    for path in candidates:
        try:
            res = process_file(path, dry_run=dry_run)
            if res is None:
                continue
            orig_em, new_em, orig_size, new_size, wrote = res
            total_orig += orig_em
            total_new += new_em
            modified.append((path, orig_em, new_em, orig_size, new_size))
        except Exception as e:
            errors.append((path, str(e)))

    print(f"Processed: {len(modified)} files")
    print(f"Total em-dashes: {total_orig} -> {total_new}  (removed: {total_orig - total_new})")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for path, err in errors:
            print(f"  {path}: {err}")
    print()
    print("=== Top 10 files by em-dashes removed ===")
    modified.sort(key=lambda x: -(x[1] - x[2]))
    for path, oe, ne, os_, ns_ in modified[:10]:
        print(f"  {path.replace(REPO_ROOT + '/', ''):60s}  {oe:4d} -> {ne:3d}  (Δbytes {ns_ - os_:+5d})")


if __name__ == "__main__":
    main()
