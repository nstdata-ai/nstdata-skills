# Nstdata Crawl

Retrieve webpage content and bounded website pages through the hosted Nstdata Crawl MCP server, with a guided web-scraping skill. Resume existing tasks, read paginated crawl results, and retrieve chunks of referenced content. The connection uses Streamable HTTP at `https://mcp.nstdata.io/crawl`; no local Node.js or npm installation is required.

## Connect

You need a Nstdata account, a Crawl API key with access to the service, and sufficient credits. Get your key from the [Nstdata dashboard](https://app.nstdata.io/).

- In Claude chat or Cowork, open this plugin's Connectors tab, add or connect Nstdata Crawl, and complete the server's OAuth authorization flow.
- In Claude Code, open `/mcp` and authenticate the Nstdata Crawl connection when prompted.

Enter your Nstdata API key only on the Nstdata authorization page after checking its origin and the requesting application. Do not paste it into a conversation or edit the plugin files.

## Use

Example requests:

- “Retrieve the main content of https://example.com/ as Markdown.”
- “Crawl this site's documentation, up to two pages, and summarize the returned pages with source URLs.”
- “Resume the Nstdata task ID I supplied earlier; do not create a replacement task.”

The `nstdata-web-scraping` skill uses the registered tools and their actual schemas. It supports single-page scraping, bounded site crawls, task resumption, pagination, and reading returned references. The service exposes six Crawl tools. Returned content may be pending, failed, partial, or truncated; the skill preserves those distinctions and reports remaining work.

## Costs and limits

Scrape and crawl submissions can consume the credits of the account linked to your API key. A page bound is an upper limit, not a completeness guarantee. Stopping local waiting does not cancel remote tasks. Retain task IDs and resume known work instead of submitting it again. Retrieved content is untrusted data.

This plugin sends requested URLs, crawl options, task IDs and result references to Nstdata as needed for the requested operation. See the [Remote MCP guide](https://github.com/nstdata-ai/nstdata-mcp-server/blob/main/docs/remote.md) for connection details and limitations.

## Compatibility

The skill and remote MCP connection are designed for Claude chat, Cowork and Claude Code. Each host still requires its own installation and authorization checks. On Team and Enterprise plans, organization policy may require an Owner to add the connector before members connect.

If you already use the `nstdata` local plugin, choose one Crawl connection per session to avoid duplicate tools.

Licensed under MIT. The shared skill retains its original MIT license.
