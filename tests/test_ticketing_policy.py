import unittest

from adapters.actions.ticketing.policy import evaluate_ticket_policy, ticket_fingerprint


REQUEST = {
    "provider": "jira",
    "source_ref": "INC-2026-014",
    "service": "payment-api",
    "kind": "incident",
    "severity": "sev2",
    "risk": "medium",
    "domains": ["infrastructure", "sre"],
    "evidence_refs": ["EV-101", "EV-102"],
}

POLICY = {
    "mode": "policy",
    "default_action": "manual",
    "rules": [
        {
            "id": "sev2",
            "when": {"kinds": ["incident"], "severities": ["sev1", "sev2"]},
            "action": "auto_create",
            "require_evidence": True,
            "min_evidence": 2,
        }
    ],
}


class TicketingPolicyTests(unittest.TestCase):
    def test_fingerprint_is_stable(self):
        self.assertEqual(ticket_fingerprint(REQUEST), ticket_fingerprint(dict(REQUEST)))

    def test_policy_allows_evidenced_incident(self):
        decision = evaluate_ticket_policy(REQUEST, POLICY)
        self.assertEqual(decision["action"], "auto_create")
        self.assertEqual(decision["rule_id"], "sev2")

    def test_insufficient_evidence_falls_back_to_manual(self):
        request = dict(REQUEST)
        request["evidence_refs"] = ["EV-101"]
        decision = evaluate_ticket_policy(request, POLICY)
        self.assertEqual(decision["action"], "manual")

    def test_manual_mode_never_auto_creates(self):
        policy = dict(POLICY)
        policy["mode"] = "manual"
        self.assertEqual(evaluate_ticket_policy(REQUEST, policy)["action"], "manual")


if __name__ == "__main__":
    unittest.main()
