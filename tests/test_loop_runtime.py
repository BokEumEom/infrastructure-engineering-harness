import unittest
from loops.runtime import add_verified_fact, budget_exhausted, record_iteration, regression_summary, transition


def state():
    return {"schema_version":"1.0","run_id":"RUN-1","loop_id":"incident-response","status":"initialized","iteration":0,"started_at":"2026-08-25T00:00:00Z","updated_at":"2026-08-25T00:00:00Z","current_step":None,"verified_facts":[],"assumptions":[],"history":[],"progress":{"last_material_progress_iteration":0,"no_progress_iterations":0},"regression_obligations":[{"id":"availability","description":"availability remains healthy","status":"pending"}],"pending_human_gate":None}


class LoopRuntimeTests(unittest.TestCase):
    def test_rejects_agent_self_verification(self):
        with self.assertRaises(ValueError): add_verified_fact(state(), {"id":"x","statement":"self certified","verified_by":"agent","evidence_refs":["EV-1"]})
    def test_verified_fact_requires_evidence(self):
        with self.assertRaises(ValueError): add_verified_fact(state(), {"id":"x","statement":"verified externally","verified_by":"tool","evidence_refs":[]})
    def test_no_progress_budget(self):
        spec={"budgets":{"max_iterations":8,"max_no_progress_iterations":2}}; current=transition(state(),"running")
        current=record_iteration(current,step="observe",event="gap",outcome="no_progress"); current=record_iteration(current,step="observe",event="gap",outcome="no_progress")
        self.assertEqual("max_no_progress_iterations",budget_exhausted(spec,current))
    def test_terminal_cannot_transition(self):
        current=transition(state(),"failed")
        with self.assertRaises(ValueError): transition(current,"running")
    def test_regression_failure_wins(self):
        current=state(); current["regression_obligations"][0]["status"]="failed"; self.assertEqual("failed",regression_summary(current))


if __name__ == "__main__": unittest.main()
