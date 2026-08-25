#!/usr/bin/env python3
"""Validate AGENTS.md as a bounded, addressable behavioral context surface."""
from __future__ import annotations
import re, sys
from pathlib import Path
import yaml

RULE_RE = re.compile(r"<!--\s*rule:\s*([a-z0-9][a-z0-9-]*)\s*-->")

def estimated_tokens(text: str) -> int:
    return (len(text.encode("utf-8")) + 3) // 4

def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_agents_contract.py AGENTS.md POLICY.yaml", file=sys.stderr)
        return 2
    agents = Path(sys.argv[1])
    policy = yaml.safe_load(Path(sys.argv[2]).read_text(encoding="utf-8"))
    text = agents.read_text(encoding="utf-8")
    budget = int(policy["memory"]["budget_tokens"])
    tokens = estimated_tokens(text)
    rules = RULE_RE.findall(text)
    failures: list[str] = []
    if tokens > budget:
        failures.append(f"estimated AGENTS.md tokens {tokens} exceed budget {budget}")
    duplicates = sorted({r for r in rules if rules.count(r) > 1})
    if duplicates:
        failures.append("duplicate rule ids: " + ", ".join(duplicates))
    if not rules:
        failures.append("AGENTS.md must contain at least one addressable <!-- rule: ... --> marker")
    if failures:
        print("AGENTS CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"AGENTS CONTRACT PASSED ({tokens}/{budget} estimated tokens, {len(rules)} rule ids)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
