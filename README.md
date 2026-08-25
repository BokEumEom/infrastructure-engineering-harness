# Infrastructure Engineering Harness

**English** | [한국어](README.ko.md)

A provider-neutral, cross-agent harness for turning infrastructure knowledge and current evidence into reviewable engineering decisions across **Infrastructure Engineering, SRE, DevOps, and FinOps**.

> **Infrastructure Knowledge → Context → Agent → Decision/Proposal → Human Review → Infrastructure**

The project is designed for **Codex, Kiro, Claude Code, and other repository-aware agents**. It does not require one cloud, one runtime, Terraform, Kubernetes, Datadog, or any particular CI/CD, cost, or ticketing platform.

## Why this exists

Agents can already generate IaC, configuration, scripts, runbooks and operational procedures. The harder problem is giving them enough organizational context to decide **what should change, why, with what evidence, and under which constraints**.

This harness makes Architecture, ADRs, incidents, operating policy, reliability objectives, delivery rules, cost ownership and current evidence usable as agent context.

## Architecture

```text
Durable Knowledge + Optional Live Evidence
                    ↓
              Context Resolution
                    ↓
               Harness Core
                    ↓
      ┌─────────────┼─────────────┐
Infrastructure     SRE          DevOps        FinOps
Architecture   Reliability    Delivery      Cost/Value
Capacity       SLO/Budget     Recovery      Allocation
Failure modes  Incidents      Stability     Unit economics
      └─────────────┼─────────────┘
                    ↓
          Evidence-based Decision
                    ↓
              Change Proposal
                    ↓
       Validation / Eval / Review
                    ↓
 PR / Ticket / Runbook / Controlled Procedure
                    ↓
              Human Approval
                    ↓
                Execution
```

See [Architecture](docs/ARCHITECTURE.md) and [Production Readiness](docs/PRODUCTION-READINESS.md).

## Domain packs

The shared core is reused by four engineering lenses:

| Pack | Use it for | Additional context |
| --- | --- | --- |
| [Infrastructure](domains/infrastructure/README.md) | architecture, capacity, migration, dependency and change risk | architecture, ADR, runtime/capacity evidence |
| [SRE](domains/sre/README.md) | SLI/SLO, error budgets, incidents, reliability, toil | `domains/sre.yaml` |
| [DevOps](domains/devops/README.md) | build/release/deployment, rollback, delivery performance | `domains/devops.yaml` |
| [FinOps](domains/finops/README.md) | allocation, usage efficiency, commitments, unit economics | `domains/finops.yaml` |

Use multiple packs for cross-domain decisions. A cost optimization that violates an SLO should remain visible as a FinOps opportunity **and** an SRE constraint, not become an averaged generic recommendation.

## Agent support

### Codex

Use the repository `AGENTS.md` as the operating contract. It routes tasks to the appropriate domain pack and context.

### Kiro

Kiro can use `AGENTS.md`; `.kiro/steering/infrastructure-harness.md` provides an additional workspace steering adapter.

### Claude Code

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

Skills include:

```text
/infra-harness:incident-analysis
/infra-harness:architecture-review
/infra-harness:change-review
/infra-harness:sre-review
/infra-harness:delivery-review
/infra-harness:finops-review
/infra-harness:ticketing
```

## Usage modes

### A. Embedded context

Put the context with a service or infrastructure repository:

```text
service-repository/
├── AGENTS.md
└── .infra-context/
    ├── service-catalog.yaml
    ├── architecture/
    ├── adr/
    ├── incidents/
    ├── policies/
    ├── runbooks/
    └── domains/
        ├── sre.yaml
        ├── devops.yaml
        └── finops.yaml
```

Example:

```text
Analyze the latency incident using .infra-context.
Use Infrastructure and SRE lenses. Separate evidence from assumptions and do not execute a production change.
```

### B. Central harness / platform workspace

Keep service repositories unchanged and manage organizational context centrally:

```text
harness-workspace/
├── AGENTS.md
├── contexts/
│   ├── payment-platform/
│   ├── identity-platform/
│   └── shared-network/
└── read-only sources
    ├── service repositories
    ├── runtime / observability
    ├── deployment systems
    └── cost / business data
```

Example:

```text
Analyze payment-platform using contexts/payment-platform.
The proposed capacity reduction affects cost and reliability, so use Infrastructure, SRE and FinOps packs.
Treat external systems as read-only and produce a proposal only if the evidence is sufficient.
```

See [Central Context Example](examples/central-context/README.md).

## Example: one decision, four lenses

A service has stable traffic, high capacity headroom, a 99.9% SLO, healthy error budget, a reversible deployment path, and rising monthly cost.

- **Infrastructure** checks whether capacity is genuinely oversized and whether failure modes change.
- **SRE** checks whether reduced capacity can still satisfy the SLO and error-budget policy.
- **DevOps** checks rollout, validation, rollback and failed-deployment recovery.
- **FinOps** checks unit cost, allocation, expected savings and whether engineering effort/risk is justified.

The final proposal contains the trade-offs and evidence from each lens before approval.

## Context and schemas

Machine-readable contracts live in `schemas/` for service catalog, incidents, ADRs, policy, evidence, change proposals, ticket requests/policies, domain profiles and eval suites.

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

## Optional live evidence adapters

The core works without live integrations. Add read-only adapters only when current state is required.

Possible sources include Prometheus, OpenTelemetry backends, Datadog, cloud-native monitoring, runtime APIs, source control, deployment history, SLO tooling, cost/usage systems and business metrics. **Datadog is optional.** Normalize results to `schemas/evidence.schema.json`.

## MCP-first Jira / Linear ticket automation

Ticket creation is implemented as a **workflow action through MCP**, not as Jira REST or Linear GraphQL code inside the harness.

```text
Incident / Review / Change Proposal
              ↓
         Ticket Request
              ↓
     Policy + Deduplication
              ↓
     Official Remote MCP Server
       ├─ Atlassian Rovo MCP
       └─ Linear MCP
              ↓
       Search → Create/Update
```

The harness owns the provider-neutral rules:

- `schemas/ticket-request.schema.json` — what work should be tracked
- `schemas/ticket-policy.schema.json` — `disabled`, `manual`, or policy-based `auto_create`
- stable SHA-256 fingerprint for deduplication
- search-before-create
- evidence/source references in every generated ticket

The provider MCP server owns authentication, permissions and actual Jira/Linear tool calls.

Example policy:

```yaml
mode: policy
default_action: manual
rules:
  - id: high-severity-incident
    when:
      kinds: [incident]
      severities: [sev1, sev2]
    action: auto_create
    require_evidence: true
    min_evidence: 2
```

This can automatically create a well-evidenced SEV1/SEV2 follow-up while leaving FinOps or architecture recommendations in manual mode.

Official MCP endpoints used by the examples:

```text
Atlassian Rovo MCP  https://mcp.atlassian.com/v1/mcp/authv2
Linear read/write  https://mcp.linear.app/mcp
Linear read-only   https://mcp.linear.app/mcp/readonly
```

See [MCP connections](mcp/README.md), [Ticketing workflow](workflows/ticketing.md), and [Ticketing adapter](adapters/actions/ticketing/README.md).

## Provider-neutral evaluation

The repository includes:

- 30 provider-neutral incident scenarios in `evals/standard/`
- Infrastructure domain scenarios
- SRE error-budget/reliability scenarios
- DevOps delivery/recovery scenarios
- FinOps allocation/unit-economics scenarios

Example:

```bash
python scripts/check_domain_eval.py \
  evals/domains/sre.json \
  error-budget-exhausted \
  examples/eval-output/domain-sre-error-budget.json
```

## Terraform or IaC is not required

The change artifact depends on the environment:

```text
IaC-managed        Proposal → Code/Config → Plan → PR → Approval
Non-IaC service    Proposal → Change Ticket → Console/API Procedure → Approval
Operational work   Proposal → Reviewed Runbook → Maintenance Window → Approval
Hybrid             Proposal → Script/Config/API Change → Controlled Pipeline/Operator
```

The common contract is evidence, risk, blast radius, validation, recovery and independent approval — not Terraform.

## Safety model

Agent-side hooks are defense-in-depth, not a security boundary. Real production enforcement belongs outside the model in IAM/RBAC, deployment/change approvals, policy-as-code, protected branches, audit systems and other independent controls.

Ticket creation permission is intentionally separate from production mutation permission. Do not auto-approve broad MCP write tool sets simply because ticket automation is enabled.

## Quick start

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python -m unittest discover -s tests
```

## Reference models

- Google SRE — SLOs and error budgets: https://sre.google/sre-book/service-level-objectives/
- DORA software delivery performance: https://dora.dev/insights/dora-metrics-history/
- FinOps Framework: https://www.finops.org/framework/
- Atlassian Rovo MCP: https://support.atlassian.com/atlassian-ai-gateway/docs/set-up-clients/
- Linear MCP: https://linear.app/docs/mcp

## License

MIT
