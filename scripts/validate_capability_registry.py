#!/usr/bin/env python3
"""Validate the capability registry schema and safety invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "capability-registry.schema.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_registry(data: dict) -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = ".".join(str(p) for p in error.path) or "$"
        errors.append(f"schema:{where}: {error.message}")

    sources = data.get("sources", []) if isinstance(data, dict) else []
    capabilities = data.get("capabilities", []) if isinstance(data, dict) else []

    source_ids = [s.get("id") for s in sources if isinstance(s, dict)]
    if len(source_ids) != len(set(source_ids)):
        errors.append("invariant: source ids must be unique")
    capability_ids = [c.get("id") for c in capabilities if isinstance(c, dict)]
    if len(capability_ids) != len(set(capability_ids)):
        errors.append("invariant: capability ids must be unique")

    source_map = {s.get("id"): s for s in sources if isinstance(s, dict) and s.get("id")}
    for source in sources:
        if not isinstance(source, dict):
            continue
        if source.get("type") == "github":
            revision = str(source.get("revision", ""))
            if not SHA40.match(revision):
                errors.append(f"invariant: github source {source.get('id')} must pin a 40-char commit SHA")
            if source.get("trust") == "pinned_reference" and source.get("execution") != "reference_only":
                errors.append(f"invariant: pinned reference source {source.get('id')} must be reference_only")

    for capability in capabilities:
        if not isinstance(capability, dict):
            continue
        source_id = capability.get("source")
        source = source_map.get(source_id)
        if source is None:
            errors.append(f"invariant: capability {capability.get('id')} references unknown source {source_id}")
            continue
        if source.get("execution") == "reference_only" and capability.get("execution_policy") != "reference_only":
            errors.append(f"invariant: external reference capability {capability.get('id')} must remain reference_only")
        if capability.get("risk") in {"high", "critical"} and not capability.get("requires_human_gate"):
            errors.append(f"invariant: high-risk capability {capability.get('id')} must require a human gate")

    local_capabilities = {
        c.get("id"): c
        for c in capabilities
        if isinstance(c, dict) and c.get("source") == "harness-local" and c.get("id")
    }
    local_skill_dirs = {
        path.parent.name: path
        for path in (ROOT / "skills").glob("*/SKILL.md")
    }

    missing_registry = sorted(set(local_skill_dirs) - set(local_capabilities))
    for skill_id in missing_registry:
        errors.append(f"invariant: local Skill {skill_id} must be registered as harness-local capability")

    for skill_id, capability in local_capabilities.items():
        expected_path = ROOT / "skills" / str(capability.get("skill_path", ""))
        if skill_id not in local_skill_dirs:
            errors.append(f"invariant: harness-local capability {skill_id} has no skills/{skill_id}/SKILL.md")
        elif not expected_path.exists():
            errors.append(f"invariant: harness-local capability {skill_id} skill_path does not exist: {capability.get('skill_path')}")

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "capabilities" / "registry.yaml"
    data = load_registry(path)
    errors = validate_registry(data)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"OK: capability registry valid ({len(data['sources'])} sources, {len(data['capabilities'])} capabilities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
