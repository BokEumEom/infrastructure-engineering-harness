# 5-minute Quickstart

**English** | [한국어](QUICKSTART.ko.md) | [日本語](QUICKSTART.ja.md) | [简体中文](QUICKSTART.zh-CN.md)

You do not need cloud credentials or a production environment to try the Infrastructure Engineering Agent. You also do not need to write or invoke Python commands directly.

> **Current Research Preview runtime:** Python 3 is still used internally. The public quickstart interface is the `agent` command so the implementation runtime can change later without changing the user workflow.

## macOS / Linux

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
```

## Windows

```powershell
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
agent.cmd setup
agent.cmd demo
```

`setup` installs the small Research Preview dependency set. `demo` uses only checked-in fixtures: it does not connect to a cloud account, Kubernetes cluster, observability system, or production environment.

## What `demo` does

```text
Infrastructure Engineering Agent
        ↓
Reference Context Validation
        ↓
Resource Graph + Evidence Fixture
        ↓
Scenario Contract Validation
        ↓
DEMO PASS / FAIL
```

A successful demo confirms deterministic contract and fixture wiring. It does **not** execute a live model or prove live-agent effectiveness.

## Run the reference Agent through a scenario

```bash
./agent scenario evals/scenarios/sre-dependency-saturation.json
```

The default `scenario` command now runs the checked-in scenario through the reference Agent Orchestrator:

```text
Scenario
   ↓
Context + Resource Graph
   ↓
Deterministic fixture model
   ↓
evidence.list
   ↓
evidence.read
   ↓
assessment
   ↓
Independent Verification
   ↓
Scenario Scorer
   ↓
Fixture Runtime Recording
```

Hidden evaluator data such as `ground_truth`, `required_evidence`, and success conditions are not placed in model-visible Context. The fixture model discovers available evidence through read-only tools before forming an assessment.

This is still a **credential-free deterministic fixture run**, not a live model benchmark.

## Scenario commands

```text
./agent scenario <path>
    Run the scenario through the reference Orchestrator and score the result.

./agent scenario run <path>
    Explicit form of the default scenario run.

./agent scenario eval <path>
    Run and also print detailed scorer diagnostics.

./agent scenario check <path>
    Only validate scenario/fixture references. No Agent turn is executed.
```

## Useful commands

```text
./agent demo
    Fast, credential-free contract demo.

./agent validate
    Contributor-facing deterministic validation.

./agent scenario evals/scenarios/sre-dependency-saturation.json
    Execute one fixture scenario through the reference Agent Orchestrator.

./agent doctor
    Show local runtime/dependency status.

./agent setup
    Install the current Research Preview dependencies.
```

On Windows, replace `./agent` with `agent.cmd`.

## Contributor validation

Before opening a PR:

```bash
./agent validate
```

## Next steps

- Add a real incident pattern: `contrib/scenarios/README.md`
- Submit a reproducible agent run: `validation-reports/README.md`
- Add an evidence/discovery adapter: `CONTRIBUTING.md`
- Read the architecture: `docs/ARCHITECTURE.md`

Fixture recordings use `source: fixture`. Live agent execution remains a separate later validation phase using `source: live`; fixture results must not be presented as live-agent benchmarks.

Legacy compatibility: `./harness` and `harness.cmd` remain available as internal-harness entrypoints during the Research Preview.
