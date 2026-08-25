# Capability Routing Example

Request:

> Build a containerized public API with a CI/CD pipeline, vendor-neutral telemetry and an operational runbook. Do not execute production changes.

Expected routing:

```text
1. architecture-review / sre-review
   → decide topology, dependencies, objectives and constraints

2. capability-routing
   → select only the needed implementation references
      - kubernetes-ops
      - helm-charts
      - github-actions or gitlab-ci (based on actual repository context)
      - opentelemetry
      - runbook-creation

3. generate local artifacts
   → manifests/chart/config/pipeline/runbook

4. validate locally
   → syntax/schema/tests/policy checks that are actually available

5. change-review
   → evidence, blast radius, validation, rollback/recovery, approval

6. execution
   → outside the default agent authority

7. change-validation loop
   → verify the real outcome after authorized execution
```

If the source control system is unknown, the agent must not select GitHub Actions or GitLab CI by guess. It should keep the delivery capability unresolved until repository evidence identifies the platform.
