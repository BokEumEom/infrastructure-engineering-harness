# Architecture

The harness separates durable knowledge, environment discovery, current evidence, bounded context assembly, engineering judgment, technology implementation knowledge, loop control, runtime execution mechanics, production execution, and governed knowledge consolidation.

```text
Durable Knowledge                 Live Environment
Service Catalog / ADR / Policy    Cloud / K8s / CI / Observability
          │                                  │
          │                         Read-only Discovery
          │                                  ↓
          │                           Resource Graph
          │                                  │
          └──────────────┬───────────────────┘
                         ↓
                 Context Resolution
                         ↓
                 Bounded Context Pack
             knowledge + evidence + gaps
                         ↓
                  Domain Lens(es)
                         ↓
                  Decision Skill
             what should change and why
                         ↓
                Capability Routing
             how to build/operate/verify
                         ↓
                  Bound Capability
      capability + resource + evidence + permission scope
                         ↓
          Implementation / Verification Capability
                         ↓
               Reviewable Local Artifact
                         ↓
               Validation / Human Gate
                         ↓
               Runtime Kernel Boundary
    Event Log / Skill Registry / Tool Pipeline
    Guard / Approval / Sandbox / Persistence
                         ↓
             Independently Authorized Execution
                         ↓
               Loop Engineering Control
          Observe → Decide → Verify → Reconcile
             ↑                         ↓
             └──────── Learn ──────────┘
                         ↓
             terminal: done/escalated/failed
                         ↓
                  Learning Candidate
 Observation / Verified Fact / Assessment kept distinct
                         ↓
              Knowledge Consolidation
        dedupe / contradiction / owner review
                         ↓
 Incident / Runbook / ADR or Policy candidate / Eval
                         ↓
           Governed Durable Knowledge
                         ↓
                      Next Loop
```

## Shared core

The core owns contracts that should not vary by model, provider or discipline: progressive context loading, bounded Context Packs, explicit evidence gaps, service/dependency model, evidence/provenance, ADR/incident knowledge, epistemic classes, knowledge candidates, domain profiles, change/ticket contracts, capability source trust, environment/resource binding, loop state and provider-neutral eval infrastructure.

## Environment discovery and resource graph

`environment/` defines the provider-neutral layer between live infrastructure and task context.

Discovery adapters may inspect cloud, Kubernetes, CI/CD, observability, cost and security systems in read-only mode and normalize discovered resources into `schemas/resource-graph.schema.json`. A Resource Graph records resources, typed relationships and discovery provenance.

Discovery is not durable organizational truth and is not automatically a Loop verified fact. It may enrich current context while Architecture, ADRs, Policies and Service Catalog remain protected sources of truth.

A **Bound Capability** combines an existing capability with explicit resource ids, evidence sources and permission scope. Binding may narrow authority but must never increase it. A third-party `reference_only` capability remains non-executable even when bound to a real production resource.

## Evidence adapters

Provider-specific operational data enters through `adapters/evidence/`.

```text
Provider API → read-only adapter → adapter result → normalization → Evidence → independent verification
```

Adapter results require provenance and observation time. They may be useful current evidence, but the adapter and model cannot self-promote observations into Loop `verified_facts`.

## Context Pack and evidence gaps

Context resolution should produce a bounded, task-specific Context Pack conforming to `schemas/context-pack.schema.json` instead of dumping all available knowledge into the model.

A Context Pack combines only the information required for the current workflow/Loop step:

- authoritative or governed organizational knowledge;
- current evidence and verified facts;
- resource/dependency scope;
- freshness metadata;
- token budget;
- explicit unknowns and required evidence.

A missing signal is represented as a `gap`, not hidden behind confidence language. A blocking gap prevents the downstream Loop condition from being treated as verified.

Context Pack assembly does not change authority. A provisional learning candidate remains provisional even when included in context, and stale evidence remains stale.

## Domain, Decision, Capability and Loop

These layers have different responsibilities:

```text
Context Pack→ what bounded knowledge/evidence/gaps the current step may use
Domain      → which engineering questions and constraints matter
Decision    → what should be done and why
Capability  → how to implement or verify using technology-specific knowledge
Binding     → where the capability applies, with which evidence and permission scope
Runtime     → how model context, Skills, tools, policy, approval and durable execution events are mediated
Loop        → when to repeat, verify, escalate, stop and learn
```

The current domain lenses are Infrastructure, SRE, DevOps, FinOps and Security.

Decision Skills remain provider-neutral. Capability Skills may be technology-specific. A technology-specific capability must not silently replace an Architecture/SRE/Security/FinOps decision.

## Capability trust boundary

`capabilities/registry.yaml` records local and external capability sources.

Third-party sources are `pinned_reference` by default:

- immutable revision required;
- license recorded;
- minimum relevant Skill loaded progressively;
- scripts/commands/assets treated as reference material;
- external commands are not automatically executed;
- useful patterns are translated into local reviewable artifacts;
- current-state claims still require environment/tool/human/test evidence;
- execution remains separately authorized.

An organization can vendor/review selected capabilities and register them as managed/local sources.

## Runtime Kernel

`runtime/` defines the initial provider-neutral execution contract. It is a reference kernel, not yet a production daemon.

The Runtime Kernel adopts several strong agent-runtime patterns while keeping infrastructure-specific hard invariants outside replaceable plugin seams:

- append-only typed Runtime Event Log;
- **model-visible means logged** reconstructability;
- revisioned run state with stale-update rejection;
- lazy Runtime Skill Registry over the trusted Capability Registry;
- guarded Tool Execution Pipeline;
- monotonic hard-deny guards;
- fail-closed one-shot approval;
- explicit sandbox enforcement facts;
- normalized tool result before Evidence promotion.

Runtime plugins/providers may vary model adapters, persistence backends, tool implementations, sandboxes and remote execution systems. They must not replace Evidence provenance, independent production authorization, auditability or source-of-truth protection.

Runtime events answer what the Agent actually saw/requested/executed. They are not automatically engineering truth. Environment/tool/human/test verification is still required before a claim enters Loop `verified_facts`.

## Scenario evaluation

`evals/scenarios/` holds infrastructure scenarios with explicit ground truth, required evidence, red herrings, prohibited actions, expected behavior and success conditions. These scenarios are intended for future live runners and paired Skill/Context experiments, while schema validation keeps the scenario contract deterministic in CI.

## Loop state

Loop state is explicit outside agent prose and is updated only with independently verified facts. A successful condition can remain a regression obligation in later iterations.

Runtime state and Loop state are intentionally separate. Runtime state reconstructs agent execution; Loop state reconciles an engineering objective against independently verified world state.

## Knowledge consolidation

Loop learning is not automatically organizational truth. The harness uses the following epistemic sequence:

```text
Observation
    ↓ independent verification
Verified Fact
    ↓ reasoning
Engineering Assessment
    ↓ outcome evidence
Learning Candidate
    ↓ artifact owner / governance review
Durable Organizational Knowledge
```

`schemas/knowledge-candidate.schema.json` defines the proposal boundary. Supporting and contradicting evidence remain attached to the candidate. Confidence may describe an assessment but does not replace verification.

Consolidation may deduplicate, group, detect contradictions and propose target updates. It must not silently overwrite Architecture, ADRs, Policies, Service Catalog, Runbooks, or other protected truth. Failed hypotheses and prohibited paths remain available as negative corpus/eval candidates.

See `docs/KNOWLEDGE-CONSOLIDATION.md`.

## Workflow surface

The user-facing workflow surface may route simple intents such as incident, reliability, delivery, FinOps, security, change and learn into the appropriate Domain/Loop/Skills. This is progressive disclosure only: routing never increases authority or bypasses evidence, approval, regression, or production boundaries.

See `docs/WORKFLOW-SURFACE.md`.

## Production boundary

The default harness may analyze, design, generate code/config/pipelines/runbooks, verify available checks and create workflow artifacts, but production execution remains independently authorized. `change-validation` can orchestrate precheck → approval → external execution → post-verification without making the model or runtime the authorization boundary.

## Agent and tool adapters

Codex/Kiro use `AGENTS.md`; Claude Code additionally exposes local Skills. Cloud/runtime/observability/delivery/cost systems are optional discovery and evidence adapters. Jira/Linear workflow actions use MCP. External Skill libraries are optional capability references. Tool output must be normalized before it is treated as evidence.

Future execution adapters should implement the contracts under `runtime/` instead of bypassing them with direct model-to-provider mutation.

See `environment/README.md`, `adapters/evidence/README.md`, `runtime/README.md`, `capabilities/README.md`, `docs/CAPABILITY-MODEL.md`, `docs/WORKFLOW-SURFACE.md`, `docs/KNOWLEDGE-CONSOLIDATION.md`, `loops/README.md` and `docs/REFERENCE-MODELS.md`.
