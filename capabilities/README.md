# Capability Model

Capabilities are the implementation, verification, and operational knowledge layer used **after** the harness has resolved the engineering decision and constraints.

```text
Knowledge + Evidence
        ↓
Domain / Decision Skill
        ↓
Capability Routing
        ↓
Implementation / Verification Capability
        ↓
Code / Config / Procedure / Runbook / Review
        ↓
Validation + Human/Policy Gate
        ↓
Execution System
        ↓
Loop Verification
```

## Why this is separate from Decision Skills

A Decision Skill answers **what should be done and why**. An implementation Capability answers **how to build, configure, inspect, or operate a specific technology**. A verification/control Capability can add cross-cutting reflexes such as artifact hygiene, SSOT review, or eval integrity without becoming a new engineering Domain.

Examples:

- `architecture-review` decides whether a topology is appropriate.
- `kubernetes-ops` can provide Kubernetes implementation knowledge.
- `sre-review` decides whether reliability controls are sufficient.
- `opentelemetry` can provide telemetry implementation knowledge.
- `artifact-hygiene` checks that a changed artifact is clean, current, and safe to hand off.
- `eval-integrity` checks that an evaluation has an independent signal rather than circular scoring.

This separation prevents technology-specific or low-level reference instructions from silently overriding architecture, security, reliability, cost, source-of-truth, or approval constraints.

## External Capability Sources

`registry.yaml` can point to external skill libraries. External sources are not automatically trusted executors.

Default policy for a third-party GitHub source:

1. pin an immutable commit revision;
2. record its license;
3. treat skill content as reference material;
4. never execute referenced scripts or commands automatically;
5. translate useful guidance into a local proposal, code/config diff, runbook, verification plan, or governed local Skill;
6. apply normal harness policy, evidence, validation, and human gates;
7. promote a capability to `managed` only after organizational review/vendorization.

Current reference sources:

- `BagelHole/DevOps-Security-Agent-Skills` — selected DevOps, security, observability, CI/CD, runbook, and compliance implementation knowledge;
- `LilMGenius/paperthin` — selected low-level artifact hygiene, SSOT, eval-integrity, cycle-learning, restart, and cross-lens review patterns.

Both are pinned to reviewed commit revisions and remain `reference_only`. The harness intentionally selects a small subset instead of importing entire catalogs into every agent context.

## Build and Operate

Capability routing supports both build and operations work:

```text
Design → Build → Deploy → Operate → Observe → Improve → Learn
```

A build request may select delivery, cloud, orchestration and security capabilities. An operational incident may select observability, on-call, runbook and platform capabilities. Artifact reflexes can run after either path before handoff. The same production safety model applies throughout.

## Registry validation

```bash
python scripts/validate_capability_registry.py capabilities/registry.yaml
```
