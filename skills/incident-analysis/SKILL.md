---
name: incident-analysis
description: Analyze infrastructure incidents using provider-neutral project context and current evidence. Use for latency, errors, saturation, availability, deployment, dependency, network, storage, or identity failures.
---

# Infrastructure Incident Analysis

## Goal

Produce the most defensible explanation of the incident and the safest useful next action.

Use your own engineering judgment about investigation order. Do not follow a fixed checklist when a different path is better supported by the evidence.

## Requirements

- distinguish confirmed impact from assumptions;
- cite material evidence and provenance; never invent current values;
- consider meaningful competing explanations when uncertainty matters;
- record evidence that supports and contradicts important hypotheses;
- expose material unknowns and the smallest useful evidence needed next;
- avoid production mutation as a way to test an unverified hypothesis;
- if remediation may impact production, prepare/review the change behind the applicable authorization boundary;
- do not claim recovery without current independent evidence.

## Useful context

Load only when relevant:

- service/dependency information;
- current telemetry, traces, logs, or provider state;
- recent changes;
- architecture/ADRs when the hypothesis or remediation depends on them;
- incidents/runbooks when they materially reduce uncertainty;
- production/security policy when an action or boundary is relevant.

## Output contract

Return the substance needed by the task, and when used in a Loop make these fields explicit:

- impact — confirmed vs assumed;
- assessment — leading explanation(s), confidence, and contradiction;
- evidence — identifiers/provenance for material claims;
- unknowns — evidence gaps that affect the decision;
- next action — the highest-value safe next step;
- remediation — only when evidence is sufficient, with risk/blast radius as applicable.

## Loop handoff

When invoked by Loop Engineering, emit the shared `loop_handoff` contract. The handoff is a control signal, not authoritative evidence. The model may select the next useful action; the Loop/Runtime decides whether authority, evidence, budget, regression, or terminal conditions permit it.
