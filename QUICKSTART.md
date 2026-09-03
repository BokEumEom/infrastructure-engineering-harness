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
SRE Dependency Saturation Scenario
        ↓
Safety / Consistency Check
        ↓
DEMO PASS / FAIL
```

A successful demo confirms that the deterministic Agent/runtime contracts and scenario wiring are coherent. It does **not** prove that a live AI agent performs better.

## Useful commands

```text
./agent demo
    Fast, credential-free first experience.

./agent validate
    Contributor-facing deterministic validation.

./agent scenario evals/scenarios/sre-dependency-saturation.json
    Validate one scenario and its referenced fixtures.

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

The current `demo` is deterministic by design. Live agent execution is recorded separately through `source: live` Validation Reports; fixture results must not be presented as live-agent benchmarks.
\nLegacy compatibility: `./harness` and `harness.cmd` remain available as internal-harness entrypoints during the Research Preview.\n