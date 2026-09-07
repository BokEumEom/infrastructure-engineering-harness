from __future__ import annotations

import asyncio
from pathlib import Path
import unittest

from runtime.scenario_runner import run_scenario


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "evals" / "scenarios" / "sre-dependency-saturation.json"


class ScenarioRunnerTests(unittest.TestCase):
    def test_scenario_runs_through_orchestrator_and_scores(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))

        self.assertEqual("verified", execution.outcome.status)
        self.assertEqual(2, execution.outcome.model_turns)
        self.assertEqual(2, execution.outcome.tool_calls)
        self.assertEqual("dependency_saturation", execution.assessment["classification"])
        self.assertEqual({"ev:db-wait", "ev:cpu"}, set(execution.assessment["evidence_ids"]))
        self.assertTrue(execution.score.ok)
        self.assertEqual((5, 5), (execution.score.passed, execution.score.total))

    def test_ground_truth_is_not_model_visible(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        snapshots = [
            event for event in execution.outcome.event_log.events
            if event.type == "context/snapshot"
        ]
        self.assertEqual(1, len(snapshots))
        context = snapshots[0].data["context"]
        self.assertNotIn("ground_truth", context)
        self.assertNotIn("success_conditions", context)

    def test_scenario_execution_remains_read_only(self) -> None:
        execution = asyncio.run(run_scenario(SCENARIO, root=ROOT))
        requests = [
            event for event in execution.outcome.event_log.events
            if event.type == "tool/requested"
        ]
        self.assertTrue(requests)
        self.assertTrue(all(event.data.get("execution_authority") == "read" for event in requests))


if __name__ == "__main__":
    unittest.main()
