"""Deterministic Skill release control with canary rollout and kill switch."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class SkillReleaseDecision:
    skill_id: str
    enabled: bool
    state: str
    reason: str
    bucket: float | None = None


class SkillReleaseController:
    """Host-owned release policy for model-visible Skills.

    A disabled Skill is removed regardless of model intent. Canary assignment is
    deterministic for a stable rollout key, so the same session/run does not flap.
    """

    def __init__(self, policy: dict[str, Any]):
        self.policy = policy
        self.defaults = policy.get("defaults", {"state": "active", "canary_percent": 100})
        self.rules = {item["skill_id"]: item for item in policy.get("rules", [])}

    @classmethod
    def from_file(cls, path: str | Path) -> "SkillReleaseController":
        return cls(yaml.safe_load(Path(path).read_text(encoding="utf-8")))

    @staticmethod
    def _bucket(skill_id: str, rollout_key: str) -> float:
        digest = hashlib.sha256(f"{skill_id}:{rollout_key}".encode("utf-8")).hexdigest()
        value = int(digest[:8], 16) % 10000
        return value / 100.0

    def decision(self, skill_id: str, *, rollout_key: str | None = None) -> SkillReleaseDecision:
        rule = self.rules.get(skill_id, {})
        state = rule.get("state", self.defaults.get("state", "active"))
        if state not in {"active", "canary", "disabled"}:
            raise ValueError(f"unsupported release state for {skill_id}: {state}")

        if state == "disabled":
            return SkillReleaseDecision(
                skill_id=skill_id,
                enabled=False,
                state=state,
                reason=rule.get("reason", "kill_switch_disabled"),
            )

        if state == "active":
            return SkillReleaseDecision(
                skill_id=skill_id,
                enabled=True,
                state=state,
                reason="active",
            )

        percent = float(rule.get("canary_percent", self.defaults.get("canary_percent", 0)))
        if percent < 0 or percent > 100:
            raise ValueError("canary_percent must be between 0 and 100")
        if rollout_key is None:
            return SkillReleaseDecision(
                skill_id=skill_id,
                enabled=False,
                state=state,
                reason="canary_requires_rollout_key",
            )
        bucket = self._bucket(skill_id, rollout_key)
        enabled = bucket < percent
        return SkillReleaseDecision(
            skill_id=skill_id,
            enabled=enabled,
            state=state,
            reason="canary_included" if enabled else "canary_excluded",
            bucket=bucket,
        )
