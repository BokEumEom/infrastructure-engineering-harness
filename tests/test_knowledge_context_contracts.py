from pathlib import Path
import copy
import json
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeContextContractTests(unittest.TestCase):
    def _load(self, path):
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    def test_context_pack_example_validates(self):
        schema = self._load("schemas/context-pack.schema.json")
        example = self._load("examples/context-pack/incident-response.json")
        Draft202012Validator(schema).validate(example)

    def test_knowledge_candidate_example_validates(self):
        schema = self._load("schemas/knowledge-candidate.schema.json")
        example = self._load("examples/knowledge/incident-learning-candidate.json")
        Draft202012Validator(schema).validate(example)

    def test_verified_fact_candidate_requires_supporting_evidence(self):
        schema = self._load("schemas/knowledge-candidate.schema.json")
        example = self._load("examples/knowledge/incident-learning-candidate.json")
        candidate = copy.deepcopy(example)
        candidate["epistemic_class"] = "verified_fact"
        candidate["evidence"]["supporting"] = []
        errors = list(Draft202012Validator(schema).iter_errors(candidate))
        self.assertTrue(errors)

    def test_context_pack_exposes_blocking_evidence_gaps(self):
        example = self._load("examples/context-pack/incident-response.json")
        blocking = [gap for gap in example["gaps"] if gap["blocking"]]
        self.assertTrue(blocking)
        self.assertTrue(blocking[0]["required_evidence"])


if __name__ == "__main__":
    unittest.main()
