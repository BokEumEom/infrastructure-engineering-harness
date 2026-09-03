"""Deterministic staged-change and apply-time revalidation contracts."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any
from uuid import uuid4

from .provenance import ResourceProvenanceIndex


def _digest(value: dict[str, Any]) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class StagedChange:
    change_id: str
    revision: int
    resource_graph_id: str
    resource_ids: tuple[str, ...]
    policy_revision: str
    proposal_digest: str
    proposal: dict[str, Any]


@dataclass(frozen=True)
class ApprovalGrant:
    approval_id: str
    change_id: str
    change_revision: int
    resource_graph_id: str
    policy_revision: str
    proposal_digest: str
    outcome: str = "allowed_once"


@dataclass(frozen=True)
class ApplyCheck:
    allowed: bool
    code: str


class ChangeControl:
    """Reference host-owned approval state.

    Approval is bound to an exact staged revision and is one-shot. The model does
    not create ApprovalGrant objects in a production implementation; the host does.
    """

    def __init__(self) -> None:
        self._consumed: set[str] = set()

    def stage(
        self,
        proposal: dict[str, Any],
        *,
        resource_graph_id: str,
        resource_ids: list[str],
        policy_revision: str,
        revision: int = 1,
    ) -> StagedChange:
        return StagedChange(
            change_id=f"change-{uuid4().hex[:12]}",
            revision=revision,
            resource_graph_id=resource_graph_id,
            resource_ids=tuple(dict.fromkeys(resource_ids)),
            policy_revision=policy_revision,
            proposal_digest=_digest(proposal),
            proposal=dict(proposal),
        )

    def grant(self, change: StagedChange) -> ApprovalGrant:
        return ApprovalGrant(
            approval_id=f"approval-{uuid4().hex[:12]}",
            change_id=change.change_id,
            change_revision=change.revision,
            resource_graph_id=change.resource_graph_id,
            policy_revision=change.policy_revision,
            proposal_digest=change.proposal_digest,
        )

    def validate_apply(
        self,
        change: StagedChange,
        grant: ApprovalGrant,
        *,
        current_resource_graph_id: str,
        current_policy_revision: str,
        provenance: ResourceProvenanceIndex,
        bound_scope: list[str],
    ) -> ApplyCheck:
        if grant.approval_id in self._consumed:
            return ApplyCheck(False, "APPROVAL_ALREADY_CONSUMED")
        if grant.outcome != "allowed_once":
            return ApplyCheck(False, "APPROVAL_NOT_GRANTED")
        if grant.change_id != change.change_id or grant.change_revision != change.revision:
            return ApplyCheck(False, "CHANGE_REVISION_MISMATCH")
        if grant.proposal_digest != change.proposal_digest:
            return ApplyCheck(False, "CHANGE_DIGEST_MISMATCH")
        if current_resource_graph_id != change.resource_graph_id or grant.resource_graph_id != change.resource_graph_id:
            return ApplyCheck(False, "RESOURCE_GRAPH_STALE")
        if current_policy_revision != change.policy_revision or grant.policy_revision != change.policy_revision:
            return ApplyCheck(False, "POLICY_REVISION_STALE")
        provenance_check = provenance.validate(change.resource_ids, bound_scope=bound_scope)
        if not provenance_check.allowed:
            return ApplyCheck(False, provenance_check.code)
        return ApplyCheck(True, "APPLY_REVALIDATION_OK")

    def consume(self, grant: ApprovalGrant) -> None:
        if grant.approval_id in self._consumed:
            raise ValueError("approval grant already consumed")
        self._consumed.add(grant.approval_id)
