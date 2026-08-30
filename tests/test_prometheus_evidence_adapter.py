import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from adapters.evidence import PrometheusEvidenceAdapter, PrometheusQuery, normalize_adapter_result

ROOT = Path(__file__).resolve().parents[1]


class PrometheusEvidenceAdapterTests(unittest.TestCase):
    def test_collects_latency_and_saturation_observations(self):
        fixture = json.loads((ROOT / "examples" / "environment" / "prometheus-query-results.json").read_text(encoding="utf-8"))
        responses = {item["query"]: item["response"] for item in fixture["queries"]}
        adapter = PrometheusEvidenceAdapter("http://prometheus.example", transport=responses.__getitem__)

        result = adapter.collect(
            [
                PrometheusQuery(
                    name=item["name"],
                    query=item["query"],
                    component=item["component"],
                    signal=item["signal"],
                    unit=item.get("unit"),
                )
                for item in fixture["queries"]
            ],
            observed_at=fixture["observed_at"],
            scope=fixture["scope"],
        )

        self.assertEqual(result["collection_mode"], "read_only")
        self.assertEqual(result["freshness_seconds"], 10)
        self.assertEqual([item["signal"] for item in result["observations"]], ["request_latency_p95", "connection_saturation"])
        self.assertEqual(result["observations"][0]["value"], 0.88)
        self.assertEqual(result["observations"][1]["provenance"]["resource"], "db:orders")

        bundle = normalize_adapter_result(result)
        self.assertEqual(bundle["freshness_seconds"], 10)
        self.assertNotIn("verified", bundle["observations"][0])
        self._validate(result, "evidence-adapter-result.schema.json")
        self._validate(bundle, "evidence.schema.json")

    def test_rejects_non_successful_query(self):
        adapter = PrometheusEvidenceAdapter("http://prometheus.example", transport=lambda _: {"status": "error"})

        with self.assertRaises(ValueError):
            adapter.collect(
                [PrometheusQuery(name="latency", query="up", component="svc:payment-api", signal="up")],
                observed_at="2026-05-30T12:27:10Z",
                scope={"service": "payment-api"},
            )

    def _validate(self, data, schema_name):
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(data))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
