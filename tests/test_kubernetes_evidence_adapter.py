from __future__ import annotations

import unittest
from unittest.mock import patch

from adapters.evidence.base import normalize_adapter_result
from adapters.evidence.kubernetes import collect_kubernetes_evidence


class KubernetesEvidenceAdapterTests(unittest.TestCase):
    @patch("adapters.evidence.kubernetes.shutil.which", return_value="/usr/bin/kubectl")
    @patch("adapters.evidence.kubernetes._run")
    @patch("adapters.evidence.kubernetes._json")
    def test_collects_bounded_read_only_evidence(self, mock_json, mock_run, _mock_which) -> None:
        def fake_json(cmd, *, timeout=15):
            command = " ".join(cmd)
            if " version -o json" in command:
                return ({"clientVersion": {"gitVersion": "v1.36.1"}, "serverVersion": {"gitVersion": "v1.36.1"}}, None)
            if " get nodes -o json" in command:
                return ({"items": [{
                    "metadata": {"name": "worker-1"},
                    "spec": {},
                    "status": {
                        "conditions": [{"type": "Ready", "status": "True"}],
                        "nodeInfo": {"kubeletVersion": "v1.36.1"},
                    },
                }]}, None)
            if " get namespace demo-app -o json" in command:
                return ({"metadata": {"labels": {"pod-security.kubernetes.io/enforce": "restricted"}}, "status": {"phase": "Active"}}, None)
            if " get pods -A -o json" in command:
                return ({"items": []}, None)
            if " get events -A " in command:
                return ({"items": []}, None)
            return ({"items": []}, None)

        def fake_run(cmd, *, timeout=15):
            command = " ".join(cmd)
            if "config current-context" in command:
                return ("kind-platform\n", None)
            if "top nodes" in command:
                return ("worker-1 100m 2% 512Mi 3%\n", None)
            if "top pods" in command:
                return ("demo-app web-abc 10m 64Mi\n", None)
            return ("", None)

        mock_json.side_effect = fake_json
        mock_run.side_effect = fake_run

        result = collect_kubernetes_evidence(namespace="demo-app")
        self.assertEqual(result["collection_mode"], "read_only")
        self.assertEqual(result["scope"]["context"], "kind-platform")
        self.assertGreaterEqual(len(result["observations"]), 10)

        references = [item["provenance"]["reference"] for item in result["observations"]]
        forbidden = (" apply ", " delete ", " patch ", " replace ", " create ", " edit ", " scale ")
        for reference in references:
            padded = f" {reference} "
            self.assertFalse(any(token in padded for token in forbidden), reference)

        normalized = normalize_adapter_result(result)
        self.assertTrue(normalized["bundle_id"].startswith("adapter:kubernetes-kubectl:"))
        self.assertEqual(len(normalized["observations"]), len(result["observations"]))


if __name__ == "__main__":
    unittest.main()
