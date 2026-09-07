# Samsung AgentCore AIOps Patterns

Samsung Account SRE's Amazon Bedrock AgentCore AIOps case study is a **production-scale AIOps operating-model reference**, not a requirement to turn this project into a multi-agent system.

Primary references:

- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-1/
- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-2/

## What we adopt

### 1. Trace/span observability

A production Agent should make a request reconstructable across model, tool, backend, verification, and optional delegate work.

```text
trace
├─ agent span
├─ model span
├─ tool span
├─ backend span
├─ verification span
└─ optional delegate span
```

The provider-neutral reference is `runtime/observability.py`. It deliberately does not depend on AgentCore or OpenTelemetry; exporters may map the contract later.

### 2. Many channels, one turn path

Slack, Web, CLI, GitHub, MCP, or API should not each implement their own memory, guard, routing, and approval semantics.

```text
CLI ─────┐
Web ─────┤
Slack ───┤
GitHub ──┤
MCP ─────┤
         ↓
normalized TurnRequest
         ↓
Infrastructure Agent Turn Runtime
```

`runtime/channel.py` defines the normalized ingress contract. Authentication/authorization is host-owned and happens before normalization. Channel metadata never expands authority.

### 3. Task-specific evaluation

Evaluation should reflect the task being performed rather than forcing one universal score across all infrastructure work.

`evals/task-profiles.yaml` defines initial profiles for incident, change, FinOps, and delivery work. These profiles select metrics and weights; they do not replace Skill Lift, Context Lift, Harness Lift, Domain Eval, or Loop Eval.

### 4. Optional specialist delegation

Samsung's environment found value in hierarchical specialist agents at large organizational/tool scale. This project retains **Single Agent by default**.

Delegation becomes available only as an optional scaling mechanism when evaluation demonstrates that a narrower specialist improves outcomes enough to justify handoff/context cost.

```text
Infrastructure Engineering Agent
              ↓
     optional specialist
              ↓
        read-only analysis
```

`runtime/delegation.py` enforces two invariants:

- delegated capabilities/resource scope cannot exceed the parent;
- delegate output cannot make newly named resources mutation-eligible.

No Orchestrator → Supervisor → Sub-agent hierarchy is required by the base architecture.

### 5. Semantic learning stops at Learning Candidate

Operational conversations may reveal repeated procedures, corrections, or useful patterns. Automatic extraction can propose them, but repetition does not make them organizational truth.

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

`runtime/learning.py` materializes this boundary through the existing Knowledge Candidate contract.

## What we do not copy

### Mandatory three-level multi-agent hierarchy

Samsung operates at a scale where domain/tool growth justified hierarchical agent specialization. This project starts with one Infrastructure Engineering Agent and progressively filtered capabilities/Skills.

Rule:

> **Single Agent by default; specialize only when measured complexity earns it.**

### Automatic operational-rule promotion from memory

A repeated statement, correction, or pattern remains provisional until independently supported and governed. Persistent Memory is not a Policy or Verified Fact store.

### AgentCore-specific runtime dependency

AgentCore Runtime, Observability, Evaluation, Memory, Identity, and Guardrails are useful product references, but the core remains provider-neutral. AWS-specific integrations belong in provider/runtime adapters.

## Autonomy mapping

Samsung's staged Level 1 → Level 2 autonomy strongly aligns with the local authority model:

```text
Level 1
read / analyze / propose

Level 2
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

The local runtime intentionally keeps production write authority outside model prose.

## Relationship to Commerce Agents

The two references answer different scaling questions:

- **Commerce Agents:** start with a capable single Agent, progressive Skills/tools, backend-owned credentials, and runtime-enforced safety.
- **Samsung AgentCore AIOps:** when an AIOps platform grows across teams/domains/channels, add strong observability/evaluation and specialize only where scale demands it.

Local synthesis:

```text
Single Infrastructure Engineering Agent
              ↓
filtered Skills / Capabilities / Tools
              ↓
shared Runtime / Harness boundary
              ↓
trace + task-specific evaluation
              ↓
optional constrained delegates only when earned
```
