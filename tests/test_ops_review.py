from __future__ import annotations

import unittest

from runtime.ops_review import compare_ops_reviews, review_ops_evidence


def prom_obs(oid: str, value: float):
    return {
        "id": oid,
        "source_type": "metrics",
        "source": "prometheus",
        "component": "test",
        "signal": oid,
        "status": "observed",
        "value": {
            "resultType": "vector",
            "result": [{"metric": {}, "value": [1, str(value)]}],
        },
        "provenance": {"reference": "http://prometheus/api/v1/query", "query": oid},
    }


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


def healthy_bundles():
    k8s = {
        "schema_version": "1.0",
        "bundle_id": "k8s:healthy",
        "observed_at": "2026-09-09T00:00:00+00:00",
        "observations": [
            k8s_obs("k8s.nodes", {"total": 3, "ready": 3, "nodes": []}),
            k8s_obs("k8s.pods", {"unhealthy_count": 0, "unhealthy": [], "total_restarts": 0}),
            k8s_obs("k8s.deployments", {"items": [
                {"name": "web", "desired": 2, "ready": 2},
                {"name": "catalog", "desired": 2, "ready": 2},
                {"name": "orders", "desired": 2, "ready": 2},
            ]}),
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
            prom_obs("prometheus.platform_api_target_up", 1),
            prom_obs("prometheus.platform_api_error_ratio_5m", 0),
            prom_obs("prometheus.platform_api_error_ratio_1h", 0),
            prom_obs("prometheus.platform_api_p95_latency_5m", 0.08),
            prom_obs("prometheus.platform_api_burn_rate_5m", 0),
            prom_obs("prometheus.platform_api_burn_rate_1h", 0),
            prom_obs("prometheus.catalog_target_up", 1),
            prom_obs("prometheus.orders_target_up", 1),
            prom_obs("prometheus.catalog_error_ratio_5m", 0),
            prom_obs("prometheus.orders_error_ratio_5m", 0),
            prom_obs("prometheus.demo_restarts_1h", 0),
            prom_obs("prometheus.oomkilled_containers", 0),
            prom_obs("prometheus.demo_hpa_saturation", 0.5),
            prom_obs("prometheus.envoy_live", 1),
            prom_obs("prometheus.otel_failed_spans_5m", 0),
            prom_obs("prometheus.otel_refused_spans_5m", 0),
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

    def test_persistent_finding_becomes_learning_candidate(self):
        k8s, prom = healthy_bundles()
        for observation in prom["observations"]:
            if observation["id"] == "prometheus.platform_api_p95_latency_5m":
                observation["value"]["result"][0]["value"][1] = "0.8"
        before = review_ops_evidence(k8s, prom)
        after = review_ops_evidence(k8s, prom)
        comparison = compare_ops_reviews(before, after)

        self.assertIn("platform_api.high_p95_latency", comparison["persistent"])
        self.assertTrue(any(item["type"] == "persistent_finding" for item in comparison["learning_candidates"]))
        self.assertFalse(comparison["verified_recovery"])


if __name__ == "__main__":
    unittest.main()
