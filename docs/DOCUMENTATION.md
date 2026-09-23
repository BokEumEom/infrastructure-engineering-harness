# Documentation Policy

The documentation system is optimized for progressive disclosure, low duplication, and resistance to code/document drift.

## Canonical layout

Project-level technical documentation belongs under docs/.

The repository root keeps only entry or governance artifacts whose location is part of the repository interface, such as README.md, AGENTS.md, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, and localized entry documentation. Component-local README files, Skills, schemas, fixtures, and executable contracts stay next to the component they describe when locality is part of how they are used.

docs/README.md is the canonical documentation index.

## Progressive disclosure

Documentation should normally follow this path:

~~~text
root README
    ↓
docs/README.md
    ↓
topic overview or category index
    ↓
focused detail document
~~~

Keep overview documents small. Prefer links to canonical detail over copied summaries. A reader should usually reach a focused document within two or three navigation steps.

Do not split a small document merely to satisfy structure. Split when a section has an independent lifecycle, audience, or maintenance owner.

## Change triggers

Update the relevant documentation when a change affects:

- user-visible behavior or workflows;
- architecture or component boundaries;
- source-of-truth ownership;
- configuration, CLI, API, schema, or compatibility contracts;
- installation, setup, operations, or troubleshooting;
- release status or capability availability;
- evaluation semantics or evidence claims;
- safety, authorization, or verification boundaries.

A documentation change is usually not required for:

- internal refactoring with no behavior change;
- formatting-only changes;
- test-only changes that do not change the documented contract;
- implementation cleanup that preserves public behavior.

The decision is impact-based, not file-count-based.

## Architecture, decisions, and evidence

Architecture documentation describes the current state.

Durable decisions that explain why the current state exists belong under [decisions/](decisions/README.md). Do not turn architecture pages into chronological decision logs.

Evaluation results, benchmarks, validation guidance, and claim-supporting artifacts are routed through [evidence/](evidence/README.md). Runtime Evidence Adapter implementation remains in adapters/evidence/; that code is not the documentation evidence archive.

## Automated checks

Run:

~~~bash
python scripts/check_docs.py
~~~

The structural check verifies:

- docs/README.md exists and is reachable from root README.md;
- local Markdown links resolve;
- top-level documentation and category indexes are indexed;
- documents under docs/ are reachable from the canonical index.

On pull requests, CI also emits a non-blocking documentation-drift warning when functional areas change without any Markdown documentation change. This is advisory because not every code change requires documentation.

Structural checks do not prove that prose matches the implementation.

## Human semantic review

Periodically, and before material releases, review semantic correctness rather than rereading every file indiscriminately.

Focus on changed or high-risk surfaces:

- does root README still describe the actual project boundary?
- does docs/README.md route to the current canonical documents?
- does Architecture match current component ownership and execution flow?
- does Quickstart still run as written?
- are release-status and capability claims current?
- did recent material changes omit documentation updates?
- are duplicate, obsolete, or orphaned explanations accumulating?
- do evaluation and evidence claims still point to reproducible support?

A review may legitimately conclude that no documentation change is needed.

## Adding or moving documents

When adding a document:

1. put project-level technical documentation under docs/;
2. link it from the nearest relevant index;
3. update docs/README.md only when the top-level navigation changes;
4. keep one canonical home for each durable explanation;
5. run python scripts/check_docs.py.

Avoid bulk renames or directory churn solely for aesthetics. The current flat technical documents can move into category directories incrementally when a move reduces ambiguity or maintenance cost.
