#!/usr/bin/env python3
"""Validate task-specific evaluator profiles and weight invariants."""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def validate_profiles(data: dict) -> list[str]:
    schema = json.loads((ROOT / "schemas" / "task-eval-profiles.schema.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        where = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema:{where}: {error.message}")

    for name, profile in data.get("profiles", {}).items():
        required = set(profile.get("required_metrics", []))
        weights = profile.get("weights", {})
        if set(weights) != required:
            errors.append(f"invariant:{name}: weights must exactly match required_metrics")
        total = sum(float(value) for value in weights.values())
        if abs(total - 1.0) > 1e-9:
            errors.append(f"invariant:{name}: weights must sum to 1.0 (got {total})")
    return errors


def main() -> int:
    path = ROOT / "evals" / "task-profiles.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = validate_profiles(data)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"OK: task evaluator profiles valid ({len(data['profiles'])} profiles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
