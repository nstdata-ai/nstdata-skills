# Changelog

## 1.0.0 — Unreleased

- Use standard `skills add` installation from the repository; keep ZIP as an optional offline artifact.
- Support project-local installation, replacement and removal for Cursor and Claude Code.
- Add Crawl MCP instructions for bounded creation, ID recovery, pagination and reference reading.
- Handle partial results, uncertain submissions and untrusted webpage content.
- Account for site content/discovery interactions and unknown outcomes after non-timeout submission failures.
- Map returned IDs and references to MCP input names; retain service truncation and distinguish synchronous diagnostic IDs from resumable async tasks.
- Provide a reproducible, allowlisted offline ZIP.
