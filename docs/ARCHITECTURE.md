# Architecture

The harness separates durable knowledge, current evidence, engineering judgment, technology implementation knowledge, loop control and production execution.

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

## Loop state

Loop state is explicit outside agent prose and is updated only with independently verified facts. A successful condition can remain a regression obligation in later iterations.

## Production boundary

The default harness may analyze, design, generate code/config/pipelines/runbooks, verify available checks and create workflow artifacts, but production execution remains independently authorized. `change-validation` can orchestrate precheck → approval → external execution → post-verification without making the model the authorization boundary.

## Agent and tool adapters

Codex/Kiro use `AGENTS.md`; Claude Code additionally exposes local Skills. Cloud/runtime/observability/delivery/cost systems are optional evidence adapters. Jira/Linear workflow actions use MCP. External Skill libraries are optional capability references. Tool output must be normalized before it is treated as evidence.

See `capabilities/README.md`, `docs/CAPABILITY-MODEL.md`, `loops/README.md` and `docs/REFERENCE-MODELS.md`.
