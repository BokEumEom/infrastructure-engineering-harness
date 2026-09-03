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
Evidence · Resource Provenance · State · Guard · Approval · Permission
         ↓
Infrastructure Backend
         ↓
AWS / K8s / CI/CD / Observability / Cost / Security systems
         ↓
Independent Verification
         ↓
Verified Outcome
```

The model owns reasoning and next-action judgment. It does not own credentials, independent truth, approval state, production authority, or verified completion.

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
- Context/Skill progressive disclosure;
- Guard and policy enforcement;
- independent approval;
- state persistence;
- regression obligations;
- independent verification;
- Skill / Context / Harness Lift evaluation.

The product is the Agent. The harness is part of how the Agent is built and governed.
