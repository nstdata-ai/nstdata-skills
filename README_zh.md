# Nstdata Skills

[English](README.md)

在支持 Agent Skills 的客户端中，通过 Nstdata Crawl MCP 获取网页内容。

## 功能

| 工作流 | 行为 |
|---|---|
| 单页抓取 | 只提交一次，读取 Markdown 等所需内容。 |
| 异步任务接续 | 使用已有任务 ID 继续查询，不重复提交。 |
| 有界整站抓取 | 在授权范围内收集页面，沿实际返回的游标分页。 |
| 引用正文读取 | 分块读取返回的引用，明确标注部分内容和服务截断。 |

Skill 提供操作指令，复用你已配置的 Nstdata MCP 和已有授权；不安装服务，也不提供 API 凭据。

## 快速开始

需要 Node.js 24、支持 Agent Skills 的客户端及 Nstdata Crawl API Key。仓库和 MCP 包尚未发布；下列命令在发布后使用，本地源码验证见[贡献说明](CONTRIBUTING.md#local-checkout)。

### 1. 安装 Skill

在实际使用 Skill 的项目中运行：

```sh
npx skills add nstdata-ai/nstdata-skills --skill nstdata-web-scraping --agent cursor --yes
```

Claude Code 将 `--agent cursor` 替换为 `--agent claude-code`。标准 [skills CLI](https://github.com/vercel-labs/skills) 自动安装所需文件，无需解压 ZIP。默认安装到当前项目：Cursor 从 `.agents/skills/` 发现 Skill，Claude Code 使用 `.claude/skills/`。

### 2. 连接 Nstdata MCP

已有 Crawl MCP 配置可直接复用。尚未配置时，在 MCP 包及其依赖发布后，将以下条目加入 Cursor 项目的 `.cursor/mcp.json`，保留其他已有条目：

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

客户端需能找到 Node.js 24 和 `npx`。真实 Token 保存在受保护的本地客户端配置中，不提交版本控制。Claude Code 按其 [MCP 配置说明](https://code.claude.com/docs/en/mcp) 注册同一 stdio 服务。

### 3. 使用 Skill

开启新的客户端对话，选择 `/nstdata-web-scraping`，例如：

> 将 https://example.com/ 读取为 Markdown。只提交一次；若仅返回 Markdown 引用，使用结果读取工具读取正文。

Agent 使用实际注册的工具 schema，保留来源 URL 和部分结果，并限制状态查询、分页及引用读取次数。真实请求使用你的 Nstdata 账号额度。

## 更新或移除

重新执行安装命令即可更新。自定义修改保留在 Skill 目录之外；旧手动副本的处理见[迁移说明](CONTRIBUTING.md#local-checkout)。

从当前项目移除该 Skill 的安装：

```sh
npx skills remove nstdata-web-scraping --yes
```

保留其他 Skill 和 MCP 配置。

## 客户端兼容性

Cursor 已验证标准安装和单页抓取／正文读取工作流。Claude Code 已验证安装，实际 Agent 工作流尚未验收。其他支持 Agent Skills 的客户端需自行配置 MCP 并验证。

[Cursor Skills](https://cursor.com/docs/skills) · [Claude Code Skills](https://code.claude.com/docs/en/skills) · [贡献说明](CONTRIBUTING.md) · [MIT 许可](LICENSE)
