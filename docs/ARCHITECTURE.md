# Architecture

The harness separates **durable infrastructure knowledge**, **runtime evidence**, **agent reasoning**, and **production execution**.

```text
Durable Knowledge                     Optional Live Evidence
(service catalog, ADRs, policy,       (metrics, logs, traces, deploys,
incidents, runbooks)                  cloud/runtime state)
          │                                      │
          └──────────────┬───────────────────────┘
                         ▼
                  Context Resolver
               (progressive loading)
                         ▼
                 Infrastructure Agent
                         ▼
              Evidence-based Decision
                         ▼
                  Change Proposal
                         ▼
             Validation / Policy / Eval
                         ▼
                     Pull Request
                         ▼
                   Human Approval
                         ▼
                   Infrastructure
```

## Core vs adapters

The core is vendor-neutral:

- `AGENTS.md`
- `.infra-context/` contract
- JSON Schemas
- incident / architecture / change-review workflows
- evidence provenance
- provider-neutral evals
- change proposal workflow

Agent and tool integrations are adapters:

- Claude Code plugin/skills/hooks
- Kiro steering
- Codex `AGENTS.md`
- cloud APIs or CLIs
- observability platforms
- deployment systems
- source-control and CI/CD systems

No adapter is required for the core knowledge model. A team can start with repository context only and add live read-only evidence later.

## Progressive context loading

The agent should first resolve a service from the service catalog, then load only context that can change the decision. This prevents a large knowledge base from becoming an always-on prompt.

## Evidence normalization

Live integrations must normalize observations to `schemas/evidence.schema.json`. This makes reasoning independent of whether evidence originated from a cloud-native monitor, Prometheus, OpenTelemetry, Datadog, another APM, deployment history, or a human-provided incident artifact.

## Production boundary

The default architecture ends at a **reviewable proposal**. Direct production execution is intentionally outside the core agent loop. Organizations may automate execution separately, but should preserve independent authorization, policy checks, audit logs, and rollback controls.
