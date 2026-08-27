---
name: loop-engineering
description: Reconcile long-running infrastructure engineering goals against explicit external state, independent verification, hard constraints, budgets, and terminal conditions. Use when work requires repeated observation or follow-up rather than a one-shot answer.
---

# Loop Engineering

A Loop constrains state, authority, verification, and completion. It should not unnecessarily prescribe how a capable model must reason.

Read the selected `loops/<loop-id>/loop.yaml` and only the additional guidance needed for the current task.

## Control model

```text
Goal + Current State + Hard Constraints + Terminal Conditions
                         ↓
               Model chooses next action
                         ↓
          Runtime / policy / authorization gate
                         ↓
                New evidence or outcome
                         ↓
              Independent verification
                         ↓
                    Reconcile
```

Sequential steps are appropriate only when the real process is intrinsically ordered or reproducibility requires them. Adaptive Loops expose useful actions/checkpoints without forcing their order.

## Invariants

- Loop state is explicit outside model prose and survives context resets.
- `verified_facts` accept only environment/tool/human/test verification with evidence references.
- Assumptions and engineering assessments are not verified facts.
- Missing evidence stays missing; confidence does not fill a gap.
- Repetition cannot bypass production, destructive, permission, or financial authorization.
- Iteration, duration, and no-progress budgets are enforced.
- Existing guarantees may remain regression obligations.
- `done` requires independently verified terminal conditions, not agent self-certification.

## One iteration

For the current state:

1. start with the minimal Context Pack;
2. pull additional context/evidence only when useful;
3. choose the highest-value permitted next action;
4. collect the resulting environment/tool/human/test observation;
5. update verified state only from independent evidence;
6. check hard constraints, human gates, regressions, budgets, and terminal conditions;
7. continue, wait, verify, escalate, fail, exhaust budget, or finish.

The numbered list is a control-plane lifecycle, not an investigation recipe.

## Loop handoff

```yaml
loop_handoff:
  event: <stable_event>
  outcome: progress | no_progress | blocked | verified | failed | escalated
  evidence_refs: []
  verified_conditions: []
  assumptions: []
  next_action:
    type: skill | action | context | evidence | wait | human_gate | terminal
    target: <name>
  writeback_candidates: []
```

A handoff does not make its claims true.

## Learning

Terminal or abandoned Loops may propose Knowledge Candidates, incident/runbook updates, ADR/policy candidates, measurements, eval cases, and negative corpus entries. Preserve supporting and contradicting evidence. Promotion into durable organizational knowledge follows the artifact owner's normal review path.

See `docs/HARNESS-UNHOBBLING.md` and `docs/KNOWLEDGE-CONSOLIDATION.md`.
