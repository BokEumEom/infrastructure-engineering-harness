#!/usr/bin/env python3
"""Conservative Claude Code PreToolUse guard for destructive shell commands.

This is a safety example, not a security boundary. Real production enforcement
belongs in IAM, CI/CD approvals, protected branches, and policy-as-code.
"""

import json
import re
import sys

DENY_PATTERNS = [
    (r"\bterraform\s+(apply|destroy)\b", "Direct Terraform mutation is blocked. Produce a plan or PR for human review."),
    (r"\baws\b[^\n]*(\sdelete-|\sterminate-instances\b|\sdelete-stack\b)", "Destructive AWS commands are blocked by the infrastructure harness."),
    (r"\bkubectl\s+delete\b", "Destructive Kubernetes deletion is blocked. Prepare a reviewed change instead."),
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
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    }
                },
                sys.stdout,
            )
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
