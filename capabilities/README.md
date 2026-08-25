# Capability Model

Capabilities are the implementation and operational knowledge layer used **after** the harness has resolved the engineering decision and constraints.

```text
Knowledge + Evidence
        ↓
Domain / Decision Skill
        ↓
Capability Routing
        ↓
Implementation Capability
        ↓
Code / Config / Procedure / Runbook
        ↓
Validation + Human/Policy Gate
        ↓
Execution System
        ↓
Loop Verification
```

## Why this is separate from Decision Skills

A Decision Skill answers **what should be done and why**. An implementation Capability answers **how to build, configure, inspect, or operate a specific technology**.

Examples:

- `architecture-review` decides whether a topology is appropriate.
- `kubernetes-ops` can provide Kubernetes implementation knowledge.
- `sre-review` decides whether reliability controls are sufficient.
- `opentelemetry` can provide telemetry implementation knowledge.

This separation prevents technology-specific instructions from silently overriding architecture, security, reliability, cost, or approval constraints.

## External Capability Sources

`registry.yaml` can point to external skill libraries. External sources are not automatically trusted executors.

Default policy for a third-party GitHub source:

1. pin an immutable commit revision;
2. record its license;
3. treat skill content as reference material;
4. never execute referenced scripts or commands automatically;
5. translate useful guidance into a local proposal, code/config diff, runbook, or verification plan;
6. apply normal harness policy, evidence, validation, and human gates;
7. promote a capability to `managed` only after organizational review/vendorization.

The initial reference source is BagelHole/DevOps-Security-Agent-Skills, pinned to the revision reviewed by this project. The harness intentionally selects a small subset instead of importing 160+ skills into every agent context.

## Build and Operate

Capability routing supports both build and operations work:

```text
Design → Build → Deploy → Operate → Observe → Improve → Learn
```

A build request may select delivery, cloud, orchestration and security capabilities. An operational incident may select observability, on-call, runbook and platform capabilities. The same production safety model applies to both.

## Registry validation

```bash
python scripts/validate_capability_registry.py capabilities/registry.yaml
```
