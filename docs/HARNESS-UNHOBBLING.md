# Harness Unhobbling

Infrastructure Engineering Harness should improve engineering outcomes without teaching capable models a rigid way to think.

The design principle is:

> **The harness should constrain authority and truth, not intelligence.**

This follows a broader context-engineering shift: as model capability improves, accumulated instructions can become redundant, conflicting, or overly prescriptive. Anthropic reported in July 2026 that it removed more than 80% of Claude Code's system prompt for newer Claude models without measurable loss on its coding evaluations, and described the previous state as overconstrained.

Reference:
https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

The Harness treats that as a reference signal, not proof that every infrastructure agent should use less context. The correct amount of guidance must be measured against real tasks and models.

## Hard vs soft

### Hard invariants

These should be enforced by Runtime, schema, policy, tool boundaries, independent verification, or human authorization rather than repeated prompt prose:

- production mutation authorization;
- destructive action protection;
- privilege / permission expansion;
- financial commitment gates;
- evidence provenance;
- `verified_by: agent` rejection;
- append-only/auditable runtime events;
- monotonic deny;
- state revision and stale-update rejection;
- regression verification;
- source-of-truth protection.

### Soft guidance

These should normally be discoverable and loaded only when useful:

- investigation order;
- which hypothesis to consider first;
- which Domain lens to invoke;
- which Skill to read;
- implementation technique;
- preferred decomposition;
- report formatting beyond required contract fields;
- optional workflow checkpoints.

A capable model may choose a better path than a static procedure. The Harness should make that possible while preserving hard invariants.

## Minimal always-loaded context

Always-loaded agent guidance should answer only:

1. What is the objective of this repository?
2. Which hard invariants must never be inferred away?
3. Where can more context, Skills, Loops, and capabilities be found?
4. What does verified completion require?

Everything else should prefer progressive disclosure.

## Adaptive Loop

A Loop is primarily:

```text
Goal
 + current state
 + hard constraints
 + terminal conditions
 + budget
 + available actions/capabilities
```

It does not need to be a fixed chain of thought or fixed investigation order.

```text
Current State
     ↓
Model chooses best next action
     ↓
Harness checks authority / evidence / state
     ↓
Environment changes or new evidence arrives
     ↓
Independent verification
     ↓
Reconcile against goal and terminal conditions
```

Sequential steps remain valid when the real-world process is intrinsically ordered or when a reproducible procedure is the engineering requirement. They are no longer the default assumption for reasoning-heavy work.

## Pull-based context

Context Pack is an interface, not a prompt dump.

Start with minimal scope and allow the model/runtime to request additional context when uncertainty or the task requires it:

```text
Minimal seed context
       ↓
Model identifies information need
       ↓
Context Resolver retrieves bounded material
       ↓
Freshness / permission / authority filtering
       ↓
Updated Context Pack
```

The resolver should prefer authoritative knowledge and current evidence, expose gaps, and avoid injecting unrelated instructions.

## Harness Lift

A Harness change is not automatically an improvement because it is safer-looking, more detailed, or more structured.

Evaluate three profiles using the same task, model, workspace, tools, permissions, and scorer:

- **bare** — model + tools + hard Runtime/safety enforcement;
- **minimal** — bare + minimal invariants + progressive discovery;
- **full** — the richer/prescriptive Harness candidate being evaluated.

Measure:

- outcome correctness;
- evidence quality;
- safety;
- exploration quality;
- autonomy / unnecessary blocking;
- tool efficiency;
- token usage;
- duration;
- regression behavior.

The important comparison is not only `full > bare`. A full Harness is suspect when `minimal > full` with no safety or verification advantage.

Only live runs may support a claim that one Harness profile improves real agent performance. Checked-in fixtures validate scoring and CI plumbing only.

## Deletion is a valid optimization

Context engineering should be evidence-driven in both directions.

A rule can be removed when:

- the model already performs the behavior reliably without it;
- the rule duplicates a hard Runtime invariant;
- the behavior is narrow enough for a Skill;
- it conflicts with stronger task-local context;
- it reduces exploration or causes unnecessary tool calls;
- Harness Lift shows no benefit or a regression.

Do not preserve prompt instructions merely because they existed in earlier models.
