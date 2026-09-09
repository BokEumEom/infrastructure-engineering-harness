from __future__ import annotations

import unittest

from adapters.evidence.kubernetes import _safe_operational_env


class KubernetesOperationalEnvTests(unittest.TestCase):
    def test_only_allowlisted_literal_values_are_collected(self) -> None:
        deployment_spec = {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "api",
                            "env": [
                                {"name": "SERVICE_ROLE", "value": "orders"},
                                {"name": "FAULT_LATENCY_MS", "value": "800"},
                                {"name": "FAULT_ERROR_RATE_PERCENT", "value": "25"},
                                {"name": "APP_VERSION", "value": "abc1234"},
                                {"name": "OTEL_SERVICE_NAME", "value": "orders-service"},
                                {"name": "DATABASE_PASSWORD", "value": "must-not-be-collected"},
                                {
                                    "name": "FAULT_LATENCY_MS",
                                    "valueFrom": {"secretKeyRef": {"name": "hidden", "key": "fault"}},
                                },
                                {
                                    "name": "APP_VERSION",
                                    "valueFrom": {"configMapKeyRef": {"name": "runtime", "key": "version"}},
                                },
                            ],
                        }
                    ]
                }
            }
        }

        result = _safe_operational_env(deployment_spec)

        self.assertEqual(result["SERVICE_ROLE"], "orders")
        self.assertEqual(result["FAULT_LATENCY_MS"], "800")
        self.assertEqual(result["FAULT_ERROR_RATE_PERCENT"], "25")
        self.assertEqual(result["APP_VERSION"], "abc1234")
        self.assertEqual(result["OTEL_SERVICE_NAME"], "orders-service")
        self.assertNotIn("DATABASE_PASSWORD", result)
        self.assertEqual(len(result), 5)


if __name__ == "__main__":
    unittest.main()
