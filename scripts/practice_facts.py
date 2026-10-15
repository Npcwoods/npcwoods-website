#!/usr/bin/env python3
"""Load the practice facts ledger and compare the named surfaces to it.

The ledger is the locked roster. This script reports drift. It does not edit
pages, skills, or spare website copies.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


def load_ledger(path: Path) -> dict:
    ledger = json.loads(path.read_text(encoding="utf-8"))
    served = ledger["states_served"]
    licenses = ledger["aprn_licenses"]
    if "FL" not in served:
        raise ValueError("states_served must include FL")
    if licenses != [state for state in served if state != "FL"]:
        raise ValueError("aprn_licenses must be states_served without FL")
    acute = ledger["acute_care_credential"]
    if acute.get("status") != "settled" or acute.get("value") != "AGACNP-BC":
        raise ValueError("acute_care_credential must be settled as AGACNP-BC (Chris, 2026-10-15)")
    return ledger


def surface_mismatches(root: Path, ledger: dict) -> list[str]:
    problems: list[str] = []
    must_contain = ledger["surface_must_contain"]
    must_not_contain = ledger["surface_must_not_contain"]
    for rel in ledger["surfaces"]:
        path = root / rel
        if not path.is_file():
            problems.append(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in must_contain:
            if needle not in text:
                problems.append(f"{rel}: missing {needle!r}")
        for needle in must_not_contain:
            if needle in text:
                problems.append(f"{rel}: contains {needle!r}")
    return problems


# --------------------------------------------------------------------------
# Page-level checks used by scripts/deploy.py before anything is uploaded.
# --------------------------------------------------------------------------

# Words Chris bans on the site. MD is case-sensitive so "md" in code never trips it.
BANNED_WORDS_ANY_CASE = ("appointment", "physician", "doctor", "insurance")
BANNED_WORDS_EXACT_CASE = ("MD",)

_BANNED_ANY_CASE_RX = re.compile(
    r"\b(?:" + "|".join(BANNED_WORDS_ANY_CASE) + r")s?\b", re.IGNORECASE)
_BANNED_EXACT_CASE_RX = re.compile(r"\b(?:" + "|".join(BANNED_WORDS_EXACT_CASE) + r")\b")

# Things that are not page words: comments, CSS, URL-ish attribute values, URLs,
# data URIs, and URL slugs such as /doctor-visit/ or /uti-treatment/mesa-az/.
_NOT_PAGE_TEXT = (
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"<style\b.*?</style>", re.S | re.I),
    re.compile(r"""\b(?:href|src|srcset|action|poster|data-src|data-href|class|id|for|name|xlink:href)"""
               r"""\s*=\s*(?:"[^"]*"|'[^']*')""", re.I),
    re.compile(r"""(?:https?:)?//[^\s"'<>)\]]+""", re.I),
    re.compile(r"""data:[^\s"'<>)]+""", re.I),
    re.compile(r"""(?<![\w.])/[A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-.%]*)+"""),
)


def page_words(html: str, allowed_phrases: list[str] | tuple[str, ...] = ()) -> str:
    """Return the text banned words are checked against (URLs and slugs removed)."""
    text = html
    for rx in _NOT_PAGE_TEXT:
        text = rx.sub(" ", text)
    for phrase in allowed_phrases:
        if phrase:
            # whole phrase only: "American Family Physician" does not swallow "...Physicians"
            text = re.sub(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", " ", text, flags=re.IGNORECASE)
    return text


def banned_word_hits(html: str, allowed_phrases: list[str] | tuple[str, ...] = ()) -> list[str]:
    """Banned words found in page text, each with a little context."""
    text = page_words(html, allowed_phrases)
    hits = []
    for rx in (_BANNED_ANY_CASE_RX, _BANNED_EXACT_CASE_RX):
        for m in rx.finditer(text):
            ctx = " ".join(text[max(0, m.start() - 40): m.end() + 30].split())
            hits.append(f"{m.group(0)!r} in “…{ctx}…”")
    return hits


def page_drift(rel: str, html: str, ledger: dict) -> list[str]:
    """Facts drift for one page about to be uploaded. rel is repo-relative."""
    problems = []
    lower = html.lower()
    for needle in ledger.get("page_must_not_contain", ledger.get("surface_must_not_contain", [])):
        if needle.lower() in lower:
            problems.append(f"contains {needle!r} (facts ledger)")
    for pattern in ledger.get("page_must_not_match_regex", []):
        m = re.search(pattern, html)
        if m:
            problems.append(f"matches {pattern!r} at “{html[max(0, m.start() - 30):m.end() + 10]}” (facts ledger)")
    if rel in ledger.get("surfaces", []):
        for needle in ledger.get("surface_must_contain", []):
            if needle not in html:
                problems.append(f"missing {needle!r} (facts ledger surface)")
    return problems
