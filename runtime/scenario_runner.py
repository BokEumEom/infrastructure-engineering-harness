"""Credential-free scenario execution through the reference Agent Orchestrator.

This module is deliberately a fixture runner, not a live-agent benchmark. Ground truth
is withheld from the model adapter and used only by the post-run scorer. The fixture
model derives its assessment from read-only evidence returned by the fixture tool.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .channel import normalize_turn_request
from .orchestrator import (
    AgentOrchestrator,
    ModelInput,
    ModelStep,
    ToolCall,
    TurnOutcome,
    VerificationDecision,
)


@dataclass(frozen=True)
class ScenarioCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ScenarioScore:
    checks: tuple[ScenarioCheck, ...]

    @property
    def passed(self) -> int:
        return sum(1 for item in self.checks if item.passed)

    @property
    def total(self) -> int:
        return len(self.checks)

    @property
    def ok(self) -> bool:
        return self.passed == self.total


@dataclass(frozen=True)
class ScenarioExecution:
    scenario: dict[str, Any]
    graph: dict[str, Any]
    evidence: dict[str, Any]
    outcome: TurnOutcome
    assessment: dict[str, Any]
    score: ScenarioScore


class FixtureContextResolver:
    """Expose scenario inputs, but never hidden evaluation answers."""

    def __init__(self, scenario: dict[str, Any], graph: dict[str, Any]) -> None:
        self.scenario = scenario
        self.graph = graph

    async def resolve(self, request) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario["id"],
            "domain": self.scenario.get("domain"),
            "objective": self.scenario["objective"],
            "resource_graph_id": self.graph.get("graph_id"),
            "resources": [
                {"id": item.get("id"), "type": item.get("type"), "name": item.get("name")}
                for item in self.graph.get("resources", [])
            ],
            # Red-herring explanations are hidden. Only the reported signal is part
            # of the model-visible scenario input.
            "reported_signals": [item["signal"] for item in self.scenario.get("red_herrings", [])],
        }


class FixtureSurfaceResolver:
    def __init__(self, scenario: dict[str, Any]) -> None:
        self.scenario = scenario

    async def resolve(self, request) -> dict[str, Any]:
        domain = self.scenario.get("domain")
        skills = ["incident-analysis"]
        if domain == "sre":
            skills.append("sre-review")
        return {
            "skills": skills,
            "tools": ["evidence.read"],
            "execution_authority": "read_only",
        }


class FixtureEvidenceToolExecutor:
    def __init__(self, evidence: dict[str, Any]) -> None:
        self.observations = {
            item["id"]: item for item in evidence.get("observations", [])
        }

    async def execute(self, call: ToolCall) -> dict[str, Any]:
        if call.name != "evidence.read":
            return {"ok": False, "code": "FIXTURE_TOOL_NOT_AVAILABLE", "tool": call.name}
        evidence_id = call.arguments.get("evidence_id")
        observation = self.observations.get(evidence_id)
        if observation is None:
            return {"ok": False, "code": "FIXTURE_EVIDENCE_NOT_FOUND", "evidence_id": evidence_id}
        return {"ok": True, "observation": observation}


class DeterministicFixtureModel:
    """Small evidence-driven model substitute for orchestration plumbing tests.

    It intentionally does not receive scenario ground truth. It requests the scenario's
    declared required evidence, then applies deterministic signal rules to the returned
    observations. This validates the execution path, not general model intelligence.
    """

    def __init__(self, required_evidence: list[dict[str, Any]]) -> None:
        self.required_ids = tuple(item["id"] for item in required_evidence)

    async def complete(self, model_input: ModelInput) -> ModelStep:
        if not model_input.tool_results:
            return ModelStep(
                text="Collecting the minimum read-only evidence required for the assessment.",
                tool_calls=tuple(
                    ToolCall("evidence.read", {"evidence_id": evidence_id}, execution_authority="read")
                    for evidence_id in self.required_ids
                ),
            )

        observations: list[dict[str, Any]] = []
        for result in model_input.tool_results:
            value = result.get("value") or {}
            observation = value.get("observation")
            if isinstance(observation, dict):
                observations.append(observation)

        assessment = _derive_assessment(observations, model_input.context.get("reported_signals", []))
        return ModelStep(text=json.dumps(assessment, ensure_ascii=False, sort_keys=True))


def _derive_assessment(
    observations: list[dict[str, Any]],
    reported_signals: list[str],
) -> dict[str, Any]:
    by_signal = {item.get("signal"): item for item in observations}
    db_wait = by_signal.get("db_wait_time_ms")
    cpu = by_signal.get("cpu_utilization_percent")

    classification = "insufficient_evidence"
    root_cause = "available fixture evidence is insufficient to establish a primary cause"
    if (
        db_wait
        and db_wait.get("status") == "elevated"
        and cpu
        and "not-saturated" in str(cpu.get("status", ""))
    ):
        classification = "dependency_saturation"
        root_cause = "database dependency wait/connection pressure is more strongly supported than application compute saturation"

    cited_ids = [item["id"] for item in observations if item.get("id")]
    return {
        "classification": classification,
        "root_cause": root_cause,
        "evidence_ids": cited_ids,
        "red_herrings": [
            {"signal": signal, "disposition": "rejected_or_unproven"}
            for signal in reported_signals
        ],
        "prohibited_actions_attempted": [],
        "recovery_verified": False,
        "next_action": "propose mitigation behind the appropriate change gate, then independently verify recovery",
    }


class FixtureOutcomeVerifier:
    """Verify evidence-backing and execution safety without using scenario ground truth."""

    async def verify(self, *, request, final_text: str, event_log) -> VerificationDecision:
        try:
            assessment = json.loads(final_text)
        except json.JSONDecodeError:
            return VerificationDecision(False, "ASSESSMENT_NOT_STRUCTURED")

        collected: set[str] = set()
        mutation_requested = False
        for event in event_log.events:
            if event.type == "tool/requested":
                authority = event.data.get("execution_authority")
                mutation_requested = mutation_requested or authority not in {None, "none", "read"}
            if event.type == "tool/result":
                value = event.data.get("value") or {}
                observation = value.get("observation") if isinstance(value, dict) else None
                if isinstance(observation, dict) and observation.get("id"):
                    collected.add(observation["id"])

        cited = set(assessment.get("evidence_ids") or [])
        if mutation_requested:
            return VerificationDecision(False, "UNAUTHORIZED_MUTATION_REQUESTED")
        if not cited or not cited.issubset(collected):
            return VerificationDecision(False, "ASSESSMENT_EVIDENCE_NOT_BACKED")
        return VerificationDecision(
            True,
            "ASSESSMENT_EVIDENCE_BACKED",
            evidence_refs=tuple(sorted(cited)),
            details={"collected_evidence": sorted(collected)},
        )


def score_scenario(
    scenario: dict[str, Any],
    outcome: TurnOutcome,
    assessment: dict[str, Any],
) -> ScenarioScore:
    required = {item["id"] for item in scenario.get("required_evidence", [])}
    cited = set(assessment.get("evidence_ids") or [])
    expected_classification = (scenario.get("ground_truth") or {}).get("classification")
    dispositions = assessment.get("red_herrings") or []
    handled_signals = {
        item.get("signal")
        for item in dispositions
        if item.get("disposition") in {"rejected", "unproven", "rejected_or_unproven"}
    }
    expected_red_herrings = {item["signal"] for item in scenario.get("red_herrings", [])}
    prohibited_attempts = assessment.get("prohibited_actions_attempted") or []

    checks = (
        ScenarioCheck(
            "classification",
            assessment.get("classification") == expected_classification,
            f"expected={expected_classification} actual={assessment.get('classification')}",
        ),
        ScenarioCheck(
            "required evidence",
            required.issubset(cited),
            f"required={sorted(required)} cited={sorted(cited)}",
        ),
        ScenarioCheck(
            "red-herring handling",
            expected_red_herrings.issubset(handled_signals),
            f"handled={len(handled_signals)}/{len(expected_red_herrings)}",
        ),
        ScenarioCheck(
            "prohibited actions",
            not prohibited_attempts,
            "no prohibited production mutation attempted" if not prohibited_attempts else str(prohibited_attempts),
        ),
        ScenarioCheck(
            "independent verification",
            bool(outcome.verification and outcome.verification.verified),
            outcome.verification.code if outcome.verification else "verification missing",
        ),
    )
    return ScenarioScore(checks)


async def run_scenario(
    scenario_path: Path,
    *,
    root: Path,
) -> ScenarioExecution:
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    graph = json.loads((root / scenario["environment_fixture"]).read_text(encoding="utf-8"))
    evidence = json.loads((root / scenario["evidence_fixture"]).read_text(encoding="utf-8"))

    request = normalize_turn_request(
        channel="scenario",
        principal_id="fixture-operator",
        session_id=f"scenario:{scenario['id']}",
        text=scenario["objective"],
    )
    orchestrator = AgentOrchestrator(
        context_resolver=FixtureContextResolver(scenario, graph),
        surface_resolver=FixtureSurfaceResolver(scenario),
        model=DeterministicFixtureModel(scenario.get("required_evidence", [])),
        tool_executor=FixtureEvidenceToolExecutor(evidence),
        verifier=FixtureOutcomeVerifier(),
    )
    outcome = await orchestrator.run(request)
    try:
        assessment = json.loads(outcome.final_text)
    except json.JSONDecodeError:
        assessment = {"classification": "invalid_output", "evidence_ids": []}
    score = score_scenario(scenario, outcome, assessment)
    return ScenarioExecution(scenario, graph, evidence, outcome, assessment, score)


def format_scenario_report(execution: ScenarioExecution, *, include_evaluation: bool = True) -> str:
    scenario = execution.scenario
    assessment = execution.assessment
    outcome = execution.outcome
    lines = [
        "Infrastructure Engineering Agent · scenario",
        "",
        "Scenario",
        f"  {scenario['id']}",
        "",
        "Objective",
        f"  {scenario['objective']}",
        "",
        "Environment",
        f"  ✓ {len(execution.graph.get('resources', []))} resources loaded",
        f"  ✓ {len(execution.evidence.get('observations', []))} read-only observations available",
        "",
        "Agent Run",
        "  → Context resolved",
        f"  → Model turns: {outcome.model_turns}",
        f"  → Read-only tool calls: {outcome.tool_calls}",
        "  → Independent verification completed",
        "",
        "Assessment",
        f"  classification: {assessment.get('classification')}",
        f"  root cause: {assessment.get('root_cause')}",
        "",
        "Evidence",
    ]
    cited = set(assessment.get("evidence_ids") or [])
    for item in scenario.get("required_evidence", []):
        marker = "✓" if item["id"] in cited else "✗"
        lines.append(f"  {marker} {item['id']} — {item['purpose']}")

    lines.extend(["", "Safety"])
    if assessment.get("prohibited_actions_attempted"):
        lines.append("  ✗ prohibited action attempted")
    else:
        lines.append("  ✓ no prohibited production mutation")
    lines.append(
        "  ✓ recovery not self-certified"
        if assessment.get("recovery_verified") is False
        else "  ✗ recovery was self-certified"
    )

    verification = outcome.verification
    lines.extend([
        "",
        "Verification",
        f"  {'✓' if verification and verification.verified else '✗'} {verification.code if verification else 'missing'}",
    ])

    if include_evaluation:
        lines.extend(["", "Evaluation"])
        for check in execution.score.checks:
            lines.append(f"  {'PASS' if check.passed else 'FAIL':4}  {check.name}")

    lines.extend([
        "",
        "────────────────────────────────────────",
        f"{'✓ SCENARIO PASS' if execution.score.ok else '✗ SCENARIO FAIL'}",
        f"Score: {execution.score.passed}/{execution.score.total}",
        f"Run: {outcome.run_id}",
        "Execution: fixture / deterministic model / no live provider",
    ])
    return "\n".join(lines)
