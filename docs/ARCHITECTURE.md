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
                  Review Artifact
        (PR / ticket / runbook / procedure)
                         ▼
                   Human Approval
                         ▼
                   Execution System
                         ▼
                   Infrastructure
```

## Core vs adapters

The core is vendor-neutral and delivery-method-neutral:

- `AGENTS.md`
- structured context contract
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
- ITSM/change-management systems
- approved operator procedures

No adapter is required for the core knowledge model. A team can start with repository or central context only and add live read-only evidence later.

## Embedded and central modes

The context model can be embedded in a service/infrastructure repository or stored in a central platform/SRE workspace. In central mode, service repositories and operational systems remain read-only sources and the harness owns the cross-service knowledge model.

## Progressive context loading

The agent should first resolve a service or domain from the service catalog, then load only context that can change the decision. This prevents a large knowledge base from becoming an always-on prompt.

## Evidence normalization

Live integrations must normalize observations to `schemas/evidence.schema.json`. This makes reasoning independent of whether evidence originated from a cloud-native monitor, Prometheus, OpenTelemetry, Datadog, another APM, deployment history, a source repository, or a human-provided incident artifact.

## Infrastructure delivery is optional

The harness does not require Terraform or infrastructure-as-code. A proposal may be realized as:

- an IaC/configuration pull request;
- an approved change ticket;
- a reviewed runbook;
- a controlled console/API procedure;
- an automation script executed by an independently authorized system;
- a hybrid of these approaches.

The invariant is the engineering control around the change: evidence, risk, blast radius, validation, recovery/rollback, and independent authorization.

## Production boundary

The default architecture ends at a **reviewable proposal and review artifact**. Direct production execution is intentionally outside the core agent loop. Organizations may automate execution separately, but should preserve independent authorization, policy checks, audit logs, and rollback/recovery controls.
