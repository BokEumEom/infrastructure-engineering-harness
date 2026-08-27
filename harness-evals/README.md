# Harness Lift

Harness Lift measures whether Harness guidance improves the model or merely adds structure.

Run the same case with the same model, workspace, tools, permissions, and scorer under three profiles:

- `bare` — model + tools + hard runtime/safety enforcement;
- `minimal` — bare + minimal always-loaded invariants + progressive discovery;
- `full` — richer/prescriptive guidance being evaluated.

The primary questions are:

1. Does minimal improve outcome over bare without safety/evidence regression?
2. Does full improve on minimal enough to justify its additional constraints and context cost?
3. Does full reduce exploration, autonomy, or efficiency even if top-line correctness looks unchanged?

A Harness is **hobbling** when richer guidance performs worse than minimal guidance without buying a meaningful safety or verification improvement.

## Source rules

`source: fixture` validates schema/scoring/gating only.

Only `source: live` may support a claim that a Harness profile improves or degrades real model behavior.

## Fixtures

- `fixtures/plumbing.triple.json` — positive plumbing case; policy gate should pass.
- `fixtures/unhobbling.triple.json` — deliberate negative case where full guidance underperforms minimal; policy gate should reject it.

## Commands

```bash
python scripts/score_harness_lift.py harness-evals/fixtures/plumbing.triple.json /tmp/harness-lift.json
python scripts/check_harness_lift.py harness-evals/policy.yaml /tmp/harness-lift.json
```

For real claims add `--require-live` to the policy check.

See `docs/HARNESS-UNHOBBLING.md`.
