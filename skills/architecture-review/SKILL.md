---
name: architecture-review
description: Review infrastructure architecture proposals against current service context, architecture principles, ADRs, incident history, operational complexity, reliability, security, and cost. Use for migrations, new managed services, platform changes, or design reviews.
---

# Infrastructure Architecture Review

Evaluate proposals against the system that actually exists.

## Context loading

Load only relevant context:

1. `.infra-context/service-catalog.yaml`
2. Relevant architecture documents
3. Existing ADRs related to the affected domain
4. Production and security policy
5. Incident history when it reveals an operational constraint

## Review questions

- What problem is the proposal solving?
- Which existing constraints and dependencies matter?
- Does it conflict with an existing ADR?
- What new failure modes or operational burdens are introduced?
- What becomes simpler?
- What is the migration and rollback path?
- What observability is required?
- What are the security and cost trade-offs?
- Is a new ADR required?

## Required output

### Decision summary
Recommend: adopt, adopt with conditions, experiment, defer, or reject.

### Context
Summarize the current-state constraints that matter.

### Trade-offs
Explain benefits, costs, risks, and new operational responsibilities.

### Migration requirements
List prerequisites, validation steps, rollback requirements, and observability changes.

### ADR impact
Identify ADRs that must be created, superseded, or revisited.

### Context used
List the files that materially influenced the recommendation.

Do not present uncertain assumptions as established architecture facts.
