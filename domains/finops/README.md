# FinOps Pack

Use this pack when the decision concerns technology spend, cost ownership, allocation, usage efficiency, rate/commitment decisions, or cost relative to business value.

FinOps in this harness is not limited to one cloud provider. The same model can cover public cloud, SaaS, data platforms, AI services, data center, licenses, and other technology consumption.

## Context

Durable financial-operating context lives in `.infra-context/domains/finops.yaml` and conforms to `schemas/finops-profile.schema.json`.

Current spend, usage, rates, utilization and business-volume measurements belong in evidence bundles.

## Decision questions

1. Is spend allocated to an accountable owner and product/service scope?
2. Did cost rise because usage/value rose, or because unit efficiency deteriorated?
3. What is the relevant unit-economic metric?
4. Is an optimization opportunity safe given reliability, performance, security and contractual constraints?
5. Is a commitment/rate decision supported by stable demand and an appropriate horizon?
6. Are shared costs handled transparently?
7. Is the expected savings or cost avoidance worth the engineering effort and risk?

## Workflow

See `workflows/cost-value-review.md`.

## Eval

`evals/domains/finops.json` tests allocation, unit economics, usage optimization, commitment risk, shared cost and reliability trade-offs.

References:
- https://www.finops.org/framework/capabilities/allocation/
- https://www.finops.org/framework/capabilities/unit-economics/
- https://www.finops.org/framework/capabilities/usage-optimization/
