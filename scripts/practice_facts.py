#!/usr/bin/env python3
"""Load the practice facts ledger and compare the named surfaces to it.

The ledger is the locked roster. This script reports drift. It does not edit
pages, skills, or spare website copies.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_ledger(path: Path) -> dict:
    ledger = json.loads(path.read_text(encoding="utf-8"))
    served = ledger["states_served"]
    licenses = ledger["aprn_licenses"]
    if "FL" not in served:
        raise ValueError("states_served must include FL")
    if licenses != [state for state in served if state != "FL"]:
        raise ValueError("aprn_licenses must be states_served without FL")
    if ledger["acute_care_credential"]["status"] != "open":
        raise ValueError("acute_care_credential stays open until Chris picks one")
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
