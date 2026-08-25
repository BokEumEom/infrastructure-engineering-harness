---
name: change-review
description: Review infrastructure-as-code, configuration, and platform changes using service criticality, architecture, ADRs, policy, evidence, failure modes, and rollback requirements. Provider-neutral; use for Terraform, OpenTofu, Pulumi, CloudFormation, Kubernetes manifests, or other infrastructure changes.
---

# Infrastructure Change Review

Review a change as an infrastructure decision, not only as syntax.

## Context loading

1. service catalog
2. affected architecture
3. production/security policy
4. relevant ADRs
5. relevant incident history
6. evidence or plan output when available

## Review dimensions

- reliability and failure modes
- blast radius
- authorization/security scope
- data durability
- rollout and rollback behavior
- observability and verification
- cost/capacity implications
- maintainability and ownership
- architecture/ADR compatibility
- unknowns that prevent a confident decision

## Required output

### Summary
What changes and overall risk.

### Findings
Critical/high/medium/low/note, each tied to a concrete change or decision.

### Evidence and assumptions
Cite evidence IDs and separate assumptions.

### Missing context
State what prevents a confident approval.

### Recommended changes
Prefer the smallest safe improvement.

### Change proposal impact
If production-impacting, verify that the proposal includes risk, blast radius, validation, rollback, and explicit approval.

## Loop-compatible handoff

When invoked by `change-validation`, emit the shared `loop_handoff` contract from `skills/loop-engineering/SKILL.md`.

Use stable events such as `preconditions_verified`, `production_change_requires_approval`, `post_change_outcome_verified`, `verification_inconclusive`, `rollback_required`, or `regression_obligation_failed`.

Pre-change validation and post-change verification are different phases. Do not reuse a successful plan/precheck as proof that the actual environment reached the desired state. Post-change success requires current environment evidence and passed regression obligations.

Do not approve a change solely because a syntax validator or dry-run succeeds.
