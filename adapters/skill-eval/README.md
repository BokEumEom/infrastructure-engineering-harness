# Skill Evaluation Adapters

Live agent execution is an adapter boundary.

An adapter is responsible for:

1. creating isolated baseline and treatment workspaces;
2. holding prompt, model, tools and grader policy constant;
3. enabling the target Skill only in treatment;
4. capturing trajectory and usage evidence;
5. grading the six normalized runtime signals;
6. emitting `schemas/skill-paired-experiment.schema.json`.

The core harness does not require one agent runtime.

## NVIDIA SkillEvaluator

NVIDIA SkillEvaluator is a compatible reference implementation of the paired ACES methodology and can supply live runs. Do not make it a mandatory core dependency. When used, preserve its paired experiment controls and normalize the resulting signals and trajectory references to the harness contract.

A report produced from a real runner uses:

```json
"source": "live"
```

A checked-in deterministic test vector uses:

```json
"source": "fixture"
```

Never promote fixture results to `live_verified`.
