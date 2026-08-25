---
name: context-backpass
description: Propose evidence-backed improvements to AGENTS.md from repeated agent-session loss without rewriting durable engineering source-of-truth context.
---

# Context Backpass

Use this Skill when the user wants to improve, prune, or validate project-level `AGENTS.md` from actual agent-session behavior.

## Goal

Treat `AGENTS.md` as a bounded behavioral control surface. Analyze repeated session loss and produce a small reviewable proposal. Do not auto-apply changes.

## Inputs

- current `AGENTS.md`
- `agent-context/policy.yaml`
- distilled, redacted session evidence conforming to `schemas/context-evidence.schema.json`
- optional Context Lift results

## Process

1. Confirm the target is `AGENTS.md`.
2. Distinguish behavioral instruction gaps from durable engineering knowledge.
3. Group repeated losses by rule or missing rule.
4. Require verbatim evidence for every proposed edit.
5. A new instruction requires at least two independent session IDs.
6. Prefer modify/remove/extract-to-skill over append-only growth.
7. Keep the proposal within the configured token budget and edit limit.
8. Produce a proposal conforming to `schemas/context-update-proposal.schema.json`.
9. Require human review before any write.
10. After a candidate revision exists, compare it with the baseline using paired Context Lift evaluation.

## Never do

- do not edit `.infra-context/`, `contexts/`, ADRs, Architecture, Policies, Domain definitions, Eval specs, Loop contracts, or Capability trust metadata based on transcript frequency;
- do not commit raw transcripts or secrets;
- do not treat a single anecdotal failure as sufficient evidence for a new global rule;
- do not rewrite the whole `AGENTS.md` when a smaller edit can address the loss;
- do not claim a real Context Lift from `source: fixture` data;
- do not bypass human review.

## Routing rule

Broad, frequent, cross-task behavior belongs in `AGENTS.md`. Narrow behavior with a detectable trigger should be extracted to an appropriate Skill. Narrow behavior without repeated evidence should normally remain out of always-loaded context.

## Output

Return:

- observed repeated losses;
- affected rule IDs;
- proposed edits and evidence session IDs;
- estimated before/after token usage;
- protected targets explicitly left untouched;
- paired Context Lift plan or result;
- human-review requirement.
