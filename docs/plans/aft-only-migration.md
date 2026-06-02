# Plan: AFT-only simplification + Stderr hook

## Goal

Reduce from 3 competing systems (AFT + fff + GitNexus) to 1 (AFT + native tools), and eliminate `2>/dev/null` pattern that agents keep using.

---

## Phase 1 — Create `block-stderr-suppression.sh` hook

### What it does

Blocks bash commands that suppress stderr, forcing the agent to handle errors properly.

### Blocked patterns

| Pattern | Example |
|---------|---------|
| `2>/dev/null` | `grep foo bar 2>/dev/null` |
| `>/dev/null 2>&1` | `build.sh >/dev/null 2>&1` |
| `&>/dev/null` | `make &>/dev/null` |
| `2>&-` | `cmd 2>&-` |
| `/dev/null` (any null redirect) | `cmd >/dev/null` |

### Deny message

```
Command with stderr suppression blocked.

This hides real errors the agent needs to see.
Instead:
  • Use exit codes to detect failure: cmd || handle_error
  • Use compressed: false if output is too large
  • If the error is expected, just ignore with &&/||
```

### Files involved

| File | Action |
|------|--------|
| `~/.claude/hooks/block-stderr-suppression.sh` | **Create** — hook script |
| `~/.claude/settings.json` | **Edit** — register hook in PreToolUse > Bash |

---

## Phase 2 — Disable GitNexus and fff

### opencode.jsonc

Disable in MCP servers section:

```jsonc
{
  "mcpServers": {
    "fff": { "enabled": false },
    "gitnexus": { "enabled": false }
  }
}
```

Keep `context7`, `exa`, `gh_grep`, `playwriter`, `agentmemory` — no overlap with AFT.

### What's lost (never used)

| GitNexus feature | Status |
|-----------------|--------|
| Cross-repo groups | Never configured |
| Route mapping / shape check | Not used |
| Pre-commit detect_changes | Not used |
| Cypher queries | Not used |
| Process flows (280 indexed) | Indexed but never queried |

Zero effective loss. AFT covers callers, impact, trace and semantic search with embeddings (better than GitNexus BM25).

---

## Phase 3 — Add global-identity.md to AGENTS.md include list

Add to AGENTS.md `## Detailed Guidelines` block, same pattern as the other 8 docs:

```markdown
- [Global Identity](docs/agent-instructions/global-identity.md) — Identity, restraints & preferences
```

### Why link (not hook)

- Deterministic: loaded every session as Instructions from:
- Same mechanism as the other 8 docs
- Doesn't depend on the hooks plugin being operational

---

## Phase 4 — Clean up AGENTS.md conflicting instructions

### Current problem (lines 242-282)

AGENTS.md has a `## MCP Tools` section that:

1. **Mentions `codebase-memory-mcp`** — MCP server NOT configured in opencode.jsonc. Agent reads this and tries to call `search_graph`, `trace_path` etc that don't exist.
2. **Duplicates what's already in `docs/agent-instructions/mcp-tools.md`**

### Action

| Lines | Content | Action |
|-------|---------|--------|
| 241-242 | Header `## MCP Tools` | **Remove** |
| 243-262 | `codebase-memory-mcp` block | **Remove** (ghost) |
| 264-282 | `## GitNexus / fff` block | **Remove** (duplicated) |

### Result

AGENTS.md no longer mentions MCP tools. Everything centralized in `docs/agent-instructions/mcp-tools.md`.

---

## Phase 5 — Simplify `docs/agent-instructions/mcp-tools.md`

Replace multi-table structure (GitNexus + fff + AFT) with a single decision tree routing to AFT or native tools.

New content: one table with task-to-tool mapping, plus AFT-specific rules.

---

## Phase 6 — Verify AFT setup

```bash
npx @cortexkit/aft doctor
```

Check:
- Plugin `@cortexkit/aft-opencode` registered in `opencode.jsonc`
- Binary downloaded at `~/.cache/aft/bin`
- LSP servers identified

---

## Summary of affected files

| File | Action |
|------|--------|
| `~/.claude/hooks/block-stderr-suppression.sh` | Create |
| `~/.claude/settings.json` | Edit (register hook) |
| `opencode.jsonc` | Edit (disable fff, gitnexus) |
| `AGENTS.md` | Edit — remove lines 242-282 + add global-identity |
| `docs/agent-instructions/mcp-tools.md` | Edit (simplify) |

## Execution order

```
1. Create hook block-stderr-suppression.sh
2. Register in settings.json
3. Disable fff + gitnexus in opencode.jsonc
4. Clean AGENTS.md (242-282)
5. Add global-identity.md to include list
6. Simplify mcp-tools.md
7. Run aft doctor to validate
8. Quick test session with grep + navigation
```

Ready for review.
