# Runtime Kernel

The Runtime Kernel is the execution layer beneath the Infrastructure Engineering control plane.

It is inspired by mature agent-runtime patterns, including DeepSeek Harness, but keeps infrastructure-specific safety invariants non-swappable.

```text
Organizational Knowledge + Evidence
              ↓
Engineering Control Plane
Domain → Decision → Capability → Loop
              ↓
        Runtime Kernel
  Event Log / Context / Skills
  Tool Pipeline / Approval
  Sandbox / Persistence
              ↓
       Execution Systems
              ↓
        Actual World State
              ↓
           Evidence
```

## Status

`runtime/` is a provider-neutral **reference kernel**, not yet a production daemon, scheduler, worker fleet, or credential broker. It defines deterministic contracts that future runtimes and adapters must preserve.

## Hard invariants

These rules are not replaceable by plugins or provider adapters:

1. **Model-visible means logged** — every input, injected context snapshot, tool schema set, and tool result that can affect a model request must be reconstructable from the append-only Runtime Event Log.
2. **Append-only event truth** — committed runtime events are never rewritten. Derived views may be rebuilt from the log.
3. **Contiguous sequence** — each run appends the next `seq`; gaps, duplicate sequence numbers, and stale revisions fail.
4. **Revisioned state** — runtime-state mutations use compare-and-set semantics so stale workers cannot overwrite newer state.
5. **Monotonic guards** — a hard deny cannot be changed to allow by a later hook, plugin, model, or retry.
6. **Fail-closed approval** — `allowed_once` is the only granting approval outcome. Rejected, cancelled, unavailable, malformed, or missing approval denies the action.
7. **Authorization is external** — possession of a runtime, tool, Skill, ticket permission, or sandbox does not grant production mutation authority.
8. **Execution claims are evidence-backed** — tool output is normalized before becoming Evidence; agent prose is never execution proof.
9. **Sandbox enforcement is a fact** — record requested mode, actual mode, enforcement completeness, and known limitations. `sandbox=true` is not sufficient evidence.
10. **Source-of-truth remains protected** — runtime learning and plugins do not silently rewrite Architecture, ADRs, Policies, Service Catalog, or authorization metadata.

## Event vocabulary

The initial event contract is defined by `schemas/runtime-event.schema.json`.

Core event families:

- `run/*` — lifecycle and recovery boundaries;
- `context/*` — model-visible context snapshots;
- `skill/*` — catalog and loaded Skill identity;
- `model/*` — request envelope and response completion;
- `tool/*` — requested call and authoritative normalized result;
- `policy/*` — advisory and monotonic guard decisions;
- `approval/*` — paired approval request/outcome audit;
- `verification/*` — independent environment/tool/human/test result;
- `loop/*` — Engineering Loop transition;
- `writeback/*` — proposed durable learning.

Runtime implementations may add typed events, but an unknown non-ignorable event must prevent faithful replay rather than being silently discarded.

## Tool execution pipeline

```text
tool/requested
      ↓
pre-policy hooks
      ↓
monotonic guards ── deny ──→ normalized denial
      ↓
approval if required ── not allowed_once ──→ normalized denial
      ↓
execution policy
sandbox + credential scope
      ↓
tool execute
      ↓
post-policy inspection
      ↓
normalized immutable result
      ↓
tool/result
      ↓
optional Evidence normalization
```

The reference implementation in `runtime/kernel.py` models the policy/approval invariants without executing real tools.

## Runtime Skill Registry

`runtime/skill_registry.py` provides a small reference registry over `capabilities/registry.yaml`.

It separates three different questions:

- **discoverable** — can this Skill appear in a catalog for this runtime scope?
- **model invocable** — may the model load it on demand?
- **execution authority** — may following the Skill cause an action? This remains `none` for third-party `reference_only` Skills.

The model should initially receive bounded Skill summaries and load bodies lazily. Large Skill bodies are not part of the always-loaded prompt.

## Persistence and recovery

A production implementation should persist the append-only event log and rebuild `RuntimeRunState` from committed events. A crash during an open action must be represented as interrupted/recovery state; it must not erase committed calls or pretend the action never happened.

Persistence providers are replaceable. Event truth, replayability, sequence monotonicity, and authorization semantics are not.

## Relationship to Engineering Loops

Runtime state and Engineering Loop state solve different problems:

- Runtime state: what the Agent runtime actually saw, requested, executed, and recorded.
- Loop state: whether an engineering objective is verified, regressed, blocked, approved, or complete.

A Runtime event can provide observations to a Loop, but it does not self-certify the Loop terminal state.

## Reference implementation

```bash
python -m unittest discover -s tests
python -m compileall runtime scripts hooks adapters loops
```
