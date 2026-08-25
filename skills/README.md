# Skill Model

The repository keeps all directly discoverable Agent Skills under `skills/` for cross-agent compatibility. Do not infer that every Skill has the same responsibility.

## Skill classes

- **Decision Skills** — determine what should change and why using organizational context and evidence.
- **Control Skills** — coordinate bounded repeated work and verification.
- **Workflow Skills** — create/review workflow artifacts such as tickets.
- **Implementation Capabilities** — technology-specific build/operate knowledge selected through `capabilities/registry.yaml`.
- **Verification Capabilities** — technology-specific checks such as supply-chain or access evidence.

Current local skills are primarily Decision, Control and Workflow Skills. Third-party implementation knowledge is registered separately so it does not flood every prompt or silently gain execution authority.

Use `capability-routing` when a task moves from an engineering decision to concrete build or operations implementation.
