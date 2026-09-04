# Reference Models

The **Infrastructure Engineering Agent** uses external projects and established engineering frameworks as design references. References are not automatically Runtime dependencies, authorities, or model-visible Skills.

The important question is not "how many projects do we reference?" but **which layer each reference is allowed to influence**.

## Reference roles

| Layer | Primary references | What they contribute |
| --- | --- | --- |
| **Agent product / application runtime** | Anthropic Commerce Agents | single-agent product architecture, backend contracts, provenance-bound writes, staged changes, capability-aware surfaces, memory/runtime patterns, prompt-performance patterns |
| **Harness / execution runtime** | DeepSeek Harness | append-only model-visible state, guarded tool pipeline, scoped Skill loading, fail-closed approval, persistence/recovery seams |
| **Context / memory** | Anthropic Context Engineering, GBrain, Backpass | unhobbling, progressive disclosure, bounded retrieval, persistent contextual state, transcript-driven context improvement |
| **Artifact / reflex quality** | Paperthin | clean-current-state rewrites, SSOT repair, restraint, independent lenses, eval-leakage reflexes |
| **Evaluation** | NVIDIA ACES / SkillEvaluator, Paperthin Mandela principles | paired lift evaluation, trajectory grading, negative controls, independent ground-truth checks |
| **Long-running reconciliation** | Kubernetes Controllers, OpenGitOps, LongHorizon-Harness, LoopsBench, IBM Loop Engineering | desired/actual state reconciliation, external task state, terminal conditions, regression obligations |
| **Engineering domain truth** | Google SRE, DORA, FinOps Framework | reliability, delivery, and cost/value engineering models |
| **Tool boundary** | MCP | provider-neutral evidence/workflow action interface |
| **Authority boundary** | Independent authorization | irreversible, destructive, financial, privilege, or production-impacting actions require authority outside model prose |

This classification prevents multiple references that solve adjacent problems from becoming duplicate Runtime surfaces.

---

## 1. Agent product / application runtime

### Anthropic Commerce Agents

`anthropics/commerce-agents` is the primary reference for the **Agent-as-product** direction.

Reusable architecture:

```text
User
 ↓
Single domain Agent
 ↓
Model judgment
 ├─ minimal prompt/context
 ├─ progressively loaded Skills
 ├─ Tools
 └─ Memory
 ↓
Runtime enforcement
 ↓
Backend contract
 ↓
Existing domain systems
```

Infrastructure translation:

```text
Infrastructure Engineering Agent
          ↓
Model Judgment
          ↓
Skill / Tool / Capability
          ↓
Internal Runtime / Harness
          ↓
Infrastructure Backend
          ↓
Provider Systems
```

Patterns adopted locally include:

- backend-owned credentials;
- provenance-bound mutation targets;
- stage → approve → apply separation;
- apply-time revalidation;
- untrusted-content fencing;
- capability-aware tool/Skill surfaces;
- progressive Skill loading;
- external persistent memory;
- stable-prefix prompt assembly and latency/cache telemetry;
- deterministic execution recording/replay integrity.

The repository does **not** depend on Commerce Agents as a package. Commerce-specific concepts, Anthropic-only request shapes, presentation components, and merchant/shopping abstractions stay outside the provider-neutral core.

Provider-specific optimizations may reproduce the relevant mechanism in a provider adapter rather than leaking it into the core Runtime.

References:
- https://claude.com/blog/the-anatomy-of-effective-commerce-agents
- https://github.com/anthropics/commerce-agents
- local mapping: `docs/COMMERCE-AGENT-PATTERNS.md`

---

## 2. Harness / execution runtime

### DeepSeek Harness

DeepSeek Harness is a Runtime Kernel reference rather than an Infrastructure Engineering semantics reference.

Reusable ideas:

- append-only Session/Event Log as runtime truth;
- every model-visible input/tool result reconstructable from logged state;
- dynamically assembled context/tool surfaces;
- lazily loaded Skills;
- pre-policy → monotonic guard → approval → execution → normalized result pipeline;
- audited fail-closed approval;
- explicit sandbox enforcement state;
- persistent/recoverable session state;
- revision checks against stale mutations.

Infrastructure-specific boundaries remain stricter locally: Runtime Events are not automatically Engineering Evidence, and availability of a runtime/tool never grants production authority.

Reference:
- https://github.com/deepseek-ai/deepseek-harness

---

## 3. Context and memory

### Anthropic Context Engineering / Unhobbling

Anthropic's Claude 5 context-engineering guidance is the main reference for reducing accumulated prompt constraints as model capability improves.

Local consequences:

- keep always-loaded Agent guidance small;
- prefer interfaces/contracts over reasoning recipes;
- progressively disclose Skills/context;
- remove rules already enforced by Runtime/schema/policy;
- use Harness Lift instead of assuming more context is better.

Reference:
- https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
- local design: `docs/HARNESS-UNHOBBLING.md`

### GBrain

GBrain is a reference for bounded context retrieval, persistent memory, explicit gaps, and hot/cold knowledge separation.

Infrastructure adaptation deliberately separates:

```text
User / Session Memory
Organizational Knowledge
Evolution Knowledge
Engineering Evidence
```

A stored memory item does not become a Verified Fact simply because it persists.

Reference:
- https://github.com/garrytan/gbrain

### Backpass / Kun Chen

Backpass treats project-level agent context as a bounded behavior surface that should improve from actual execution traces rather than grow indefinitely.

Local adaptation:

- transcript evidence may propose AGENTS/context changes;
- narrow rules should move into Skills;
- context changes are human-reviewed;
- paired Context Lift must justify claims of improvement;
- Durable Organizational Knowledge is protected from automatic prompt-learning writeback.

References:
- https://blog.kunchenguid.com/p/your-agentsmd-is-a-neural-net
- https://github.com/kunchenguid/backpass

---

## 4. Artifact and reflex quality

### Paperthin

Paperthin remains a valid and important reference, but **not a Runtime Skill dependency**.

Its durable contribution is restraint:

- rewrite drifted artifacts into a clean current state instead of layering patches;
- consolidate duplicated truth into one canonical home;
- allow a no-op when nothing improves;
- preserve lessons/negative learning without preserving accidental architecture;
- inspect evals for circularity and leakage;
- preserve disagreement across independent lenses instead of averaging it away.

These principles are already absorbed into locally governed Skills/contracts:

```text
Paperthin re0       → skills/artifact-hygiene
Paperthin ssotize   → skills/ssot-review
Paperthin mandela   → skills/eval-integrity
Paperthin cycle     → skills/loop-engineering + knowledge-candidate contracts
Paperthin prism     → independent cross-domain review principle
```

Therefore `paperthin-*` entries are intentionally **not** exposed through `capabilities/registry.yaml`. Exposing both original reference Skills and local adaptations created duplicate intent and unnecessary model choice.

Paperthin remains design provenance and a source for future pattern review. If a new Paperthin pattern is useful, adapt it into a local governed contract only when it adds measured value instead of exposing the upstream Skill directly.

Reference:
- https://github.com/LilMGenius/paperthin

---

## 5. Evaluation

### NVIDIA ACES / SkillEvaluator

ACES is the main reference for evaluating a Skill as an executable artifact rather than reviewing only its text.

Local adaptation holds task/model/workspace/tools/scoring constant and compares baseline vs treatment as **Skill Lift**. Fixture runs validate evaluator plumbing; only live runs may support live-effectiveness claims.

Reference:
- https://arxiv.org/abs/2608.20614
- https://github.com/NVIDIA/SkillEvaluator

### Paperthin Mandela principles

Paperthin's eval-leakage patterns remain useful as an **independence audit**, even though the upstream Skill is not exposed to Runtime.

The locally governed `eval-integrity` Skill checks:

- independent ground truth;
- scorer/designer separation;
- variable isolation;
- control leakage;
- fixture/live distinction;
- negative controls;
- trajectory evidence when behavior is part of the claim.

This complements rather than duplicates ACES: ACES supplies the paired experiment shape; eval-integrity asks whether the experiment can independently falsify its own claim.

---

## 6. Long-running reconciliation

### Kubernetes Controllers + OpenGitOps

Controllers provide the durable desired-state/actual-state reconciliation model. OpenGitOps reinforces declarative/versioned desired state and continuous reconciliation.

References:
- https://kubernetes.io/docs/concepts/architecture/controller/
- https://opengitops.dev/

### LongHorizon-Harness

LongHorizon-Harness motivates explicit task state outside an ever-growing model context and separation of manage/execute/audit concerns.

Reference:
- https://arxiv.org/abs/2608.01964

### LoopsBench

LoopsBench motivates dependency-aware long-running evaluation and retaining completed work as regression obligations.

Reference:
- https://arxiv.org/abs/2608.00267

### IBM Loop Engineering

IBM's Loop Engineering framing contributes Goal → Action → Observation → Adjustment cycles with verifiable stopping criteria.

Reference:
- https://www.ibm.com/think/topics/loop-engineering

Engineering Loops remain optional: ordinary one-shot Agent work does not enter a Loop merely because a Loop definition exists.

---

## 7. Engineering domain truth

### Google SRE

Used for SLI/SLO, error budgets, incident response, reliability policy, and escalation/learning models.

References:
- https://sre.google/sre-book/service-level-objectives/
- https://sre.google/workbook/error-budget-policy/

### DORA

Used for delivery performance baselines, dominant-constraint improvement, and validating progress without sacrificing stability.

Reference:
- https://dora.dev/guides/dora-metrics/

### FinOps Framework

Used for iterative Inform → Optimize → Operate and measured realized technology value rather than expected savings alone.

References:
- https://www.finops.org/framework/
- https://www.finops.org/framework/phases/

These references define domain semantics; they do not become Agent Runtime architecture.

---

## 8. Tool and authority boundaries

### MCP

MCP is used as a provider-neutral boundary for evidence retrieval and governed workflow actions. Tool availability is not production authorization.

Reference:
- https://modelcontextprotocol.io/

### Independent authorization

Irreversible, destructive, privilege-expanding, financial, and production-impacting actions require authorization outside model prose. This is a project invariant rather than an external package dependency.

---

## Adoption rule

A new external reference should answer all four questions before being added:

1. **Which layer does it improve?**
2. **Is that role already covered by a stronger reference/local contract?**
3. **Does it introduce a new mechanism or merely duplicate terminology?**
4. **Should it be design provenance, a Runtime reference source, or an actual managed local implementation?**

Default decision:

```text
Useful external idea
       ↓
Reference Model
       ↓
local adaptation only if needed
       ↓
evaluate lift / integrity
       ↓
expose to Runtime only when it earns the surface area
```

## Synthesis

```text
Desired Outcome
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
Independently Authorized Execution when required
                ↓
Independent Verification
                ↓
Reconcile only when the task needs a Loop
                ↓
Verified Outcome
                ↓
Learning Candidate → Governance → Durable Knowledge
```
