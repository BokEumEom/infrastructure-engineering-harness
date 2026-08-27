# Loop Engineering

Loop Engineering is the control layer for long-running infrastructure work.

The default model is **adaptive**: a Loop defines the goal, state, hard constraints, terminal conditions, budgets, and useful actions. It does not force a capable model through a static reasoning sequence.

```text
Goal + External State + Constraints
              ↓
      Model Judgment
              ↓
       Next useful action
              ↓
 Runtime / authorization / evidence boundary
              ↓
     Independent observation
              ↓
          Reconcile
              ↓
 continue / wait / verify / escalate / fail / done
```

A **Skill** provides optional task-specific guidance. A **Loop** decides whether the work remains within authority and budget, what is independently verified, and whether terminal conditions are actually satisfied.

## Invariants

1. **External state** — Loop state is explicit and lives outside model prose.
2. **Verified facts only** — `verified_facts` may be updated only from environment, tool, human, or test evidence.
3. **No self-certified done** — an agent statement is never sufficient to satisfy a terminal condition.
4. **Bounded execution** — every Loop has iteration, duration, and no-progress budgets.
5. **Regression obligations** — previously established guarantees may remain obligations.
6. **Human gates** — production mutation, authorization changes, destructive actions, and financial commitments remain independently authorized.
7. **Learning is explicit** — durable learning is proposed as governed writeback, not silently promoted.
8. **Epistemic classes stay separate** — Observation, Verified Fact, Engineering Assessment, Learning Candidate, and Durable Knowledge are not collapsed.
9. **Reasoning order is not a hard invariant** — investigation/checkpoint order is left to model judgment unless the real process requires sequencing.

## Adaptive vs sequential

### Adaptive

Use for reasoning-heavy work such as incident investigation where the best next check depends on current evidence.

An adaptive Loop exposes `actions` with `when_useful` hints. They are affordances, not a required order.

### Sequential

Use when ordering itself is part of the engineering contract: for example a regulated rollout, a migration with irreversible phase boundaries, or a reproducible operational procedure.

Sequential Loops may continue to use `steps`.

## Context

Adaptive Loops should prefer pull-based context:

```text
minimal seed
    ↓
information need
    ↓
bounded retrieval
    ↓
freshness / permission / authority filter
    ↓
updated Context Pack
```

The model may request more context, but retrieval cannot expand execution authority.

## Runtime contract

Loop definitions conform to `schemas/loop-spec.schema.json`. Execution state conforms to `schemas/loop-state.schema.json`. Terminal output conforms to `schemas/loop-result.schema.json`.

The reference runtime executes one reconciliation iteration at a time. It does not prescribe the model's reasoning path.

## Reference loops

- `incident-response` — adaptive evidence/mitigation/recovery reconciliation
- `reliability-improvement`
- `delivery-improvement`
- `finops-optimization`
- `change-validation`

Existing reference Loops may be sequential until migrated. Sequential is supported, but no longer assumed to be inherently better.

## Done means verified

Success criteria must be independently verified, required regression obligations must pass, required human gates must be clear, and the Loop must remain within budget.

## Learning boundary

A terminal or abandoned Loop may emit Knowledge Candidates. A candidate never becomes authoritative merely because another agent retrieves it.

See `docs/HARNESS-UNHOBBLING.md`, `docs/KNOWLEDGE-CONSOLIDATION.md`, and `schemas/knowledge-candidate.schema.json`.
