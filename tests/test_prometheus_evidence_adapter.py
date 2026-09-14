from __future__ import annotations

import unittest
from unittest.mock import patch

from adapters.evidence.base import normalize_adapter_result
from adapters.evidence.prometheus import collect_prometheus_evidence


class PrometheusEvidenceAdapterTests(unittest.TestCase):
    @patch("adapters.evidence.prometheus._get_json")
    def test_collects_query_results_with_provenance(self, mock_get_json) -> None:
        def fake_get_json(url, *, timeout=10, headers=None):
            if url.endswith("/api/v1/status/runtimeinfo"):
                return ({"status": "success", "data": {"storageRetention": "6h"}}, None)
            return ({
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [{"metric": {}, "value": [1, "1"]}],
                },
            }, None)

        mock_get_json.side_effect = fake_get_json

        result = collect_prometheus_evidence(
            base_url="http://127.0.0.1:9090/",
            queries={
                "demo_up": {
                    "query": 'min(up{namespace="demo-app"})',
                    "component": "demo-app",
                    "signal": "target_up",
                }
            },
            scope={"namespace": "demo-app"},
        )

        self.assertEqual(result["collection_mode"], "read_only")
        self.assertEqual(result["scope"]["base_url"], "http://127.0.0.1:9090")
        self.assertEqual(len(result["observations"]), 2)

        metric = result["observations"][1]
        self.assertEqual(metric["source_type"], "metrics")
        self.assertEqual(metric["component"], "demo-app")
        self.assertEqual(metric["provenance"]["query"], 'min(up{namespace="demo-app"})')

        normalized = normalize_adapter_result(result)
        self.assertTrue(normalized["bundle_id"].startswith("adapter:prometheus-http-api:"))

    @patch("adapters.evidence.prometheus._get_json")
    def test_gateway_host_header_is_forwarded_and_recorded(self, mock_get_json) -> None:
        def fake_get_json(url, *, timeout=10, headers=None):
            self.assertEqual(headers, {"Host": "prometheus.lab.local"})
            if url.endswith("/api/v1/status/runtimeinfo"):
                return ({"status": "success", "data": {}}, None)
            return ({
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [{"metric": {"platform_service": "platform-api"}, "value": [1, "1"]}],
                },
            }, None)

        mock_get_json.side_effect = fake_get_json

        result = collect_prometheus_evidence(
            base_url="http://127.0.0.1:8080",
            headers={"Host": "prometheus.lab.local"},
            queries={
                "platform_api_target_up": {
                    "query": 'min(up{platform_service="platform-api"})',
                    "component": "platform-api",
                    "signal": "target_up",
                }
            },
            scope={"host_header": "prometheus.lab.local"},
        )

        metric = result["observations"][1]
        self.assertEqual(metric["status"], "observed")
        self.assertEqual(metric["provenance"]["host_header"], "prometheus.lab.local")
        self.assertEqual(result["scope"]["host_header"], "prometheus.lab.local")
        self.assertEqual(mock_get_json.call_count, 2)

    @patch("adapters.evidence.prometheus._get_json")
    def test_query_failure_stays_unavailable_evidence(self, mock_get_json) -> None:
        mock_get_json.side_effect = [
            ({"status": "success", "data": {}}, None),
            (None, "connection refused"),
        ]

        result = collect_prometheus_evidence(
            base_url="http://127.0.0.1:9090",
            queries={"demo_up": {"query": "up", "component": "demo-app", "signal": "target_up"}},
        )

        self.assertEqual(result["observations"][1]["status"], "unavailable")
        self.assertIn("connection refused", result["observations"][1]["value"]["error"])


if __name__ == "__main__":
    unittest.main()
