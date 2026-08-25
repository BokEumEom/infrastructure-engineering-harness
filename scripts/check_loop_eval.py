#!/usr/bin/env python3
"""Validate one loop execution result against a golden loop scenario."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: check_loop_eval.py SUITE.json SCENARIO_ID RESULT.json", file=sys.stderr)
        return 2
    suite = load(sys.argv[1]); scenario_id = sys.argv[2]; result = load(sys.argv[3])
    scenario = next((item for item in suite["scenarios"] if item["id"] == scenario_id), None)
    if scenario is None:
        print(f"unknown scenario: {scenario_id}", file=sys.stderr); return 2
    expected = scenario["expected"]; failures = []
    if result.get("loop_id") != scenario["loop_id"]: failures.append(f"loop_id expected {scenario['loop_id']!r}, got {result.get('loop_id')!r}")
    if result.get("terminal_status") != expected["terminal_status"]: failures.append(f"terminal_status expected {expected['terminal_status']!r}, got {result.get('terminal_status')!r}")
    iterations = result.get("iterations")
    if not isinstance(iterations, int) or iterations > expected["max_iterations"]: failures.append(f"iterations must be <= {expected['max_iterations']}, got {iterations!r}")
    events = set(result.get("events", []))
    missing = [x for x in expected["required_events"] if x not in events]
    if missing: failures.append("missing required events: " + ", ".join(missing))
    prohibited = [x for x in expected["must_not_events"] if x in events]
    if prohibited: failures.append("prohibited events present: " + ", ".join(prohibited))
    writeback = {item.get("type") for item in result.get("writeback", [])}
    missing_wb = [x for x in expected["required_writeback"] if x not in writeback]
    if missing_wb: failures.append("missing writeback: " + ", ".join(missing_wb))
    regression = {item.get("id"): item.get("status") for item in result.get("regression_results", [])}
    failed_reg = [x for x in expected["regression_obligations"] if regression.get(x) != "passed"]
    if failed_reg: failures.append("regression obligations not passed: " + ", ".join(failed_reg))
    if failures:
        print("FAIL")
        for failure in failures: print(f"- {failure}")
        return 1
    print("PASS"); return 0


if __name__ == "__main__": raise SystemExit(main())
