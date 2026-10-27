# Contributing

Keep instructions consistent with actual Nstdata MCP schemas.

Add a focused workflow scenario when changing creation, recovery or continuation rules; never use real credentials or unapproved external targets in tests.

Use Python 3.9+ with the standard library:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

The builder writes the optional `nstdata-web-scraping-1.0.0.zip` to `dist/` and prints its SHA-256. Keep `VERSION`, the artifact filename and CHANGELOG aligned. Packaging tests verify reproducibility and extraction; they do not execute a model or the MCP server.

Verify the standard installer with Node.js 24 and `skills@1.7.4`:

```sh
installer_dir="$(mktemp -d)"
npm install --prefix "$installer_dir" --ignore-scripts --no-audit --no-fund skills@1.7.4
NSTDATA_SKILLS_CLI="$installer_dir/node_modules/skills/bin/cli.mjs" \
  python3 -m unittest discover -s tests -v
```

The installer tests use disposable project directories and isolated installer state, with telemetry disabled. They verify Cursor/Claude Code installation, exact installed contents, replacement/removal and preservation of unrelated files and MCP configuration. No host application, MCP credentials or Crawl requests are used. Without `NSTDATA_SKILLS_CLI`, these tests are explicitly skipped. CI supplies the installer and runs them.

The repository's direct `nstdata-web-scraping/` child is discoverable by the standard installer. Only that skill directory is installed; repository-level CI, tests, packaging scripts and local `dist/` output are not skill payload. Keep the source directory and optional ZIP contents identical.

Validate changed tool sequences separately against the exact installed MCP version using synthetic/loopback responses, then record the host version for actual host acceptance.

The selected single-page workflow has manual Cursor acceptance. For changes affecting another workflow, verify that workflow in the intended host; Claude Code acceptance remains deferred. Record host/version attribution and limitations separately from packaging and protocol tests.

Packaging must remain allowlisted and deterministic.

Report security issues without secrets or captured customer content.

## Local checkout

Run the same installer from the target project, passing the absolute path of this repository as the source:

```sh
cd /ABSOLUTE/PATH/TO/TARGET_PROJECT
npx skills add /ABSOLUTE/PATH/TO/nstdata-skills --skill nstdata-web-scraping --agent cursor --yes
```

Use `--agent claude-code` for Claude Code. The skill installer does not install or reconfigure MCP; use the client configuration in the [README](README.md#2-connect-nstdata-mcp).

When replacing a manual installation in another discovery directory, back it up and remove that old copy to avoid duplicate discovery. Keep unrelated skills, local customizations and existing MCP configuration.

The optional ZIP contains only `nstdata-web-scraping/SKILL.md`, `LICENSE` and `references/continuation.md`; extract it under the target client's skill discovery directory only when standard installation is unavailable.
