# Samsung AgentCore AIOps Patterns

Samsung Account SRE's Amazon Bedrock AgentCore AIOps case study is a **production-scale AIOps operating-model reference**, not a requirement to turn this project into a multi-agent system.

Primary references:

- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-1/
- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-2/

## Key distinction: Orchestrator Runtime vs Orchestrator Agent

This project now has an explicit **Agent Orchestrator / Turn Runtime**. It is not an LLM router Agent.

```text
User / Channel
      ↓
Deterministic Agent Orchestrator
      ↓
Single Infrastructure Engineering Agent
      ↓
optional constrained specialist only when earned
```

The Orchestrator owns turn flow, context/surface assembly, model/tool iteration, budgets, telemetry correlation, and completion transition. It does not own engineering truth or production authorization.

Samsung's Orchestrator → Supervisor → Sub-agent hierarchy remains a **scale-out option**, not the base architecture.

## What we adopt

### 1. Trace/span observability

A production Agent should make a request reconstructable across model, tool, backend, verification, and optional delegate work.

```text
Runtime Event Log
      ↓
trace
├─ agent span
├─ model span
├─ tool span
├─ backend span
├─ verification span
└─ optional delegate span
```

`runtime/observability.py` is provider-neutral. Span lifecycle can be committed to the same Runtime Event Log so AgentCore/OpenTelemetry exporters do not become competing execution truth stores.

### 2. Many channels, one turn path

```text
CLI ─────┐
Web ─────┤
Slack ───┤
GitHub ──┤
MCP ─────┤
         ↓
normalized TurnRequest
         ↓
Agent Orchestrator / Turn Runtime
```

`runtime/channel.py` defines normalized ingress. Authentication/authorization happens before normalization. Channel metadata never expands authority.

### 3. Task-specific evaluation

`evals/task-profiles.yaml` defines initial incident, change, FinOps, and delivery profiles. These select outcome metrics/weights and complement Artifact Lift, Runtime invariant, and Loop/regression evaluation rather than creating a second universal scoring system.

### 4. Optional specialist delegation

Single Agent remains the default.

Delegation becomes available only when measured complexity shows that a narrower specialist improves outcomes enough to justify handoff/context cost.

`runtime/delegation.py` enforces:

- delegate capability/resource scope cannot exceed the parent;
- delegation is read-only by default;
- delegate output cannot make newly named resources mutation-eligible.

### 5. Semantic learning stops at Learning Candidate

```text
conversation / run pattern
          ↓
semantic extraction
          ↓
Learning Candidate
          ↓
evidence + review + governance
          ↓
Durable Knowledge only if promoted
```

`runtime/learning.py` materializes this boundary. Repetition does not create Policy, Runbook truth, ADRs, Service Catalog truth, or Verified Facts.

## What we do not copy

### Mandatory three-level multi-agent hierarchy

Rule:

> **Single Agent by default; specialize only when measured complexity earns it.**

### Automatic operational-rule promotion from memory

Persistent Memory remains contextual state. Any durable operational learning must pass the existing epistemic and governance path.

### AgentCore-specific core dependency

AgentCore Runtime, Observability, Evaluation, Memory, Identity, and Guardrails are useful product references. AWS-specific implementations belong in provider/runtime adapters; the core remains provider-neutral.

## Autonomy mapping

Samsung's staged autonomy aligns with the local authority model:

```text
read / analyze / propose
        ↓
stage exact change
        ↓
independent approval
        ↓
apply-time revalidation
        ↓
execute
        ↓
independent verification
```

The reference Orchestrator is read-only and therefore cannot bypass this governed change path.

## Relationship to Commerce Agents

- **Commerce Agents** answers how to start with one capable Agent, a standard model/tool loop, progressive Skills/tools, backend-owned credentials, and runtime-enforced safety.
- **Samsung AgentCore AIOps** shows the production pressures that appear across teams, domains, tools, and channels: observability, task-specific evaluation, shared runtime modules, staged autonomy, and optional specialization.

Local synthesis:

```text
Agent Orchestrator / Turn Runtime
              ↓
Single Infrastructure Engineering Agent
              ↓
Context / Skills / Tools
              ↓
Harness / Control Plane
              ↓
trace + task-specific evaluation
              ↓
optional constrained delegates only when earned
```
