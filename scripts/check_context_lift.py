#!/usr/bin/env python3
"""Apply Context Lift policy gates to a normalized report."""
from __future__ import annotations
import json, sys
from pathlib import Path
import yaml

def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def main() -> int:
    if len(sys.argv) not in (3,4):
        print("usage: check_context_lift.py POLICY.yaml REPORT.json [--require-live]", file=sys.stderr)
        return 2
    policy=yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))["paired_eval"]
    report=load_json(sys.argv[2]); summary=report["summary"]
    require_live=len(sys.argv)==4 and sys.argv[3]=="--require-live"
    failures=[]
    if summary["case_count"] < policy["minimum_cases"]:
        failures.append(f"case_count {summary['case_count']} < {policy['minimum_cases']}")
    missing=sorted(set(policy["required_case_kinds"])-set(summary["case_kinds"]))
    if missing: failures.append("missing case kinds: "+", ".join(missing))
    if summary["mean_composite_lift"] < policy["minimum_mean_composite_lift"]:
        failures.append("mean composite Context Lift below policy")
    if summary["mean_outcome_lift"] < policy["minimum_mean_outcome_lift"]:
        failures.append("mean outcome Context Lift below policy")
    if summary["negative_case_rate"] > policy["maximum_negative_case_rate"]:
        failures.append("negative case rate exceeds policy")
    if policy["fail_on_safety_regression"] and summary["safety_regressions"]:
        failures.append(f"safety regressions: {summary['safety_regressions']}")
    if policy["fail_on_instruction_regression"] and summary["instruction_regressions"]:
        failures.append(f"instruction regressions: {summary['instruction_regressions']}")
    if require_live and report["source"] != policy["claim_requires_source"]:
        failures.append(f"Context Lift claim requires source={policy['claim_requires_source']}")
    if failures:
        print("CONTEXT LIFT GATE FAILED")
        for failure in failures: print(f"- {failure}")
        return 1
    print(f"CONTEXT LIFT GATE PASSED source={report['source']} composite={summary['mean_composite_lift']:+.4f}")
    return 0

if __name__=="__main__": raise SystemExit(main())
