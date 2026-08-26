# Reference Models

Infrastructure Engineering Harness combines mature infrastructure feedback models with emerging agent Loop Engineering rather than replacing established practice.

Loop Engineering is an **emerging agent engineering term**, not an infrastructure industry standard. The harness therefore uses it as an execution pattern while grounding safety and operations in established engineering models.

| Reference | Contribution |
| --- | --- |
| DeepSeek Harness | Plugin-composed runtime, append-only session events, model-visible/logged reconstructability, guarded tool pipeline, scoped Skill discovery, fail-closed approval, sandbox and persistence seams |
| NVIDIA ACES / SkillEvaluator | Paired live evaluation with and without a Skill, trajectory grading and Skill Lift |
| Kun Chen / backpass | Transcript-driven, budgeted, evidence-gated improvement of project-level agent memory |
| Paperthin | Artifact restraint, clean-current-state rewrites, SSOT repair, eval independence, earned reuse, and cross-lens disagreement |
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
Observe Actual State
       ↓
Resolve Organizational Context
       ↓
Domain Skill(s)
       ↓
Decision / Proposal
       ↓
Runtime Kernel
 Event Log / Skill Registry / Tool Guard / Approval / Sandbox
       ↓
Independent Action or Human Gate
       ↓
Independent Verification
       ↓
Artifact Hygiene / Eval Integrity as applicable
       ↓
Regression Check
       ↓
Reconcile → continue or terminal
                       ↓
                      Learn
                       ↓
 Incident / Runbook / ADR or Policy candidate / Measurement / Eval / Negative corpus
                       ↓
                    Next Loop
```

Agent behavior has two separate learning paths:

```text
Skill behavior → paired Skill Lift → Skill revision
AGENTS behavior → transcript loss → proposed context edit → paired Context Lift
```

Neither path may rewrite engineering truth or bypass authorization. The model does not own truth, completion, or authorization; environment evidence, deterministic checks, runtime guards, provider controls and human approvals remain independent parts of the loop.
