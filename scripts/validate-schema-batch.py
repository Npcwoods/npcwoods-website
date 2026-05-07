#!/usr/bin/env python3
"""Validate schema.org / JSON-LD blocks on a batch of live URLs.

Fetches each URL, extracts every <script type="application/ld+json"> block,
parses the JSON, and runs rule-based checks for the 7 known bug classes
identified in the 2026-04-22 schema-fix plan, plus generic sanity checks.

Output: JSON report with per-URL errors + aggregate counts.

Usage:
    python3 scripts/validate-schema-batch.py [--in URLS.tsv] [--out REPORT.json]

TSV columns: url, template
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TSV = REPO_ROOT / "scripts" / "schema-validate-urls-2026-04-22.tsv"
DEFAULT_OUT = Path("/Users/chriswoods/Desktop/Chris-HQ/npcwoods-business/reports/schema-validate-2026-04-22-pre.json")

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

JSON_LD_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def fetch(url: str) -> str:
    cache_bust = int(time.time())
    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}v={cache_bust}"
    r = requests.get(
        full,
        headers={"User-Agent": UA, "Accept": "text/html", "Cache-Control": "no-cache"},
        timeout=30,
        allow_redirects=True,
    )
    r.raise_for_status()
    return r.text


def extract_ld_blocks(html: str) -> list[tuple[int, str]]:
    return [(i, m.group(1).strip()) for i, m in enumerate(JSON_LD_RE.finditer(html))]


def iter_nodes(obj):
    """Yield every dict node inside the JSON-LD tree."""
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from iter_nodes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_nodes(v)


def type_is(node, *types) -> bool:
    t = node.get("@type")
    if isinstance(t, list):
        return any(x in t for x in types)
    return t in types


def check_block(parsed, block_index, url) -> list[dict]:
    """Run rule-based checks. Returns list of error dicts."""
    errors: list[dict] = []

    # Generic: must have @context and @type or @graph
    nodes_with_graph_or_root = list(iter_nodes(parsed))
    root_ok = (
        isinstance(parsed, dict) and (
            "@context" in parsed or "@graph" in parsed or "@type" in parsed
        )
    )
    if not root_ok:
        errors.append({"bug": "sanity", "severity": "ERROR", "detail": "root lacks @context/@graph/@type"})

    persons = []
    med_businesses = []
    med_therapies = []

    for node in nodes_with_graph_or_root:
        # Bug 1: Person or Physician using "credential" instead of "hasCredential"
        if type_is(node, "Person", "Physician") and "credential" in node:
            errors.append({
                "bug": "bug1_credential",
                "severity": "ERROR",
                "detail": f"Person has 'credential' (should be 'hasCredential'): {node.get('credential')!r}",
                "node_id": node.get("@id"),
            })

        # Bug 2: MedicalBusiness/MedicalOrganization with "Family Practice" (should be FamilyPractice enum)
        if type_is(node, "MedicalBusiness", "MedicalOrganization", "Physician"):
            spec = node.get("medicalSpecialty")
            if isinstance(spec, str) and spec == "Family Practice":
                errors.append({
                    "bug": "bug2_medicalSpecialty",
                    "severity": "ERROR",
                    "detail": "medicalSpecialty='Family Practice' (schema.org enum is 'FamilyPractice')",
                    "node_id": node.get("@id"),
                })

        # Bug 3: jobTitle copy (report as WARNING — per WL-004 both forms valid)
        if type_is(node, "Person", "Physician"):
            jt = node.get("jobTitle", "")
            if isinstance(jt, str) and "Double Board-Certified" in jt:
                errors.append({
                    "bug": "bug3_jobTitle_copy",
                    "severity": "WARNING",
                    "detail": f"jobTitle uses 'Double Board-Certified' form: {jt!r}",
                    "node_id": node.get("@id"),
                })
            persons.append(node)

        # Bug 4: MedicalTherapy missing required-ish props
        if type_is(node, "MedicalTherapy", "TherapeuticProcedure", "MedicalProcedure"):
            missing = [p for p in ("relevantSpecialty", "code") if p not in node]
            if missing:
                errors.append({
                    "bug": "bug4_medtherapy_missing",
                    "severity": "WARNING",
                    "detail": f"MedicalTherapy missing recommended props: {missing}",
                    "node_id": node.get("@id"),
                })
            med_therapies.append(node)

        # Bug 6: Person.worksFor inline MedicalBusiness duplication
        if type_is(node, "Person", "Physician"):
            wf = node.get("worksFor")
            if isinstance(wf, dict) and wf.get("@type") in ("MedicalBusiness", "MedicalOrganization", "Organization"):
                if not (len(wf) == 1 and "@id" in wf):
                    # Inline object with more than just an @id reference
                    errors.append({
                        "bug": "bug6_worksfor_inline",
                        "severity": "ERROR",
                        "detail": "Person.worksFor is inline MedicalBusiness object (should be {'@id': ...} reference to main org node)",
                        "node_id": node.get("@id"),
                    })

        if type_is(node, "MedicalBusiness", "MedicalOrganization"):
            med_businesses.append(node)

    # Bug 7: Inconsistent Person variants across blocks
    person_job_titles = {p.get("jobTitle") for p in persons if p.get("jobTitle")}
    person_ids = {p.get("@id") for p in persons}
    if len(person_job_titles) > 1:
        errors.append({
            "bug": "bug7_person_inconsistent",
            "severity": "ERROR",
            "detail": f"Multiple Person jobTitle variants on same page: {sorted(person_job_titles)}",
        })
    # Missing @id is bug7-adjacent because it breaks cross-source de-duplication
    for p in persons:
        if "@id" not in p:
            errors.append({
                "bug": "bug7_person_missing_id",
                "severity": "WARNING",
                "detail": "Person node missing @id (prevents cross-source de-dup)",
            })

    return errors


def validate_url(url: str, template: str) -> dict:
    result = {
        "url": url,
        "template": template,
        "ok": True,
        "blocks": 0,
        "errors": [],
    }
    try:
        html = fetch(url)
    except Exception as e:
        result["ok"] = False
        result["errors"].append({"bug": "fetch", "severity": "ERROR", "detail": str(e)})
        return result

    blocks = extract_ld_blocks(html)
    result["blocks"] = len(blocks)
    if not blocks:
        result["errors"].append({"bug": "no_jsonld", "severity": "ERROR", "detail": "no JSON-LD blocks found on page"})
        result["ok"] = False
        return result

    for i, raw in blocks:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as e:
            result["errors"].append({
                "bug": "parse",
                "severity": "ERROR",
                "block_index": i,
                "detail": f"JSON parse error: {e}",
            })
            continue

        errs = check_block(parsed, i, url)
        for e in errs:
            e["block_index"] = i
            # Snapshot which @type the block is emitting for aggregation
            if isinstance(parsed, dict):
                if "@graph" in parsed:
                    types = [n.get("@type") for n in parsed["@graph"] if isinstance(n, dict)]
                    e["block_types"] = [str(t) for t in types if t]
                else:
                    e["block_types"] = [str(parsed.get("@type", ""))]
            result["errors"].append(e)

    result["ok"] = all(e["severity"] != "ERROR" for e in result["errors"])
    return result


def aggregate(results: list[dict]) -> dict:
    bug_counts: dict[str, int] = {}
    sev_counts = {"ERROR": 0, "WARNING": 0}
    total_blocks = 0
    urls_with_errors = 0
    for r in results:
        total_blocks += r["blocks"]
        if not r["ok"]:
            urls_with_errors += 1
        for e in r["errors"]:
            bug_counts[e["bug"]] = bug_counts.get(e["bug"], 0) + 1
            sev_counts[e.get("severity", "ERROR")] = sev_counts.get(e.get("severity", "ERROR"), 0) + 1
    return {
        "total_urls": len(results),
        "urls_with_errors": urls_with_errors,
        "total_blocks_validated": total_blocks,
        "by_severity": sev_counts,
        "by_bug": bug_counts,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="tsv", type=Path, default=DEFAULT_TSV)
    ap.add_argument("--out", dest="out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--sleep", type=float, default=2.0, help="seconds between URLs")
    args = ap.parse_args()

    if not args.tsv.exists():
        print(f"[fatal] tsv not found: {args.tsv}", file=sys.stderr)
        return 2

    rows = []
    for line in args.tsv.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2 or parts[0].lower() == "url":
            continue
        rows.append({"url": parts[0].strip(), "template": parts[1].strip()})

    print(f"Validating {len(rows)} URL(s)...")
    results = []
    for i, row in enumerate(rows):
        print(f"  [{i + 1}/{len(rows)}] {row['template']:22s} {row['url']}")
        r = validate_url(row["url"], row["template"])
        err_errors = sum(1 for e in r["errors"] if e.get("severity") == "ERROR")
        err_warns = sum(1 for e in r["errors"] if e.get("severity") == "WARNING")
        status = "OK" if r["ok"] else "FAIL"
        print(f"      -> {status} | blocks={r['blocks']} ERROR={err_errors} WARN={err_warns}")
        results.append(r)
        if i < len(rows) - 1:
            time.sleep(args.sleep)

    agg = aggregate(results)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "tsv": str(args.tsv),
        "summary": agg,
        "results": results,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print()
    print(f"Wrote: {args.out}")
    print(f"Summary: {json.dumps(agg, indent=2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
