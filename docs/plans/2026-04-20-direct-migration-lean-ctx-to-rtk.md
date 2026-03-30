# Direct Migration: lean-ctx → RTK

**Date:** 2026-04-20  
**Status:** Completed  
**Scope:** Replace lean-ctx with RTK while maintaining compression and adding granular security

---

## 1. Objective

Remove `lean-ctx` (MCP with `ctx_shell` that bypasses permissions) and implement `RTK` (Rust Token Killer) as the tool output compression solution, preserving:

- 60-90% compression on bash commands
- Granular permissions via `bash` patterns (security)
- Compatibility with magic-context and caveman (if installed)
- Stability of current workflow

---

## 2. Current Context

| Component      | Status              | Notes                                   |
|-----------------|--------------------|-----------------------------------------|
| magic-context   | ✅ Active          | Manages conversational context         |
| caveman        | ❌ Not installed   | LLM output compression                  |
| lean-ctx (MCP)  | ⚠️ Active (issue) | Uses `ctx_shell` → bypasses `bash` perms |
| Bash permissions| ✅ Configured      | Dangerous patterns set to `ask`         |
| opencode.json   | ✅ Configured      | MCP `lean-ctx` + permissions            |
| Git hooks       | ❌ Not configured  | Missing final defense layer            |

**Problem:**  
Agent uses `ctx_shell` (MCP) to execute commands → `bash` permissions do not apply → risk of destructive commands without confirmation.

---

## 3. Prerequisites

- ✅ OpenCode installed and working
- ✅ magic-context active (will remain)
- ✅ OPENROUTER_API_KEY set (unaffected)
- ⚠️ **RTK binary** must be installed (via curl script, no Rust needed)
- ⚠️ Access to edit `~/.config/opencode/opencode.json`
- ⚠️ OpenCode restart required

---

## 4. RTK Configuration

### 4.1. About Built-in Filters

RTK has **36 built-in filters** that automatically compress output for common commands (git, npm, cargo, docker, pytest, etc.). These are applied automatically and cannot be configured individually.

Reference: https://github.com/rtk-ai/rtk/blob/master/docs/guide/getting-started/configuration.md

### 4.2. Excluded Commands

Commands that should NOT be rewritten by RTK:

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

Justification:
- `curl`: raw API data may need to stay intact
- `playwright`: snapshots/PDFs/HTML must be preserved
- `ssh`/`scp`: remote connections
- `kubectl exec`: container output may be verbose but necessary
- `git diff`, `git rebase`, `git cherry-pick`, `git apply`: output detalhado é essencial
- `git diff`, `git rebase`, `git cherry-pick`, `git apply`: output detalhado é essencial para o agente não se perder

### 4.3. Official RTK Configuration

Using official config.toml structure from RTK documentation:

```toml
# ~/.config/rtk/config.toml

[tracking]
enabled = true
history_days = 90

[display]
colors = true
emoji = true
max_width = 120

[filters]
ignore_dirs = [".git", "node_modules", "target", "__pycache__", ".venv", "vendor"]
ignore_files = ["*.lock", "*.min.js", "*.min.css"]

[tee]
enabled = true
mode = "failures"
max_files = 20

[telemetry]
enabled = false  # Disabled for privacy

[hooks]
exclude_commands = ["curl", "playwright", "ssh", "scp", "kubectl exec"]
```

---

## 5. Bash Permissions (Security)

With RTK, the agent uses **bash** → pattern matching rules apply.

Update `opencode.json` to include `rm -rf *` and `sh -c *`:

```json
"permission": {
  "bash": {
    "*": "allow",
    "rm -rf *": "ask",
    "dd *": "ask",
    "git checkout *": "ask",
    "git reset *": "ask",
    "git restore *": "ask",
    "git clean *": "ask",
    "sh -c *": "ask"
  }
}
```

`sh -c *` covers cases like `sh -c "rm -rf /tmp/*"` that could bypass explicit git rules.

---

## 6. Direct Migration Steps

### Phase 1 — Preparation

1. **Document current state (baseline):**
   ```bash
   # Run in OpenCode
   /ctx-status > docs/plans/baseline-ctx-status.txt
   ```
   Also save:
   - Current `opencode.json` (copy to `docs/plans/opencode-backup.json`)
   - `~/.config/rtk/` (if exists, backup)

2. **Install RTK binary** (via curl, no Rust):
   ```bash
   curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
   ```

3. **Verify installation:**
   ```bash
   rtk --version
   ```

4. **Install OpenCode plugin:**
   ```bash
   rtk init -g --opencode
   ```

5. **Create RTK configuration** (official format):
   ```bash
   cat > ~/.config/rtk/config.toml << 'EOF'
   [tracking]
   enabled = true
   history_days = 90

   [display]
   colors = true
   emoji = true
   max_width = 120

   [filters]
   ignore_dirs = [".git", "node_modules", "target", "__pycache__", ".venv", "vendor"]
   ignore_files = ["*.lock", "*.min.js", "*.min.css"]

   [tee]
   enabled = true
   mode = "failures"
   max_files = 20

   [telemetry]
   enabled = false

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
   EOF
   ```

6. **Restart OpenCode** to load plugin.

### Phase 2 — Remove lean-ctx

1. **Disable lean-ctx MCP in `opencode.json`:**
   - Remove the `"lean-ctx": { ... }` section inside `"mcp"` (lines 28–33)
   - Save change.

2. **Uninstall lean-ctx:**
   ```bash
   lean-ctx uninstall
   ```
   This removes: shell hook entries, MCP configs, agent rules files, and ~/.lean-ctx/ data directory.

3. **Remove lean-ctx binary** (no Rust, use rm):
   ```bash
   rm $(which lean-ctx)
   ```

3. **Restart OpenCode** again.

### Phase 3 — Adjust Permissions

Add `rm -rf *` and `sh -c *` to `permission.bash` (if not already present).

### Phase 4 — Validation

1. **Check active tools:**
   - Run `/ctx-status`
   - Confirm `ctx_shell` (lean-ctx) **does not appear**
   - Confirm `magic-context` is still active

2. **Test RTK compression:**
   ```bash
   # In OpenCode, execute:
   git status
   # Expected: compact format (e.g., "branch=main, changes=2")
   npm test  # if available
   # Should show aggregated results if testOutputAggregation works
   ```

3. **Test permissions:**
   - `rm -rf /tmp/test` → should show confirmation dialog
   - `git checkout -- .` → should show confirmation
   - `sh -c "echo test"` → should show confirmation (sh -c *)

4. **Verify magic-context:**
   - `/ctx-status` → Token distribution, injected memories, compartments
   - Should be functioning normally

5. **Check RTK savings:**
   ```bash
   rtk gain --history
   ```

6. **Test critical functionality:**
   - Read large files (`read` tool) → working (now no file compression, only bash output compressed)
   - Search (`grep`) → working
   - If anything breaks, note for tweaking

### Phase 5 — Monitoring (1 week)

- Every 2 days: run `/ctx-status` and compare with baseline
- Run `rtk gain --history` to track savings
- Note:
  - Tool Calls tokens (should drop significantly vs baseline)
  - Conversation tokens (should remain stable)
  - Total tokens per session
  - Issues: incomprehensible outputs, failed commands, information loss

---

## 7. Success Criteria

| Criterion              | Expected                              | How to Measure                     |
|------------------------|---------------------------------------|------------------------------------|
| Tool Calls tokens ↓    | ≥50% reduction vs baseline            | `/ctx-status` before/after         |
| Permissions work       | Dangerous commands require confirmation| Test `rm -rf`, `git checkout`, `sh -c` |
| magic-context intact   | Memories, compartments, stats normal  | `/ctx-status`                     |
| Commands compressed    | Shorter outputs, still useful         | Visual check: git status, npm test |
| No errors              | No tool call failures                 | OpenCode logs, /ctx-status        |

---

## 8. Risks and Mitigations

| Risk                                                       | Impact            | Mitigation                                             |
|------------------------------------------------------------|-------------------|--------------------------------------------------------|
| RTK over-compresses and loses information                 | Medium            | Conservative profile; tweak config if needed           |
| Critical command mistakenly excluded                      | Low               | Test frequently used commands before migrating         |
| Hook conflict (lean-ctx not fully removed)                 | Medium            | Uninstall lean-ctx hooks completely                    |
| `bash` permissions don't cover all vectors                | Low               | Review patterns; `sh -c *` covers shell execution      |
| RTK doesn't compress read files (read tool)               | Low (not focus)   | Accept; magic-context already helps context            |

---

## 9. Rollback (if needed)

1. **Re-add lean-ctx MCP to `opencode.json`:**
   ```json
   "mcp": {
     "lean-ctx": {
       "command": ["lean-ctx"],
       "enabled": true,
       "environment": { "LEAN_CTX_DATA_DIR": "/home/johnatas/.lean-ctx" },
       "type": "local"
     }
   }
   ```

2. **Reactivate lean-ctx:**
   ```bash
   # First, reinstall binary via curl
   curl -fsSL https://leanctx.com/install.sh | sh
   # Then run setup
   lean-ctx setup
   ```

3. **Remove RTK plugin:**
   ```bash
   rm ~/.config/opencode/plugins/rtk.ts
   ```

4. **Restart OpenCode**

5. **Validate** `/ctx-status` returns to previous state (compare with baseline)

---

## 10. Estimated Timeline

| Step                              | Time   | Dependencies          |
|-----------------------------------|--------|-----------------------|
| Baseline measurements             | 10 min | —                     |
| RTK installation (curl + plugin)  | 15 min | network               |
| RTK configuration (create config) | 5 min  | decisions made        |
| Remove lean-ctx (MCP + hooks)     | 10 min | backup done           |
| OpenCode restart                  | 2 min  | —                     |
| Initial validation (manual tests) | 1h     | OpenCode running      |
| Monitoring (1 week)               | —      | after migration       |

**Total execution time:** ~2h (excluding monitoring)

---

## 11. Expected Artifacts

- ✅ `docs/plans/2026-04-20-migracao-direta-lean-ctx-para-rtk.md` (this plan)
- ✅ `docs/plans/baseline-ctx-status.txt` (previous metrics)
- ✅ `docs/plans/opencode-backup.json` (config backup)
- ✅ `~/.config/rtk/config.toml` (active configuration)
- ✅ `~/.config/opencode/plugins/rtk.ts` (active plugin)

---

## 12. Open Questions (already answered)

1. **RTK configuration:** Using official config.toml (tracking, tee, telemetry disabled, exclude_commands)
2. **Caveman:** not currently installed, not needed for migration
3. **Remove lean-ctx completely:** yes, use `lean-ctx uninstall` + remove MCP from opencode.json
4. **Permissions:** add `rm -rf *` and `sh -c *` as `ask`
5. **RTK installation:** via curl script (no Rust)

---

## 13. Next Steps

After reviewing and approving this plan, execute **Phases 1 to 5** in order.

---

**Note:** This plan assumes you have read and agree with the listed configuration decisions. If any changes are needed, adjust before execution.
