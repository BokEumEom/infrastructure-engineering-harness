# DevOps / Software Delivery Pack

Use this pack for build, test, release, deployment, rollback, change-risk, delivery-flow, and recovery questions.

## Context

Durable delivery context lives in `.infra-context/domains/devops.yaml` and conforms to `schemas/devops-profile.schema.json`.

Current delivery measurements should arrive as evidence rather than being hard-coded into the profile.

## Software delivery performance

The pack supports DORA's five current software delivery performance measures:

- change lead time
- deployment frequency
- failed deployment recovery time
- change failure rate
- deployment rework rate

Use trends for the same service as decision context; do not turn cross-team ranking into the goal.

## Decision questions

1. Where is flow time accumulating?
2. Is deployment instability creating rework?
3. Are changes small, testable, observable, and reversible?
4. Can a failed release recover safely and quickly?
5. Are quality gates meaningful or only ceremonial?
6. Does the deployment strategy match service criticality and rollback capability?
7. Is a change increasing delivery speed at the expense of reliability, or improving both?

## Workflow

See `workflows/delivery-review.md`.

## Eval

`evals/domains/devops.json` tests throughput, instability, rollback, batch-size, recovery and quality-gate decisions.

Reference: https://dora.dev/insights/dora-metrics-history/
