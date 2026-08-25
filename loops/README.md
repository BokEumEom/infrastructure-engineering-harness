# Loop Engineering

Loop Engineering is the control layer above domain Skills.

```text
Knowledge + Evidence
        ↓
     Context
        ↓
      Skill
        ↓
       Loop
 Observe → Decide → Act/Propose → Verify
   ↑                           ↓
   └────── Reconcile / Learn ─┘
```

A **Skill** defines what an agent can do. A **Loop** defines when to invoke skills, what must be independently verified, when to stop, when to escalate, and what learning must be written back.

## Invariants

1. **External state** — loop state is explicit and lives outside model prose.
2. **Verified facts only** — `verified_facts` may be updated only from environment, tool, human, or test evidence.
3. **No self-certified done** — an agent statement is never sufficient to satisfy a terminal condition.
4. **Bounded execution** — every loop has iteration, duration, and no-progress budgets.
5. **Regression obligations** — previously established guarantees remain obligations in later iterations.
6. **Human gates** — production mutation, authorization changes, destructive actions, and financial commitments remain independently authorized.
7. **Learning is explicit** — incidents, runbooks, measurements, policies, ADR candidates, and eval candidates are declared writebacks.

## Reference loops

- `incident-response` — investigate → verify → mitigate/propose → verify recovery → learn
- `reliability-improvement` — baseline SLO/error budget → prioritize → track → remeasure → learn
- `delivery-improvement` — baseline delivery → identify constraint → improve → remeasure → learn
- `finops-optimization` — inform → optimize → track/operate → measure realized value → learn
- `change-validation` — precheck → approval → external execution → post-verify → regression check → learn

## Autonomy levels

- `observe` — read, analyze, verify, report.
- `workflow` — may create/update workflow artifacts such as tickets when policy permits; no production mutation.
- `change` — can orchestrate a change workflow but execution is delegated to an independently authorized system and human gates apply.

## Runtime contract

Loop definitions conform to `schemas/loop-spec.schema.json`. Execution state conforms to `schemas/loop-state.schema.json`. Terminal output conforms to `schemas/loop-result.schema.json`.

A runtime should execute **one iteration at a time**: load the Loop Spec and external state, invoke the current Skill/action, collect independent observations, update verified facts, check regression obligations and budgets, then continue/wait/escalate/fail/done.

`loops/runtime.py` contains deterministic reference helpers for state transitions, verified facts, progress budgets, and regression status. It is intentionally not a production workflow engine.

## Done means verified

An agent statement is not a completion check. Success criteria must be independently verified, regression obligations must pass, required human gates must be clear, and the loop must remain within its budget.

## Evaluation

Loop evals judge the execution trace, not just a final classification.

```bash
python scripts/check_loop_eval.py evals/loops/standard.json incident-recovered examples/eval-output/loop-incident-recovered.json
```
