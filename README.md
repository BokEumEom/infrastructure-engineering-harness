# Infrastructure Engineering Agent

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

A provider-neutral **Infrastructure Engineering Agent** for investigating, reviewing, planning, and verifying Infrastructure, Operations, DevOps, SRE, FinOps, and Security work.

> **Let the agent reason freely; make execution flow explicit; constrain authority and truth at the control-plane boundary.**

> **Status: Research Preview.** The Agent contract, reference Turn Runtime, Skills, Resource Graph, deterministic scenarios, evaluation plumbing, and local CLI are available. Live adapters, persistent production runtime, and controlled execution remain experimental.

The historical repository name `infrastructure-engineering-harness` remains for compatibility. **The product is the Agent; the Orchestrator runs it; the Harness is its internal control plane.**

## Try it

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

`demo` uses checked-in fixtures only. `DEMO PASS` proves deterministic contract plumbing, not live-agent effectiveness.

## One Agent, multiple engineering capabilities

```text
Infrastructure Engineering Agent
        ├─ Infrastructure
        ├─ Operations
        ├─ DevOps / Delivery
        ├─ SRE / Reliability
        ├─ FinOps
        └─ Security
```

These are capability domains/lenses inside one Agent. Separate specialist Agents are optional scale-out mechanisms, not the default architecture.

## Canonical architecture

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

The **Orchestrator owns flow**. The **Harness owns authority/truth boundaries**. The model owns reasoning and next-action judgment. None may self-grant production authority or self-certify successful completion.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Agent Turn Runtime

`runtime/orchestrator.py` is a provider-neutral reference Turn Runtime:

```text
TurnRequest
   ↓
Context + available surface
   ↓
Model
   ↓
read-only Tools when needed
   ↓
Model continuation
   ↓
Independent Verification
   ↓
verified / unverified
```

It is intentionally read-only. Workflow/change authority must continue through Resource Provenance, `ToolPipeline`, `ChangeControl`, independent approval, and an authorized backend.

## Model-visible surface

The model should primarily need:

```text
Context
Skills
Tools
```

Domain, Capability, Binding, Workflow, and Loop remain useful internal metadata but are not a mandatory reasoning chain. `capability-routing` remains an optional implementation-planning Skill.

Compatibility concepts still used by lower-level contracts include:

- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source;
- **Runtime Kernel** — Event Log, Tool Pipeline, Guard, Approval, State, and related control-plane primitives.

## Runtime Event Log is execution SSOT

```text
Runtime Event Log
  ├─ Trace / Span
  ├─ Latency / Cache Metrics
  ├─ Recording
  └─ Evaluation
```

The append-only Event Log is the canonical execution record. Trace, metrics, recordings, and evaluation must correlate to or derive from the same runtime history rather than become competing execution truth stores.

## Backend boundary

The current provider-neutral facade lives at `agents/infrastructure_engineering/backend.py`:

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

Future provider implementations should prefer narrower typed Resource / Evidence / Change / Verification protocols behind this facade.

Credentials stay behind the host/runtime boundary. Chat approval is not execution authorization.

## Core building blocks

- **Agent Orchestrator / Turn Runtime** — one execution lifecycle for every channel
- **Context Pack** — bounded context with provenance, freshness, and explicit gaps
- **Skills / Tools** — progressively exposed guidance and actions
- **Capability Registry** — internal source/trust/risk/availability metadata
- **Resource Graph** — provider-neutral resources, dependencies, and discovery provenance
- **Bound Capability** — narrowed resource/evidence/permission scope
- **Runtime Kernel / Harness Control Plane** — Event Log, provenance, guards, approval, change control, audit, recording
- **Independent Verification** — current environment/tool/human/test evidence for material outcomes
- **Engineering Loop** — optional repeated reconciliation only when needed
- **Knowledge Consolidation** — Observation → Verified Fact → Assessment → Learning Candidate → governed Durable Knowledge
- **Skill Lift / Context Lift / Harness Lift** — artifact/context/harness effectiveness evaluation
- **Artifact Reflex** — Paperthin-inspired artifact hygiene, SSOT, and eval-integrity rules

## Safety model

- Read-only discovery/evidence is the default authority.
- Mutation targets require trusted Resource Provenance and bound scope.
- Tool output is not automatically a Verified Fact.
- `verified_by: agent` is invalid.
- External logs, tickets, PR text, tags, annotations, and similar content are fenced/bounded as untrusted data.
- Chat text, Orchestrator state, channels, Skills, or delegates cannot grant production authorization.
- Approval binds to an exact staged revision and is revalidated before apply.
- Production mutation, destructive action, privilege expansion, and financial commitments require independent authorization.
- Delegation cannot expand parent authority.

## Reference models

Primary structural references are intentionally few:

- **Anthropic Commerce Agents** — Agent product / standard model-tool loop / Backend / runtime safety
- **Anthropic Context Engineering** — minimal context / progressive disclosure / unhobbling
- **Samsung Account AgentCore AIOps** — production observability / channel convergence / task evaluation / scale-out pressure
- **Kubernetes Controllers + LongHorizon-Harness** — reconciliation and external task state
- **NVIDIA ACES / SkillEvaluator** — artifact/effect evaluation

Supporting references include DeepSeek Harness for event/runtime extensibility, GBrain for memory taxonomy, Backpass for context evolution, Paperthin for artifact/eval hygiene, LoopsBench for long-running evaluation, and MCP/OpenGitOps as supporting standards. Google SRE, DORA, and FinOps remain engineering-domain references.

> **Reference widely, expose narrowly.**

See [Reference Models](docs/REFERENCE-MODELS.md), [Commerce Agent Patterns](docs/COMMERCE-AGENT-PATTERNS.md), and [Samsung AgentCore AIOps Patterns](docs/AWS-AGENTCORE-AIOPS-PATTERNS.md).

## Contribute

- turn a sanitized real-world failure pattern into a [Scenario](contrib/scenarios/README.md);
- run the Agent and submit a [Validation Report](validation-reports/README.md);
- add a read-only cloud / Kubernetes / Prometheus / CI/CD adapter;
- add a Skill Eval / Harness Lift / negative case;
- propose a well-grounded Reference Model.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Commands

```text
./agent setup
./agent demo
./agent validate
./agent scenario evals/scenarios/sre-dependency-saturation.json
./agent doctor
```

Legacy `./harness` commands remain compatible during Research Preview.

## Localization

English is canonical for machine-readable contracts, schemas, Skills, policies, and evaluation definitions. Korean, Japanese, and Simplified Chinese README / Quickstart files remain first-class entry documentation.

See [Localization Policy](docs/LOCALIZATION.md).

## Current maturity

- Orchestrator: reference read-only Turn Runtime, not a production model/provider runtime;
- live discovery/evidence adapters: limited;
- Harness / Control Plane: reference implementation, not a production daemon;
- Backend: contract/facade, not a complete AWS/Kubernetes implementation;
- autonomous production mutation: not promised;
- real Agent effectiveness: requires `source: live` validation evidence.

See [Release Status](docs/RELEASE-STATUS.md) and [Community Validation](docs/COMMUNITY-VALIDATION.md).

## License

MIT
