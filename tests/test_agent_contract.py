from pathlib import Path
import importlib.util
import json
import unittest

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class InfrastructureEngineeringAgentContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = yaml.safe_load(
            (ROOT / "agents" / "infrastructure_engineering" / "agent.yaml").read_text(encoding="utf-8")
        )
        self.schema = json.loads(
            (ROOT / "schemas" / "agent-contract.schema.json").read_text(encoding="utf-8")
        )

    def test_agent_contract_validates(self):
        Draft202012Validator(self.schema).validate(self.contract)

    def test_agent_is_product_and_harness_is_internal(self):
        self.assertEqual("agent", self.contract["surface"]["product"])
        self.assertEqual("agent", self.contract["surface"]["default_entrypoint"])
        self.assertEqual("harness", self.contract["runtime_boundary"]["implementation"])

    def test_chat_approval_never_grants_authority(self):
        self.assertFalse(self.contract["authority"]["chat_approval_is_authorization"])
        self.assertEqual("independently_authorized", self.contract["authority"]["production_mutation"])

    def test_mutation_requires_provenance_and_revision_revalidation(self):
        backend = self.contract["backend"]
        self.assertTrue(backend["resource_provenance_required_for_mutation"])
        self.assertTrue(backend["apply_revalidates_staged_revision"])
        owned = set(self.contract["runtime_boundary"]["owns"])
        self.assertIn("untrusted_content_fencing", owned)
        self.assertIn("runtime_recording", owned)

    def test_backend_contract_imports(self):
        path = ROOT / "agents" / "infrastructure_engineering" / "backend.py"
        spec = importlib.util.spec_from_file_location("infrastructure_agent_backend", path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module, "InfrastructureEngineeringBackend"))


if __name__ == "__main__":
    unittest.main()
