---
name: sre-review
description: Review reliability using SLI/SLO, error budgets, burn rates, incident context, dependency risk and toil. Use for SRE decisions, release reliability checks, incident policy, SLO reviews, or reliability prioritization.
---

# SRE Review

Read `domains/sre/README.md` and the applicable SRE profile from the selected context root.

Use current SLI, burn-rate, alert and incident values only when provided as evidence or available through read-only tools. Never invent them.

Required output:

1. Reliability state — healthy, at-risk, budget-exhausted, acute incident, chronic risk, or insufficient evidence.
2. User impact and relevant SLI/SLO.
3. Evidence/provenance IDs.
4. Error-budget interpretation when applicable.
5. Immediate mitigation or verification.
6. Release/change guidance.
7. Reliability follow-up and durable knowledge to capture.
8. Cross-domain implications for Infrastructure, DevOps or FinOps.

## Loop-compatible handoff

When invoked inside `incident-response` or `reliability-improvement`, also emit a `loop_handoff` using the shared contract in `skills/loop-engineering/SKILL.md`.

Use stable events such as `baseline_recorded`, `error_budget_exhausted_requires_policy_action`, `recovery_verified`, `post_change_reliability_verified`, or `reliability_regressed`. Only include independently supported conditions in `verified_conditions`.

A reliability loop is not complete until post-change/current-state evidence verifies the relevant objective and required regression obligations pass.

Do not recommend a risky release solely because delivery throughput is desirable when reliability policy says otherwise.
