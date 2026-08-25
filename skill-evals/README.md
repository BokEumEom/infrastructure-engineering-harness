# Skill Runtime Evaluation

Static validation asks whether a Skill is well formed. Runtime evaluation asks whether the Skill makes an agent perform the same task better.

The repository uses a paired protocol inspired by NVIDIA ACES:

```text
same task + model + workspace + scorer

without target Skill ─┐
                      ├─ compare trajectories/outcomes → Skill Lift
with target Skill ────┘
```

## Runtime signals

Normalized runs preserve six signals: `security`, `skill_execution`, `skill_efficiency`, `accuracy`, `goal_accuracy`, and `behavior_check`.

The harness reports five dimensions:

- Security = `security`
- Correctness = `accuracy`
- Discoverability = `skill_execution`
- Effectiveness = mean(`goal_accuracy`, `behavior_check`)
- Efficiency = `skill_efficiency`

`mean_outcome_lift` averages `accuracy` and `goal_accuracy` lift. Token, tool-call, and duration changes are report-only signals; fewer tokens do not automatically mean better engineering.

## Case design

Every repository-owned Skill should eventually include explicit, implicit, contextual, and negative cases. A Skill that helps positive tasks but activates on irrelevant work is not healthy.

## CI levels

`fixture` experiments validate schemas, scoring, and gating logic only. They are not evidence that a Skill improves a live agent.

`live` experiments must keep prompt, model, harness, workspace, tools, and scorer fixed while changing only target Skill availability. Run them in isolated environments and retain trajectory references.

Recommended cadence:

- PR: static checks + deterministic fixtures + changed-Skill live suite when a runtime is configured
- nightly/release: full paired live regression across supported harnesses
- registry: only mark `live_verified` from live reports, never fixture reports

See `docs/SKILL-EVALUATION.md`.
