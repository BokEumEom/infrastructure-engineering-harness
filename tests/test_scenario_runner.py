from __future__ import annotations

import asyncio
import json
from pathlib import Path
import tempfile
import unittest

from runtime.recording import verify_recording
from runtime.scenario_runner import format_scenario_report, run_scenario


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "evals" / "scenarios" / "sre-dependency-saturation.json"


class ScenarioRunnerTests(unittest.TestCase):
    def test_scenario_runs_through_orchestrator_and_scores(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))

        self.assertEqual("verified", execution.outcome.status)
        self.assertEqual(3, execution.outcome.model_turns)
        self.assertEqual(3, execution.outcome.tool_calls)
        self.assertEqual("dependency_saturation", execution.assessment["classification"])
        self.assertEqual({"ev:db-wait", "ev:cpu"}, set(execution.assessment["evidence_ids"]))
        self.assertTrue(execution.score.ok)
        self.assertEqual((5, 5), (execution.score.passed, execution.score.total))
        self.assertTrue(verify_recording(execution.recording).valid)
        self.assertEqual("fixture", execution.recording["source"])

    def test_evaluator_only_fields_are_not_model_visible(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        snapshots = [
            event for event in execution.outcome.event_log.events
            if event.type == "context/snapshot"
        ]
        self.assertEqual(1, len(snapshots))
        context = snapshots[0].data["context"]
        for hidden in (
            "ground_truth",
            "required_evidence",
            "success_conditions",
            "expected_behavior",
            "red_herrings",
            "prohibited_actions",
        ):
            self.assertNotIn(hidden, context)
        self.assertEqual(
            [
                "application CPU at 72%",
                "recent frontend deployment",
                "unrelated Kafka warning",
            ],
            context["reported_signals"],
        )

    def test_model_discovers_evidence_before_reading_it(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        requests = [
            event.data["tool_name"] for event in execution.outcome.event_log.events
            if event.type == "tool/requested"
        ]
        self.assertEqual("evidence.list", requests[0])
        self.assertEqual(["evidence.read", "evidence.read"], requests[1:])

    def test_red_herring_dispositions_are_derived_without_answer_key(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        dispositions = {
            item["signal"]: item["disposition"]
            for item in execution.assessment["red_herrings"]
        }
        self.assertEqual("rejected", dispositions["application CPU at 72%"])
        self.assertEqual("unproven", dispositions["recent frontend deployment"])
        self.assertEqual("unproven", dispositions["unrelated Kafka warning"])

    def test_scorer_uses_ground_truth_only_after_model_execution(self) -> None:
        scenario = json.loads(SCENARIO.read_text(encoding="utf-8"))
        scenario["ground_truth"]["classification"] = "compute_saturation"
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
            json.dump(scenario, handle)
            mutated = Path(handle.name)
        try:
            execution = asyncio.run(run_scenario(mutated, root=ROOT))
        finally:
            mutated.unlink(missing_ok=True)

        self.assertEqual("dependency_saturation", execution.assessment["classification"])
        self.assertFalse(execution.score.ok)
        self.assertFalse(execution.score.checks[0].passed)
        self.assertIn("expected=compute_saturation", execution.score.checks[0].detail)

    def test_scenario_execution_remains_read_only(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        requests = [
            event for event in execution.outcome.event_log.events
            if event.type == "tool/requested"
        ]
        self.assertTrue(requests)
        self.assertTrue(all(event.data.get("execution_authority") == "read" for event in requests))

    def test_report_exposes_required_runtime_sections_and_boundary(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        report = format_scenario_report(execution)
        for section in (
            "Classification",
            "Evidence",
            "Red Herrings",
            "Safety",
            "Verification",
            "Runtime Event Log",
            "Score",
            "Recording",
            "Execution Boundary",
        ):
            self.assertIn(section, report)
        self.assertIn("fixture/runtime validation only; not live-agent effectiveness", report)
        self.assertIn("no live AWS, Datadog, or model API provider", report)


if __name__ == "__main__":
    unittest.main()
