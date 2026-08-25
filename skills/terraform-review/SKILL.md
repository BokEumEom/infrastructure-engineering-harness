---
name: terraform-review
description: Review Terraform changes using project architecture, service criticality, ADRs, naming conventions, and production policy. Use for Terraform PR reviews, module design reviews, or infrastructure change-risk analysis.
---

# Terraform Review

Review Terraform as an infrastructure decision, not only as syntax.

## Context loading

Read context progressively:

1. `.infra-context/service-catalog.yaml`
2. Relevant service architecture
3. Applicable production/security policy
4. Relevant ADRs
5. Incident history only when it materially affects the proposed change

## Review dimensions

Evaluate:

- reliability and failure modes
- blast radius
- security and IAM scope
- data durability
- deployment and rollback behavior
- naming and ownership consistency
- observability requirements
- cost implications
- maintainability and module boundaries
- compatibility with documented ADRs

## Required output

### Summary
State what the change does and its overall risk.

### Findings
Classify findings as critical, high, medium, low, or note. Tie each finding to a concrete resource or design decision.

### Missing context
State which unknowns prevent a confident decision.

### Recommended changes
Prefer the smallest safe improvement. Do not rewrite working Terraform without a material reason.

### Context used
List the project context files that influenced the review.

## Rules

- Do not approve a production-impacting change solely because `terraform validate` passes.
- Treat stateful resources, network boundaries, IAM, and destructive lifecycle changes as high-scrutiny areas.
- Flag architecture changes that lack an ADR.
- Prefer explicit human review for production changes.
