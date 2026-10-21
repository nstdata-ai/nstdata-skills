# Nstdata Skills

[中文](README_zh.md)

Agent Skills for webpage retrieval, bounded site crawling and result continuation through Nstdata MCP.

## Install

Use Node.js 24. The repository and MCP package are prepared locally and have not been released; the GitHub/npm commands below are the publication path. Before publication, use the local-checkout command and your existing local MCP installation.

For Cursor, run in the project where you want to use the skill:

```sh
npx skills add nstdata-ai/nstdata-skills --skill nstdata-web-scraping --agent cursor --yes
```

For Claude Code, replace `--agent cursor` with `--agent claude-code`. The standard [skills CLI](https://github.com/vercel-labs/skills) discovers the skill and installs its files; downloading or extracting a ZIP is unnecessary. Installation is project-local by default. Cursor uses `.agents/skills/`; Claude Code uses `.claude/skills/`.

For a local checkout, run inside this repository:

```sh
npx skills add . --skill nstdata-web-scraping --agent cursor --yes
```

Rerun the same install command to replace this skill with the source version. Keep local customizations outside its directory. When migrating from a manual copy in another discovery location, remove that old copy to avoid loading the skill twice.

To remove the skill from the current project:

```sh
npx skills remove nstdata-web-scraping --yes
```

## Configure Nstdata MCP

The installer installs instructions, not the MCP server or credentials. Configure Nstdata MCP with Crawl enabled before using the skill. After the MCP package is published, the Cursor project configuration in `.cursor/mcp.json` is:

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

Keep the real token in protected local client configuration and outside version control. Preserve existing MCP entries. For Claude Code, register the same stdio server using its [MCP configuration](https://code.claude.com/docs/en/mcp). The MCP package and its dependencies must be publicly available before the npm entry can work.

## Use

Start a new host session and select `/nstdata-web-scraping`. For example:

> Retrieve https://example.com/ as Markdown. Submit once; if only a Markdown reference is returned, read it using the result-reading tool.

The skill discovers actual tool schemas, reuses existing task IDs, preserves source URLs and partial results, and bounds status, pagination and reference calls. It uses the existing authorization and cost limits.

| Host | Verification scope |
|---|---|
| Cursor | Standard project installation and the single-page scrape/readable-content workflow |
| Claude Code | Standard project installation; actual agent workflow acceptance pending |

Installation tests do not establish agent behavior in other hosts or workflows.

## Offline distribution

`nstdata-web-scraping-1.0.0.zip` remains an optional offline artifact. It contains only the skill instructions, continuation reference and license. Build and checksum instructions are in [Contributing](CONTRIBUTING.md).

[Cursor skills](https://cursor.com/docs/skills) · [Claude Code skills](https://code.claude.com/docs/en/skills) · [MIT license](LICENSE)
