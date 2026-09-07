from pathlib import Path
import json
import unittest

import yaml
from jsonschema import Draft202012Validator

from runtime.channel import normalize_turn_request
from runtime.delegation import (
    DelegationRequest,
    DelegationResult,
    merge_delegate_result,
    validate_delegation,
)
from runtime.learning import semantic_memory_to_learning_candidate
from runtime.observability import AgentTrace


ROOT = Path(__file__).resolve().parents[1]


class AgentCoreAiOpsPatternTests(unittest.TestCase):
    def test_trace_records_model_tool_backend_and_verification_spans(self):
        trace = AgentTrace(trace_id="trace-test")
        root = trace.start_span("turn", kind="agent")
        model = trace.start_span("reason", kind="model", parent_span_id=root.span_id)
        trace.end_span(model, duration_ms=120)
        tool = trace.start_span("metrics", kind="tool", parent_span_id=root.span_id)
        trace.end_span(tool, duration_ms=80)
        backend = trace.start_span("observability-backend", kind="backend", parent_span_id=tool.span_id)
        trace.end_span(backend, duration_ms=40)
        verify = trace.start_span("verify", kind="verification", parent_span_id=root.span_id)
        trace.end_span(verify, duration_ms=30)
        trace.end_span(root, duration_ms=300)

        summary = trace.summary()
        self.assertEqual("trace-test", summary["trace_id"])
        self.assertEqual(5, summary["completed_span_count"])
        self.assertEqual(1, summary["count_by_kind"]["verification"])

    def test_all_channels_normalize_into_same_turn_contract(self):
        for channel in ("cli", "web", "slack", "github", "mcp", "api", "test"):
            request = normalize_turn_request(
                channel=channel,
                principal_id="operator-1",
                session_id="session-1",
                text="check service health",
            )
            self.assertEqual(channel, request.channel)
            self.assertEqual("operator-1", request.principal_id)

    def test_delegate_cannot_expand_capabilities_or_resource_scope(self):
        valid = DelegationRequest(
            delegate_id="db-specialist",
            purpose="analyze database evidence",
            allowed_capabilities=("incident-analysis",),
            allowed_resource_ids=("db:orders",),
        )
        validate_delegation(
            valid,
            parent_capabilities={"incident-analysis", "sre-review"},
            parent_resource_scope={"db:orders", "svc:payment-api"},
        )

        invalid = DelegationRequest(
            delegate_id="security-specialist",
            purpose="expand review",
            allowed_capabilities=("security-review",),
            allowed_resource_ids=("prod:other",),
        )
        with self.assertRaises(PermissionError):
            validate_delegation(
                invalid,
                parent_capabilities={"incident-analysis"},
                parent_resource_scope={"db:orders"},
            )

    def test_delegate_discovery_never_expands_mutation_eligibility(self):
        result = DelegationResult(
            delegate_id="db-specialist",
            assessment={"summary": "possible dependency"},
            discovered_resource_ids=("db:newly-named",),
        )
        eligible = merge_delegate_result(
            result,
            mutation_eligible_resource_ids={"db:orders"},
        )
        self.assertEqual({"db:orders"}, eligible)

    def test_semantic_memory_becomes_governed_candidate_not_truth(self):
        candidate = semantic_memory_to_learning_candidate(
            claim="Check connection saturation before resizing this service tier.",
            run_id="run-1",
            source_ref="recording:run-1",
            owner="platform-team",
            target_type="runbook",
            service="payment-api",
        )
        schema = json.loads(
            (ROOT / "schemas" / "knowledge-candidate.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(schema).validate(candidate)
        self.assertEqual("proposed", candidate["status"])
        self.assertTrue(candidate["governance"]["review_required"])
        self.assertNotEqual("verified_fact", candidate["epistemic_class"])

    def test_task_eval_profiles_are_task_specific_and_normalized(self):
        data = yaml.safe_load((ROOT / "evals" / "task-profiles.yaml").read_text(encoding="utf-8"))
        self.assertIn("incident", data["profiles"])
        self.assertIn("change", data["profiles"])
        self.assertNotEqual(
            set(data["profiles"]["incident"]["required_metrics"]),
            set(data["profiles"]["finops"]["required_metrics"]),
        )
        for profile in data["profiles"].values():
            self.assertAlmostEqual(1.0, sum(profile["weights"].values()))


if __name__ == "__main__":
    unittest.main()
