# Linear via Official Remote MCP

Use Linear's official authenticated remote MCP server.

Read/write endpoint:

```text
https://mcp.linear.app/mcp
```

Linear also provides a read-only endpoint:

```text
https://mcp.linear.app/mcp/readonly
```

The read/write server exposes tools for finding, creating and updating Linear objects such as issues, projects and comments. Tool names should be discovered from the connected MCP server rather than hardcoded into harness core logic.

## Recommended workflow

1. Discover the available Linear MCP tools and target team/project.
2. Search for an existing issue using the `source_ref`, title and harness marker.
3. Update/comment on an existing issue when it represents the same work.
4. If no issue exists and policy allows creation, invoke the MCP issue-create tool.
5. Include evidence references and the harness fingerprint marker in the description.
6. Return the Linear issue identifier/URL to the calling channel.

For agents that only need analysis, connect the read-only MCP endpoint. Enable the read/write endpoint only for workflows that are allowed to create/update work items.

Official docs: https://linear.app/docs/mcp
