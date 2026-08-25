# Domain Packs

The harness has one shared core and multiple engineering lenses.

```text
Knowledge + Evidence
        ↓
   Harness Core
        ↓
┌────────┼─────────┬─────────┐
│        │         │         │
Infrastructure   SRE      DevOps    FinOps
Architecture   Reliability Delivery  Cost/Value
Capacity       SLO        Change    Allocation
Failure modes  Incident   Recovery  Unit economics
```

A domain pack does not create a separate source of truth. It adds domain-specific context, review questions, workflows, and evals on top of the same service catalog, architecture, ADRs, incidents, policies, and evidence bundle.

Use more than one pack when a decision crosses disciplines. Keep each conclusion attributable to its lens instead of collapsing trade-offs into a single generic recommendation.

- `infrastructure/` — architecture, capacity, dependency and change-risk decisions
- `sre/` — reliability, SLI/SLO, error budget, incidents and toil
- `devops/` — software delivery, release risk, rollback and delivery performance
- `finops/` — allocation, technology cost, usage optimization, commitments and unit economics
