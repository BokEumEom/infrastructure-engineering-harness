---
name: architecture-review
description: Review infrastructure architecture proposals against provider-neutral service context, principles, ADRs, incident history, operational complexity, reliability, security, cost, and migration/rollback requirements.
---

# Infrastructure Architecture Review

Evaluate proposals against the system that actually exists, without assuming a specific cloud or runtime.

## Context loading

1. service catalog
2. affected architecture
3. related ADRs
4. production/security policy
5. incident history that reveals operational constraints
6. optional current evidence when the decision depends on actual utilization or behavior

## Review questions

- What problem is being solved?
- Which current constraints and dependencies matter?
- Does the proposal conflict with an ADR?
- Which failure modes and operational burdens are introduced or removed?
- What is the migration and rollback path?
- What evidence supports capacity/performance assumptions?
- What observability is required regardless of vendor?
- What are the security and cost trade-offs?
- Is a new ADR required?

## Output

Decision: adopt, adopt with conditions, experiment, defer, or reject; followed by context, trade-offs, evidence/assumptions, migration requirements, ADR impact, and context used.

Do not present uncertain assumptions as established facts.
