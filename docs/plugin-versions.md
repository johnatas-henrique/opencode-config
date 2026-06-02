# Plugin & Tool Versions

> **How to update:** Plugins with `@latest` auto-update on OpenCode restart.
> To force update: restart OpenCode. To check latest: `npm view <pkg> version`.

## OpenCode Plugins (opencode.jsonc)

| Plugin                               | Config Tag | Latest Release | Last Checked |
| ------------------------------------ | ---------- | -------------- | ------------ |
| @cortexkit/aft-opencode              | @latest    | 0.33.0         | 2026-05-30   |
| @cortexkit/opencode-magic-context    | @latest    | 0.21.8         | 2026-05-30   |
| @franlol/opencode-md-table-formatter | @latest    | 0.0.6          | 2026-05-30   |
| @gotgenes/opencode-agent-identity    | (no tag)   | 3.1.1          | 2026-05-30   |
| @johnatas-henrique/opencode-hooks    | @latest    | 0.8.0          | 2026-05-30   |
| opencode-handoff                     | (no tag)   | 0.5.0          | 2026-05-30   |
| agentmemory-capture.ts               | local      | —              | —            |

## TUI Plugins (tui.json)

| Plugin                            | Config Tag | Latest Release | Last Checked |
| --------------------------------- | ---------- | -------------- | ------------ |
| @guard22/opencode-status-signals  | @latest    | 0.3.4          | 2026-05-30   |
| opencode-sidechat                 | (no tag)   | —              | —            |

## MCP Servers (opencode.jsonc)

| Server      | Command                           | Version Source    |
| ----------- | --------------------------------- | ----------------- |
| context7    | remote                            | N/A (remote)      |
| exa         | remote                            | N/A (remote)      |
| gh_grep     | remote                            | N/A (remote)      |
| playwriter  | `playwriter`                        | CLI version       |
| markitdown  | `uvx markitdown-mcp@latest`        | PyPI latest       |
| agentmemory | `npx -y @agentmemory/mcp`          | npm latest        |

## CLI Tools

| Tool  | Version | Location        | Status                     |
| ----- | ------- | --------------- | -------------------------- |
| rtk   | 0.40.0  | ~/.local/bin/   | ⚠️ Deprecated (replaced by AFT bash rewrite) |

## Core

| Package             | Version |
| ------------------- | ------- |
| @opencode-ai/plugin | 1.15.10 |

## Verification Commands

```bash
# Check npm latest for any package
npm view @cortexkit/aft-opencode version
npm view @cortexkit/opencode-magic-context version

# Check RTK
rtk --version

# Check agentmemory
npx @agentmemory/mcp --version 2>/dev/null || echo "check manually"
```
