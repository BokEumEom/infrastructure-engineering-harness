# Production Change Proposal Workflow

The default harness stops before production mutation.

## Flow

```text
Evidence → Recommendation → Change Proposal → Validation/Plan → PR → Human Approval → Deployment System
```

## Required proposal fields

A proposal must conform to `schemas/change-proposal.schema.json` and include:

- stable evidence references
- target service/component
- proposed changes
- risk level
- blast radius
- validation steps
- rollback steps
- explicit `approval_required: true`

## Rules

1. Do not generate a proposal from telemetry that has no provenance.
2. Prefer the smallest reversible change.
3. If evidence is incomplete, request verification rather than escalating the change size.
4. Stateful, identity, network-boundary, and destructive changes receive higher scrutiny.
5. The agent may generate code/config and a plan, but production execution belongs to an independently authorized workflow.
6. A successful syntax validation or plan does not constitute production approval.

## Recommended PR artifacts

- change proposal JSON/YAML
- code/config diff
- dry-run/plan output
- policy results
- relevant eval results when agent reasoning changed
- rollback command/procedure owned by the deployment system
