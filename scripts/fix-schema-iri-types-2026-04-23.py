#!/usr/bin/env python3
"""
Fix two recurring schema.org validator errors on NPCWoods pages:

  1. `medicalSpecialty: "FamilyPractice"` (plain string)
        → `medicalSpecialty: "https://schema.org/FamilyPractice"` (IRI)

  2. `availableService.@type: "MedicalProcedure" | "MedicalTherapy"` (wrong
     type — availableService on MedicalBusiness expects Service, not procedure)
        → `availableService.@type: "Service"`

Same safety discipline as add-gbp-sameas.py:
  - JSON parse / modify / serialize (no raw regex rewriting of structure)
  - Pristine dated backup in scripts/.backups/ before first write
  - Only touches entities that are top-level or @graph-root
  - Size-shrink guard (>95% of original)
  - Idempotent: re-running is a no-op
  - Self-tests

Usage:
    python3 scripts/fix-schema-iri-types-2026-04-23.py              # dry-run
    python3 scripts/fix-schema-iri-types-2026-04-23.py --apply
    python3 scripts/fix-schema-iri-types-2026-04-23.py --self-test
"""

import argparse
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

SPECIALTY_IRI_MAP = {
    "FamilyPractice": "https://schema.org/FamilyPractice",
    # Extendable: add other bare values here if we ever use them.
}
PROCEDURE_TYPES_TO_SERVICE = {"MedicalProcedure", "MedicalTherapy"}
BUSINESS_TYPES = {"MedicalBusiness", "LocalBusiness", "Organization", "MedicalClinic"}

SCRIPT_BLOCK_RE = re.compile(
    r'(<script\b[^>]*\btype="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)
SIZE_SHRINK_FLOOR = 0.95

ROOT = Path(__file__).resolve().parent.parent
TARGETS_FILE = ROOT / "scripts" / ".gbp-targets.txt"  # same 17 files we edited
BACKUP_ROOT = ROOT / "scripts" / ".backups" / (
    "schema-iri-" + datetime.date.today().strftime("%Y%m%d")
)


def is_npcwoods_entity(obj):
    if not isinstance(obj, dict):
        return False
    aid = obj.get("@id", "") or ""
    url = obj.get("url", "") or ""
    name = obj.get("name", "") or ""
    if "npcwoods.com" in aid or "npcwoods.com" in url:
        return True
    if "npcwoods" in name.lower():
        return True
    return None  # "top-level caller decides"


def _is_business(o):
    if not isinstance(o, dict):
        return False
    t = o.get("@type")
    if isinstance(t, list):
        return any(x in BUSINESS_TYPES for x in t)
    return t in BUSINESS_TYPES


def fix_entity(entity):
    """Apply the two fixes. Returns list of action strings."""
    actions = []
    # Fix 1: medicalSpecialty plain-string -> IRI
    ms = entity.get("medicalSpecialty")
    if isinstance(ms, str) and ms in SPECIALTY_IRI_MAP:
        entity["medicalSpecialty"] = SPECIALTY_IRI_MAP[ms]
        actions.append(f"medicalSpecialty:{ms}->IRI")
    elif isinstance(ms, list):
        new = []
        changed = False
        for v in ms:
            if isinstance(v, str) and v in SPECIALTY_IRI_MAP:
                new.append(SPECIALTY_IRI_MAP[v])
                changed = True
            else:
                new.append(v)
        if changed:
            entity["medicalSpecialty"] = new
            actions.append("medicalSpecialty:list->IRI")

    # Fix 2: availableService.@type MedicalProcedure/MedicalTherapy -> Service
    def rewrite_asvc(svc):
        if not isinstance(svc, dict):
            return svc, False
        t = svc.get("@type")
        if isinstance(t, str) and t in PROCEDURE_TYPES_TO_SERVICE:
            svc["@type"] = "Service"
            return svc, True
        if isinstance(t, list):
            new_t = [("Service" if x in PROCEDURE_TYPES_TO_SERVICE else x) for x in t]
            if new_t != t:
                svc["@type"] = new_t
                return svc, True
        return svc, False

    asvc = entity.get("availableService")
    if isinstance(asvc, dict):
        _, changed = rewrite_asvc(asvc)
        if changed:
            actions.append("availableService.@type->Service")
    elif isinstance(asvc, list):
        any_changed = False
        for i, svc in enumerate(asvc):
            _, c = rewrite_asvc(svc)
            any_changed = any_changed or c
        if any_changed:
            actions.append("availableService[].@type->Service")

    return actions


def walk_top_and_graph(block_obj):
    """Yield business entities at the top level of a block or inside @graph."""
    if isinstance(block_obj, dict):
        graph = block_obj.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if _is_business(item):
                    yield item, "graph"
            return
        if _is_business(block_obj):
            yield block_obj, "root"


def process_block(block_json_text):
    try:
        obj = json.loads(block_json_text)
    except json.JSONDecodeError:
        return block_json_text, ["skip: invalid JSON"]

    all_actions = []
    for entity, position in walk_top_and_graph(obj):
        # For @graph entries, require a positive NPCWoods identity signal
        # (npcwoods.com @id/url or "npcwoods" in name). Returning None means
        # "no identity signal at all" — skip to be safe.
        if position == "graph" and is_npcwoods_entity(entity) is not True:
            continue
        actions = fix_entity(entity)
        all_actions.extend(actions)

    if not all_actions:
        return block_json_text, ["skip: nothing to fix"]

    new_text = json.dumps(obj, indent=2, ensure_ascii=False)
    return new_text, all_actions


def process_file(path: Path, apply: bool):
    report = {"path": str(path.relative_to(ROOT)), "blocks": [], "wrote": False, "error": None}
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as e:
        report["error"] = f"read failed: {e}"
        return report

    parts = []
    last_end = 0
    changed = False
    for m in SCRIPT_BLOCK_RE.finditer(original):
        parts.append(original[last_end:m.start()])
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        ws = re.match(r'^(\s*)(.*?)(\s*)$', body, re.DOTALL)
        leading, middle, trailing = ws.group(1), ws.group(2), ws.group(3)
        new_middle, actions = process_block(middle)
        report["blocks"].append({"actions": actions})
        if new_middle == middle:
            parts.append(opener + body + closer)
        else:
            parts.append(opener + leading + new_middle + trailing + closer)
            changed = True
        last_end = m.end()
    parts.append(original[last_end:])
    new_content = "".join(parts)

    if not changed:
        return report

    if len(new_content) < len(original) * SIZE_SHRINK_FLOOR:
        report["error"] = (
            f"size-shrink guard: new={len(new_content)} orig={len(original)} "
            f"({len(new_content) / len(original):.1%})"
        )
        return report

    if apply:
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
        _, rel = parts
        targets.append(ROOT / rel)
    return targets


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return run_self_tests()

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] backup dir: {BACKUP_ROOT.relative_to(ROOT)}")
    print()

    targets = load_targets()
    wrote = errors = 0
    all_actions_count = {}

    for path in targets:
        if not path.exists():
            print(f"  MISSING  {path.relative_to(ROOT)}")
            errors += 1
            continue
        r = process_file(path, apply=args.apply)
        if r["error"]:
            print(f"  ERROR    {r['path']}: {r['error']}")
            errors += 1
            continue
        acts = [a for blk in r["blocks"] for a in blk["actions"]]
        interesting = [a for a in acts if not a.startswith("skip")]
        for a in interesting:
            all_actions_count[a] = all_actions_count.get(a, 0) + 1
        flag = "[W]" if r["wrote"] else ("[~]" if interesting and not args.apply else "[=]")
        summary = ", ".join(sorted(set(interesting))) or "no-op"
        print(f"  {flag} {r['path']:<55} {summary}")
        if r["wrote"]:
            wrote += 1

    print()
    print(f"Summary: files_written={wrote} errors={errors}")
    for a, n in sorted(all_actions_count.items()):
        print(f"  {a}: {n}")
    return 0 if errors == 0 else 1


# --------------------------------------------------------------------------
# Self-tests
# --------------------------------------------------------------------------

def run_self_tests():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            print(f"FAIL {label}\n  got={got!r}\n  want={want!r}")
            ok = False
        else:
            print(f"PASS {label}")

    # Test 1: medicalSpecialty IRI conversion on flat MedicalBusiness
    blk = json.dumps({"@type": "MedicalBusiness", "name": "NPCWoods",
                      "medicalSpecialty": "FamilyPractice",
                      "availableService": {"@type": "MedicalProcedure", "name": "Async visit"}})
    new, actions = process_block(blk)
    parsed = json.loads(new)
    check("T1 medicalSpecialty IRI", parsed["medicalSpecialty"], "https://schema.org/FamilyPractice")
    check("T1 availableService Service", parsed["availableService"]["@type"], "Service")
    check("T1 actions", set(actions), {"medicalSpecialty:FamilyPractice->IRI", "availableService.@type->Service"})

    # Test 2: MedicalTherapy also becomes Service
    blk = json.dumps({"@type": "MedicalBusiness", "name": "NPCWoods",
                      "medicalSpecialty": "FamilyPractice",
                      "availableService": {"@type": "MedicalTherapy", "name": "UTI tx"}})
    new, actions = process_block(blk)
    parsed = json.loads(new)
    check("T2 MedicalTherapy->Service", parsed["availableService"]["@type"], "Service")

    # Test 3: @graph case — MedicalBusiness nested inside graph
    blk = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Person", "name": "Chris", "sameAs": ["https://npi.x"]},
        {"@type": "MedicalBusiness", "@id": "https://npcwoods.com/#mb",
         "name": "NPCWoods", "medicalSpecialty": "FamilyPractice"},
    ]})
    new, actions = process_block(blk)
    parsed = json.loads(new)
    check("T3 graph: MB specialty fixed",
          parsed["@graph"][1]["medicalSpecialty"], "https://schema.org/FamilyPractice")
    check("T3 graph: Person untouched",
          parsed["@graph"][0].get("medicalSpecialty"), None)

    # Test 4: nested non-NPCWoods Organization is skipped
    blk = json.dumps({"@graph": [
        {"@type": "Organization", "name": "AANP",  # not NPCWoods — skip
         "medicalSpecialty": "FamilyPractice"},
        {"@type": "MedicalBusiness", "@id": "https://npcwoods.com/#mb",
         "name": "NPCWoods", "medicalSpecialty": "FamilyPractice"},
    ]})
    new, actions = process_block(blk)
    parsed = json.loads(new)
    check("T4 AANP untouched",
          parsed["@graph"][0]["medicalSpecialty"], "FamilyPractice")
    check("T4 NPCWoods fixed",
          parsed["@graph"][1]["medicalSpecialty"], "https://schema.org/FamilyPractice")

    # Test 5: idempotency — second run is no-op on already-fixed entity
    blk = json.dumps({"@type": "MedicalBusiness", "name": "NPCWoods",
                      "medicalSpecialty": "https://schema.org/FamilyPractice",
                      "availableService": {"@type": "Service", "name": "Async visit"}})
    new, actions = process_block(blk)
    check("T5 idempotent actions", actions, ["skip: nothing to fix"])
    check("T5 unchanged body", new, blk)

    # Test 6: leaves unrelated dicts alone (FAQPage, BreadcrumbList)
    blk = json.dumps({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Q"}]})
    new, actions = process_block(blk)
    check("T6 FAQPage skip", actions, ["skip: nothing to fix"])

    # Test 7: availableService as a list
    blk = json.dumps({"@type": "MedicalBusiness", "name": "NPCWoods",
                      "availableService": [
                          {"@type": "MedicalProcedure", "name": "A"},
                          {"@type": "Service", "name": "B"},
                      ]})
    new, actions = process_block(blk)
    parsed = json.loads(new)
    check("T7 list: first fixed", parsed["availableService"][0]["@type"], "Service")
    check("T7 list: second unchanged", parsed["availableService"][1]["@type"], "Service")

    print()
    print("ALL TESTS PASSED" if ok else "TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
