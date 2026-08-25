# Infrastructure Engineering Harness

**English** | [한국어](README.ko.md)

A provider-neutral, cross-agent harness for turning infrastructure knowledge and live evidence into reviewable engineering decisions.

> **Infrastructure Knowledge → Context → Agent → Decision/Proposal → Human Review → Infrastructure**

The project is designed for **Codex, Kiro, Claude Code, and other agents** rather than one model, one cloud, or one infrastructure delivery method. It focuses on the layer before execution: architecture knowledge, decisions, operational history, policy, evidence provenance, evaluation, and change control.

## Why this exists

Agents can already generate infrastructure-as-code, manifests, scripts, configuration, runbooks, and operational procedures quickly. The harder problem is giving them enough context to answer:

- Why is this change appropriate for this system?
- What past decision or incident constrains it?
- What current evidence supports the diagnosis?
- What is the blast radius and rollback path?
- What should remain under independent human/production control?

## Core architecture

```text
Durable Infrastructure Knowledge          Optional Live Evidence
Service catalog / ADR / incidents         Metrics / logs / traces
Policy / runbooks / architecture          runtime / deploy / status
              │                                  │
              └──────────────┬───────────────────┘
                             ▼
                    Progressive Context
                             ▼
                    Infrastructure Agent
                             ▼
                   Evidence-based Decision
                             ▼
                      Change Proposal
                             ▼
          Validation / Policy / Eval / Review
                             ▼
        PR / Change Ticket / Approved Runbook
                             ▼
                       Human Approval
                             ▼
                      Infrastructure
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/PRODUCTION-READINESS.md](docs/PRODUCTION-READINESS.md).

## Agent support

### Codex

`AGENTS.md` is the primary repository instruction file. Keep durable knowledge in structured context; `AGENTS.md` acts as a map and operating contract.

### Kiro

Kiro supports `AGENTS.md`; this repository also includes `.kiro/steering/infrastructure-harness.md` as a workspace steering adapter.

### Claude Code

The repository includes a Claude Code plugin adapter with Skills, reviewer agent, and a defensive `PreToolUse` hook:

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

Skills:

```text
/infra-harness:incident-analysis
/infra-harness:change-review
/infra-harness:architecture-review
```

## Usage modes

The harness does **not** require every service repository to contain agent files. Two adoption modes are supported conceptually.

### Mode A — Embedded context

Use this when a service or infrastructure repository should own its own operational knowledge.

```text
service-repository/
├── AGENTS.md
├── application-or-infrastructure-files/
└── .infra-context/
    ├── service-catalog.yaml
    ├── architecture/
    ├── adr/
    ├── incidents/
    ├── policies/
    └── runbooks/
```

Typical request:

```text
Analyze the current latency incident using AGENTS.md and .infra-context.
Separate evidence from assumptions, rank hypotheses, and do not make a production change.
```

### Mode B — Central harness / platform workspace

Use this when a platform, SRE, or infrastructure team wants to keep service repositories unchanged.

```text
infrastructure-harness-workspace/
├── AGENTS.md
├── schemas/
├── evals/
├── workflows/
├── adapters/
└── contexts/
    ├── payment-platform/
    ├── identity-platform/
    └── shared-network/

service repositories / monitoring / runtime systems
                 │
                 └── read-only sources
```

In this mode, the harness repository is the reasoning/control workspace. Service repositories, deployment history, monitoring systems, cloud/runtime APIs, and status feeds are read-only evidence sources.

Typical request:

```text
Analyze the payment-platform incident using contexts/payment-platform.
Inspect the payment service repository only as a read-only source.
Use current evidence if available. Produce hypotheses, verification steps, and a change proposal only if justified.
```

This mode is often a better fit for organizations where architecture boundaries span multiple repositories.

## Provider-neutral context contract

A context set uses the same knowledge categories whether it is embedded in a service repository or stored centrally:

```text
service-catalog.yaml
architecture/
adr/
incidents/
policies/
runbooks/
```

The reference data intentionally avoids assuming ECS, Kubernetes, a specific database, AWS, or a particular observability product. Component types are expressed as capabilities such as `compute`, `datastore`, `messaging`, `network`, `storage`, `identity`, and `external_dependency`.

## Context schemas and CI validation

Machine-readable contracts live in `schemas/`:

- service catalog
- incident knowledge
- ADR
- policy
- live evidence/provenance
- change proposal
- eval suite

Run:

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

GitHub Actions runs the same validation on pushes and pull requests.

## Live evidence: optional adapters

The core works without live integrations. Add read-only adapters when you need current state.

Datadog is **optional**. A team can use Prometheus, OpenTelemetry backends, cloud-native monitoring, another APM, or repository-only evidence. Cloud providers are also adapters rather than assumptions in the reasoning model.

All integrations should normalize data to `schemas/evidence.schema.json` before reasoning. See [adapters/README.md](adapters/README.md).

## Evidence and provenance

A recommendation should be traceable to stable evidence IDs, including source type, observation time, signal, component, and source/query/resource reference when available. This keeps "the agent says so" from becoming an operational justification.

## Provider-neutral evaluation

`evals/standard/incident-scenarios.json` contains **30 golden incident scenarios** spanning compute, datastore, messaging, cache, network, identity, deployment, storage, external dependencies, availability, and observability gaps.

The scenarios test judgment such as "do not scale a healthy tier when the bottleneck is downstream" rather than testing a vendor-specific service name.

Example:

```bash
python scripts/check_eval_output.py \
  evals/standard/incident-scenarios.json \
  dependency-latency-001 \
  examples/eval-output/dependency-latency-001.json
```

## Terraform or IaC is not required

The harness is not a Terraform workflow and does not require infrastructure-as-code.

A change proposal can result in different execution artifacts depending on the environment:

```text
IaC-managed environment
Evidence → Proposal → Code/Config Diff → Plan/Dry Run → PR → Approval → Deployment

Non-IaC managed service
Evidence → Proposal → Change Ticket → Approved Console/API Procedure → Approval → Operator Execution

Operational procedure
Evidence → Proposal → Reviewed Runbook → Maintenance Window → Approval → Operator Execution

Hybrid environment
Evidence → Proposal → Script/Config/API Change → Validation → Controlled Pipeline or Operator
```

Examples of environments that may not use Terraform include vendor-managed SaaS, managed network appliances, legacy systems, database operations, hardware platforms, cloud resources maintained through another control system, or teams that deliberately use approved console/API workflows.

The harness requirement is not "produce Terraform." The requirement is:

- cite evidence;
- state risk and blast radius;
- define validation;
- define rollback or recovery;
- use an independently authorized execution path.

## Production change workflow

The default harness stops at a reviewable proposal:

```text
Evidence → Recommendation → Change Proposal → Validation → Review Artifact → Human Approval → Execution System
```

The review artifact can be a **pull request, change ticket, approved runbook, plan, or controlled procedure**.

`schemas/change-proposal.schema.json` requires evidence references, risk, blast radius, validation, rollback, and explicit approval. See [workflows/change-proposal.md](workflows/change-proposal.md).

## Practical incident example

Suppose a request-serving service shows high end-to-end latency while the service compute layer remains healthy and a critical datastore dependency is saturated.

The agent should reason like this:

```text
Current evidence
├── service compute utilization: normal
├── dependency connection utilization: high
└── dependency operation latency: high

Historical context
└── previous dependency saturation incident

Decision
├── primary hypothesis: dependency saturation
├── do not scale healthy compute without evidence
├── verify connection pressure / slow operations / recent changes
└── produce a reversible change proposal only after verification
```

The same reasoning should work whether the service runs on containers, virtual machines, serverless compute, physical hosts, or a managed platform.

## Safety model

Agent hooks are defense in depth, **not a security boundary**. Real production enforcement belongs in least-privilege IAM/RBAC, CI/CD approvals, protected branches, change-management controls, policy-as-code, audit logs, and deployment/operations authorization outside the model.

The bundled Claude hook blocks several common direct mutation commands, but production pilots should begin with read-only access.

## Quick start

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

For embedded mode, copy `examples/.infra-context` into a target repository. For central mode, use the same context structure under a service/domain-specific directory in your harness workspace. Keep secrets and sensitive payloads out of agent context.

## Design principles

1. Evidence before action.
2. Progressive disclosure instead of loading the whole knowledge base.
3. Decisions and incident history are first-class context.
4. Provider and observability vendors are adapters, not core assumptions.
5. IaC is optional; engineering controls are not.
6. Recommendations carry provenance.
7. Production changes are reviewable and reversible.
8. Independent authorization remains outside the model.
9. Agent judgment is regression-tested with provider-neutral evals.

## License

MIT
