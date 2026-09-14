"""Deterministic HPA/ResourceQuota capacity review for the reference environment."""
from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Any


def _parse_time(raw: Any) -> datetime | None:
    value = str(raw or "").strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _observations(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in bundle.get("observations", []) if isinstance(item, dict)}


def _item_by_name(observation: dict[str, Any] | None, name: str) -> dict[str, Any] | None:
    value = (observation or {}).get("value")
    if not isinstance(value, dict):
        return None
    for item in value.get("items") or []:
        if isinstance(item, dict) and item.get("name") == name:
            return item
    return None


def _recent_quota_warnings(
    warning_observation: dict[str, Any] | None,
    *,
    observed_at: datetime,
    max_age_seconds: int,
    workload_prefix: str,
) -> list[dict[str, Any]]:
    value = (warning_observation or {}).get("value")
    if not isinstance(value, dict):
        return []
    recent: list[dict[str, Any]] = []
    for event in value.get("recent") or []:
        if not isinstance(event, dict):
            continue
        message = str(event.get("message") or "")
        obj = str(event.get("object") or "")
        if "exceeded quota" not in message.lower():
            continue
        if workload_prefix and workload_prefix not in obj and workload_prefix not in message:
            continue
        event_time = _parse_time(event.get("time"))
        if event_time is None:
            continue
        age = (observed_at - event_time.astimezone(timezone.utc)).total_seconds()
        if 0 <= age <= max_age_seconds:
            recent.append(event)
    return recent


def _quota_cpu_limit(events: list[dict[str, Any]]) -> str | None:
    for event in events:
        message = str(event.get("message") or "")
        match = re.search(r"limited:\s*[^\n]*requests\.cpu=([^,\s]+)", message)
        if match:
            return match.group(1)
    return None


def review_capacity_evidence(
    k8s_bundle: dict[str, Any],
    *,
    workload: str = "web",
    target_hpa_max: int = 8,
    target_requests_cpu: str = "2",
    warning_max_age_seconds: int = 900,
) -> dict[str, Any]:
    """Correlate HPA saturation with recent quota-rejection evidence.

    This reviewer is intentionally bounded to capacity diagnosis/proposal. It does
    not mutate Kubernetes, Git, Terraform, or approval state.
    """
    observed_at = _parse_time(k8s_bundle.get("observed_at")) or datetime.now(timezone.utc)
    indexed = _observations(k8s_bundle)
    hpa = _item_by_name(indexed.get("k8s.hpa"), workload)
    deployment = _item_by_name(indexed.get("k8s.deployments"), workload)
    warnings = _recent_quota_warnings(
        indexed.get("k8s.warning_events"),
        observed_at=observed_at,
        max_age_seconds=warning_max_age_seconds,
        workload_prefix=f"{workload}-",
    )

    findings: list[dict[str, Any]] = []
    hpa_limited = False
    if hpa:
        conditions = hpa.get("conditions") if isinstance(hpa.get("conditions"), dict) else {}
        hpa_limited = conditions.get("ScalingLimited") == "True"
        at_max = hpa.get("current") is not None and hpa.get("max") is not None and int(hpa.get("current") or 0) >= int(hpa.get("max") or 0)
        if hpa_limited or at_max:
            findings.append({
                "id": f"capacity.{workload}_hpa_saturated",
                "severity": "P1",
                "observation": (
                    f"{workload} HPA current={hpa.get('current')} desired={hpa.get('desired')} max={hpa.get('max')} "
                    f"ScalingLimited={conditions.get('ScalingLimited')}"
                ),
                "evidence_refs": ["k8s.hpa"],
            })

    quota_limit = _quota_cpu_limit(warnings)
    if warnings:
        findings.append({
            "id": "capacity.resource_quota_blocking_scaleout",
            "severity": "P1",
            "observation": f"Recent Kubernetes FailedCreate events show ResourceQuota blocking scale-out; requests.cpu limit={quota_limit or 'observed in event'}",
            "evidence_refs": ["k8s.warning_events"],
        })

    correlated = bool(hpa_limited and warnings)
    if correlated:
        findings.append({
            "id": f"capacity.{workload}_hpa_quota_correlated",
            "severity": "P1",
            "observation": "HPA scale-out is limited while recent Pod creation is rejected by ResourceQuota",
            "evidence_refs": ["k8s.hpa", "k8s.warning_events", "k8s.deployments"],
        })

    proposal = None
    if correlated:
        current_max = int(hpa.get("max") or 0) if hpa else 0
        proposal = {
            "schema_version": "1.0",
            "proposal_type": "capacity_remediation",
            "intent": "restore scale-out headroom without bypassing GitOps or Terraform ownership",
            "target": workload,
            "changes": [
                {
                    "owner": "terraform",
                    "resource": "ResourceQuota/demo-app-capacity",
                    "field": "spec.hard.requests.cpu",
                    "from": quota_limit,
                    "to": target_requests_cpu,
                },
                {
                    "owner": "gitops",
                    "resource": f"HorizontalPodAutoscaler/{workload}",
                    "field": "spec.maxReplicas",
                    "from": current_max,
                    "to": target_hpa_max,
                },
            ],
            "risk_inputs": {
                "destructive": False,
                "privilege_expansion": False,
                "public_exposure": False,
                "capacity_increase": True,
                "cost_implication": True,
                "ownership_domains": ["terraform", "gitops"],
            },
            "post_checks": [
                f"{workload} HPA is no longer ScalingLimited",
                "no fresh exceeded-quota FailedCreate events",
                "application HTTPS path remains healthy",
                "fresh Ops review contains no new blocking findings",
            ],
            "rollback": [
                f"restore HorizontalPodAutoscaler/{workload} maxReplicas={current_max} through GitOps",
                "restore Terraform ResourceQuota to the pre-change approved baseline",
                "re-run fresh capacity and Ops evidence",
            ],
        }

    state = "at_risk" if findings else "healthy"
    if correlated and deployment and int(deployment.get("ready") or 0) < int(deployment.get("desired") or 0):
        state = "acute"

    return {
        "schema_version": "1.0",
        "review_type": "capacity",
        "observed_at": observed_at.isoformat(),
        "state": state,
        "workload": workload,
        "findings": findings,
        "proposal": proposal,
        "evidence_summary": {
            "hpa": hpa,
            "deployment": deployment,
            "recent_quota_warning_count": len(warnings),
            "quota_requests_cpu_limit": quota_limit,
        },
    }
