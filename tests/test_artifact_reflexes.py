from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_local_artifact_reflex_skills_exist():
    for skill in ("artifact-hygiene", "ssot-review", "eval-integrity"):
        text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        assert f"name: {skill}" in text


def test_paperthin_is_pinned_reference_only():
    registry = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
    source = next(s for s in registry["sources"] if s["id"] == "paperthin")
    assert source["trust"] == "pinned_reference"
    assert source["execution"] == "reference_only"
    assert source["revision"] == "3bca079a51bcfff5dafb53d1d7f9f523d66ee317"

    referenced = [c for c in registry["capabilities"] if c["source"] == "paperthin"]
    assert referenced
    assert all(c["execution_policy"] == "reference_only" for c in referenced)


def test_local_reflexes_are_governed():
    registry = yaml.safe_load((ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in registry["capabilities"]}
    for skill in ("artifact-hygiene", "ssot-review", "eval-integrity"):
        assert by_id[skill]["source"] == "harness-local"
        assert by_id[skill]["execution_policy"] == "governed"


def test_loop_learning_preserves_negative_corpus_and_earned_reuse():
    text = (ROOT / "skills" / "loop-engineering" / "SKILL.md").read_text(encoding="utf-8")
    assert "negative corpus" in text.lower()
    assert "earned reuse" in text.lower()


def test_agents_contract_contains_artifact_reflex_rule():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "<!-- rule: artifact-hygiene-before-handoff -->" in text
    assert "<!-- rule: eval-independent-evidence -->" in text
