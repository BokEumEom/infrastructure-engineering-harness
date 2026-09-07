from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class ArchitectureConvergenceTests(unittest.TestCase):
    def test_orchestrator_is_explicit_runtime_contract(self):
        contract = yaml.safe_load(
            (ROOT / "agents" / "infrastructure_engineering" / "agent.yaml").read_text(encoding="utf-8")
        )
        owned = set(contract["runtime_boundary"]["owns"])
        self.assertIn("turn_orchestration", owned)
        self.assertIn("telemetry_event_ssot", owned)
        self.assertTrue((ROOT / "runtime" / "orchestrator.py").exists())

    def test_runtime_event_log_is_documented_as_execution_ssot(self):
        architecture = (ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
        runtime = (ROOT / "runtime" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Runtime Event Log is execution SSOT", architecture)
        self.assertIn("Runtime Event Log is SSOT", runtime)

    def test_model_surface_is_context_skills_tools_not_mandatory_routing_chain(self):
        capability_model = (ROOT / "docs" / "CAPABILITY-MODEL.md").read_text(encoding="utf-8")
        self.assertIn("Context\nSkills\nTools", capability_model)
        self.assertIn("not a required architecture node", capability_model)

    def test_paperthin_remains_reference_not_runtime_capability_source(self):
        registry = yaml.safe_load(
            (ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8")
        )
        source_ids = {source["id"] for source in registry["sources"]}
        capability_ids = {item["id"] for item in registry["capabilities"]}
        self.assertNotIn("paperthin", source_ids)
        self.assertFalse(any(item.startswith("paperthin-") for item in capability_ids))

    def test_engineering_loop_is_optional_in_canonical_architecture(self):
        architecture = (ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("does **not** enter an Engineering Loop", architecture)
        self.assertIn("only when needed", architecture)


if __name__ == "__main__":
    unittest.main()
