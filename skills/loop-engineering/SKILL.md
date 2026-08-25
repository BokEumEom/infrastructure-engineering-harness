---
name: loop-engineering
description: Orchestrate long-running infrastructure engineering work as bounded observe-decide-act-verify-reconcile loops with explicit external state, independent verification, regression obligations, human gates, and learning writeback. Use when work requires repeated checks across incidents, reliability, delivery, FinOps, or change validation rather than a one-shot answer.
---

# Loop Engineering

Use this Skill as the control layer above domain Skills.

Read `loops/README.md`, the selected `loops/<loop-id>/loop.yaml`, and `docs/REFERENCE-MODELS.md`.

## Core rule

A Skill may propose an answer. A Loop decides whether the work may continue, must wait/escalate, or is actually done. Never mark a loop done because the agent says the goal is complete.

## Execution model

1. Load the Loop Spec and current external Loop State.
2. Resolve only the context required for the current step.
3. Invoke the specified domain Skill or action.
4. Collect environment/tool/human/test observations.
5. Update `verified_facts` only from independently verified observations.
6. Record one iteration and material/no-progress status.
7. Check human gates, regression obligations, and execution budgets.
8. Decide: continue, wait, verify, escalate, fail, budget-exhausted, or done.
9. On terminal state, emit a Loop Result and explicit learning/writeback.

## State rules

- State is explicit and should survive model/context resets.
- Keep assumptions separate from verified facts.
- `verified_by: agent` is invalid.
- Do not hide missing evidence inside confidence language.
- Do not reset no-progress counters unless material progress occurred.
- Previous successful guarantees remain regression obligations until the loop terminates.

## Human gates

Loop iteration must never be used to bypass independent approval for production mutation, destructive operations, authorization expansion, financial commitments, or other organization-defined high-impact actions.

## Loop-compatible Skill handoff

```yaml
loop_handoff:
  event: <stable_event_name>
  outcome: progress | no_progress | blocked | verified | failed | escalated
  evidence_refs: []
  verified_conditions: []
  assumptions: []
  next_action:
    type: skill | action | wait | human_gate | terminal
    target: <name>
  writeback_candidates: []
```

The handoff is not authoritative evidence. Only independent observations may enter `verified_facts`.

## Completion

Before `done`, all required success criteria must be independently verified, required regression obligations must pass, no required human gate may remain pending, and the loop must still be within its budget.

## Learning

Terminal loops should explicitly propose durable learning: Incident, Runbook change, ADR candidate, Policy candidate, Eval candidate, Measurement, Delivery record, Optimization record, or Change record. Do not silently overwrite organizational source-of-truth documents.
