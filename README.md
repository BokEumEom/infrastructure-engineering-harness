# Infrastructure Engineering Harness

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

A provider-neutral, cross-agent harness for turning infrastructure knowledge and current evidence into reviewable engineering decisions and governed implementation across **Infrastructure Engineering / SRE / DevOps / FinOps / Security**.

> **Knowledge → Context → Decision Skill → Capability → Loop → Verified Outcome → Learning → Next Loop**

> **Status: Research Preview.** Core contracts, deterministic scenarios, evaluation plumbing, and the Harness CLI are available now. Live adapters, persistent runtime, and controlled execution remain experimental.

## Try it first

You do not need to understand the full architecture before using the project.

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./harness setup
./harness demo
```

Windows:

```powershell
harness.cmd setup
harness.cmd demo
```

See the [5-minute Quickstart](QUICKSTART.md).

`demo` uses checked-in fixtures only. It does not connect to a cloud account, Kubernetes cluster, observability system, or production environment. `DEMO PASS` confirms deterministic contract consistency; it does **not** prove live-agent effectiveness.

## What problem does it solve?

Agents can already generate IaC, configuration, scripts, pipelines, and runbooks. The harder questions are:

- what should change and why;
- which evidence is sufficient to justify a decision;
- which constraints and trust boundaries must hold;
- which Skill / Capability should be selected;
- how the real outcome is independently verified after execution.

```text
Organizational Knowledge + Live Environment
                    ↓
              Resource Graph
                    ↓
             Context Resolution
                    ↓
                Domain Lens
                    ↓
              Decision Skill
                    ↓
             Capability Routing
                    ↓
              Bound Capability
                    ↓
               Runtime Kernel
                    ↓
        Authorized External Execution
                    ↓
           Independent Verification
                    ↓
            Engineering Loop + Learn
```

## Core building blocks

- **Domain** — Infrastructure / SRE / DevOps / FinOps / Security engineering lens
- **Decision Skill** — decides what should be done and why
- **Capability** — selects implementation or verification knowledge
- **Resource Graph** — provider-neutral model of real resources and dependencies
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — reference Session/Event Log, Tool Pipeline, Guard, Approval, and Sandbox runtime
- **Engineering Loop** — Observe → Decide → Act/Propose → Verify → Learn
- **Skill Lift / Context Lift** — paired evaluation of actual Skill / Context contribution
- **Artifact Reflex** — Paperthin-inspired artifact hygiene, SSOT, and eval-integrity rules

Detailed architecture lives in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/REFERENCE-MODELS.md](docs/REFERENCE-MODELS.md), [loops/README.md](loops/README.md), and [docs/PRODUCTION-READINESS.md](docs/PRODUCTION-READINESS.md).

## Safety model

- Read-only evidence collection is the default starting point.
- Tool output is not automatically promoted to a verified engineering fact.
- `verified_by: agent` is invalid.
- Third-party `reference_only` Skills do not gain execution authority.
- Production mutation, destructive actions, permission expansion, and financial commitments require independent authorization.
- Fixture validation and live-agent effectiveness are explicitly separated.
- The model does not own truth, completion, authorization, or the production control plane.

## External references

The harness can learn from external projects without granting them authority. Reviewed sources are pinned and registered as `reference_only`. Examples include BagelHole/DevOps-Security-Agent-Skills and Paperthin. Runtime, evaluation, environment-discovery, and SRE projects are tracked as reference models rather than copied wholesale.

See [capabilities/README.md](capabilities/README.md) and [docs/REFERENCE-MODELS.md](docs/REFERENCE-MODELS.md).

## Contribute without changing framework code

A useful contribution can be operational knowledge or validation evidence:

- turn a sanitized real-world failure pattern into a [Scenario](contrib/scenarios/README.md);
- run an agent and submit a reproducible [Validation Report](validation-reports/README.md);
- add a read-only Kubernetes / Prometheus / cloud adapter;
- add a Skill Eval or negative case;
- propose a well-grounded Reference Model.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Useful commands

```text
./harness demo
./harness validate
./harness scenario evals/scenarios/sre-dependency-saturation.json
./harness doctor
./harness setup
```

Windows uses `harness.cmd` instead of `./harness`.

## Localization

English is the canonical language for machine-readable schemas, Skills, architecture contracts, policies, and evaluation definitions. Korean, Japanese, and Simplified Chinese README / Quickstart files are maintained as first-class entry documentation, with CI checks for key semantic markers and links.

See [Localization Policy](docs/LOCALIZATION.md).

## Current maturity

This project is intentionally explicit about what is not yet proven:

- live environment discovery adapters are still limited;
- live observability adapters are not yet broadly implemented;
- the Runtime Kernel is still a reference implementation, not a production daemon;
- there is no autonomous production mutation promise;
- real agent effectiveness requires `source: live` validation evidence.

See [Release Status](docs/RELEASE-STATUS.md) and [Community Validation](docs/COMMUNITY-VALIDATION.md).

## License

MIT
