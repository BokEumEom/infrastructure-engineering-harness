"""Deterministic evidence-backed Ops review for live infrastructure bundles.

This module intentionally does not mutate infrastructure or rewrite Agent Skills.
It converts read-only evidence into review findings and explicit learning
candidates. Independent post-change evidence is required to close findings.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


STATE_RANK = {
    "healthy": 0,
    "at_risk": 1,
    "insufficient_evidence": 2,
    "acute": 3,
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _index(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in bundle.get("observations", [])}


def _scalar(observation: dict[str, Any] | None) -> float | None:
    if not observation or observation.get("status") == "unavailable":
        return None
    value = observation.get("value")
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, dict):
        return None
    result = value.get("result")
    if not isinstance(result, list) or not result:
        return None
    sample = result[0]
    raw = sample.get("value") if isinstance(sample, dict) else None
    if not isinstance(raw, list) or len(raw) < 2:
        return None
    try:
        return float(raw[1])
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _finding(
    fid: str,
    severity: str,
    observation: str,
    impact: str,
    evidence_refs: list[str],
    recommendation: str,
    verification: list[str],
) -> dict[str, Any]:
    return {
        "id": fid,
        "severity": severity,
        "observation": observation,
        "impact": impact,
        "evidence_refs": evidence_refs,
        "recommendation": recommendation,
        "verification": verification,
    }


def _deployment_env(deployments: Any, name: str) -> dict[str, str]:
    if not isinstance(deployments, list):
        return {}
    for item in deployments:
        if item.get("name") == name:
            env = item.get("operational_env")
            return env if isinstance(env, dict) else {}
    return {}


def review_ops_evidence(
    k8s_bundle: dict[str, Any],
    prometheus_bundle: dict[str, Any],
) -> dict[str, Any]:
    k8s = _index(k8s_bundle)
    prom = _index(prometheus_bundle)
    findings: list[dict[str, Any]] = []
    learning_candidates: list[dict[str, Any]] = []

    required_k8s = [
        "k8s.nodes",
        "k8s.pods",
        "k8s.deployments",
        "k8s.gateways",
        "k8s.httproutes",
        "k8s.argocd",
    ]
    required_prom = [
        "prometheus.platform_api_target_up",
        "prometheus.platform_api_error_ratio_5m",
        "prometheus.platform_api_p95_latency_5m",
        "prometheus.envoy_live",
        "prometheus.otel_failed_spans_5m",
    ]

    missing: list[str] = []
    for ref in required_k8s:
        item = k8s.get(ref)
        if not item or item.get("status") == "unavailable":
            missing.append(ref)
    for ref in required_prom:
        item = prom.get(ref)
        if not item or item.get("status") == "unavailable" or _scalar(item) is None:
            missing.append(ref)

    if missing:
        learning_candidates.append({
            "type": "evidence_gap",
            "refs": missing,
            "proposal": "repair or extend the evidence adapter/query profile before treating the review as complete",
        })

    nodes = k8s.get("k8s.nodes", {}).get("value", {})
    if isinstance(nodes, dict) and nodes.get("total"):
        total = int(nodes.get("total", 0))
        ready = int(nodes.get("ready", 0))
        if ready < total:
            findings.append(_finding(
                "cluster.nodes_not_ready", "P0",
                f"{ready}/{total} Kubernetes nodes are Ready",
                "Scheduling capacity and workload redundancy are reduced.",
                ["k8s.nodes"],
                "Identify the non-Ready node and its kubelet/runtime/network condition before rescheduling workloads.",
                ["collect a new k8s.nodes observation", "confirm all nodes Ready", "verify affected workloads recover"],
            ))

    pod_health = k8s.get("k8s.pods", {}).get("value", {})
    if isinstance(pod_health, dict) and int(pod_health.get("unhealthy_count", 0)) > 0:
        findings.append(_finding(
            "cluster.unhealthy_pods", "P1",
            f"{pod_health.get('unhealthy_count')} Pods are not Running/Ready",
            "A cluster or workload problem may be active; unhealthy Pods must be scoped before remediation.",
            ["k8s.pods"],
            "Correlate unhealthy Pod namespaces/reasons with Warning events and service telemetry.",
            ["new k8s.pods evidence shows no unexpected unhealthy Pods", "service SLI remains healthy"],
        ))

    deployments = k8s.get("k8s.deployments", {}).get("value", {}).get("items", [])
    degraded_deployments = []
    for item in deployments if isinstance(deployments, list) else []:
        desired = item.get("desired")
        ready = item.get("ready", 0)
        if desired is not None and int(ready or 0) < int(desired or 0):
            degraded_deployments.append(item.get("name"))
    if degraded_deployments:
        findings.append(_finding(
            "demo_app.deployment_unavailable", "P0",
            f"Deployments below desired Ready replicas: {', '.join(map(str, degraded_deployments))}",
            "The demo service topology has lost intended redundancy or capacity.",
            ["k8s.deployments"],
            "Inspect rollout state, Pod reasons, resource pressure and recent GitOps revision before restarting anything.",
            ["all demo-app deployments ready==desired", "Gateway request succeeds", "error ratio returns to normal"],
        ))

    active_faults: dict[str, dict[str, float]] = {}
    for deployment_name in ("web", "catalog", "orders"):
        env = _deployment_env(deployments, deployment_name)
        latency_ms = _as_float(env.get("FAULT_LATENCY_MS"))
        error_percent = _as_float(env.get("FAULT_ERROR_RATE_PERCENT"))
        if latency_ms > 0 or error_percent > 0:
            active_faults[deployment_name] = {
                "latency_ms": latency_ms,
                "error_percent": error_percent,
            }
    if active_faults:
        rendered = ", ".join(
            f"{name}(latency={values['latency_ms']:.0f}ms,error={values['error_percent']:.0f}%)"
            for name, values in sorted(active_faults.items())
        )
        findings.append(_finding(
            "demo_app.controlled_fault_enabled", "P2",
            f"Controlled fault injection is enabled: {rendered}",
            "Runtime symptoms may be intentional; incident conclusions should preserve the GitOps experiment context.",
            ["k8s.deployments"],
            "Correlate the enabled fault with service metrics/traces and remove it through GitOps for remediation.",
            ["fresh k8s.deployments evidence shows FAULT_* values returned to zero", "affected service SLI recovers"],
        ))

    argocd = k8s.get("k8s.argocd", {}).get("value", {}).get("items", [])
    unhealthy_apps = [
        item for item in argocd if item.get("sync") not in {None, "Synced"} or item.get("health") not in {None, "Healthy"}
    ] if isinstance(argocd, list) else []
    if unhealthy_apps:
        names = [f"{item.get('name')}:{item.get('sync')}/{item.get('health')}" for item in unhealthy_apps]
        findings.append(_finding(
            "gitops.application_drift", "P1",
            "Argo CD applications are not fully Synced/Healthy: " + ", ".join(names),
            "Desired state and runtime state may have diverged or reconciliation may be failing.",
            ["k8s.argocd"],
            "Inspect Argo resource conditions and the exact failed resource; do not patch the workload around GitOps ownership.",
            ["Argo CD applications report Synced/Healthy", "post-sync service SLI is healthy"],
        ))

    warning_events = k8s.get("k8s.warning_events", {}).get("value", {})
    if isinstance(warning_events, dict) and int(warning_events.get("count", 0)) > 0:
        findings.append(_finding(
            "cluster.warning_events_present", "P2",
            f"Kubernetes reports {warning_events.get('count')} Warning events in the retained event window",
            "Warnings can explain rollout, scheduling, probe, image or resource failures but may also be historical.",
            ["k8s.warning_events"],
            "Review recency and object scope; correlate only recent relevant warnings with current symptoms.",
            ["relevant Warning events cease after remediation", "service telemetry confirms recovery"],
        ))

    target_up = _scalar(prom.get("prometheus.platform_api_target_up"))
    if target_up is not None and target_up < 1:
        findings.append(_finding(
            "platform_api.metrics_target_down", "P0",
            f"platform-api Prometheus target up={target_up}",
            "The application may be unavailable or the monitoring path may be broken; either condition blocks trustworthy operations.",
            ["prometheus.platform_api_target_up"],
            "Differentiate application failure from scrape failure using Kubernetes readiness, Gateway request and Prometheus target metadata.",
            ["target up=1", "HTTPS user path succeeds", "fresh metrics advance"],
        ))

    envoy_live = _scalar(prom.get("prometheus.envoy_live"))
    if envoy_live is not None and envoy_live < 1:
        findings.append(_finding(
            "gateway.envoy_not_live", "P0",
            f"Envoy live metric={envoy_live}",
            "The shared ingress path for application and Grafana may be unavailable.",
            ["prometheus.envoy_live", "k8s.gateways"],
            "Inspect Gateway listener conditions and Envoy Pods before changing application workloads.",
            ["envoy_server_live=1", "Gateway listeners Programmed/Accepted", "HTTPS user path succeeds"],
        ))

    error_5m = _scalar(prom.get("prometheus.platform_api_error_ratio_5m"))
    error_1h = _scalar(prom.get("prometheus.platform_api_error_ratio_1h"))
    burn_5m = _scalar(prom.get("prometheus.platform_api_burn_rate_5m"))
    burn_1h = _scalar(prom.get("prometheus.platform_api_burn_rate_1h"))
    if burn_5m is not None and burn_1h is not None and burn_5m > 14.4 and burn_1h > 14.4:
        findings.append(_finding(
            "platform_api.fast_error_budget_burn", "P0",
            f"availability burn rate is {burn_5m:.2f}x over 5m and {burn_1h:.2f}x over 1h",
            "The lab 99.9% availability error budget is being consumed at paging speed.",
            ["prometheus.platform_api_burn_rate_5m", "prometheus.platform_api_burn_rate_1h"],
            "Hold risky changes and localize the failing dependency with service metrics, traces and structured logs.",
            ["both burn-rate windows fall below alert threshold", "new review contains no fast-burn finding"],
        ))
    elif error_5m is not None and error_5m >= 0.05:
        findings.append(_finding(
            "platform_api.high_error_ratio", "P0",
            f"platform-api 5m 5xx ratio is {error_5m:.2%}",
            "User-facing requests are failing at an acute rate.",
            ["prometheus.platform_api_error_ratio_5m"],
            "Use downstream service error ratios and traces to identify the dependency causing 502/5xx responses.",
            ["5m error ratio returns below threshold", "HTTPS requests succeed", "new traces show healthy dependency spans"],
        ))
    elif error_5m is not None and error_5m >= 0.01:
        findings.append(_finding(
            "platform_api.elevated_error_ratio", "P1",
            f"platform-api 5m 5xx ratio is {error_5m:.2%}",
            "Availability is degraded even if the service is not yet in acute failure.",
            ["prometheus.platform_api_error_ratio_5m", "prometheus.platform_api_error_ratio_1h"],
            "Correlate error timing with deploy revision, downstream errors and trace/log evidence.",
            ["5m and 1h error ratios return to baseline", "post-change review marks finding resolved"],
        ))

    for service in ("catalog", "orders"):
        target_ref = f"prometheus.{service}_target_up"
        error_ref = f"prometheus.{service}_error_ratio_5m"
        p95_ref = f"prometheus.{service}_p95_latency_5m"
        target = _scalar(prom.get(target_ref))
        error_ratio = _scalar(prom.get(error_ref))
        service_p95 = _scalar(prom.get(p95_ref))
        if target is not None and target < 1:
            findings.append(_finding(
                f"dependency.{service}_target_down", "P1",
                f"{service}-service scrape target up={target}",
                "A platform-api dependency or its telemetry target is unavailable.",
                [target_ref],
                "Check the dependency Deployment/Service and compare with platform-api 502/errors and trace spans.",
                ["dependency target up=1", "platform-api dependency span succeeds"],
            ))
        if error_ratio is not None and error_ratio > 0.05:
            findings.append(_finding(
                f"dependency.{service}_high_error_ratio", "P1",
                f"{service}-service 5m 5xx ratio is {error_ratio:.2%}",
                "The dependency can propagate failures into the public platform-api.",
                [error_ref],
                "Inspect dependency logs and traces before scaling or restarting; verify whether fault injection is enabled.",
                ["dependency error ratio <5%", "platform-api error ratio recovers"],
            ))
        if service_p95 is not None and service_p95 > 0.5:
            findings.append(_finding(
                f"dependency.{service}_high_p95_latency", "P1",
                f"{service}-service P95 latency is {service_p95:.3f}s",
                "The dependency is slow enough to inflate end-to-end user latency.",
                [p95_ref],
                "Inspect the dependency trace span/log duration and compare with resource saturation before scaling.",
                ["dependency P95 <500ms", "platform-api P95 returns below threshold"],
            ))

        fault = active_faults.get(service)
        symptom_refs: list[str] = []
        if error_ratio is not None and error_ratio > 0.05:
            symptom_refs.append(error_ref)
        if service_p95 is not None and service_p95 > 0.5:
            symptom_refs.append(p95_ref)
        if fault and symptom_refs:
            findings.append(_finding(
                f"dependency.{service}_fault_injection_correlated", "P1",
                f"{service}-service has an active GitOps fault profile and matching service symptoms",
                "The configured experiment is a strong causal candidate for the observed dependency degradation.",
                ["k8s.deployments", *symptom_refs],
                "Remove the FAULT_* values through GitOps, let Argo reconcile, then collect fresh metrics/traces/logs before closing the incident.",
                ["FAULT_LATENCY_MS=0 and FAULT_ERROR_RATE_PERCENT=0", "dependency SLI recovers", "ops-compare verifies recovery"],
            ))

    p95 = _scalar(prom.get("prometheus.platform_api_p95_latency_5m"))
    if p95 is not None and p95 > 0.5:
        findings.append(_finding(
            "platform_api.high_p95_latency", "P1",
            f"platform-api P95 latency is {p95:.3f}s",
            "User requests are slower than the current 500ms operational threshold.",
            ["prometheus.platform_api_p95_latency_5m"],
            "Compare catalog/orders P95 and trace child spans; scale only if CPU/HPA evidence supports saturation.",
            ["P95 <500ms", "trace latency localizes/removes the slow span", "HPA/resource evidence is normal"],
        ))

    restarts = _scalar(prom.get("prometheus.demo_restarts_1h"))
    if restarts is not None and restarts > 0:
        findings.append(_finding(
            "demo_app.restarts", "P1",
            f"demo-app containers restarted {restarts:.0f} times in the last hour",
            "Restarts may indicate OOM, probe, process or rollout instability.",
            ["prometheus.demo_restarts_1h", "k8s.pods", "k8s.warning_events"],
            "Inspect last termination reason and Warning events before changing memory or probes.",
            ["restart increase remains zero over a new observation window", "no relevant Warning events"],
        ))

    oom = _scalar(prom.get("prometheus.oomkilled_containers"))
    if oom is not None and oom > 0:
        findings.append(_finding(
            "cluster.oomkilled", "P1",
            f"OOMKilled container metric reports {oom:.0f}",
            "Memory limits or workload behavior have caused hard container termination.",
            ["prometheus.oomkilled_containers"],
            "Identify the exact container and compare working set against request/limit before resizing.",
            ["no new OOMKilled termination", "memory headroom is observable after change"],
        ))

    hpa_saturation = _scalar(prom.get("prometheus.demo_hpa_saturation"))
    if hpa_saturation is not None and hpa_saturation >= 1:
        findings.append(_finding(
            "demo_app.hpa_saturated", "P1",
            "At least one demo-app HPA desires its configured max replicas",
            "The workload may have no remaining horizontal scaling headroom.",
            ["prometheus.demo_hpa_saturation", "k8s.hpa"],
            "Check request rate, CPU, latency and node capacity before increasing max replicas.",
            ["HPA desired/max <1", "latency/error SLI healthy", "node capacity remains adequate"],
        ))

    failed_spans = _scalar(prom.get("prometheus.otel_failed_spans_5m"))
    refused_spans = _scalar(prom.get("prometheus.otel_refused_spans_5m"))
    if (failed_spans is not None and failed_spans > 0) or (refused_spans is not None and refused_spans > 0):
        findings.append(_finding(
            "observability.trace_pipeline_loss", "P1",
            f"OTel failed spans/s={failed_spans or 0:.3f}, refused spans/s={refused_spans or 0:.3f}",
            "Distributed tracing evidence is incomplete and incident localization can be misleading.",
            ["prometheus.otel_failed_spans_5m", "prometheus.otel_refused_spans_5m"],
            "Inspect Collector exporter/receiver health and Tempo reachability; do not treat missing traces as application recovery.",
            ["failed/refused span rates return to zero", "fresh multi-service trace is visible"],
        ))

    if missing:
        state = "insufficient_evidence"
        release_guidance = "insufficient_evidence"
    elif any(item["severity"] == "P0" for item in findings):
        state = "acute"
        release_guidance = "hold"
    elif any(item["severity"] == "P1" for item in findings):
        state = "at_risk"
        release_guidance = "continue"
    else:
        state = "healthy"
        release_guidance = "continue"

    if findings:
        repeated_domains = sorted({item["id"].split(".", 1)[0] for item in findings})
        learning_candidates.append({
            "type": "review_feedback",
            "domains": repeated_domains,
            "proposal": "if these findings persist across independent runs, review runbook/context/skill coverage with context-backpass rather than silently changing policy",
        })

    return {
        "schema_version": "1.0",
        "review_id": f"ops-review:{_now()}",
        "reviewed_at": _now(),
        "state": state,
        "release_guidance": release_guidance,
        "evidence": {
            "kubernetes_bundle": k8s_bundle.get("bundle_id"),
            "kubernetes_observed_at": k8s_bundle.get("observed_at"),
            "prometheus_bundle": prometheus_bundle.get("bundle_id"),
            "prometheus_observed_at": prometheus_bundle.get("observed_at"),
            "missing_required": missing,
        },
        "findings": findings,
        "learning_candidates": learning_candidates,
    }


def compare_ops_reviews(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_findings = {item["id"]: item for item in before.get("findings", [])}
    after_findings = {item["id"]: item for item in after.get("findings", [])}

    resolved = sorted(set(before_findings) - set(after_findings))
    persistent = sorted(set(before_findings) & set(after_findings))
    new = sorted(set(after_findings) - set(before_findings))

    before_state = str(before.get("state", "insufficient_evidence"))
    after_state = str(after.get("state", "insufficient_evidence"))
    before_rank = STATE_RANK.get(before_state, 2)
    after_rank = STATE_RANK.get(after_state, 2)

    persistent_blocking = sorted(
        fid for fid in persistent
        if after_findings.get(fid, {}).get("severity") in {"P0", "P1"}
    )
    new_blocking = sorted(
        fid for fid in new
        if after_findings.get(fid, {}).get("severity") in {"P0", "P1"}
    )

    learning_candidates: list[dict[str, Any]] = []
    if persistent_blocking:
        learning_candidates.append({
            "type": "persistent_finding",
            "finding_ids": persistent_blocking,
            "proposal": "review whether the runbook, implementation capability, evidence query or remediation hypothesis is insufficient",
        })
    if new_blocking:
        learning_candidates.append({
            "type": "regression",
            "finding_ids": new_blocking,
            "proposal": "treat new post-change P0/P1 findings as regression evidence and reopen the change review",
        })

    return {
        "schema_version": "1.0",
        "compared_at": _now(),
        "before": {"review_id": before.get("review_id"), "state": before_state},
        "after": {"review_id": after.get("review_id"), "state": after_state},
        "resolved": resolved,
        "persistent": persistent,
        "new": new,
        "persistent_blocking": persistent_blocking,
        "new_blocking": new_blocking,
        "improved": after_rank < before_rank and not new_blocking,
        "regressed": after_rank > before_rank or bool(new_blocking),
        "verified_recovery": bool(resolved) and not persistent_blocking and not new_blocking and after_state == "healthy",
        "learning_candidates": learning_candidates,
    }
