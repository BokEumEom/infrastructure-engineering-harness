"""Deterministic reference helpers for a future persistent Agent Runtime.

This module deliberately does not call real tools. It models contracts that a
runtime implementation must preserve: append-only events, optimistic revision
checks, monotonic guards, fail-closed approval, and immutable normalized tool
outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable
from uuid import uuid4

from .provenance import ResourceProvenanceIndex


class StaleRevisionError(RuntimeError):
    """Raised when a caller tries to mutate state from an old revision."""


class ApprovalOutcome(str, Enum):
    ALLOWED_ONCE = "allowed_once"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    UNAVAILABLE = "unavailable"


class GuardDecision(str, Enum):
    ABSTAIN = "abstain"
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class RuntimeEvent:
    run_id: str
    seq: int
    type: str
    data: dict[str, Any]
    timestamp: str
    model_visible: bool = False
    ignorable: bool = False


@dataclass
class RuntimeEventLog:
    """Append-only in-memory reference event log."""

    run_id: str
    _events: list[RuntimeEvent] = field(default_factory=list)

    @property
    def events(self) -> tuple[RuntimeEvent, ...]:
        return tuple(self._events)

    def append(
        self,
        event_type: str,
        data: dict[str, Any],
        *,
        model_visible: bool = False,
        ignorable: bool = False,
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            run_id=self.run_id,
            seq=len(self._events),
            type=event_type,
            data=dict(data),
            timestamp=datetime.now(timezone.utc).isoformat(),
            model_visible=model_visible,
            ignorable=ignorable,
        )
        self._events.append(event)
        return event

    def replay_types(self) -> tuple[str, ...]:
        return tuple(event.type for event in self._events)


@dataclass
class RuntimeState:
    """Small CAS state projection for one runtime run."""

    run_id: str
    revision: int = 0
    status: str = "initialized"
    last_seq: int = -1
    pending_approval_id: str | None = None

    def mutate(self, expected_revision: int, **changes: Any) -> int:
        if expected_revision != self.revision:
            raise StaleRevisionError(
                f"stale runtime revision: expected {expected_revision}, current {self.revision}"
            )
        allowed = {"status", "last_seq", "pending_approval_id"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValueError(f"unsupported runtime state fields: {sorted(unknown)}")
        for key, value in changes.items():
            setattr(self, key, value)
        self.revision += 1
        return self.revision


@dataclass(frozen=True)
class GuardResult:
    name: str
    decision: GuardDecision
    reason: str | None = None


@dataclass(frozen=True)
class ToolPipelineResult:
    call_id: str
    status: str
    executed: bool
    approval_outcome: ApprovalOutcome | None
    guard_results: tuple[GuardResult, ...]
    normalized_result: dict[str, Any]


class ToolPipeline:
    """Reference policy pipeline without a real executor.

    A monotonic DENY always wins. Approval is fail closed: ALLOWED_ONCE is the
    only outcome that permits an approval-gated action.
    """

    def __init__(self, event_log: RuntimeEventLog):
        self.event_log = event_log

    @staticmethod
    def resolve_guards(results: Iterable[GuardResult]) -> GuardDecision:
        resolved = GuardDecision.ABSTAIN
        for result in results:
            if result.decision is GuardDecision.DENY:
                return GuardDecision.DENY
            if result.decision is GuardDecision.ALLOW:
                resolved = GuardDecision.ALLOW
        return resolved

    def evaluate(
        self,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        guards: Iterable[GuardResult] = (),
        approval_required: bool = False,
        approval_outcome: ApprovalOutcome | None = None,
        simulated_value: dict[str, Any] | None = None,
        execution_authority: str = "none",
        resource_provenance_required: bool = False,
        provenance: ResourceProvenanceIndex | None = None,
        target_resource_ids: Iterable[str] = (),
        bound_resource_scope: Iterable[str] | None = None,
    ) -> ToolPipelineResult:
        call_id = f"call-{uuid4().hex[:12]}"
        if execution_authority not in {"none", "read", "workflow", "change"}:
            raise ValueError("execution_authority must be none, read, workflow, or change")

        effective_guards = list(guards)
        provenance_mandatory = resource_provenance_required or execution_authority == "change"

        if provenance_mandatory:
            if provenance is None:
                effective_guards.append(
                    GuardResult(
                        "resource-provenance",
                        GuardDecision.DENY,
                        "RESOURCE_PROVENANCE_UNAVAILABLE",
                    )
                )
            else:
                check = provenance.validate(
                    target_resource_ids,
                    bound_scope=bound_resource_scope,
                )
                effective_guards.append(
                    GuardResult(
                        "resource-provenance",
                        GuardDecision.ALLOW if check.allowed else GuardDecision.DENY,
                        check.code,
                    )
                )

        guard_results = tuple(effective_guards)
        self.event_log.append(
            "tool/requested",
            {
                "call_id": call_id,
                "tool_name": tool_name,
                "arguments": arguments,
                "execution_authority": execution_authority,
            },
            model_visible=True,
        )

        for guard in guard_results:
            self.event_log.append(
                "policy/guard_decided",
                {
                    "call_id": call_id,
                    "guard": guard.name,
                    "decision": guard.decision.value,
                    "reason": guard.reason,
                },
            )

        if self.resolve_guards(guard_results) is GuardDecision.DENY:
            result = {"ok": False, "code": "GUARD_DENIED", "tool_name": tool_name}
            self.event_log.append("tool/result", {"call_id": call_id, "result": result}, model_visible=True)
            return ToolPipelineResult(
                call_id=call_id,
                status="denied",
                executed=False,
                approval_outcome=approval_outcome,
                guard_results=guard_results,
                normalized_result=result,
            )

        if approval_required:
            approval_id = f"approval-{uuid4().hex[:12]}"
            self.event_log.append(
                "approval/requested",
                {"approval_id": approval_id, "call_id": call_id, "tool_name": tool_name},
            )
            effective = approval_outcome or ApprovalOutcome.UNAVAILABLE
            self.event_log.append(
                "approval/decided",
                {"approval_id": approval_id, "call_id": call_id, "outcome": effective.value},
            )
            if effective is not ApprovalOutcome.ALLOWED_ONCE:
                result = {"ok": False, "code": "APPROVAL_DENIED", "tool_name": tool_name}
                self.event_log.append("tool/result", {"call_id": call_id, "result": result}, model_visible=True)
                return ToolPipelineResult(
                    call_id=call_id,
                    status="denied",
                    executed=False,
                    approval_outcome=effective,
                    guard_results=guard_results,
                    normalized_result=result,
                )
            approval_outcome = effective

        value = dict(simulated_value or {"ok": True})
        result = {"ok": True, "tool_name": tool_name, "value": value}
        self.event_log.append("tool/result", {"call_id": call_id, "result": result}, model_visible=True)
        return ToolPipelineResult(
            call_id=call_id,
            status="completed",
            executed=True,
            approval_outcome=approval_outcome,
            guard_results=guard_results,
            normalized_result=result,
        )
