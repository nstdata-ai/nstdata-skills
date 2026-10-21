# Nstdata Skills

[English](README.md)

通过 Nstdata MCP 执行网页读取、有界整站抓取和结果接续。

## 安装

使用 Node.js 24。仓库和 MCP 包目前已本地准备、尚未发布；以下 GitHub/npm 命令用于发布后安装。发布前使用本地源码命令和已有的本地 MCP 安装。

Cursor：在需要使用 Skill 的项目中运行：

```sh
npx skills add nstdata-ai/nstdata-skills --skill nstdata-web-scraping --agent cursor --yes
```

Claude Code：将 `--agent cursor` 替换为 `--agent claude-code`。标准 [skills CLI](https://github.com/vercel-labs/skills) 自动发现并安装所需文件，无需下载或解压 ZIP。默认仅安装到当前项目：Cursor 使用 `.agents/skills/`，Claude Code 使用 `.claude/skills/`。

本地源码验收：在本仓库目录中运行：

```sh
npx skills add . --skill nstdata-web-scraping --agent cursor --yes
```

更新时重新执行同一安装命令，以源码版本替换该 Skill；自定义修改保留在其目录之外。从其他发现路径中的手动安装副本迁移时，先移除旧副本，避免重复加载。

从当前项目移除该 Skill：

```sh
npx skills remove nstdata-web-scraping --yes
```

## 配置 Nstdata MCP

安装器只安装指令，不安装 MCP 服务或配置凭据。使用前应已配置 Nstdata MCP 并启用 Crawl。MCP 包发布后，Cursor 项目的 `.cursor/mcp.json` 配置如下：

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

真实 Token 保留在受保护的本地客户端配置中，不提交版本控制；保留已有 MCP 条目。Claude Code 按其 [MCP 配置说明](https://code.claude.com/docs/en/mcp) 注册同一个 stdio 服务。上述 npm 入口生效的前提是 MCP 包及其依赖均已公开发布。

## 使用

开启新的宿主会话，选择 `/nstdata-web-scraping`，例如：

> 将 https://example.com/ 读取为 Markdown。只提交一次；若仅返回 Markdown 引用，使用结果读取工具读取正文。

Skill 使用实际发现的工具 schema，复用已有任务 ID，保留来源 URL 和部分结果，并限制状态查询、分页及引用读取次数；沿用已有授权和消耗边界。

| 宿主 | 验证范围 |
|---|---|
| Cursor | 标准项目安装、单页抓取及可读正文工作流 |
| Claude Code | 标准项目安装；实际 Agent 工作流待验收 |

安装测试不代表其他宿主或工作流中的 Agent 行为已验收。

## 离线分发

`nstdata-web-scraping-1.0.0.zip` 保留为可选离线产物，仅包含 Skill 指令、接续参考和许可。构建与校验值说明见[贡献说明](CONTRIBUTING.md)。

[Cursor Skills](https://cursor.com/docs/skills) · [Claude Code Skills](https://code.claude.com/docs/en/skills) · [MIT 许可](LICENSE)
