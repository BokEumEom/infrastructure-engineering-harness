---
name: delivery-review
description: Review software delivery flow, deployment risk, rollback, quality gates and DORA software delivery performance signals. Use for DevOps, release, deployment, CI/CD, change-flow, recovery or delivery-performance questions.
---

# DevOps / Delivery Review

Read `domains/devops/README.md` and the applicable delivery profile from the selected context root.

Treat delivery metrics as evidence, not goals to optimize independently. Prefer trends for the same service and look for flow/stability trade-offs.

Required output:

1. Delivery state and affected value-stream step.
2. Evidence for throughput or instability.
3. Release/change risk.
4. Rollback and failed-deployment recovery assessment.
5. Missing or weak quality gates.
6. Smallest improvement that benefits flow and stability.
7. Reliability implications and cross-domain handoffs.

## Loop-compatible handoff

When invoked by `delivery-improvement`, also emit the shared `loop_handoff` contract from `skills/loop-engineering/SKILL.md`.

Prefer stable events such as `baseline_recorded`, `constraint_identified`, `progress_verified`, `cross_team_constraint`, or `delivery_instability_regressed`. A delivery improvement must be compared with its previous service-level baseline; do not mark success because one metric improved while a protected stability or reliability obligation regressed.

A successful build or syntax validation is not sufficient production approval.
