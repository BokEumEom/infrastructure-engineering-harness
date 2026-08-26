# 5-minute Quickstart

You do not need cloud credentials or a production environment to try the harness.

## 1. Clone and install

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
```

## 2. Validate the reference context

```bash
python scripts/validate_context.py examples/.infra-context
```

## 3. Run a realistic infrastructure scenario check

```bash
python scripts/check_infra_scenario.py evals/scenarios/sre-dependency-saturation.json
```

The scenario includes ground truth, required evidence, red herrings, prohibited actions and success conditions. It also cross-checks that the referenced environment and evidence fixtures actually exist.

## 4. Run all deterministic tests

```bash
python -m unittest discover -s tests
```

## What you just tested

```text
Environment fixture
      ↓
Resource Graph
      ↓
Required Evidence
      ↓
Scenario Contract
      ↓
Safety / consistency checks
```

These deterministic checks validate the harness contracts. They do **not** prove that a live AI agent performs better. Real Skill Lift, Context Lift or agent validation claims require `source: live` runs under the matching evaluation contract.

## Next steps

- Add a real incident pattern: see `contrib/scenarios/README.md`.
- Submit a reproducible agent run: see `validation-reports/README.md`.
- Add an evidence/discovery adapter: see `CONTRIBUTING.md`.
- Read the architecture only after you have run the quickstart: `docs/ARCHITECTURE.md`.
