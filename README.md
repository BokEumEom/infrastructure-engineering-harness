# Infrastructure Engineering Harness

**English** | [한국어](README.ko.md)

A provider-neutral, cross-agent harness for turning infrastructure knowledge and live evidence into reviewable engineering decisions.

> **Infrastructure Knowledge → Context → Agent → Code/Proposal → Human Review → Infrastructure**

The project is designed for **Codex, Kiro, Claude Code, and other agents** rather than one model or one infrastructure stack. It focuses on the layer before code: architecture knowledge, decisions, operational history, policy, evidence provenance, evaluation, and change control.

## Why this exists

Agents can already generate Terraform, manifests, scripts, and configuration quickly. The harder problem is giving them enough context to answer:

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
                  Validation / Eval / PR
                             ▼
                       Human Approval
                             ▼
                      Infrastructure
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/PRODUCTION-READINESS.md](docs/PRODUCTION-READINESS.md).

## Agent support

### Codex

`AGENTS.md` is the primary repository instruction file. Keep durable knowledge in `.infra-context/`; `AGENTS.md` acts as a map and operating contract.

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

## Provider-neutral context contract

A target project owns its knowledge:

```text
.infra-context/
├── service-catalog.yaml
├── architecture/
├── adr/
├── incidents/
├── policies/
└── runbooks/
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

## Production change workflow

The default harness stops at a reviewable proposal:

```text
Evidence → Recommendation → Change Proposal → Plan/Validation → PR → Human Approval → Deployment
```

`schemas/change-proposal.schema.json` requires evidence references, risk, blast radius, validation, rollback, and explicit approval. See [workflows/change-proposal.md](workflows/change-proposal.md).

## Safety model

Agent hooks are defense in depth, **not a security boundary**. Real production enforcement belongs in least-privilege IAM/RBAC, CI/CD approvals, protected branches, policy-as-code, audit logs, and deployment authorization outside the model.

The bundled Claude hook blocks several common direct mutation commands, but production pilots should begin with read-only access.

## Quick start

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

To adopt the context model in another repository, copy `examples/.infra-context` and adapt it to your system. Keep secrets and sensitive payloads out of agent context.

## Design principles

1. Evidence before action.
2. Progressive disclosure instead of loading the whole knowledge base.
3. Decisions and incident history are first-class context.
4. Provider and observability vendors are adapters, not core assumptions.
5. Recommendations carry provenance.
6. Production changes are reviewable and reversible.
7. Independent authorization remains outside the model.
8. Agent judgment is regression-tested with provider-neutral evals.

## License

MIT
