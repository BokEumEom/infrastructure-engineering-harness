from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.ops_review import compare_ops_reviews, review_ops_evidence


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals" / "ops" / "orders-fault-benchmark.json"


class OpsBenchmarkFixtureTests(unittest.TestCase):
    def test_orders_fault_benchmark_fixture(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

        fault = review_ops_evidence(
            fixture["fault"]["kubernetes"],
            fixture["fault"]["prometheus"],
        )
        recovery = review_ops_evidence(
            fixture["recovery"]["kubernetes"],
            fixture["recovery"]["prometheus"],
        )
        comparison = compare_ops_reviews(fault, recovery)
        expected = fixture["expected"]

        self.assertEqual(fault["state"], expected["fault_state"])
        self.assertEqual(fault["release_guidance"], expected["fault_release_guidance"])

        fault_ids = {finding["id"] for finding in fault["findings"]}
        self.assertTrue(set(expected["required_findings"]) <= fault_ids)

        correlated = next(
            finding for finding in fault["findings"]
            if finding["id"] == "dependency.orders_fault_injection_correlated"
        )
        self.assertIn("k8s.deployments", correlated["evidence_refs"])
        self.assertTrue(
            {"prometheus.orders_error_ratio_5m", "prometheus.orders_p95_latency_5m"}
            & set(correlated["evidence_refs"])
        )

        self.assertEqual(recovery["state"], expected["recovery_state"])
        self.assertEqual(comparison["verified_recovery"], expected["verified_recovery"])
        self.assertEqual(comparison["persistent_blocking"], expected["persistent_blocking"])
        self.assertEqual(comparison["new_blocking"], expected["new_blocking"])

        # The retained P2 warning is intentionally allowed to persist without
        # turning a successful remediation into a false-negative recovery.
        self.assertIn("cluster.warning_events_present", comparison["persistent"])
        self.assertNotIn("cluster.warning_events_present", comparison["persistent_blocking"])


if __name__ == "__main__":
    unittest.main()
