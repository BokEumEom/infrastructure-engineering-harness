---
name: finops-review
description: Review technology cost and value using allocation, usage efficiency, unit economics, rate or commitment opportunities, reliability constraints and business context. Use for FinOps, cost anomaly, rightsizing, allocation, commitments, unit-cost or optimization questions.
---

# FinOps Review

Read `domains/finops/README.md` and the applicable FinOps profile from the selected context root.

Current cost, usage, utilization, rate and business-volume values must come from evidence. Datadog or any cloud billing product is optional.

Required output:

1. Cost/value classification.
2. Scope, owner and allocation quality.
3. Total-cost and unit-economic interpretation.
4. Evidence/provenance IDs.
5. Optimization type: allocation, usage, rate/commitment, architecture/workload placement, or insufficient evidence.
6. Expected value or savings with uncertainty when measurable.
7. Reliability, security, contractual and operational constraints.
8. Recommendation and approval requirements.

## Loop-compatible handoff

When invoked by `finops-optimization`, emit the shared `loop_handoff` contract from `skills/loop-engineering/SKILL.md`.

Prefer stable events such as `opportunity_verified`, `realized_value_measured`, `commitment_purchase_requires_approval`, `reliability_constraint_blocks_optimization`, or `reliability_regressed`.

Expected savings are not a terminal result. A FinOps loop should compare expected and realized cost/value after the authorized change and preserve reliability and allocation traceability as regression obligations.

Never infer waste from total spend growth alone. Never recommend a commitment purchase without demand evidence and organizational approval.
