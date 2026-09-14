"""Validate discoverability, governance, and eval contracts for artifact Skills.

Behavioral expectations belong in skill-evals, not exact prompt wording asserts.
"""
import json
from pathlib import Path
import unittest

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("artifact-hygiene", "ssot-review", "eval-integrity")


class ArtifactReflexContractTests(unittest.TestCase):
    def test_local_artifact_reflex_skills_are_discoverable(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                metadata = yaml.safe_load(text.split("---", 2)[1])
                self.assertEqual(metadata["name"], skill)
                self.assertTrue(metadata["description"].strip())

    def test_paperthin_remains_outside_runtime_skill_sources(self):
        registry = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
        self.assertNotIn("paperthin", {source["id"] for source in registry["sources"]})
        self.assertFalse(any(capability["id"].startswith("paperthin-") for capability in registry["capabilities"]))

    def test_local_reflexes_are_governed(self):
        registry = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
        by_id = {capability["id"]: capability for capability in registry["capabilities"]}
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertEqual(by_id[skill]["source"], "harness-local")
                self.assertEqual(by_id[skill]["execution_policy"], "governed")

    def test_artifact_eval_suites_validate(self):
        schema = json.loads((ROOT / "schemas" / "skill-eval-suite.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for skill in SKILLS:
            with self.subTest(skill=skill):
                suite = json.loads((ROOT / "skill-evals" / skill / "evals.json").read_text(encoding="utf-8"))
                validator.validate(suite)
                self.assertEqual(suite["skill_id"], skill)
                ids = [case["id"] for case in suite["cases"]]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertEqual({case["kind"] for case in suite["cases"]},
                                 {"explicit", "implicit", "contextual", "negative"})


if __name__ == "__main__":
    unittest.main()
