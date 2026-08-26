# 5-minute Quickstart

You do not need cloud credentials or a production environment to try the harness. You also do not need to write or invoke Python commands directly.

> **Current Research Preview runtime:** Python 3 is still used internally. The public quickstart interface is the `harness` command so the implementation runtime can change later without changing the user workflow.

## macOS / Linux

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./harness setup
./harness demo
```

## Windows

```powershell
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
harness.cmd setup
harness.cmd demo
```

`setup` installs the small Research Preview dependency set. `demo` uses only checked-in fixtures: it does not connect to a cloud account, Kubernetes cluster, observability system or production environment.

## What `demo` does

```text
Infrastructure Engineering Harness
        ↓
Reference context validation
        ↓
Resource Graph + Evidence fixture
        ↓
SRE dependency-saturation scenario
        ↓
Safety / consistency checks
        ↓
DEMO PASS / FAIL
```

A successful demo confirms that the deterministic Harness contracts and scenario wiring are coherent. It does **not** prove that a live AI agent performs better.

## Useful commands

```text
./harness demo
    Fast, credential-free first experience.

./harness validate
    Contributor-facing deterministic validation.

./harness scenario evals/scenarios/sre-dependency-saturation.json
    Validate one scenario and its referenced fixtures.

./harness doctor
    Show local runtime/dependency status.

./harness setup
    Install the current Research Preview dependencies.
```

On Windows, replace `./harness` with `harness.cmd`.

## Try another scenario

```bash
./harness scenario evals/scenarios/sre-dependency-saturation.json
```

A scenario can include:

- ground truth;
- required evidence;
- plausible red herrings;
- prohibited actions;
- expected behavior;
- success conditions.

It also cross-checks that referenced environment and evidence fixtures exist.

## Contributor validation

Before opening a PR:

```bash
./harness validate
```

This runs the contributor-facing contract checks and unit tests through one stable entry point. Maintainers may still use the lower-level scripts directly in CI when debugging a specific contract.

## Next steps

- Add a real incident pattern: see `contrib/scenarios/README.md`.
- Submit a reproducible agent run: see `validation-reports/README.md`.
- Add an evidence/discovery adapter: see `CONTRIBUTING.md`.
- Read the architecture after trying the harness: `docs/ARCHITECTURE.md`.

## Live agent execution

The current `demo` is deterministic by design. A later CLI layer will provide a stable command such as `harness run --agent ... --scenario ...` once live Agent adapters are mature enough to make that command reproducible across runtimes. Until then, live runs are submitted through the Validation Report contract rather than pretending the fixture demo is a live-agent benchmark.
