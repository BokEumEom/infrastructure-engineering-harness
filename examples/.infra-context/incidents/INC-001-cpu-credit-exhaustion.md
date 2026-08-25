# INC-001 — Database CPU credit exhaustion

## Summary

A production API experienced elevated latency while application task CPU remained normal.

## Signals

- API p95 latency increased significantly.
- Database CPU utilization was sustained at a high level.
- CPU credit balance reached zero.
- Database connections were near the expected upper operating range.
- Event-stream lag remained normal.

## Root cause

A burstable database instance was used for a sustained production workload. CPU credits were exhausted, which degraded database performance and propagated latency to the API.

## Resolution

Move the sustained production workload to a non-burstable instance family after capacity and cost review.

## Lesson

Do not treat normal ECS CPU as evidence that the application tier is healthy end-to-end. Check stateful dependencies before scaling application tasks.
