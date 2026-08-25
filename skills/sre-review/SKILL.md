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

Do not recommend a risky release solely because delivery throughput is desirable when reliability policy says otherwise.
