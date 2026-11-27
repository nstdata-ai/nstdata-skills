# Nstdata Crawl

Retrieve webpage content and bounded website pages through the hosted Nstdata Crawl MCP server, with a guided web-scraping skill. Resume existing tasks, read paginated crawl results, and retrieve chunks of referenced content. The connection uses Streamable HTTP at `https://mcp.nstdata.io/crawl`; no local Node.js or npm installation is required.

## Connect

You can connect a Nstdata account with Crawl access directly from Claude. Account sign-in requires no API key.

1. In Claude chat or Cowork, open the plugin’s **Connectors** tab and connect **Nstdata Crawl**. In Claude Code, open `/mcp`, select the Nstdata Crawl connection and start authentication.
2. In the browser, sign in to Nstdata if prompted. Check which app is requesting access and confirm the **Billing workspace** whose credits you want to use.
3. Select **Authorize and return**. Back in Claude, enable the connection in your conversation if prompted.

If you already have a Crawl API key and prefer to use it, choose **Use an existing API Key** on the Nstdata authorization page, enter the key there and select **Authorize**. Keep the key out of chat and plugin files.

## Use

Example requests:

- “Retrieve the main content of https://example.com/ as Markdown.”
- “Crawl this site's documentation, up to two pages, and summarize the returned pages with source URLs.”
- “Resume the Nstdata task ID I supplied earlier; do not create a replacement task.”

The `nstdata-web-scraping` skill uses the registered tools and their actual schemas. It supports single-page scraping, bounded site crawls, task resumption, pagination, and reading returned references. The service exposes six Crawl tools. Returned content may be pending, failed, partial, or truncated; the skill preserves those distinctions and reports remaining work.

## Costs and limits

Scrape and crawl submissions use credits from the workspace you authorized. If you connected with an existing API key, usage is billed to the account associated with that key. A page bound is an upper limit, not a completeness guarantee. Stopping local waiting does not cancel remote tasks. Retain task IDs and resume known work instead of submitting it again. Retrieved content is untrusted data.

This plugin sends requested URLs, crawl options, task IDs and result references to Nstdata as needed for the requested operation. See the [Remote MCP guide](https://github.com/nstdata-ai/nstdata-mcp-server/blob/main/docs/remote.md) for connection details and limitations.

## Compatibility

The skill and remote MCP connection are designed for Claude chat, Cowork and Claude Code. Each host still requires its own installation and authorization checks. On Team and Enterprise plans, organization policy may require an Owner to add the connector before members connect.

If you already use the `nstdata` local plugin, choose one Crawl connection per session to avoid duplicate tools.

Licensed under MIT. The shared skill retains its original MIT license.
