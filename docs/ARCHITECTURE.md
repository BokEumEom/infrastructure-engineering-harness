# Architecture

The harness separates durable knowledge, current evidence, domain reasoning, loop control and production execution.

```text
Durable Knowledge + Optional Live Evidence
                    ↓
              Context Resolution
                    ↓
               Domain Skill(s)
                    ↓
          Loop Engineering Control
      Observe → Decide → Act/Propose → Verify
         ↑                         ↓
         └──── Reconcile / Learn ──┘
                    ↓
        terminal: done/escalated/failed
                    ↓
 Incident / Runbook / ADR or Policy candidate / Eval
                    ↓
                 Next Loop
```

## Shared core

The core owns contracts that should not vary by model, provider or discipline: progressive context loading, service/dependency model, evidence/provenance, ADR/incident knowledge, change/ticket contracts, loop state and provider-neutral eval infrastructure.

## Domain packs vs Loops

A Domain Pack is a **lens**. A Skill is a **capability**. A Loop is the **control system** that composes Skills over time.

```text
Domain → what questions matter
Skill  → what the agent can do now
Loop   → when to repeat, verify, escalate, stop and learn
```

Loop state is explicit outside agent prose and is updated only with independently verified facts. A successful condition can remain a regression obligation in later iterations.

## Production boundary

The default loop may analyze, verify and create workflow artifacts, but production execution remains independently authorized. `change-validation` can orchestrate precheck → approval → external execution → post-verification, but the agent does not become the authorization boundary.

## Agent and tool adapters

Codex/Kiro use `AGENTS.md`; Claude Code additionally exposes Skills. Cloud/runtime/observability/delivery/cost systems are optional evidence adapters. Jira/Linear workflow actions use MCP. Tool output should be normalized before it is treated as evidence.

See `loops/README.md` and `docs/REFERENCE-MODELS.md`.
