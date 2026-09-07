# Infrastructure Engineering Agent

The **Infrastructure Engineering Agent** is the user-facing product built on this repository.

It handles infrastructure work across six capability domains:

- Infrastructure — architecture, dependencies, capacity, IaC, migration;
- Operations — current state, incidents, resource health, operational action;
- DevOps — CI/CD, build, deployment, release, rollback;
- SRE — SLO, error budget, reliability, toil, recovery verification;
- FinOps — cost, allocation, efficiency, commitments, realized value;
- Security — trust boundaries, identity, privilege, exposure, supply chain.

These are lenses/capability domains inside one Agent, not separate Agents by default.

## Product model

```text
User / Channel
      ↓
normalized TurnRequest
      ↓
Agent Orchestrator / Turn Runtime
      ↓
Context + Memory + Skills + Tools
      ↓
Infrastructure Engineering Agent
      ↓
Model Judgment / next action
      ↓
Tool Executor
      ↓
Harness / Control Plane
Provenance · Scope · Fence · Guard · Approval
Change Revision · Audit · Recording
      ↓
Infrastructure Backend
      ↓
AWS / K8s / CI/CD / Observability / Cost / Security
      ↓
Independent Verification
   ↙             ↘
 done          reconcile only if needed
```

The model owns reasoning and next-action judgment. The Orchestrator owns turn flow. Neither owns credentials, engineering truth, approval state, production authority, or verified completion.

## Orchestrator / Turn Runtime

`runtime/orchestrator.py` is the provider-neutral reference application runtime.

It coordinates:

- channel-normalized requests;
- Context and available surface resolution;
- model calls;
- read-only tool iteration;
- model/tool budgets;
- trace/span correlation;
- independent verification;
- final `verified`, `unverified`, or budget-exceeded status.

The reference Orchestrator deliberately rejects workflow/change authority. Production mutation must remain behind resource provenance, ToolPipeline/ChangeControl, independent authorization, and the backend execution boundary.

> **Orchestrator owns flow, not truth or authority.**

## Model-visible surface

The model should primarily need:

```text
Context
Skills
Tools
```

Domain, Capability, Binding, Workflow, and Loop remain useful runtime metadata but are not a mandatory reasoning chain.

A future surface resolver should combine Capability Registry, invocation policy, release policy, discovered/connected systems, and resource/permission scope before each turn.

## Backend contract

`backend.py` is the provider-neutral integration facade. It currently separates:

```text
discover / collect evidence
          ↓
model judgment
          ↓
stage_change
          ↓
review / approval
          ↓
apply-time provenance + revision revalidation
          ↓
apply_approved_change
          ↓
verify_outcome
```

The facade is expected to evolve behind smaller typed Resource / Evidence / Change / Verification backend protocols rather than become one indefinitely generic API.

Platform credentials remain host/runtime-owned and are never passed to the model.

## Harness as internal control plane

The Harness is the non-optional boundary that constrains authority and truth:

- Runtime Event Log as execution SSOT;
- Evidence and Resource Provenance;
- untrusted external-data fencing;
- resource/permission scope;
- persistent user/session memory outside model state;
- Skill release controls;
- monotonic guards and policy enforcement;
- independently owned revision-bound approval;
- apply-time change revalidation;
- immutable recording/replay integrity;
- independent verification and regression obligations;
- protected organizational truth.

The product is the Agent. The Orchestrator runs the Agent. The Harness controls the safety/truth boundary.

## Runtime telemetry

The Runtime Event Log is canonical. Trace/span events, latency/cache metrics, recordings, and evaluation should be correlated to or projected from the same execution history.

```text
Runtime Event Log
  ├─ Trace
  ├─ Metrics
  ├─ Recording
  └─ Evaluation
```

This prevents observability helpers from becoming competing truth stores.

## Memory / prompt performance / release control

- **Persistent Memory** — user/session contextual state; model writes limited to session scope; memory is not verified engineering truth.
- **Prompt Performance** — stable global/session context before volatile turn context; cache/token/latency data are measurable without binding the core to one provider.
- **Skill Release Control** — `active`, deterministic `canary`, and `disabled` states owned by the host/runtime.

See `docs/MEMORY-PERFORMANCE-RELEASE.md`.

## Optional delegation

Single Agent is the default. Specialist delegation exists only as a scale-out mechanism when measured complexity justifies it.

Delegates are read-only by default, cannot exceed parent capability/resource scope, and cannot make newly named resources mutation-eligible.

See `docs/AWS-AGENTCORE-AIOPS-PATTERNS.md`.
