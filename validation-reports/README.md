# Validation Reports

A validation report is a first-class community contribution. It records what happened when an agent or harness was run against a known scenario.

## Why reports exist

The project should not rely only on claims that a Skill, prompt or agent is useful. Reports make results inspectable and comparable across agents, models, harness revisions and scenarios.

## Two sources

- `fixture` — validates schemas, scorers, CI wiring or deterministic reference behavior.
- `live` — records a real agent execution under a reproducible setup.

A fixture report must never claim real agent effectiveness, Skill Lift or Context Lift. The schema enforces this.

## Minimum metadata

Every report records:

- exact harness revision;
- scenario path/id;
- agent and model;
- pass/fail/partial result;
- evidence ids used;
- whether an unsafe action was attempted;
- reproduction notes when possible.

Optional diagnostics include tool calls, duration and estimated cost.

## Privacy

Do not commit raw production transcripts, credentials, customer identifiers or proprietary telemetry. Prefer sanitized/synthetic scenarios and concise trajectory summaries.

## Submission

1. Copy `validation-reports/example.fixture.json`.
2. Fill in your run metadata.
3. Keep `source: fixture` unless an actual agent executed the scenario.
4. Open a PR, or use the `Agent validation run` Issue form when you want feedback before committing a report.
5. CI validates the report contract.

The long-term goal is a public verification board built from these reports. It should prioritize reproducibility and safety over a simplistic model leaderboard.
