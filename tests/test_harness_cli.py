from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "agent"
HARNESS = ROOT / "harness"
SCENARIO = "evals/scenarios/sre-dependency-saturation.json"


class AgentCliTests(unittest.TestCase):
    def run_cli(self, entrypoint: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(entrypoint), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_agent_help_exposes_stable_commands(self) -> None:
        result = self.run_cli(AGENT, "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Infrastructure Engineering Agent CLI", result.stdout)
        for command in (
            "setup",
            "demo",
            "validate",
            "scenario",
            "k8s-evidence",
            "prometheus-evidence",
            "ops-review",
            "ops-compare",
            "doctor",
        ):
            self.assertIn(command, result.stdout)

    def test_agent_doctor_is_credential_free(self) -> None:
        result = self.run_cli(AGENT, "doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Infrastructure Engineering Agent · doctor", result.stdout)
        self.assertIn("Default scenario: found", result.stdout)

    def test_agent_demo_runs_checked_in_fixture_path(self) -> None:
        result = self.run_cli(AGENT, "demo")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEMO PASS", result.stdout)
        self.assertIn("Production mutation: none", result.stdout)
        self.assertIn("not live agent effectiveness", result.stdout)

    def assert_scenario_runtime_output(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Infrastructure Engineering Agent · scenario", result.stdout)
        self.assertIn("Fixture Context Resolver", result.stdout)
        self.assertIn("Reference Orchestrator", result.stdout)
        self.assertIn("classification", result.stdout.lower())
        self.assertIn("dependency_saturation", result.stdout)
        self.assertIn("Evidence", result.stdout)
        self.assertIn("Red Herrings", result.stdout)
        self.assertIn("Safety", result.stdout)
        self.assertIn("ASSESSMENT_EVIDENCE_BACKED", result.stdout)
        self.assertIn("Runtime Event Log", result.stdout)
        self.assertIn("model turns: 3", result.stdout)
        self.assertIn("read-only tool calls: 3", result.stdout)
        self.assertIn("Score: 5/5", result.stdout)
        self.assertIn("Recording", result.stdout)
        self.assertIn("not live-agent effectiveness", result.stdout)
        self.assertIn("no live AWS, Datadog, or model API provider", result.stdout)
        self.assertIn("SCENARIO PASS", result.stdout)

    def test_agent_scenario_default_is_run_alias(self) -> None:
        result = self.run_cli(AGENT, "scenario", SCENARIO)
        self.assert_scenario_runtime_output(result)

    def test_agent_scenario_run_executes_same_runtime_contract(self) -> None:
        result = self.run_cli(AGENT, "scenario", "run", SCENARIO)
        self.assert_scenario_runtime_output(result)

    def test_agent_scenario_check_remains_static_contract_validation(self) -> None:
        result = self.run_cli(AGENT, "scenario", "check", SCENARIO)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("binds 3 resources, 2 observations, 3 red herrings", result.stdout)
        self.assertNotIn("Runtime Event Log", result.stdout)
        self.assertNotIn("model turns:", result.stdout)

    def test_harness_entrypoint_remains_compatible(self) -> None:
        result = self.run_cli(HARNESS, "doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Infrastructure Engineering Agent · doctor", result.stdout)


if __name__ == "__main__":
    unittest.main()
