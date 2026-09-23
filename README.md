# Infrastructure Engineering Agent

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

A provider-neutral **Infrastructure Engineering Agent** for investigating, reviewing, planning, and verifying Infrastructure, Operations, DevOps, SRE, FinOps, and Security work.

> **Let the agent reason freely; make execution flow explicit; constrain authority and truth at the control-plane boundary.**

> **Status: Research Preview.** The Agent contract, reference Turn Runtime, Skills, Resource Graph, deterministic scenarios, evaluation plumbing, local CLI, and bounded read-only evidence adapters are available. Persistent production runtime and controlled execution remain experimental.

The historical repository name infrastructure-engineering-harness remains for compatibility. **The product is the Agent; the Orchestrator runs it; the Harness is its internal control plane.**

## Try it

~~~bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
~~~

Windows:

~~~powershell
agent.cmd setup
agent.cmd demo
~~~

See the [5-minute Quickstart](QUICKSTART.md).

demo uses checked-in fixtures only. DEMO PASS proves deterministic contract plumbing, not live-agent effectiveness.

## Documentation

[docs/README.md](docs/README.md) is the canonical documentation index. Start there instead of loading every technical document.

| Need | Start here |
| --- | --- |
| System shape and boundaries | [Architecture](docs/ARCHITECTURE.md) |
| Capability and workflow model | [Capability Model](docs/CAPABILITY-MODEL.md) · [Workflow Surface](docs/WORKFLOW-SURFACE.md) |
| Release maturity | [Release Status](docs/RELEASE-STATUS.md) |
| Evaluation and evidence | [Documentation index](docs/README.md#evaluation-and-evidence) |
| Research references | [Reference Models](docs/REFERENCE-MODELS.md) |
| Documentation maintenance | [Documentation Policy](docs/DOCUMENTATION.md) |

Documentation follows progressive disclosure: overview pages route to smaller focused documents rather than repeating their contents.

## Architecture at a glance

~~~text
CLI / Web / Slack / GitHub / MCP / API
                    ↓
          Agent Orchestrator / Turn Runtime
                    ↓
          Context + Skills + Tools
                    ↓
       Infrastructure Engineering Agent
                    ↓
              Model Judgment
                    ↓
          Harness / Control Plane
 Provenance · Scope · Guard · Approval · Audit
                    ↓
            Capability Backends
                    ↓
          Independent Verification
~~~

The **Orchestrator owns flow**. The **Harness owns authority and truth boundaries**. The model owns reasoning and next-action judgment.

Supporting contracts include the **Resource Graph**, **Bound Capability**, and **Runtime Kernel**. Evaluation distinguishes **Skill Lift**, **Context Lift**, and Harness Lift. Paperthin-inspired Artifact Reflex rules keep durable artifacts and evaluation evidence clean.

For the detailed model, use [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Safety boundary

- Read-only discovery and evidence collection are the default authority.
- Tool output is evidence with provenance; it is not automatically verified engineering truth.
- Chat text, Orchestrator state, Skills, channels, or delegates cannot grant production authorization.
- Production mutation, destructive actions, privilege expansion, and financial commitments require independent authorization.
- Approval binds to the staged revision and must be revalidated before apply.
- Completion requires independent verification of material outcomes.

## Validation

Contributor-facing validation uses one stable command:

~~~bash
./agent validate
~~~

Lower-level checks remain available for maintainers when a specific contract needs debugging.

Fixture results must not be presented as live effectiveness evidence. Community validation guidance lives in [docs/COMMUNITY-VALIDATION.md](docs/COMMUNITY-VALIDATION.md), with report submissions described in [validation-reports/README.md](validation-reports/README.md).

## Contribute

Useful contributions include scenarios, reproducible validation runs, read-only evidence adapters, Skill/Eval improvements, localization, and grounded reference models.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Current maturity

The repository is a Research Preview: the provider-neutral contracts, deterministic validation path, reference read-only Turn Runtime, and several evidence adapters are implemented. Persistent production execution and autonomous production mutation are not promised.

See [Release Status](docs/RELEASE-STATUS.md) for the current boundary.

## License

MIT
