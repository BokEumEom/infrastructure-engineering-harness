from pathlib import Path
import unittest

import yaml

from runtime.kernel import (
    ApprovalOutcome,
    GuardDecision,
    GuardResult,
    RuntimeEventLog,
    RuntimeState,
    StaleRevisionError,
    ToolPipeline,
)
from runtime.skill_registry import RuntimeSkillRegistry


ROOT = Path(__file__).resolve().parents[1]


class RuntimeKernelTests(unittest.TestCase):
    def test_event_log_is_append_only_and_contiguous(self):
        log = RuntimeEventLog("run-1")
        first = log.append("run/started", {"source": "test"})
        second = log.append("context/snapshot", {"digest": "abc"}, model_visible=True)
        self.assertEqual((first.seq, second.seq), (0, 1))
        self.assertEqual(log.replay_types(), ("run/started", "context/snapshot"))
        self.assertIsInstance(log.events, tuple)

    def test_runtime_state_rejects_stale_revision(self):
        state = RuntimeState("run-1")
        revision = state.mutate(0, status="running")
        self.assertEqual(revision, 1)
        with self.assertRaises(StaleRevisionError):
            state.mutate(0, status="done")

    def test_monotonic_guard_deny_wins(self):
        log = RuntimeEventLog("run-1")
        result = ToolPipeline(log).evaluate(
            tool_name="cloud.change",
            arguments={"resource": "prod"},
            guards=(
                GuardResult("workflow", GuardDecision.ALLOW),
                GuardResult("production-boundary", GuardDecision.DENY, "not authorized"),
                GuardResult("late-plugin", GuardDecision.ALLOW),
            ),
            approval_required=False,
        )
        self.assertFalse(result.executed)
        self.assertEqual(result.normalized_result["code"], "GUARD_DENIED")

    def test_missing_approval_fails_closed(self):
        log = RuntimeEventLog("run-1")
        result = ToolPipeline(log).evaluate(
            tool_name="ticket.write",
            arguments={"title": "x"},
            approval_required=True,
            approval_outcome=None,
        )
        self.assertFalse(result.executed)
        self.assertEqual(result.approval_outcome, ApprovalOutcome.UNAVAILABLE)
        self.assertIn("approval/requested", log.replay_types())
        self.assertIn("approval/decided", log.replay_types())

    def test_allowed_once_is_only_approval_grant(self):
        log = RuntimeEventLog("run-1")
        result = ToolPipeline(log).evaluate(
            tool_name="ticket.write",
            arguments={"title": "x"},
            approval_required=True,
            approval_outcome=ApprovalOutcome.ALLOWED_ONCE,
            simulated_value={"ticket": "OPS-1"},
        )
        self.assertTrue(result.executed)
        self.assertEqual(result.status, "completed")

    def test_runtime_skill_policy_can_make_skill_user_only(self):
        registry = RuntimeSkillRegistry.from_files(
            ROOT / "capabilities" / "registry.yaml",
            ROOT / "runtime" / "skill-policy.yaml",
        )
        model_ids = {item.id for item in registry.list(for_model=True)}
        user_ids = {item.id for item in registry.list(for_user=True)}
        self.assertNotIn("context-backpass", model_ids)
        self.assertIn("context-backpass", user_ids)
        with self.assertRaises(PermissionError):
            registry.get("context-backpass", actor="model")

    def test_runtime_skill_policy_only_targets_registered_capabilities(self):
        capability_data = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
        policy_data = yaml.safe_load((ROOT / "runtime" / "skill-policy.yaml").read_text(encoding="utf-8"))
        capability_ids = {item["id"] for item in capability_data["capabilities"]}
        for rule in policy_data["rules"]:
            self.assertIn(rule["skill_id"], capability_ids)

    def test_reference_skill_has_no_execution_authority(self):
        registry = RuntimeSkillRegistry.from_files(
            ROOT / "capabilities" / "registry.yaml",
            ROOT / "runtime" / "skill-policy.yaml",
        )
        skill = registry.get("kubernetes-ops", actor="model")
        self.assertEqual(skill.execution_authority, "none")


if __name__ == "__main__":
    unittest.main()
