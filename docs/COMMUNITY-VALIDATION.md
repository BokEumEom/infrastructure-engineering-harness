# Community Validation

The project should grow through reproducible engineering evidence, not only through framework code or star count.

## Participation loop

```text
Discover
   ↓
Run the 5-minute quickstart
   ↓
Choose a scenario / validation / adapter task
   ↓
Produce a reproducible artifact
   ↓
CI checks the contract
   ↓
Result is reviewable by others
   ↓
Scenario, adapter or harness improves
```

## Contributions we value

Code is only one contribution type. The project explicitly values:

- anonymized infrastructure scenarios based on real operational experience;
- live validation reports from Codex, Claude Code, Kiro or other agents;
- red herrings and negative controls that make benchmarks harder to game;
- read-only provider adapters;
- Skill and Context Lift experiments;
- documentation and portability fixes;
- reference-model research with a concrete local design consequence.

## Verification board model

The intended public view is a verification board, not initially a winner-takes-all model leaderboard.

A row should be reconstructable from a `validation-report` and contain at least:

- agent/model;
- harness revision;
- scenario;
- fixture vs live source;
- result;
- evidence completeness;
- unsafe action attempted or not;
- optional tool-call, duration and cost diagnostics.

Reproducibility and safety take precedence over score aggregation.

## Community health signals

Useful early project metrics include:

- external contributors;
- external scenarios;
- live validation reports;
- repeat contributors;
- independently implemented adapters;
- organizations or teams that report testing the harness.

Stars are useful discovery signals, but they are not evidence that the harness works.

## Release posture

The current project should be described as an experimental/research preview until live adapters, durable runtime persistence and controlled execution integrations have broader independent validation. See `docs/RELEASE-STATUS.md`.
