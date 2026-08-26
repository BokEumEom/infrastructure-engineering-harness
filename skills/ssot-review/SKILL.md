---
name: ssot-review
description: Audit one fact, decision, policy, or definition that appears across multiple artifacts and identify the canonical home. Start read-only, classify copies and contradictions, and propose references or reconciliation. Mutate only after explicit approval and never cross trust or permission boundaries silently.
---

# SSOT Review

Use this Skill when one maintained truth appears in several places and drift is possible.

## Goal

One fact should have one authoritative home. Other maintained surfaces should reference that home rather than carry independent copies, unless duplication is intentionally required by a boundary or delivery format.

## Workflow

1. Name the exact truth in scope. Do not audit the whole repository when only one fact or decision is at issue.
2. Search for all occurrences using at least two independent search formulations or paths.
3. Classify each occurrence as exact copy, paraphrase, partial, stale, contradictory, or intentional boundary copy.
4. Identify the strongest canonical home: closest to where the fact is owned, changed, reviewed, and enforced.
5. Record unique details that exist only in non-canonical copies so consolidation cannot lose information.
6. Separate contradictions from duplicates. Contradictions require an owner decision; do not infer the winner from recency alone.
7. Produce a read-only plan: canonical home, occurrence map, proposed reference/removal/reconciliation action, and any human decision required.
8. Only after explicit approval, apply the consolidation through the appropriate governed workflow.
9. Verify every remaining reference resolves and no unique detail was lost.

## Rules

- Audit is read-only by default.
- A clean result with no scatter is valid; do not invent work.
- Do not consolidate across public/private, tenant, customer/internal, security, legal, or other trust boundaries without explicit confirmation.
- Protected Harness knowledge remains governed by its owner and schema. Convenience does not make another file more authoritative.
- A reference is preferable to a duplicate when the consumer can follow it reliably.

## Output

Return the truth in scope, occurrence table, proposed canonical home, contradictions, mutation plan, and approval state.
