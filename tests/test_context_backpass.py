from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class ContextBackpassTests(unittest.TestCase):
    def test_new_rule_requires_two_independent_sessions(self):
        schema = json.loads((ROOT / "schemas/context-update-proposal.schema.json").read_text())
        proposal = {
            "schema_version": "1.0",
            "target": "AGENTS.md",
            "before_tokens": 1000,
            "after_tokens": 1050,
            "budget_tokens": 5000,
            "human_review_required": True,
            "source_of_truth_writeback": False,
            "edits": [{
                "id": "add-rule",
                "operation": "add",
                "new_rule_id": "new-rule",
                "reason": "observed once",
                "replacement_text": "Do the thing.",
                "evidence_session_ids": ["session-1"]
            }]
        }
        errors = list(Draft202012Validator(schema).iter_errors(proposal))
        self.assertTrue(errors)

    def test_context_lift_claim_rejects_fixture(self):
        policy = ROOT / "agent-context/policy.yaml"
        fixture = ROOT / "agent-context/fixtures/agents-context.paired.json"
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            subprocess.run([sys.executable, str(ROOT / "scripts/score_context_lift.py"), str(fixture), str(report)], check=True)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/check_context_lift.py"), str(policy), str(report), "--require-live"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires source=live", result.stdout)

    def test_policy_protects_source_of_truth(self):
        policy = yaml.safe_load((ROOT / "agent-context/policy.yaml").read_text())
        protected = set(policy["protected_targets"])
        self.assertIn(".infra-context/", protected)
        self.assertIn("contexts/", protected)
        self.assertIn("domains/", protected)


if __name__ == "__main__":
    unittest.main()
