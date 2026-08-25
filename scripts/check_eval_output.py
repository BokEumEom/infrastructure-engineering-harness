#!/usr/bin/env python3
"""Minimal evaluator for infrastructure-agent JSON output.

Usage:
    python scripts/check_eval_output.py EVAL.json OUTPUT.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_eval_output.py EVAL.json OUTPUT.json", file=sys.stderr)
        return 2

    fixture = load(sys.argv[1])
    output = load(sys.argv[2])
    expected = fixture["expected"]

    failures: list[str] = []

    if output.get("primary_hypothesis") != expected["primary_hypothesis"]:
        failures.append(
            f"primary_hypothesis: expected {expected['primary_hypothesis']!r}, "
            f"got {output.get('primary_hypothesis')!r}"
        )

    checks = set(output.get("checks", []))
    missing = [item for item in expected.get("required_checks", []) if item not in checks]
    if missing:
        failures.append(f"missing required checks: {', '.join(missing)}")

    recommendations = set(output.get("recommendations", []))
    prohibited = [
        item for item in expected.get("must_not_recommend", []) if item in recommendations
    ]
    if prohibited:
        failures.append(f"prohibited recommendations present: {', '.join(prohibited)}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
