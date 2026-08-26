#!/usr/bin/env python3
"""Validate first-class localized entry documentation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

README_FILES = [
    "README.md",
    "README.ko.md",
    "README.ja.md",
    "README.zh-CN.md",
]

QUICKSTART_FILES = [
    "QUICKSTART.md",
    "QUICKSTART.ko.md",
    "QUICKSTART.ja.md",
    "QUICKSTART.zh-CN.md",
]

LANGUAGE_LINKS = [
    "README.md",
    "README.ko.md",
    "README.ja.md",
    "README.zh-CN.md",
]

QUICKSTART_LINKS = [
    "QUICKSTART.md",
    "QUICKSTART.ko.md",
    "QUICKSTART.ja.md",
    "QUICKSTART.zh-CN.md",
]

README_MARKERS = [
    "Research Preview",
    "Resource Graph",
    "Bound Capability",
    "Runtime Kernel",
    "Skill Lift",
    "Context Lift",
    "Paperthin",
    "CONTRIBUTING.md",
    "validation-reports/README.md",
]

QUICKSTART_MARKERS = [
    "harness setup",
    "harness demo",
    "harness validate",
    "harness scenario",
    "harness doctor",
    "harness.cmd",
    "source: live",
]


def check_files(files: list[str], markers: list[str], links: list[str]) -> list[str]:
    failures: list[str] = []
    for rel in files:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"missing localized entry document: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(f"{rel}: missing parity marker '{marker}'")
        for link in links:
            if link == rel:
                continue
            if link not in text:
                failures.append(f"{rel}: missing language navigation link '{link}'")
    return failures


def main() -> int:
    failures: list[str] = []
    failures.extend(check_files(README_FILES, README_MARKERS, LANGUAGE_LINKS))
    failures.extend(check_files(QUICKSTART_FILES, QUICKSTART_MARKERS, QUICKSTART_LINKS))

    policy = ROOT / "docs" / "LOCALIZATION.md"
    if not policy.exists():
        failures.append("missing localization policy: docs/LOCALIZATION.md")
    else:
        text = policy.read_text(encoding="utf-8")
        for rel in README_FILES + QUICKSTART_FILES:
            if rel not in text:
                failures.append(f"docs/LOCALIZATION.md: missing supported file '{rel}'")

    if failures:
        print("LOCALIZATION CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("LOCALIZATION CONTRACT PASSED")
    print("Supported entry languages: English, Korean, Japanese, Simplified Chinese")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
