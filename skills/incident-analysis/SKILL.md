---
name: incident-analysis
description: Analyze infrastructure incidents using provider-neutral project context, evidence provenance, incident history, runbooks, and policy. Use for latency, errors, saturation, availability, deployment, dependency, network, storage, or identity failures.
---

# Infrastructure Incident Analysis

Analyze incidents using evidence before recommending changes.

## Context loading

1. service catalog
2. relevant architecture
3. relevant production/security policy
4. relevant incidents and runbooks
5. ADRs only when remediation changes architecture or conflicts with a recorded decision
6. optional live evidence normalized to `schemas/evidence.schema.json`

Do not require a specific cloud, runtime, datastore, or observability vendor.

## Workflow

1. Identify affected service, criticality, impact and start time.
2. Check recent deployment/configuration changes when evidence exists.
3. Map critical dependencies.
4. Gather service and dependency evidence.
5. Generate multiple hypotheses.
6. Rank them using supporting and contradicting evidence.
7. Specify the minimum checks that can confirm/reject the leading hypothesis.
8. Propose remediation only when evidence is sufficient.
9. For production-impacting remediation, produce a change proposal rather than executing it.

## Required output

- Impact: confirmed impact vs assumptions.
- Evidence: material signals with provenance references; never invent values.
- Hypotheses: ranked causes with supporting/contradicting evidence and confidence.
- Verification: smallest checks needed to reduce uncertainty.
- Remediation: reversible actions with risk/blast radius.
- Context used: context and evidence IDs that materially influenced the conclusion.

## Loop-compatible handoff

When invoked by `loop-engineering`, also emit:

```yaml
loop_handoff:
  event: <stable event such as impact_confirmed or hypothesis_verified>
  outcome: progress | no_progress | blocked | verified | failed | escalated
  evidence_refs: []
  verified_conditions: []
  assumptions: []
  next_action:
    type: skill | action | wait | human_gate | terminal
    target: <next target>
  writeback_candidates: []
```

The handoff is a control signal, not authoritative evidence. Do not place an assumption in `verified_conditions`, and do not declare incident recovery without an independent recovery check.

## Safety

Do not directly execute production mutations as part of incident analysis.
