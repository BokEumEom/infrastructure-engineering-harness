# Reference Models

Infrastructure Engineering Harness combines mature infrastructure feedback models with emerging agent Loop Engineering rather than replacing established practice.

Loop Engineering is an **emerging agent engineering term**, not an infrastructure industry standard. The harness therefore uses it as an execution pattern while grounding safety and operations in established engineering models.

| Reference | Contribution |
| --- | --- |
| DeepSeek Harness | Plugin-composed runtime, append-only session events, model-visible/logged reconstructability, guarded tool pipeline, scoped Skill discovery, fail-closed approval, sandbox and persistence seams |
| NVIDIA ACES / SkillEvaluator | Paired live evaluation with and without a Skill, trajectory grading and Skill Lift |
| Kun Chen / backpass | Transcript-driven, budgeted, evidence-gated improvement of project-level agent memory |
| Paperthin | Artifact restraint, clean-current-state rewrites, SSOT repair, eval independence, earned reuse, and cross-lens disagreement |
| gstack | Workflow-composed Agent UX, progressive Skill routing, chained artifacts, review/test/ship/reflect sequencing, and cross-session learning surface |
| GBrain | Persistent agent memory, bounded context packs, explicit gaps, hot/cold knowledge separation, fact/opinion distinction, synthesis, and governed retrieval surfaces |
| Anthropic Context Engineering (Claude 5) | Unhobbling: remove redundant/prescriptive always-loaded guidance, prefer progressive disclosure, interfaces, and model judgment as capability improves |\n| Anthropic Commerce Agents | Agent-as-product architecture, backend integration contracts, runtime tool gates, provenance-bound writes, staged changes, host-owned approval, capability-aware tool/prompt surfaces, and live-recording/replay eval patterns |
| IBM Loop Engineering | Goal, action, observation and adjustment cycles with verifiable stopping criteria |
| LongHorizon-Harness | Explicit task state outside growing agent context; independently verified facts; manage/execute/audit separation |
| LoopsBench | Long-horizon dependency structure and completed work retained as regression obligations |
| Kubernetes Controllers | Desired-state vs actual-state control loops and reconciliation |
| OpenGitOps | Declarative/versioned desired state and continuous reconciliation |
| Google SRE | SLI/SLO, error budgets, reliability policy, escalation and learning |
| DORA | Service-level baseline, constraint improvement, progress validation and repetition |
| FinOps Framework | Iterative Inform → Optimize → Operate and measured technology value |
| MCP | Provider-neutral tool boundary for evidence and workflow actions |
| Independent authorization | Boundary for irreversible, destructive, financial, or production-impacting actions |

## DeepSeek Harness

DeepSeek Harness is a developer-preview general Agent Runtime built around a plugin-composed architecture. Its strongest reusable runtime ideas are different from this project's engineering-domain semantics:

- the append-only Session Event Log is the runtime source of truth;
- anything model-visible must be reconstructable from logged state;
- prompt sections, dynamic context and tool schemas are assembled through scoped providers;
- Skills are discovered through provider registries, shown initially as bounded summaries and loaded lazily;
- tool calls pass through pre-execute policy, monotonic guards, approval, execution wrappers, post-execute policy and authoritative normalized results;
- approval is audited and fail closed; only a one-shot explicit grant permits the gated action;
- sandbox policy is resolved per call and reports enforcement completeness instead of treating `sandbox=true` as proof;
- persistence preserves committed events and represents interruption/recovery rather than erasing an incomplete execution;
- same-session Goal state uses revisions so stale mutations can be rejected.

The harness adopts these ideas as a **Runtime Kernel reference**, not as a replacement for Infrastructure Engineering control-plane semantics. `runtime/` therefore adds append-only Runtime Events, revisioned state, Runtime Skill invocation policy, guarded Tool Pipeline contracts, one-shot Approval, sandbox evidence fields and deterministic tests.

One important boundary is intentionally stricter here: not everything is a replaceable plugin. Evidence provenance, independent production authorization, auditability and source-of-truth protection remain hard invariants. A runtime event records what the Agent saw or did; it becomes engineering evidence only after the appropriate environment/tool/human/test verification.

https://github.com/deepseek-ai/deepseek-harness

## NVIDIA ACES / SkillEvaluator

ACES evaluates a target Skill as an executable agent artifact rather than only inspecting `SKILL.md`. It holds task, model, harness, workspace and scoring policy constant, runs a baseline without the Skill and a treatment with the Skill, then reports the difference as Skill Lift. The harness adopts the paired experiment shape, explicit/implicit/contextual/negative task design, runtime signals for security/discovery/workflow/outcome/efficiency, and the rule that checked-in fixtures do not count as live verification.

https://arxiv.org/abs/2608.20614
https://github.com/NVIDIA/SkillEvaluator

## Kun Chen / backpass

The article "Your AGENTS.md is a Neural Net" and the `backpass` project treat project-level agent memory as a bounded behavioral surface improved from the sessions that actually ran. Useful operational ideas include a token budget, deterministic transcript distillation, verbatim evidence, at least two independent sessions before adding a new instruction, small edit batches, human review, and extracting narrow instructions into Skills instead of growing always-loaded memory indefinitely.

This harness adopts those ideas with a stricter infrastructure boundary: transcript evidence may propose changes to `AGENTS.md`, but it must not optimize durable source-of-truth artifacts such as Architecture, ADRs, Policies, Service Catalog, Domain definitions, Loop contracts, Evals, or Capability trust metadata. Candidate context revisions are evaluated with paired Context Lift experiments before claiming they improve agent behavior.

https://blog.kunchenguid.com/p/your-agentsmd-is-a-neural-net
https://github.com/kunchenguid/backpass

## Paperthin

Paperthin packages low-level agentic design patterns around restraint: clean an artifact instead of layering patches, consolidate duplicated truth into one canonical home, check a newly changed artifact with fresh verification, audit evaluations for circularity, preserve lessons and negative corpus across iterations, and surface disagreement across genuinely different lenses rather than averaging it away.

The harness does not install Paperthin as an execution dependency. A pinned MIT-licensed revision is registered as `reference_only`, while the reusable principles are implemented through local governed Skills:

- `artifact-hygiene` — clean current-state artifacts, preserve authoritative history, and allow a no-op when nothing improves;
- `ssot-review` — read-only scatter/contradiction audit before any consolidation;
- `eval-integrity` — independent-ground-truth and leakage review for Skill Lift, Context Lift, benchmarks, metrics, and experiments;
- `loop-engineering` learning — preserve earned reuse, negative corpus, anti-patterns, and next-cycle quality gates instead of copying accidental architecture forward.

The external `prism` pattern also reinforces an existing cross-domain rule: reliability, security, delivery, cost, and infrastructure constraints should not be averaged into one blended score when their disagreement is the material engineering fact.

https://github.com/LilMGenius/paperthin

## gstack

gstack is used as a **workflow composition and Agent UX reference**, not as an infrastructure authority model. Its most relevant idea is that Skills are experienced as a connected process rather than an unstructured menu: upstream thinking/planning artifacts feed downstream review, QA, shipping and reflection.

The harness adopts this in a provider-neutral form:

- simple user intents expose useful Loop/Skill composition without forcing a universal routing chain;
- users do not need to manually select every internal Skill;
- workflow steps pass explicit artifacts/evidence forward;
- review, verification and reflection remain distinct stages;
- the simple workflow surface does not bypass internal policy, human gates or independent production authorization.

This is documented in `docs/WORKFLOW-SURFACE.md`. Unlike gstack's software-shipping focus, this harness keeps infrastructure outcome verification and production control-plane authorization as independent hard boundaries.

https://github.com/garrytan/gstack

## GBrain

GBrain is used as a **persistent memory, retrieval, context-pack and knowledge-consolidation reference**. Particularly reusable ideas are bounded context assembly, explicit knowledge gaps, cross-session persistence, and separating fast/recent memory from more durable consolidated knowledge.

The harness translates those ideas into a stricter engineering epistemic model:

```text
Observation
    ↓ independent verification
Verified Fact
    ↓ engineering reasoning
Engineering Assessment
    ↓ outcome evidence
Learning Candidate
    ↓ governance
Durable Organizational Knowledge
```

The harness therefore does **not** import a generic memory item directly as engineering truth. It keeps observations, verified facts, assessments and durable organizational knowledge separate; confidence is never a substitute for verification. `schemas/context-pack.schema.json` defines bounded task context with freshness and evidence gaps, while `schemas/knowledge-candidate.schema.json` defines the review boundary for learned material.

GBrain's distinction between hot facts and cold/retrospective knowledge also motivates explicit consolidation after a Loop rather than uncontrolled growth of always-loaded context. The resulting model is documented in `docs/KNOWLEDGE-CONSOLIDATION.md`.

https://github.com/garrytan/gbrain

## Anthropic Context Engineering / Unhobbling

Anthropic reported in July 2026 that it removed more than 80% of Claude Code's system prompt for newer Claude models without measurable loss on its coding evaluations, and described the previous context as overconstraining the model. The broader lesson is not "short prompts always win"; it is that accumulated rules must continue to earn their place as model capability changes.

The Harness adopts this as an **unhobbling reference**:

- keep always-loaded agent guidance small;
- move narrow procedures to progressively disclosed Skills or references;
- prefer interface/contract descriptions over fixed reasoning recipes;
- let the model choose investigation order and next action when ordering is not itself a requirement;
- enforce authority, evidence, state, approval, and verification through Runtime/schema/policy boundaries;
- measure bare vs minimal vs richer Harness profiles instead of assuming more guidance is better.

This motivates `docs/HARNESS-UNHOBBLING.md` and `harness-evals/`.

https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

## Anthropic Commerce Agents

`anthropics/commerce-agents` is used as an **agent product / backend / runtime-enforcement reference**. Its most reusable pattern is not commerce-specific: the shopping and merchant agents are user-facing products, while prompts, Skills, backend contracts, gates, executor/runtime, and approvals sit beneath them.

The Infrastructure Engineering Agent adopts the same separation in provider-neutral form:

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

Particularly relevant patterns:

- **backend-owned credentials** — platform credentials remain server-side; the model sees normalized results;
- **provenance-bound writes** — a model cannot safely target arbitrary identifiers merely by naming them; infrastructure mutation should bind to resources discovered/validated in the current trusted scope;
- **stage → approve → apply** — mutation proposals are staged first and approval state is owned by the host/runtime, not inferred from chat text;
- **tool-call enforcement** — safety and authorization rules hold in code even when the model misstates them;
- **capability-aware surfaces** — when a capability is disabled, its tools and related prompt guidance disappear rather than remaining as dead context;
- **progressive Skill loading** — the model receives bounded Skill summaries and loads bodies only when useful;
- **delegation cannot expand authority** — read-only analysis/subagents do not gain write scope merely by discovering an identifier;
- **live recording → replay eval** — real executions can be recorded once and deterministically re-scored in CI.

The current reference runtime now implements the deterministic local form of several of these ideas through `runtime/provenance.py`, `runtime/fencing.py`, `runtime/change_control.py`, `runtime/recording.py`, and capability projection in `runtime/skill_registry.py`. Live provider enforcement remains experimental.

The project remains stricter on independent engineering verification, epistemic classes, Loop reconciliation, regression obligations, and cross-provider neutrality.

https://claude.com/blog/the-anatomy-of-effective-commerce-agents\nhttps://github.com/anthropics/commerce-agents

## IBM Loop Engineering

IBM describes loop engineering as designing agentic workflows that iteratively guide agents through goals, action, observation and adjustment. This harness adopts bounded loops but adds infrastructure-specific reconciliation, independent authorization and provenance.

https://www.ibm.com/think/topics/loop-engineering

## LongHorizon-Harness

LongHorizon-Harness frames long-running agent execution as task-state management. Its Manage-Execute-Audit model keeps task state explicit outside execution and updates it with independently verified environment facts. This motivates `loop-state`, external `verified_facts`, and one-iteration-at-a-time execution.

https://arxiv.org/abs/2608.01964

## LoopsBench

LoopsBench evaluates sustained agent loops using dependency DAGs and keeps completed units as regression obligations. The harness generalizes this beyond coding: recovered reliability, data integrity, security scope, delivery stability and cost traceability can remain obligations in later iterations.

https://arxiv.org/abs/2608.00267

## Kubernetes Controllers and OpenGitOps

Kubernetes controllers continually observe actual state and try to move it toward desired state. OpenGitOps adds declarative/versioned desired state and continuous reconciliation. The harness applies the same idea to engineering outcomes even when Terraform, Kubernetes or GitOps are not used.

https://kubernetes.io/docs/concepts/architecture/controller/
https://opengitops.dev/

## Google SRE

SRE provides the reliability control signals used by the SRE loops: SLI/SLO, error budget, incident response and error-budget policy.

https://sre.google/sre-book/service-level-objectives/
https://sre.google/workbook/error-budget-policy/

## DORA

DORA recommends application/service-level measurement, establishing a baseline, identifying the dominant constraint, making an improvement, checking progress and repeating. `delivery-improvement` follows this pattern and protects stability as a regression obligation.

https://dora.dev/guides/dora-metrics/

## FinOps Framework

FinOps is performed iteratively through Inform, Optimize and Operate. `finops-optimization` adds realized-value verification so expected savings are compared with actual cost/value and reliability outcomes.

https://www.finops.org/framework/
https://www.finops.org/framework/phases/

## Synthesis

```text
Desired Outcome
       ↓
Minimal Seed Context
       ↓
Model Judgment
   ↙          ↘
Pull Context   Use Tools / Skills / Capabilities
   ↘          ↙
      Proposed Action
            ↓
Runtime / Evidence / Permission / Approval Boundary
            ↓
Independently Authorized Action
            ↓
Independent Verification
            ↓
Reconcile Goal + State + Constraints + Regression
            ↓
continue / terminal
            ↓
Learning Candidate → Governance → Durable Knowledge
```

The Infrastructure Engineering Agent is free to choose a better reasoning path. Its internal harness/runtime remains strict about what the model cannot self-assert: independent truth, protected authority, production control, and verified completion.

Guidance itself is evaluated:

```text
Skill behavior   → paired Skill Lift
AGENTS behavior  → paired Context Lift
Whole Harness    → bare / minimal / full Harness Lift
```

Neither evaluation path may rewrite engineering truth or bypass authorization. Richer guidance must earn its complexity; deletion is a valid optimization when live evidence shows equal or better outcomes without safety or evidence regression.
