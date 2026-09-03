#!/usr/bin/env python3
"""Check contributor-facing community and validation entry points."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "agent",
    "agent.cmd",
    "harness",
    "harness.cmd",
    "README.ko.md",
    "README.ja.md",
    "README.zh-CN.md",
    "QUICKSTART.md",
    "QUICKSTART.ko.md",
    "QUICKSTART.ja.md",
    "QUICKSTART.zh-CN.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/scenario.yml",
    ".github/ISSUE_TEMPLATE/validation.yml",
    ".github/ISSUE_TEMPLATE/adapter.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "validation-reports/README.md",
    "validation-reports/example.fixture.json",
    "contrib/scenarios/README.md",
    "docs/COMMUNITY-VALIDATION.md",
    "docs/RELEASE-STATUS.md",
    "docs/LOCALIZATION.md",
]

ISSUE_FORMS = [
    ".github/ISSUE_TEMPLATE/scenario.yml",
    ".github/ISSUE_TEMPLATE/validation.yml",
    ".github/ISSUE_TEMPLATE/adapter.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
]


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"missing community file: {rel}")

    for launcher in ("agent", "harness"):
        launcher_path = ROOT / launcher
        if launcher_path.exists() and not (launcher_path.stat().st_mode & 0o111):
            failures.append(f"{launcher}: macOS/Linux launcher must be executable")

    for rel in ISSUE_FORMS:
        path = ROOT / rel
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for key in ("name", "description", "body"):
            if not data.get(key):
                failures.append(f"{rel}: missing required Issue Form field '{key}'")
        if "about" in data:
            failures.append(f"{rel}: use Issue Form 'description', not legacy 'about'")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "QUICKSTART.md",
        "CONTRIBUTING.md",
        "validation-reports/README.md",
        "Research Preview",
        "README.ko.md",
        "README.ja.md",
        "README.zh-CN.md",
    ):
        if marker not in readme:
            failures.append(f"README.md: missing contributor/localization marker '{marker}'")

    quickstart = (ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    for marker in ("./agent setup", "./agent demo", "./agent validate", "agent.cmd demo"):
        if marker not in quickstart:
            failures.append(f"QUICKSTART.md: missing Agent CLI marker '{marker}'")
    if "python scripts/" in quickstart or "python -m unittest" in quickstart:
        failures.append("QUICKSTART.md: user-facing path must use the Agent CLI, not lower-level Python commands")

    report_path = ROOT / "validation-reports/example.fixture.json"
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("source") == "fixture":
            claims = report.get("claims", {})
            for claim in ("agent_effectiveness", "skill_lift", "context_lift"):
                if claims.get(claim) is not False:
                    failures.append(f"fixture validation report must not claim {claim}")

    if failures:
        print("COMMUNITY CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("COMMUNITY CONTRACT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
