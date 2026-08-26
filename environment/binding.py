"""Environment binding helpers.

A Bound Capability is a runtime-scoped view over an existing capability. Binding
may narrow scope and permissions, but it must never manufacture execution
authority that the capability source did not already possess.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bind_capability(
    registry: dict[str, Any],
    resource_graph: dict[str, Any],
    *,
    capability_id: str,
    resource_ids: list[str],
    evidence_sources: list[str] | None = None,
    permission_mode: str = "read_only",
    allowed_operations: list[str] | None = None,
    prohibited_operations: list[str] | None = None,
) -> dict[str, Any]:
    if permission_mode not in {"read_only", "workflow", "change"}:
        raise ValueError("permission_mode must be read_only, workflow, or change")

    capabilities = {item["id"]: item for item in registry["capabilities"]}
    sources = {item["id"]: item for item in registry["sources"]}
    if capability_id not in capabilities:
        raise KeyError(f"unknown capability: {capability_id}")

    resources = {item["id"]: item for item in resource_graph["resources"]}
    missing = sorted(set(resource_ids) - set(resources))
    if missing:
        raise KeyError(f"unknown resource ids: {', '.join(missing)}")

    capability = capabilities[capability_id]
    source = sources[capability["source"]]
    execution_authority = "none" if source["execution"] == "reference_only" else "governed"

    # Binding narrows execution. A reference-only capability remains non-executable
    # regardless of the requested permission mode.
    if execution_authority == "none" and permission_mode == "change":
        permission_mode = "read_only"

    human_gate_required = bool(capability.get("requires_human_gate")) or permission_mode == "change"

    return {
        "schema_version": "1.0",
        "binding_id": f"{capability_id}:{resource_graph['graph_id']}",
        "capability_id": capability_id,
        "resource_graph_id": resource_graph["graph_id"],
        "resource_scope": resource_ids,
        "evidence_sources": evidence_sources or [],
        "permission_scope": {
            "mode": permission_mode,
            "allowed_operations": allowed_operations or [],
            "prohibited_operations": prohibited_operations or ["unapproved_production_mutation"],
        },
        "execution_authority": execution_authority,
        "human_gate_required": human_gate_required,
    }
