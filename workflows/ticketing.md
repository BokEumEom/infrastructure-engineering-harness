# MCP Ticketing Workflow

```text
Engineering Analysis
      ↓
Ticket Request
      ↓
Schema Validation
      ↓
Policy Decision
      ↓
Fingerprint
      ↓
Search Existing via MCP
      ├─ found → update/comment
      └─ not found
              ↓
      manual approval OR policy auto-create
              ↓
          MCP create tool
              ↓
       Ticket ID / URL returned
```

## Safety boundary

Ticket creation is allowed as a workflow action when policy permits, but it must not imply authorization to execute infrastructure changes. A Jira or Linear ticket can request a production change; execution still follows `workflows/change-proposal.md` and independent approval controls.

## Automatic creation

Automatic creation should be narrow and deterministic. Recommended candidates:

- SEV1/SEV2 incident follow-up with sufficient evidence
- failed deployment requiring tracked remediation
- repeated SLO violation where policy explicitly requires a work item

Recommended manual candidates:

- FinOps optimization opportunities
- architecture refactors
- capacity changes without immediate reliability impact
- low-confidence hypotheses

## Dedup

Search-before-create is mandatory. The request's `source_ref` is the primary human-readable key; the SHA-256 harness fingerprint is the secondary stable identifier.
