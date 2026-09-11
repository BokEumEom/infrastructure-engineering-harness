from __future__ import annotations

import unittest

from runtime.ops_review import compare_ops_reviews, review_ops_evidence


def prom_obs(
    oid: str,
    value: float,
    *,
    component: str | None = None,
    signal: str | None = None,
):
    inferred_component = component or "test"
    inferred_signal = signal or oid
    return {
        "id": oid,
        "source_type": "metrics",
        "source": "prometheus",
        "component": inferred_component,
        "signal": inferred_signal,
        "status": "observed",
        "value": {
            "resultType": "vector",
            "result": [{"metric": {}, "value": [1, str(value)]}],
        },
        "provenance": {"reference": "http://prometheus/api/v1/query", "query": oid},
    }


def service_obs(prefix: str, component: str, *, target: float = 1, error: float = 0, p95: float = 0.05):
    return [
        prom_obs(f"prometheus.{prefix}_target_up", target, component=component, signal="target_up"),
        prom_obs(f"prometheus.{prefix}_error_ratio_5m", error, component=component, signal="error_ratio_5m"),
        prom_obs(
            f"prometheus.{prefix}_p95_latency_5m",
            p95,
            component=component,
            signal="p95_latency_seconds_5m",
        ),
    ]


def k8s_obs(oid: str, value, status: str = "healthy"):
    return {
        "id": oid,
        "source_type": "status",
        "source": "kubernetes",
        "component": "test",
        "signal": oid,
        "status": status,
        "value": value,
        "provenance": {"reference": f"kubectl get {oid}"},
    }


def deployment(name: str, role: str, *, service_name: str | None = None):
    operational_env = {
        "SERVICE_ROLE": role,
        "FAULT_LATENCY_MS": "0",
        "FAULT_ERROR_RATE_PERCENT": "0",
    }
    if service_name:
        operational_env["OTEL_SERVICE_NAME"] = service_name
    return {
        "name": name,
        "desired": 2,
        "ready": 2,
        "operational_env": operational_env,
    }


def healthy_bundles(*, expanded: bool = False):
    deployments = [
        deployment("web", "gateway", service_name="platform-api"),
        deployment("catalog", "catalog", service_name="catalog-service"),
        deployment("orders", "orders", service_name="orders-service"),
    ]
    dependency_observations = [
        *service_obs("catalog", "catalog-service", p95=0.04),
        *service_obs("orders", "orders-service", p95=0.05),
    ]

    if expanded:
        deployments.extend([
            deployment("inventory", "inventory", service_name="inventory-service"),
            deployment("payments", "payments", service_name="payments-service"),
            deployment("recommendations", "recommendations", service_name="recommendations-service"),
        ])
        dependency_observations.extend([
            *service_obs("inventory", "inventory-service", p95=0.03),
            *service_obs("payments", "payments-service", p95=0.04),
            *service_obs("recommendations", "recommendations-service", p95=0.06),
        ])

    k8s = {
        "schema_version": "1.0",
        "bundle_id": "k8s:healthy",
        "observed_at": "2026-09-09T00:00:00+00:00",
        "observations": [
            k8s_obs("k8s.nodes", {"total": 3, "ready": 3, "nodes": []}),
            k8s_obs("k8s.pods", {"unhealthy_count": 0, "unhealthy": [], "total_restarts": 0}),
            k8s_obs("k8s.deployments", {"items": deployments}),
            k8s_obs("k8s.gateways", {"items": []}),
            k8s_obs("k8s.httproutes", {"items": []}),
            k8s_obs("k8s.argocd", {"items": [
                {"name": "platform", "sync": "Synced", "health": "Healthy"},
                {"name": "demo-app", "sync": "Synced", "health": "Healthy"},
            ]}),
            k8s_obs("k8s.warning_events", {"count": 0, "recent": []}),
        ],
    }
    prom = {
        "schema_version": "1.0",
        "bundle_id": "prom:healthy",
        "observed_at": "2026-09-09T00:00:00+00:00",
        "observations": [
            prom_obs("prometheus.platform_api_target_up", 1, component="platform-api", signal="target_up"),
            prom_obs("prometheus.platform_api_error_ratio_5m", 0, component="platform-api", signal="error_ratio_5m"),
            prom_obs("prometheus.platform_api_error_ratio_1h", 0, component="platform-api", signal="error_ratio_1h"),
            prom_obs(
                "prometheus.platform_api_p95_latency_5m",
                0.08,
                component="platform-api",
                signal="p95_latency_seconds_5m",
            ),
            prom_obs("prometheus.platform_api_burn_rate_5m", 0, component="platform-api", signal="slo_burn_rate_5m"),
            prom_obs("prometheus.platform_api_burn_rate_1h", 0, component="platform-api", signal="slo_burn_rate_1h"),
            *dependency_observations,
            prom_obs("prometheus.demo_restarts_1h", 0),
            prom_obs("prometheus.oomkilled_containers", 0),
            prom_obs("prometheus.demo_hpa_saturation", 0.5),
            prom_obs("prometheus.envoy_live", 1, component="envoy-gateway", signal="proxy_live"),
            prom_obs("prometheus.otel_failed_spans_5m", 0, component="otel-collector", signal="failed_spans_rate_5m"),
            prom_obs("prometheus.otel_refused_spans_5m", 0, component="otel-collector", signal="refused_spans_rate_5m"),
        ],
    }
    return k8s, prom


class OpsReviewTests(unittest.TestCase):
    def test_healthy_evidence_produces_healthy_review(self):
        k8s, prom = healthy_bundles()
        review = review_ops_evidence(k8s, prom)
        self.assertEqual(review["state"], "healthy")
        self.assertEqual(review["release_guidance"], "continue")
        self.assertEqual(review["findings"], [])
        self.assertEqual(review["evidence"]["missing_required"], [])
        self.assertEqual(review["topology"]["dependencies"], ["catalog-service", "orders-service"])

    def test_expanded_topology_is_discovered_without_hardcoded_service_logic(self):
        k8s, prom = healthy_bundles(expanded=True)
        review = review_ops_evidence(k8s, prom)
        self.assertEqual(review["state"], "healthy")
        self.assertEqual(review["topology"]["dependencies"], [
            "catalog-service",
            "inventory-service",
            "orders-service",
            "payments-service",
            "recommendations-service",
        ])

    def test_new_dependency_failure_is_detected_generically(self):
        k8s, prom = healthy_bundles(expanded=True)
        for observation in prom["observations"]:
            if observation["id"] == "prometheus.payments_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.25"
        review = review_ops_evidence(k8s, prom)
        ids = {item["id"] for item in review["findings"]}
        self.assertEqual(review["state"], "at_risk")
        self.assertIn("dependency.payments_high_error_ratio", ids)

    def test_dependency_failure_and_fast_burn_are_detected(self):
        k8s, prom = healthy_bundles()
        for observation in prom["observations"]:
            if observation["id"] == "prometheus.platform_api_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.12"
            if observation["id"] == "prometheus.platform_api_error_ratio_1h":
                observation["value"]["result"][0]["value"][1] = "0.03"
            if observation["id"] == "prometheus.platform_api_burn_rate_5m":
                observation["value"]["result"][0]["value"][1] = "120"
            if observation["id"] == "prometheus.platform_api_burn_rate_1h":
                observation["value"]["result"][0]["value"][1] = "30"
            if observation["id"] == "prometheus.orders_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.18"

        review = review_ops_evidence(k8s, prom)
        ids = {item["id"] for item in review["findings"]}
        self.assertEqual(review["state"], "acute")
        self.assertEqual(review["release_guidance"], "hold")
        self.assertIn("platform_api.fast_error_budget_burn", ids)
        self.assertIn("dependency.orders_high_error_ratio", ids)

    def test_gitops_fault_profile_is_correlated_with_orders_symptoms(self):
        k8s, prom = healthy_bundles()
        deployments = next(item for item in k8s["observations"] if item["id"] == "k8s.deployments")
        orders = next(item for item in deployments["value"]["items"] if item["name"] == "orders")
        orders["operational_env"]["FAULT_LATENCY_MS"] = "800"
        orders["operational_env"]["FAULT_ERROR_RATE_PERCENT"] = "25"

        for observation in prom["observations"]:
            if observation["id"] == "prometheus.platform_api_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.20"
            if observation["id"] == "prometheus.orders_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.25"
            if observation["id"] == "prometheus.platform_api_p95_latency_5m":
                observation["value"]["result"][0]["value"][1] = "0.95"
            if observation["id"] == "prometheus.orders_p95_latency_5m":
                observation["value"]["result"][0]["value"][1] = "0.82"

        review = review_ops_evidence(k8s, prom)
        ids = {item["id"] for item in review["findings"]}
        self.assertEqual(review["state"], "acute")
        self.assertIn("demo_app.controlled_fault_enabled", ids)
        self.assertIn("dependency.orders_high_error_ratio", ids)
        self.assertIn("dependency.orders_high_p95_latency", ids)
        self.assertIn("dependency.orders_fault_injection_correlated", ids)
        correlated = next(item for item in review["findings"] if item["id"] == "dependency.orders_fault_injection_correlated")
        self.assertIn("k8s.deployments", correlated["evidence_refs"])
        self.assertIn("prometheus.orders_error_ratio_5m", correlated["evidence_refs"])

    def test_missing_required_signal_is_insufficient_evidence(self):
        k8s, prom = healthy_bundles()
        prom["observations"] = [
            item for item in prom["observations"]
            if item["id"] != "prometheus.envoy_live"
        ]
        review = review_ops_evidence(k8s, prom)
        self.assertEqual(review["state"], "insufficient_evidence")
        self.assertEqual(review["release_guidance"], "insufficient_evidence")
        self.assertIn("prometheus.envoy_live", review["evidence"]["missing_required"])
        self.assertTrue(any(item["type"] == "evidence_gap" for item in review["learning_candidates"]))

    def test_missing_new_dependency_telemetry_is_insufficient_evidence(self):
        k8s, prom = healthy_bundles(expanded=True)
        prom["observations"] = [
            item for item in prom["observations"]
            if item["id"] != "prometheus.inventory_p95_latency_5m"
        ]
        review = review_ops_evidence(k8s, prom)
        self.assertEqual(review["state"], "insufficient_evidence")
        self.assertIn(
            "prometheus.inventory.p95_latency_seconds_5m",
            review["evidence"]["missing_required"],
        )

    def test_post_change_review_can_verify_recovery(self):
        k8s, prom = healthy_bundles()
        for observation in prom["observations"]:
            if observation["id"] == "prometheus.platform_api_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.10"
        before = review_ops_evidence(k8s, prom)

        k8s_after, prom_after = healthy_bundles()
        after = review_ops_evidence(k8s_after, prom_after)
        comparison = compare_ops_reviews(before, after)

        self.assertIn("platform_api.high_error_ratio", comparison["resolved"])
        self.assertTrue(comparison["improved"])
        self.assertTrue(comparison["verified_recovery"])
        self.assertFalse(comparison["regressed"])

    def test_p2_persistence_does_not_block_verified_recovery(self):
        k8s, prom = healthy_bundles()
        warnings = next(item for item in k8s["observations"] if item["id"] == "k8s.warning_events")
        warnings["value"] = {"count": 1, "recent": [{"reason": "HistoricalWarning"}]}
        for observation in prom["observations"]:
            if observation["id"] == "prometheus.platform_api_error_ratio_5m":
                observation["value"]["result"][0]["value"][1] = "0.10"
        before = review_ops_evidence(k8s, prom)

        k8s_after, prom_after = healthy_bundles()
        warnings_after = next(item for item in k8s_after["observations"] if item["id"] == "k8s.warning_events")
        warnings_after["value"] = {"count": 1, "recent": [{"reason": "HistoricalWarning"}]}
        after = review_ops_evidence(k8s_after, prom_after)
        comparison = compare_ops_reviews(before, after)

        self.assertIn("cluster.warning_events_present", comparison["persistent"])
        self.assertEqual(comparison["persistent_blocking"], [])
        self.assertTrue(comparison["verified_recovery"])

    def test_persistent_finding_becomes_learning_candidate(self):
        k8s, prom = healthy_bundles()
        for observation in prom["observations"]:
            if observation["id"] == "prometheus.platform_api_p95_latency_5m":
                observation["value"]["result"][0]["value"][1] = "0.8"
        before = review_ops_evidence(k8s, prom)
        after = review_ops_evidence(k8s, prom)
        comparison = compare_ops_reviews(before, after)

        self.assertIn("platform_api.high_p95_latency", comparison["persistent"])
        self.assertIn("platform_api.high_p95_latency", comparison["persistent_blocking"])
        self.assertTrue(any(item["type"] == "persistent_finding" for item in comparison["learning_candidates"]))
        self.assertFalse(comparison["verified_recovery"])


if __name__ == "__main__":
    unittest.main()
