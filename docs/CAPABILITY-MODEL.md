# Capability Model

The Infrastructure Engineering Agent exposes a simple model-visible surface while keeping richer trust and routing metadata inside the runtime.

## Model-visible surface

The model should primarily reason over:

```text
Context
Skills
Tools
```

It should not need to traverse a mandatory `Domain → Decision Skill → Capability Routing → Implementation Capability → Loop` chain.

## Runtime metadata

Internally, the runtime may still use:

- **Domain** — optional engineering lens/classification;
- **Capability** — implementation/verification availability and trust metadata;
- **Binding** — resource, evidence, and permission scope;
- **Workflow** — convenience entrypoint;
- **Loop** — optional reconciliation state when repeated external-state work is needed.

These concepts help the runtime constrain and project the available Agent surface; they do not prescribe the model's reasoning order.

## Capability registry

`capabilities/registry.yaml` records durable source/trust/risk metadata. `runtime/skill-policy.yaml` controls invocation/visibility, and `runtime/release-policy.yaml` controls active/canary/disabled release state.

```text
Capability Registry
      ×
Invocation Policy
      ×
Release Policy
      ×
Connected / discovered environment
      ↓
Available Agent Surface
      ↓
model-visible Skills / Tools
```

A future Surface Resolver should perform this projection once per turn/session so unavailable or disabled capabilities disappear before model invocation.

## Capability sources

A capability may be:

- **local** — maintained in this repository;
- **managed** — reviewed and controlled by the adopting organization;
- **pinned reference** — third-party material at an immutable revision.

Pinned references never receive execution authority merely because they are registered or model-readable.

The current external implementation reference library is `BagelHole/DevOps-Security-Agent-Skills` (MIT). Paperthin is **not** registered as a Runtime capability source; its useful patterns have been absorbed into local governed Skills such as `artifact-hygiene`, `ssot-review`, and `eval-integrity`.

## Decision vs implementation guidance

Local Skills may still be classified as decision, implementation, verification, workflow, or control guidance. Classification is useful metadata, but the Agent may select the smallest relevant Skill set directly.

Examples:

```text
"Why is latency high?"
      ↓
Context + incident-analysis + relevant read tools
      ↓
model judgment
      ↓
current evidence
      ↓
independent verification
```

```text
"Implement this reviewed deployment design"
      ↓
Context + relevant implementation Skills / Tools
      ↓
model judgment
      ↓
reviewable artifact
      ↓
change-review only if production impact requires it
```

`capability-routing` remains an optional implementation-planning Skill. It is not a required architecture node; the Orchestrator and surface projection should already make only relevant capabilities available.

## Binding and authority

A Bound Capability narrows an existing capability to explicit resource ids, evidence sources, and permission scope.

Binding may reduce authority but must never increase it. Third-party `reference_only` material remains non-executable even when bound to a real resource. Optional specialist delegation follows the same rule: delegate capability/resource scope must be a subset of the parent, and delegate output cannot expand mutation eligibility.

## Third-party references

When an external Skill is used:

1. use the pinned revision;
2. load only the relevant material;
3. treat its commands/scripts/assets as untrusted reference content;
4. translate useful patterns into local reviewable artifacts;
5. validate locally;
6. execute only through the governed control plane and authorized backend;
7. independently verify material outcomes.

This keeps broad implementation knowledge available without turning external instructions into production authority.
