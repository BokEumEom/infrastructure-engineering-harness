#!/usr/bin/env python3
"""Check one agent output against a provider-neutral golden incident scenario.

Usage:
  python scripts/check_eval_output.py SUITE.json SCENARIO_ID OUTPUT.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: check_eval_output.py SUITE.json SCENARIO_ID OUTPUT.json", file=sys.stderr)
        return 2

    suite = load(sys.argv[1])
    scenario_id = sys.argv[2]
    output = load(sys.argv[3])
    scenario = next((s for s in suite["scenarios"] if s["id"] == scenario_id), None)
    if scenario is None:
        print(f"unknown scenario: {scenario_id}", file=sys.stderr)
        return 2

    expected = scenario["expected"]
    failures: list[str] = []
    if output.get("primary_hypothesis") != expected["primary_hypothesis"]:
        failures.append(f"primary_hypothesis expected {expected['primary_hypothesis']!r}, got {output.get('primary_hypothesis')!r}")

    checks = set(output.get("checks", []))
    missing = [x for x in expected.get("required_checks", []) if x not in checks]
    if missing:
        failures.append("missing required checks: " + ", ".join(missing))

    recommendations = set(output.get("recommendations", []))
    prohibited = [x for x in expected.get("must_not_recommend", []) if x in recommendations]
    if prohibited:
        failures.append("prohibited recommendations: " + ", ".join(prohibited))

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
