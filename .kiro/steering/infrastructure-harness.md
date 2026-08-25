---
inclusion: always
---

# Infrastructure Harness Steering

Use the repository root `AGENTS.md` as the primary operating contract.

Infrastructure-specific knowledge lives in `.infra-context/`. Load it progressively rather than reading the entire directory.

For incidents and change reviews:

- evidence before action
- distinguish facts from assumptions
- prefer provider-neutral component categories
- use optional live adapters only for read-only evidence collection
- Datadog or any other observability product is optional
- production changes require the proposal workflow in `workflows/change-proposal.md`
- never treat an agent hook as the only production security boundary

When a recommendation depends on telemetry, include provenance that conforms to `schemas/evidence.schema.json`.
