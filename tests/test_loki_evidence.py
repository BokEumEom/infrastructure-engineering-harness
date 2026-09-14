from __future__ import annotations

import unittest
from unittest.mock import patch

from adapters.evidence.loki import collect_loki_evidence


class LokiEvidenceTests(unittest.TestCase):
    @patch("adapters.evidence.loki._get_json")
    def test_collects_logs_and_trace_ids(self, get_json) -> None:
        get_json.return_value = (
            {
                "status": "success",
                "data": {
                    "resultType": "streams",
                    "result": [
                        {
                            "stream": {"namespace": "demo-app", "app": "orders"},
                            "values": [
                                ["1", '{"level":"error","trace_id":"abc123","event":"orders_dependency_failed"}'],
                                ["2", '{"level":"info","trace_id":"def456","event":"http_request_completed"}'],
                            ],
                        }
                    ],
                },
            },
            None,
        )

        result = collect_loki_evidence(
            base_url="http://127.0.0.1:8080",
            queries={
                "errors": {
                    "component": "orders-service",
                    "signal": "error_logs",
                    "query": '{namespace="demo-app"} | json | level="error"',
                }
            },
            headers={"Host": "loki.lab.local"},
        )

        observation = result["observations"][0]
        self.assertEqual(result["collection_mode"], "read_only")
        self.assertEqual(observation["source_type"], "logs")
        self.assertEqual(observation["value"]["entry_count"], 2)
        self.assertEqual(observation["value"]["trace_ids"], ["abc123", "def456"])
        self.assertEqual(observation["provenance"]["host_header"], "loki.lab.local")


if __name__ == "__main__":
    unittest.main()
