import importlib.util, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("skill_lift",ROOT/"scripts/score_skill_lift.py")
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

class SkillLiftTests(unittest.TestCase):
    def test_dimensions_follow_runtime_signals(self):
        d=M.dimensions({"security":1,"skill_execution":.8,"skill_efficiency":.7,"accuracy":.9,"goal_accuracy":.6,"behavior_check":.8})
        self.assertEqual(d["security"],1); self.assertEqual(d["discoverability"],.8); self.assertEqual(d["correctness"],.9)
        self.assertAlmostEqual(d["effectiveness"],.7); self.assertEqual(d["efficiency"],.7)
    def test_verdict_bands(self):
        self.assertEqual(M.verdict(-.10),"fail"); self.assertEqual(M.verdict(.05),"pass"); self.assertEqual(M.verdict(0),"neutral")
    def test_fixture_has_all_case_kinds(self):
        exp=json.loads((ROOT/"skill-evals/fixtures/incident-analysis.paired.json").read_text())
        self.assertEqual({p["kind"] for p in exp["pairs"]},{"explicit","implicit","contextual","negative"})

if __name__=="__main__": unittest.main()
