# Infrastructure Engineering Harness — Agent Guide

This is the cross-agent operating contract for Codex, Kiro, Claude Code adapters, and other repository-aware agents.

## Prime directive

Treat infrastructure work as an evidence-based engineering decision, not a code-generation task.

For one-shot analysis use the relevant Domain Skill. For work that requires repeated observation, verification, change follow-up, or learning, use the `loop-engineering` control layer and a Loop Spec under `loops/`.

## Context roots

Use an explicitly supplied context path first. Otherwise use `.infra-context/` for embedded mode or `contexts/<service-or-platform>/` for central mode. Load progressively; do not load the whole knowledge base by default.

## Domain routing

- architecture, capacity, dependencies, migration, infrastructure change → `domains/infrastructure/README.md`
- SLI/SLO, error budget, incidents, reliability, toil → `domains/sre/README.md`
- build, release, deployment, rollback, delivery performance → `domains/devops/README.md`
- cost, allocation, usage efficiency, commitments, unit economics → `domains/finops/README.md`

## Loop routing

Use `skills/loop-engineering/SKILL.md` and the matching Loop Spec when the task requires repeated feedback:

- incident lifecycle → `loops/incident-response/loop.yaml`
- SLO/error-budget improvement → `loops/reliability-improvement/loop.yaml`
- delivery bottleneck improvement → `loops/delivery-improvement/loop.yaml`
- FinOps optimization and realized-value verification → `loops/finops-optimization/loop.yaml`
- pre/post production change verification → `loops/change-validation/loop.yaml`

Loop invariants:

1. Loop state is explicit and external to model prose.
2. Keep assumptions separate from verified facts.
3. `verified_by: agent` is invalid; facts require environment/tool/human/test evidence.
4. Never self-certify `done`.
5. Enforce iteration and no-progress budgets.
6. Preserve previous guarantees as regression obligations.
7. Do not use repeated iterations to bypass a human or policy gate.
8. Terminal loops emit explicit learning/writeback candidates.

## Evidence contract

Material recommendations must be traceable to evidence IDs conforming to `schemas/evidence.schema.json`. Never invent telemetry, SLO, delivery, cost or business values.

## MCP ticketing workflow

Jira and Linear workflow writes use connected MCP servers. Build a provider-neutral Ticket Request, apply Ticket Policy, compute a stable fingerprint, search before create, and create/update only when the policy and user authorization permit. Ticket permission never implies production mutation permission.

## Safety contract

Prefer read-only discovery. Production changes follow `workflows/change-proposal.md`; ticket writes follow `workflows/ticketing.md`. Production mutation, destructive actions, authorization expansion and financial commitments remain independently authorized. Hooks are defense-in-depth, not a security boundary.

## Validation

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/check_loop_eval.py evals/loops/standard.json incident-recovered examples/eval-output/loop-incident-recovered.json
python -m unittest discover -s tests
python -m compileall scripts hooks adapters loops
```

## Repository map

- `domains/` — Infrastructure, SRE, DevOps, FinOps lenses
- `loops/` — bounded Engineering Loops and reference runtime helpers
- `schemas/` — context, evidence, change, ticket, loop and eval contracts
- `evals/` — one-shot and long-horizon regression scenarios
- `skills/` — Claude Code skills including Loop Engineering
- `adapters/` and `mcp/` — optional evidence/workflow integrations
- `workflows/` — production change and ticketing workflows
- `docs/REFERENCE-MODELS.md` — research and operational models behind the harness
