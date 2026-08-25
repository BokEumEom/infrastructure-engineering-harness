# Jira via Atlassian Rovo MCP

Use the official Atlassian Rovo MCP Server rather than embedding Jira REST calls in the harness.

Current remote endpoint:

```text
https://mcp.atlassian.com/v1/mcp/authv2
```

Atlassian exposes Jira read, search and write tool groups. Relevant tools include:

- `getAccessibleAtlassianResources` — resolve `cloudId` first
- `getJiraProjectIssueTypesMetadata`
- `getJiraIssueTypeMetaWithFields`
- `searchJiraIssuesUsingJql`
- `getJiraIssue`
- `createJiraIssue`
- `editJiraIssue`
- `addCommentToJiraIssue`

## Recommended workflow

1. Resolve the accessible Atlassian resource/cloud ID.
2. Resolve project and issue-type metadata rather than guessing required fields.
3. Search by stable `source_ref` and harness marker before creating.
4. If found, add evidence/status as a comment or update approved fields.
5. If not found and ticket policy allows creation, call `createJiraIssue`.
6. Return the Jira issue key/URL to the calling channel.

## Permissions

Keep MCP permissions least-privileged. Ticket creation needs Jira write access; reading and dedup search need read/search permissions. Do not grant broader Jira/Confluence/Compass write access solely for ticket automation.

Atlassian MCP calls execute with the authenticated user's effective permissions and are subject to organization MCP controls and audit logging.

Official docs:

- https://support.atlassian.com/atlassian-ai-gateway/docs/set-up-clients/
- https://support.atlassian.com/atlassian-ai-gateway/docs/supported-tools/
