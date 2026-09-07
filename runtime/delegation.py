"""Optional specialist delegation without authority expansion."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DelegationRequest:
    delegate_id: str
    purpose: str
    allowed_capabilities: tuple[str, ...]
    allowed_resource_ids: tuple[str, ...]
    read_only: bool = True


@dataclass(frozen=True)
class DelegationResult:
    delegate_id: str
    assessment: dict[str, Any]
    discovered_resource_ids: tuple[str, ...] = ()


def validate_delegation(
    request: DelegationRequest,
    *,
    parent_capabilities: set[str],
    parent_resource_scope: set[str],
) -> None:
    """Ensure delegation narrows or preserves the parent's authority.

    Delegation is a scaling mechanism, not an authorization mechanism. A specialist may
    analyze a narrower domain but cannot gain write authority or expand resource scope.
    """
    if not request.read_only:
        raise PermissionError("specialist delegation is read-only by default")
    if not set(request.allowed_capabilities).issubset(parent_capabilities):
        raise PermissionError("delegate capabilities exceed parent authority")
    if not set(request.allowed_resource_ids).issubset(parent_resource_scope):
        raise PermissionError("delegate resource scope exceeds parent authority")


def merge_delegate_result(
    result: DelegationResult,
    *,
    mutation_eligible_resource_ids: set[str],
) -> set[str]:
    """Return the unchanged mutation-eligible set.

    A delegate may discover identifiers for investigation, but its output cannot grant
    production mutation eligibility. Trusted resource discovery must establish that.
    """
    _ = result
    return set(mutation_eligible_resource_ids)
