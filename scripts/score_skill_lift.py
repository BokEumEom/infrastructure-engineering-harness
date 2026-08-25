#!/usr/bin/env python3
"""Normalize paired baseline/treatment runs into a schema-validated Skill Lift report."""
from __future__ import annotations
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
SIGNALS=("security","skill_execution","skill_efficiency","accuracy","goal_accuracy","behavior_check")
DIMENSIONS=("security","correctness","discoverability","effectiveness","efficiency")

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def mean(xs): return sum(xs)/len(xs)
def pct(before, after): return None if before == 0 else ((after-before)/before)*100.0

def validate(data, schema_name):
    schema=load(ROOT/"schemas"/schema_name)
    errors=sorted(Draft202012Validator(schema).iter_errors(data),key=lambda e:list(e.absolute_path))
    if errors:
        for e in errors: print(f"SCHEMA ERROR {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}",file=sys.stderr)
        raise ValueError(schema_name)

def dimensions(scores):
    return {
        "security": scores["security"],
        "correctness": scores["accuracy"],
        "discoverability": scores["skill_execution"],
        "effectiveness": mean([scores["goal_accuracy"], scores["behavior_check"]]),
        "efficiency": scores["skill_efficiency"],
    }

def triplet(a,b): return {"baseline":round(a,6),"treatment":round(b,6),"lift":round(b-a,6)}
def verdict(lift): return "pass" if lift >= .05 else "fail" if lift <= -.10 else "neutral"

def main():
    if len(sys.argv)!=3:
        print("usage: score_skill_lift.py EXPERIMENT.json OUTPUT.json",file=sys.stderr); return 2
    exp=load(sys.argv[1])
    try: validate(exp,"skill-paired-experiment.schema.json")
    except ValueError: return 1
    cases=[]
    for pair in exp["pairs"]:
        b,t=pair["baseline"],pair["treatment"]
        bd,td=dimensions(b["scores"]),dimensions(t["scores"])
        signals={s:triplet(b["scores"][s],t["scores"][s]) for s in SIGNALS}
        dims={d:triplet(bd[d],td[d]) for d in DIMENSIONS}
        bc,tc=mean(list(bd.values())),mean(list(td.values()))
        token_pct=pct(b["usage"]["tokens"],t["usage"]["tokens"])
        duration_pct=pct(b["usage"]["duration_ms"],t["usage"]["duration_ms"])
        cases.append({
            "case_id":pair["case_id"],"kind":pair["kind"],"signals":signals,"dimensions":dims,
            "composite":triplet(bc,tc),
            "usage_delta":{
                "tokens":t["usage"]["tokens"]-b["usage"]["tokens"],
                "tool_calls":t["usage"]["tool_calls"]-b["usage"]["tool_calls"],
                "duration_ms":t["usage"]["duration_ms"]-b["usage"]["duration_ms"],
                "token_change_percent":None if token_pct is None else round(token_pct,3),
                "duration_change_percent":None if duration_pct is None else round(duration_pct,3)},
            "verdict":verdict(tc-bc)})
    lifts=[c["composite"]["lift"] for c in cases]
    outcome=[mean([c["signals"]["accuracy"]["lift"],c["signals"]["goal_accuracy"]["lift"]]) for c in cases]
    report={
        "schema_version":"1.0","source":exp["source"],"skill_id":exp["skill_id"],"harness":exp["harness"],"model":exp["model"],"workspace_id":exp["workspace_id"],"cases":cases,
        "summary":{
            "case_count":len(cases),"case_kinds":sorted(set(c["kind"] for c in cases)),
            "mean_dimension_lift":{d:round(mean([c["dimensions"][d]["lift"] for c in cases]),6) for d in DIMENSIONS},
            "mean_composite_lift":round(mean(lifts),6),"mean_outcome_lift":round(mean(outcome),6),
            "positive_case_rate":round(sum(x>0 for x in lifts)/len(lifts),6),"negative_case_rate":round(sum(x<0 for x in lifts)/len(lifts),6),
            "security_regressions":sum(c["dimensions"]["security"]["lift"]<0 for c in cases)}}
    try: validate(report,"skill-lift-report.schema.json")
    except ValueError: return 1
    Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"WROTE {sys.argv[2]} composite_lift={report['summary']['mean_composite_lift']:+.4f}")
    return 0
if __name__=="__main__": raise SystemExit(main())
