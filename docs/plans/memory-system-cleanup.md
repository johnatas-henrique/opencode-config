# Memory System Cleanup Plan

**Date:** 2026-05-28
**Status:** CANCELLED — agentmemory was updated and bugs were fixed; keeping agentmemory instead of migrating to claude-mem
**Reason for cancellation:** Agentmemory daemon (agm.service) is running reliably, the `experimental.chat.system.transform` hook was patched in `agentmemory-capture.ts`, pinned slots are being injected, and the MCP tools work. See `agentmemory-verification-plan.md` for current validation.

## Context

Previous session completed Phase 1 of open-stack-cleanup (removed gitnexus, playwright, fff, markitdown MCPs). This plan addresses the memory system specifically.

## Problem

- agentmemory captures observations but agent doesn't search/save proactively
- 7+ memories saved but never used in sessions
- No auto-injection of context at session start
- global-identity.md instructions are advisory, not enforced

## Solution: Hybrid Approach

### What to Disable

| Component | File | Reason |
|-----------|------|--------|
| agentmemory MCP server | opencode.jsonc | Agent doesn't use it proactively |
| agentmemory-capture.ts plugin | opencode.jsonc | Captures data but doesn't inject context |
| cross-session-memory.md | docs/agent-instructions/ | Obsolete with plugin-based memory |

### What to Keep

| Component | File | Reason |
|-----------|------|--------|
| global-identity.md | docs/agent-instructions/ | Instructions that MUST always load |
| opencode-hooks | opencode.jsonc | Infrastructure for injection |
| All other instructions | docs/agent-instructions/ | Process, workflow, testing, etc. |

### What to Add

| Component | Action | Reason |
|-----------|--------|--------|
| opencode-hooks config | Add session.created hook | Inject global-identity.md automatically |
| claude-mem plugin | Install | Project-scoped memories (auto-save + auto-inject) |

## Architecture

```
~/.config/opencode/
├── opencode.jsonc
│   ├── plugins:
│   │   ├── opencode-hooks            # ✅ Keep (global injection)
│   │   ├── claude-mem                # 🆕 Add (memories)
│   │   └── agentmemory-capture.ts    # ❌ Remove
│   └── mcp:
│       ├── context7                  # ✅ Keep
│       ├── exa                       # ✅ Keep
│       ├── gh_grep                   # ✅ Keep
│       ├── playwriter                # ✅ Keep
│       └── agentmemory               # ❌ Remove
│
├── AGENTS.md                         # Simplified
│   ├── References to cross-session-memory.md → ❌ Removed
│   └── Reference to opencode-hooks   → 🆕 Added
│
├── docs/agent-instructions/
│   ├── global-identity.md            # ✅ Keep (injected via hook)
│   ├── cross-session-memory.md       # ❌ Remove (plugin handles)
│   └── ... (other instructions)      # ✅ Keep
│
└── plugins/
    └── agentmemory-capture.ts        # ❌ Remove
```

## How It Works Post-Plan

### Session Flow (After)

```
1. Session starts
2. opencode-hooks runs script: reads global-identity.md
3. Content injected into session automatically
4. claude-mem injects project memories
5. Agent ALWAYS receives memories (zero dependency)
6. Plugin ALWAYS saves observations (zero dependency)
```

### Global Identity Injection

```
session.created → opencode-hooks → cat global-identity.md → appendToSession
```

### Project Memories (claude-mem)

```
Agent uses tools → claude-mem captures via PostToolUse hook
                → worker processes via AI
                → saves to SQLite

SessionStart → claude-mem injects project memories
              → agent receives context automatically
```

## Why claude-mem (not opencode-mem)

| Criterion | claude-mem | opencode-mem | Decision |
|-----------|------------|--------------|----------|
| Shares between tools | ✅ Single SQLite `~/.claude-mem/` | ❌ OpenCode only | claude-mem |
| Future Claude Code use | ✅ Same memory | ❌ Separate memory | claude-mem |
| Community | ✅ 79k stars | 🟡 788 stars | claude-mem |
| Documentation | ✅ Extensive | 🟡 README only | claude-mem |
| Setup | ❌ Worker service (port 37777) | ✅ Native plugin | opencode-mem |
| Maintenance | ❌ May need restart | ✅ Zero | opencode-mem |

**Choice: claude-mem** because:
1. Memory shared if you start using Claude Code
2. 79k stars = active community, support, updates
3. Extensive documentation resolves issues quickly
4. Worker service is acceptable tradeoff

## Implementation Checklist

| # | Action | File affected |
|---|--------|---------------|
| 1 | Remove agentmemory MCP from opencode.jsonc | opencode.jsonc |
| 2 | Remove agentmemory-capture.ts from opencode.jsonc | opencode.jsonc |
| 3 | Remove plugin file | plugins/agentmemory-capture.ts |
| 4 | Remove cross-session-memory.md | docs/agent-instructions/ |
| 5 | Update AGENTS.md (remove cross-session refs) | AGENTS.md |
| 6 | Add session.created hook in opencode-hooks | opencode.jsonc |
| 7 | Install claude-mem | opencode.jsonc |
| 8 | Configure claude-mem (provider, port, etc.) | ~/.claude-mem/settings.json |
| 9 | Test global-identity.md injection | Test session |
| 10 | Test auto-save + auto-inject of memories | Test session |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| claude-mem worker service port conflict | Configure fixed port via `CLAUDE_MEM_WORKER_PORT` |
| Injection hook fails | Test with `--verbose` on opencode-hooks |
| Old agentmemory memories lost | Export before removing (if needed) |
| claude-mem doesn't work well with OpenCode | Documentation shows it works (v13.3.0) |

## Next Steps

1. **Phase 1:** Disable agentmemory (MCP + plugin + instruction)
2. **Phase 2:** Configure global-identity injection via opencode-hooks
3. **Phase 3:** Install and configure claude-mem
4. **Phase 4:** Test everything together
5. **Phase 5:** Clean up broken references

## Dependencies

- Wait for open-stack-cleanup completion
- Verify results before implementing this plan
