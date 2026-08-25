# Runbook — Database-backed API latency

## Trigger

Use when an API backed by a relational database shows elevated latency or timeout rates.

## Checks

1. Confirm the affected service and incident start time.
2. Check recent deployments and infrastructure changes.
3. Check application CPU and memory.
4. Check database CPU, connections, latency, lock waits, and slow queries.
5. Check CPU credit balance if the instance family is burstable.
6. Check downstream messaging or cache dependencies to rule out correlated failures.
7. Compare with known incident history.

## Interpretation

- Normal application CPU with high database latency suggests the bottleneck may be stateful dependency saturation rather than insufficient application tasks.
- CPU credit balance at zero plus sustained database CPU is strong evidence of burstable instance exhaustion.

## Before remediation

Document evidence, blast radius, rollback path, and expected result. Prefer a reviewed infrastructure change over direct production mutation.
