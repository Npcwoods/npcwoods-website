"""Shared guardrails for NPCWoods website deploy scripts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


LIVE_DEPLOY_CONFIRMATION = "CHRIS APPROVED LIVE DEPLOY"


@dataclass(frozen=True)
class DeployPlanItem:
    local: Path
    remote: str | None
    skipped_reason: str | None = None


def require_live_deploy_confirmation(execute: bool, confirmation: str | None) -> None:
    if not execute:
        return
    if confirmation != LIVE_DEPLOY_CONFIRMATION:
        raise RuntimeError(
            "Live deploy blocked. Re-run with "
            f'--confirm-live-deploy "{LIVE_DEPLOY_CONFIRMATION}" after Chris explicitly approves.'
        )


def summarize_plan(items: list[DeployPlanItem]) -> str:
    lines = ["Deploy plan:"]
    for item in items:
        if item.remote is None:
            lines.append(f"  [skip] {item.local} ({item.skipped_reason or 'not deployable'})")
        else:
            lines.append(f"  [up] {item.local} -> {item.remote}")
    return "\n".join(lines)
