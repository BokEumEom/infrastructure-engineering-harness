#!/usr/bin/env python3
"""Check that an infrastructure scenario references real fixtures and valid eval contracts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_SUCCESS_CONDITIONS = {
    "classification_matches_ground_truth",
    "required_evidence_cited",
    "red_herrings_not_promoted",
    "no_prohibited_mutation",
    "recovery_requires_independent_verification",
}


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

    reported_signals = scenario.get("reported_signals") or []
    if not reported_signals:
        failures.append("scenario must contain at least one model-visible reported signal")

    red_herrings = scenario.get("red_herrings") or []
    if not red_herrings:
        failures.append("scenario must contain at least one red herring")
    reported_signal_set = set(reported_signals)
    for red_herring in red_herrings:
        signal = red_herring.get("signal")
        if signal not in reported_signal_set:
            failures.append(f"red herring is not present in reported_signals: {signal}")

    if not scenario.get("prohibited_actions"):
        failures.append("scenario must contain at least one prohibited action")

    ground_truth = scenario.get("ground_truth") or {}
    if not ground_truth.get("classification"):
        failures.append("scenario ground_truth.classification is required")

    success_conditions = scenario.get("success_conditions") or []
    if not success_conditions:
        failures.append("scenario must contain success conditions")
    condition_ids: list[str] = []
    for condition in success_conditions:
        if not isinstance(condition, dict):
            failures.append("success conditions must use structured {id, description} objects")
            continue
        condition_id = condition.get("id")
        description = condition.get("description")
        if not condition_id or not description:
            failures.append("success condition requires id and description")
            continue
        condition_ids.append(condition_id)
        if condition_id not in SUPPORTED_SUCCESS_CONDITIONS:
            failures.append(f"unsupported success condition id: {condition_id}")

    if len(condition_ids) != len(set(condition_ids)):
        failures.append("success condition ids must be unique")

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print(
        f"OK: {scenario['id']} binds {len(resource_ids)} resources, "
        f"{len(evidence_ids)} observations, {len(red_herrings)} red herrings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
