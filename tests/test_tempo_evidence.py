from __future__ import annotations

import unittest
from unittest.mock import patch

from adapters.evidence.tempo import collect_tempo_evidence


class TempoEvidenceTests(unittest.TestCase):
    @patch("adapters.evidence.tempo._get_json")
    def test_collects_search_results(self, get_json) -> None:
        get_json.return_value = (
            {
                "traces": [
                    {
                        "traceID": "abc123",
                        "rootServiceName": "platform-api",
                        "rootTraceName": "GET /",
                        "durationMs": 120,
                    }
                ],
                "metrics": {"inspectedTraces": 1},
            },
            None,
        )

        result = collect_tempo_evidence(
            base_url="http://127.0.0.1:8080",
            searches={
                "platform": {
                    "component": "platform-api",
                    "signal": "recent_traces",
                    "tags": "service.name=platform-api",
                }
            },
            headers={"Host": "tempo.lab.local"},
        )

        observation = result["observations"][0]
        self.assertEqual(result["collection_mode"], "read_only")
        self.assertEqual(observation["source_type"], "traces")
        self.assertEqual(observation["value"]["trace_count"], 1)
        self.assertEqual(observation["value"]["traces"][0]["traceID"], "abc123")
        self.assertEqual(observation["provenance"]["host_header"], "tempo.lab.local")

    @patch("adapters.evidence.tempo._get_json")
    def test_can_fetch_one_trace_by_id(self, get_json) -> None:
        get_json.side_effect = [
            ({"traces": []}, None),
            ({"batches": [{"resource": {}}]}, None),
        ]

        result = collect_tempo_evidence(
            base_url="http://127.0.0.1:8080",
            searches={"recent": {"component": "platform", "signal": "recent_traces"}},
            trace_id="abc123",
        )

        trace = result["observations"][-1]
        self.assertEqual(trace["id"], "tempo.trace")
        self.assertEqual(trace["status"], "observed")
        self.assertEqual(trace["provenance"]["trace_id"], "abc123")


if __name__ == "__main__":
    unittest.main()
