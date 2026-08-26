# Decision Skills and Capability Skills

Infrastructure Engineering Harness separates **engineering judgment** from **technology implementation knowledge**, then exposes trusted capability metadata to the Runtime Skill Registry.

## Model

```text
Organizational Knowledge + Current Evidence
                    ↓
             Domain Decision Skill
                    ↓
             Engineering Decision
                    ↓
             Capability Routing
                    ↓
       Implementation / Verification Capability
                    ↓
       Code / Config / Pipeline / Runbook / Procedure
                    ↓
             Review + Validation
                    ↓
              Runtime Kernel
         Skill / Tool / Guard / Approval
                    ↓
        Independently Authorized Execution
                    ↓
              Loop Verification
                    ↓
                  Learn
```

## Decision Skills

Decision Skills are intentionally provider-neutral. They decide architecture, reliability, delivery, cost, incident and change questions using durable context and evidence.

They must not outsource the engineering decision to a technology-specific reference.

## Capability Skills

Capability Skills encode implementation or operational know-how: Kubernetes, CI/CD, telemetry, cloud platforms, runbooks, security controls, supply-chain verification, and similar topics.

A capability may be:

- **local** — maintained in this repository;
- **managed** — reviewed and controlled by the adopting organization;
- **pinned reference** — third-party material at an immutable revision.

Pinned references never receive execution authority by registration alone.

## Runtime discovery

`capabilities/registry.yaml` is the durable trust/risk/source registry. `runtime/skill-policy.yaml` is a separate invocation-visibility overlay.

The split answers different questions:

```text
Capability Registry
→ where did this Skill come from?
→ what is its trust level and risk?
→ is it local, managed, or reference-only?

Runtime Skill Policy
→ may the model discover/load it?
→ may a human invoke it?
→ should it appear in the current catalog?
```

All directly discoverable local `skills/*/SKILL.md` entries must be represented as `harness-local` capabilities; CI checks this parity. This prevents a Runtime catalog from silently omitting a repository Skill.

The Runtime initially exposes bounded summaries and lazily loads Skill bodies. A third-party `reference_only` Skill may be readable by the model while still having `execution_authority: none`.

## Third-party skill libraries

A large external skill catalog is useful for breadth but introduces context, freshness and supply-chain concerns. The harness therefore does not copy every skill into the active agent context.

Instead:

1. register the source and immutable revision;
2. map only useful skills to intents;
3. route to the minimum relevant capability;
4. expose only bounded runtime summaries;
5. load reference material progressively;
6. generate local, reviewable artifacts;
7. validate locally;
8. execute only through separately authorized tools/systems;
9. verify outcomes through an Engineering Loop.

The first registered implementation reference library is `BagelHole/DevOps-Security-Agent-Skills` (MIT), selected for practical DevOps/SRE/Security implementation knowledge. Paperthin is separately registered for artifact/eval reflex references. Neither is an authorization boundary or runtime dependency.

## Build and operations examples

### Build

```text
"Build a new containerized API"
        ↓
architecture-review + sre-review
        ↓
Decision and constraints
        ↓
capability-routing
        ↓
kubernetes-ops + helm-charts + github-actions + opentelemetry
        ↓
reviewable manifests/pipeline/telemetry plan
        ↓
change-review
        ↓
Runtime guard / approval / external execution
```

### Operate

```text
"Latency alert is firing"
        ↓
incident-analysis
        ↓
verified hypothesis
        ↓
capability-routing
        ↓
opentelemetry + alerting-oncall + runbook-creation
        ↓
local diagnostic/operational artifacts
        ↓
incident-response loop verifies recovery and writes learning back
```

This is how the harness can support the lifecycle `Design → Build → Deploy → Operate → Observe → Improve → Learn` without granting arbitrary third-party instructions production authority.
