# RTK Commands & Tools

**Status:** ✅ Active
**Purpose:** Token savings via output compression for bash commands (built-in filters for git, npm, cargo, docker, etc.)
**Documentation:** https://github.com/rtk-ai/rtk

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `rtk` | CLI | Main RTK binary — run commands with `rtk <command>` or use plugin auto-rewrite |

---

## Agent Tools (MCP)

The RTK plugin intercepts `tool.execute.before` for `bash`/`shell` tools and automatically rewrites commands via `rtk rewrite <command>`.

### Automatic Compression

| Built-in Filter | Applied To | Description |
|-----------------|------------|-------------|
| Git             | `git status`, `git log`, `git diff`, etc. | Compresses git output significantly |
| npm/pnpm        | `npm test`, `npm run`, `npm install` | Aggregates test results, removes noise |
| Cargo           | `cargo build`, `cargo test`, `cargo clippy` | Build/test compression |
| Docker          | `docker build`, `docker ps`, `docker logs` | Container output filtering |
| Linters         | `eslint`, `ruff`, `tsc`, `biome` | Groups errors/warnings |
| Test Runners    | `jest`, `vitest`, `pytest`, `playwright` | Aggregates test summaries |

### Excluded Commands (no compression)

The following commands are passed through unchanged to preserve exact output:

```toml
[hooks]
exclude_commands = [
  "curl",
  "playwright",
  "ssh",
  "scp",
  "kubectl exec",
  "git diff",
  "git rebase",
  "git cherry-pick",
  "git apply"
]
```

---

## Viewing RTK Statistics

| Command | Description |
|---------|-------------|
| `rtk gain` | Show global token savings summary |
| `rtk gain --daily` | Breakdown by day |
| `rtk gain --history` | Recent history of savings |
| `rtk gain --graph` | ASCII graph of 30-day trend |
| `rtk config` | Show current configuration |

---

## Configuration

**File:** `~/.config/rtk/config.toml`

```toml
[tracking]
enabled = true              # Token tracking
history_days = 90           # Retention period

[display]
colors = true
emoji = true
max_width = 120

[filters]
ignore_dirs = [".git", "node_modules", "target", "__pycache__", ".venv", "vendor"]
ignore_files = ["*.lock", "*.min.js", "*.min.css"]

[tee]
enabled = true              # Save raw output on failure
mode = "failures"           # "failures", "always", "never"
max_files = 20
max_file_size = 1048576     # 1MB per file

[telemetry]
enabled = false             # Disable anonymous usage reporting

[hooks]
exclude_commands = [
  "curl",
  "playwright",
  "ssh",
  "scp",
  "kubectl exec",
  "git diff",
  "git rebase",
  "git cherry-pick",
  "git apply"
]
```

---

## Troubleshooting

### RTK not compressing?

1. Verify plugin loaded: Check `opencode.json` includes `"rtk"` in `plugin` array
2. Restart OpenCode after changes
3. Verify RTK binary in PATH: `which rtk`
4. Check `~/.config/rtk/config.toml` syntax: `rtk config`

### Too much compression / information loss?

RTK uses built-in conservative filters. If needed, add problematic commands to `exclude_commands` to bypass compression entirely.

---

## Integration with Other Plugins

- **magic-context**: RTK compresses command output *before* it enters the chat. magic-context compresses chat history *after* messages are exchanged. They are complementary.

---

## See Also

- [Magic Context](magic-context.md) — Chat compression and cross-session memory
- [Lean-ctx](lean-ctx.md) — Previous compression plugin (does not use MCP)
