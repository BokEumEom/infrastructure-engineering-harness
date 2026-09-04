from pathlib import Path
import json
import tempfile
import unittest

import yaml
from jsonschema import Draft202012Validator

from runtime.context_assembly import (
    ContextSection,
    LatencyBudget,
    LatencyTracker,
    assemble_prompt_context,
)
from runtime.memory import PersistentMemoryStore
from runtime.release_control import SkillReleaseController
from runtime.skill_registry import RuntimeSkillRegistry


ROOT = Path(__file__).resolve().parents[1]


class MemoryPerformanceReleaseTests(unittest.TestCase):
    def test_session_memory_persists_across_store_reopen(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "memory.sqlite"
            with PersistentMemoryStore(db) as store:
                record = store.put(
                    scope="session",
                    owner_id="operator-1",
                    session_id="session-1",
                    kind="task_checkpoint",
                    content={"step": "verify-db"},
                    source="runtime",
                    actor="model",
                )
                memory_id = record.memory_id

            with PersistentMemoryStore(db) as reopened:
                loaded = reopened.get(memory_id)
                self.assertIsNotNone(loaded)
                self.assertEqual("verify-db", loaded.content["step"])

    def test_model_cannot_directly_persist_user_memory(self):
        with tempfile.TemporaryDirectory() as tmp, PersistentMemoryStore(Path(tmp) / "memory.sqlite") as store:
            with self.assertRaises(PermissionError):
                store.put(
                    scope="user",
                    owner_id="operator-1",
                    kind="preference",
                    content={"report_style": "concise"},
                    source="model-inference",
                    actor="model",
                )

    def test_memory_rejects_secret_like_fields_and_supports_forget(self):
        with tempfile.TemporaryDirectory() as tmp, PersistentMemoryStore(Path(tmp) / "memory.sqlite") as store:
            with self.assertRaises(ValueError):
                store.put(
                    scope="session",
                    owner_id="operator-1",
                    session_id="session-1",
                    kind="working_context",
                    content={"api_key": "do-not-store"},
                    source="runtime",
                    actor="trusted_runtime",
                )
            record = store.put(
                scope="user",
                owner_id="operator-1",
                kind="preference",
                content={"report_style": "concise"},
                source="user",
                actor="user",
            )
            self.assertTrue(store.forget(record.memory_id, actor="user"))
            self.assertIsNone(store.get(record.memory_id))

    def test_memory_schema_validates_runtime_record(self):
        schema = json.loads((ROOT / "schemas" / "agent-memory.schema.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp, PersistentMemoryStore(Path(tmp) / "memory.sqlite") as store:
            record = store.put(
                scope="session",
                owner_id="operator-1",
                session_id="session-1",
                kind="working_context",
                content={"focus": "payment-api"},
                source="runtime",
                actor="model",
            )
            Draft202012Validator(schema).validate(record.__dict__)

    def test_context_assembly_keeps_volatile_content_out_of_stable_prefix(self):
        assembly = assemble_prompt_context(
            [
                ContextSection("Live evidence", "cpu=72%", "volatile"),
                ContextSection("Agent contract", "minimal invariants", "global"),
                ContextSection("Session memory", "service=payment-api", "session"),
            ]
        )
        self.assertIn("Agent contract", assembly.stable_prefix)
        self.assertIn("Session memory", assembly.stable_prefix)
        self.assertNotIn("cpu=72%", assembly.stable_prefix)
        self.assertIn("cpu=72%", assembly.volatile_suffix)
        self.assertGreater(assembly.estimated_cacheable_tokens, 0)

    def test_latency_tracker_exposes_cache_and_turn_metrics(self):
        tracker = LatencyTracker()
        tracker.record_model_turn(
            duration_ms=1200,
            input_tokens=1000,
            output_tokens=200,
            cache_read_tokens=700,
            cache_write_tokens=100,
        )
        tracker.record_tool_batch(duration_ms=300, tool_calls=2)
        summary = tracker.summary()
        self.assertEqual(1, summary["model_turns"])
        self.assertEqual(2, summary["tool_calls"])
        self.assertEqual(1500, summary["accounted_ms"])
        self.assertEqual(0.7, summary["cache_read_ratio"])
        failures = tracker.budget_failures(
            LatencyBudget(max_model_turns=1, max_tool_calls=1, max_accounted_ms=1400)
        )
        self.assertIn("TOOL_CALL_BUDGET_EXCEEDED", failures)
        self.assertIn("LATENCY_BUDGET_EXCEEDED", failures)

    def test_release_policy_schema_validates(self):
        schema = json.loads(
            (ROOT / "schemas" / "runtime-skill-release-policy.schema.json").read_text(encoding="utf-8")
        )
        policy = yaml.safe_load((ROOT / "runtime" / "release-policy.yaml").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(policy)

    def test_default_release_policy_is_loaded_by_registry(self):
        registry = RuntimeSkillRegistry.from_files(
            ROOT / "capabilities" / "registry.yaml",
            ROOT / "runtime" / "skill-policy.yaml",
        )
        self.assertIsNotNone(registry.release_controller)
        self.assertIn("incident-analysis", {item.id for item in registry.list(for_model=True)})

    def test_kill_switch_removes_skill_from_model_surface(self):
        controller = SkillReleaseController(
            {
                "defaults": {"state": "active", "canary_percent": 100},
                "rules": [{"skill_id": "incident-analysis", "state": "disabled", "reason": "regression"}],
            }
        )
        registry = RuntimeSkillRegistry.from_files(
            ROOT / "capabilities" / "registry.yaml",
            ROOT / "runtime" / "skill-policy.yaml",
        )
        ids = {
            item.id
            for item in registry.list(for_model=True, release_controller=controller, rollout_key="run-1")
        }
        self.assertNotIn("incident-analysis", ids)
        with self.assertRaises(PermissionError):
            registry.get(
                "incident-analysis",
                actor="model",
                release_controller=controller,
                rollout_key="run-1",
            )

    def test_canary_assignment_is_stable_for_rollout_key(self):
        controller = SkillReleaseController(
            {
                "defaults": {"state": "active", "canary_percent": 100},
                "rules": [{"skill_id": "incident-analysis", "state": "canary", "canary_percent": 25}],
            }
        )
        first = controller.decision("incident-analysis", rollout_key="session-42")
        second = controller.decision("incident-analysis", rollout_key="session-42")
        self.assertEqual(first, second)
        self.assertIsNotNone(first.bucket)


if __name__ == "__main__":
    unittest.main()
