# Artifact Reflexes

Infrastructure Engineering Harness uses a small set of cross-cutting artifact reflexes so agents do not treat every request as a reason to add more files, rules, or prose.

These patterns are informed by `LilMGenius/paperthin` but are implemented locally under Harness evidence, safety, approval, Skill Lift, Context Lift, and source-of-truth contracts.

## Reflex model

```text
Create / Change Artifact
          ↓
   Artifact Hygiene
          │
          ├─ current-state artifact → clean current v0
          ├─ historical artifact → preserve authoritative history
          ├─ scattered fact → SSOT Review
          ├─ eval/metric → Eval Integrity
          └─ nothing material wrong → no-op
          ↓
      Local Validation
          ↓
  Domain / Change / Security Review as needed
          ↓
       Handoff / Loop
```

## 1. Clean current state, not patch scars

For current-state docs, Skills, plans, runbooks, and instructions, prefer the smallest artifact that states what is true now. Remove stale deltas, duplicated explanation, scaffolding residue, and editing history that does not help future execution.

This rule does **not** apply by erasing provenance from ADRs, incident records, audit logs, changelogs, or other artifacts whose purpose is to preserve history.

A pass that finds nothing material to improve should change nothing.

## 2. One maintained truth, one canonical home

When a fact or decision is scattered across maintained artifacts:

1. audit occurrences read-only;
2. classify copies, partials, stale values, contradictions, and intentional boundary copies;
3. identify the strongest canonical home;
4. preserve unique details;
5. propose references/removals/reconciliation;
6. mutate only after approval when the change crosses maintained artifacts.

Do not consolidate across trust, visibility, customer, tenant, security, or legal boundaries merely to reduce duplication.

## 3. Eval independence

A score is not automatically evidence. Skill Lift, Context Lift, domain evals, and loop evals should identify an independent signal that can disagree with the agent or scorer.

Check:

- baseline/treatment variable isolation;
- independent truth or deterministic oracle;
- scorer/designer circularity;
- control leakage;
- shared dataset/labeler bias;
- framing leakage;
- negative controls;
- fixture/live separation;
- trajectory evidence when process quality is part of the claim.

## 4. Earned reuse across loops

A failed or disappointing cycle can still produce durable value. Preserve only what earned reuse through evidence: contracts, schemas, gates, vocabulary, runbooks, verified procedures, real-surface tests, and negative corpus.

Do not copy forward accidental architecture merely because implementation already exists. Learning writeback should make the next cycle's first gate explicit.

## External reference boundary

Reference source:

```text
LilMGenius/paperthin
revision: 3bca079a51bcfff5dafb53d1d7f9f523d66ee317
license: MIT
trust: pinned_reference
execution: reference_only
```

Selected reference Skills are registered in `capabilities/registry.yaml`. Their commands, scripts, and mutation rules are never automatically trusted or executed. The Harness reproduces useful principles through local governed Skills.

## Local Skills

- `skills/artifact-hygiene/SKILL.md`
- `skills/ssot-review/SKILL.md`
- `skills/eval-integrity/SKILL.md`

These are cross-cutting control/verification Skills, not new engineering Domains.
