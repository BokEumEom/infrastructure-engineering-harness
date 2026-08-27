#!/usr/bin/env python3
"""Score bare/minimal/full Harness profiles without assuming more context is better."""
from __future__ import annotations
import json
import sys
from pathlib import Path

DIMS=("outcome","evidence","safety","exploration","autonomy","efficiency")

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def mean(xs): return sum(xs)/len(xs)
def composite(run): return mean([run["scores"][d] for d in DIMS])
def delta(a,b): return round(b-a,6)

def main() -> int:
    if len(sys.argv)!=3:
        print("usage: score_harness_lift.py EXPERIMENT.json OUTPUT.json", file=sys.stderr)
        return 2
    exp=load(sys.argv[1])
    cases=[]
    for case in exp["cases"]:
        runs={p:case[p] for p in ("bare","minimal","full")}
        comps={p:composite(runs[p]) for p in runs}
        item={
            "case_id":case["case_id"],
            "kind":case["kind"],
            "profiles":{
                p:{
                    "composite":round(comps[p],6),
                    "outcome":runs[p]["scores"]["outcome"],
                    "evidence":runs[p]["scores"]["evidence"],
                    "safety":runs[p]["scores"]["safety"],
                    "usage":runs[p]["usage"]
                } for p in runs
            },
            "lift":{
                "minimal_vs_bare_composite":delta(comps["bare"],comps["minimal"]),
                "minimal_vs_bare_outcome":delta(runs["bare"]["scores"]["outcome"],runs["minimal"]["scores"]["outcome"]),
                "full_vs_minimal_composite":delta(comps["minimal"],comps["full"]),
                "full_vs_minimal_outcome":delta(runs["minimal"]["scores"]["outcome"],runs["full"]["scores"]["outcome"])
            }
        }
        cases.append(item)
    summary={
        "case_count":len(cases),
        "case_kinds":sorted({c["kind"] for c in cases}),
        "mean_minimal_vs_bare_composite":round(mean([c["lift"]["minimal_vs_bare_composite"] for c in cases]),6),
        "mean_minimal_vs_bare_outcome":round(mean([c["lift"]["minimal_vs_bare_outcome"] for c in cases]),6),
        "mean_full_vs_minimal_composite":round(mean([c["lift"]["full_vs_minimal_composite"] for c in cases]),6),
        "mean_full_vs_minimal_outcome":round(mean([c["lift"]["full_vs_minimal_outcome"] for c in cases]),6),
        "full_worse_than_minimal_cases":sum(c["lift"]["full_vs_minimal_composite"]<0 for c in cases),
        "minimal_safety_regressions_vs_bare":sum(c["profiles"]["minimal"]["safety"]<c["profiles"]["bare"]["safety"] for c in cases),
        "full_safety_regressions_vs_minimal":sum(c["profiles"]["full"]["safety"]<c["profiles"]["minimal"]["safety"] for c in cases),
        "minimal_evidence_regressions_vs_bare":sum(c["profiles"]["minimal"]["evidence"]<c["profiles"]["bare"]["evidence"] for c in cases),
        "full_evidence_regressions_vs_minimal":sum(c["profiles"]["full"]["evidence"]<c["profiles"]["minimal"]["evidence"] for c in cases)
    }
    report={"schema_version":"1.0","source":exp["source"],"harness_id":exp["harness_id"],"model":exp["model"],"workspace_id":exp["workspace_id"],"cases":cases,"summary":summary}
    Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"WROTE {sys.argv[2]} minimal_vs_bare={summary['mean_minimal_vs_bare_composite']:+.4f} full_vs_minimal={summary['mean_full_vs_minimal_composite']:+.4f}")
    return 0

if __name__=="__main__": raise SystemExit(main())
