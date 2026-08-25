# Infrastructure Engineering Pack

Use this pack for architecture, platform, capacity, migration, dependency, network-boundary, stateful-resource, and infrastructure change decisions.

## Context

Start with the shared service catalog and load only relevant:

- architecture
- ADRs
- incidents and runbooks
- production/security policy
- current runtime/capacity evidence

## Decision questions

1. Which capability or dependency is the real constraint?
2. What failure domains and blast radius change?
3. Is capacity actually insufficient, or is the bottleneck elsewhere?
4. Does the proposal conflict with an ADR or operating constraint?
5. What becomes operationally simpler or more complex?
6. Is the migration reversible and observable?
7. Does a stateful, identity, network, or destructive change require additional review?

## Workflow

See `workflows/architecture-capacity-review.md`.

## Eval

`evals/domains/infrastructure.json` checks provider-neutral architecture and capacity judgment. It does not require Terraform, Kubernetes, AWS, or any specific runtime.
