#!/usr/bin/env python3
"""Emergency restore: revert every page where today's footer-synced.bak exists.

Caused by a too-greedy regex in sync-footer-snippet.py (v1) that consumed
page-level <style> blocks. Restores the .footer-synced.bak content and removes
the bad backup so a future correct sync can run.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "html", ROOT / "landing-pages"]

restored = 0
for root in SCAN_DIRS:
    for bak in root.rglob("index.html.footer-synced.bak"):
        target = bak.with_name("index.html")
        target.write_text(bak.read_text(encoding="utf-8"), encoding="utf-8")
        bak.unlink()
        restored += 1
        print(f"[restore] {target.relative_to(ROOT)}")
print(f"\nRestored {restored} pages.")
