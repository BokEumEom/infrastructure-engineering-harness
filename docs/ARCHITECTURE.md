# Architecture

The harness separates durable knowledge, current evidence, engineering judgment, technology implementation knowledge, loop control, runtime execution mechanics and production execution.

```text
Durable Knowledge + Optional Live Evidence
                    ↓
              Context Resolution
                    ↓
               Domain Lens(es)
                    ↓
               Decision Skill
          what should change and why
                    ↓
             Capability Routing
          how to build/operate/verify
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
 Incident / Runbook / ADR or Policy candidate / Eval
                    ↓
                 Next Loop
```

## Shared core

The core owns contracts that should not vary by model, provider or discipline: progressive context loading, service/dependency model, evidence/provenance, ADR/incident knowledge, domain profiles, change/ticket contracts, capability source trust, loop state and provider-neutral eval infrastructure.

## Domain, Decision, Capability and Loop

These layers have different responsibilities:

```text
Domain      → which engineering questions and constraints matter
Decision    → what should be done and why
Capability  → how to implement or verify using technology-specific knowledge
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

## Loop state

Loop state is explicit outside agent prose and is updated only with independently verified facts. A successful condition can remain a regression obligation in later iterations.

Runtime state and Loop state are intentionally separate. Runtime state reconstructs agent execution; Loop state reconciles an engineering objective against independently verified world state.

## Production boundary

The default harness may analyze, design, generate code/config/pipelines/runbooks, verify available checks and create workflow artifacts, but production execution remains independently authorized. `change-validation` can orchestrate precheck → approval → external execution → post-verification without making the model or runtime the authorization boundary.

## Agent and tool adapters

Codex/Kiro use `AGENTS.md`; Claude Code additionally exposes local Skills. Cloud/runtime/observability/delivery/cost systems are optional evidence adapters. Jira/Linear workflow actions use MCP. External Skill libraries are optional capability references. Tool output must be normalized before it is treated as evidence.

Future execution adapters should implement the contracts under `runtime/` instead of bypassing them with direct model-to-provider mutation.

See `runtime/README.md`, `capabilities/README.md`, `docs/CAPABILITY-MODEL.md`, `loops/README.md` and `docs/REFERENCE-MODELS.md`.
