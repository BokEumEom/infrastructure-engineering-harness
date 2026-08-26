from pathlib import Path
import json
import unittest
import yaml

from adapters.evidence.base import normalize_adapter_result
from environment.binding import bind_capability

ROOT = Path(__file__).resolve().parents[1]


class EnvironmentContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
        self.graph = json.loads((ROOT / "examples" / "environment" / "resource-graph.json").read_text(encoding="utf-8"))

    def test_reference_capability_binding_cannot_gain_change_authority(self):
        bound = bind_capability(
            self.registry,
            self.graph,
            capability_id="kubernetes-ops",
            resource_ids=["svc:payment-api"],
            permission_mode="change",
        )
        self.assertEqual(bound["execution_authority"], "none")
        self.assertEqual(bound["permission_scope"]["mode"], "read_only")
        self.assertTrue(bound["human_gate_required"])

    def test_binding_rejects_unknown_resource(self):
        with self.assertRaises(KeyError):
            bind_capability(
                self.registry,
                self.graph,
                capability_id="incident-analysis",
                resource_ids=["svc:missing"],
            )

    def test_evidence_adapter_preserves_provenance(self):
        adapter_result = json.loads((ROOT / "examples" / "environment" / "evidence-adapter-result.json").read_text(encoding="utf-8"))
        bundle = normalize_adapter_result(adapter_result)
        self.assertEqual(bundle["observations"][0]["provenance"]["reference"], "service/payment-api/span/db.query")
        self.assertNotIn("verified", bundle["observations"][0])

    def test_non_read_only_adapter_is_rejected(self):
        adapter_result = json.loads((ROOT / "examples" / "environment" / "evidence-adapter-result.json").read_text(encoding="utf-8"))
        adapter_result["collection_mode"] = "change"
        with self.assertRaises(ValueError):
            normalize_adapter_result(adapter_result)


if __name__ == "__main__":
    unittest.main()
