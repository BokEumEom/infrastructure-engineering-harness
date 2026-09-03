# Infrastructure Engineering Agent

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

A provider-neutral **Infrastructure Engineering Agent** for investigating, reviewing, planning, and verifying infrastructure work across Infrastructure, Operations, DevOps, SRE, FinOps, and Security.

> **Let the agent reason freely; constrain authority and truth at the runtime boundary.**

> **Status: Research Preview.** The Agent contract, Skills, Resource Graph, deterministic scenarios, evaluation plumbing, and local CLI are available. Live adapters, persistent runtime, and controlled execution remain experimental.

The repository keeps the historical name `infrastructure-engineering-harness` for compatibility. **The product identity is now Infrastructure Engineering Agent; the harness is its internal control plane.**

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

See the [5-minute Quickstart](QUICKSTART.md).

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

Examples:

- "Review this Terraform change."
- "Why did payment-api latency increase?"
- "Improve this deployment pipeline."
- "Is this service burning its error budget?"
- "Find the main infrastructure cost driver."
- "Review the IAM and trust boundaries."

These are capability domains/lenses inside one Agent, not separate agents by default.

## Architecture

```text
Organizational Knowledge + Live Environment
                    ↓
              Minimal Context
                    ↓
       Infrastructure Engineering Agent
                    ↓
              Model Judgment
          ↙         ↓         ↘
      Context     Skills    Capabilities
          ↘         ↓         ↙
                   Action
                    ↓
       Agent Runtime / Harness Control Plane
 Evidence · Resource Provenance · State · Guard
 Permission · Approval · Audit · Verification
                    ↓
          Infrastructure Backend
                    ↓
 AWS / K8s / CI/CD / Observability / Cost / Security
                    ↓
          Independent Verification
                    ↓
             Verified Outcome
                    ↓
                  Learn
```

The Agent owns reasoning and next-action judgment. It does not own credentials, independent truth, approval state, production authority, or verified completion.

## Agent contract and backend

The product contract lives at [agents/infrastructure_engineering/agent.yaml](agents/infrastructure_engineering/agent.yaml).

The provider-neutral backend interface lives at [agents/infrastructure_engineering/backend.py](agents/infrastructure_engineering/backend.py). It separates:

```text
discover_resources / collect_evidence
                 ↓
             judgment
                 ↓
            stage_change
                 ↓
         review / approval
                 ↓
      apply_approved_change
                 ↓
          verify_outcome
```

Platform credentials stay behind the backend/runtime boundary. Model-visible text approval is never equivalent to independently owned authorization.

## Core building blocks

- **Agent Contract** — the user-facing Infrastructure Engineering Agent role, capabilities, authority, backend, and completion boundary
- **Minimal Agent Context** — small always-loaded truth/authorization/verification invariants
- **Workflow Surface** — natural user intents without forcing a fixed reasoning route
- **Context Pack** — pull-oriented task context with provenance, freshness, and explicit evidence gaps
- **Skill / Capability** — progressively loaded engineering guidance and implementation/verification knowledge
- **Resource Graph** — provider-neutral resources, dependencies, and discovery provenance
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — internal Event Log, Tool Pipeline, Guard, Approval, Sandbox, and state reference runtime
- **Engineering Loop** — goal + external state + constraints + terminal conditions; adaptive when reasoning order is not itself a requirement
- **Knowledge Consolidation** — Observation → Verified Fact → Engineering Assessment → Learning Candidate → governed Durable Knowledge
- **Skill Lift / Context Lift / Harness Lift** — evaluation of whether guidance actually improves or hobbles the Agent
- **Artifact Reflex** — Paperthin-inspired artifact hygiene, SSOT, and eval-integrity rules

Detailed architecture: [Agent model](agents/infrastructure_engineering/README.md), [Architecture](docs/ARCHITECTURE.md), [Harness Unhobbling](docs/HARNESS-UNHOBBLING.md), [Reference Models](docs/REFERENCE-MODELS.md), [Workflow Surface](docs/WORKFLOW-SURFACE.md), and [Knowledge Consolidation](docs/KNOWLEDGE-CONSOLIDATION.md).

## Safety model

- Read-only discovery/evidence is the default authority.
- A resource should be discovered/bound before a production mutation can target it.
- Tool output is not automatically a verified engineering fact.
- `verified_by: agent` is invalid.
- Chat text cannot grant production authorization.
- Production mutation, destructive action, privilege expansion, and financial commitments require independent authorization.
- Hard boundaries belong in Runtime/schema/policy/backend enforcement rather than repeated prompt prose.
- The Agent may reason freely; it cannot self-certify truth, authority, or successful completion.

## Reference models

The project learns from external systems without granting them authority. Important references include DeepSeek Harness, NVIDIA SkillEvaluator/ACES, Paperthin, gstack, GBrain, WikiSkill, Kubernetes Controllers, SRE/DORA/FinOps, and Anthropic's **commerce-agents**.

Commerce Agents is particularly relevant for the separation of **agent product surface → backend contract → provenance gates → staged writes → host approval → runtime enforcement**. Those patterns inform this Agent direction while the project remains provider-neutral and infrastructure-specific.

See [docs/REFERENCE-MODELS.md](docs/REFERENCE-MODELS.md) and [capabilities/README.md](capabilities/README.md).

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

English is the canonical language for machine-readable contracts, schemas, Skills, policies, and evaluation definitions. Korean, Japanese, and Simplified Chinese README / Quickstart files remain first-class entry documentation.

See [Localization Policy](docs/LOCALIZATION.md).

## Current maturity

This project is intentionally explicit about what is not yet proven:

- live discovery/evidence adapters are still limited;
- the Runtime Kernel is a reference implementation, not a production daemon;
- the Infrastructure Engineering Backend is a contract, not a complete AWS/Kubernetes implementation;
- autonomous production mutation is not promised;
- real Agent effectiveness requires `source: live` validation evidence.

See [Release Status](docs/RELEASE-STATUS.md) and [Community Validation](docs/COMMUNITY-VALIDATION.md).

## License

MIT
