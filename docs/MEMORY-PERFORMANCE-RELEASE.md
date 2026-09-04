# Memory, Prompt Performance, and Skill Release Control

These runtime capabilities strengthen the Infrastructure Engineering Agent without adding more always-loaded prompt rules.

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

This layer is provider-neutral. It does **not** claim that Claude, OpenAI, or another model provider actually produced a cache hit until live provider telemetry proves it.

The optimization priority is:

```text
reduce unnecessary turns
        ↓
reduce unnecessary tool calls / serialize only when required
        ↓
keep stable context prefix cacheable
        ↓
measure real provider latency/cache telemetry later
```

Performance optimizations must not bypass evidence, provenance, authorization, or verification.

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

`runtime/release-policy.yaml` defaults all Skills to active. Production environments may supply an environment-specific policy.

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
