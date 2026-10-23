# Nstdata Skills

[中文](README_zh.md)

Retrieve webpage content through Nstdata Crawl MCP from an Agent Skills client.

## Capabilities

| Workflow | Behavior |
|---|---|
| Single page | Submit once and retrieve the requested content, including Markdown. |
| Async task | Resume an existing task by ID without submitting it again. |
| Bounded site crawl | Collect pages within the authorized scope and follow real pagination cursors. |
| Referenced content | Read returned references in chunks and report partial or truncated content. |

The skill supplies instructions. It uses your configured Nstdata MCP server and existing authorization; it does not install a server or provide API credentials.

## Get started

Requires Node.js 24, an Agent Skills client and a Nstdata Crawl API key. This repository and the MCP package are not yet published. The commands below apply after publication; local checkout verification is in [Contributing](CONTRIBUTING.md#local-checkout).

### 1. Install the skill

Run from the project where you want to use it:

```sh
npx skills add nstdata-ai/nstdata-skills --skill nstdata-web-scraping --agent cursor --yes
```

For Claude Code, replace `--agent cursor` with `--agent claude-code`. The standard [skills CLI](https://github.com/vercel-labs/skills) installs the required files without ZIP extraction. Installation is project-local: Cursor discovers `.agents/skills/`; Claude Code uses `.claude/skills/`.

### 2. Connect Nstdata MCP

If Crawl MCP is already configured, keep that configuration. Otherwise, after the MCP package and its dependencies are published, add this entry to the Cursor project's `.cursor/mcp.json`, preserving other entries:

```json
{
  "mcpServers": {
    "nstdata": {
      "command": "npx",
      "args": ["--yes", "@nstdata-ai/mcp-server@1.0.1"],
      "env": {
        "NSTDATA_MODULES": "crawl",
        "NSTDATA_API_TOKEN": "YOUR_CRAWL_API_TOKEN"
      }
    }
  }
}
```

The client must be able to find Node.js 24 and `npx`. Keep the real token in protected local client configuration outside version control. For Claude Code, register the same stdio server using its [MCP configuration](https://code.claude.com/docs/en/mcp).

### 3. Use the skill

Start a new client conversation and select `/nstdata-web-scraping`. For example:

> Retrieve https://example.com/ as Markdown. Submit once; if only a Markdown reference is returned, read it using the result-reading tool.

The agent follows the registered tool schemas, preserves source URLs and partial results, and bounds status, pagination and reference calls. Actual requests use your Nstdata account's quota.

## Update or remove

Rerun the install command to update the skill. Keep local customizations outside its directory. For a previous manual installation, see [migration](CONTRIBUTING.md#local-checkout).

Remove this skill's installations from the current project:

```sh
npx skills remove nstdata-web-scraping --yes
```

Other skills and MCP configuration are preserved.

## Client compatibility

Cursor has been verified for standard installation and a single-page scrape/content-reading workflow. Claude Code installation has been verified; its actual agent workflow remains unverified. Other Agent Skills clients need their own MCP configuration and verification.

[Cursor skills](https://cursor.com/docs/skills) · [Claude Code skills](https://code.claude.com/docs/en/skills) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)
