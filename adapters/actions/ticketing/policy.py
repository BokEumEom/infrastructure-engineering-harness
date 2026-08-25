"""Provider-neutral ticket policy and deduplication helpers.

Network writes are intentionally not implemented here. Jira and Linear writes are
performed by connected MCP servers after this policy layer returns an allowed action.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def ticket_fingerprint(request: dict[str, Any]) -> str:
    """Return a stable provider-scoped deduplication fingerprint."""
    identity = {
        "provider": _norm(request.get("provider")),
        "source_ref": _norm(request.get("source_ref")),
        "service": _norm(request.get("service")),
        "kind": _norm(request.get("kind")),
    }
    canonical = json.dumps(identity, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _rule_matches(request: dict[str, Any], when: dict[str, Any]) -> bool:
    scalar_checks = {
        "providers": _norm(request.get("provider")),
        "kinds": _norm(request.get("kind")),
        "severities": _norm(request.get("severity")),
        "risks": _norm(request.get("risk")),
    }
    for field, actual in scalar_checks.items():
        expected = when.get(field)
        if expected and actual not in {_norm(v) for v in expected}:
            return False

    expected_domains = {_norm(v) for v in when.get("domains", [])}
    if expected_domains:
        request_domains = {_norm(v) for v in request.get("domains", [])}
        if not expected_domains.intersection(request_domains):
            return False
    return True


def evaluate_ticket_policy(request: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Return action, reason, matched rule, evidence status and fingerprint."""
    mode = policy.get("mode", "manual")
    fingerprint = ticket_fingerprint(request)

    if mode == "disabled":
        return {"action": "disabled", "reason": "ticketing policy is disabled", "rule_id": None, "fingerprint": fingerprint}
    if mode == "manual":
        return {"action": "manual", "reason": "ticketing requires explicit user action", "rule_id": None, "fingerprint": fingerprint}

    for rule in policy.get("rules", []):
        if not _rule_matches(request, rule.get("when", {})):
            continue
        evidence = request.get("evidence_refs", [])
        min_evidence = int(rule.get("min_evidence", 1))
        if rule.get("require_evidence", True) and len(evidence) < min_evidence:
            return {
                "action": "manual",
                "reason": f"rule {rule['id']} matched but evidence is insufficient",
                "rule_id": rule["id"],
                "fingerprint": fingerprint,
            }
        return {
            "action": rule["action"],
            "reason": f"matched policy rule {rule['id']}",
            "rule_id": rule["id"],
            "fingerprint": fingerprint,
        }

    return {
        "action": policy.get("default_action", "manual"),
        "reason": "no policy rule matched",
        "rule_id": None,
        "fingerprint": fingerprint,
    }
