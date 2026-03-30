# Plan: Migration to lean-ctx

| | Created | Updated |
| -- | -- | -- |
| **Status** | completed | 2026-04-17 |
| **Agent** | plan | - |
| **Priority** | high | - |

---

## Execution

| Timestamp | Step |
| -- | -- |
| 2026-04-17 22:00 | Remove plugins from opencode.json (context-mode, dcp, tokenscope) |
| 2026-04-17 22:01 | Disable context-mode MCP |
| 2026-04-17 22:01 | Restore read/grep/glob permissions |
| 2026-04-17 22:02 | Keep auto-compaction enabled (user request) |
| 2026-04-17 22:03 | Install lean-ctx (`npm install -g lean-ctx-bin`) |
| 2026-04-17 22:04 | Setup for OpenCode (`lean-ctx init --agent opencode`) |
| 2026-04-17 22:05 | Configure checkpoint_interval=30 |
| 2026-04-17 22:06 | Verify (`lean-ctx doctor`) |
| 2026-04-17 22:07 | Create migration plan document |
| 2026-04-17 22:10 | Add AGENTS.md cleanup instructions |

## Objective

Replace context-mode, opencode-dcp, and tokenscope with lean-ctx for better context management with configurable checkpoint intervals and MCP server.

---

## Problems Solved

| Problem | Solution |
|---------|----------|
| DCP compacts during long tasks | lean-ctx `checkpoint_interval: 30` (was 15) |
| context-mode hit or miss | lean-ctx MCP server with smart tools |
| No visibility of savings | `lean-ctx gain` command |

---

## What Was Already Done

These steps were already executed in the session:

### 1. opencode.json — Plugins Removed

```json
"plugin": [
  "opencode-handoff",
  "opencode-session-recall",
  "@gotgenes/opencode-agent-identity",
  "@knikolov/opencode-plugin-simple-memory",
  "@franlol/opencode-md-table-formatter@latest"
]
```

### 2. opencode.json — MCP Disabled

```json
"context-mode": {
  "type": "local",
  "enabled": false,
  "command": ["context-mode"]
}
```

### 3. opencode.json — Permissions Restored

Before:
```json
"tool": {
  "*": "allow",
  "read": "deny",
  "grep": "deny",
  "glob": "deny"
}
```

After:
```json
"tool": {
  "*": "allow"
}
```

### 4. opencode.json — Compaction Status

Compaction remains **enabled** (auto: true, prune: true) as per user request. No changes made.

### 5. lean-ctx Installed & Configured

```bash
npm install -g lean-ctx-bin
lean-ctx init --agent opencode
lean-ctx config set checkpoint_interval 30
```

### 6. Verification

```bash
lean-ctx doctor
# 9/11 checks passed (shell aliases optional)
```

---

## What YOU Need to Do

### Step 1: Restart OpenCode (REQUIRED)

Close and reopen OpenCode to load the new configuration.

### Step 2: Shell Aliases (RECOMMENDED)

Enables automatic compression of shell command output.

```bash
lean-ctx init --global
```

Run **once** in terminal. Persists between sessions.

### Step 3: Verify Savings (AFTER USE)

After using OpenCode for a while:

```bash
lean-ctx gain
```

---

## Verification Commands

Run these anytime:

| Command | Purpose |
|---------|---------|
| `lean-ctx doctor` | Verify installation |
| `lean-ctx gain` | See token savings |
| `lean-ctx session status` | Current session info |
| `lean-ctx dashboard` | Real-time dashboard |
| `lean-ctx discover` | Find unoptimized commands |

---

## Configuration

File: `~/.lean-ctx/config.toml`

```toml
checkpoint_interval = 30  # Auto-checkpoint every 30 tool calls
```

---

## Lean-ctx Tools (How Agent Uses)

The agent uses lean-ctx MCP tools automatically. These replace native tools:

| Prefer | Instead of | Why |
|--------|----------|-----|
| `ctx_read(path, mode)` | `Read` / `cat` | Cached, 10 read modes, re-reads ~13 tokens |
| `ctx_shell(command)` | `Shell` / `bash` | Pattern compression |
| `ctx_search(pattern, path)` | `Grep` / `rg` | Compact results |
| `ctx_tree(path, depth)` | `ls` / `find` | Compact directory |
| `ctx_edit(path, old, new)` | `Edit` | Search-and-replace |

---

## Shell Aliases (Optional but Recommended)

Shell aliases comprimem a saída de comandos shell automaticamente.

**When to run:** No terminal/bash, após reiniciar o opencode.

```bash
lean-ctx init --global
```

Isso adiciona aliases ao ~/.zshrc. **Uma vez só.** Persiste entre sessões.

**What it does:**
- `git status` → `lean-ctx -c "git status"` (comprimido)
- `cargo test` → `lean-ctx -c "cargo test"` (comprimido)
- etc.

---

## AGENTS.md — Check for context-mode References

If you need to rollback or deactivate later:

```bash
grep -i "context-mode" ~/.config/opencode/AGENTS.md
```

**If it's there, remove it** similar to lean-ctx blocks that were auto-added.

### Remove [CTX-MODE] MANDATORY Section

Since context-mode has been replaced by lean-ctx, remove the mandatory context-mode directive block from AGENTS.md:

```markdown
<!-- [CTX-MODE] MANDATORY -->
MANDATORY: Use ctx_execute_file for file analysis. Use ctx_execute for commands. Use ctx_batch_execute for multiple operations.
NEVER: Use read/cat/grep for analysis. This floods context.
<!-- [/CTX-MODE] -->
```

This conflicts with the new lean-ctx system. Remove the entire block.

**Optional:** Also remove the reference to `context-mode.md` from the instructions section if you want a clean setup.

---

## Rollback Plan

If issues occur:

1. Re-enable plugins in opencode.json:
   - Add back: `context-mode`, `@tarquinen/opencode-dcp@latest`, `@ramtinj95/opencode-tokenscope@latest`
2. Set `context-mode` MCP to `enabled: true`
3. Restore permissions to `deny`
4. Set `compaction.auto: true`
5. Cleanup AGENTS.md (remove lean-ctx references)
6. Uninstall lean-ctx: `npm uninstall -g lean-ctx-bin`

---

## Summary Checklist

- [x] Remove plugins from opencode.json
- [x] Disable context-mode MCP
- [x] Restore permissions
- [x] Install lean-ctx
- [x] Setup for OpenCode
- [x] Configure checkpoint_interval
- [ ] Restart OpenCode ← YOUR ACTION
- [ ] (Optional) Shell aliases
- [ ] Verify savings ← AFTER USE