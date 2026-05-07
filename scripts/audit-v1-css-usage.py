#!/usr/bin/env python3
"""
audit-v1-css-usage.py

Phase 1 audit of legacy v1 CSS in /homepage/page-npcwoods-home.php.

Reads the v1 <style> block (currently lines 37..2121), extracts every CSS
selector (handling top-level rules and nested @media blocks), and emits a
TSV verdict manifest.

For each selector:
  - look up where its anchor tokens (class/id/tag) appear in markup and JS
  - decide KEEP / DELETE / INVESTIGATE based on:
      * is the selector referenced in markup outside .home-v2 (LIVE)?
      * is the selector referenced ONLY inside .home-v2? (SHADOWED -> DELETE)
      * does v2 explicitly !important-reset the same selector? (DEAD -> DELETE)
      * is the selector wired to JS hooks?

Idempotent. Re-running overwrites only the TSV. No mutation of source.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

ROOT = "/Users/chriswoods/Desktop/Chris-HQ/npcwoods-website"
HOMEPAGE = os.path.join(ROOT, "homepage", "page-npcwoods-home.php")
TSV_OUT  = os.path.join(ROOT, "scripts", "v1-css-cleanup-manifest-2026-04-30.tsv")


# ----------------------------------------------------------------------
# Step 1: locate boundaries dynamically (don't trust the docstring numbers)
# ----------------------------------------------------------------------

def load_lines() -> list[str]:
    with open(HOMEPAGE, "r", encoding="utf-8") as f:
        return f.readlines()


def find_boundaries(lines: list[str]) -> dict:
    """Find the line spans we care about. 1-indexed inclusive."""
    style_starts = [i + 1 for i, l in enumerate(lines) if re.match(r"^\s*<style\b", l)]
    style_ends   = [i + 1 for i, l in enumerate(lines) if re.match(r"^\s*</style>", l)]

    # The first <style>...</style> is v1 legacy. Second is v2 (.home-v2 scoped).
    if len(style_starts) < 2 or len(style_ends) < 2:
        raise RuntimeError(f"Expected at least 2 <style> blocks; got starts={style_starts} ends={style_ends}")

    v1_start, v1_end = style_starts[0], style_ends[0]
    v2_start, v2_end = style_starts[1], style_ends[1]

    # home-v2 wrapper opens after main; closes via </main>
    home_v2_open = next(
        (i + 1 for i, l in enumerate(lines) if 'class="home-v2"' in l),
        None,
    )
    main_close = next(
        (i + 1 for i, l in enumerate(lines) if re.match(r"^\s*</main>", l)),
        None,
    )

    return {
        "v1_style":   (v1_start, v1_end),
        "v2_style":   (v2_start, v2_end),
        "home_v2":    (home_v2_open, main_close),
        "n":          len(lines),
    }


# ----------------------------------------------------------------------
# Step 2: extract every CSS selector inside v1 block, with line span
# ----------------------------------------------------------------------

@dataclass
class Rule:
    selector: str          # the raw selector list, e.g. ".foo, .bar:hover"
    line_start: int
    line_end: int
    inside_media: str | None  # e.g. "@media (max-width: 640px)" or None
    block_bytes: int       # approx bytes for the rule block (selector + body)


COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def strip_comments(src: str) -> str:
    return COMMENT_RE.sub("", src)


def extract_rules(lines: list[str], v1_start: int, v1_end: int) -> list[Rule]:
    """
    Walk the v1 <style> block. Track brace depth.
      depth 0 -> inside top-level CSS region
      @media starts a brace block; rules INSIDE it are nested
    """
    rules: list[Rule] = []

    # Build a list of (line_no, char_offset_in_concat, char) so we can map
    # any char position in the joined string back to a line number.
    block_lines = lines[v1_start:v1_end - 1]   # exclude <style> and </style> tags
    base_line_no = v1_start + 1                # the line of the first content line after <style>

    src = "".join(block_lines)
    # Build line-offset table
    line_offsets = []
    pos = 0
    for ln, line in enumerate(block_lines):
        line_offsets.append(pos)
        pos += len(line)
    line_offsets.append(pos)  # sentinel

    def line_of(char_idx: int) -> int:
        # binary-ish search; small file, linear is fine
        for i in range(len(line_offsets) - 1):
            if line_offsets[i] <= char_idx < line_offsets[i + 1]:
                return base_line_no + i
        return base_line_no + len(block_lines) - 1

    src_clean = strip_comments(src)
    # NOTE: stripping comments shifts char positions vs. original src. To keep
    # line attribution correct, replace each comment with same-length spaces.
    def blank_comments(s: str) -> str:
        out = []
        last = 0
        for m in re.finditer(r"/\*.*?\*/", s, re.DOTALL):
            out.append(s[last:m.start()])
            # preserve newlines so line counts stay aligned
            blanked = re.sub(r"[^\n]", " ", m.group(0))
            out.append(blanked)
            last = m.end()
        out.append(s[last:])
        return "".join(out)

    src2 = blank_comments(src)

    # Now scan with brace tracking.
    i = 0
    n = len(src2)
    media_stack: list[str] = []   # nesting of @media or @supports etc.

    while i < n:
        ch = src2[i]
        if ch.isspace():
            i += 1
            continue

        # @rule (could be @media, @supports, @keyframes, @import, @font-face)
        if ch == "@":
            # find end of the @-prelude up to '{' or ';'
            j = i
            while j < n and src2[j] not in "{;":
                j += 1
            prelude = src2[i:j].strip()
            if j < n and src2[j] == ";":
                # @import / @charset -> single-line rule, not a block
                rule_start_ln = line_of(i)
                rule_end_ln   = line_of(j)
                rules.append(Rule(
                    selector=prelude,
                    line_start=rule_start_ln,
                    line_end=rule_end_ln,
                    inside_media=media_stack[-1] if media_stack else None,
                    block_bytes=(j - i + 1),
                ))
                i = j + 1
                continue
            elif j < n and src2[j] == "{":
                # block @-rule. If @media/@supports, we recurse into its body.
                head = prelude.split()[0] if prelude else "@?"
                if head in ("@media", "@supports"):
                    media_stack.append(prelude)
                    i = j + 1
                    continue
                else:
                    # @keyframes, @font-face, etc. -> treat the whole thing as a single rule
                    depth = 1
                    k = j + 1
                    while k < n and depth > 0:
                        if src2[k] == "{":
                            depth += 1
                        elif src2[k] == "}":
                            depth -= 1
                        k += 1
                    rules.append(Rule(
                        selector=prelude,
                        line_start=line_of(i),
                        line_end=line_of(k - 1),
                        inside_media=media_stack[-1] if media_stack else None,
                        block_bytes=(k - i),
                    ))
                    i = k
                    continue

        # Closing brace for an @media/@supports block
        if ch == "}":
            if media_stack:
                media_stack.pop()
            i += 1
            continue

        # Regular selector list. Read up to '{' but skip braces inside ()/[]
        j = i
        paren = 0
        bracket = 0
        while j < n:
            c = src2[j]
            if c == "(":
                paren += 1
            elif c == ")":
                paren -= 1
            elif c == "[":
                bracket += 1
            elif c == "]":
                bracket -= 1
            elif c == "{" and paren == 0 and bracket == 0:
                break
            elif c == "}" and paren == 0 and bracket == 0:
                # malformed or stray -> bail
                break
            j += 1
        if j >= n or src2[j] != "{":
            i = j + 1
            continue

        selector = re.sub(r"\s+", " ", src2[i:j]).strip()

        # consume the body
        depth = 1
        k = j + 1
        while k < n and depth > 0:
            if src2[k] == "{":
                depth += 1
            elif src2[k] == "}":
                depth -= 1
            k += 1

        rules.append(Rule(
            selector=selector,
            line_start=line_of(i),
            line_end=line_of(k - 1),
            inside_media=media_stack[-1] if media_stack else None,
            block_bytes=(k - i),
        ))
        i = k

    return rules


# ----------------------------------------------------------------------
# Step 3: collect markup/JS evidence
# ----------------------------------------------------------------------

# Anchor tokens to look for, derived from each selector.
# Examples:
#   ".foo .bar:hover"  -> ["foo", "bar"]   (classes)
#   "#bar"             -> ids = ["bar"]
#   "section.hero"     -> tag "section" + class "hero"
#   ".reveal.visible"  -> ["reveal", "visible"]
CLASS_RE = re.compile(r"\.([A-Za-z_][A-Za-z0-9_-]*)")
ID_RE    = re.compile(r"#([A-Za-z_][A-Za-z0-9_-]*)")


def selector_tokens(selector: str) -> dict:
    classes = set(CLASS_RE.findall(selector))
    ids     = set(ID_RE.findall(selector))
    return {"classes": classes, "ids": ids}


@dataclass
class Region:
    """A line-span region of the homepage file that we can search in."""
    name: str
    start: int  # 1-indexed inclusive
    end: int    # 1-indexed inclusive
    text: str


def build_regions(lines: list[str], b: dict) -> dict[str, Region]:
    def slice_text(s: int, e: int) -> str:
        # 1-indexed inclusive -> python list slice
        return "".join(lines[max(0, s - 1):e])

    v1s, v1e = b["v1_style"]
    v2s, v2e = b["v2_style"]
    hv2s, hv2e = b["home_v2"]
    n = b["n"]

    # markup-outside-home-v2: from after v1 </style> to before <div class="home-v2">,
    # PLUS from after </main> to end of file.
    pre_main_start  = v1e + 1
    pre_main_end    = (hv2s - 1) if hv2s else (v2s - 1)
    post_main_start = (hv2e + 1) if hv2e else None
    post_main_end   = n

    pre_text  = slice_text(pre_main_start, pre_main_end) if pre_main_end >= pre_main_start else ""
    post_text = slice_text(post_main_start, post_main_end) if (post_main_start and post_main_end >= post_main_start) else ""
    outside_v2_text = pre_text + "\n" + post_text

    inside_v2_text  = slice_text(hv2s, hv2e) if (hv2s and hv2e) else ""

    # JS regions: any <script>...</script> not the schema JSON. We treat all
    # <script> bodies after the v1 style block as JS evidence.
    js_chunks = []
    in_script = False
    script_buf = []
    for idx, line in enumerate(lines, start=1):
        if idx <= v1e:
            continue
        if "<script" in line and "application/ld+json" not in line:
            in_script = True
            script_buf = [line]
            continue
        if in_script:
            script_buf.append(line)
            if "</script>" in line:
                js_chunks.append("".join(script_buf))
                in_script = False
                script_buf = []
    js_text = "\n".join(js_chunks)

    return {
        "outside_v2": Region("outside_v2", pre_main_start, post_main_end or n, outside_v2_text),
        "inside_v2":  Region("inside_v2",  hv2s or 0, hv2e or 0, inside_v2_text),
        "js":         Region("js",         v1e + 1, n, js_text),
    }


# ----------------------------------------------------------------------
# Step 4: verdict logic
# ----------------------------------------------------------------------

# v2 has !important resets that explicitly neutralize v1 styling for these classes.
# Lines (current): 2631-2645 (.home-v2 section.hero, .home-v2 section.steps, .home-v2 .step,
#                              .home-v2 .stars).
V2_OVERRIDDEN = {"hero", "steps", "step", "stars"}

# v2 also forces the nav back to white at lines ~2651-2657 (.npc-nav inside .home-v2 wrapper context).
# The nav itself sits OUTSIDE .home-v2, so v1 .npc-nav rules still apply when scrolled.
# But the v1 transparent-over-hero rules at 850-867 (.npc-nav:not(.scrolled)) may be
# overridden by the v2 reset at 2651-2657 since v2 lives outside .home-v2 too in those rules
# (note: .home-v2 is on a DIV inside <main>, but those v2 rules are NOT prefixed with .home-v2).
# We mark these as INVESTIGATE.
V2_NAV_RESET_LINES = (2645, 2660)  # approximate range of v2 .npc-nav force-white reset

# Selectors whose rules MUST be kept regardless of automated guess.
# These are the "load-bearing" production systems.
HARD_KEEP_TOKENS = {
    # nav system (lines ~343-867 minus 850-867 transparent rules)
    "npc-nav", "npc-nav-inner", "npc-nav-logo", "npc-nav-links", "npc-nav-cta",
    "npc-nav-toggle", "npc-dropdown", "nav-arrow",
    "npc-menu-overlay", "npc-slide-panel", "npc-panel-header", "npc-panel-logo",
    "npc-panel-close", "npc-panel-body", "npc-panel-section", "npc-panel-section-label",
    "npc-panel-link", "npc-panel-link-icon", "npc-panel-link-text", "npc-panel-link-sub",
    "npc-panel-link-arrow", "npc-panel-divider", "npc-panel-cta", "npc-panel-phone",
    "npc-state-link", "npc-state-link-pulse",  # states grid in panel
    # save-contact widget at the very bottom of the page (line ~3789+)
    "npc-save-wrap", "npc-save-btn", "npc-save-card", "npc-save-card-close",
    "npc-save-card-profile", "npc-save-card-avatar", "npc-save-card-name",
    "npc-save-card-title", "npc-save-card-msg", "npc-save-card-dl", "npc-save-card-hint",
    "npc-save-dot", "npc-save-hidden", "npc-save-visible", "npc-save-card-open",
    # footer
    "site-footer", "footer-grid", "footer-brand", "footer-links", "footer-contact",
    "footer-bottom", "footer-site", "footer-logo-img",
    # mobile sticky CTA (lives outside .home-v2)
    "mobile-sticky-cta",
    # btn-primary -> referenced by mobile-sticky-cta anchor (line ~3587)
    "btn-primary",
}

HARD_KEEP_IDS = {
    "npcHamburger", "npcSlidePanel", "npcOverlay", "npcPanelClose",
    "npcSaveWrap", "npcSaveBtn", "npcSaveCard", "npcSaveDismiss", "npcSaveDownload",
    "mobileCta", "main", "skip-link",
}

# Tokens that v1 styles but the rendered DOM uses INSIDE .home-v2 -> shadowed -> DELETE
# These are derived from selector patterns we already know are dead in v2.
SHADOWED_BY_V2 = {
    # base markup tokens that are rebuilt inside .home-v2 with !important resets
    "hero", "steps", "step", "stars",
    # other v1-only classes that have no markup outside .home-v2 (computed below)
}

# Common tokens that exist purely as v1 layout helpers and have no v2 analog in markup.
# Listed here so we don't keep marking them INVESTIGATE.
LIKELY_DEAD_HINTS = {
    "hero-photo-wrap", "hero-bottom", "hero-pills", "hero-pill", "hero-overlay",
    "hero-trust", "hero-actions", "hero-sub", "hero-badge",
    "compare-grid", "compare-vs", "compare-column",
    "about-grid", "testimonials-grid",
    "pain-grid", "conditions-grid", "condition-card",
    "pricing-card", "pricing-amount",
    "proof-bar", "proof-bar-inner",
    "reviews-banner", "review-card",
    "faq-item", "faq-question", "faq-chevron", "faq-answer",
    "section-header",
    "btn-secondary", "btn-ghost", "btn-inverted",
    "reveal", "stagger", "visible",
}


def classify(rule: Rule, regions: dict[str, Region]) -> tuple[str, str]:
    sel = rule.selector
    toks = selector_tokens(sel)
    classes = toks["classes"]
    ids     = toks["ids"]

    notes: list[str] = []

    # 1) :root, base resets, the @media at the top, and a few keyframes -> KEEP
    if sel.startswith("@font-face") or sel.startswith("@import") or sel.startswith("@charset"):
        return ("KEEP", "at-rule (font/import/charset)")
    if sel.startswith("@keyframes"):
        return ("KEEP", "keyframes (cheap; may animate v2)")
    if sel.startswith("@supports"):
        return ("KEEP", "@supports wrapper")
    if sel == ":root" or sel.startswith(":root"):
        return ("KEEP", ":root custom properties used by v2")

    # Bare HTML element resets (body, html, *, h1, h2, p, a, img, etc.)
    bare_html = re.fullmatch(
        r"\*|html|body|main|section|article|aside|nav|header|footer|"
        r"h[1-6]|p|a|img|button|input|textarea|select|label|ul|ol|li|"
        r"figure|figcaption|table|thead|tbody|tr|td|th|small|strong|em",
        sel.strip(),
    )
    if bare_html:
        return ("KEEP", "base element reset (used by all markup)")

    # The top-of-file reduced-motion @media targeting * and .reveal -> KEEP (covers v2 too)
    if sel.startswith("@media (prefers-reduced-motion"):
        return ("KEEP", "prefers-reduced-motion @media (covers entire page)")

    # Skip-link rule
    if "skip-link" in classes or "skip-link" in ids:
        return ("KEEP", "accessibility skip-link is rendered outside .home-v2")

    # Focus / scrollbar / selection rules
    if any(x in sel for x in [":focus-visible", "::-webkit-scrollbar", "::selection"]):
        return ("KEEP", "page-wide focus/scrollbar/selection styles")

    # 2) Hard-keep production systems
    keep_class_hits = HARD_KEEP_TOKENS & classes
    keep_id_hits    = HARD_KEEP_IDS    & ids
    if keep_class_hits or keep_id_hits:
        # BUT: if the selector also contains a class that's known-dead AND that
        # known-dead class appears as an ANCESTOR/parent in the selector (not as
        # part of a compound like `.btn-primary.hero-actions`), the rule can't
        # fire because the ancestor doesn't exist in markup. Mark DELETE.
        dead_ancestors = (LIKELY_DEAD_HINTS - HARD_KEEP_TOKENS) & classes
        if dead_ancestors:
            # Confirm: does any of the dead ancestors actually appear in markup
            # anywhere on the page?
            real_outside = []
            for c in dead_ancestors:
                if re.search(rf'class="(?:[^"]*\s)?{re.escape(c)}(?:\s[^"]*)?"', regions["outside_v2"].text):
                    real_outside.append(c)
            if not real_outside:
                return ("DELETE",
                        f"selector references {sorted(keep_class_hits | {('#' + i) for i in keep_id_hits})} "
                        f"but is gated by dead ancestor(s) {sorted(dead_ancestors)} with no markup")
        bits = []
        if keep_class_hits: bits.append("classes=" + ",".join(sorted(keep_class_hits)))
        if keep_id_hits:    bits.append("ids=" + ",".join(sorted(keep_id_hits)))
        return ("KEEP", "production system: " + "; ".join(bits))

    # 3) Selector targets a class explicitly nuked by v2 !important resets
    overridden = V2_OVERRIDDEN & classes
    if overridden:
        # Confirm there's no use OUTSIDE .home-v2
        outside_hits = []
        for c in classes:
            if re.search(rf'class="(?:[^"]*\s)?{re.escape(c)}(?:\s[^"]*)?"', regions["outside_v2"].text):
                outside_hits.append(c)
        if not outside_hits:
            return ("DELETE",
                    f"v1 styling shadowed by v2 !important reset (classes={sorted(overridden)}); "
                    f"no markup outside .home-v2")
        else:
            return ("INVESTIGATE",
                    f"classes {sorted(overridden)} shadowed in v2 BUT also appear outside .home-v2: {sorted(set(outside_hits))}")

    # 4) Generic verdict via markup search
    # For each class token, check: does the class appear in markup INSIDE .home-v2 only,
    # or also OUTSIDE? Same for ids.
    inside_hits  = set()
    outside_hits = set()
    js_hits      = set()

    for c in classes:
        cls_pat = rf'class="(?:[^"]*\s)?{re.escape(c)}(?:\s[^"]*)?"'
        if re.search(cls_pat, regions["inside_v2"].text):
            inside_hits.add(c)
        if re.search(cls_pat, regions["outside_v2"].text):
            outside_hits.add(c)
        # JS hooks: querySelector('.c'), classList.add('c'), classList.toggle('c'), .closest('.c')
        if re.search(rf"['\"`]\.{re.escape(c)}\b", regions["js"].text) or \
           re.search(rf"classList\.(add|remove|toggle|contains)\(\s*['\"`]{re.escape(c)}['\"`]", regions["js"].text):
            js_hits.add(c)

    for i_ in ids:
        if re.search(rf'id="{re.escape(i_)}"', regions["inside_v2"].text):
            inside_hits.add("#" + i_)
        if re.search(rf'id="{re.escape(i_)}"', regions["outside_v2"].text):
            outside_hits.add("#" + i_)
        if re.search(rf"getElementById\(\s*['\"`]{re.escape(i_)}['\"`]", regions["js"].text) or \
           re.search(rf"['\"`]#{re.escape(i_)}\b", regions["js"].text):
            js_hits.add("#" + i_)

    # If selector references no classes and no ids (pure tag combinators), treat as investigate
    if not classes and not ids:
        return ("KEEP", "tag-only selector — base styling, retain")

    if outside_hits:
        return ("KEEP",
                f"referenced in markup outside .home-v2: {sorted(outside_hits)}"
                + (f"; js: {sorted(js_hits)}" if js_hits else ""))

    if js_hits and not inside_hits and not outside_hits:
        # JS hooks a class that has NO markup anywhere = both CSS and JS are dead.
        return ("DELETE",
                f"JS targets {sorted(js_hits)} but class has zero markup anywhere -> JS+CSS both dead")

    if inside_hits and not outside_hits:
        # Inside .home-v2 only. v2 has its own scoped rules at .home-v2 .x{...}.
        # The plain v1 rule .x{...} still applies (cascade), but anything v2 redeclares
        # via .home-v2 .x{...} wins on specificity. v1 contributions usually orphan.
        return ("DELETE",
                f"only used inside .home-v2 (markup classes={sorted(inside_hits)}); "
                f"v2 has scoped .home-v2 selectors that win on specificity")

    # No markup hits anywhere. If JS also doesn't touch it -> DELETE.
    if not inside_hits and not outside_hits and not js_hits:
        # Hint at known-dead categories
        dead_match = LIKELY_DEAD_HINTS & classes
        if dead_match:
            return ("DELETE",
                    f"no markup or JS reference; v1-only legacy class {sorted(dead_match)}")
        return ("DELETE", "no markup or JS reference anywhere in file")

    # Fallback: investigate
    return ("INVESTIGATE",
            f"ambiguous: inside={sorted(inside_hits)} outside={sorted(outside_hits)} js={sorted(js_hits)}")


# ----------------------------------------------------------------------
# Step 5: Special-case override for the transparent-nav-over-hero rules
# ----------------------------------------------------------------------

def post_classify_transparent_nav(rule: Rule, verdict: str, evidence: str, b: dict) -> tuple[str, str]:
    """The .npc-nav transparent-over-hero rules at lines ~850-867 are a special case.
       v2 reset at lines ~2651-2657 forces .npc-nav to white !important. Those v2 rules
       are NOT scoped under .home-v2 in their selector text, so they apply globally.
       JS at line ~3712 toggles .scrolled based on heroBottom — but the v2 force-white
       reset would override the transparent variant anyway. Mark these as INVESTIGATE
       so a human can confirm the gradient hero is dead."""
    sel = rule.selector
    if (".npc-nav:not(.scrolled)" in sel or
        (sel.strip() == ".npc-nav.scrolled" and 850 <= rule.line_start <= 870) or
        (sel.strip() == ".npc-nav" and 850 <= rule.line_start <= 870)):
        return ("INVESTIGATE",
                "transparent-over-hero rule (lines ~850-867); v1 blue gradient hero is dead, "
                "v2 reset at ~2651-2657 forces .npc-nav to white !important. Likely safe to delete "
                "alongside the JS .scrolled toggle, but verify the v2 reset truly wins.")
    return (verdict, evidence)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    lines = load_lines()
    b = find_boundaries(lines)
    regions = build_regions(lines, b)

    rules = extract_rules(lines, b["v1_style"][0], b["v1_style"][1])

    # Write TSV
    rows = []
    rows.append("selector\tline_range\tverdict\tevidence\tbytes\tinside_media")
    totals = {"KEEP": 0, "DELETE": 0, "INVESTIGATE": 0, "TOTAL": 0}
    bytes_by = {"KEEP": 0, "DELETE": 0, "INVESTIGATE": 0, "TOTAL": 0}

    for r in rules:
        verdict, evidence = classify(r, regions)
        verdict, evidence = post_classify_transparent_nav(r, verdict, evidence, b)
        totals[verdict] += 1
        totals["TOTAL"] += 1
        bytes_by[verdict] += r.block_bytes
        bytes_by["TOTAL"] += r.block_bytes
        sel_safe = r.selector.replace("\t", " ").replace("\n", " ")
        ev_safe  = evidence.replace("\t", " ").replace("\n", " ")
        media    = (r.inside_media or "").replace("\t", " ")
        rows.append(f"{sel_safe}\t{r.line_start}-{r.line_end}\t{verdict}\t{ev_safe}\t{r.block_bytes}\t{media}")

    with open(TSV_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")

    # Print summary to stdout
    print(f"Boundaries:")
    print(f"  v1 <style>: lines {b['v1_style'][0]}-{b['v1_style'][1]}")
    print(f"  v2 <style>: lines {b['v2_style'][0]}-{b['v2_style'][1]}")
    print(f"  .home-v2 wrapper: lines {b['home_v2'][0]}-{b['home_v2'][1]}")
    print(f"\nTotal v1 selectors: {totals['TOTAL']}")
    print(f"  KEEP: {totals['KEEP']}  ({bytes_by['KEEP']} bytes)")
    print(f"  DELETE: {totals['DELETE']}  ({bytes_by['DELETE']} bytes)")
    print(f"  INVESTIGATE: {totals['INVESTIGATE']}  ({bytes_by['INVESTIGATE']} bytes)")
    print(f"  Total v1 bytes: {bytes_by['TOTAL']}")
    print(f"\nManifest written to: {TSV_OUT}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
