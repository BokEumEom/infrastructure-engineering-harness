# Reference Models

The **Infrastructure Engineering Agent** uses external projects and engineering frameworks as design references. References are not automatically Runtime dependencies, authorities, or model-visible Skills.

> **Reference widely, expose narrowly.**

A reference should influence only the layer where it contributes a distinct mechanism.

## Reference tiers

### Primary structural references

| Layer | Primary reference | Local use |
| --- | --- | --- |
| **Agent product / turn runtime** | Anthropic Commerce Agents | one capable Agent, standard model/tool loop, Skills/tools, backend-owned credentials, staged writes, runtime safety |
| **Context engineering** | Anthropic Context Engineering | unhobbling, minimal always-loaded context, progressive disclosure, measured context lift |
| **Production AIOps scale-out** | Samsung Account AgentCore AIOps | trace/span observability, channel convergence, task-specific evaluation, staged autonomy, specialization only when scale earns it |
| **Reconciliation** | Kubernetes Controllers + LongHorizon-Harness | desired/actual state, explicit external task state, independent verification, optional repeated reconciliation |
| **Artifact/effect evaluation** | NVIDIA ACES / SkillEvaluator | paired treatment evaluation, trajectory/outcome scoring, reproducible artifact evaluation |

These references shape the top-level architecture directly.

### Supporting references

| Area | References | Local role |
| --- | --- | --- |
| **Runtime event/extensibility** | DeepSeek Harness | append-only/reconstructable runtime events, dynamic surfaces, persistence/recovery seams; not the authority model for the whole control plane |
| **Memory taxonomy** | GBrain | bounded retrieval, memory vs durable knowledge separation |
| **Context evolution** | Backpass | transcript-driven context proposals without indefinite AGENTS/context growth |
| **Artifact quality** | Paperthin | clean-current-state rewrites, SSOT repair, no-op restraint, independent eval/leakage reflexes |
| **Long-running eval** | LoopsBench | dependency-aware long-running evaluation and regression obligations |
| **Supporting standards** | MCP, OpenGitOps | provider-neutral tool boundary and declarative/versioned desired-state patterns |

### Engineering domain references

- **Google SRE** — SLI/SLO, error budgets, incident/reliability semantics;
- **DORA** — software delivery performance and stability;
- **FinOps Framework** — cost allocation, optimization, realized technology value.

These define engineering semantics, not Agent Runtime architecture.

---

## 1. Anthropic Commerce Agents

Commerce Agents remains the primary reference for the **Agent-as-product** direction:

```text
User
 ↓
Single capable Agent
 ↓
Model judgment
 ├─ minimal context
 ├─ progressive Skills
 ├─ Tools
 └─ Memory
 ↓
shared runtime enforcement
 ↓
Backend contract
 ↓
Existing systems
```

Local adoption includes backend-owned credentials, provenance-bound mutation targets, stage → approve → apply, apply-time revalidation, fencing, capability-aware surfaces, progressive Skill loading, external memory, cache-aware context layout, and recording.

The repository does not depend on Commerce Agents as a package. Commerce-specific abstractions and Anthropic-only request shapes stay outside the provider-neutral core.

References:
- https://claude.com/blog/the-anatomy-of-effective-commerce-agents
- https://github.com/anthropics/commerce-agents
- local mapping: `docs/COMMERCE-AGENT-PATTERNS.md`

## 2. Anthropic Context Engineering

Used to keep always-loaded guidance small, move hard invariants into code/policy/schema, progressively disclose task guidance, and remove constraints that no longer improve outcomes.

Reference:
- https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
- local design: `docs/HARNESS-UNHOBBLING.md`

## 3. Samsung Account AgentCore AIOps

Primary reference for production-scale AIOps concerns:

- one processing path across channels;
- trace/span observability;
- task-specific evaluation;
- staged autonomy;
- shared runtime modules;
- specialist delegation only when domain/tool/organization scale justifies its cost.

The project deliberately does **not** require an Orchestrator → Supervisor → Sub-agent hierarchy.

Local rule:

> **Single Agent by default; specialize only when measured complexity earns it.**

References:
- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-1/
- https://aws.amazon.com/ko/blogs/tech/agentcore-aiops-samsung-2/
- local mapping: `docs/AWS-AGENTCORE-AIOPS-PATTERNS.md`

## 4. Kubernetes Controllers + LongHorizon-Harness

Kubernetes Controllers provide the durable desired-state/actual-state reconciliation model. LongHorizon-Harness reinforces keeping task state outside model prose and updating it from independently supported facts.

These references justify **optional Engineering Loops**, not a mandatory Loop on every request.

References:
- https://kubernetes.io/docs/concepts/architecture/controller/
- https://arxiv.org/abs/2608.01964

OpenGitOps remains a supporting standard for declarative/versioned desired state:
- https://opengitops.dev/

## 5. NVIDIA ACES / SkillEvaluator

Primary reference for evaluating Skills and other Agent artifacts as executable treatments rather than reviewing text alone.

Local adaptation keeps task/model/workspace/tools/scoring fixed and compares baseline vs treatment as Skill Lift, Context Lift, or Harness Lift. Fixture runs validate plumbing; live runs are required for live-effectiveness claims.

References:
- https://arxiv.org/abs/2608.20614
- https://github.com/NVIDIA/SkillEvaluator

## 6. DeepSeek Harness

DeepSeek Harness remains valuable for **event/runtime extensibility patterns**:

- append-only/reconstructable runtime history;
- dynamic context/tool surfaces;
- lazy Skills;
- persistence/recovery seams;
- stale revision checks.

It is not the primary authority model for this project's Harness because local Evidence provenance, independent authorization, approval, source-of-truth protection, and independent verification are intentionally non-swappable invariants.

Reference:
- https://github.com/deepseek-ai/deepseek-harness

## 7. GBrain and Backpass

### GBrain

Used for bounded retrieval and separating contextual memory from durable organizational knowledge. Local storage classes remain distinct internally, while the model-facing facade is one bounded Context surface.

Reference:
- https://github.com/garrytan/gbrain

### Backpass

Used for transcript-driven context improvement. Context changes remain proposals, are reviewed, and should earn their place through Context Lift.

References:
- https://blog.kunchenguid.com/p/your-agentsmd-is-a-neural-net
- https://github.com/kunchenguid/backpass

## 8. Paperthin

Paperthin remains an artifact-quality and eval-integrity reference, **not a Runtime Skill dependency**.

Its useful principles are already absorbed locally:

```text
re0 / cleanup      → artifact-hygiene
ssotize            → ssot-review
mandela            → eval-integrity
cycle learning     → loop-engineering + Knowledge Candidate
```

Reference:
- https://github.com/LilMGenius/paperthin

## 9. LoopsBench

Used specifically as a long-running evaluation reference for dependency-aware tasks and regression obligations, rather than as a second Loop architecture.

Reference:
- https://arxiv.org/abs/2608.00267

## 10. MCP and authority boundary

MCP is a provider-neutral boundary for evidence retrieval and governed workflow actions. Tool availability is not production authorization.

Reference:
- https://modelcontextprotocol.io/

Production-impacting, destructive, privilege-expanding, and financial actions require authority outside model prose. That rule is a local project invariant.

---

## Adoption rule

Before adding a reference, answer:

1. Which architectural layer does it improve?
2. Is that role already covered by a stronger reference or local contract?
3. Does it add a distinct mechanism or only new terminology?
4. Should it remain design provenance, become a Runtime reference, or justify a governed local implementation?

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
expose to Runtime only when it earns surface area
```

The canonical synthesized architecture lives in `docs/ARCHITECTURE.md` rather than in any single external reference.
