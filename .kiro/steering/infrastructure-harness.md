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
- Security → `domains/security/README.md`

Use multiple packs for cross-domain decisions and state trade-offs explicitly.

When a reviewed decision must become concrete build or operations artifacts, use `skills/capability-routing/SKILL.md` and `capabilities/registry.yaml`. Select the minimum relevant capabilities. Third-party `pinned_reference` skills are reference material only: use the registered immutable revision and never automatically execute their scripts, commands or assets.

Evidence before action. Prefer read-only live evidence. Datadog, Terraform, a particular cloud, Kubernetes, or a particular runtime are optional. Production execution remains outside the default reasoning loop and capability routing does not grant execution authority.
