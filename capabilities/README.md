# Capability Model

Capabilities are the implementation, verification, and operational knowledge exposed to the **Infrastructure Engineering Agent** after current scope, evidence, and constraints are understood.

```text
User Intent + Evidence
        ↓
Infrastructure Engineering Agent
        ↓
Decision / Control Skill
        ↓
Capability Selection
        ↓
Implementation / Verification Capability
        ↓
Code / Config / Procedure / Runbook / Review
        ↓
Runtime Guard + Human/Policy Gate
        ↓
Execution / Verification
```

## Why this is separate from Decision Skills

A Decision Skill answers **what should be done and why**. An implementation Capability answers **how to build, configure, inspect, or operate a specific technology**. A verification/control Skill can add cross-cutting reflexes such as artifact hygiene, SSOT review, or eval integrity without becoming a new engineering Domain.

Examples:

- `architecture-review` decides whether a topology is appropriate.
- `kubernetes-ops` can provide Kubernetes implementation knowledge.
- `sre-review` decides whether reliability controls are sufficient.
- `opentelemetry` can provide telemetry implementation knowledge.
- `artifact-hygiene` checks that a changed artifact is clean and current.
- `eval-integrity` checks that an evaluation contains independent evidence rather than circular scoring.

This separation prevents technology-specific or low-level reference instructions from silently overriding architecture, security, reliability, cost, source-of-truth, or authorization constraints.

## Runtime Capability Sources vs Design References

`registry.yaml` contains only sources that may contribute entries to the Runtime Skill/Capability catalog.

A third-party project does **not** belong in this registry merely because it influenced the design. Design provenance belongs in `docs/REFERENCE-MODELS.md`.

Default policy for a third-party Runtime Capability source:

1. pin an immutable commit revision;
2. record its license;
3. treat its Skill content as reference material unless explicitly governed locally;
4. never execute referenced scripts or commands automatically;
5. expose only a small useful subset through the Capability Registry;
6. apply normal Runtime evidence, authorization, validation, and human gates;
7. promote a capability beyond `reference_only` only after local ownership/review.

Current external Runtime Capability source:

- `BagelHole/DevOps-Security-Agent-Skills` — selected DevOps, security, observability, CI/CD, runbook, and compliance implementation knowledge.

### Why Paperthin is no longer a Runtime Capability source

Paperthin remains an important **design/reference model**, but its key patterns have already been absorbed into locally governed Skills:

```text
Paperthin re0       → artifact-hygiene
Paperthin ssotize   → ssot-review
Paperthin mandela   → eval-integrity
Paperthin cycle     → loop-engineering / learning contracts
Paperthin prism     → independent cross-domain lenses
```

Keeping both the local adaptations and `paperthin-*` reference Skills in the model-visible catalog duplicated intent, increased Skill-selection ambiguity, and conflicted with the project's unhobbling/minimal-surface principle.

Paperthin attribution and design provenance therefore remain in `docs/REFERENCE-MODELS.md`, while the Runtime catalog exposes only the locally governed implementations.

## Build and Operate

Capability selection supports both build and operations work:

```text
Design → Build → Deploy → Operate → Observe → Improve → Learn
```

A build request may select delivery, cloud, orchestration and security capabilities. An operational incident may select observability, on-call, runbook and platform capabilities. Artifact-quality reflexes can run after either path before handoff. The same production safety model applies throughout.

## Registry validation

```bash
python scripts/validate_capability_registry.py capabilities/registry.yaml
```
