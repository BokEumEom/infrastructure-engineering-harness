# Decision Skills and Capability Skills

Infrastructure Engineering Harness separates **engineering judgment** from **technology implementation knowledge**.

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

## Third-party skill libraries

A large external skill catalog is useful for breadth but introduces context, freshness and supply-chain concerns. The harness therefore does not copy every skill into the active agent context.

Instead:

1. register the source and immutable revision;
2. map only useful skills to intents;
3. route to the minimum relevant capability;
4. read reference material progressively;
5. generate local, reviewable artifacts;
6. validate locally;
7. execute only through separately authorized tools/systems;
8. verify outcomes through an Engineering Loop.

The first registered reference library is `BagelHole/DevOps-Security-Agent-Skills` (MIT), selected for practical DevOps/SRE/Security implementation knowledge. It is a reference source, not an authorization boundary or runtime dependency.

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
