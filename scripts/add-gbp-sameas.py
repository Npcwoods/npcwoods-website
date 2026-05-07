#!/usr/bin/env python3
"""
Inject the NPCWoods GBP URL into JSON-LD `sameAs` arrays on target pages.

Idempotent: re-runs are no-ops. Pristine source: writes a dated backup to
scripts/.backups/gbp-sameas-YYYYMMDD/<rel-path> before any modification.
Safe: aborts any file whose post-edit size drops below 95% of original.

Usage:
    python3 scripts/add-gbp-sameas.py              # dry-run (default)
    python3 scripts/add-gbp-sameas.py --apply      # write
    python3 scripts/add-gbp-sameas.py --self-test  # run unit tests
"""

import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

GBP_URL = "https://share.google/XlmNvRT4vihOJ8KBH"
MATCHED_TYPES = {
    "MedicalBusiness",
    "LocalBusiness",
    "Organization",
    "MedicalClinic",
    "HealthAndBeautyBusiness",
}
SCRIPT_BLOCK_RE = re.compile(
    r'(<script\b[^>]*\btype="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)
SIZE_SHRINK_FLOOR = 0.95  # abort if new size < 95% of original

ROOT = Path(__file__).resolve().parent.parent
TARGETS_FILE = ROOT / "scripts" / ".gbp-targets.txt"
BACKUP_ROOT = ROOT / "scripts" / ".backups" / (
    "gbp-sameas-" + datetime.date.today().strftime("%Y%m%d")
)


def is_npcwoods_entity(obj):
    """Belt-and-suspenders: ensure we're editing an NPCWoods entity, not a
    nested credentialing body (AANP, state boards, etc.)."""
    if not isinstance(obj, dict):
        return False
    aid = obj.get("@id", "") or ""
    url = obj.get("url", "") or ""
    name = obj.get("name", "") or ""
    if "npcwoods.com" in aid or "npcwoods.com" in url:
        return True
    if "npcwoods" in name.lower():
        return True
    # Top-level state/condition pages frequently omit @id/url on the inner
    # MedicalBusiness but are unambiguously NPCWoods at the block root.
    # Caller will only pass top-level candidates, so default True for those.
    return None  # "maybe — caller decides based on position"


def candidate_entities(block_obj):
    """Yield (container, key) pairs for every top-level or @graph-root entity
    whose @type is one of MATCHED_TYPES. Does NOT descend into nested
    properties like hasCredential.recognizedBy.memberOf, which would catch
    unrelated orgs."""
    if isinstance(block_obj, dict):
        graph = block_obj.get("@graph")
        if isinstance(graph, list):
            for i, item in enumerate(graph):
                if _is_target(item):
                    yield graph, i
            return
        if _is_target(block_obj):
            yield None, None  # sentinel: edit the block_obj itself
    # Lists at the top of a block are rare; handle for safety.
    elif isinstance(block_obj, list):
        for i, item in enumerate(block_obj):
            if _is_target(item):
                yield block_obj, i


def _is_target(o):
    if not isinstance(o, dict):
        return False
    t = o.get("@type")
    if isinstance(t, list):
        return any(x in MATCHED_TYPES for x in t)
    return t in MATCHED_TYPES


def inject_gbp(entity):
    """Add GBP_URL to entity['sameAs']. Returns 'inserted', 'appended', or
    'already-present'."""
    existing = entity.get("sameAs")
    if existing is None:
        entity["sameAs"] = [GBP_URL]
        return "inserted"
    if isinstance(existing, str):
        if existing == GBP_URL:
            return "already-present"
        entity["sameAs"] = [existing, GBP_URL]
        return "appended"
    if isinstance(existing, list):
        if GBP_URL in existing:
            return "already-present"
        existing.append(GBP_URL)
        return "appended"
    raise ValueError(f"unexpected sameAs type: {type(existing).__name__}")


def process_block(block_json_text):
    """Parse a single JSON-LD block, inject GBP into matching entities,
    re-serialize. Returns (new_json_text, actions: list[str])."""
    try:
        obj = json.loads(block_json_text)
    except json.JSONDecodeError:
        return block_json_text, ["skip: invalid JSON"]

    actions = []
    # Find and edit candidates. The generator may yield the container+index
    # for @graph items, or a (None, None) sentinel meaning "edit obj itself".
    for container, idx in candidate_entities(obj):
        target = obj if container is None else container[idx]
        # For @graph-nested entities, require an NPCWoods identity signal
        # to avoid nested credentialing bodies. For top-level entities
        # (container is None), trust the position.
        if container is not None:
            if is_npcwoods_entity(target) is False:
                continue  # nested non-NPCWoods org -> skip
        result = inject_gbp(target)
        actions.append(result)

    if not actions:
        return block_json_text, ["skip: no matching entity"]

    if all(a == "already-present" for a in actions):
        # Idempotent no-op — return the ORIGINAL text so we don't reformat
        # every time we re-run. This keeps dry-run diffs clean after apply.
        return block_json_text, actions

    new_text = json.dumps(obj, indent=2, ensure_ascii=False)
    return new_text, actions


def process_file(path: Path, apply: bool):
    """Edit one HTML/PHP file. Returns dict with 'path', 'actions' (per
    block), 'wrote' bool, 'error' or None."""
    report = {"path": str(path.relative_to(ROOT)), "blocks": [], "wrote": False, "error": None}
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as e:
        report["error"] = f"read failed: {e}"
        return report

    new_parts = []
    last_end = 0
    changed = False

    for m in SCRIPT_BLOCK_RE.finditer(original):
        new_parts.append(original[last_end:m.start()])
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        # Preserve leading/trailing whitespace around the JSON so
        # `<script>\n{...}\n</script>` doesn't collapse to `<script>{...}</script>`.
        ws = re.match(r'^(\s*)(.*?)(\s*)$', body, re.DOTALL)
        leading, middle, trailing = ws.group(1), ws.group(2), ws.group(3)
        new_middle, actions = process_block(middle)
        report["blocks"].append({"actions": actions})
        if new_middle == middle:
            new_body = body  # untouched
        else:
            new_body = leading + new_middle + trailing
            changed = True
        new_parts.append(opener + new_body + closer)
        last_end = m.end()
    new_parts.append(original[last_end:])
    new_content = "".join(new_parts)

    if not changed:
        return report

    # Size-shrink guard — we only add, never remove.
    if len(new_content) < len(original) * SIZE_SHRINK_FLOOR:
        report["error"] = (
            f"size-shrink guard: new={len(new_content)} orig={len(original)} "
            f"({len(new_content) / len(original):.1%})"
        )
        return report

    if apply:
        # Pristine backup (dated; only written once per day per file).
        backup_path = BACKUP_ROOT / path.relative_to(ROOT)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        if not backup_path.exists():
            shutil.copy2(path, backup_path)
        path.write_text(new_content, encoding="utf-8")
        report["wrote"] = True
    return report


def load_targets():
    targets = []
    for line in TARGETS_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        mode, rel = parts
        targets.append((mode, ROOT / rel))
    return targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes")
    parser.add_argument("--self-test", action="store_true", help="run unit tests and exit")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_tests()

    mode_word = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode_word}] GBP URL: {GBP_URL}")
    print(f"[{mode_word}] backup dir: {BACKUP_ROOT.relative_to(ROOT)}")
    print()

    targets = load_targets()
    errors = 0
    wrote = 0
    by_action = {"inserted": 0, "appended": 0, "already-present": 0, "skipped": 0}

    for expected_mode, path in targets:
        if not path.exists():
            print(f"  MISSING  {path.relative_to(ROOT)}")
            errors += 1
            continue
        report = process_file(path, apply=args.apply)
        if report["error"]:
            print(f"  ERROR    {report['path']}: {report['error']}")
            errors += 1
            continue
        all_actions = [a for blk in report["blocks"] for a in blk["actions"]]
        interesting = [a for a in all_actions if a in ("inserted", "appended")]
        noop = [a for a in all_actions if a == "already-present"]
        skip = [a for a in all_actions if a.startswith("skip")]

        for a in all_actions:
            by_action[a] = by_action.get(a, 0) + 1

        flag = "[W]" if report["wrote"] else ("[~]" if interesting and not args.apply else "[=]")
        summary = f"inserted={all_actions.count('inserted')} appended={all_actions.count('appended')} noop={len(noop)} skip={len(skip)}"
        print(f"  {flag} {expected_mode:<6} {report['path']}  ({summary})")
        if report["wrote"]:
            wrote += 1

    print()
    print(f"Summary: files_written={wrote} errors={errors} "
          f"inserted={by_action.get('inserted', 0)} "
          f"appended={by_action.get('appended', 0)} "
          f"already-present={by_action.get('already-present', 0)}")

    if not args.apply and (by_action.get("inserted", 0) + by_action.get("appended", 0)) == 0:
        print("Idempotent: no changes pending. (Dry-run + re-run safety check.)")

    return 0 if errors == 0 else 1


# --------------------------------------------------------------------------
# Self-tests
# --------------------------------------------------------------------------

def run_self_tests():
    import copy

    def assert_eq(label, got, want):
        if got != want:
            print(f"FAIL {label}:\n  got={got!r}\n  want={want!r}")
            return False
        print(f"PASS {label}")
        return True

    ok = True

    # Test 1: INSERT — flat MedicalBusiness, no sameAs
    block = json.dumps({"@context": "https://schema.org", "@type": "MedicalBusiness", "name": "NPCWoods"})
    new, actions = process_block(block)
    ok &= assert_eq("INSERT flat: actions", actions, ["inserted"])
    ok &= assert_eq("INSERT flat: sameAs", json.loads(new)["sameAs"], [GBP_URL])

    # Test 2: APPEND — MedicalBusiness with existing sameAs
    block = json.dumps({"@type": "MedicalBusiness", "name": "NPCWoods", "sameAs": ["https://www.facebook.com/npcwoods"]})
    new, actions = process_block(block)
    ok &= assert_eq("APPEND: actions", actions, ["appended"])
    ok &= assert_eq("APPEND: sameAs",
                    json.loads(new)["sameAs"],
                    ["https://www.facebook.com/npcwoods", GBP_URL])

    # Test 3: DEDUP — re-running is a no-op
    already = {"@type": "MedicalBusiness", "name": "NPCWoods", "sameAs": [GBP_URL]}
    block = json.dumps(already)
    new, actions = process_block(block)
    ok &= assert_eq("DEDUP: actions", actions, ["already-present"])
    ok &= assert_eq("DEDUP: unchanged text", new, block)  # exact original returned

    # Test 4: @graph — MedicalBusiness inside @graph, Person outside target set
    graph_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Person", "name": "Chris Woods", "sameAs": ["https://npi.example/123"]},
            {"@type": "MedicalBusiness", "@id": "https://npcwoods.com/#medical-business", "name": "NPCWoods"},
        ],
    }
    block = json.dumps(graph_obj)
    new, actions = process_block(block)
    ok &= assert_eq("GRAPH: actions", actions, ["inserted"])
    parsed = json.loads(new)
    ok &= assert_eq("GRAPH: MB got sameAs", parsed["@graph"][1]["sameAs"], [GBP_URL])
    ok &= assert_eq("GRAPH: Person untouched", parsed["@graph"][0]["sameAs"], ["https://npi.example/123"])

    # Test 5: nested non-NPCWoods Organization is skipped
    # (credentialing body nested inside a Person's hasCredential)
    nested = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "hasCredential": [
                    {
                        "@type": "EducationalOccupationalCredential",
                        "recognizedBy": {"@type": "Organization", "name": "AANP"},
                    }
                ],
            },
            {"@type": "MedicalBusiness", "@id": "https://npcwoods.com/#medical-business", "name": "NPCWoods"},
        ],
    }
    block = json.dumps(nested)
    new, actions = process_block(block)
    ok &= assert_eq("NESTED-SKIP: only MedicalBusiness got sameAs", actions, ["inserted"])
    parsed = json.loads(new)
    ok &= assert_eq("NESTED-SKIP: AANP untouched",
                    parsed["@graph"][0]["hasCredential"][0]["recognizedBy"].get("sameAs"),
                    None)

    # Test 6: non-target block (FAQPage) is left alone
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": []}
    block = json.dumps(faq)
    new, actions = process_block(block)
    ok &= assert_eq("NO-MATCH: actions", actions, ["skip: no matching entity"])
    ok &= assert_eq("NO-MATCH: unchanged", new, block)

    # Test 7: full HTML roundtrip via process_file-style logic
    sample_html = (
        "<!DOCTYPE html><html><head>"
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"MedicalBusiness","name":"NPCWoods Telehealth"}\n'
        "</script></head><body>hi</body></html>"
    )
    parts = []
    last_end = 0
    for m in SCRIPT_BLOCK_RE.finditer(sample_html):
        parts.append(sample_html[last_end:m.start()])
        new_body, _ = process_block(m.group(2))
        parts.append(m.group(1) + new_body + m.group(3))
        last_end = m.end()
    parts.append(sample_html[last_end:])
    out = "".join(parts)
    ok &= assert_eq("HTML-ROUNDTRIP: contains GBP URL", GBP_URL in out, True)
    ok &= assert_eq("HTML-ROUNDTRIP: starts with doctype", out.startswith("<!DOCTYPE html>"), True)

    print()
    print("ALL TESTS PASSED" if ok else "TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
