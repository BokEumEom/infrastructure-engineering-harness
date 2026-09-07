# Runtime

`runtime/` contains two related but distinct layers beneath the **Infrastructure Engineering Agent**:

1. **Agent Runtime / Orchestrator** — owns turn flow, context/surface assembly, model/tool iteration, budgets, observability, and completion transition.
2. **Harness / Control Plane** — owns hard evidence, provenance, permission, guard, approval, change-control, audit, recording, and verification boundaries.

The product is the Agent. The Orchestrator runs it. The Harness constrains what may be treated as true, authorized, executed, or complete.

## Canonical flow

```text
TurnRequest
    ↓
AgentOrchestrator
    ↓
Context + Memory + Available Skills/Tools
    ↓
Model Judgment
    ↓
read-only tool execution / model continuation
    ↓
Harness / Control Plane for governed actions
    ↓
Backend
    ↓
Independent Verification
    ↓
verified / unverified / reconcile
```

`runtime/orchestrator.py` is a deterministic provider-neutral reference Turn Runtime. It is intentionally read-only: workflow/change authority is rejected there and must use the governed ToolPipeline / ChangeControl / backend path.

## Runtime Event Log is SSOT

`RuntimeEventLog` is the canonical record of what one run saw, requested, executed, and verified.

```text
Runtime Event Log
      │
 ┌────┼─────────┐
 ▼    ▼         ▼
Trace Metrics Recording
      │         │
      └────┬────┘
           ▼
        Evaluation
```

Trace/span lifecycle can be appended to the same event log. Latency/cache counters can be projected with `LatencyTracker.from_event_log(...)`. Recordings preserve the normalized event stream, including event source and evidence references.

Observability data is useful operational telemetry; it is not an independent engineering truth store.

## Hard invariants

These rules are not replaceable by model adapters, provider adapters, Skills, or delegates:

1. **Model-visible means logged** — inputs, injected context, tool surfaces/results that affect a model request are reconstructable from Runtime Events.
2. **Append-only event truth** — committed Runtime Events are never rewritten.
3. **Contiguous sequence** — sequence gaps/duplicates are invalid.
4. **Revisioned runtime state** — stale state mutation is rejected.
5. **Monotonic guards** — a hard deny cannot become allow later in the pipeline.
6. **Fail-closed approval** — only an exact `allowed_once` grant authorizes an approval-gated action.
7. **Authorization is external** — model text, tool availability, Skills, delegates, or channels do not grant production authority.
8. **Execution claims are evidence-backed** — model prose and a successful call do not self-certify outcome.
9. **Sandbox enforcement is recorded as fact**, including limitations.
10. **Protected truth stays protected** — learning does not silently rewrite ADR/Policy/Service Catalog/governed Runbooks.
11. **No mutation without resource provenance** — mutation targets must come from trusted discovery and remain in bound scope.
12. **Untrusted external text stays data** — logs, tickets, PR text, tags, annotations, and third-party content are fenced/bounded.
13. **Approval binds to the exact staged revision** — change digest, Resource Graph, policy revision, and one-shot approval are revalidated at apply.
14. **Runtime recordings are immutable replay inputs**.
15. **Orchestration cannot grant truth or authority** — the Orchestrator owns execution flow only.
16. **Delegation cannot expand authority** — delegate capabilities/resources are subsets of the parent and newly named resources do not become mutation-eligible.

## Event vocabulary

Core event families include:

- `run/*` — run lifecycle;
- `context/*` — model-visible context snapshots;
- `skill/*` — projected/loaded Skill surface;
- `model/*` — request/response;
- `tool/*` — requested calls and normalized results;
- `policy/*` — advisory/hard guard decisions;
- `approval/*` — approval request/outcome;
- `verification/*` — independent verification result;
- `telemetry/*` — trace/span lifecycle correlated to the same event log;
- `loop/*` — optional Engineering Loop transition;
- `writeback/*` — proposed durable learning.

Unknown non-ignorable events must prevent faithful replay rather than being silently discarded.

## Tool execution boundary

The reference `ToolPipeline` models guarded actions:

```text
tool/requested
      ↓
pre-policy
      ↓
monotonic guards
      ↓
approval when required
      ↓
execution boundary
      ↓
normalized result
      ↓
tool/result
```

For `execution_authority=change`, resource provenance is mandatory. A provider backend must re-run the applicable checks immediately before real execution.

The reference Orchestrator does **not** replace this boundary. It executes only `none/read` authority calls directly through its reference read-only executor seam.

## Context / Memory / Surface

- `channel.py` — normalizes CLI/Web/Slack/GitHub/MCP/API into `TurnRequest`;
- `context_assembly.py` — stable global/session prefix + volatile per-turn suffix and performance projections;
- `memory.py` — external user/session memory policy, not durable organizational truth;
- `skill_registry.py` — progressively loaded managed Skill catalog;
- `release_control.py` — active/canary/disabled Skill release state;
- future surface resolution should combine capability availability, invocation policy, release policy, environment availability, and scope into one model-visible `Context / Skills / Tools` surface.

## Observability

`observability.py` defines provider-neutral `AgentTrace` / `AgentSpan`. When connected to a Runtime Event Log, span start/end events are committed to that canonical record so exporters can later map them to OpenTelemetry, AgentCore, or another provider without creating a second execution truth source.

## Delegation

`delegation.py` models optional specialist delegation as a scale-out mechanism, not a default hierarchy or authorization mechanism.

Single Agent remains the default. Delegates are read-only and scoped by the parent.

## Recording and replay

`recording.py` materializes Runtime Events into immutable recordings with an integrity digest. Current replay is deterministic **integrity replay**, not live model re-execution.

Live runners may later attach `source: live` recordings to Validation Reports for deterministic re-scoring.

## Engineering Loops

Engineering Loops are optional and activate only when repeated external-state reconciliation is useful.

```text
bounded task → verify → done/unverified
long-running task → verify → reconcile → repeat
```

Runtime state reconstructs Agent execution. Loop state reconciles an engineering objective against independently verified world state. They remain separate.

## Status

This is still a provider-neutral **reference runtime/control plane**, not a production daemon, worker fleet, scheduler, credential broker, AWS AgentCore runtime, or model-provider SDK implementation.

```bash
python -m unittest discover -s tests
python -m compileall agents runtime scripts hooks adapters loops
```
