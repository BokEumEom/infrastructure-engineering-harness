#!/usr/bin/env python3
"""Check that an infrastructure scenario references real fixtures and evidence ids."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_infra_scenario.py <scenario.json>")
        return 2

    scenario_path = Path(sys.argv[1])
    if not scenario_path.is_absolute():
        scenario_path = ROOT / scenario_path
    scenario = load(scenario_path)

    env_path = ROOT / scenario["environment_fixture"]
    evidence_path = ROOT / scenario["evidence_fixture"]
    failures: list[str] = []

    if not env_path.exists():
        failures.append(f"missing environment fixture: {scenario['environment_fixture']}")
    if not evidence_path.exists():
        failures.append(f"missing evidence fixture: {scenario['evidence_fixture']}")

    if failures:
        for failure in failures:
            print(failure)
        return 1

    graph = load(env_path)
    evidence = load(evidence_path)
    resource_ids = {item["id"] for item in graph.get("resources", [])}
    evidence_ids = {item["id"] for item in evidence.get("observations", [])}

    for required in scenario.get("required_evidence", []):
        if required["id"] not in evidence_ids:
            failures.append(f"required evidence id not found in evidence fixture: {required['id']}")

    for observation in evidence.get("observations", []):
        resource = (observation.get("provenance") or {}).get("resource")
        if resource and resource not in resource_ids:
            failures.append(f"evidence {observation['id']} references unknown resource: {resource}")

    if not scenario.get("red_herrings"):
        failures.append("scenario must contain at least one red herring")
    if not scenario.get("prohibited_actions"):
        failures.append("scenario must contain at least one prohibited action")

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print(
        f"OK: {scenario['id']} binds {len(resource_ids)} resources, "
        f"{len(evidence_ids)} observations, {len(scenario['red_herrings'])} red herrings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
