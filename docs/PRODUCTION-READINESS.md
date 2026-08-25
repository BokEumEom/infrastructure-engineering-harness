# Production Readiness

This repository is a reference harness for production-oriented infrastructure engineering. It is not itself a production authorization system.

## Adoption levels

### Level 0 — Repository context

Use `AGENTS.md`, `.infra-context/`, and the schemas. No live tools. Useful for architecture and IaC review.

### Level 1 — Read-only evidence

Add one or more adapters that collect metrics, logs, traces, deployment history, runtime state, or configuration. Normalize all results to the evidence contract.

### Level 2 — Change proposal automation

Allow the agent to generate code/config changes, plans, risk summaries, and pull requests. Keep production execution outside the agent's authority.

### Level 3 — Controlled execution

If an organization chooses automated execution, require independent controls such as short-lived credentials, least privilege, environment allowlists, CI approvals, policy-as-code, protected branches, audit logging, and tested rollback.

## Required controls for a production pilot

- schema validation in CI
- read-only-by-default live integrations
- evidence provenance in recommendations
- provider-neutral regression evals
- explicit change proposal and rollback plan
- human approval for high-impact changes
- independent authorization outside the model
- secrets excluded from context files
- context ownership and review process

## What hooks can and cannot do

Agent hooks can prevent common accidental commands and improve ergonomics. They do not replace cloud authorization, Kubernetes RBAC, deployment approvals, or policy engines. Assume an agent-side regex can be bypassed and design the real control plane accordingly.
