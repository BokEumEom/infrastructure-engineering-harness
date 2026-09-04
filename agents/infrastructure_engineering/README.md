# Infrastructure Engineering Agent

The **Infrastructure Engineering Agent** is the user-facing product built on this repository.

It handles infrastructure engineering work across six capability domains:

- Infrastructure — architecture, dependencies, capacity, IaC, migration;
- Operations — current state, incidents, resource health, operational action;
- DevOps — CI/CD, build, deployment, release, rollback;
- SRE — SLO, error budget, reliability, toil, recovery verification;
- FinOps — cost, allocation, efficiency, commitments, realized value;
- Security — trust boundaries, identity, privilege, exposure, supply chain.

These domains are capabilities/lenses inside one agent. The user should not need to decide whether a task is "Ops" or "SRE" before asking for help.

## Product model

```text
User Intent
    ↓
Infrastructure Engineering Agent
    ↓
Model Judgment
  ↙      ↓       ↘
Context Skills Capabilities
  ↘      ↓       ↙
       Action
         ↓
Agent Runtime / Harness Control Plane
Evidence · Resource Provenance · Fence · State · Guard · Approval · Permission
Memory · Cache/Latency · Skill Release · Recording
         ↓
Infrastructure Backend
         ↓
AWS / K8s / CI/CD / Observability / Cost / Security systems
         ↓
Independent Verification
         ↓
Verified Outcome
```

The model owns reasoning and next-action judgment. It does not own credentials, independent truth, approval state, Skill release state, production authority, or verified completion.

## Backend contract

`backend.py` is the provider-neutral seam inspired by agent systems that keep business/platform credentials and hard write rules behind a server-owned backend.

The contract separates:

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

A real AWS, Kubernetes, GitHub, GitLab, Datadog, Prometheus, or other adapter implements these operations using credentials held by the host/runtime, not by the model.

## Harness as internal architecture

"Harness" remains a useful engineering term, but it is no longer the product identity.

Within this project it means the internal control mechanisms that make the Agent dependable:

- Runtime Event Log;
- Evidence and Resource provenance;
- untrusted external-data fencing;
- Context/Skill progressive disclosure and capability-aware projection;
- persistent user/session memory outside model state;
- cache-aware context assembly and latency metrics/budgets;
- Skill canary and hard kill-switch release control;
- Guard and policy enforcement;
- independently owned, revision-bound approval;
- immutable runtime recording/replay integrity;
- state persistence;
- regression obligations;
- independent verification;
- Skill / Context / Harness Lift evaluation.

The product is the Agent. The harness is part of how the Agent is built and governed.

## Memory / prompt performance / release control

The reference runtime now adds three operational layers:

1. **Persistent Memory** — SQLite-backed `user` and `session` memory. Model writes are limited to session memory; user-scope persistence requires user/trusted-runtime authority. Memory is context, not verified fact.
2. **Prompt Performance** — context is assembled as stable `global → session` prefix plus `volatile` suffix. Cache-read/write tokens, model/tool latency, turns, calls, and latency budgets are measurable without assuming a specific model provider.
3. **Skill Release Control** — `active`, deterministic `canary`, and `disabled` states sit in front of the Runtime Skill Registry. `disabled` is a hard kill switch owned by the host/runtime.

See `docs/MEMORY-PERFORMANCE-RELEASE.md`.

## Commerce-agent-derived runtime rules

The current reference runtime implements several patterns from Anthropic's Commerce Agents architecture:

- mutation targets can be gated against resources actually discovered in the current Resource Graph;
- unavailable or disabled Skills can be projected out of the model-visible surface;
- external text can be bounded and fenced as untrusted data;
- approvals bind to the exact staged change/policy/resource-graph revision and are one-shot;
- Runtime Events can be snapshotted into an integrity-checked recording;
- persistent memory, cache-aware prompt layout, and Skill release controls remain runtime state rather than prompt instructions.

These are deterministic reference contracts. Live provider adapters must invoke the same gates immediately before real production execution.

See `docs/COMMERCE-AGENT-PATTERNS.md`.
