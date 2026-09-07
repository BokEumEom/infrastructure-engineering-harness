# Workflow Surface

The **Infrastructure Engineering Agent** is the user-facing product. Every channel converges on the same **Agent Orchestrator / Turn Runtime**; the internal Harness / Control Plane provides evidence, permission, approval, audit, and verification boundaries.

## Entry surfaces

```text
CLI / Web / Slack / GitHub / MCP / API
                 ↓
          normalized TurnRequest
                 ↓
      Agent Orchestrator / Turn Runtime
                 ↓
     Infrastructure Engineering Agent
```

Natural language is the primary interaction model. Convenience intents may include:

```text
incident
reliability
delivery
finops
security
change
learn
```

These are discovery/routing hints, not separate Agents or mandatory reasoning pipelines.

## Turn model

```text
TurnRequest
    ↓
Context Resolver + Available Surface
    ↓
Model Judgment
  ↙          ↘
Skills      Tools
  ↘          ↙
   new evidence / result
           ↓
      model continuation
           ↓
Independent Verification
      ↙             ↘
    done       reconcile if needed
                    ↓
             Engineering Loop
```

A one-shot review or analysis normally ends after verification. Engineering Loops activate only when repeated observation/reconciliation against external state materially helps.

## Available Agent Surface

Users and models should not need to reason about every internal registry layer. The Orchestrator/runtime should project the currently relevant surface from:

```text
Capability Registry
× Invocation Policy
× Release Policy
× connected/discovered environment
× permission/resource scope
        ↓
Context + Skills + Tools
```

Domain, Capability, Binding, and Workflow remain useful runtime metadata but do not prescribe the reasoning order.

`capability-routing` is an optional implementation-planning Skill, not a mandatory hop.

## Suggested intent metadata

| Intent | Typical task profile | Typical local Skills |
| --- | --- | --- |
| incident | incident | incident-analysis, sre-review |
| reliability | incident/reliability | sre-review, architecture-review |
| delivery | delivery | delivery-review, change-review |
| finops | finops | finops-review, architecture-review |
| security | security | security-review, change-review |
| change | change | change-review, architecture-review |
| learn | governance | loop-engineering, artifact-hygiene, eval-integrity |

Mappings are recommendations for progressive disclosure only. The Agent may select a smaller or different relevant Skill/Tool set while the hard control-plane boundaries remain unchanged.

## Optional delegation

The Infrastructure Engineering Agent remains single by default. A specialist delegate may be used only when measured complexity justifies handoff cost.

Delegation must:

- remain read-only by default;
- stay within parent capability and resource scope;
- never grant production authority;
- never make newly named resources mutation-eligible.

## No implicit authority

Routing, a Skill, a channel, or a delegate never grants permission.

A user request such as "fix production" can cause the Orchestrator to prepare a change path, but production mutation still requires provenance, independently owned authorization, exact staged revision approval, apply-time revalidation, and independent outcome verification.
