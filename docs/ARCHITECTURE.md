# Architecture

The harness separates durable knowledge, current evidence, domain reasoning and production execution.

```text
Durable Knowledge                     Optional Live Evidence
service catalog / ADR / policy        metrics / logs / traces / SLO
incidents / runbooks / domain policy  runtime / delivery / cost / business
          │                                      │
          └──────────────┬───────────────────────┘
                         ▼
                  Context Resolution
                 progressive loading
                         ▼
                  Shared Harness Core
                         ▼
        ┌────────────────┼────────────────┐
        │                │                │
Infrastructure         SRE             DevOps           FinOps
architecture       reliability       delivery         cost/value
capacity           SLO/budget        recovery         allocation
failure modes      incidents         stability        unit economics
        └────────────────┬────────────────┘
                         ▼
                Evidence-based Decision
                         ▼
                   Change Proposal
                         ▼
          Validation / Policy / Eval / Review
                         ▼
 PR / Change Ticket / Approved Runbook / Controlled Procedure
                         ▼
                   Human Approval
                         ▼
                   Execution System
```

## Shared core

The core owns contracts that should not vary by model, cloud or discipline:

- context discovery and progressive loading
- service ownership and dependency model
- evidence/provenance
- ADR and incident knowledge
- safety and change-proposal contract
- provider-neutral eval infrastructure

## Domain packs

Domain packs add a lens, not a new truth source. They define domain-specific durable context, questions, workflows and evals. Cross-domain decisions preserve separate findings so reliability, delivery, architecture and cost trade-offs stay visible.

## Agent adapters

- Codex and compatible agents: `AGENTS.md`
- Kiro: `AGENTS.md` plus `.kiro/steering/`
- Claude Code: Skills, reviewer agent and defensive hooks

## Tool adapters

Cloud APIs, runtime systems, observability platforms, deployment systems, cost/usage sources and source control are optional adapters. Normalize current observations to `schemas/evidence.schema.json` before reasoning.

## Production boundary

The default harness ends at a reviewable proposal or approved procedure. Direct production execution is outside the core loop. Organizations that automate execution should preserve independent authorization, policy checks, auditability and recovery controls.
