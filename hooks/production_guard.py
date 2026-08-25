#!/usr/bin/env python3
"""Defense-in-depth guard for common direct infrastructure mutations.

This is not a security boundary. Production enforcement belongs in independent
authorization, CI/CD approvals, protected branches, and policy-as-code.
"""

import json
import re
import sys

DENY_PATTERNS = [
    (r"\b(terraform|tofu)\s+(apply|destroy)\b", "Direct IaC mutation is blocked. Produce a plan or reviewed proposal."),
    (r"\bpulumi\s+(up|destroy)\b", "Direct Pulumi mutation is blocked. Produce a preview or reviewed proposal."),
    (r"\bkubectl\s+delete\b", "Direct resource deletion is blocked. Use a reviewed change workflow."),
    (r"\bhelm\s+uninstall\b", "Direct release deletion is blocked. Use a reviewed change workflow."),
    (r"\brm\s+-[^\n]*r[^\n]*f[^\n]*\s+/(\s|$)", "Recursive deletion of the filesystem root is blocked."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    command = str(payload.get("tool_input", {}).get("command", ""))
    for pattern, reason in DENY_PATTERNS:
        if re.search(pattern, command, flags=re.IGNORECASE):
            json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}, sys.stdout)
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
