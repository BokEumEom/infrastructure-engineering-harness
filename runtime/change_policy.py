"""Deterministic risk classification for staged infrastructure change proposals."""
from __future__ import annotations

from typing import Any


def evaluate_change_policy(proposal: dict[str, Any]) -> dict[str, Any]:
    """Classify a bounded infrastructure proposal before approval/execution.

    The policy is intentionally conservative. Destructive, privilege-expanding or
    public-exposure changes are high risk and are not executable by the reference
    environment benchmark. Capacity/cost changes are medium risk and require an
    explicit one-shot approval. Other bounded non-destructive changes are low risk.
    """
    inputs = proposal.get("risk_inputs") if isinstance(proposal.get("risk_inputs"), dict) else {}
    destructive = bool(inputs.get("destructive"))
    privilege_expansion = bool(inputs.get("privilege_expansion"))
    public_exposure = bool(inputs.get("public_exposure"))
    capacity_increase = bool(inputs.get("capacity_increase"))
    cost_implication = bool(inputs.get("cost_implication"))
    ownership_domains = [str(x) for x in (inputs.get("ownership_domains") or [])]

    reasons: list[str] = []
    if destructive:
        reasons.append("destructive operation")
    if privilege_expansion:
        reasons.append("privilege expansion")
    if public_exposure:
        reasons.append("public exposure change")
    if capacity_increase:
        reasons.append("capacity increase")
    if cost_implication:
        reasons.append("cost implication")
    if len(set(ownership_domains)) > 1:
        reasons.append("cross-ownership change")

    if destructive or privilege_expansion or public_exposure:
        risk = "high"
        decision = "blocked"
        approval_required = True
        executable = False
    elif capacity_increase or cost_implication or len(set(ownership_domains)) > 1:
        risk = "medium"
        decision = "approval_required"
        approval_required = True
        executable = True
    else:
        risk = "low"
        decision = "allowed"
        approval_required = False
        executable = True

    return {
        "schema_version": "1.0",
        "policy_revision": "infra-change-policy-v1",
        "risk": risk,
        "decision": decision,
        "approval_required": approval_required,
        "executable": executable,
        "reasons": reasons or ["bounded non-destructive change"],
        "boundaries": {
            "destructive": destructive,
            "privilege_expansion": privilege_expansion,
            "public_exposure": public_exposure,
            "capacity_increase": capacity_increase,
            "cost_implication": cost_implication,
            "ownership_domains": ownership_domains,
        },
    }
