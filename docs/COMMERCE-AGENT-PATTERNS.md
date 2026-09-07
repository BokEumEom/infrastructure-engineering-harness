# Commerce Agent Patterns for Infrastructure Engineering

Anthropic's *The Anatomy of Effective Commerce Agents* and `anthropics/commerce-agents` remain the primary references for building the Infrastructure Engineering Agent as a product rather than as a large prompt.

References:

- https://claude.com/blog/the-anatomy-of-effective-commerce-agents
- https://github.com/anthropics/commerce-agents

## Local synthesis

Commerce Agents reinforces two separate ideas:

1. use **one capable Agent** with progressively exposed Skills/Tools rather than a front intent-router + domain-agent farm by default;
2. still use a deterministic **application runtime / turn loop** to assemble context, call the model, execute tools, and continue the turn.

Local architecture:

```text
User / Channel
      ↓
Agent Orchestrator / Turn Runtime
      ↓
Single Infrastructure Engineering Agent
      ↓
Context + Skills + Tools
      ↓
model judgment / next action
      ↓
Tool Executor
      ↓
Harness / Control Plane
Provenance · Fence · Scope · Guard · Approval
Change Control · Audit · Recording
      ↓
Infrastructure Backend
      ↓
Provider systems
      ↓
Independent Verification
```

The Orchestrator is **not another LLM router Agent**. It is the deterministic application runtime around the standard model/tool loop.

Infrastructure / Operations / DevOps / SRE / FinOps / Security remain capability domains inside one Agent. Separate specialist delegates are optional and must earn their handoff cost through evaluation.

## Implementation status

| Commerce principle | Local implementation | Status |
| --- | --- | --- |
| One capable Agent + Skills | single Infrastructure Engineering Agent | implemented contract |
| Standard Agent turn loop | `runtime/orchestrator.py` | reference read-only runtime implemented |
| Minimal system context | bounded `AGENTS.md`, Context/Harness Lift | implemented |
| Backend-owned credentials | `InfrastructureEngineeringBackend` facade | contract; live providers experimental |
| Provenance-bound writes | `ResourceProvenanceIndex` + ToolPipeline | reference control plane implemented |
| Stage → approve → apply | `ChangeControl` + revision-bound one-shot approval | reference implemented |
| Apply-time revalidation | graph/policy/change digest/scope checks | reference implemented |
| Capability-aware surface | Skill Registry projection + policy/release controls | partial; unified Surface Resolver is future |
| Untrusted-content fencing | `runtime/fencing.py` | reference transform implemented |
| Runtime recording/replay | Event Log → immutable recording + integrity replay | reference implemented |
| Outcome-based verification | independent verifier contracts | implemented contracts |
| Persistent user/session memory | `PersistentMemoryStore` | reference implemented |
| Prompt caching / latency | stable prefix layout + Event Log-derived metrics | reference implemented; provider cache hits unverified |
| Canary / Skill kill switch | `active/canary/disabled` release controller | reference implemented |
| Full live execution replay | integrity replay only | future |
| Provider-specific optimization | provider-neutral layout only | future live/provider adapter work |

"Implemented" means deterministic local contracts exist and are tested. It does **not** mean a production AWS/Kubernetes/Datadog backend or live provider performance has been proven.

## Resource provenance and staged writes

A model-generated identifier is not enough to authorize mutation.

```text
trusted discovery
      ↓
Resource Graph
      ↓
Bound Capability scope
      ↓
exact staged revision
      ↓
independent approval
      ↓
apply-time revalidation
      ↓
execution
```

For `execution_authority=change`, provenance is mandatory. The reference Orchestrator intentionally refuses change authority so it cannot bypass this boundary.

## Capability-aware surface

The model should see only the currently usable surface:

```text
Capability Registry
× Invocation Policy
× Release Policy
× environment availability
× resource / permission scope
      ↓
Context + Skills + Tools
```

This is the infrastructure translation of Commerce Agents' deployment-driven tool/Skill surface. `capability-routing` is therefore optional implementation guidance, not a required routing layer.

## Memory and prompt performance

Persistent memory remains external contextual state, not engineering truth. Provider-neutral context assembly keeps stable global/session material before volatile per-turn evidence.

Runtime performance telemetry should converge on the canonical Event Log:

```text
Runtime Event Log
  ├─ model/tool latency
  ├─ cache token telemetry
  ├─ trace/span
  └─ recording/evaluation
```

Provider-specific cache controls, eager dispatch, rolling cache markers, or history compaction belong in provider adapters rather than the core.

See `docs/MEMORY-PERFORMANCE-RELEASE.md`.

## Recording and replay

The Event Log can be materialized into an integrity-checked recording. Current replay verifies sequence, identity, digest, source, and evidence-reference preservation; it does not re-run a live model.

Future live runners can create `source: live` recordings for deterministic re-scoring without confusing fixture plumbing with real Agent effectiveness.
