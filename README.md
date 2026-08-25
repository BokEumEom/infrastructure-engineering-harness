# Infrastructure Engineering Harness

**English** | [한국어](README.ko.md)

A provider-neutral, cross-agent harness for turning infrastructure knowledge and current evidence into reviewable engineering decisions and governed implementation across **Infrastructure Engineering, SRE, DevOps, FinOps, and Security**.

> **Knowledge → Context → Decision Skill → Capability → Loop → Verified Outcome → Learning → Next Loop**

The project is designed for **Codex, Kiro, Claude Code, and other repository-aware agents**. It does not require one cloud, runtime, IaC tool, observability product, CI/CD system, cost platform, security product, or ticketing system.

## Why this exists

Agents can already generate IaC, configuration, scripts, pipelines, runbooks and operational procedures. The harder problem is deciding **what should change, why, with what evidence, under which constraints, which implementation knowledge is appropriate, and how the real outcome is verified**.

This harness separates those responsibilities:

```text
Organizational Knowledge + Current Evidence
                    ↓
               Domain Lens
                    ↓
               Decision Skill
        what should change and why?
                    ↓
             Capability Routing
          how should it be built?
                    ↓
       Implementation / Verification Skill
                    ↓
        Reviewable Local Artifact
                    ↓
       Validation + Human/Policy Gate
                    ↓
     Independently Authorized Execution
                    ↓
           Loop Verification + Learn
```

This separation lets the harness use broad implementation knowledge without allowing technology-specific or third-party instructions to silently become architecture decisions or production authority.

See [Architecture](docs/ARCHITECTURE.md), [Capability Model](docs/CAPABILITY-MODEL.md), [Loop Engineering](loops/README.md), [Reference Models](docs/REFERENCE-MODELS.md), and [Production Readiness](docs/PRODUCTION-READINESS.md).

## Build and operate

The harness is designed to support the full engineering lifecycle:

```text
Design → Build → Deploy → Operate → Observe → Improve → Learn
  ↑                                                   │
  └───────────────────────────────────────────────────┘
```

Typical supported work includes:

- architecture and migration review
- infrastructure/application platform build planning
- IaC, configuration, CI/CD and deployment artifact generation
- observability and alerting design
- runbook and operational procedure generation
- incident analysis and recovery verification
- SLO/error-budget review
- change review and rollback design
- FinOps optimization and realized-value verification
- security/trust-boundary review
- MCP/workflow tool review
- supply-chain and access-review planning
- Jira/Linear ticket workflow through MCP

The default harness **does not directly own production execution**. It can produce and validate the artifacts required for execution; Level 3 controlled execution requires independent credentials, authorization, policy and audit controls.

### Example: build a new service

```text
User requirement
  "Build a containerized public API with CI/CD,
   vendor-neutral telemetry and an operational runbook."
                    ↓
architecture-review + sre-review + security-review
                    ↓
Engineering decision and constraints
                    ↓
capability-routing
                    ↓
Kubernetes / Helm / CI/CD / OpenTelemetry / Runbook capabilities
                    ↓
Local manifests / pipeline / telemetry config / runbook
                    ↓
change-review
                    ↓
External execution after approval
                    ↓
change-validation loop
```

If the real platform is unknown, the agent must not guess a cloud, Kubernetes, GitHub Actions, GitLab CI, Terraform or any other implementation technology.

### Example: operate an existing service

```text
Latency alert / user report
          ↓
incident-analysis
          ↓
Current evidence + historical context
          ↓
Verified hypothesis
          ↓
capability-routing when technology-specific guidance is needed
          ↓
Observability / runbook / platform capability
          ↓
Mitigation proposal or operational artifact
          ↓
incident-response loop
          ↓
Verify recovery → regression check → learn
```

## Domain packs

The shared core is reused by five engineering lenses:

| Pack | Use it for | Additional context |
| --- | --- | --- |
| [Infrastructure](domains/infrastructure/README.md) | architecture, capacity, migration, dependencies, change risk | architecture, ADR, runtime/capacity evidence |
| [SRE](domains/sre/README.md) | SLI/SLO, error budgets, incidents, reliability, toil | `domains/sre.yaml` |
| [DevOps](domains/devops/README.md) | build/release/deployment, rollback, delivery performance | `domains/devops.yaml` |
| [FinOps](domains/finops/README.md) | allocation, usage efficiency, commitments, unit economics | `domains/finops.yaml` |
| [Security](domains/security/README.md) | trust boundaries, identity/privilege, sensitive data, external integrations, supply chain | `domains/security.yaml` |

A Domain is a **lens**. A Decision Skill is **engineering judgment**. A Capability is **implementation/verification knowledge**. A Loop is the **control system** that verifies outcomes over time.

```text
Domain      → what questions and constraints matter?
Decision    → what should be done and why?
Capability  → how can it be implemented or verified?
Loop        → when to repeat, verify, escalate, stop and learn?
```

## Decision Skills and Capability Skills

Directly discoverable local skills stay under `skills/` for compatibility with Claude Code and other Agent Skills consumers.

Local skills are primarily:

```text
Decision
├── architecture-review
├── incident-analysis
├── change-review
├── sre-review
├── delivery-review
├── finops-review
└── security-review

Control / Workflow
├── capability-routing
├── loop-engineering
└── ticketing
```

Technology-specific implementation and verification knowledge is selected through `capabilities/registry.yaml` rather than loaded into every prompt.

### External reference capability library

The initial external reference source is:

```text
BagelHole/DevOps-Security-Agent-Skills
revision: 0365f57a079b1332f95cf26e31dd2d5332a8399f
license: MIT
trust: pinned_reference
execution: reference_only
```

The harness currently maps only a focused subset:

- Kubernetes operations
- Helm charts
- GitHub Actions / GitLab CI
- OpenTelemetry
- alerting/on-call
- runbook creation
- threat modeling
- MCP server security
- SBOM / software supply chain
- policy-as-code
- access review

This repository does **not** automatically vendor or execute all 160+ external skills.

For a third-party capability:

1. use the immutable revision registered in `capabilities/registry.yaml`;
2. load only the capability relevant to the task;
3. treat commands, scripts and assets as reference material;
4. never automatically execute them;
5. translate useful guidance into local reviewable code/config/runbook/procedure;
6. apply local evidence, policy, Security and Change Review;
7. execute only through independently authorized tools/systems;
8. verify the real outcome through a Loop.

An organization can later vendor/review selected capabilities and promote them from `pinned_reference` to a managed local source.

See [Capabilities](capabilities/README.md) and [Capability Model](docs/CAPABILITY-MODEL.md).

## Capability routing example

```text
/infra-harness:capability-routing

Decision:
The service should run as a containerized workload with rolling deployment,
99.9% availability objective and vendor-neutral telemetry.

Turn this decision into reviewable build artifacts.
Use capabilities/registry.yaml, select the minimum capabilities,
do not execute production changes, and do not guess unknown platform facts.
```

Expected flow:

```text
Decision refs
    ↓
Capability selection
    ↓
Source + pinned revision
    ↓
Local artifact generation
    ↓
Validation
    ↓
Change/Security review
    ↓
External execution or approval gate
```

See [Capability Routing Example](examples/capability-routing/README.md).

## Loop Engineering

Loop Engineering is an execution layer above Skills and Capabilities. Use it when the task cannot be safely completed as a one-shot answer.

Reference loops:

| Loop | Purpose |
| --- | --- |
| `incident-response` | investigate → verify hypothesis → propose mitigation → verify recovery → learn |
| `reliability-improvement` | baseline SLO/error budget → prioritize → track → remeasure → learn |
| `delivery-improvement` | baseline delivery → find constraint → improve → remeasure → learn |
| `finops-optimization` | inform → optimize → track/operate → measure realized value → learn |
| `change-validation` | precheck → independent approval → external execution → post-verify → regression check |

Loop contracts provide:

1. **External state** — loop state is explicit and survives model/context resets.
2. **Independent verification** — `verified_by: agent` is invalid; facts require environment, tool, human, or test evidence.
3. **Bounded execution** — iteration, duration and no-progress budgets prevent indefinite loops.
4. **Regression obligations** — previously achieved guarantees remain checks in later iterations.

A model cannot self-certify `done`.

## Agent support

### Codex

Use root `AGENTS.md` as the cross-agent operating contract. It routes decisions, implementation capability selection and repeated work.

### Kiro

Kiro can use `AGENTS.md`; `.kiro/steering/infrastructure-harness.md` remains an additional workspace adapter.

### Claude Code

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

Primary local skills include:

```text
/infra-harness:incident-analysis
/infra-harness:architecture-review
/infra-harness:change-review
/infra-harness:sre-review
/infra-harness:delivery-review
/infra-harness:finops-review
/infra-harness:security-review
/infra-harness:capability-routing
/infra-harness:ticketing
/infra-harness:loop-engineering
```

## Usage modes

### A. Embedded context

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
        ├── finops.yaml
        └── security.yaml
```

### B. Central harness / platform workspace

Service repositories can remain unchanged while Platform/SRE/Infrastructure teams manage organizational knowledge centrally:

```text
harness-workspace/
├── AGENTS.md
├── contexts/
│   ├── payment-platform/
│   ├── identity-platform/
│   └── shared-network/
├── capabilities/
└── read-only sources
    ├── service repositories
    ├── runtime / observability
    ├── deployment systems
    └── cost / business data
```

See [Central Context Example](examples/central-context/README.md).

## Machine-readable contracts

`schemas/` contains contracts for service catalog, incidents, ADRs, policies, evidence, change proposals, ticketing, capability registry, domain profiles and Loop Engineering.

Relevant contracts include:

```text
capability-registry.schema.json  source trust + capability routing metadata
security-profile.schema.json     security/trust/identity durable context
loop-spec.schema.json            what a loop should do
loop-state.schema.json           externally maintained execution state
loop-result.schema.json          terminal outcome and learning
loop-eval-suite.schema.json      long-horizon regression scenarios
```

Validation:

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/validate_capability_registry.py capabilities/registry.yaml
python scripts/check_domain_eval.py \
  evals/domains/security.json \
  mcp-write-boundary \
  examples/eval-output/domain-security-mcp-boundary.json
python scripts/check_loop_eval.py \
  evals/loops/standard.json \
  incident-recovered \
  examples/eval-output/loop-incident-recovered.json
python -m unittest discover -s tests
```

## Optional live evidence adapters

The core works without live integrations. Add read-only adapters only when current state is required. Sources can include Prometheus, OpenTelemetry, Datadog, cloud-native monitoring, runtime APIs, source control, deployment history, SLO tooling, cost/usage systems and business metrics. **Datadog is optional.** Normalize current observations to `schemas/evidence.schema.json` before treating them as facts.

## MCP-first Jira / Linear ticket automation

Ticket creation is a workflow action through MCP rather than Jira REST or Linear GraphQL code embedded in the harness.

```text
Incident / Review / Loop
          ↓
     Ticket Request
          ↓
 Policy + Deduplication
          ↓
   Remote MCP Server
          ↓
 Search → Create/Update
```

The Security lens keeps workflow write permission separate from production mutation permission.

See [MCP connections](mcp/README.md) and [Ticketing workflow](workflows/ticketing.md).

## Evaluation

The repository includes one-shot, cross-domain, security and long-horizon evaluations:

- 30 provider-neutral incident scenarios
- Infrastructure / SRE / DevOps / FinOps / Security domain scenarios
- capability registry trust/supply-chain unit tests
- Loop scenarios that test terminal status, iteration budgets, required/prohibited events, learning writeback and regression obligations
- deterministic unit tests that reject agent self-verification and enforce no-progress budgets

The evaluation question is not only **“did the agent identify the right answer?”**, but also **“did it select appropriate implementation knowledge, preserve trust boundaries, and reach a verified outcome through a bounded process?”**

## Terraform or IaC is not required

```text
IaC-managed        Proposal → Code/Config → Plan → PR → Approval
Non-IaC service    Proposal → Change Ticket → Console/API Procedure → Approval
Operational work   Proposal → Reviewed Runbook → Maintenance Window → Approval
Hybrid             Proposal → Script/Config/API Change → Controlled Pipeline/Operator
```

Capabilities provide implementation knowledge above these choices; Loop Engineering verifies outcomes after execution.

## Safety model

- Read-only evidence collection is the default starting point.
- Third-party Skill content is reference material unless explicitly reviewed and managed.
- External scripts/commands are never automatically executed by capability routing.
- Agent hooks are defense-in-depth, not a security boundary.
- Production mutation, destructive actions, authorization expansion and financial commitments remain independently authorized.
- A Loop cannot repeat its way around a human gate.
- Ticket creation permission is separate from production mutation permission.
- The model does not own truth, completion, authorization, or the production control plane.

## Reference models

The design combines mature engineering control loops and recent agent-loop research. See [Reference Models](docs/REFERENCE-MODELS.md).

| Reference model | Harness design derived from it |
| --- | --- |
| IBM Loop Engineering | goal/action/observation/adjustment, explicit stopping criteria |
| LongHorizon-Harness | external state, independently verified facts, manage/execute/audit separation |
| LoopsBench | long-horizon evaluation and regression obligations |
| Kubernetes Controllers | desired vs actual state reconciliation |
| OpenGitOps | declarative/versioned state and continuous reconciliation where applicable |
| Google SRE | SLI/SLO, error budget, reliability policy and escalation |
| DORA | baseline → identify constraint → improve → check progress → repeat |
| FinOps Framework | Inform → Optimize → Operate → measure → repeat |
| MCP | provider-neutral evidence/workflow tool boundary |
| Agent Skills | progressively loaded implementation/operational knowledge |
| Independent human/policy controls | authorization boundary for high-impact actions |

## Quick start

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/validate_capability_registry.py capabilities/registry.yaml
python -m unittest discover -s tests
```

## License

MIT
