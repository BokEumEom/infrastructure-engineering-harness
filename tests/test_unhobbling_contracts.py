from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class UnhobblingContractTests(unittest.TestCase):
    def test_adaptive_incident_loop_validates(self):
        schema = json.loads((ROOT / "schemas" / "loop-spec.schema.json").read_text(encoding="utf-8"))
        spec = yaml.safe_load((ROOT / "loops" / "incident-response" / "loop.yaml").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(spec)
        self.assertEqual(spec["mode"], "adaptive")
        self.assertNotIn("steps", spec)
        self.assertEqual(spec["context"]["strategy"], "pull")

    def test_harness_lift_fixture_validates(self):
        schema = json.loads((ROOT / "schemas" / "harness-lift-experiment.schema.json").read_text(encoding="utf-8"))
        fixture = json.loads((ROOT / "harness-evals" / "fixtures" / "plumbing.triple.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(fixture)

    def _score(self, fixture):
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "score_harness_lift.py"), str(fixture), tmp.name],
            cwd=ROOT, check=True, capture_output=True, text=True
        )
        return Path(tmp.name)

    def test_positive_harness_lift_fixture_passes(self):
        report = self._score(ROOT / "harness-evals" / "fixtures" / "plumbing.triple.json")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_harness_lift.py"), str(ROOT / "harness-evals" / "policy.yaml"), str(report)],
            cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_hobbling_fixture_is_rejected(self):
        report = self._score(ROOT / "harness-evals" / "fixtures" / "unhobbling.triple.json")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_harness_lift.py"), str(ROOT / "harness-evals" / "policy.yaml"), str(report)],
            cwd=ROOT, capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hobbles", result.stdout)


if __name__ == "__main__":
    unittest.main()
