from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "harness"


class HarnessCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_help_exposes_stable_commands(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("setup", "demo", "validate", "scenario", "doctor"):
            self.assertIn(command, result.stdout)

    def test_doctor_is_credential_free(self) -> None:
        result = self.run_cli("doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Infrastructure Engineering Harness · doctor", result.stdout)
        self.assertIn("Default scenario: found", result.stdout)

    def test_demo_runs_checked_in_fixture_path(self) -> None:
        result = self.run_cli("demo")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEMO PASS", result.stdout)
        self.assertIn("Production mutation: none", result.stdout)
        self.assertIn("not live agent effectiveness", result.stdout)


if __name__ == "__main__":
    unittest.main()
