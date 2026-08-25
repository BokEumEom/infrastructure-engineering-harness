#!/usr/bin/env python3
"""Validate a context update proposal against agent-context policy."""
from __future__ import annotations
import json, sys
from pathlib import Path
import yaml


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_context_proposal.py POLICY.yaml PROPOSAL.json", file=sys.stderr)
        return 2
    policy = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    proposal = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    failures=[]
    memory=policy["memory"]; evidence=policy["evidence"]; ppolicy=policy["proposal"]
    if proposal.get("target") != memory["target"]:
        failures.append("proposal target differs from policy memory target")
    if proposal.get("budget_tokens") != memory["budget_tokens"]:
        failures.append("proposal budget_tokens must match policy budget")
    if proposal.get("after_tokens", 10**9) > memory["budget_tokens"]:
        failures.append("proposal exceeds AGENTS.md token budget")
    edits=proposal.get("edits", [])
    if len(edits) > ppolicy["max_edits"]:
        failures.append("proposal exceeds max edit count")
    if ppolicy["human_review_required"] and proposal.get("human_review_required") is not True:
        failures.append("human review must remain required")
    if proposal.get("source_of_truth_writeback") is not False:
        failures.append("source-of-truth writeback is prohibited")
    for edit in edits:
        if edit.get("operation") == "add" and len(set(edit.get("evidence_session_ids", []))) < evidence["min_sessions_for_new_rule"]:
            failures.append(f"new rule {edit.get('id')} lacks independent session evidence")
    if failures:
        print("CONTEXT PROPOSAL GATE FAILED")
        for failure in failures: print(f"- {failure}")
        return 1
    print(f"CONTEXT PROPOSAL GATE PASSED ({len(edits)} edits, {proposal['after_tokens']}/{memory['budget_tokens']} tokens)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
