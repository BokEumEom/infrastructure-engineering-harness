# Infrastructure Engineering Harness — Agent Guide

This file is the cross-agent entry point for Codex, Kiro, and any agent that supports `AGENTS.md`.
Keep this file short. Durable infrastructure knowledge belongs in `.infra-context/`; schemas and workflows live in this repository.

## Prime directive

Treat infrastructure work as an evidence-based engineering decision, not a code-generation task.

Before recommending or generating a production-impacting change:

1. Identify the affected service and its criticality.
2. Load only relevant context from `.infra-context/`.
3. Separate confirmed evidence from assumptions.
4. Use current/live evidence when available, normalized to `schemas/evidence.schema.json`.
5. Compare with applicable ADRs, incidents, policies, and runbooks.
6. State risk, blast radius, validation, and rollback.
7. Produce a reviewed change proposal instead of directly mutating production.

## Context loading order

1. `.infra-context/service-catalog.yaml`
2. Relevant `.infra-context/architecture/*`
3. Relevant `.infra-context/policies/*`
4. Relevant `.infra-context/incidents/*` and `.infra-context/runbooks/*`
5. Relevant `.infra-context/adr/*`
6. Live evidence from optional read-only adapters

Do not load every context file by default.

## Safety contract

- Never assume write access is required for analysis.
- Prefer read-only tools for discovery and evidence collection.
- Do not directly apply infrastructure changes, delete resources, broaden IAM/authorization, or mutate production data.
- A production change must follow `workflows/change-proposal.md` and include human approval outside the model.
- Hooks are defense-in-depth examples, not a security boundary. Enforce real controls in IAM/RBAC, CI/CD, protected branches, policy-as-code, and deployment approvals.

## Evidence contract

Every material recommendation should be traceable to evidence. Use stable evidence IDs and include source type, observation time, component, signal, and source/provenance when available. Never invent telemetry values.

## Provider neutrality

Core reasoning must use capability categories such as `compute`, `datastore`, `messaging`, `network`, `storage`, `identity`, and `external_dependency` rather than assuming a specific cloud, container platform, database, or observability vendor.

Vendor integrations are optional adapters. Datadog is optional. Cloud-provider tools are optional. A filesystem-only workflow must still be usable.

## Validation

Install validation dependencies:

```bash
python -m pip install -r requirements.txt
```

Validate the reference context and contracts:

```bash
python scripts/validate_context.py examples/.infra-context
```

Inspect the provider-neutral eval suite:

```bash
python scripts/check_eval_output.py \
  evals/standard/incident-scenarios.json \
  dependency-latency-001 \
  examples/eval-output/dependency-latency-001.json
```

Before completing harness changes, run:

```bash
python scripts/validate_context.py examples/.infra-context
python -m compileall scripts hooks
```

## Repository map

- `docs/ARCHITECTURE.md` — harness architecture and boundaries
- `.infra-context/` — project-owned knowledge when adopted in a target repository
- `schemas/` — machine-readable contracts
- `skills/` — Claude Code skill adapter
- `.kiro/steering/` — Kiro steering adapter
- `AGENTS.md` — Codex/Kiro/cross-agent entry point
- `adapters/` — optional live evidence integrations
- `evals/standard/` — provider-neutral golden scenarios
- `workflows/` — production change workflow
