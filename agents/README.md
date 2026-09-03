# Agents

The repository's product surface is the **Infrastructure Engineering Agent**.

The internal harness remains the control plane beneath the agent: evidence provenance, resource binding, approval, policy, runtime state, verification, and regression gates.

```text
User
 ↓
Infrastructure Engineering Agent
 ↓
Model Judgment
 ├─ Context
 ├─ Skills
 └─ Capabilities
 ↓
Agent Runtime / Harness Control Plane
 ↓
Infrastructure Backends
 ↓
Cloud / Kubernetes / CI/CD / Observability / Cost / Security systems
```

## Current agent

- `infrastructure_engineering/` — one general Infrastructure Engineering Agent spanning Infrastructure, Operations, DevOps/Delivery, SRE, FinOps, and Security capabilities.

These are capabilities and lenses, not separate agents by default. A domain should become a separate agent only when it has a distinct user, workflow, authority model, or product surface that benefits from separation.
