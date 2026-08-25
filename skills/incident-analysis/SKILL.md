---
name: incident-analysis
description: Analyze infrastructure incidents using provider-neutral project context, evidence provenance, incident history, runbooks, and policy. Use for latency, errors, saturation, availability, deployment, dependency, network, storage, or identity failures.
---

# Infrastructure Incident Analysis

Analyze incidents using evidence before recommending changes.

## Context loading

1. `.infra-context/service-catalog.yaml`
2. relevant architecture
3. relevant production/security policy
4. relevant incidents and runbooks
5. ADRs only when the remediation changes architecture or conflicts with a recorded decision
6. optional live evidence normalized to `schemas/evidence.schema.json`

Do not require a specific cloud, runtime, datastore, or observability vendor. Datadog is optional.

## Workflow

1. Identify affected service, criticality, impact, and start time.
2. Check recent deployment/configuration changes when evidence exists.
3. Map critical dependencies.
4. Gather service and dependency evidence.
5. Generate multiple hypotheses.
6. Rank them using supporting and contradicting evidence.
7. Specify the minimum checks that can confirm/reject the leading hypothesis.
8. Propose remediation only when evidence is sufficient.
9. For production-impacting remediation, produce a change proposal following `workflows/change-proposal.md`.

## Required output

### Impact
Confirmed impact vs assumptions.

### Evidence
For every material signal, include its evidence/provenance reference. Never invent values.

### Hypotheses
Ranked causes with supporting evidence, contradicting evidence, and confidence.

### Verification
Smallest checks needed to reduce uncertainty.

### Remediation
Prefer reversible actions and state risk/blast radius.

### Context used
List context and evidence IDs that materially influenced the conclusion.

## Safety

Do not directly execute production mutations as part of incident analysis.
