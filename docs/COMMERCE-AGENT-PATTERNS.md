# Commerce Agent Patterns for Infrastructure Engineering

Anthropic's *The Anatomy of Effective Commerce Agents* and the `anthropics/commerce-agents` repository are reference models for building the Infrastructure Engineering Agent as a product rather than as a large prompt.

References:

- https://claude.com/blog/the-anatomy-of-effective-commerce-agents
- https://github.com/anthropics/commerce-agents

## Adopted architecture

```text
User
 ↓
Single Infrastructure Engineering Agent
 ↓
standard model/tool loop
 ├─ minimal context
 ├─ progressive Skills
 ├─ capabilities
 └─ evidence
 ↓
Runtime / Harness boundary
 ├─ resource provenance
 ├─ untrusted-data fencing
 ├─ permission / guard
 ├─ staged change / approval
 ├─ audit / recording
 └─ independent verification
 ↓
Infrastructure Backend
 ↓
Provider systems
```

Infrastructure / Operations / DevOps / SRE / FinOps / Security remain capability domains inside one Agent. Separate sub-agents are not the default.

An Engineering Loop is optional control for work that genuinely needs repeated observation and reconciliation. A one-shot review does not enter a Loop merely because a Loop exists.

## Implementation status

| Commerce principle | Local implementation | Status |
| --- | --- | --- |
| One capable agent + Skills | single Infrastructure Engineering Agent; progressive Skill Registry | implemented contract |
| Minimal system context | bounded `AGENTS.md`, Context/Harness Lift | implemented |
| Backend-owned credentials | `InfrastructureEngineeringBackend` seam | contract; live providers experimental |
| Provenance-bound writes | `ResourceProvenanceIndex` + ToolPipeline provenance guard | reference runtime implemented |
| Stage → approve → apply | `ChangeControl` + revision-bound one-shot grant | reference runtime implemented |
| Apply-time revalidation | graph/policy/change digest/scope re-check | reference runtime implemented |
| Capability-aware surface | `enabled_capability_ids` projection | reference runtime implemented |
| Untrusted-content fencing | `runtime/fencing.py` | reference transform implemented |
| Runtime recording/replay | immutable event recording + integrity replay | reference runtime implemented |
| Outcome-based verification | independent verification + Loop terminal/regression obligations | implemented contracts |
| Persistent user/session memory | not implemented | future |
| Full live execution replay | integrity replay only; no model re-execution | future |
| Prompt caching / latency optimization | not implemented | future after live runner |
| Canary / Skill kill switch | not implemented | future release-control layer |

"Implemented" here means the deterministic reference/runtime contract exists and is tested. It does **not** mean a production AWS/Kubernetes/Datadog backend is complete.

## Resource provenance

A mutation-capable call should not target a resource merely because the model emitted an identifier.

```text
trusted discovery
      ↓
Resource Graph snapshot
      ↓
session/runtime provenance index
      ↓
Bound Capability resource scope
      ↓
mutation target
```

When the reference ToolPipeline is configured with `resource_provenance_required=True`, an undiscovered or out-of-scope target is a monotonic deny.

Creation operations may need a provenanced parent/container scope rather than a pre-existing target resource. Provider adapters should model that explicitly instead of disabling the provenance rule.

## Untrusted infrastructure text

External engineering text can carry instructions that must not become authority:

- logs and traces;
- PR/issue descriptions and comments;
- Slack/Jira/Linear incident text;
- cloud tags and Kubernetes annotations;
- CI output;
- repository files from untrusted sources;
- third-party runbooks or documentation.

`runtime/fencing.py` removes invisible/control formatting, bounds the text, prevents fence-marker spoofing, and marks it as untrusted external data.

This is defense in depth, not a complete prompt-injection solution. Provider adapters and Context Resolution should apply the fence before untrusted text becomes model-visible.

## Staged changes

Approval is not attached only to a string change ID.

The reference contract binds approval to:

- change ID;
- change revision;
- proposal digest;
- Resource Graph snapshot;
- policy revision;
- one-shot grant.

Immediately before real execution, the provider backend should re-run these checks and resource provenance checks. If the resource graph or policy has changed, re-stage/re-review rather than silently applying stale intent.

## Capability-aware context

A capability that is not available should disappear from the model surface:

```text
connected/discovered systems
          ↓
enabled capability IDs
          ↓
Runtime Skill projection
          ↓
model-visible Skill/tool catalog
```

This prevents dead tools and irrelevant instructions from accumulating in context.

## Recording and replay

The Runtime Event Log can be materialized into an immutable recording with a digest.

Current replay verifies recording integrity, sequence, and run identity. It is deliberately not called a live-agent replay.

Future runners can:

```text
live execution
    ↓
source: live Runtime Recording
    ↓
Validation Report recording_ref
    ↓
deterministic scorer / regression replay
```

This keeps CI evidence reproducible while avoiding unnecessary model calls for checks that do not require model re-execution.
