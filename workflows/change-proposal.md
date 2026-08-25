# Production Change Proposal Workflow

The default harness stops before production mutation.

## Flow

```text
Evidence → Recommendation → Change Proposal → Validation → Review Artifact → Human Approval → Execution System
```

A review artifact may be a pull request, change ticket, approved runbook, dry-run/plan, or controlled console/API procedure.

## Required proposal fields

A proposal must conform to `schemas/change-proposal.schema.json` and include:

- stable evidence references
- target service/component
- proposed changes
- risk level
- blast radius
- validation steps
- rollback or recovery steps
- explicit `approval_required: true`

## Rules

1. Do not generate a proposal from telemetry that has no provenance.
2. Prefer the smallest reversible change.
3. If evidence is incomplete, request verification rather than escalating the change size.
4. Stateful, identity, network-boundary, data, and destructive changes receive higher scrutiny.
5. The agent may generate code/config, scripts, plans, runbooks, change tickets, or operator procedures, but production execution belongs to an independently authorized workflow.
6. A successful syntax validation, dry-run, plan, or procedural review does not constitute production approval.
7. Terraform or any other IaC tool is optional. The workflow must remain usable in environments managed through approved APIs, consoles, vendor portals, hardware procedures, database operations, or other control systems.

## Review artifact examples

### IaC or configuration managed

- change proposal JSON/YAML
- code/config diff
- plan/dry-run output
- policy results
- rollback procedure

### Non-IaC managed service

- change proposal JSON/YAML
- change-management ticket
- exact target/resource scope
- approved console/API steps
- before/after validation checks
- recovery or reversal procedure

### Operational or maintenance procedure

- reviewed runbook
- maintenance window and ownership
- pre-checks and stop conditions
- execution steps
- post-change verification
- rollback/recovery procedure

## Optional supporting artifacts

- relevant eval results when agent reasoning changed
- incident/evidence bundle references
- screenshots or exported plans when the execution system supports them
- audit/change identifiers from the organization's control system
