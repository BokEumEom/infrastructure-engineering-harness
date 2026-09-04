"""Scope-neutral Runtime Skill Registry with invocation and release controls."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .release_control import SkillReleaseController


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
    release_state: str = "active"


class RuntimeSkillRegistry:
    def __init__(self, capability_registry: dict[str, Any], invocation_policy: dict[str, Any]):
        self.capability_registry = capability_registry
        self.invocation_policy = invocation_policy
        self._sources = {item["id"]: item for item in capability_registry["sources"]}
        self._rules = {item["skill_id"]: item for item in invocation_policy.get("rules", [])}

    @classmethod
    def from_files(cls, capability_path: Path, policy_path: Path) -> "RuntimeSkillRegistry":
        return cls(
            yaml.safe_load(capability_path.read_text(encoding="utf-8")),
            yaml.safe_load(policy_path.read_text(encoding="utf-8")),
        )

    def _invocation(self, skill_id: str) -> dict[str, bool]:
        defaults = self.invocation_policy["defaults"]
        rule = self._rules.get(skill_id, {})
        return {
            "model_invocable": rule.get("model_invocable", defaults["model_invocable"]),
            "user_invocable": rule.get("user_invocable", defaults["user_invocable"]),
            "catalog_visible": rule.get("catalog_visible", defaults["catalog_visible"]),
        }

    def list(
        self,
        *,
        for_model: bool = False,
        for_user: bool = False,
        enabled_capability_ids: set[str] | None = None,
        release_controller: SkillReleaseController | None = None,
        rollout_key: str | None = None,
    ) -> tuple[RuntimeSkillSummary, ...]:
        summaries: list[RuntimeSkillSummary] = []
        for capability in self.capability_registry["capabilities"]:
            skill_id = capability["id"]
            if enabled_capability_ids is not None and skill_id not in enabled_capability_ids:
                continue

            release_state = "active"
            if release_controller is not None:
                release = release_controller.decision(skill_id, rollout_key=rollout_key)
                release_state = release.state
                if not release.enabled:
                    continue

            invocation = self._invocation(skill_id)
            if not invocation["catalog_visible"]:
                continue
            if for_model and not invocation["model_invocable"]:
                continue
            if for_user and not invocation["user_invocable"]:
                continue

            source = self._sources[capability["source"]]
            execution_authority = "none" if source["execution"] == "reference_only" else "governed"
            summaries.append(
                RuntimeSkillSummary(
                    id=skill_id,
                    source=capability["source"],
                    skill_path=capability["skill_path"],
                    category=capability["category"],
                    risk=capability["risk"],
                    model_invocable=invocation["model_invocable"],
                    user_invocable=invocation["user_invocable"],
                    catalog_visible=invocation["catalog_visible"],
                    execution_authority=execution_authority,
                    intents=tuple(capability["intents"]),
                    release_state=release_state,
                )
            )
        return tuple(sorted(summaries, key=lambda item: item.id))

    def get(
        self,
        skill_id: str,
        *,
        actor: str,
        enabled_capability_ids: set[str] | None = None,
        release_controller: SkillReleaseController | None = None,
        rollout_key: str | None = None,
    ) -> RuntimeSkillSummary:
        if actor not in {"model", "user", "trusted_runtime"}:
            raise ValueError("actor must be model, user, or trusted_runtime")
        registered_ids = {item["id"] for item in self.capability_registry["capabilities"]}
        if skill_id not in registered_ids:
            raise KeyError(skill_id)
        if enabled_capability_ids is not None and skill_id not in enabled_capability_ids:
            raise PermissionError(f"skill {skill_id} is not enabled in the current runtime surface")
        if release_controller is not None:
            release = release_controller.decision(skill_id, rollout_key=rollout_key)
            if not release.enabled:
                raise PermissionError(f"skill {skill_id} blocked by release policy: {release.reason}")

        all_entries = {
            item.id: item
            for item in self.list(
                enabled_capability_ids=enabled_capability_ids,
                release_controller=release_controller,
                rollout_key=rollout_key,
            )
        }
        entry = all_entries[skill_id]
        if actor == "model" and not entry.model_invocable:
            raise PermissionError(f"skill {skill_id} is not model invocable")
        if actor == "user" and not entry.user_invocable:
            raise PermissionError(f"skill {skill_id} is not user invocable")
        return entry
