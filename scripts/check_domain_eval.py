#!/usr/bin/env python3
"""Check a structured agent output against a cross-domain golden scenario.

Usage:
  python scripts/check_domain_eval.py SUITE.json SCENARIO_ID OUTPUT.json

Output contract:
  {"classification": str, "checks": [str], "recommendations": [str]}
"""
from __future__ import annotations
import json
import sys
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: check_domain_eval.py SUITE.json SCENARIO_ID OUTPUT.json", file=sys.stderr)
        return 2
    suite = load(sys.argv[1])
    scenario_id = sys.argv[2]
    output = load(sys.argv[3])
    scenario = next((x for x in suite["scenarios"] if x["id"] == scenario_id), None)
    if scenario is None:
        print(f"unknown scenario: {scenario_id}", file=sys.stderr)
        return 2
    expected = scenario["expected"]
    failures: list[str] = []
    if output.get("classification") != expected["classification"]:
        failures.append(f"classification expected {expected['classification']!r}, got {output.get('classification')!r}")
    checks = set(output.get("checks", []))
    for item in expected.get("required_checks", []):
        if item not in checks:
            failures.append(f"missing required check: {item}")
    recommendations = set(output.get("recommendations", []))
    for item in expected.get("required_recommendations", []):
        if item not in recommendations:
            failures.append(f"missing required recommendation: {item}")
    for item in expected.get("must_not_recommend", []):
        if item in recommendations:
            failures.append(f"prohibited recommendation present: {item}")
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
