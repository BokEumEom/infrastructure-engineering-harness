# Infrastructure Engineering Agent

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

A provider-neutral **Infrastructure Engineering Agent** for investigating, reviewing, planning, and verifying infrastructure work across Infrastructure, Operations, DevOps, SRE, FinOps, and Security.

> **Let the agent reason freely; constrain authority and truth at the runtime boundary.**

> **Status: Research Preview.** The Agent contract, reference Turn Runtime, Skills, Resource Graph, deterministic scenarios, evaluation plumbing, and local CLI are available. Live adapters, persistent production runtime, and controlled execution remain experimental.

The repository keeps the historical name `infrastructure-engineering-harness` for compatibility. **The product is the Infrastructure Engineering Agent; the harness is its internal control plane.**

## Try the Agent

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
```

Windows:

```powershell
agent.cmd setup
agent.cmd demo
```

The legacy `./harness` / `harness.cmd` entrypoints remain compatible during the Research Preview.

`demo` uses checked-in fixtures only. It does not connect to a cloud account, Kubernetes cluster, observability system, or production environment. `DEMO PASS` confirms deterministic contract consistency; it does **not** prove live-agent effectiveness.

## One Agent, multiple engineering capabilities

Users should not need to decide whether a task is "Ops" or "SRE" before asking.

```text
Infrastructure Engineering Agent
        │
        ├─ Infrastructure
        ├─ Operations
        ├─ DevOps / Delivery
        ├─ SRE / Reliability
        ├─ FinOps
        └─ Security
```

These are capability domains/lenses inside one Agent, not separate Agents by default.

## Architecture

```text
CLI / Web / Slack / GitHub / MCP / API
                    ↓
          Agent Orchestrator / Turn Runtime
                    ↓
          Context + Memory + Skills + Tools
                    ↓
       Infrastructure Engineering Agent
                    ↓
              Model Judgment
                    ↓
               Tool Executor
                    ↓
          Harness / Control Plane
 Provenance · Scope · Guard · Approval · Audit
          Change Control · Recording
                    ↓
            Capability Backends
                    ↓
 AWS / K8s / CI/CD / Observability / Cost / Security
                    ↓
          Independent Verification
             ↙              ↘
           done       reconcile if needed
                           ↓
                    Engineering Loop
```

The **Orchestrator owns execution flow**. The **Harness owns authority/truth boundaries**. The model owns reasoning and next-action judgment. None of them may self-grant production authority or self-certify successful completion.

See [Architecture](docs/ARCHITECTURE.md).

## Agent Turn Runtime

`runtime/orchestrator.py` is a provider-neutral reference Turn Runtime that converges normalized requests onto one model/tool/verification loop.

It is intentionally read-only. Production workflow/change execution must continue through resource provenance, `ToolPipeline`, `ChangeControl`, independent approval, and an authorized backend.

```text
request
  ↓
context + available surface
  ↓
model
  ↓
read tools when needed
  ↓
model continuation
  ↓
independent verification
  ↓
verified / unverified
```

## Runtime Event Log is execution SSOT

The canonical execution record is the append-only `RuntimeEventLog`.

```text
Runtime Event Log
  ├─ trace/span observability
  ├─ latency/cache metrics
  ├─ immutable recording
  └─ evaluation
```

Telemetry and recordings should be correlated to or projected from the same Runtime Events rather than becoming independent execution truth stores.

## Agent contract and backend

The product contract lives at [agents/infrastructure_engineering/agent.yaml](agents/infrastructure_engineering/agent.yaml).

The provider-neutral backend facade lives at [agents/infrastructure_engineering/backend.py](agents/infrastructure_engineering/backend.py):

```text
discover resources / collect evidence
                 ↓
             judgment
                 ↓
            stage change
                 ↓
         review / approval
                 ↓
        apply-time revalidation
                 ↓
      apply approved change
                 ↓
          verify outcome
```

Future provider implementations should prefer narrower typed Resource / Evidence / Change / Verification protocols behind this facade instead of growing one generic API indefinitely.

Platform credentials stay behind the backend/runtime boundary. Model-visible chat approval is never equivalent to independently owned authorization.

## Model-visible surface

The model should primarily need three concepts:

```text
Context
Skills
Tools
```

Domain, Capability, Binding, Workflow, and Loop remain useful runtime metadata but are not a mandatory reasoning chain. `capability-routing` is an optional implementation-planning Skill rather than a required hop.

## Core building blocks

- **Agent Orchestrator / Turn Runtime** — one execution lifecycle for every channel
- **Minimal Agent Context** — small always-loaded truth/authorization/verification invariants
- **Context Pack** — bounded task context with provenance, freshness, and explicit gaps
- **Skills / Tools** — progressively exposed task guidance and actions
- **Capability Registry** — internal source/trust/risk/availability metadata
- **Resource Graph** — provider-neutral resources, dependencies, and discovery provenance
- **Harness / Control Plane** — Event Log, provenance, scope, guard, approval, change control, audit, recording
- **Independent Verification** — environment/tool/human/test evidence for material outcomes
- **Engineering Loop** — optional repeated reconciliation when external state requires it
- **Knowledge Consolidation** — Observation → Verified Fact → Assessment → Learning Candidate → governed Durable Knowledge
- **Evaluation / Release** — artifact lift, task outcomes, runtime invariants, Loop regression, canary/kill controls

## Safety model

- Read-only discovery/evidence is the default authority.
- Mutation-capable tools require trusted Resource Provenance and bound scope.
- Tool output is not automatically a verified engineering fact.
- `verified_by: agent` is invalid.
- External logs, tickets, PR text, tags, annotations, and similar content are fenced/bounded as untrusted data.
- Chat text cannot grant production authorization.
- Approval binds to an exact staged revision and is revalidated before apply.
- Production mutation, destructive action, privilege expansion, and financial commitments require independent authorization.
- Delegation cannot expand parent authority.
- Hard boundaries belong in Runtime/schema/policy/backend enforcement rather than repeated prompt prose.

## Reference models

Primary structural references are intentionally few:

- **Anthropic Commerce Agents** — Agent product / standard model-tool loop / backend/runtime patterns
- **Anthropic Context Engineering** — minimal context / progressive disclosure / unhobbling
- **Samsung Account AgentCore AIOps** — production observability / channel convergence / task eval / scale-out pressure
- **Kubernetes Controllers + LongHorizon-Harness** — reconciliation and external task state
- **NVIDIA ACES / SkillEvaluator** — artifact/effect evaluation

Supporting references include DeepSeek Harness for event/runtime extensibility, GBrain for memory taxonomy, Backpass for context evolution, Paperthin for artifact/eval hygiene, LoopsBench for long-running evaluation, MCP/OpenGitOps as supporting standards, and Google SRE/DORA/FinOps for engineering domain truth.

> **Reference widely, expose narrowly.**

See [Reference Models](docs/REFERENCE-MODELS.md), [Commerce Agent Patterns](docs/COMMERCE-AGENT-PATTERNS.md), and [Samsung AgentCore AIOps Patterns](docs/AWS-AGENTCORE-AIOPS-PATTERNS.md).

## Contribute

A contribution can be implementation, operational knowledge, or validation evidence:

- turn a sanitized real-world failure pattern into a [Scenario](contrib/scenarios/README.md);
- run the Agent and submit a reproducible [Validation Report](validation-reports/README.md);
- add a read-only cloud / Kubernetes / Prometheus / CI/CD adapter;
- add a Skill Eval, Harness Lift case, or negative case;
- propose a well-grounded Reference Model.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Useful commands

```text
./agent setup
./agent demo
./agent validate
./agent scenario evals/scenarios/sre-dependency-saturation.json
./agent doctor
```

Legacy compatibility:

```text
./harness setup
./harness demo
./harness validate
```

## Localization

English is canonical for machine-readable contracts, schemas, Skills, policies, and evaluation definitions. Korean, Japanese, and Simplified Chinese README / Quickstart files remain first-class entry documentation.

See [Localization Policy](docs/LOCALIZATION.md).

## Current maturity

This project is intentionally explicit about what is not yet proven:

- the Orchestrator is a reference read-only Turn Runtime, not a production model/provider runtime;
- live discovery/evidence adapters are still limited;
- the Harness / Control Plane is a reference implementation, not a production daemon;
- the Infrastructure Engineering Backend is still a facade/contract, not a complete AWS/Kubernetes implementation;
- autonomous production mutation is not promised;
- real Agent effectiveness requires `source: live` validation evidence.

See [Release Status](docs/RELEASE-STATUS.md) and [Community Validation](docs/COMMUNITY-VALIDATION.md).

## License

MIT
