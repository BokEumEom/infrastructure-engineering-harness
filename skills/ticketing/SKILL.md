---
name: ticketing
description: Create or update Jira/Linear work items through connected MCP servers after applying harness ticket policy and deduplication. Use when incident, change, SRE, DevOps, FinOps, or infrastructure analysis should become tracked work.
---

# MCP Ticketing

Use MCP ticketing as a controlled workflow write.

## Before writing

1. Produce a valid Ticket Request (`schemas/ticket-request.schema.json`).
2. Load the applicable ticket policy.
3. Compute the harness fingerprint.
4. Determine `disabled`, `manual`, or `auto_create`.
5. Discover the connected MCP server and available tools.
6. Search for existing work using `source_ref` and fingerprint before create.

## Jira

Prefer the official Atlassian Rovo MCP server. Resolve `cloudId` and issue metadata before creating. Use search/read tools for dedup and `createJiraIssue` only when policy permits.

## Linear

Prefer Linear's official remote MCP server. Discover issue search/create/update tools at runtime. Use the read-only MCP endpoint for analysis-only environments.

## Manual vs policy mode

- `manual`: show the proposed ticket and require explicit user intent before calling a write tool.
- `policy`: an `auto_create` result may create without another conversational confirmation, but only within the configured policy scope.
- `disabled`: do not call ticket write tools.

## Required ticket content

Include summary, service, domain lens, evidence references, risk/severity when relevant, validation/follow-up, source reference and fingerprint marker.

Never turn ticket creation permission into permission for production infrastructure mutation.
