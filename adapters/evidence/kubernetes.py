"""Read-only Kubernetes evidence adapter for Infrastructure Engineering Agent."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import shutil
import subprocess
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _kubectl_base(context: str | None) -> list[str]:
    cmd = ["kubectl"]
    if context:
        cmd.extend(["--context", context])
    return cmd


def _run(cmd: list[str], *, timeout: int = 15) -> tuple[str | None, str | None]:
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if result.returncode != 0:
        return None, (result.stderr or result.stdout or f"exit={result.returncode}").strip()
    return result.stdout, None


def _json(cmd: list[str], *, timeout: int = 15) -> tuple[dict[str, Any] | None, str | None]:
    stdout, error = _run(cmd, timeout=timeout)
    if error:
        return None, error
    try:
        return json.loads(stdout or "{}"), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def _condition_map(conditions: list[dict[str, Any]] | None) -> dict[str, str]:
    return {str(item.get("type")): str(item.get("status")) for item in conditions or []}


def _obs(
    oid: str,
    *,
    component: str,
    signal: str,
    value: Any,
    reference: str,
    source_type: str = "status",
    status: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": oid,
        "source_type": source_type,
        "source": "kubernetes",
        "component": component,
        "signal": signal,
        "value": value,
        "provenance": {"reference": reference},
    }
    if status:
        item["status"] = status
    return item


def _error_obs(oid: str, *, component: str, signal: str, reference: str, error: str) -> dict[str, Any]:
    return _obs(
        oid,
        component=component,
        signal=signal,
        value={"error": error},
        reference=reference,
        source_type="status",
        status="unavailable",
    )


def collect_kubernetes_evidence(*, namespace: str = "demo-app", context: str | None = None) -> dict[str, Any]:
    """Collect a bounded, read-only Kubernetes evidence bundle.

    The adapter intentionally summarizes operational state rather than returning
    full manifests. It never performs mutating kubectl operations.
    """
    if shutil.which("kubectl") is None:
        raise RuntimeError("kubectl is required for Kubernetes evidence collection")

    observed_at = _now()
    base = _kubectl_base(context)
    observations: list[dict[str, Any]] = []

    context_cmd = base + ["config", "current-context"]
    current_context, context_error = _run(context_cmd)
    resolved_context = (current_context or context or "unknown").strip()
    if context_error:
        observations.append(_error_obs(
            "k8s.context", component="cluster", signal="current_context",
            reference=" ".join(context_cmd), error=context_error,
        ))
    else:
        observations.append(_obs(
            "k8s.context", component="cluster", signal="current_context",
            value=resolved_context, reference=" ".join(context_cmd), source_type="configuration",
        ))

    version_cmd = base + ["version", "-o", "json"]
    version, error = _json(version_cmd)
    if error:
        observations.append(_error_obs(
            "k8s.version", component="cluster", signal="version",
            reference=" ".join(version_cmd), error=error,
        ))
    else:
        observations.append(_obs(
            "k8s.version", component="cluster", signal="version",
            value=version, reference=" ".join(version_cmd), source_type="configuration",
        ))

    nodes_cmd = base + ["get", "nodes", "-o", "json"]
    nodes, error = _json(nodes_cmd)
    if error:
        observations.append(_error_obs(
            "k8s.nodes", component="cluster", signal="node_health",
            reference=" ".join(nodes_cmd), error=error,
        ))
    else:
        node_items = (nodes or {}).get("items", [])
        summary = []
        ready_count = 0
        for node in node_items:
            conditions = _condition_map(node.get("status", {}).get("conditions"))
            ready = conditions.get("Ready") == "True"
            ready_count += int(ready)
            summary.append({
                "name": node.get("metadata", {}).get("name"),
                "ready": ready,
                "kubeletVersion": node.get("status", {}).get("nodeInfo", {}).get("kubeletVersion"),
                "unschedulable": bool(node.get("spec", {}).get("unschedulable", False)),
            })
        observations.append(_obs(
            "k8s.nodes", component="cluster", signal="node_health",
            value={"total": len(summary), "ready": ready_count, "nodes": summary},
            reference=" ".join(nodes_cmd), source_type="runtime",
            status="healthy" if ready_count == len(summary) and summary else "degraded",
        ))

    pods_cmd = base + ["get", "pods", "-A", "-o", "json"]
    pods, error = _json(pods_cmd)
    if error:
        observations.append(_error_obs(
            "k8s.pods", component="cluster", signal="pod_health",
            reference=" ".join(pods_cmd), error=error,
        ))
    else:
        pod_items = (pods or {}).get("items", [])
        unhealthy: list[dict[str, Any]] = []
        total_restarts = 0
        namespace_counts: dict[str, int] = {}
        for pod in pod_items:
            meta = pod.get("metadata", {})
            status_obj = pod.get("status", {})
            ns = str(meta.get("namespace", "default"))
            namespace_counts[ns] = namespace_counts.get(ns, 0) + 1
            statuses = status_obj.get("containerStatuses") or []
            restarts = sum(int(c.get("restartCount", 0)) for c in statuses)
            total_restarts += restarts
            ready = all(bool(c.get("ready")) for c in statuses) if statuses else status_obj.get("phase") == "Succeeded"
            if status_obj.get("phase") not in {"Running", "Succeeded"} or not ready:
                unhealthy.append({
                    "namespace": ns,
                    "name": meta.get("name"),
                    "phase": status_obj.get("phase"),
                    "restarts": restarts,
                    "reason": status_obj.get("reason"),
                })
        observations.append(_obs(
            "k8s.pods", component="cluster", signal="pod_health",
            value={
                "total": len(pod_items),
                "unhealthy": unhealthy[:50],
                "unhealthy_count": len(unhealthy),
                "total_restarts": total_restarts,
                "namespace_counts": namespace_counts,
            },
            reference=" ".join(pods_cmd), source_type="runtime",
            status="healthy" if not unhealthy else "degraded",
        ))

    ns_cmd = base + ["get", "namespace", namespace, "-o", "json"]
    ns_data, error = _json(ns_cmd)
    if error:
        observations.append(_error_obs(
            "k8s.namespace", component=namespace, signal="namespace_policy",
            reference=" ".join(ns_cmd), error=error,
        ))
    else:
        observations.append(_obs(
            "k8s.namespace", component=namespace, signal="namespace_policy",
            value={
                "labels": (ns_data or {}).get("metadata", {}).get("labels", {}),
                "phase": (ns_data or {}).get("status", {}).get("phase"),
            },
            reference=" ".join(ns_cmd), source_type="configuration",
        ))

    for resource, oid, signal in (
        ("deployments", "k8s.deployments", "deployment_health"),
        ("horizontalpodautoscalers", "k8s.hpa", "autoscaling"),
        ("poddisruptionbudgets", "k8s.pdb", "disruption_budget"),
        ("networkpolicies", "k8s.networkpolicy", "network_isolation"),
        ("serviceaccounts", "k8s.serviceaccounts", "service_accounts"),
    ):
        cmd = base + ["get", resource, "-n", namespace, "-o", "json"]
        data, error = _json(cmd)
        if error:
            observations.append(_error_obs(
                oid, component=namespace, signal=signal, reference=" ".join(cmd), error=error,
            ))
            continue
        items = (data or {}).get("items", [])
        summaries: list[dict[str, Any]] = []
        for item in items:
            meta = item.get("metadata", {})
            spec = item.get("spec", {})
            status_obj = item.get("status", {})
            entry: dict[str, Any] = {"name": meta.get("name")}
            if resource == "deployments":
                entry.update({
                    "desired": spec.get("replicas"),
                    "ready": status_obj.get("readyReplicas", 0),
                    "available": status_obj.get("availableReplicas", 0),
                    "updated": status_obj.get("updatedReplicas", 0),
                })
            elif resource == "horizontalpodautoscalers":
                entry.update({
                    "min": spec.get("minReplicas"),
                    "max": spec.get("maxReplicas"),
                    "current": status_obj.get("currentReplicas"),
                    "desired": status_obj.get("desiredReplicas"),
                    "conditions": _condition_map(status_obj.get("conditions")),
                })
            elif resource == "poddisruptionbudgets":
                entry.update({
                    "currentHealthy": status_obj.get("currentHealthy"),
                    "desiredHealthy": status_obj.get("desiredHealthy"),
                    "disruptionsAllowed": status_obj.get("disruptionsAllowed"),
                })
            elif resource == "networkpolicies":
                entry.update({"policyTypes": spec.get("policyTypes", [])})
            elif resource == "serviceaccounts":
                entry.update({"automountServiceAccountToken": item.get("automountServiceAccountToken")})
            summaries.append(entry)
        observations.append(_obs(
            oid, component=namespace, signal=signal,
            value={"count": len(summaries), "items": summaries},
            reference=" ".join(cmd), source_type="configuration" if resource in {"networkpolicies", "serviceaccounts"} else "status",
        ))

    warning_cmd = base + ["get", "events", "-A", "--field-selector", "type=Warning", "-o", "json"]
    events, error = _json(warning_cmd)
    if error:
        observations.append(_error_obs(
            "k8s.warning_events", component="cluster", signal="warning_events",
            reference=" ".join(warning_cmd), error=error,
        ))
    else:
        event_items = (events or {}).get("items", [])

        def _event_time(item: dict[str, Any]) -> str:
            return str(item.get("eventTime") or item.get("lastTimestamp") or item.get("metadata", {}).get("creationTimestamp") or "")

        event_items.sort(key=_event_time, reverse=True)
        compact = [{
            "namespace": item.get("metadata", {}).get("namespace"),
            "reason": item.get("reason"),
            "object": f"{item.get('involvedObject', {}).get('kind')}/{item.get('involvedObject', {}).get('name')}",
            "message": item.get("message"),
            "time": _event_time(item),
        } for item in event_items[:25]]
        observations.append(_obs(
            "k8s.warning_events", component="cluster", signal="warning_events",
            value={"count": len(event_items), "recent": compact},
            reference=" ".join(warning_cmd), source_type="runtime",
            status="healthy" if not event_items else "attention",
        ))

    for resource, oid, component, signal in (
        ("gateways.gateway.networking.k8s.io", "k8s.gateways", "gateway-api", "gateway_status"),
        ("httproutes.gateway.networking.k8s.io", "k8s.httproutes", "gateway-api", "route_status"),
        ("applications.argoproj.io", "k8s.argocd", "argocd", "application_status"),
    ):
        cmd = base + ["get", resource, "-A", "-o", "json"]
        data, error = _json(cmd)
        if error:
            observations.append(_error_obs(
                oid, component=component, signal=signal, reference=" ".join(cmd), error=error,
            ))
            continue
        items = (data or {}).get("items", [])
        compact: list[dict[str, Any]] = []
        for item in items:
            meta = item.get("metadata", {})
            status_obj = item.get("status", {})
            entry: dict[str, Any] = {"namespace": meta.get("namespace"), "name": meta.get("name")}
            if resource.startswith("applications"):
                entry.update({
                    "sync": status_obj.get("sync", {}).get("status"),
                    "health": status_obj.get("health", {}).get("status"),
                    "revision": status_obj.get("sync", {}).get("revision"),
                })
            else:
                entry["conditions"] = _condition_map(status_obj.get("conditions"))
                if resource.startswith("gateways"):
                    entry["listeners"] = [{
                        "name": listener.get("name"),
                        "attachedRoutes": listener.get("attachedRoutes"),
                        "conditions": _condition_map(listener.get("conditions")),
                    } for listener in status_obj.get("listeners", [])]
                else:
                    entry["parents"] = [{
                        "sectionName": parent.get("parentRef", {}).get("sectionName"),
                        "conditions": _condition_map(parent.get("conditions")),
                    } for parent in status_obj.get("parents", [])]
            compact.append(entry)
        observations.append(_obs(
            oid, component=component, signal=signal,
            value={"count": len(compact), "items": compact},
            reference=" ".join(cmd), source_type="status",
        ))

    top_nodes_cmd = base + ["top", "nodes", "--no-headers"]
    top_nodes, top_nodes_error = _run(top_nodes_cmd)
    observations.append(
        _error_obs(
            "k8s.top_nodes", component="cluster", signal="node_utilization",
            reference=" ".join(top_nodes_cmd), error=top_nodes_error,
        ) if top_nodes_error else _obs(
            "k8s.top_nodes", component="cluster", signal="node_utilization",
            value={"rows": [line for line in (top_nodes or "").splitlines() if line.strip()]},
            reference=" ".join(top_nodes_cmd), source_type="usage",
        )
    )

    top_pods_cmd = base + ["top", "pods", "-A", "--no-headers"]
    top_pods, top_pods_error = _run(top_pods_cmd)
    observations.append(
        _error_obs(
            "k8s.top_pods", component="cluster", signal="pod_utilization",
            reference=" ".join(top_pods_cmd), error=top_pods_error,
        ) if top_pods_error else _obs(
            "k8s.top_pods", component="cluster", signal="pod_utilization",
            value={"rows": [line for line in (top_pods or "").splitlines() if line.strip()]},
            reference=" ".join(top_pods_cmd), source_type="usage",
        )
    )

    return {
        "schema_version": "1.0",
        "adapter_id": "kubernetes-kubectl",
        "observed_at": observed_at,
        "collection_mode": "read_only",
        "scope": {"context": resolved_context, "namespace": namespace},
        "observations": observations,
    }
