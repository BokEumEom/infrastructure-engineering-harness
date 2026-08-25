# ADR-001 — Prefer non-burstable instances for sustained production databases

## Status

Accepted

## Context

High-criticality production database workloads can sustain CPU demand for long periods. Burstable instances depend on CPU credits and may degrade after those credits are exhausted.

## Decision

For sustained, high-criticality production database workloads, prefer non-burstable instance families. A burstable instance may be used only when workload evidence and an explicit capacity review justify it.

## Consequences

- Capacity cost may be higher than the smallest burstable option.
- Performance is more predictable under sustained load.
- Changes to existing database instance families still require normal capacity, cost, and rollback review.

## Revisit when

- the workload becomes intermittent rather than sustained
- a managed/serverless option materially changes the capacity model
- measured utilization demonstrates a different cost/performance optimum
