#!/usr/bin/env python3
"""Generate an NPCWoods landing page audit report.

The lab is advisory: it never edits landing pages. It scans revenue-oriented
landing pages, adds NPCWoods conversion/compliance checks, imports local
Impeccable findings, and writes a static HTML report plus JSON data.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from dataclasses import asdict, dataclass
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HQ_ROOT = ROOT.parent
LANDING_ROOT = ROOT / "landing-pages"
OUTPUT_ROOT = ROOT / "automation-output" / "landing-page-lab"
IMPECCABLE_CLI = HQ_ROOT / "impeccable" / "bin" / "cli.js"

EXPECTED_SMS_PHONE = "4806394722"
EXCLUDED_DEFAULT_DIRS = {"learn", "medications", "sitemap"}
SCORE_CATEGORIES = ("conversion", "compliance", "visual", "technical")

PENALTY_BY_PRIORITY = {
    0: 24,
    1: 14,
    2: 8,
    3: 3,
}

PRIORITY_LABELS = {
    0: "Critical",
    1: "High",
    2: "Medium",
    3: "Low",
}


@dataclass
class Finding:
    category: str
    priority: int
    title: str
    body: str
    file: str
    line: int | None = None
    snippet: str | None = None
    source: str = "landing-page-lab"
    key: str | None = None


@dataclass
class PageResult:
    path: str
    rel_path: str
    file_url: str
    screenshot: str | None
    scores: dict[str, int]
    total_score: int
    revenue_risk: int
    findings: list[dict]
    top_fixes: list[dict]


def strip_script_style(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<script\b.*?</script>", "", text, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", "", text, flags=re.I | re.S)
    return text


def visible_line(line: str) -> str:
    line = re.sub(r"<script\b.*", "", line, flags=re.I)
    line = re.sub(r"<style\b.*", "", line, flags=re.I)
    line = re.sub(r"<[^>]+>", " ", line)
    return re.sub(r"\s+", " ", line).strip()


def normalize_phone(value: str) -> str:
    return re.sub(r"\D+", "", value)


def line_number_for(text: str, needle_start: int) -> int:
    return text.count("\n", 0, needle_start) + 1


def first_match_line(text: str, pattern: str, flags: int = re.I) -> int | None:
    match = re.search(pattern, text, flags)
    if not match:
        return None
    return line_number_for(text, match.start())


def file_url(path: Path) -> str:
    return path.resolve().as_uri()


def rel_from_root(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def has_glob(value: str) -> bool:
    return any(ch in value for ch in "*?[]")


def should_include_default(path: Path) -> bool:
    try:
        rel = path.relative_to(LANDING_ROOT)
    except ValueError:
        return False

    parts = set(rel.parts[:-1])
    if parts & EXCLUDED_DEFAULT_DIRS:
        return False
    if path.name.startswith("test-"):
        return False
    if path.name != "index.html" and path.parent != LANDING_ROOT:
        return False
    if any(part.startswith(".") for part in rel.parts):
        return False
    return path.suffix == ".html"


def resolve_page_arg(value: str) -> list[Path]:
    candidates: list[Path] = []
    base_value = value.strip()
    if not base_value:
        return candidates

    bases = [ROOT, LANDING_ROOT]
    raw = Path(base_value).expanduser()

    if raw.is_absolute():
        candidate = raw
        if has_glob(str(candidate)):
            candidates.extend(Path("/").glob(str(candidate).lstrip("/")))
        elif candidate.is_dir():
            candidates.append(candidate / "index.html")
        else:
            candidates.append(candidate)
        return candidates

    for base in bases:
        candidate = base / base_value
        if has_glob(base_value):
            candidates.extend(base.glob(base_value))
        elif candidate.is_dir():
            candidates.append(candidate / "index.html")
        else:
            candidates.append(candidate)

    return candidates


def discover_pages(page_args: list[str], limit: int | None) -> list[Path]:
    if page_args:
        pages: list[Path] = []
        for arg in page_args:
            pages.extend(resolve_page_arg(arg))
        pages = [p.resolve() for p in pages if p.exists() and p.suffix == ".html"]
    else:
        pages = [p.resolve() for p in sorted(LANDING_ROOT.rglob("*.html")) if should_include_default(p)]

    deduped: list[Path] = []
    seen: set[Path] = set()
    for page in pages:
        if page not in seen:
            seen.add(page)
            deduped.append(page)

    if limit is not None:
        deduped = deduped[:limit]
    return deduped


def add_finding(
    findings: list[Finding],
    category: str,
    priority: int,
    title: str,
    body: str,
    file: Path,
    *,
    line: int | None = None,
    snippet: str | None = None,
    source: str = "landing-page-lab",
    key: str | None = None,
) -> None:
    findings.append(
        Finding(
            category=category,
            priority=priority,
            title=title,
            body=body,
            file=str(file),
            line=line,
            snippet=snippet,
            source=source,
            key=key,
        )
    )


def scan_forbidden_visible_language(path: Path, html: str, findings: list[Finding]) -> None:
    forbidden = [
        (
            "insurance",
            0,
            "Forbidden ad/compliance term",
            "Visible page copy contains 'insurance'. NPCWoods ad and landing-page guidance says to use '$59 flat fee', 'simple pricing', or similar phrasing instead.",
        ),
        (
            "copay",
            2,
            "Flag-prone billing term",
            "Visible page copy contains 'copay'. Keep billing language focused on '$59 flat fee' and simple pricing unless this is intentionally used in a comparison table.",
        ),
    ]
    inside_invisible_block = False
    for line_no, raw_line in enumerate(html.splitlines(), start=1):
        if re.search(r"<(?:script|style)\b", raw_line, re.I):
            inside_invisible_block = True
        if inside_invisible_block:
            if re.search(r"</(?:script|style)>", raw_line, re.I):
                inside_invisible_block = False
            continue

        visible = visible_line(raw_line)
        if not visible:
            continue
        if re.match(r"^(?:slug|url|path|file):\s", visible, re.I):
            continue
        for term, priority, title, body in forbidden:
            if re.search(rf"\b{re.escape(term)}s?\b", visible, re.I):
                add_finding(
                    findings,
                    "compliance",
                    priority,
                    title,
                    body,
                    path,
                    line=line_no,
                    snippet=visible[:180],
                    key=f"forbidden-{term}",
                )


def scan_claim_safety(path: Path, visible_text: str, html: str, findings: list[Finding]) -> None:
    claim_patterns = [
        (
            r"\bguarantee(?:d|s)?\b",
            0,
            "Guaranteed-results language",
            "Avoid guarantees on medical landing pages. Use conservative language such as 'when clinically appropriate' or 'if appropriate after review.'",
            "guarantee",
        ),
        (
            r"\bcure(?:d|s)?\b",
            1,
            "Cure language",
            "Avoid cure claims. Keep copy focused on evaluation, guidance, and treatment when clinically appropriate.",
            "cure",
        ),
        (
            r"\b(?:will|get)\s+(?:a\s+)?prescription\b|\bprescription\s+guaranteed\b",
            0,
            "Prescription promise",
            "Do not imply a prescription is guaranteed. Say prescriptions are provided only when clinically appropriate.",
            "prescription-promise",
        ),
        (
            r"\bchildren\b|\bkids\b|\bpediatric\b|\bteen(?:s|agers)?\b",
            1,
            "Possible pediatric implication",
            "Condition campaigns are adult-focused. Remove pediatric implications unless the page clearly excludes treatment for minors.",
            "pediatric",
        ),
        (
            r"\bdoctor\b|\bdr\.",
            2,
            "Provider-title drift",
            "Chris should be framed as a licensed NP, provider, or clinician. Avoid medical titles that imply he is not an NP.",
            "doctor-title",
        ),
    ]
    for pattern, priority, title, body, key in claim_patterns:
        line = first_match_line(visible_text, pattern)
        if line is None:
            continue
        html_line = first_match_line(html, pattern)
        snippet = ""
        match = re.search(pattern, visible_text, re.I)
        if match:
            start = max(match.start() - 80, 0)
            end = min(match.end() + 100, len(visible_text))
            snippet = re.sub(r"\s+", " ", visible_text[start:end]).strip()
        add_finding(
            findings,
            "compliance",
            priority,
            title,
            body,
            path,
            line=html_line or line,
            snippet=snippet,
            key=key,
        )


def scan_cta_and_conversion(path: Path, html: str, visible_text: str, findings: list[Finding]) -> None:
    sms_matches = list(re.finditer(r"""href\s*=\s*["']sms:([^"']+)["']""", html, re.I))
    normalized_targets = [normalize_phone(match.group(1)) for match in sms_matches]

    if not sms_matches:
        add_finding(
            findings,
            "conversion",
            1,
            "Missing SMS CTA",
            "No sms: CTA was found. Revenue pages should make texting Chris the primary action.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="missing-sms-cta",
        )
    else:
        wrong_targets = [target for target in normalized_targets if EXPECTED_SMS_PHONE not in target]
        if wrong_targets:
            add_finding(
                findings,
                "conversion",
                1,
                "SMS CTA points to a different number",
                f"Expected sms:{EXPECTED_SMS_PHONE}. Found target(s): {', '.join(sorted(set(wrong_targets)))}.",
                path,
                line=line_number_for(html, sms_matches[0].start()),
                snippet=sms_matches[0].group(0),
                key="wrong-sms-target",
            )
        if len(sms_matches) < 2:
            add_finding(
                findings,
                "conversion",
                2,
                "CTA is not repeated",
                "Only one SMS CTA was found. Repeat the primary text CTA after major decision points and near the final section.",
                path,
                line=line_number_for(html, sms_matches[0].start()),
                key="low-cta-count",
            )

    body_start = re.search(r"<body\b[^>]*>", html, re.I)
    above_fold = html[body_start.end() : body_start.end() + 4000] if body_start else html[:4000]
    if not re.search(r"""href\s*=\s*["']sms:""", above_fold, re.I):
        add_finding(
            findings,
            "conversion",
            2,
            "No above-fold SMS CTA",
            "The first screen should include the main text CTA so the page communicates the action within a few seconds.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="no-above-fold-cta",
        )

    if not re.search(r"\$ ?59\b|59\s*(?:flat|fee)", visible_text, re.I):
        add_finding(
            findings,
            "conversion",
            1,
            "Missing $59 flat-fee clarity",
            "Revenue pages should make the simple $59 flat fee easy to see, especially near CTAs.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="missing-59",
        )

    trust_terms = [
        r"licensed\s+(?:np|nurse practitioner|provider|clinician)",
        r"\bdouble board-certified\b",
        r"\bclinician\b",
        r"\bprovider\b",
    ]
    if not any(re.search(pattern, visible_text, re.I) for pattern in trust_terms):
        add_finding(
            findings,
            "conversion",
            1,
            "Missing clinician trust framing",
            "Add a clear licensed NP/provider trust signal so visitors understand who is reviewing their text.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="missing-clinician-trust",
        )

    if not re.search(r"\b(?:same[- ]day|today|tonight)\b", visible_text, re.I):
        add_finding(
            findings,
            "conversion",
            2,
            "Missing same-day urgency",
            "NPCWoods pages usually convert best when they make the same-day text-first path explicit.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="missing-same-day",
        )

    if not re.search(r"\b(?:text|sms|message)\b", visible_text, re.I):
        add_finding(
            findings,
            "conversion",
            2,
            "Missing text-first positioning",
            "The page should clearly frame the service around texting or messaging, not a generic appointment flow.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="missing-text-first",
        )


def scan_safety_and_basics(path: Path, html: str, visible_text: str, findings: list[Finding]) -> None:
    if not re.search(r"\b(?:red flags?|emergency|ER|urgent care|in-person|seek care|go to)\b", visible_text, re.I):
        add_finding(
            findings,
            "compliance",
            1,
            "Missing red-flag guidance",
            "Condition pages should route red flags to urgent, in-person, or emergency care.",
            path,
            line=first_match_line(html, r"<body\b") or 1,
            key="missing-red-flags",
        )

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    if not title or len(title) < 20:
        add_finding(
            findings,
            "technical",
            2,
            "Weak or missing title tag",
            "Add a specific title tag that names the condition/location and NPCWoods value.",
            path,
            line=first_match_line(html, r"<title\b"),
            snippet=title,
            key="weak-title",
        )

    meta_desc = re.search(
        r"""<meta\s+[^>]*name\s*=\s*["']description["'][^>]*content\s*=\s*["']([^"']+)["']""",
        html,
        re.I | re.S,
    )
    if not meta_desc:
        meta_desc = re.search(
            r"""<meta\s+[^>]*content\s*=\s*["']([^"']+)["'][^>]*name\s*=\s*["']description["'][^>]*>""",
            html,
            re.I | re.S,
        )
    if not meta_desc:
        add_finding(
            findings,
            "technical",
            2,
            "Missing meta description",
            "Add a meta description for search snippets and share previews.",
            path,
            line=first_match_line(html, r"<head\b") or 1,
            key="missing-meta-description",
        )

    h1_count = len(re.findall(r"<h1\b", html, re.I))
    if h1_count != 1:
        add_finding(
            findings,
            "technical",
            2,
            "Unexpected H1 count",
            f"Expected one H1. Found {h1_count}.",
            path,
            line=first_match_line(html, r"<h1\b"),
            key="h1-count",
        )

    if not re.search(r"""rel\s*=\s*["']canonical["']""", html, re.I):
        add_finding(
            findings,
            "technical",
            3,
            "Missing canonical link",
            "Add a canonical URL to reduce duplicate-indexing ambiguity.",
            path,
            line=first_match_line(html, r"<head\b") or 1,
            key="missing-canonical",
        )


def impeccable_priority(item: dict) -> int:
    antipattern = str(item.get("antipattern", ""))
    high = {
        "low-contrast",
        "text-overflow",
        "horizontal-scroll",
        "mobile-overflow",
        "nested-card",
        "layout-shift",
    }
    low = {
        "overused-font",
        "side-tab",
    }
    if antipattern in high:
        return 1
    if antipattern in low:
        return 3
    return 2


def run_impeccable(path: Path) -> tuple[list[Finding], str | None]:
    if not IMPECCABLE_CLI.exists():
        return (
            [
                Finding(
                    category="visual",
                    priority=2,
                    title="Impeccable CLI unavailable",
                    body=f"Expected detector at {IMPECCABLE_CLI}. Visual anti-pattern findings were skipped.",
                    file=str(path),
                    source="impeccable",
                    key="impeccable-missing",
                )
            ],
            None,
        )

    cmd = ["node", str(IMPECCABLE_CLI), "detect", "--fast", "--json", str(path)]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(HQ_ROOT),
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return (
            [
                Finding(
                    category="visual",
                    priority=2,
                    title="Impeccable scan failed",
                    body=f"Visual anti-pattern scan could not run: {exc}",
                    file=str(path),
                    source="impeccable",
                    key="impeccable-error",
                )
            ],
            str(exc),
        )

    raw = extract_json_payload(proc.stdout, proc.stderr)
    if not raw:
        if proc.returncode == 0:
            return ([], None)
        return (
            [
                Finding(
                    category="visual",
                    priority=2,
                    title="Impeccable returned no JSON",
                    body=(proc.stderr or "No detector output was returned.").strip(),
                    file=str(path),
                    source="impeccable",
                    key="impeccable-no-json",
                )
            ],
            proc.stderr.strip() or None,
        )

    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        return (
            [
                Finding(
                    category="visual",
                    priority=2,
                    title="Impeccable JSON parse failed",
                    body=f"Could not parse detector JSON: {exc}",
                    file=str(path),
                    snippet=raw[:240],
                    source="impeccable",
                    key="impeccable-json-error",
                )
            ],
            raw[:500],
        )

    findings: list[Finding] = []
    for item in items:
        findings.append(
            Finding(
                category="visual",
                priority=impeccable_priority(item),
                title=str(item.get("name") or item.get("antipattern") or "Visual anti-pattern"),
                body=str(item.get("description") or "Impeccable flagged this UI pattern for review."),
                file=str(item.get("file") or path),
                line=item.get("line"),
                snippet=item.get("snippet"),
                source="impeccable",
                key=str(item.get("antipattern") or "impeccable"),
            )
        )
    return (findings, None)


def compute_scores(findings: list[Finding]) -> tuple[dict[str, int], int, int]:
    penalties = {category: 0 for category in SCORE_CATEGORIES}
    total_penalty = 0
    for finding in findings:
        penalty = PENALTY_BY_PRIORITY.get(finding.priority, 3)
        category = finding.category if finding.category in penalties else "technical"
        penalties[category] += penalty
        total_penalty += penalty

    scores = {category: max(0, 100 - penalty) for category, penalty in penalties.items()}
    total_score = round(sum(scores.values()) / len(scores))
    revenue_risk = (100 - scores["conversion"]) * 2 + (100 - scores["compliance"]) * 3 + (100 - scores["visual"])
    return scores, total_score, revenue_risk


def chrome_candidates() -> list[str]:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for binary in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(binary)
        if found:
            candidates.append(found)
    return candidates


def capture_screenshot(path: Path, out_dir: Path) -> str | None:
    chrome = next((candidate for candidate in chrome_candidates() if Path(candidate).exists()), None)
    if not chrome:
        return None

    out_path = out_dir / f"{path.stem}-{abs(hash(path.as_posix()))}.png"
    url = file_url(path)
    with tempfile.TemporaryDirectory(prefix="landing-page-lab-chrome-") as profile_dir:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-sandbox",
            "--disable-background-networking",
            "--disable-breakpad",
            "--disable-component-update",
            "--disable-crash-reporter",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-sync",
            "--metrics-recording-only",
            "--disable-default-apps",
            "--mute-audio",
            "--no-first-run",
            f"--user-data-dir={profile_dir}",
            "--window-size=390,1200",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2500",
            f"--screenshot={out_path}",
            url,
        ]
        try:
            subprocess.run(cmd, text=True, capture_output=True, timeout=20, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return None
    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path.name
    return None


def scan_page(path: Path, screenshots_dir: Path, with_screenshots: bool) -> PageResult:
    html = path.read_text(encoding="utf-8", errors="replace")
    content_html = strip_script_style(html)
    visible_text = re.sub(r"<[^>]+>", " ", content_html)
    visible_text = re.sub(r"\s+", " ", visible_text).strip()

    findings: list[Finding] = []
    scan_forbidden_visible_language(path, html, findings)
    scan_claim_safety(path, visible_text, html, findings)
    scan_cta_and_conversion(path, html, visible_text, findings)
    scan_safety_and_basics(path, html, visible_text, findings)

    impeccable_findings, _ = run_impeccable(path)
    findings.extend(impeccable_findings)

    scores, total_score, revenue_risk = compute_scores(findings)
    sorted_findings = sorted(findings, key=lambda item: (item.priority, item.category, item.title))
    top_fixes = sorted_findings[:3]

    screenshot = capture_screenshot(path, screenshots_dir) if with_screenshots else None

    return PageResult(
        path=str(path),
        rel_path=rel_from_root(path),
        file_url=file_url(path),
        screenshot=screenshot,
        scores=scores,
        total_score=total_score,
        revenue_risk=revenue_risk,
        findings=[asdict(finding) for finding in sorted_findings],
        top_fixes=[asdict(finding) for finding in top_fixes],
    )


def score_class(score: int) -> str:
    if score >= 85:
        return "good"
    if score >= 70:
        return "warn"
    return "bad"


def finding_anchor(finding: dict) -> str:
    line = finding.get("line")
    if line:
        return f"{finding.get('file')}:{line}"
    return str(finding.get("file"))


def render_finding(finding: dict) -> str:
    line = finding.get("line")
    snippet = finding.get("snippet")
    source = finding.get("source", "landing-page-lab")
    priority = PRIORITY_LABELS.get(int(finding.get("priority", 3)), "Low")
    file_path = Path(str(finding.get("file", "")))
    if file_path.exists():
        href = file_url(file_path)
    else:
        href = "#"
    line_label = f":{line}" if line else ""
    snippet_html = f"<code>{escape(str(snippet))}</code>" if snippet else ""
    return f"""
      <li class="finding p{finding.get('priority', 3)}">
        <div class="finding-head">
          <span class="pill">{escape(priority)}</span>
          <strong>{escape(str(finding.get('title', 'Finding')))}</strong>
          <span class="source">{escape(str(source))}</span>
        </div>
        <p>{escape(str(finding.get('body', '')))}</p>
        <a class="file-link" href="{escape(href)}">{escape(finding_anchor(finding))}{escape(line_label if False else "")}</a>
        {snippet_html}
      </li>
    """


def render_report(results: list[PageResult], out_dir: Path, generated_at: str) -> str:
    sorted_results = sorted(results, key=lambda item: (-item.revenue_risk, item.total_score, item.rel_path))
    total_pages = len(sorted_results)
    total_findings = sum(len(item.findings) for item in sorted_results)
    critical = sum(1 for item in sorted_results for finding in item.findings if finding["priority"] == 0)
    avg_score = round(sum(item.total_score for item in sorted_results) / total_pages) if total_pages else 0

    rows = []
    cards = []
    for result in sorted_results:
        screenshot_html = ""
        if result.screenshot:
            screenshot_html = f'<img class="shot" src="screenshots/{escape(result.screenshot)}" alt="">'
        else:
            screenshot_html = '<div class="shot missing">No screenshot</div>'

        score_bits = "".join(
            f'<span class="metric {score_class(score)}">{escape(name.title())}: {score}</span>'
            for name, score in result.scores.items()
        )
        top_fix_bits = "".join(render_finding(finding) for finding in result.top_fixes)
        all_findings_bits = "".join(render_finding(finding) for finding in result.findings)
        file_href = escape(result.file_url)

        rows.append(
            f"""
            <tr>
              <td><a href="#{escape(slugify(result.rel_path))}">{escape(result.rel_path)}</a></td>
              <td><span class="score {score_class(result.total_score)}">{result.total_score}</span></td>
              <td>{result.scores['conversion']}</td>
              <td>{result.scores['compliance']}</td>
              <td>{result.scores['visual']}</td>
              <td>{len(result.findings)}</td>
            </tr>
            """
        )

        cards.append(
            f"""
            <section class="page-card" id="{escape(slugify(result.rel_path))}">
              <div class="page-grid">
                <div>
                  <div class="eyebrow">Revenue risk {result.revenue_risk}</div>
                  <h2>{escape(result.rel_path)}</h2>
                  <div class="score-row">
                    <span class="score {score_class(result.total_score)}">{result.total_score}</span>
                    {score_bits}
                  </div>
                  <div class="actions">
                    <a href="{file_href}">Open source page</a>
                    <a href="findings.json">Raw JSON</a>
                  </div>
                  <h3>Top fixes</h3>
                  <ol class="findings top-fixes">{top_fix_bits or '<li>No top fixes. Looking sharp.</li>'}</ol>
                </div>
                <a class="shot-link" href="{file_href}">{screenshot_html}</a>
              </div>
              <details>
                <summary>All findings ({len(result.findings)})</summary>
                <ol class="findings">{all_findings_bits or '<li>No findings.</li>'}</ol>
              </details>
            </section>
            """
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NPCWoods Landing Page Lab</title>
  <style>
    :root {{
      --ink: #18211f;
      --muted: #60716b;
      --paper: #f8faf7;
      --panel: #ffffff;
      --line: #dfe7e2;
      --blue: #2563eb;
      --green: #16815f;
      --amber: #b76b00;
      --red: #c53030;
      --shadow: 0 14px 40px rgba(24, 33, 31, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font: 15px/1.5 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 32px 20px 56px; }}
    header {{ display: flex; justify-content: space-between; gap: 24px; align-items: flex-end; margin-bottom: 24px; }}
    h1 {{ font-size: 38px; line-height: 1.02; margin: 0 0 8px; letter-spacing: 0; }}
    h2 {{ margin: 4px 0 14px; font-size: 24px; line-height: 1.15; letter-spacing: 0; overflow-wrap: anywhere; }}
    h3 {{ margin: 22px 0 10px; font-size: 15px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); }}
    p {{ margin: 0 0 10px; }}
    .subtle {{ color: var(--muted); }}
    .summary {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 20px 0 24px; }}
    .stat, .page-card, .scoreboard {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .stat {{ padding: 16px; }}
    .stat strong {{ display: block; font-size: 28px; line-height: 1; margin-bottom: 6px; }}
    .scoreboard {{ overflow: hidden; margin-bottom: 24px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.07em; }}
    tr:last-child td {{ border-bottom: 0; }}
    .page-card {{ padding: 18px; margin: 18px 0; }}
    .page-grid {{ display: grid; grid-template-columns: minmax(0, 1fr) 260px; gap: 18px; align-items: start; }}
    .eyebrow {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .score-row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
    .score, .metric, .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      border-radius: 999px;
      padding: 4px 10px;
      font-weight: 700;
      background: #eef4f1;
      color: var(--ink);
    }}
    .score {{ min-width: 48px; justify-content: center; font-size: 18px; }}
    .metric {{ font-size: 12px; }}
    .good {{ background: #e8f6ef; color: var(--green); }}
    .warn {{ background: #fff5df; color: var(--amber); }}
    .bad {{ background: #fdecec; color: var(--red); }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 14px 0; }}
    .shot, .shot.missing {{
      width: 100%;
      aspect-ratio: 13 / 20;
      object-fit: cover;
      object-position: top;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #edf2ef;
    }}
    .shot.missing {{ display: grid; place-items: center; color: var(--muted); }}
    .findings {{ padding-left: 0; list-style: none; margin: 0; }}
    .finding {{ border-top: 1px solid var(--line); padding: 12px 0; }}
    .finding:first-child {{ border-top: 0; }}
    .finding-head {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 6px; }}
    .source {{ color: var(--muted); font-size: 12px; }}
    .file-link {{ display: inline-block; margin: 2px 0 6px; font-size: 12px; overflow-wrap: anywhere; }}
    code {{ display: block; max-width: 100%; overflow-x: auto; background: #f3f6f4; border: 1px solid var(--line); padding: 8px; border-radius: 6px; color: #31443d; }}
    details {{ margin-top: 10px; }}
    summary {{ cursor: pointer; color: var(--blue); font-weight: 700; }}
    footer {{ color: var(--muted); margin-top: 28px; }}
    @media (max-width: 760px) {{
      header {{ display: block; }}
      h1 {{ font-size: 30px; }}
      .summary {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .page-grid {{ grid-template-columns: 1fr; }}
      .shot-link {{ max-width: 320px; }}
      .scoreboard {{ overflow-x: auto; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>Landing Page Lab</h1>
        <p class="subtle">NPCWoods revenue-page audit, generated {escape(generated_at)}.</p>
      </div>
      <a href="findings.json">Download raw findings</a>
    </header>

    <section class="summary">
      <div class="stat"><strong>{total_pages}</strong><span>Pages scanned</span></div>
      <div class="stat"><strong>{avg_score}</strong><span>Average score</span></div>
      <div class="stat"><strong>{total_findings}</strong><span>Total findings</span></div>
      <div class="stat"><strong>{critical}</strong><span>Critical issues</span></div>
    </section>

    <section class="scoreboard">
      <table>
        <thead>
          <tr>
            <th>Page</th>
            <th>Total</th>
            <th>Conversion</th>
            <th>Compliance</th>
            <th>Visual</th>
            <th>Findings</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </section>

    {''.join(cards)}

    <footer>
      Advisory report only. No landing page source files were edited.
    </footer>
  </div>
</body>
</html>
"""
    report_path = out_dir / "report.html"
    report_path.write_text(html, encoding="utf-8")
    return report_path.name


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "page"


def extract_json_payload(stdout: str, stderr: str) -> str:
    """Return the JSON emitted by Impeccable, even when it uses stderr.

    The local CLI exits nonzero when it finds anti-patterns, and in that path
    JSON may be written to stderr. Treat both streams as possible data.
    """
    for stream in (stdout, stderr, f"{stdout}\n{stderr}"):
        text = stream.strip()
        if not text:
            continue
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            pass

        for opener, closer in (("[", "]"), ("{", "}")):
            start = text.find(opener)
            end = text.rfind(closer)
            if start == -1 or end == -1 or end <= start:
                continue
            candidate = text[start : end + 1]
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                continue
    return ""


def write_outputs(results: list[PageResult], run_dir: Path, json_only: bool) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "screenshots").mkdir(exist_ok=True)

    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    payload = {
        "generated_at": generated_at,
        "root": str(ROOT),
        "pages_scanned": len(results),
        "results": [asdict(result) for result in sorted(results, key=lambda item: (-item.revenue_risk, item.rel_path))],
    }
    (run_dir / "findings.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if not json_only:
        render_report(results, run_dir, generated_at)
    return run_dir


def update_latest(run_dir: Path) -> Path:
    latest_dir = OUTPUT_ROOT / "latest"
    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    shutil.copytree(run_dir, latest_dir)
    return latest_dir


def open_report(latest_dir: Path, json_only: bool) -> None:
    target = latest_dir / ("findings.json" if json_only else "report.html")
    subprocess.run(["open", str(target)], check=False)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Limit number of pages scanned.")
    parser.add_argument(
        "--page",
        action="append",
        default=[],
        help="Path or glob to audit. May be repeated. Relative paths resolve from repo root and landing-pages/.",
    )
    parser.add_argument("--json-only", action="store_true", help="Write findings.json without report.html.")
    parser.add_argument("--no-screenshots", action="store_true", help="Skip best-effort Chrome screenshots.")
    parser.add_argument("--open", action="store_true", help="Open the latest report after generation.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    pages = discover_pages(args.page, args.limit)
    if not pages:
        print("No landing pages matched the requested scan scope.", file=sys.stderr)
        return 2

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = OUTPUT_ROOT / "runs" / timestamp
    screenshots_dir = run_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print(f"Landing Page Lab: scanning {len(pages)} page(s)")
    results = []
    for index, page in enumerate(pages, start=1):
        print(f"[{index}/{len(pages)}] {rel_from_root(page)}")
        results.append(scan_page(page, screenshots_dir, not args.no_screenshots))

    write_outputs(results, run_dir, args.json_only)
    latest_dir = update_latest(run_dir)

    output_file = latest_dir / ("findings.json" if args.json_only else "report.html")
    print(f"Latest report: {output_file}")
    if args.open:
        open_report(latest_dir, args.json_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
