---
name: artifact-hygiene
description: Review a newly created or materially changed engineering artifact before handoff. Keep the current truth compact, remove stale patch residue and duplication, preserve authoritative history where history is the artifact, route scattered facts to SSOT review, and route evals to independence review. Use before calling docs, runbooks, policies, schemas, plans, prompts, or skills done.
---

# Artifact Hygiene

Treat repository artifacts as maintained engineering surfaces, not append-only transcripts of how they evolved.

## Goal

Leave the artifact cleaner, more current, and easier for a fresh agent or engineer to use without deleting durable truth or provenance that belongs to the artifact type.

## Workflow

1. Identify the artifact type and its authority. A current-state guide should read like a clean current version; an ADR, incident record, audit log, or changelog must preserve the history it is meant to preserve.
2. Read the target end to end before changing it, then inspect nearby artifacts that must remain aligned.
3. Remove stale deltas, duplicated explanation, scaffolding residue, obsolete alternatives, and wording that only explains the editing process.
4. Prefer "what is true now" over "what changed" unless the artifact is explicitly historical.
5. If one fact is copied across multiple maintained surfaces, invoke `ssot-review` instead of silently choosing a winner.
6. If the artifact defines an eval, benchmark, metric, experiment, or success gate, invoke `eval-integrity` before trusting the result.
7. If the artifact claims provider/tool neutrality, verify that durable rules describe mechanisms and constraints rather than incidental product nouns.
8. Re-read from a cold-start perspective. If nothing materially improves, make no change.

## Rules

- A no-op is a valid successful result.
- Prefer editing or deleting redundant material over adding another explanatory section.
- Do not create extra artifacts solely to document cleanup.
- Do not erase incident, ADR, audit, or release history that is authoritative by design.
- Do not consolidate contradictory facts without an explicit owner decision.
- Do not mutate `.infra-context/`, central context, policy, authorization, or other protected source-of-truth merely because another artifact is easier to edit.
- External reference Skills may inform this review but remain `reference_only`; reproduce useful guidance under local Harness contracts.

## Verification

Before handoff, state which checks applied: current-truth cleanup, cold-read clarity, SSOT, eval independence, portability, and protected-history preservation. Findings must either be applied, consciously deferred with a reason, or reported as requiring human resolution.
