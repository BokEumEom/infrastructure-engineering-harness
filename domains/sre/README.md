# SRE Pack

Use this pack when the primary question is service reliability, user-visible objectives, incident risk, release risk from reliability state, or operational toil.

## Context

Durable SRE context lives in `.infra-context/domains/sre.yaml` and conforms to `schemas/sre-profile.schema.json`.

Current SLI values, burn rates, alert state, incident signals, and availability/latency observations belong in evidence bundles, not in durable policy files.

## Core concepts

- SLI: what is measured from the user/service perspective
- SLO: the objective for an SLI over a defined window
- Error budget: tolerated unreliability implied by the SLO
- Burn rate: how quickly that budget is being consumed
- Incident policy: severity, ownership, escalation, mitigation and postmortem expectations
- Toil: repetitive operational work that should be measured and reduced

## Decision questions

1. Which SLI and SLO represent the actual user impact?
2. Is the error budget healthy, at risk, or exhausted?
3. Is a fast or slow burn occurring?
4. Should a risky release continue, be constrained, or pause?
5. Is the alert actionable and tied to user impact?
6. Which mitigation reduces impact fastest without increasing blast radius?
7. What incident knowledge should become durable context afterward?

## Workflow

See `workflows/reliability-review.md`.

## Eval

`evals/domains/sre.json` tests error-budget, burn-rate, incident, SLI completeness, dependency risk, and toil decisions.

Reference: https://sre.google/sre-book/service-level-objectives/ and https://sre.google/sre-book/embracing-risk/
