# Production infrastructure policy

## Principles

1. Protect availability and data integrity before optimizing cost.
2. Prefer reversible changes with explicit rollback paths.
3. Production mutations require human-reviewed workflows.
4. Avoid burstable instance families for sustained, high-criticality database workloads unless there is documented evidence that the workload profile is appropriate.
5. Architecture changes should be recorded as ADRs.

## Prohibited direct actions

Agents must not directly:

- apply or destroy Terraform in production
- delete production cloud resources
- mutate production databases
- broaden IAM permissions
- bypass protected deployment workflows

## Change evidence

A production change proposal should include:

- observed evidence
- expected benefit
- risk and blast radius
- validation steps
- rollback plan
