"""Provider-neutral backend contract for the Infrastructure Engineering Agent.

The model reasons over normalized results. Credentials, authorization and platform-specific
mutation stay behind this interface.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class InfrastructureEngineeringBackend(ABC):
    """Integration boundary between the agent runtime and infrastructure systems.

    Reads are provider-specific but normalized before the model consumes them.
    Production writes are staged first. Applying a change is a separate operation and
    requires independently owned approval state outside model prose.
    """

    @abstractmethod
    async def discover_resources(self, scope: dict[str, Any]) -> dict[str, Any]:
        """Return a provider-neutral Resource Graph fragment with discovery provenance."""

    @abstractmethod
    async def collect_evidence(
        self, resource_ids: list[str], query: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Return timestamped read-only observations with source provenance."""

    @abstractmethod
    async def get_recent_changes(
        self, resource_ids: list[str], window: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Return deployment/configuration/change records relevant to the scope."""

    @abstractmethod
    async def stage_change(
        self,
        proposal: dict[str, Any],
        *,
        resource_graph_id: str,
        resource_ids: list[str],
        policy_revision: str,
    ) -> dict[str, Any]:
        """Create a revisioned, reviewable change record without mutating production.

        The target resources must already be present in trusted discovery provenance.
        """

    @abstractmethod
    async def get_pending_changes(self) -> list[dict[str, Any]]:
        """Return staged changes visible to the current principal/session."""

    @abstractmethod
    async def apply_approved_change(
        self,
        change_id: str,
        *,
        expected_revision: int,
    ) -> dict[str, Any]:
        """Apply only the exact staged revision independently approved by the host/runtime.

        Implementations must revalidate resource provenance, policy revision and the
        staged change revision immediately before execution.
        """

    @abstractmethod
    async def verify_outcome(
        self, change_id: str | None, objective: dict[str, Any]
    ) -> dict[str, Any]:
        """Collect current independent evidence for the claimed engineering outcome."""
