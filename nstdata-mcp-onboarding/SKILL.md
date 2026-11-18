---
name: nstdata-mcp-onboarding
description: Connect Codex, Cursor, Claude Code, or another compatible client to the hosted Nstdata Crawl MCP. Use when the user asks to add, authenticate, or verify the remote connection.
license: MIT
---

# Connect Nstdata Crawl MCP

Use `https://mcp.nstdata.io/crawl` with Streamable HTTP and browser OAuth. The hosted service runs remotely. The Nstdata API key comes from the [Nstdata dashboard](https://app.nstdata.io/) and is entered by the user on the Nstdata authorization page.

## Set up the active client

Identify the user's intended client and scope. Look for an existing Nstdata Crawl connection by URL or registered Crawl tools and reuse it. If it needs authentication, reconnect it. Preserve unrelated entries and flag a same-name entry with a different URL instead of overwriting it.

When the user asks to connect the service, use the active client's supported UI or command when available. If the user only asks how it works, explain the steps without changing configuration.

| Client | Add the connection | Authenticate and check |
| --- | --- | --- |
| Codex | Run `codex mcp add nstdata-crawl --url https://mcp.nstdata.io/crawl` or add that URL in the MCP settings. The CLI registers it in the user's Codex configuration. | Complete the browser flow if it opens. For a saved connection that still needs authorization, use the client's authentication control or `codex mcp login nstdata-crawl`. |
| Cursor | Add the entry below to the current project's `.cursor/mcp.json`, or use the MCP settings. Use the global configuration only if the user wants it across projects. | Open MCP settings, select the new connection, and follow its OAuth prompt. |
| Claude Code | In the target project, run `claude mcp add --transport http --scope local nstdata-crawl https://mcp.nstdata.io/crawl`. Use `--scope user` when requested across projects. | Open `/mcp` in Claude Code and authenticate there. |
| Claude chat or Cowork | In a client that supports custom connectors, add the hosted URL through Connectors, or use the [Nstdata Crawl plugin](https://github.com/nstdata-ai/nstdata-skills/tree/main/plugins/nstdata-crawl) if available. | Complete the connector's OAuth flow and enable it in the intended conversation. |
| Other client | Use its custom MCP settings to add the hosted URL as a Streamable HTTP server with OAuth. | If the host lacks a required control, report the specific remaining action for the user. |

For Cursor, merge this entry into the existing `mcpServers` object:

```json
{
  "mcpServers": {
    "nstdata-crawl": {
      "url": "https://mcp.nstdata.io/crawl"
    }
  }
}
```

Use the OAuth URL issued by the client and let the user review the requesting app and enter the key on the official Nstdata page at `https://mcp.nstdata.io`. Leave manual authorization headers and bearer-token fields empty. Keep keys, tokens and OAuth callbacks out of chat, commands, logs and repository files.

## Verify that the connection is ready

Check the connection in the intended session. If the host requires a new conversation or reload to expose its tools, do that or tell the user which action is required. Look for the six Crawl tools through the active client's tool discovery. Host prefixes can vary:

- `nstdata_crawl_scrape` and `nstdata_crawl_scrape_result`
- `nstdata_crawl_start`, `nstdata_crawl_status`, and `nstdata_crawl_pages`
- `nstdata_crawl_read_result`

Report whether configuration is saved, OAuth is complete, and the tools are visible. Tool discovery is the default setup check. Run a live Crawl request only if the user also requested one, since it can consume credits. For ongoing crawl workflows, use [`nstdata-web-scraping`](https://github.com/nstdata-ai/nstdata-skills/tree/main/nstdata-web-scraping) if available.

[Official hosted MCP guide](https://github.com/nstdata-ai/nstdata-mcp-server/blob/main/docs/remote.md)
