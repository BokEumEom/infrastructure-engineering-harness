# MCP connections

The harness is designed to consume official remote MCP servers when a provider offers them. Credentials and OAuth sessions belong to the MCP client/provider, not this repository.

## Linear

Remote read/write endpoint:

```text
https://mcp.linear.app/mcp
```

Read-only endpoint:

```text
https://mcp.linear.app/mcp/readonly
```

Claude Code:

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

Codex:

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
```

## Atlassian Rovo MCP

Current remote endpoint recommended by Atlassian:

```text
https://mcp.atlassian.com/v1/mcp/authv2
```

Configure this URL in the MCP client and complete the provider authentication flow. Atlassian organization policies may restrict MCP access and tool groups.

## Kiro workspace example

Kiro supports remote HTTP MCP servers in `.kiro/settings/mcp.json`. Do **not** auto-approve write tools by default.

```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp",
      "disabled": false,
      "autoApprove": []
    },
    "atlassian": {
      "url": "https://mcp.atlassian.com/v1/mcp/authv2",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

For organization-managed Kiro environments, MCP registry policy can further constrain which servers are available.

## Principle

MCP is the integration boundary; Domain Packs and reasoning remain provider-neutral.
