#!/usr/bin/env python3
"""Validate the Infrastructure Engineering Agent contract."""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    contract_path = ROOT / "agents" / "infrastructure_engineering" / "agent.yaml"
    schema_path = ROOT / "schemas" / "agent-contract.schema.json"
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    for error in sorted(Draft202012Validator(schema).iter_errors(contract), key=lambda e: list(e.path)):
        where = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{where}: {error.message}")

    required_runtime_ownership = {
        "evidence_provenance",
        "resource_provenance",
        "permission_scope",
        "approval_state",
        "independent_verification",
        "untrusted_content_fencing",
        "change_revision_validation",
        "runtime_recording",
        "persistent_memory",
        "cache_aware_context_assembly",
        "latency_metrics",
        "skill_release_control",
    }
    owned = set(contract.get("runtime_boundary", {}).get("owns", []))
    missing = sorted(required_runtime_ownership - owned)
    if missing:
        failures.append("runtime boundary missing: " + ", ".join(missing))

    if failures:
        print("AGENT CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AGENT CONTRACT PASSED")
    print(f"Product: {contract['name']}")
    print("Capabilities: " + ", ".join(contract["capability_domains"]))
    print("Runtime: internal harness control plane")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
