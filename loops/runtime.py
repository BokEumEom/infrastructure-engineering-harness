"""Small deterministic helpers for infrastructure engineering loop state.

This module does not execute agent skills. It provides reference control-plane
functions for state transitions, independently verified facts, progress budgets,
and regression obligations.
"""
from __future__ import annotations

from copy import deepcopy

TERMINAL_STATUSES = {"done", "escalated", "failed", "budget_exhausted"}
VERIFIERS = {"environment", "tool", "human", "test"}
ALLOWED_TRANSITIONS = {
    "initialized": {"running", "escalated", "failed"},
    "running": {"running", "waiting", "verifying", "done", "escalated", "failed", "budget_exhausted"},
    "waiting": {"running", "verifying", "escalated", "failed", "budget_exhausted"},
    "verifying": {"running", "waiting", "done", "escalated", "failed", "budget_exhausted"},
}


def transition(state: dict, new_status: str) -> dict:
    current = state["status"]
    if current in TERMINAL_STATUSES:
        raise ValueError(f"terminal state cannot transition: {current}")
    if new_status not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"invalid transition: {current} -> {new_status}")
    updated = deepcopy(state)
    updated["status"] = new_status
    return updated


def add_verified_fact(state: dict, fact: dict) -> dict:
    verifier = fact.get("verified_by")
    if verifier not in VERIFIERS:
        raise ValueError("verified facts require environment/tool/human/test verification")
    if not fact.get("evidence_refs"):
        raise ValueError("verified facts require evidence_refs")
    updated = deepcopy(state)
    existing = {item["id"] for item in updated.get("verified_facts", [])}
    if fact["id"] not in existing:
        updated.setdefault("verified_facts", []).append(deepcopy(fact))
    return updated


def record_iteration(state: dict, *, step: str, event: str, outcome: str, evidence_refs: list[str] | None = None) -> dict:
    if state["status"] in TERMINAL_STATUSES:
        raise ValueError("cannot record an iteration after terminal state")
    if outcome not in {"progress", "no_progress", "blocked", "verified", "failed", "escalated"}:
        raise ValueError(f"unsupported outcome: {outcome}")
    updated = deepcopy(state)
    updated["iteration"] += 1
    iteration = updated["iteration"]
    updated["current_step"] = step
    updated.setdefault("history", []).append({"iteration": iteration, "step": step, "event": event, "outcome": outcome, "evidence_refs": list(evidence_refs or [])})
    progress = updated.setdefault("progress", {"last_material_progress_iteration": 0, "no_progress_iterations": 0})
    if outcome in {"progress", "verified"}:
        progress["last_material_progress_iteration"] = iteration
        progress["no_progress_iterations"] = 0
    elif outcome in {"no_progress", "blocked"}:
        progress["no_progress_iterations"] += 1
    return updated


def budget_exhausted(spec: dict, state: dict) -> str | None:
    budgets = spec["budgets"]
    if state["iteration"] >= budgets["max_iterations"]:
        return "max_iterations"
    if state.get("progress", {}).get("no_progress_iterations", 0) >= budgets["max_no_progress_iterations"]:
        return "max_no_progress_iterations"
    return None


def regression_summary(state: dict) -> str:
    statuses = [item["status"] for item in state.get("regression_obligations", [])]
    if any(status == "failed" for status in statuses):
        return "failed"
    if statuses and all(status == "passed" for status in statuses):
        return "passed"
    return "pending"
