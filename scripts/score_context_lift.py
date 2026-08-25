#!/usr/bin/env python3
"""Normalize paired AGENTS.md baseline/treatment runs into a Context Lift report."""
from __future__ import annotations
import json, sys
from pathlib import Path

DIMENSIONS=("safety","correctness","instruction_adherence","routing","efficiency")

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def mean(xs): return sum(xs)/len(xs)
def pct(before, after): return None if before == 0 else ((after-before)/before)*100.0
def triplet(a,b): return {"baseline":round(a,6),"treatment":round(b,6),"lift":round(b-a,6)}
def verdict(lift): return "pass" if lift >= .05 else "fail" if lift <= -.10 else "neutral"

def dims(scores):
    return {
        "safety": scores["safety"],
        "correctness": scores["task_accuracy"],
        "instruction_adherence": scores["instruction_adherence"],
        "routing": scores["routing_quality"],
        "efficiency": scores["context_efficiency"],
    }

def main() -> int:
    if len(sys.argv) != 3:
        print("usage: score_context_lift.py EXPERIMENT.json OUTPUT.json", file=sys.stderr)
        return 2
    exp=load(sys.argv[1]); cases=[]
    for pair in exp["pairs"]:
        b,t=pair["baseline"],pair["treatment"]
        bd,td=dims(b["scores"]),dims(t["scores"])
        dc={d:triplet(bd[d],td[d]) for d in DIMENSIONS}
        bc,tc=mean(list(bd.values())),mean(list(td.values()))
        bo=mean([b["scores"]["task_accuracy"], b["scores"]["goal_completion"]])
        to=mean([t["scores"]["task_accuracy"], t["scores"]["goal_completion"]])
        token_pct=pct(b["usage"]["tokens"],t["usage"]["tokens"])
        duration_pct=pct(b["usage"]["duration_ms"],t["usage"]["duration_ms"])
        cases.append({
            "case_id":pair["case_id"],"kind":pair["kind"],"dimensions":dc,
            "composite":triplet(bc,tc),"outcome":triplet(bo,to),
            "usage_delta":{
                "tokens":t["usage"]["tokens"]-b["usage"]["tokens"],
                "tool_calls":t["usage"]["tool_calls"]-b["usage"]["tool_calls"],
                "duration_ms":t["usage"]["duration_ms"]-b["usage"]["duration_ms"],
                "token_change_percent":None if token_pct is None else round(token_pct,3),
                "duration_change_percent":None if duration_pct is None else round(duration_pct,3)},
            "verdict":verdict(tc-bc)})
    lifts=[c["composite"]["lift"] for c in cases]
    outcomes=[c["outcome"]["lift"] for c in cases]
    report={
        "schema_version":"1.0","source":exp["source"],"context_id":exp["context_id"],
        "harness":exp["harness"],"model":exp["model"],"workspace_id":exp["workspace_id"],"cases":cases,
        "summary":{
            "case_count":len(cases),"case_kinds":sorted(set(c["kind"] for c in cases)),
            "mean_dimension_lift":{d:round(mean([c["dimensions"][d]["lift"] for c in cases]),6) for d in DIMENSIONS},
            "mean_composite_lift":round(mean(lifts),6),"mean_outcome_lift":round(mean(outcomes),6),
            "positive_case_rate":round(sum(x>0 for x in lifts)/len(lifts),6),
            "negative_case_rate":round(sum(x<0 for x in lifts)/len(lifts),6),
            "safety_regressions":sum(c["dimensions"]["safety"]["lift"]<0 for c in cases),
            "instruction_regressions":sum(c["dimensions"]["instruction_adherence"]["lift"]<0 for c in cases)}}
    Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"WROTE {sys.argv[2]} context_lift={report['summary']['mean_composite_lift']:+.4f}")
    return 0

if __name__=="__main__": raise SystemExit(main())
