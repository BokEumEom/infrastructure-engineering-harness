---
name: ssot-review
description: Identify the canonical home of a fact duplicated across maintained artifacts. Use for source-of-truth drift or consolidation reviews.
---

# SSOT Review

Use this Skill when one maintained truth appears in several places and drift is possible.

## Goal

One fact should have one authoritative home. Other maintained surfaces should reference that home rather than carry independent copies, unless duplication is intentionally required by a boundary or delivery format.

## Workflow

1. Name the exact truth in scope. Do not audit the whole repository when only one fact or decision is at issue.
2. Search for occurrences within scope. Add search formulations or paths when the initial results leave a material risk of missing alternate wording or maintained copies.
3. Classify each occurrence as exact copy, paraphrase, partial, stale, contradictory, or intentional boundary copy.
4. Identify the strongest canonical home: closest to where the fact is owned, changed, reviewed, and enforced.
5. Record unique details that exist only in non-canonical copies so consolidation cannot lose information.
6. Separate contradictions from duplicates. Contradictions require an owner decision; do not infer the winner from recency alone.
7. Identify the canonical home, occurrences, proposed actions, and any unresolved owner decisions. For an audit-only request, return these findings without editing.
8. Complete consolidation already authorized by the user when the canonical source and meaning are clear and only unprotected documents within the same trust and visibility boundary are affected. Request a decision or approval for ambiguous authority, contradictory facts, protected source-of-truth changes, or boundary changes; continue independent authorized work. Existing authorization applies only to its stated scope, and protected changes still use the appropriate governed workflow.
9. Verify every remaining reference resolves and no unique detail was lost.

## Rules

- Audit is read-only by default.
- A clean result with no scatter is valid; do not invent work.
- Do not consolidate across public/private, tenant, customer/internal, security, legal, or other trust boundaries without explicit confirmation.
- Protected Harness knowledge remains governed by its owner and schema. Convenience does not make another file more authoritative.
- A reference is preferable to a duplicate when the consumer can follow it reliably.

## Output

Return the truth in scope, occurrence table, proposed canonical home, contradictions, mutation plan, and approval state.
