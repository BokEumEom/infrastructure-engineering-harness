from __future__ import annotations

import unittest

from runtime.change_policy import evaluate_change_policy


class ChangePolicyTests(unittest.TestCase):
    def test_capacity_cross_owner_change_requires_approval(self) -> None:
        proposal = {
            "risk_inputs": {
                "destructive": False,
                "privilege_expansion": False,
                "public_exposure": False,
                "capacity_increase": True,
                "cost_implication": True,
                "ownership_domains": ["terraform", "gitops"],
            }
        }
        result = evaluate_change_policy(proposal)
        self.assertEqual(result["risk"], "medium")
        self.assertEqual(result["decision"], "approval_required")
        self.assertTrue(result["approval_required"])
        self.assertTrue(result["executable"])

    def test_destructive_change_is_blocked(self) -> None:
        result = evaluate_change_policy({
            "risk_inputs": {
                "destructive": True,
                "ownership_domains": ["terraform"],
            }
        })
        self.assertEqual(result["risk"], "high")
        self.assertEqual(result["decision"], "blocked")
        self.assertFalse(result["executable"])


if __name__ == "__main__":
    unittest.main()
