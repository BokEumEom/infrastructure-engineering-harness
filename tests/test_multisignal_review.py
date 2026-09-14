from __future__ import annotations

import unittest

from runtime.multisignal_review import correlate_multisignal_evidence


class MultiSignalReviewTests(unittest.TestCase):
    def test_correlates_log_trace_id_with_tempo_without_changing_ops_decision(self) -> None:
        ops = {
            "state": "at_risk",
            "release_guidance": "hold",
            "findings": [{"id": "dependency.orders_high_p95_latency", "severity": "P1"}],
        }
        loki = {
            "observations": [
                {
                    "id": "loki.errors",
                    "status": "observed",
                    "value": {
                        "result": [
                            {
                                "stream": {"app": "orders"},
                                "values": [["1", '{"trace_id":"abc123","service":"orders-service","event":"orders_dependency_failed","level":"error"}']],
                            }
                        ]
                    },
                }
            ]
        }
        tempo = {
            "observations": [
                {
                    "id": "tempo.recent",
                    "status": "observed",
                    "value": {
                        "traces": [{"traceID": "abc123", "rootServiceName": "platform-api", "durationMs": 900}]
                    },
                }
            ]
        }

        result = correlate_multisignal_evidence(ops, loki, tempo)

        self.assertEqual(result["status"], "correlated")
        self.assertEqual(result["decision_effect"], "enrichment_only")
        self.assertEqual(result["ops_state"], "at_risk")
        self.assertEqual(result["release_guidance"], "hold")
        self.assertEqual(result["correlation_count"], 1)
        self.assertEqual(result["correlations"][0]["trace_id"], "abc123")
        self.assertEqual(result["correlations"][0]["log_services"], ["orders-service"])

    def test_correlates_exact_trace_followup_when_search_sample_does_not_overlap(self) -> None:
        ops = {"state": "healthy", "release_guidance": "continue", "findings": []}
        loki = {
            "observations": [
                {
                    "id": "loki.recent",
                    "status": "observed",
                    "value": {
                        "result": [
                            {
                                "stream": {"app": "web"},
                                "values": [["2", '{"trace_id":"exact123","service":"platform-api","event":"request_completed","level":"info"}']],
                            }
                        ]
                    },
                }
            ]
        }
        tempo = {
            "observations": [
                {
                    "id": "tempo.search",
                    "status": "observed",
                    "value": {"traces": [{"traceID": "different456"}]},
                },
                {
                    "id": "tempo.trace.1",
                    "status": "observed",
                    "signal": "trace_by_id",
                    "value": {"trace_id": "exact123", "trace": {"batches": [{"resource": {}}]}},
                    "provenance": {"trace_id": "exact123", "lookup": "exact"},
                },
            ]
        }

        result = correlate_multisignal_evidence(ops, loki, tempo)

        self.assertEqual(result["status"], "correlated")
        self.assertEqual(result["correlation_count"], 1)
        self.assertEqual(result["correlations"][0]["trace_id"], "exact123")
        self.assertEqual(result["correlations"][0]["tempo_summaries"][-1]["lookup"], "exact")
        self.assertEqual(result["decision_effect"], "enrichment_only")

    def test_reports_source_gap_without_changing_ops_decision(self) -> None:
        ops = {"state": "healthy", "release_guidance": "continue", "findings": []}
        loki = {"observations": [{"id": "loki.logs", "status": "unavailable", "value": {"error": "down"}}]}
        tempo = {"observations": []}

        result = correlate_multisignal_evidence(ops, loki, tempo)

        self.assertEqual(result["status"], "source_unavailable")
        self.assertEqual(result["ops_state"], "healthy")
        self.assertEqual(result["release_guidance"], "continue")
        self.assertEqual(result["source_unavailable"], ["loki.logs"])


if __name__ == "__main__":
    unittest.main()
