import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_capability_registry", ROOT / "scripts" / "validate_capability_registry.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(module)


class CapabilityRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = module.load_registry(ROOT / "capabilities" / "registry.yaml")

    def test_registry_is_valid(self):
        self.assertEqual(module.validate_registry(self.registry), [])

    def test_floating_external_revision_is_rejected(self):
        data = copy.deepcopy(self.registry)
        ext = next(s for s in data["sources"] if s["type"] == "github")
        ext["revision"] = "main"
        errors = module.validate_registry(data)
        self.assertTrue(any("40-char commit SHA" in e for e in errors))

    def test_external_reference_cannot_become_executable(self):
        data = copy.deepcopy(self.registry)
        ext_id = next(s["id"] for s in data["sources"] if s["execution"] == "reference_only")
        cap = next(c for c in data["capabilities"] if c["source"] == ext_id)
        cap["execution_policy"] = "governed"
        errors = module.validate_registry(data)
        self.assertTrue(any("must remain reference_only" in e for e in errors))

    def test_high_risk_capability_requires_gate(self):
        data = copy.deepcopy(self.registry)
        cap = next(c for c in data["capabilities"] if c["risk"] == "high")
        cap["requires_human_gate"] = False
        errors = module.validate_registry(data)
        self.assertTrue(any("must require a human gate" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
