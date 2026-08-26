"""Scope-neutral reference Runtime Skill Registry.

The durable capability registry owns source trust/risk/execution metadata.
This runtime layer owns invocation visibility and lazy selection policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class RuntimeSkillSummary:
    id: str
    source: str
    skill_path: str
    category: str
    risk: str
    model_invocable: bool
    user_invocable: bool
    catalog_visible: bool
    execution_authority: str
    intents: tuple[str, ...]


class RuntimeSkillRegistry:
    def __init__(self, capability_registry: dict[str, Any], invocation_policy: dict[str, Any]):
        self.capability_registry = capability_registry
        self.invocation_policy = invocation_policy
        self._sources = {item["id"]: item for item in capability_registry["sources"]}
        self._rules = {item["skill_id"]: item for item in invocation_policy.get("rules", [])}

    @classmethod
    def from_files(cls, capability_path: Path, policy_path: Path) -> "RuntimeSkillRegistry":
        capability_registry = yaml.safe_load(capability_path.read_text(encoding="utf-8"))
        invocation_policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        return cls(capability_registry, invocation_policy)

    def _invocation(self, skill_id: str) -> dict[str, bool]:
        defaults = self.invocation_policy["defaults"]
        rule = self._rules.get(skill_id, {})
        return {
            "model_invocable": rule.get("model_invocable", defaults["model_invocable"]),
            "user_invocable": rule.get("user_invocable", defaults["user_invocable"]),
            "catalog_visible": rule.get("catalog_visible", defaults["catalog_visible"]),
        }

    def list(self, *, for_model: bool = False, for_user: bool = False) -> tuple[RuntimeSkillSummary, ...]:
        summaries: list[RuntimeSkillSummary] = []
        for capability in self.capability_registry["capabilities"]:
            invocation = self._invocation(capability["id"])
            if not invocation["catalog_visible"]:
                continue
            if for_model and not invocation["model_invocable"]:
                continue
            if for_user and not invocation["user_invocable"]:
                continue

            source = self._sources[capability["source"]]
            execution_authority = (
                "none" if source["execution"] == "reference_only" else "governed"
            )
            summaries.append(
                RuntimeSkillSummary(
                    id=capability["id"],
                    source=capability["source"],
                    skill_path=capability["skill_path"],
                    category=capability["category"],
                    risk=capability["risk"],
                    model_invocable=invocation["model_invocable"],
                    user_invocable=invocation["user_invocable"],
                    catalog_visible=invocation["catalog_visible"],
                    execution_authority=execution_authority,
                    intents=tuple(capability["intents"]),
                )
            )
        return tuple(sorted(summaries, key=lambda item: item.id))

    def get(self, skill_id: str, *, actor: str) -> RuntimeSkillSummary:
        if actor not in {"model", "user", "trusted_runtime"}:
            raise ValueError("actor must be model, user, or trusted_runtime")
        all_entries = {item.id: item for item in self.list()}
        if skill_id not in all_entries:
            raise KeyError(skill_id)
        entry = all_entries[skill_id]
        if actor == "model" and not entry.model_invocable:
            raise PermissionError(f"skill {skill_id} is not model invocable")
        if actor == "user" and not entry.user_invocable:
            raise PermissionError(f"skill {skill_id} is not user invocable")
        return entry
