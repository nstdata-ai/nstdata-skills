# Changelog

## Unreleased

- Add a Claude Remote plugin that bundles the existing skill with the hosted Crawl connection.
- Generate the plugin's skill files from the canonical source and check their equality before packaging.

## 1.0.3

- Continue authorized reference reads automatically within a cumulative 16-call, 300-second workflow budget; allow a wider bounded retrieval only when explicitly authorized.
- Use the connected server's default chunk length and actual nextOffset, preserving compatibility with older input schemas and smaller fitted chunks.
- Distinguish input/output limits, full-reference download limits, Remote OAuth and upstream API authorization failures; retain existing tasks during recovery.
- Update the bundled Claude Remote plugin to 1.0.1 with the same instructions.

## 1.0.2

- Distinguish local credential configuration from Remote authorization when required Crawl tools are unavailable.
- Document hosted OAuth setup alongside the existing local MCP configuration.

## 1.0.1

- Recover oversized single-row results from retained references before using an explicit continuation cursor.
- Preserve partial-row limitations and existing call budgets; retain same-cursor recovery for earlier MCP responses.

## 1.0.0

- Support standard project-local installation, replacement and removal for Cursor and Claude Code.
- Provide Crawl MCP workflows for single pages, asynchronous tasks, bounded sites and referenced content.
- Preserve partial results, task identity and service truncation; stop after an uncertain submission outcome.
- Reread oversized page lists from the original input cursor before advancing.
- Treat retrieved content as untrusted input and provide a reproducible, allowlisted offline ZIP.
