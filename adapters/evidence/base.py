"""Provider-neutral evidence adapter normalization.

Adapter output is an observation bundle. Normalization preserves provenance but
never marks observations as independently verified facts; Engineering Loops own
that promotion after environment/tool/human/test verification.
"""
from __future__ import annotations

from typing import Any


def normalize_adapter_result(result: dict[str, Any], *, bundle_id: str | None = None) -> dict[str, Any]:
    if result.get("collection_mode") != "read_only":
        raise ValueError("evidence adapters must collect in read_only mode")
    observations = result.get("observations") or []
    if not observations:
        raise ValueError("adapter result must contain observations")

    normalized: list[dict[str, Any]] = []
    for observation in observations:
        provenance = observation.get("provenance") or {}
        if not provenance.get("reference"):
            raise ValueError(f"observation {observation.get('id')} lacks provenance.reference")
        item = dict(observation)
        item.setdefault("observed_at", result["observed_at"])
        normalized.append(item)

    return {
        "schema_version": "1.0",
        "bundle_id": bundle_id or f"adapter:{result['adapter_id']}:{result['observed_at']}",
        "observed_at": result["observed_at"],
        "observations": normalized,
    }
