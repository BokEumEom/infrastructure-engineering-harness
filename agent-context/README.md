# Agent Context Learning

`AGENTS.md` is the always-loaded behavioral control surface for this harness. Treat it as a minimal, evidence-driven context artifact rather than an append-only notebook. The target is not the largest useful prompt; it is the smallest always-loaded guidance that still improves real outcomes.

The optimization loop is:

```text
Agent session
   ↓
Distilled + redacted transcript evidence
   ↓
Repeated loss pattern
   ↓
Context update proposal
   ↓
Human review
   ↓
Paired Context Lift evaluation
   ↓
Accept / reject
```

## What may be optimized

- concise cross-agent behavior rules in `AGENTS.md`
- routing guidance when repeated sessions show a real gap
- extraction of narrow procedures from `AGENTS.md` into a Skill
- stale or overbroad behavioral instructions when evidence supports removal or rewrite

## What must not be optimized from transcript frequency

The following are durable source-of-truth artifacts, not model weights:

- `.infra-context/` and `contexts/`
- Architecture and ADRs
- Policies and service catalog
- Domain definitions
- Eval specifications
- Loop contracts
- Capability trust metadata

A rule being rarely used is not evidence that an architecture fact, security policy, or reliability objective should disappear.

## Evidence rules

1. Raw transcripts are local/private runtime material and should not be committed.
2. Persist only redacted, minimal evidence records conforming to `schemas/context-evidence.schema.json` when needed for review.
3. Every proposed edit must cite session evidence.
4. A new instruction requires evidence from at least two independent sessions.
5. One proposal contains at most five edits.
6. Every edit is a proposal; no analysis step writes `AGENTS.md` automatically.
7. Rejected edits should not be repeated without materially new evidence.

## Instruction units

Address stable rules in `AGENTS.md` with comments such as:

```markdown
<!-- rule: production-independent-authorization -->
Production mutations remain independently authorized.
```

Rule IDs make transcript loss and proposals traceable without duplicating the full instruction set into another registry.

## Token budget

Always-loaded context has a recurring cost. The default project budget is 5,000 estimated tokens, checked by `scripts/check_agents_contract.py` using a harness-neutral bytes/4 estimate. The budget is a guardrail, not a precise tokenizer measurement.

The project budget is intentionally small. Additions should normally be zero-sum: rewrite, remove, or extract narrow procedures into a Skill rather than append. If a behavior is already enforced by Runtime/schema/policy, prefer deleting duplicate prompt prose.

## Context Lift

A cleaner-looking `AGENTS.md` is not sufficient evidence of improvement. Compare the old and proposed revision using the same task, model, harness, workspace, tools and scorer.

Dimensions:

- Safety
- Correctness
- Instruction adherence
- Routing quality
- Context efficiency

`source: fixture` validates the scorer and CI plumbing only. Only `source: live` paired runs may support a claim that a context revision improved real agent behavior.

See `schemas/context-paired-experiment.schema.json`, `schemas/context-lift-report.schema.json`, and `agent-context/policy.yaml`.

## Relationship to Skill Lift

```text
Skill Lift
  asks: does this Skill improve the agent?

Context Lift
  asks: does this always-loaded AGENTS.md revision improve the agent?

Loop Eval
  asks: did the system reach and retain a verified engineering outcome?
```

These are complementary regression layers, not substitutes for one another.

Harness Lift adds a third question: does the richer Harness improve on a minimal Harness, or is it hobbling model judgment? See `harness-evals/README.md` and `docs/HARNESS-UNHOBBLING.md`.
