# MCP-first Ticketing Action Adapter

Ticketing is a **workflow write**, not a production infrastructure write. The harness can create Jira or Linear work items, but it does not call their REST/GraphQL APIs directly.

Instead:

```text
Harness Decision / Change Proposal
              ↓
        Ticket Request
              ↓
      Policy + Dedup Gate
              ↓
        MCP Tool Discovery
              ↓
   Jira Rovo MCP / Linear MCP
              ↓
      Search → Create/Update
```

## Why MCP-first

- one integration model across Codex, Kiro, Claude Code and other MCP clients
- OAuth and provider permissions stay with the official remote MCP server
- provider APIs are not coupled to harness reasoning logic
- tool availability and permissions can be discovered at runtime
- the same policy layer can work with future ticketing MCP providers

## Required behavior

1. Build a request conforming to `schemas/ticket-request.schema.json`.
2. Evaluate `schemas/ticket-policy.schema.json` before any write tool call.
3. Compute a stable fingerprint using `ticket_fingerprint()`.
4. Search for an existing ticket using `source_ref` and, when practical, the fingerprint marker.
5. If a matching ticket exists, update/comment instead of creating a duplicate.
6. Create only when the policy result is `auto_create`, or when it is `manual` and a human explicitly requests creation.
7. Include evidence references and a plain-text marker in the ticket body:

```text
[infra-harness:source=INC-2026-014]
[infra-harness:fingerprint=<sha256>]
```

8. Never auto-approve unrelated or high-impact MCP write tools.

## Modes

- `disabled`: no ticket write is allowed.
- `manual`: analysis may prepare a ticket request, but a person must explicitly request creation.
- `policy`: matching rules may return `auto_create`; unmatched work falls back to `default_action`.

A sensible default is to auto-create only well-evidenced high-severity incident work and keep FinOps optimization or architecture follow-up in manual mode.

## Deduplication

The stable fingerprint is derived from provider + source reference + service + kind. A runtime may also persist provider ticket IDs in an external state store. The harness itself does not require a state database.

Search-before-create remains mandatory even when policy allows automatic creation.
