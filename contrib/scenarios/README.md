# Scenario Contribution Kit

Operational experience is valuable even when you do not contribute runtime code.

A scenario turns a real engineering failure pattern into a safe, reproducible evaluation asset.

## Start from an experience, not proprietary data

Good sources include:

- a dependency saturation incident;
- a misleading CPU/memory signal;
- a failed deployment or rollback;
- a cost spike with a non-obvious unit-economics cause;
- an access/trust-boundary mistake;
- an observability gap that delayed diagnosis.

Generalize names, values and topology. Never copy customer data, secrets, private logs or confidential architecture.

## Required shape

Use `schemas/infra-scenario-eval.schema.json` and an existing file under `evals/scenarios/`.

A strong scenario includes:

```text
symptom / objective
      ↓
ground truth
      ↓
required evidence
      ↓
plausible red herrings
      ↓
prohibited actions
      ↓
expected behavior
      ↓
success conditions
```

## What makes a scenario useful

### Required evidence

The conclusion should not be justified unless these signals are found.

### Red herrings

Include signals that a plausible but shallow agent might over-weight. Explain why each signal is insufficient.

### Prohibited actions

State mutations or conclusions that would be unsafe or unjustified, such as restarting production to prove a hypothesis or scaling healthy compute before dependency evidence is checked.

### Success conditions

Prefer observable behavior over prose style: evidence cited, wrong hypothesis rejected, unsafe action avoided, verification required.

## Validate locally

```bash
python scripts/validate_context.py examples/.infra-context
python scripts/check_infra_scenario.py evals/scenarios/<your-scenario>.json
```

The scenario checker cross-validates environment/evidence fixture references so an internally inconsistent benchmark cannot pass merely because its JSON shape is valid.
