# Architecture

The **Infrastructure Engineering Agent** is the product. A thin **Agent Orchestrator / Turn Runtime** runs each interaction. The internal **Harness / Control Plane** constrains authority, evidence, execution, and verified completion.

Core rule:

> **Let the model choose the reasoning path; make execution flow explicit; constrain authority and truth at the control-plane boundary.**

## Canonical architecture

```text
USER / CHANNEL
CLI / Web / Slack / GitHub / MCP / API
                    │
                    ▼
          Agent Orchestrator / Turn Runtime
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Context      Memory    Available Surface
                              Skills / Tools
        └───────────┼───────────┘
                    ▼
       Infrastructure Engineering Agent
               Model Judgment
                    │
               next action
                    ▼
              Tool Executor
                    │
                    ▼
          Harness / Control Plane
    Provenance · Scope · Guard · Approval
    Change Revision · Audit · Recording
                    │
                    ▼
            Capability Backends
 Resource · Evidence · Delivery · Change · Verify
                    │
                    ▼
 AWS / K8s / CI/CD / Observability / Cost / Security
                    │
                    ▼
        Independent Verification
               ┌────┴────┐
               │         │
              DONE   RECONCILE
                         │
                Engineering Loop
                 only when needed
                         │
                         ▼
                 Verified Outcome
                         │
                         ▼
                 Learning Candidate
                         │
                    Governance
                         │
                         ▼
                  Durable Knowledge
```

A simple review, analysis, or bounded read task may finish after independent verification. It does **not** enter an Engineering Loop merely because Loop contracts exist.

## 1. Product: one Infrastructure Engineering Agent

Infrastructure, Operations, DevOps, SRE, FinOps, and Security are capability domains/lenses inside one Agent. Separate agents are not the default architecture.

The model owns:

- engineering reasoning;
- hypothesis formation;
- next-action judgment;
- selection among the currently available Context, Skills, and Tools.

The model does **not** own credentials, engineering truth, approval state, production authority, or verified completion.

Optional specialist delegation is a scaling mechanism only. A delegate must stay inside the parent capability/resource scope and cannot expand mutation eligibility.

## 2. Application Runtime: Orchestrator

`runtime/orchestrator.py` is the reference **Agent Turn Runtime**. It converges normalized channel requests onto one execution lifecycle:

```text
TurnRequest
    ↓
resolve Context + available surface
    ↓
model turn
    ↓
read-only tool calls when requested
    ↓
model continuation
    ↓
independent verification
    ↓
verified / unverified / budget-exceeded outcome
```

The Orchestrator owns **flow**, not truth or authorization.

Production workflow/change execution is deliberately not implemented directly in the reference Orchestrator. Mutation-capable actions must continue through `ToolPipeline`, `ChangeControl`, resource provenance, approval, and an authorized backend.

All product channels normalize through `runtime/channel.py`. Channel metadata never expands authority.

## 3. Model-visible surface: Context, Skills, Tools

The model should need only three primary concepts:

```text
Context
Skills
Tools
```

Other project concepts are primarily runtime metadata:

- **Domain** — optional engineering lens/classification;
- **Capability** — availability, trust, source, risk, and implementation metadata;
- **Binding** — resource/evidence/permission scope;
- **Workflow** — convenience entrypoint;
- **Loop** — optional external reconciliation state machine.

The Agent should not be forced through `Domain → Skill → Capability Routing → Loop` as a universal chain.

### Context facade

The model-facing Context Resolver may assemble bounded material from several internal stores:

```text
User / Session Memory
Organizational Knowledge
Evolution Knowledge
Engineering Evidence
Resource Graph
        ↓
Context Resolver
        ↓
Context Pack
```

Storage classes remain separate because they have different truth and governance semantics, but the model receives one bounded contextual surface with provenance, freshness, and explicit gaps.

## 4. Harness / Control Plane

The Harness is the non-optional safety and truth boundary beneath model judgment.

Hard responsibilities include:

- Evidence and Resource Provenance;
- resource and permission scope;
- untrusted-content fencing;
- monotonic guards;
- external production authorization;
- revision-bound staged change approval;
- apply-time revalidation;
- audit and runtime state;
- recording/replay integrity;
- independent verification and regression obligations;
- protected organizational truth.

Hard boundaries belong in Runtime/schema/policy/backend enforcement rather than repeated prompt prose.

## 5. Runtime Event Log is execution SSOT

`RuntimeEventLog` is the canonical record of what one Agent run saw, requested, executed, and verified.

```text
Runtime Event Log
        │
   ┌────┼─────────┐
   ▼    ▼         ▼
 Trace Metrics  Recording
   │    │         │
   └────┴────┬────┘
             ▼
          Evaluation
```

Trace/span data, latency/cache metrics, and immutable recordings are observations or projections of the same execution history; they must not become competing truth stores.

`runtime/observability.py` can append span lifecycle events to the same Runtime Event Log. `LatencyTracker.from_event_log(...)` derives model/tool performance counters from committed runtime events.

Runtime events are still **execution facts**, not automatically Engineering Evidence or Verified Facts.

## 6. Environment, Resource Graph, and Evidence

`environment/` normalizes discovered cloud, Kubernetes, CI/CD, observability, cost, and security resources into the provider-neutral Resource Graph.

Trusted discovery establishes resource provenance. A mutation target must remain inside the appropriate Bound Capability resource scope.

Provider-specific read-only observations enter through evidence adapters and require source provenance plus observation time. Tool output is not promoted to verified engineering truth merely because a call succeeded.

## 7. Backend boundary

`InfrastructureEngineeringBackend` remains the current facade. Its responsibilities naturally separate into four capability contracts:

```text
Resource Discovery
Evidence Collection
Change Management
Outcome Verification
```

Future provider implementations should prefer narrow typed protocols behind the facade rather than growing a single `dict[str, Any]` API indefinitely.

Credentials remain server/runtime-owned and are never model context.

## 8. Independent Verification and optional Engineering Loop

Independent Verification answers whether a material claim or outcome is supported by current environment/tool/human/test evidence.

For ordinary bounded work:

```text
Action / Assessment
      ↓
Independent Verification
      ↓
Done or Unverified
```

For genuinely long-running work:

```text
Goal + Current State + Constraints + Terminal Conditions + Budget
      ↓
model chooses next action
      ↓
control-plane enforcement
      ↓
independent observation
      ↓
reconcile
      ↓
repeat only while useful
```

Runtime state and Loop state remain separate: Runtime reconstructs execution; Loop state reconciles an engineering objective against independently verified world state.

## 9. Learning and durable knowledge

Persistence or repetition does not create truth.

```text
Observation
    ↓ independent verification
Verified Fact
    ↓ reasoning
Engineering Assessment
    ↓ outcome evidence
Learning Candidate
    ↓ owner / governance review
Durable Organizational Knowledge
```

Semantic memory extraction may create a Learning Candidate, but cannot automatically promote conversation patterns into Policy, Runbook truth, ADRs, Service Catalog, or Verified Facts.

## 10. Evaluation and release

Evaluation is grouped by purpose instead of accumulating unrelated scoring frameworks:

- **Artifact lift** — Skill Lift, Context Lift, Harness Lift;
- **Task outcome** — incident, change, delivery, FinOps, security scenario profiles;
- **Runtime invariants** — provenance, approval, fencing, delegation, recording;
- **Long-running behavior** — Loop/regression evaluation;
- **Release** — canary, live recordings, outcome/cost/latency telemetry.

Domain is primarily classification/lens metadata for task evaluation, not another mandatory execution layer.

## Reference roles

Primary structural references:

- Anthropic Commerce Agents — Agent product, standard Agent loop, Skills/tools/backend/runtime safety;
- Anthropic Context Engineering — unhobbling, minimal always-loaded context, progressive disclosure;
- Samsung Account AgentCore AIOps — production observability, channel convergence, task evaluation, scale-out pressure;
- Kubernetes Controllers + LongHorizon-Harness — explicit external state and reconciliation;
- NVIDIA SkillEvaluator / ACES — artifact/effect evaluation.

Supporting references:

- DeepSeek Harness — event/runtime extensibility patterns, not the authority model for the whole control plane;
- GBrain — memory/knowledge separation;
- Backpass — context evolution;
- Paperthin — artifact hygiene, SSOT, eval-integrity reflexes;
- LoopsBench — long-running evaluation;
- MCP/OpenGitOps — tool/declarative supporting standards.

Engineering domain truth remains grounded in Google SRE, DORA, and FinOps Framework.

See `docs/REFERENCE-MODELS.md` for reference provenance and adoption rules.
