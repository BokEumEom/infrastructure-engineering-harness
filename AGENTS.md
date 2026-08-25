# Infrastructure Engineering Harness — Agent Guide

This is the cross-agent operating contract for Codex, Kiro, Claude Code adapters, and other agents that can read repository instructions.

## Prime directive

Treat infrastructure work as an **evidence-based engineering decision**, not a code-generation task.

Before recommending a material production change:

1. resolve the target service/scope and criticality;
2. load only relevant durable context;
3. select the engineering domain lens or lenses;
4. separate confirmed evidence from assumptions;
5. use current evidence when the decision depends on current state;
6. compare with ADRs, incidents, policies and constraints;
7. state risk, blast radius, validation and rollback/recovery;
8. produce a reviewable proposal rather than directly mutating production.

## Context roots

Use an explicitly supplied context path first.

Otherwise:

- Embedded mode: `.infra-context/`
- Central mode: `contexts/<service-or-platform>/`

A context root may contain:

```text
service-catalog.yaml
architecture/
adr/
incidents/
policies/
runbooks/
domains/
  sre.yaml
  devops.yaml
  finops.yaml
```

Do not load the whole knowledge base by default.

## Domain routing

Load the relevant domain pack before making domain-specific recommendations:

- architecture, capacity, dependencies, migration, infrastructure change → `domains/infrastructure/README.md`
- SLI/SLO, error budget, incidents, reliability, toil → `domains/sre/README.md`
- build, release, deployment, rollback, delivery performance → `domains/devops/README.md`
- cost, allocation, usage efficiency, commitments, unit economics → `domains/finops/README.md`

For cross-domain decisions, use multiple packs and keep conclusions separated by lens. Example: a capacity reduction may be financially attractive but violate an SRE objective; surface the trade-off instead of averaging it away.

## Context loading order

1. service catalog / ownership
2. relevant architecture
3. applicable domain profile
4. production/security/financial policy
5. relevant incidents and runbooks
6. relevant ADRs
7. current evidence from optional read-only adapters

## Evidence contract

Material recommendations should be traceable to evidence IDs conforming to `schemas/evidence.schema.json`.

Evidence may come from metrics, logs, traces, runtime state, deployments, delivery systems, SLO systems, cost/usage datasets, business metrics, incident history, or human-provided artifacts.

Never invent telemetry, cost, business-volume, SLO, or delivery values.

## Provider and tool neutrality

Core reasoning must not assume a particular cloud, container platform, database, observability product, IaC tool, CI/CD system, or cost platform.

Datadog, Terraform, Kubernetes, AWS, GitHub and similar products are adapters or execution choices, not core requirements.

## Safety contract

- Prefer read-only discovery and evidence collection.
- Do not directly apply/delete infrastructure, mutate production data, broaden authorization, purchase commitments, or bypass deployment/change controls.
- Production changes follow `workflows/change-proposal.md`.
- Hooks are defense-in-depth, not a security boundary.
- Real enforcement belongs in independently authorized systems: IAM/RBAC, CI/CD, change management, policy-as-code, protected branches, approval workflows, and audit controls.

## Validation

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/check_eval_output.py evals/standard/incident-scenarios.json dependency-latency-001 examples/eval-output/dependency-latency-001.json
python scripts/check_domain_eval.py evals/domains/sre.json error-budget-exhausted examples/eval-output/domain-sre-error-budget.json
python -m compileall scripts hooks
```

## Repository map

- `domains/` — Infrastructure, SRE, DevOps, FinOps domain packs
- `schemas/` — machine-readable context/evidence/change/eval contracts
- `evals/` — provider-neutral regression scenarios
- `skills/` — Claude Code skill adapter
- `.kiro/steering/` — Kiro steering adapter
- `adapters/` — optional read-only live evidence integrations
- `workflows/` — production change workflow
- `examples/` — embedded and central usage examples
