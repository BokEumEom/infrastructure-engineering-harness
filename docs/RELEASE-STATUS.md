# Release Status

## v0.1 target: Research Preview

The repository is preparing for a `v0.1.0` research-preview release. This status describes what users may rely on today and what remains experimental.

### Available now

- contributor-facing `harness` CLI for setup, demo, validation, scenario checks and local diagnostics;
- first-class README and Quickstart entry documentation in English, Korean, Japanese and Simplified Chinese;
- CI localization drift checks for public status, CLI, safety and evaluation-boundary markers;
- provider-neutral Domain and Decision Skill contracts;
- Capability Registry and third-party reference trust boundary;
- Infrastructure/SRE/DevOps/FinOps/Security domain evals;
- bounded Engineering Loops;
- paired Skill Lift and Context Lift contracts;
- Paperthin-inspired artifact hygiene and eval integrity;
- reference Runtime Kernel contracts;
- provider-neutral Resource Graph, Bound Capability and Evidence Adapter contracts;
- deterministic scenario fixtures and cross-file validation;
- community Validation Report contract.

The public Quickstart interface is `./harness` on macOS/Linux and `harness.cmd` on Windows. Python 3 remains the current internal implementation/runtime dependency for the Research Preview; it is not intended to be the long-term user-facing contract.

English remains canonical for machine-readable schemas, Skills, architecture contracts, policies and evaluation definitions. Localized entry documentation is governed by `docs/LOCALIZATION.md` rather than duplicating every safety-critical technical contract.

### Experimental

- live environment discovery adapters;
- live observability/evidence adapters;
- live agent scenario runners;
- persistent Runtime state/event storage;
- controlled execution backends.

### Not a current promise

- autonomous production mutation;
- the model acting as the production authorization boundary;
- fixture results proving real agent effectiveness;
- support for every cloud/tool/provider without an explicit adapter;
- a stable live-agent `harness run` interface before runner adapters are reproducible;
- full translation of every technical contract into every supported language.

A `v0.1.0` tag should be cut only after the Community & Validation Ready checklist is merged and the Harness CLI Quickstart is verified from clean macOS/Linux and Windows checkouts.
