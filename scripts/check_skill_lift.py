#!/usr/bin/env python3
"""Apply repository Skill Lift policy to a normalized report."""
from __future__ import annotations
import json, sys
from pathlib import Path
import yaml

def main():
    if len(sys.argv)!=3:
        print("usage: check_skill_lift.py POLICY.yaml REPORT.json",file=sys.stderr); return 2
    policy=yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    report=json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")); s=report["summary"]; failures=[]
    if s["case_count"] < policy["minimum_cases"]: failures.append(f"case_count {s['case_count']} < {policy['minimum_cases']}")
    missing=set(policy.get("required_case_kinds",[]))-set(s["case_kinds"])
    if missing: failures.append("missing case kinds: "+", ".join(sorted(missing)))
    if s["mean_composite_lift"] < policy["minimum_mean_composite_lift"]: failures.append(f"mean_composite_lift {s['mean_composite_lift']:.4f} < {policy['minimum_mean_composite_lift']:.4f}")
    if s["mean_outcome_lift"] < policy["minimum_mean_outcome_lift"]: failures.append(f"mean_outcome_lift {s['mean_outcome_lift']:.4f} < {policy['minimum_mean_outcome_lift']:.4f}")
    if s["negative_case_rate"] > policy["maximum_negative_case_rate"]: failures.append(f"negative_case_rate {s['negative_case_rate']:.4f} > {policy['maximum_negative_case_rate']:.4f}")
    if policy.get("fail_on_security_regression",True) and s["security_regressions"]>0: failures.append(f"security regressions: {s['security_regressions']}")
    if failures:
        print("SKILL LIFT GATE FAILED")
        for f in failures: print(f"- {f}")
        return 1
    kind="LIVE" if report["source"]=="live" else "FIXTURE"
    print(f"SKILL LIFT GATE PASSED ({kind}) composite={s['mean_composite_lift']:+.4f} outcome={s['mean_outcome_lift']:+.4f}")
    if report["source"]!="live": print("NOTE: fixture validation proves scoring/gating plumbing only; it does not verify real Skill Lift.")
    return 0
if __name__=="__main__": raise SystemExit(main())
