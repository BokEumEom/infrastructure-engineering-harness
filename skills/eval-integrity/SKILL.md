---
name: eval-integrity
description: Audit an eval, benchmark, metric, paired experiment, holdout, or success gate for circularity and leakage before using it as evidence. Check independent ground truth, scorer/designer separation, control isolation, fixture/live separation, negative controls, and whether only the intended variable changes. Read-only by default.
---

# Eval Integrity

Use this Skill before treating an evaluation result as proof that a Skill, context revision, Loop, or engineering change is better.

## Goal

Determine whether the validation contains an independent signal of reality or merely lets the system, designer, dataset, and scorer confirm one another.

## Checks

1. **Independent truth** — identify what external observation, deterministic oracle, human decision, environment result, or held-out fact can falsify the claim.
2. **Variable isolation** — for paired experiments, confirm baseline and treatment differ only by the intended Skill/context/change variable.
3. **Scorer separation** — flag cases where the same component creates expectations and then grades conformity to those expectations without an external check.
4. **Control leakage** — verify the control removes the underlying signal, not just its obvious label or surface form.
5. **Dataset independence** — check whether train/design/eval examples, labelers, fixtures, or generated cases share a source that can carry the same bias to both sides.
6. **Framing leakage** — check whether prompts, task labels, expected outcomes, or evaluator instructions reveal the hypothesis being tested unnecessarily.
7. **Fixture vs live** — fixture data may verify evaluator plumbing but must not be cited as live effectiveness evidence.
8. **Negative controls** — include cases where the Skill/context should not activate or where no improvement is expected.
9. **Trajectory evidence** — when tool use, workflow adherence, routing, or safety is part of the claim, grade the execution trajectory rather than final prose alone.

## Rules

- Read-only by default: identify the integrity risk and the smallest independence fix; do not silently rewrite the experiment.
- Same-model or same-session agreement is supporting evidence, not independent proof.
- A clean-looking score is not stronger evidence when the scorer and target share the same assumptions.
- High-stakes claims should prefer environment/test/human evidence that can disagree with the agent.
- Preserve the distinction between `source: fixture` and `source: live` in Skill Lift and Context Lift.

## Output

Return `pass`, `unclear`, or `fail`, the single most load-bearing integrity reason, affected checks, and the smallest change that would introduce independent evidence.
