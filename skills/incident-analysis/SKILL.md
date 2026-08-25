---
name: incident-analysis
description: Analyze infrastructure incidents using project architecture, service metadata, incident history, runbooks, and policy. Use when latency, errors, CPU, database, deployment, availability, or dependency failures are reported.
---

# Infrastructure Incident Analysis

Analyze incidents using evidence before recommending changes.

## Context contract

Project-specific context lives under `.infra-context/` in the target repository.

Load context progressively in this order:

1. `.infra-context/service-catalog.yaml`
2. Relevant `.infra-context/architecture/*`
3. Relevant `.infra-context/incidents/*`
4. Relevant `.infra-context/runbooks/*`
5. Applicable `.infra-context/policies/*`
6. ADRs only when a remediation would change architecture or contradict an existing decision

Do not load every context file by default.

## Workflow

1. Identify the affected service and user impact.
2. Determine when the incident started.
3. Check recent deployments or infrastructure changes.
4. Identify the service's critical dependencies.
5. Gather infrastructure, application, database, and dependency evidence.
6. Compare symptoms with known incidents and runbooks.
7. Generate multiple hypotheses.
8. Rank hypotheses by supporting and contradicting evidence.
9. Recommend verification steps before modification.
10. Propose remediation only when evidence is sufficient.

## Required output

### Impact
Describe affected services and likely user impact. Distinguish confirmed facts from assumptions.

### Evidence
List the signals that materially support the analysis.

### Hypotheses
Rank likely causes. For each one include supporting evidence, contradicting evidence, and confidence.

### Verification
Provide the smallest set of checks that can confirm or reject the leading hypotheses.

### Remediation
Only propose remediation when the evidence supports it. Prefer reversible changes and state risk.

### Context used
List the context files that influenced the conclusion.

## Safety

Never execute or instruct automatic execution of production-changing commands as part of incident analysis.

Do not:

- run `terraform apply` or `terraform destroy`
- mutate production databases
- change IAM policies
- delete cloud resources
- restart critical production systems without explicit human approval

If a destructive action appears necessary, produce a change proposal and verification plan instead.
