# Lean-ctx Commands & Tools

**Status:** ✅ Active (MCP server + shell hooks)
**Purpose:** Compression for shell output and file reads before they reach the LLM.
**Documentation:** https://leanctx.com

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `ctx_read(path, mode)` | MCP (Agent) | Smart file reading with 10 compression modes, caching |
| `ctx_shell(command, raw)` | MCP (Agent) | Execute shell commands with 90+ compression patterns |
| `ctx_search(pattern, path)` | MCP (Agent) | Regex code search with compact results |
| `ctx_tree(path, depth)` | MCP (Agent) | Compact directory tree listings |
| `ctx_edit(path, old, new)` | MCP (Agent) | Search-and-replace file editing |
| `lean-ctx -c "cmd"` | Bash CLI | Execute any shell command with compression |
| `lean-ctx read <file>` | Bash CLI | Read file with caching and compression |
| `lean-ctx grep <pattern>` | Bash CLI | Search code with compact output |
| `lean-ctx gain` | Bash CLI | View token savings and GainScore |
| `lean-ctx doctor` | Bash CLI | Verify installation and diagnose issues |

---

## MCP Tools (Agent Uses Automatically)

These tools replace native OpenCode tools and provide 60-99% token savings.

### Core File & Code Tools

| MCP Tool | Replaces | Savings | Description |
|----------|----------|---------|-------------|
| `ctx_read(path, mode)` | `Read`, `cat` | 74-99% | Smart file reads with 10 compression modes, caching, re-reads ~13 tokens |
| `ctx_multi_read(paths)` | multiple `Read` | fewer RTT | Batch read multiple files in one call |
| `ctx_tree(path, depth)` | `ls`, `find` | 34-60% | Compact directory tree listings |
| `ctx_shell(command, raw)` | `Shell`, `bash` | 60-90% | Shell commands with 90+ compression patterns |
| `ctx_search(pattern, path)` | `Grep`, `rg` | 50-80% | Regex code search with compact results |
| `ctx_edit(path, old, new)` | `Edit` | — | Search-and-replace editing (requires prior read) |

### Compression Modes (for ctx_read)

| Mode | Use Case | Token Cost |
|------|----------|------------|
| `full` | Files you will edit | 0% first read, ~99% subsequent |
| `map` | Dependencies + exports | ~10% |
| `signatures` | Function/class signatures | ~3% |
| `diff` | Changed lines since last read | ~2% |
| `aggressive` | Large files, low relevance | ~5% |
| `entropy` | Very repetitive files (logs, generated) | ~1% |
| `task` | Task-focused (requires intent) | auto |
| `lines:N-M` | Line ranges | proportional |

---

## CLI Commands (User Terminal)

These are commands **you** run in your shell.

### Setup & Diagnostics

```bash
# One-time setup: install shell aliases + configure MCP for detected AI tools
lean-ctx setup

# Quick setup for specific agent (alternative to full setup)
lean-ctx init --global         # Shell aliases only
lean-ctx init --agent opencode # MCP for OpenCode
lean-ctx init --agent cursor   # MCP for Cursor
lean-ctx init --agent claude   # MCP for Claude Code
# ... agents: codex, gemini, windsurf, copilot, cline, roo, pi, qwen, trae, amazonq, jetbrains

# Verify installation
lean-ctx doctor

# Auto-fix common issues
lean-ctx doctor --fix
```

### File Operations

```bash
# Read file (cached, structured)
lean-ctx read path/to/file.rs

# Read with specific mode
lean-ctx read path/to/file.rs -m map
lean-ctx read path/to/file.rs -m signatures
lean-ctx read path/to/file.rs -m "lines:100-200"

# Batch read
lean-ctx read file1.rs file2.rs file3.rs

# Search (grep)
lean-ctx grep "pattern" src/

# Directory tree
lean-ctx tree src/ --depth 2

# Git diff (compressed)
lean-ctx diff
```

### Shell Compression

```bash
# Execute any command with compression
lean-ctx -c "git status"
lean-ctx exec "cargo build"

# Disable compression for single command
lean-ctx -c --raw "kubectl get pods -o yaml"

# Shell mode (all commands compressed after enabling)
lean-ctx shell
# Now: git status, docker ps, etc. auto-compressed
```

### Analytics & Monitoring

```bash
# See token savings and GainScore
lean-ctx gain

# Dashboard (opens browser)
lean-ctx dashboard

# Session management
lean-ctx session status
lean-ctx sessions list
lean-ctx sessions show <id>

# Discover uncompressed commands in shell history
lean-ctx discover

# Cache management
lean-ctx cache stats
lean-ctx cache clear
lean-ctx cache invalidate <path>
```

### Configuration

```bash
# Set config values
lean-ctx config set checkpoint_interval 30
lean-ctx config set cache_ttl 300
lean-ctx config list

# Benchmark file read modes on your project
lean-ctx benchmark run .
```

---

## Configuration File

**Location:** `~/.lean-ctx/config.toml`

```toml
# Auto-checkpoint after N tool calls (default: 30)
checkpoint_interval = 30

# Cache TTL in seconds (default: 300)
cache_ttl = 300

# Enable/disable shell hooks (default: true)
shell_hooks = true

# CRP mode: "auto" (default), "never", "always"
crp_mode = "auto"

# Hooks integration: list of AI tools to auto-configure
# Leave empty to auto-detect
agents = []
```

---

## How It Integrates with OpenCode

The `lean-ctx` MCP server is defined in your `opencode.json`:

```json
{
  "mcp": {
    "lean-ctx": {
      "command": ["lean-ctx"],
      "enabled": true,
      "type": "local",
      "environment": {
        "LEAN_CTX_DATA_DIR": "/home/johnatas/.lean-ctx"
      }
    }
  }
}
```

When OpenCode needs to read a file, search code, or run a shell command, it uses the MCP tools (`ctx_read`, `ctx_search`, `ctx_shell`, etc.) instead of the native tools. The MCP server compresses the output before returning it to the LLM.

**Shell hooks** (installed by `lean-ctx init --global`) add aliases to your shell profile so commands like `git status` are automatically compressed when you run them in any terminal.

---

## Multi-Agent Launcher

```bash
# Launch any supported AI tool with lean-ctx pre-configured
lctx                    # Auto-detect current tool
lctx --agent claude     # Launch Claude Code
lctx --agent cursor     # Launch Cursor
lctx --agent gemini     # Launch Gemini CLI
```

---

## Notes

- **Cache-aware:** lean-ctx avoids re-compressing the same content by caching fingerprints.
- **Pattern-based compression:** Uses 90+ patterns to strip noise (HTTP logs, stack traces, color codes, etc.).
- **Session persistence:** Cross-session memory via `ctx_session` tools.
- **Cost savings:** Typical projects save 60-90% of input tokens, translating to ~$10-100/month in API costs.

---

## Quick Troubleshooting

```bash
# Check if MCP server is running
lean-ctx doctor

# Clear cache if files seem stale
lean-ctx cache clear

# Disable temporarily
LEAN_CTX_DISABLED=1 lean-ctx -c "git status"
```

For more details, see: https://leanctx.com/docs
