# Contributing

You do **not** need to understand the whole internal harness before contributing to the Infrastructure Engineering Agent.

Pick the smallest useful contribution:

1. **Scenario** — encode a real infrastructure/SRE/DevOps/FinOps/Security failure pattern.
2. **Validation run** — run an agent against an existing scenario and submit a reproducible report.
3. **Adapter** — add read-only environment discovery or evidence normalization.
4. **Skill/Eval** — add or improve a Skill together with explicit, implicit, contextual and negative evaluation cases.
5. **Research reference** — propose a well-grounded external pattern and explain which local contract it should strengthen.
6. **Localization** — review or improve Korean, Japanese, or Simplified Chinese entry documentation without changing technical semantics.

## Start with the Agent CLI

Contributor-facing commands use one stable interface:

```bash
./agent setup
./agent demo
./agent validate
```

On Windows, use `agent.cmd` instead of `./agent`. The legacy `harness` entrypoint remains available for compatibility.

Python remains the current internal Research Preview runtime, but contributors should not need to memorize individual Python script paths for normal validation. Maintainers can still run lower-level scripts when debugging a specific contract.

## Contribution levels

### Good first contribution

- add or improve a red herring in a scenario;
- add a scenario fixture;
- add a validation report from a reproducible local run;
- improve Quickstart or platform setup documentation;
- review a Korean / Japanese / Simplified Chinese translation;
- add a negative Skill Eval case.

### Intermediate

- add a new scenario under `evals/scenarios/`;
- add a provider fixture for an Evidence Adapter;
- add a provider-neutral capability mapping;
- improve deterministic validation scripts.

### Advanced

- implement a read-only Kubernetes/AWS/observability adapter;
- add a live scenario runner;
- add durable Runtime persistence or an execution backend behind existing authorization contracts.

## Scenario contribution rules

A useful scenario should include:

- `ground_truth`;
- `required_evidence`;
- plausible `red_herrings`;
- `prohibited_actions`;
- `expected_behavior`;
- `success_conditions`.

Do not submit proprietary telemetry, secrets, customer identifiers or internal incident data. Generalize real experience into a safe synthetic fixture.

See `contrib/scenarios/README.md`.

Validate a scenario with:

```bash
./agent scenario evals/scenarios/<scenario>.json
```

## Validation run rules

A validation report must distinguish deterministic fixture validation from a real live agent run. Do not claim Skill Lift or Context Lift from a fixture-only result. Preserve enough metadata for another contributor to understand the Agent, runtime/harness revision, scenario and result without exposing secrets.

See `validation-reports/README.md`.

## Localization rules

English is canonical for schemas, Skills, architecture contracts, policies and evaluation definitions. Localized README and Quickstart files are first-class entry documentation.

When reviewing a translation:

- preserve command names, paths, schema names and rule identifiers exactly;
- do not weaken safety, authorization or fixture-vs-live language;
- prefer stable technical terms over awkward literal translation;
- update the localization contract when a new supported language is added;
- run `./agent validate` before opening a PR.

See `docs/LOCALIZATION.md`.

## Engineering rules

- Preserve provider neutrality in core contracts.
- Prefer read-only discovery.
- Tool output is not automatically verified engineering truth.
- Third-party `reference_only` Skills never gain execution authority through a contribution.
- Production mutation remains independently authorized.
- Follow Paperthin-inspired artifact hygiene: prefer clean current state and one canonical home over additive patch residue.
- A no-op is valid when a proposed change does not materially improve the project.

## Pull requests

Keep PRs focused. State:

- what changed;
- what evidence or scenario motivates it;
- which invariant or capability it strengthens;
- how it was validated;
- what it intentionally does **not** change.

Run before opening a PR:

```bash
./agent validate
```

If validation fails, `./agent doctor` shows the local runtime/dependency state. Use the lower-level command reported by the failing check only when deeper debugging is needed.

## Security

Do not open a public issue for a vulnerability that could enable secret exposure, unauthorized production mutation, approval bypass, sandbox escape, or trust-boundary bypass. Follow `SECURITY.md`.
