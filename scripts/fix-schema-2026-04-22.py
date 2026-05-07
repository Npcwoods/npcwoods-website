#!/usr/bin/env python3
"""Idempotent batch fixer for schema.org JSON-LD bugs across static HTML.

Applies the 7-bug fix set identified in the 2026-04-22 plan:
  bug1_credential      Person.credential -> Person.hasCredential (nested object)
  bug2_medicalSpecialty "Family Practice" / "Family Medicine" -> "FamilyPractice"
  bug3_jobTitle        "Double Board-Certified ..." -> "Licensed Nurse Practitioner"
  bug4_medtherapy      MedicalTherapy add relevantSpecialty + code (when condition known)
  bug6_worksfor        Person.worksFor inline MedicalBusiness -> @id reference
  bug7_person_id       Person missing @id -> add "https://npcwoods.com/#chris-woods"
                       (only when name/jobTitle unambiguously identify Chris Woods)

Idempotency: on first touch of each file, creates <file>.schema-bak-20260422.
Always reads from the backup and writes to the target. Re-running produces
identical output.

Usage:
    python3 scripts/fix-schema-2026-04-22.py [--dry-run] [--only bug1,bug2] [--root landing-pages]
"""

import argparse
import copy
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BAK_SUFFIX = ".schema-bak-20260422"

ROOTS = [
    "landing-pages",
    "html",
    "blog",
    "homepage",
]

JSON_LD_BLOCK_RE = re.compile(
    r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)

ORG_ID = "https://npcwoods.com/#medical-business"
PERSON_ID = "https://npcwoods.com/#chris-woods"
CRED_NAME_CHRIS = "MSN, APRN, FNP-C"

# ICD-10 codes per condition hub (used for bug4 MedicalTherapy enrichment).
# Keyed by URL-path fragment; value is (icd10_code, procedure_name_hint).
CONDITION_ICD10 = {
    "uti-treatment": ("N39.0", "Urinary tract infection"),
    "sinus-infection-treatment": ("J01.90", "Acute sinusitis"),
    "strep-throat": ("J02.0", "Streptococcal pharyngitis"),
    "dental-pain": ("K04.7", "Periapical abscess"),
    "tooth-infection": ("K04.7", "Periapical abscess"),
    "ear-infection": ("H66.90", "Otitis media"),
    "bronchitis": ("J20.9", "Acute bronchitis"),
    "pink-eye": ("H10.9", "Conjunctivitis"),
    "skin-infection": ("L08.9", "Skin infection"),
    "ingrown-toenail": ("L60.0", "Ingrown nail"),
    "allergic-reaction": ("T78.40XA", "Allergy, unspecified"),
    "yeast-infection": ("B37.3", "Candidiasis of vulva and vagina"),
    "cold-sores": ("B00.1", "Herpes simplex (oral)"),
    "stomach-bug": ("A09", "Infectious gastroenteritis"),
    "covid-flu": ("J11.1", "Influenza with respiratory manifestations"),
    "ed-treatment": ("N52.9", "Erectile dysfunction, unspecified"),
}


def is_person(node: dict) -> bool:
    t = node.get("@type")
    return t == "Person" or (isinstance(t, list) and "Person" in t)


def is_business(node: dict) -> bool:
    t = node.get("@type")
    targets = ("MedicalBusiness", "MedicalOrganization", "Organization")
    return t in targets or (isinstance(t, list) and any(x in t for x in targets))


def is_therapy(node: dict) -> bool:
    t = node.get("@type")
    targets = ("MedicalTherapy", "TherapeuticProcedure", "MedicalProcedure")
    return t in targets or (isinstance(t, list) and any(x in t for x in targets))


def looks_like_chris(node: dict) -> bool:
    """Heuristic: Person node that clearly identifies Chris Woods."""
    name = (node.get("name") or "").lower()
    jt = (node.get("jobTitle") or "").lower()
    desc = (node.get("description") or "").lower()
    if "chris woods" in name:
        return True
    if "nurse practitioner" in jt and ("chris" in desc or "npcwoods" in desc):
        return True
    return False


class Transformer:
    def __init__(self, enabled_bugs: set[str], file_path: Path):
        self.enabled = enabled_bugs
        self.path = file_path
        self.counts: dict[str, int] = {}

    def tick(self, bug: str) -> None:
        self.counts[bug] = self.counts.get(bug, 0) + 1

    # --- per-node transforms -------------------------------------------------

    def fix_bug1(self, node: dict) -> None:
        """credential -> hasCredential nested object."""
        if "bug1" not in self.enabled:
            return
        if not is_person(node):
            return
        if "credential" not in node:
            return
        cred_value = node.pop("credential")
        existing = node.get("hasCredential")
        new_entry = {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "license",
            "name": cred_value if isinstance(cred_value, str) else CRED_NAME_CHRIS,
        }
        if existing is None:
            node["hasCredential"] = new_entry
        elif isinstance(existing, list):
            # Avoid dup if same name already in list
            names = {e.get("name") for e in existing if isinstance(e, dict)}
            if new_entry["name"] not in names:
                existing.append(new_entry)
        elif isinstance(existing, dict):
            # Keep both: promote to list
            names = {existing.get("name")}
            if new_entry["name"] not in names:
                node["hasCredential"] = [existing, new_entry]
        self.tick("bug1")

    def fix_bug2(self, node: dict) -> None:
        """'Family Practice' / 'Family Medicine' -> 'FamilyPractice' enum."""
        if "bug2" not in self.enabled:
            return
        spec = node.get("medicalSpecialty")
        if not isinstance(spec, str):
            return
        if spec in ("Family Practice", "Family Medicine"):
            node["medicalSpecialty"] = "FamilyPractice"
            self.tick("bug2")

    def fix_bug3(self, node: dict) -> None:
        """Person jobTitle 'Double Board-Certified ...' -> 'Licensed Nurse Practitioner'."""
        if "bug3" not in self.enabled:
            return
        if not is_person(node):
            return
        jt = node.get("jobTitle")
        if not isinstance(jt, str):
            return
        if "double board-certified" in jt.lower() or "Double Board-Certified" in jt:
            node["jobTitle"] = "Licensed Nurse Practitioner"
            self.tick("bug3")

    def fix_bug6(self, node: dict) -> None:
        """Person.worksFor inline MedicalBusiness -> {'@id': ORG_ID} reference."""
        if "bug6" not in self.enabled:
            return
        if not is_person(node):
            return
        wf = node.get("worksFor")
        if not isinstance(wf, dict):
            return
        t = wf.get("@type")
        if t not in ("MedicalBusiness", "MedicalOrganization", "Organization"):
            return
        if len(wf) == 1 and "@id" in wf:
            return  # already a reference
        # Preserve whatever @id the inline object had (falls back to ORG_ID)
        inner_id = wf.get("@id") or ORG_ID
        node["worksFor"] = {"@id": inner_id}
        self.tick("bug6")

    def fix_bug7(self, node: dict) -> None:
        """Person missing @id but clearly identifying Chris -> add PERSON_ID."""
        if "bug7" not in self.enabled:
            return
        if not is_person(node):
            return
        if "@id" in node:
            return
        if looks_like_chris(node):
            node["@id"] = PERSON_ID
            self.tick("bug7")

    def fix_bug4(self, node: dict) -> None:
        """MedicalTherapy: add relevantSpecialty + code if missing and file path hints condition."""
        if "bug4" not in self.enabled:
            return
        if not is_therapy(node):
            return
        path_str = str(self.path)
        code_tuple = None
        for slug, tup in CONDITION_ICD10.items():
            if f"/{slug}/" in path_str:
                code_tuple = tup
                break
        if not code_tuple:
            return
        icd10, hint = code_tuple
        changed = False
        if "relevantSpecialty" not in node:
            node["relevantSpecialty"] = {"@id": ORG_ID}
            changed = True
        if "code" not in node:
            node["code"] = {
                "@type": "MedicalCode",
                "codingSystem": "ICD-10",
                "code": icd10,
                "name": hint,
            }
            changed = True
        if changed:
            self.tick("bug4")

    # --- tree walker ---------------------------------------------------------

    def walk(self, obj):
        if isinstance(obj, dict):
            self.fix_bug1(obj)
            self.fix_bug2(obj)
            self.fix_bug3(obj)
            self.fix_bug6(obj)
            self.fix_bug7(obj)
            self.fix_bug4(obj)
            for v in list(obj.values()):
                self.walk(v)
        elif isinstance(obj, list):
            for v in obj:
                self.walk(v)


def transform_block(json_text: str, enabled: set[str], path: Path) -> tuple[str, dict]:
    """Transform one JSON-LD block. Returns (new_text, counts)."""
    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError:
        return json_text, {"parse_error": 1}

    tr = Transformer(enabled, path)
    tr.walk(parsed)

    if not tr.counts:
        return json_text, {}

    # Preserve a reasonable indent. The originals are typically 2-space.
    out = json.dumps(parsed, indent=2, ensure_ascii=False)
    return out, tr.counts


def process_file(path: Path, enabled: set[str], dry_run: bool) -> dict:
    """Apply transforms to one file using the idempotent backup pattern."""
    bak = path.with_suffix(path.suffix + BAK_SUFFIX)
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    original = bak.read_text(encoding="utf-8")

    file_counts: dict[str, int] = {}
    blocks_touched = 0

    def replace(m: re.Match) -> str:
        nonlocal blocks_touched
        opening, body, closing = m.group(1), m.group(2), m.group(3)
        # Preserve leading whitespace and newlines inside the script tag
        stripped = body.strip()
        if not stripped:
            return m.group(0)
        new_body, counts = transform_block(stripped, enabled, path)
        if counts and "parse_error" not in counts:
            for k, v in counts.items():
                file_counts[k] = file_counts.get(k, 0) + v
            blocks_touched += 1
            # Keep a single blank line padding like originals commonly have
            return f"{opening}\n{new_body}\n{closing}"
        if counts.get("parse_error"):
            file_counts["parse_error"] = file_counts.get("parse_error", 0) + 1
        return m.group(0)

    updated = JSON_LD_BLOCK_RE.sub(replace, original)

    if not file_counts:
        return {"status": "nochange", "counts": {}, "blocks": 0}

    if updated == original:
        return {"status": "nochange", "counts": file_counts, "blocks": blocks_touched}

    if dry_run:
        return {"status": "would-write", "counts": file_counts, "blocks": blocks_touched}

    path.write_text(updated, encoding="utf-8")
    return {"status": "written", "counts": file_counts, "blocks": blocks_touched}


def collect_targets(roots: list[str]) -> list[Path]:
    """All .html/.php files under the given roots (relative to repo)."""
    exclude_parts = {"_archive", "backups", "automation-output", "__pycache__"}
    results: list[Path] = []
    for root_name in roots:
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        for ext in ("*.html", "*.php"):
            for f in root.rglob(ext):
                if any(part in exclude_parts for part in f.parts):
                    continue
                if f.name.endswith(BAK_SUFFIX):
                    continue
                if BAK_SUFFIX in f.name:
                    continue
                results.append(f)
    return results


# --- inline tests -----------------------------------------------------------


def run_self_tests() -> None:
    # Bug 1
    n = {"@type": "Person", "name": "C", "credential": "MSN"}
    Transformer({"bug1"}, Path("/tmp/x")).walk(n)
    assert "credential" not in n
    assert n["hasCredential"]["name"] == "MSN", n

    # Bug 2
    n = {"@type": "MedicalBusiness", "medicalSpecialty": "Family Practice"}
    Transformer({"bug2"}, Path("/tmp/x")).walk(n)
    assert n["medicalSpecialty"] == "FamilyPractice"

    n = {"@type": "MedicalBusiness", "medicalSpecialty": "Family Medicine"}
    Transformer({"bug2"}, Path("/tmp/x")).walk(n)
    assert n["medicalSpecialty"] == "FamilyPractice"

    # Bug 3
    n = {"@type": "Person", "jobTitle": "Double Board-Certified Family Nurse Practitioner"}
    Transformer({"bug3"}, Path("/tmp/x")).walk(n)
    assert n["jobTitle"] == "Licensed Nurse Practitioner"

    # Bug 6
    n = {"@type": "Person", "worksFor": {"@type": "MedicalBusiness", "name": "x", "url": "y"}}
    Transformer({"bug6"}, Path("/tmp/x")).walk(n)
    assert n["worksFor"] == {"@id": ORG_ID}, n

    # Bug 7
    n = {"@type": "Person", "name": "Chris Woods"}
    Transformer({"bug7"}, Path("/tmp/x")).walk(n)
    assert n["@id"] == PERSON_ID

    # Bug 4
    n = {"@type": "MedicalTherapy"}
    Transformer({"bug4"}, Path("/repo/landing-pages/uti-treatment/index.html")).walk(n)
    assert "code" in n and n["code"]["code"] == "N39.0"

    # Combined walk
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "MedicalBusiness", "medicalSpecialty": "Family Practice"},
            {
                "@type": "Person",
                "name": "Chris Woods",
                "credential": "MSN",
                "jobTitle": "Double Board-Certified Family Nurse Practitioner",
                "worksFor": {"@type": "MedicalBusiness", "name": "NPCWoods"},
            },
        ],
    }
    tr = Transformer({"bug1", "bug2", "bug3", "bug6", "bug7"}, Path("/tmp"))
    tr.walk(graph)
    person = graph["@graph"][1]
    assert person["@id"] == PERSON_ID
    assert person["jobTitle"] == "Licensed Nurse Practitioner"
    assert person["hasCredential"]["name"] == "MSN"
    assert person["worksFor"] == {"@id": ORG_ID}
    print("self-tests: OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--only",
        default="bug1,bug2,bug3,bug4,bug6,bug7",
        help="Comma-separated bug keys to apply",
    )
    ap.add_argument("--root", action="append", help="Limit to these roots (repeatable)")
    ap.add_argument("--test", action="store_true", help="Run self-tests and exit")
    args = ap.parse_args()

    if args.test:
        run_self_tests()
        return 0

    # Always run self-tests before a real run
    run_self_tests()

    enabled = {b.strip() for b in args.only.split(",") if b.strip()}
    roots = args.root or ROOTS

    targets = collect_targets(roots)
    print(f"Targets: {len(targets)} file(s) under {roots}")
    print(f"Enabled bugs: {sorted(enabled)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}\n")

    total_counts: dict[str, int] = {}
    written = 0
    nochange = 0
    parse_errors: list[str] = []
    modified_paths: list[str] = []

    for t in targets:
        rel = t.relative_to(REPO_ROOT).as_posix()
        try:
            res = process_file(t, enabled, args.dry_run)
        except Exception as e:
            print(f"[ERR]  {rel} :: {e}")
            continue

        counts = res.get("counts", {})
        for k, v in counts.items():
            total_counts[k] = total_counts.get(k, 0) + v
        if "parse_error" in counts:
            parse_errors.append(rel)

        status = res["status"]
        if status == "written":
            written += 1
            modified_paths.append(rel)
            summary = ", ".join(f"{k}:{v}" for k, v in sorted(counts.items()) if k != "parse_error")
            print(f"[WR]   {rel}  ({res['blocks']} block(s); {summary})")
        elif status == "would-write":
            written += 1
            modified_paths.append(rel)
            summary = ", ".join(f"{k}:{v}" for k, v in sorted(counts.items()) if k != "parse_error")
            print(f"[DRY]  {rel}  ({res['blocks']} block(s); {summary})")
        else:
            nochange += 1

    print()
    print(f"Changed:  {written}")
    print(f"No-op:    {nochange}")
    print(f"Parse errors: {len(parse_errors)}")
    if parse_errors:
        for p in parse_errors[:10]:
            print(f"   - {p}")
        if len(parse_errors) > 10:
            print(f"   ... and {len(parse_errors) - 10} more")
    print()
    print("Bug counts:")
    for k, v in sorted(total_counts.items()):
        print(f"  {k:22s} {v}")

    # Emit modified-files.txt (only when writing, not dry-run)
    if not args.dry_run and modified_paths:
        out = REPO_ROOT / "scripts" / "modified-files.txt"
        out.write_text("\n".join(modified_paths) + "\n", encoding="utf-8")
        print(f"\nWrote: {out.relative_to(REPO_ROOT)} ({len(modified_paths)} paths)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
