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

    def test_agent_scenario_default_runs_orchestrator_and_evaluation(self) -> None:
        result = self.run_cli(AGENT, "scenario", SCENARIO)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Infrastructure Engineering Agent · scenario", result.stdout)
        self.assertIn("Evidence catalog discovered", result.stdout)
        self.assertIn("classification: dependency_saturation", result.stdout)
        self.assertIn("Model turns: 3", result.stdout)
        self.assertIn("Read-only tool calls: 3", result.stdout)
        self.assertIn("ASSESSMENT_EVIDENCE_BACKED", result.stdout)
        self.assertIn("SCENARIO PASS", result.stdout)
        self.assertIn("Score: 5/5", result.stdout)
        self.assertIn("Recording:", result.stdout)
        self.assertIn("no live provider", result.stdout)

    def test_agent_scenario_check_remains_static_contract_validation(self) -> None:
        result = self.run_cli(AGENT, "scenario", "check", SCENARIO)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("binds 3 resources, 2 observations, 3 red herrings", result.stdout)
        self.assertNotIn("Model turns:", result.stdout)

    def test_harness_entrypoint_remains_compatible(self) -> None:
        result = self.run_cli(HARNESS, "doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        # The compatibility command still presents the Agent product identity.
        self.assertIn("Infrastructure Engineering Agent · doctor", result.stdout)


if __name__ == "__main__":
    unittest.main()
