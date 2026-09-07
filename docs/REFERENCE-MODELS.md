# Reference Models

The **Infrastructure Engineering Agent** uses external projects and established engineering frameworks as design references. References are not automatically Runtime dependencies, authorities, or model-visible Skills.

The governing principle is:

> **Reference widely, expose narrowly.**

A reference should influence only the layer where it adds a distinct mechanism.

## Reference roles

| Layer | Primary references | What they contribute |
| --- | --- | --- |
| **Agent product / application runtime** | Anthropic Commerce Agents | single-agent product architecture, backend contracts, provenance-bound writes, staged changes, capability-aware surfaces, memory/runtime and prompt-performance patterns |
| **Production AIOps scale-out** | Samsung Account AgentCore AIOps | trace/span observability, channel convergence, task-specific evaluation, staged autonomy, optional hierarchical specialization when scale earns it |
| **Harness / execution runtime** | DeepSeek Harness | append-only model-visible state, guarded tool pipeline, scoped Skill loading, fail-closed approval, persistence/recovery seams |
| **Context / memory** | Anthropic Context Engineering, GBrain, Backpass | unhobbling, progressive disclosure, bounded retrieval, persistent contextual state, transcript-driven context improvement |
| **Artifact / reflex quality** | Paperthin | clean-current-state rewrites, SSOT repair, restraint, independent lenses, eval-leakage reflexes |
| **Evaluation** | NVIDIA ACES / SkillEvaluator, Paperthin principles | paired lift evaluation, trajectory grading, negative controls, independent ground-truth checks |
| **Long-running reconciliation** | Kubernetes Controllers, OpenGitOps, LongHorizon-Harness, LoopsBench, IBM Loop Engineering | desired/actual state reconciliation, external task state, terminal conditions, regression obligations |
| **Engineering domain truth** | Google SRE, DORA, FinOps Framework | reliability, delivery, and cost/value engineering models |
| **Tool / authority boundary** | MCP, independent authorization | provider-neutral actions plus authority outside model prose |

This classification prevents adjacent references from becoming duplicate Runtime surfaces.

---

## 1. Agent product / application runtime

### Anthropic Commerce Agents

Commerce Agents is the primary reference for the **Agent-as-product** direction:

```text
User
 ↓
Single domain Agent
 ↓
Model judgment
 ├─ minimal context
 ├─ progressive Skills
 ├─ Tools
 └─ Memory
 ↓
Runtime enforcement
 ↓
Backend contract
 ↓
Existing domain systems
```

Patterns adopted locally include backend-owned credentials, provenance-bound mutation targets, stage → approve → apply, apply-time revalidation, fencing, capability-aware surfaces, progressive Skill loading, external memory, cache-aware context layout, and deterministic recording.

The repository does not depend on Commerce Agents as a package. Commerce-specific abstractions and Anthropic-only request shapes stay outside the provider-neutral core.

References:
- https://claude.com/blog/the-anatomy-of-effective-commerce-agents
- https://github.com/anthropics/commerce-agents
- local mapping: `docs/COMMERCE-AGENT-PATTERNS.md`

---

## 2. Production AIOps scale-out

### Samsung Account AgentCore AIOps

Samsung Account SRE's AgentCore AIOps case study is the primary reference for **what changes when an AIOps platform grows across many tools, domains, teams, and channels**.

Its reusable production patterns are:

- trace/span observability across agent, model, tool, backend, and verification work;
- Slack/Web and other channels converging on one processing path;
- task-specific evaluation rather than one universal scorer;
- staged autonomy: read/analyze first, independently approved execution later;
- shared runtime modules/registries instead of each agent reimplementing infrastructure;
- specialist agents only when domain/tool scale makes specialization worthwhile.

The local project deliberately does **not** adopt a mandatory Orchestrator → Supervisor → Sub-agent hierarchy.

Local rule:

> **Single Agent by default; specialize only when measured complexity earns it.**

Optional delegation is read-only, cannot expand capability/resource authority, and cannot make newly named resources mutation-eligible.

Semantic memory extraction may produce a `Learning Candidate`, but repeated conversation patterns are not promoted directly to policy, runbook truth, or Verified Facts.

References:
- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-1/
- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-2/
- local mapping: `docs/AWS-AGENTCORE-AIOPS-PATTERNS.md`

---

## 3. Harness / execution runtime

### DeepSeek Harness

DeepSeek Harness is a Runtime Kernel reference rather than an Infrastructure Engineering semantics reference.

Reusable ideas include append-only Session/Event Log, reconstructable model-visible state, dynamically assembled tool/context surfaces, lazy Skills, guarded execution, fail-closed approval, sandbox state, persistence/recovery, and stale revision checks.

Infrastructure-specific boundaries remain stricter locally: Runtime Events are not automatically Engineering Evidence, and tool availability never grants production authority.

Reference:
- https://github.com/deepseek-ai/deepseek-harness

---

## 4. Context and memory

### Anthropic Context Engineering / Unhobbling

Used to keep always-loaded guidance small, prefer interfaces over reasoning recipes, progressively disclose Skills/context, and remove prompt rules already enforced by Runtime/schema/policy.

Reference:
- https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
- local design: `docs/HARNESS-UNHOBBLING.md`

### GBrain

Used for bounded retrieval, persistent contextual state, explicit gaps, and hot/cold knowledge separation.

Local adaptation keeps four classes separate:

```text
User / Session Memory
Organizational Knowledge
Evolution Knowledge
Engineering Evidence
```

Persistence does not make a memory item a Verified Fact.

Reference:
- https://github.com/garrytan/gbrain

### Backpass / Kun Chen

Used for transcript-driven context improvement without indefinitely growing AGENTS/context. Context changes remain reviewable and should demonstrate Context Lift.

References:
- https://blog.kunchenguid.com/p/your-agentsmd-is-a-neural-net
- https://github.com/kunchenguid/backpass

---

## 5. Artifact and reflex quality

### Paperthin

Paperthin remains a design-quality reference, **not a Runtime Skill dependency**.

Useful principles are clean-current-state rewrites, SSOT consolidation, no-op restraint, preservation of earned lessons without accidental architecture, and independent eval/leakage checks.

These are absorbed into local governed implementations:

```text
re0 / cleanup      → artifact-hygiene
ssotize            → ssot-review
mandela            → eval-integrity
cycle learning     → loop-engineering + Knowledge Candidate
```

Reference:
- https://github.com/LilMGenius/paperthin

---

## 6. Evaluation

### NVIDIA ACES / SkillEvaluator

Primary reference for paired evaluation of Skills as executable artifacts. Local adaptation keeps task/model/workspace/tools/scoring fixed and compares baseline vs treatment as Skill Lift.

Reference:
- https://arxiv.org/abs/2608.20614
- https://github.com/NVIDIA/SkillEvaluator

### Task-specific AIOps evaluation

Samsung's AIOps case reinforces that an incident, production change, delivery task, and FinOps analysis should not share one undifferentiated score.

Local task profiles live in `evals/task-profiles.yaml` and complement, rather than replace, Skill Lift, Context Lift, Harness Lift, Domain Eval, and Loop Eval.

Paperthin-style eval-integrity checks remain responsible for scorer independence, leakage, negative controls, and fixture/live distinctions.

---

## 7. Long-running reconciliation

### Kubernetes Controllers + OpenGitOps

Used for desired-state/actual-state reconciliation and declarative/versioned desired state.

References:
- https://kubernetes.io/docs/concepts/architecture/controller/
- https://opengitops.dev/

### LongHorizon-Harness / LoopsBench / IBM Loop Engineering

Used for explicit task state outside model context, manage/execute/audit separation, dependency-aware long-running evaluation, regression obligations, and verifiable stopping criteria.

References:
- https://arxiv.org/abs/2608.01964
- https://arxiv.org/abs/2608.00267
- https://www.ibm.com/think/topics/loop-engineering

Engineering Loops remain optional; ordinary one-shot Agent work does not enter a Loop merely because a Loop exists.

---

## 8. Engineering domain truth

### Google SRE

Used for SLI/SLO, error budgets, incident response, reliability policy, and learning models.

References:
- https://sre.google/sre-book/service-level-objectives/
- https://sre.google/workbook/error-budget-policy/

### DORA

Used for delivery performance baselines and improvement without sacrificing stability.

Reference:
- https://dora.dev/guides/dora-metrics/

### FinOps Framework

Used for Inform → Optimize → Operate and realized technology value rather than expected savings alone.

References:
- https://www.finops.org/framework/
- https://www.finops.org/framework/phases/

---

## 9. Tool and authority boundaries

### MCP

MCP is a provider-neutral boundary for evidence retrieval and governed workflow actions. Tool availability is not production authorization.

Reference:
- https://modelcontextprotocol.io/

### Independent authorization

Irreversible, destructive, privilege-expanding, financial, and production-impacting actions require authorization outside model prose.

---

## Adoption rule

Before adding a new external reference, answer:

1. Which layer does it improve?
2. Is the role already covered by a stronger reference/local contract?
3. Does it introduce a new mechanism or merely duplicate terminology?
4. Should it be design provenance, Runtime reference, or local implementation?

Default path:

```text
Useful external idea
       ↓
Reference Model
       ↓
local adaptation only if distinct
       ↓
evaluate lift / integrity
       ↓
expose to Runtime only when it earns the surface area
```

## Synthesis

```text
User / Channel
      ↓
Normalized Turn Request
      ↓
Infrastructure Engineering Agent
      ↓
Minimal Context + Model Judgment
   ↙                         ↘
Skills / Capabilities       Pull Evidence / Context
   ↘                         ↙
          Proposed Action
                ↓
Runtime / Provenance / Permission / Approval Boundary
                ↓
Trace / Record / Evaluate
                ↓
Independently Authorized Execution when required
                ↓
Independent Verification
                ↓
Reconcile only when the task needs a Loop
                ↓
Verified Outcome
                ↓
Learning Candidate → Governance → Durable Knowledge

Optional specialist delegation exists only when measured scale justifies it.
```
