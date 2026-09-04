#!/usr/bin/env python3
"""Validate Skill release policy schema and registered Skill references."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    policy_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "runtime" / "release-policy.yaml"
    schema = json.loads(
        (ROOT / "schemas" / "runtime-skill-release-policy.schema.json").read_text(encoding="utf-8")
    )
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    registry = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
    failures: list[str] = []

    for error in sorted(Draft202012Validator(schema).iter_errors(policy), key=lambda e: list(e.path)):
        where = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{where}: {error.message}")

    capability_ids = {item["id"] for item in registry["capabilities"]}
    seen: set[str] = set()
    for rule in policy.get("rules", []):
        skill_id = rule.get("skill_id")
        if skill_id in seen:
            failures.append(f"duplicate release rule: {skill_id}")
        seen.add(skill_id)
        if skill_id not in capability_ids:
            failures.append(f"unknown skill_id in release policy: {skill_id}")
        if rule.get("state") == "canary" and "canary_percent" not in rule:
            failures.append(f"canary rule missing canary_percent: {skill_id}")

    if failures:
        print("SKILL RELEASE POLICY FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"SKILL RELEASE POLICY PASSED rules={len(policy.get('rules', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
