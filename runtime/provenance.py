"""Resource provenance gates for mutation-capable runtime actions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ProvenanceCheck:
    allowed: bool
    code: str
    missing: tuple[str, ...] = ()
    outside_scope: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResourceProvenanceIndex:
    """Resources actually discovered by a trusted adapter for one graph snapshot."""

    graph_id: str
    resource_ids: frozenset[str]

    @classmethod
    def from_resource_graph(cls, graph: dict[str, Any]) -> "ResourceProvenanceIndex":
        return cls(
            graph_id=graph["graph_id"],
            resource_ids=frozenset(item["id"] for item in graph.get("resources", [])),
        )

    def validate(
        self,
        target_resource_ids: Iterable[str],
        *,
        bound_scope: Iterable[str] | None = None,
    ) -> ProvenanceCheck:
        targets = tuple(dict.fromkeys(target_resource_ids))
        if not targets:
            return ProvenanceCheck(False, "RESOURCE_TARGET_REQUIRED")

        missing = tuple(sorted(set(targets) - self.resource_ids))
        scope = set(bound_scope) if bound_scope is not None else None
        outside = tuple(sorted(set(targets) - scope)) if scope is not None else ()

        if missing:
            return ProvenanceCheck(False, "RESOURCE_NOT_DISCOVERED", missing=missing)
        if outside:
            return ProvenanceCheck(False, "RESOURCE_OUTSIDE_BOUND_SCOPE", outside_scope=outside)
        return ProvenanceCheck(True, "RESOURCE_PROVENANCE_OK")
