---
inclusion: always
---

# Infrastructure Engineering Harness

Use the repository root `AGENTS.md` as the primary operating contract.

Resolve the context root from the user's request. Use `.infra-context/` in embedded mode or `contexts/<scope>/` in central mode.

Before making recommendations, route the task to the relevant domain pack:

- Infrastructure Engineering → `domains/infrastructure/README.md`
- SRE → `domains/sre/README.md`
- DevOps / Software Delivery → `domains/devops/README.md`
- FinOps → `domains/finops/README.md`

Use multiple packs for cross-domain decisions and state trade-offs explicitly.

Evidence before action. Prefer read-only live evidence. Datadog, Terraform, a particular cloud, or a particular runtime are optional. Production execution remains outside the default reasoning loop.
