# Infrastructure Engineering Harness

**English** | [한국어](README.ko.md)

A provider-neutral, cross-agent harness for turning infrastructure knowledge and current evidence into reviewable engineering decisions across **Infrastructure Engineering, SRE, DevOps, and FinOps**.

> **Infrastructure Knowledge → Context → Skill → Loop → Verified Outcome → Learning → Next Loop**

The project is designed for **Codex, Kiro, Claude Code, and other repository-aware agents**. It does not require one cloud, runtime, IaC tool, observability product, CI/CD system, cost platform, or ticketing system.

## Why this exists

Agents can already generate IaC, configuration, scripts, runbooks and operational procedures. The harder problem is giving them enough organizational context to decide **what should change, why, with what evidence, under which constraints, and how the outcome is verified**.

This harness makes Architecture, ADRs, incidents, operating policy, reliability objectives, delivery rules, cost ownership and current evidence usable as agent context. Loop Engineering adds a control layer so the system can repeatedly observe, decide, verify, reconcile and learn without allowing the model to define truth or completion by itself.

## Architecture

```text
Durable Knowledge + Optional Live Evidence
                    ↓
              Context Resolution
                    ↓
               Domain Skill(s)
                    ↓
          Loop Engineering Control
      Observe → Decide → Act/Propose → Verify
         ↑                         ↓
         └──── Reconcile / Learn ──┘
                    ↓
        done / escalated / failed
                    ↓
 Incident / Runbook / ADR or Policy candidate / Eval
                    ↓
                 Next Loop
```

See [Architecture](docs/ARCHITECTURE.md), [Loop Engineering](loops/README.md), [Reference Models](docs/REFERENCE-MODELS.md), and [Production Readiness](docs/PRODUCTION-READINESS.md).

## Domain packs

The shared core is reused by four engineering lenses:

| Pack | Use it for | Additional context |
| --- | --- | --- |
| [Infrastructure](domains/infrastructure/README.md) | architecture, capacity, migration, dependencies, change risk | architecture, ADR, runtime/capacity evidence |
| [SRE](domains/sre/README.md) | SLI/SLO, error budgets, incidents, reliability, toil | `domains/sre.yaml` |
| [DevOps](domains/devops/README.md) | build/release/deployment, rollback, delivery performance | `domains/devops.yaml` |
| [FinOps](domains/finops/README.md) | allocation, usage efficiency, commitments, unit economics | `domains/finops.yaml` |

A Domain Pack is a **lens**. A Skill is a **capability**. A Loop is the **control system** that composes Skills over time.

```text
Domain → what questions matter
Skill  → what the agent can do now
Loop   → when to repeat, verify, escalate, stop and learn
```

## Loop Engineering

Loop Engineering is an execution layer above the existing Skills. It is used when the task cannot be safely completed as a one-shot answer.

Reference loops:

| Loop | Purpose |
| --- | --- |
| `incident-response` | investigate → verify hypothesis → propose mitigation → verify recovery → learn |
| `reliability-improvement` | baseline SLO/error budget → prioritize → track → remeasure → learn |
| `delivery-improvement` | baseline delivery → find constraint → improve → remeasure → learn |
| `finops-optimization` | inform → optimize → track/operate → measure realized value → learn |
| `change-validation` | precheck → independent approval → external execution → post-verify → regression check |

The loop contracts add four properties that one-shot prompts do not provide:

1. **External state** — loop state is explicit and survives model/context resets.
2. **Independent verification** — `verified_by: agent` is invalid; facts require environment, tool, human, or test evidence.
3. **Bounded execution** — iteration, duration and no-progress budgets prevent indefinite loops.
4. **Regression obligations** — previously achieved guarantees remain checks in later iterations.

A model cannot self-certify `done`. Terminal success requires verified success criteria, passed regression obligations and cleared human gates.

### Example: incident loop

```text
Alert / user report
       ↓
incident-analysis
       ↓
Leading hypothesis
       ↓
Independent verification
       ↓
Change required?
   ┌───┴──────────┐
   no             yes
   ↓               ↓
verify recovery   Change Proposal
                  ↓
             Human Approval
                  ↓
          External Execution
                  ↓
             verify recovery
                  ↓
            regression check
                  ↓
       Incident + Eval writeback
```

For Claude Code:

```text
/infra-harness:loop-engineering
Run the incident-response loop for payment-api using the selected context root.
Do not self-certify recovery; use current evidence and stop at any required production approval gate.
```

Codex and Kiro use the same Loop Specs through `AGENTS.md`.

## Agent support

### Codex

Use the repository `AGENTS.md` as the cross-agent operating contract. It routes one-shot tasks to Domain Skills and repeated work to Loop Specs.

### Kiro

Kiro can use `AGENTS.md`; `.kiro/steering/infrastructure-harness.md` remains an additional workspace adapter.

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
        └── finops.yaml
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
└── read-only sources
    ├── service repositories
    ├── runtime / observability
    ├── deployment systems
    └── cost / business data
```

See [Central Context Example](examples/central-context/README.md).

## Machine-readable contracts

`schemas/` contains contracts for service catalog, incidents, ADRs, policies, evidence, change proposals, ticketing, domain profiles and Loop Engineering.

Loop-specific contracts:

```text
loop-spec.schema.json    what the loop should do
loop-state.schema.json   externally maintained execution state
loop-result.schema.json  terminal outcome and learning
loop-eval-suite.schema.json long-horizon regression scenarios
```

Validation:

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
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

The harness owns Ticket Request, Ticket Policy, evidence/source references and search-before-create. Provider MCP servers own authentication, permissions and provider-specific tool calls.

See [MCP connections](mcp/README.md) and [Ticketing workflow](workflows/ticketing.md).

## Evaluation

The repository includes one-shot and long-horizon evaluations:

- 30 provider-neutral incident scenarios
- Infrastructure / SRE / DevOps / FinOps domain scenarios
- Loop scenarios that test terminal status, iteration budgets, required/prohibited events, learning writeback and regression obligations
- deterministic unit tests that reject agent self-verification and enforce no-progress budgets

The evaluation question becomes not only **“did the agent identify the right answer?”** but also **“did the system reach a verified outcome through a safe bounded process without regressing earlier guarantees?”**

## Terraform or IaC is not required

```text
IaC-managed        Proposal → Code/Config → Plan → PR → Approval
Non-IaC service    Proposal → Change Ticket → Console/API Procedure → Approval
Operational work   Proposal → Reviewed Runbook → Maintenance Window → Approval
Hybrid             Proposal → Script/Config/API Change → Controlled Pipeline/Operator
```

Loop Engineering operates above these execution choices. The common contract is Evidence, Risk, Blast Radius, Verification, Recovery and Independent Approval.

## Safety model

- Read-only evidence collection is the default starting point.
- Agent hooks are defense-in-depth, not a security boundary.
- Production mutation, destructive actions, authorization expansion and financial commitments remain independently authorized.
- A Loop cannot repeat its way around a human gate.
- Ticket creation permission is separate from production mutation permission.
- The model does not own truth, completion, authorization, or the production control plane.

## Reference models

The design is intentionally synthesized from mature engineering control loops and recent agent-loop research. See [Reference Models](docs/REFERENCE-MODELS.md) for how each source maps into the implementation.

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
| Independent human/policy controls | authorization boundary for high-impact actions |

Primary references:

- IBM Loop Engineering: https://www.ibm.com/think/topics/loop-engineering
- LongHorizon-Harness: https://arxiv.org/abs/2608.01964
- LoopsBench: https://arxiv.org/abs/2608.00267
- Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/
- OpenGitOps: https://opengitops.dev/
- Google SRE: https://sre.google/sre-book/service-level-objectives/ and https://sre.google/workbook/error-budget-policy/
- DORA: https://dora.dev/guides/dora-metrics/
- FinOps: https://www.finops.org/framework/phases/
- Atlassian Rovo MCP: https://support.atlassian.com/atlassian-ai-gateway/docs/set-up-clients/
- Linear MCP: https://linear.app/docs/mcp

## Quick start

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python -m unittest discover -s tests
```

## License

MIT
