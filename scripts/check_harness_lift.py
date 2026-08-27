#!/usr/bin/env python3
"""Apply Harness Lift gates and flag richer context that hobbles the model."""
from __future__ import annotations
import json
import sys
from pathlib import Path
import yaml

def main() -> int:
    if len(sys.argv) not in (3,4):
        print("usage: check_harness_lift.py POLICY.yaml REPORT.json [--require-live]", file=sys.stderr)
        return 2
    policy=yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    report=json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    s=report["summary"]
    failures=[]
    if s["case_count"] < policy["minimum_cases"]:
        failures.append("insufficient cases")
    missing=sorted(set(policy["required_case_kinds"])-set(s["case_kinds"]))
    if missing: failures.append("missing case kinds: "+", ".join(missing))
    if s["mean_minimal_vs_bare_outcome"] < policy["minimum_minimal_vs_bare_outcome_lift"]:
        failures.append("minimal Harness underperforms bare outcome")
    if s["mean_full_vs_minimal_outcome"] < -policy["maximum_full_vs_minimal_outcome_regression"]:
        failures.append("full Harness hobbles outcome relative to minimal")
    if s["mean_full_vs_minimal_composite"] < -policy["maximum_full_vs_minimal_composite_regression"]:
        failures.append("full Harness hobbles composite performance relative to minimal")
    if policy["fail_on_safety_regression"] and (s["minimal_safety_regressions_vs_bare"] or s["full_safety_regressions_vs_minimal"]):
        failures.append("safety regression detected")
    if policy["fail_on_evidence_regression"] and s["minimal_evidence_regressions_vs_bare"]:
        failures.append("minimal Harness regresses evidence quality vs bare")
    require_live=len(sys.argv)==4 and sys.argv[3]=="--require-live"
    if require_live and report["source"] != policy["claim_requires_source"]:
        failures.append(f"Harness Lift claim requires source={policy['claim_requires_source']}")
    if failures:
        print("HARNESS LIFT GATE FAILED")
        for failure in failures: print("- "+failure)
        return 1
    print(f"HARNESS LIFT GATE PASSED source={report['source']} minimal_vs_bare={s['mean_minimal_vs_bare_composite']:+.4f} full_vs_minimal={s['mean_full_vs_minimal_composite']:+.4f}")
    return 0

if __name__=="__main__": raise SystemExit(main())
