# Skill Evaluation and Skill Lift

A clean `SKILL.md` can pass schema, style, license, and safety checks while still making a live agent worse. Skill quality therefore has two independent layers: authoring quality and runtime contribution.

## Paired execution

Run the same case under the same model, harness, workspace, tools, and scorer once without the target Skill and once with it. The normalized score difference is Skill Lift.

Contracts:

- `schemas/skill-eval-suite.schema.json` — task design
- `schemas/skill-paired-experiment.schema.json` — normalized baseline/treatment runs
- `schemas/skill-lift-report.schema.json` — calculated lift and usage deltas
- `skill-evals/policy.yaml` — repository gate
- `scripts/score_skill_lift.py` — deterministic scorer
- `scripts/check_skill_lift.py` — policy gate

## Experimental invariants

Keep these fixed for each pair: user task and inputs, model/version, agent harness/system policy, starting workspace, tool availability other than the target Skill, scorer/rubric, and isolation/retry policy. If those change, do not label the difference Skill Lift.

## Evaluate trajectories, not only answers

A live grader should inspect whether the right Skill was selected, irrelevant Skills were avoided, expected engineering steps occurred, prohibited actions were avoided, tools were used productively, and the final task completed successfully. Preserve a trajectory reference or normalize an interchange format such as ATIF when available.

Infrastructure Skills should be rewarded for evidence-first reasoning and penalized for unsafe shortcuts: no invented telemetry, no scaling a healthy tier when a dependency is the bottleneck, no production mutation to prove a hypothesis, no human-gate bypass, and no broad operational context loading for negative cases.

## Gates and status

Thresholds are configuration rather than universal truth. The checked-in policy is a starting point and should be recalibrated after enough live runs exist.

A fixture report can gate scorer regressions but cannot make a Skill `live_verified`. Only paired live reports from a real agent runtime can do that.

## External evaluators

The contracts are provider-neutral. NVIDIA SkillEvaluator/ACES, Codex, Claude Code, Kiro, or another runner may execute the pair. Adapters normalize output into the paired experiment contract; core scoring and policy remain runner-independent.
