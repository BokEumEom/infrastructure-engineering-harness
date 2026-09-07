"""Learning-candidate boundary for semantic memory extraction."""
from __future__ import annotations

from typing import Any
from uuid import uuid4


ALLOWED_TARGET_TYPES = {
    "incident",
    "runbook",
    "adr_candidate",
    "policy_candidate",
    "eval_candidate",
    "measurement",
    "service_catalog_candidate",
}


def semantic_memory_to_learning_candidate(
    *,
    claim: str,
    run_id: str,
    source_ref: str,
    owner: str,
    target_type: str = "eval_candidate",
    loop_id: str = "semantic-memory-extraction",
    service: str | None = None,
) -> dict[str, Any]:
    """Turn an extracted operational pattern into a proposal, never durable truth.

    The extraction layer is allowed to suggest a procedure/lesson. It is not allowed to
    promote repeated conversation content directly into policy, runbook truth, or a
    verified fact.
    """
    if not claim.strip():
        raise ValueError("claim is required")
    if target_type not in ALLOWED_TARGET_TYPES:
        raise ValueError("unsupported knowledge target type")
    return {
        "schema_version": "1.0",
        "candidate_id": f"candidate-{uuid4().hex[:12]}",
        "epistemic_class": "procedure",
        "claim": claim.strip(),
        "status": "proposed",
        "confidence": None,
        "source": {
            "loop_id": loop_id,
            "run_id": run_id,
            "service": service,
        },
        "evidence": {
            "supporting": [source_ref],
            "contradicting": [],
        },
        "target": {
            "type": target_type,
            "path_hint": None,
        },
        "governance": {
            "review_required": True,
            "owner": owner,
            "expires_at": None,
        },
    }
