# Memory, Prompt Performance, and Skill Release Control

These runtime capabilities strengthen the Infrastructure Engineering Agent without adding more always-loaded prompt rules or rebuilding provider-specific runtimes inside the core.

## 1. Persistent user / session memory

Memory is external runtime state. It is **not** Organizational Knowledge, Evidence, or a Verified Fact.

```text
User / Session activity
        ↓
PersistentMemoryStore (SQLite reference)
        ↓
permission + TTL + scope filtering
        ↓
Context Assembly
        ↓
model-visible memory as contextual data
```

Two scopes are supported:

- `user` — durable preferences or explicit operator-level context;
- `session` — working context and task checkpoints that survive process/context restarts.

Rules:

- the model cannot directly persist `user` memory;
- model writes are limited to `session` memory;
- user or trusted runtime can persist user preferences;
- user or trusted runtime can `forget` memory;
- expired/deleted records are not returned;
- obvious secret-like fields are rejected;
- memory never becomes independent engineering truth merely because it is stored.

This is intentionally separate from:

- Organizational Knowledge — Service Catalog, ADR, Policy, Runbook;
- Evolution Knowledge — Skill/Harness learning, rejected changes, negative corpus;
- Evidence — current provider/tool observations.

### Memory scope boundary

The project should **not** grow `runtime/memory.py` into a generic memory framework that duplicates a model/provider runtime.

The local layer owns only infrastructure-specific memory policy and the provider-neutral storage contract:

```text
Memory Contract
    ├─ scope / permission
    ├─ retention / forget
    ├─ secret / sensitive-data filtering
    └─ epistemic classification
          ↓
Replaceable Store / Runtime Adapter
```

Commerce Agents remains a reference for useful mechanisms such as tier-one facts, recall-on-demand, post-turn extraction, purge-safe writes, and stronger write filtering. Those mechanisms should be adopted only where they improve this Agent's memory contract; they should not cause a second full Commerce memory runtime to be recreated here.

## 2. Prompt caching and latency

`runtime/context_assembly.py` keeps context in three deterministic tiers:

```text
global stable context
        ↓
session stable context
        ↓
volatile per-turn context
```

The first two tiers form a stable prefix. Live evidence and per-turn user state stay in the volatile suffix so they do not unnecessarily invalidate a provider prompt cache.

The runtime computes a stable-prefix SHA-256 and approximate token counts for budgeting. These estimates are not billing truth.

`LatencyTracker` records:

- model turns;
- tool calls;
- model duration;
- tool-batch duration;
- input/output tokens;
- cache-read tokens;
- cache-write tokens;
- cache-read ratio.

`LatencyBudget` can flag excessive model turns, tool calls, or accounted latency.

### Core vs provider-specific optimization

The core owns the **layout and measurements**, not vendor request syntax:

```text
runtime/context_assembly.py
        ↓ provider-neutral
stable / session / volatile context
latency + cache telemetry contract
        ↓
Provider Optimization Adapter
        ├─ Anthropic cache breakpoints / rolling cache / eager dispatch
        ├─ OpenAI-specific request/context optimizations
        └─ other provider-specific mechanisms
```

Provider adapters may use their native features aggressively as long as they preserve the same Agent/Runtime safety contracts.

For example, Anthropic Commerce Agents demonstrates static-system and tool cache breakpoints, rolling conversation cache markers, eager tool dispatch, and history compaction. These are useful **Anthropic adapter references**, not reasons to add Anthropic-only `cache_control` fields to the provider-neutral core.

The optimization priority remains:

```text
reduce unnecessary model turns
        ↓
parallelize independent reads / serialize only where correctness requires it
        ↓
reduce unnecessary tool calls
        ↓
keep stable context cacheable
        ↓
apply provider-native optimization
        ↓
measure actual provider telemetry later
```

This layer does **not** claim that Claude, OpenAI, or another provider actually produced a cache hit until live telemetry proves it. Performance optimizations must never bypass evidence, provenance, authorization, approval, or independent verification.

## 3. Skill canary and kill switch

Skill rollout is runtime release state, not model judgment.

`runtime/release_control.py` supports:

- `active` — available normally;
- `canary` — exposed to a deterministic percentage of rollout keys;
- `disabled` — hard kill switch, removed from the model-visible Skill surface.

```text
Capability availability
        ↓
Invocation policy
        ↓
Release policy
 active / canary / disabled
        ↓
Runtime Skill Registry
        ↓
model-visible Skill catalog
```

Canary assignment is stable for a `(skill_id, rollout_key)` pair. A session/run therefore does not flap between treatment and control.

A disabled Skill cannot be re-enabled by:

- model request;
- prompt text;
- Skill body;
- retry;
- user intent routed through the model.

The host/runtime owns release policy.

`runtime/release-policy.yaml` defaults all locally managed and selected Runtime-reference Skills to active. Production environments may supply an environment-specific policy.

Design references such as Paperthin are **not** added to the Capability Registry merely so they can be disabled later. If a reference pattern is already absorbed into a local Skill, only the local Skill occupies Runtime surface area.

## Release workflow

A future live release process can use:

```text
candidate Skill revision
        ↓
Skill Lift / Harness Lift
        ↓
canary rollout
        ↓
live recording + outcome metrics
        ↓
expand / rollback / kill
```

Until live runners exist, canary behavior is a deterministic reference contract only. Checked-in tests verify routing and kill-switch behavior, not production effectiveness.
