# Infrastructure Engineering Harness

An open-source Claude Code plugin that turns infrastructure knowledge into reusable agent context for safer infrastructure analysis and change proposals.

> **Infrastructure Knowledge → Context → Agent → Code → Infrastructure**

The goal is not to make an agent better at typing Terraform. The goal is to give the agent enough structured context to understand **why** an infrastructure change is appropriate, what constraints apply, and what evidence should be verified before proposing code.

## What this repository provides

- **Incident analysis Skill** — analyze symptoms using architecture, incident history, runbooks, and policy before proposing remediation.
- **Terraform review Skill** — review IaC against service criticality, architecture decisions, production policy, and maintainability standards.
- **Architecture review Skill** — compare a proposed design with existing architecture principles and ADRs.
- **Production guard Hook** — blocks common destructive infrastructure commands and requires an explicit human workflow instead.
- **Example `.infra-context/`** — a portable structure for service catalog, architecture, ADRs, incidents, and policies.
- **Eval fixture** — a small machine-readable incident case showing how agent conclusions can be checked.

This repository intentionally keeps organization-specific knowledge **outside the plugin**. The plugin defines *how to reason*. Each project owns the knowledge the agent reasons over in `.infra-context/`.

## Architecture

```text
Infrastructure Knowledge
        │
        ├── Service catalog
        ├── Architecture
        ├── ADRs
        ├── Incident history
        └── Policies / runbooks
        │
        ▼
  .infra-context/
        │
        ▼
Claude Code Skills
        │
        ├── incident-analysis
        ├── terraform-review
        └── architecture-review
        │
        ▼
 Evidence + judgment
        │
        ▼
 Change proposal / Terraform
        │
        ▼
    Human review
        │
        ▼
 Infrastructure
```

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
```

### 2. Copy the example context into a project

```bash
cp -R examples/.infra-context /path/to/your-project/.infra-context
```

Replace the sample content with your own sanitized architecture knowledge.

### 3. Test the plugin locally

From the parent directory of this repository:

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

Claude Code discovers the plugin manifest, Skills, agent, and hooks automatically. Official Claude Code documentation recommends `--plugin-dir` for local plugin testing.

### 4. Try the Skills

```text
/infra-harness:incident-analysis API latency increased. Diagnose it before recommending any production change.

/infra-harness:terraform-review Review the current Terraform changes for reliability, security, and maintainability risks.

/infra-harness:architecture-review Review this proposed runtime migration against our current architecture context and ADRs.
```

Skills are also model-invoked when their descriptions match the task.

## Context contract

A project using the harness should keep infrastructure knowledge under:

```text
.infra-context/
├── service-catalog.yaml
├── architecture/
│   └── <service>.md
├── adr/
│   └── ADR-<n>-<decision>.md
├── incidents/
│   └── INC-<n>-<incident>.md
├── policies/
│   └── production.md
└── runbooks/
    └── <scenario>.md
```

The Skills use **progressive context loading**. They should not read every document up front. They start with the service catalog, then load only architecture, incident, policy, runbook, or ADR files relevant to the task.

## Why Knowledge and Context are separate

Human knowledge might be:

> "We previously had a production database latency incident caused by CPU credit exhaustion on a burstable instance."

Agent-ready context turns that into durable, searchable evidence:

```yaml
service: orders-api
criticality: high
known_incidents:
  - type: cpu-credit-exhaustion
    component: aurora-primary
policy:
  production_burstable_instances: avoid
```

The value is not the YAML itself. The value is that a future agent can combine **current evidence + architecture + historical decisions + policy** before proposing a change.

## Guardrails

The bundled `PreToolUse` hook blocks common destructive commands such as:

- `terraform apply`
- `terraform destroy`
- `aws ... delete-*`
- destructive `kubectl delete`
- obvious recursive filesystem deletion

The guard is intentionally conservative and is **not a security boundary**. Production controls still belong in IAM, CI/CD approvals, protected branches, policy-as-code, and cloud-native authorization.

## Evaluation

`evals/incident/aurora-saturation.json` contains a minimal incident fixture with expected conclusions and prohibited recommendations.

The repository also includes a small standard-library-only checker:

```bash
python scripts/check_eval_output.py \
  evals/incident/aurora-saturation.json \
  examples/eval-output/aurora-saturation-output.json
```

This is intentionally simple. It demonstrates the contract: an infrastructure agent should be evaluated on **judgment**, not merely whether it generated valid code.

## Design principles

1. **Evidence before action** — do not recommend production changes before establishing evidence.
2. **Progressive disclosure** — load only context required for the current decision.
3. **Decisions are first-class data** — ADRs and incident history should influence future recommendations.
4. **Human approval for production** — the agent proposes; production control remains explicit.
5. **Structured where useful, narrative where necessary** — service metadata benefits from YAML; architecture reasoning often belongs in Markdown.
6. **Context stays with the project** — reusable reasoning lives in the plugin, organization knowledge lives with the infrastructure repository.

## Current scope

This is a minimal, usable foundation rather than a full autonomous infrastructure platform. It does **not** bundle live AWS, Datadog, or GitHub credentials or MCP servers. Those integrations should be added by adopters according to their own access model.

Possible next steps include provider-neutral schemas, richer eval runners, MCP integration examples, policy-as-code adapters, and additional Skills for cost review and change-risk analysis.

## Compatibility

The repository follows the current Claude Code plugin layout:

```text
.claude-plugin/plugin.json
skills/<name>/SKILL.md
agents/
hooks/hooks.json
```

References:

- Claude Code Plugins: https://code.claude.com/docs/en/plugins
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Agent Skills specification: https://agentskills.io/

## License

MIT
