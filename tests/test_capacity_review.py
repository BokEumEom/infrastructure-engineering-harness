from __future__ import annotations

import unittest

from runtime.capacity_review import review_capacity_evidence


class CapacityReviewTests(unittest.TestCase):
    def test_correlates_scaling_limit_with_recent_quota_rejection(self) -> None:
        bundle = {
            "observed_at": "2026-09-14T09:00:00+00:00",
            "observations": [
                {
                    "id": "k8s.hpa",
                    "value": {
                        "items": [
                            {
                                "name": "web",
                                "min": 2,
                                "max": 6,
                                "current": 6,
                                "desired": 6,
                                "conditions": {"ScalingLimited": "True"},
                            }
                        ]
                    },
                },
                {
                    "id": "k8s.deployments",
                    "value": {"items": [{"name": "web", "desired": 6, "ready": 4}]},
                },
                {
                    "id": "k8s.warning_events",
                    "value": {
                        "count": 1,
                        "recent": [
                            {
                                "object": "ReplicaSet/web-abc123",
                                "reason": "FailedCreate",
                                "time": "2026-09-14T08:59:30+00:00",
                                "message": "Error creating: pods is forbidden: exceeded quota: demo-app-capacity, requested: requests.cpu=100m, used: requests.cpu=900m, limited: requests.cpu=900m",
                            }
                        ],
                    },
                },
            ],
        }

        review = review_capacity_evidence(bundle)
        ids = {f["id"] for f in review["findings"]}

        self.assertEqual(review["state"], "acute")
        self.assertIn("capacity.web_hpa_saturated", ids)
        self.assertIn("capacity.resource_quota_blocking_scaleout", ids)
        self.assertIn("capacity.web_hpa_quota_correlated", ids)
        self.assertEqual(review["evidence_summary"]["quota_requests_cpu_limit"], "900m")
        self.assertEqual(review["proposal"]["changes"][0]["owner"], "terraform")
        self.assertEqual(review["proposal"]["changes"][1]["owner"], "gitops")
        self.assertTrue(review["proposal"]["risk_inputs"]["capacity_increase"])

    def test_correlates_pending_scaleout_even_when_scalinglimited_is_false(self) -> None:
        bundle = {
            "observed_at": "2026-09-14T09:00:00+00:00",
            "observations": [
                {
                    "id": "k8s.hpa",
                    "value": {
                        "items": [
                            {
                                "name": "web",
                                "max": 6,
                                "current": 4,
                                "desired": 6,
                                "conditions": {"ScalingLimited": "False"},
                            }
                        ]
                    },
                },
                {"id": "k8s.deployments", "value": {"items": [{"name": "web", "desired": 6, "ready": 4}]}},
                {
                    "id": "k8s.warning_events",
                    "value": {
                        "count": 1,
                        "recent": [
                            {
                                "object": "ReplicaSet/web-new",
                                "time": "2026-09-14T08:59:45+00:00",
                                "message": "pods is forbidden: exceeded quota: demo-app-capacity, requested: requests.cpu=100m, used: requests.cpu=900m, limited: requests.cpu=900m",
                            }
                        ],
                    },
                },
            ],
        }

        review = review_capacity_evidence(bundle)
        ids = {f["id"] for f in review["findings"]}
        self.assertIn("capacity.web_hpa_quota_correlated", ids)
        self.assertTrue(review["evidence_summary"]["hpa_scaleout_pending"])
        self.assertIsNotNone(review["proposal"])

    def test_ignores_stale_quota_warning_for_correlation(self) -> None:
        bundle = {
            "observed_at": "2026-09-14T09:00:00+00:00",
            "observations": [
                {
                    "id": "k8s.hpa",
                    "value": {"items": [{"name": "web", "max": 6, "current": 6, "desired": 6, "conditions": {"ScalingLimited": "True"}}]},
                },
                {"id": "k8s.deployments", "value": {"items": [{"name": "web", "desired": 6, "ready": 6}]}},
                {
                    "id": "k8s.warning_events",
                    "value": {
                        "count": 1,
                        "recent": [
                            {
                                "object": "ReplicaSet/web-old",
                                "time": "2026-09-14T07:00:00+00:00",
                                "message": "exceeded quota: demo-app-capacity, limited: requests.cpu=900m",
                            }
                        ],
                    },
                },
            ],
        }

        review = review_capacity_evidence(bundle, warning_max_age_seconds=900)
        ids = {f["id"] for f in review["findings"]}
        self.assertNotIn("capacity.web_hpa_quota_correlated", ids)
        self.assertIsNone(review["proposal"])


if __name__ == "__main__":
    unittest.main()
