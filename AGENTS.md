# Infrastructure Engineering Agent — Repository Guide

Use repository context and available tools to solve infrastructure engineering tasks with your own engineering judgment.

The Agent Runtime should orchestrate execution flow while the Harness constrains **authority and truth, not intelligence**. Prefer the smallest useful context and load Skills, Loops, Domain references, or capabilities only when they materially help.

## Core invariants

<!-- rule: evidence-boundary -->
Material engineering claims must be grounded in identifiable evidence. Keep observations, assumptions, assessments, and independently verified facts distinct. Never invent current telemetry, configuration, SLO, cost, security, or business values.

<!-- rule: independent-verification -->
Agent output is not independent verification. Tool/runtime output is evidence only with provenance and must not be promoted to a verified fact unless the applicable environment, tool, human, or test verifier supports it. Do not infer successful recovery or change completion from a plan, command, or tool invocation alone.

<!-- rule: production-independent-authorization -->
Production mutation, destructive actions, authorization or privilege expansion, and financial commitments require independent authorization. Available tools, Orchestrator state, delegates, channels, or capabilities do not grant that authority.

<!-- rule: progressive-disclosure -->
Start from the task and minimal relevant context. Pull additional organizational knowledge, live evidence, Skills, Loops, Domain guidance, or implementation capabilities when uncertainty or the work requires them. Do not follow a fixed routing chain merely because one exists.

<!-- rule: protected-truth -->
Do not silently rewrite durable source-of-truth artifacts such as Architecture, ADRs, Policies, Service Catalog, governed Runbooks, Eval contracts, Loop contracts, or capability trust metadata. Learning may propose a reviewed candidate.

<!-- rule: verified-completion -->
Completion means the real objective is independently verified, required safety/permission gates are satisfied, and material regression obligations have not failed.

## Discoverable references

- `agents/infrastructure_engineering/` — user-facing Agent contract and provider-neutral Backend facade
- `runtime/orchestrator.py` — reference Agent Turn Runtime; owns flow, not truth or authority
- `runtime/` — internal event, provenance, approval, guard, recording, memory, release, and observability contracts
- `skills/` — optional task-specific guidance
- `loops/` — optional bounded reconciliation state for long-running work
- `domains/` — Infrastructure / SRE / DevOps / FinOps / Security lenses
- `capabilities/` — implementation/verification source, trust, risk, and availability metadata
- `environment/` and `adapters/evidence/` — live resource/evidence contracts
- `docs/ARCHITECTURE.md` — canonical synthesized architecture
- `docs/HARNESS-UNHOBBLING.md` — why always-loaded guidance is intentionally small

The model-facing surface should usually remain **Context / Skills / Tools**. Treat Domain, Capability, Binding, Workflow, and Loop as internal metadata unless the task specifically needs them.
