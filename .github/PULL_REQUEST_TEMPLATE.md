## What changed

<!-- Keep this focused. -->

## Why

<!-- Link a scenario, validation result, issue, incident pattern, or reference model when relevant. -->

## Harness layer

- [ ] Knowledge / Context
- [ ] Domain / Decision Skill
- [ ] Capability / Adapter
- [ ] Environment / Evidence
- [ ] Runtime / Loop
- [ ] Eval / Validation
- [ ] Community / Docs

## Documentation impact

- [ ] I checked whether this changes behavior, architecture, configuration, CLI/API/schema contracts, setup, operations, release status, evaluation meaning, or safety boundaries.
- [ ] Relevant canonical documentation was updated, or no documentation change is required because the documented contract is unchanged.
- [ ] New or moved project documentation is reachable from docs/README.md.

See docs/DOCUMENTATION.md for the documentation maintenance rules.

## Validation

<!-- Paste the commands/results you ran. -->

~~~text

~~~

## Safety / invariants

- [ ] No secrets or proprietary production data are included.
- [ ] Provider output is not treated as verified engineering truth without the existing evidence boundary.
- [ ] Production authorization is not broadened by this PR.
- [ ] Third-party reference_only capabilities do not gain execution authority.
- [ ] Fixture results are not presented as live Skill/Context/Agent effectiveness evidence.

## Artifact hygiene

- [ ] I checked for duplicate truth and used the canonical home.
- [ ] I preferred a clean current-state artifact over additive patch residue.
- [ ] I preserved authoritative history where history is part of the artifact.
