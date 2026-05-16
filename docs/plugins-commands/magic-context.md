# Magic Context Commands & Tools

**Status:** ✅ Active
**Purpose:** Infinite context via cache-aware chat compression, cross-session memory, and background historian.
**Repository:** https://github.com/cortexkit/magic-context
**Documentation:** https://github.com/cortexkit/magic-context/blob/master/CONFIGURATION.md

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `/ctx-status` | TUI | Debug view: tags, drops, cache TTL, historian progress, compartment coverage |
| `/ctx-flush` | TUI | Force all queued reduction operations immediately |
| `/ctx-recomp` | TUI | Rebuild compartments and facts from raw history (full or partial `/ctx-recomp 1-11322`) |
| `/ctx-aug` | TUI | Run sidekick augmentation (retrieve relevant memories) |
| `/ctx-dream` | TUI | Run dreamer maintenance now (instead of waiting for schedule) |
| `ctx_reduce(drop)` | MCP (Agent) | Mark content for removal to shed context weight |
| `ctx_expand(start, end)` | MCP (Agent) | Expand compressed history range back to raw messages |
| `ctx_memory(...)` | MCP (Agent) | Cross-session memory CRUD (list/write/delete/update) |
| `ctx_knowledge(...)` | MCP (Agent) | Project knowledge management (facts, patterns, decisions) |
| `ctx_search(query)` | MCP (Agent) | Semantic + lexical search across memories, git commits, and history |
| `ctx_note(content)` | MCP (Agent) | Durable session notes that persist across context compression |

---

## User Commands (TUI)

Type these in the chat to interact with Magic Context:

| Command | Description |
|---------|-------------|
| `/ctx-status` | **Debug view.** Shows: §N§ tags, pending drops, cache TTL, nudge state, historian progress, compartment coverage, history compression budget. |
| `/ctx-flush` | **Force cleanup.** Immediately executes all queued reduction operations, bypassing cache TTL. Use when context is bloated. |
| `/ctx-recomp [range]` | **Rebuild state.** Reconstructs compartments and facts from raw history. Use if stored state seems corrupted or inconsistent. Optional range: `/ctx-recomp 1-11322` rebuilds only a message range. |
| `/ctx-aug` | **Sidekick augmentation.** Runs the sidekick model to retrieve relevant memories and inject them into your current prompt. Enhances context with project history. |
| `/ctx-dream` | **Manual dreamer.** Triggers the dreamer maintenance immediately (instead of waiting for scheduled run). Consolidates memories, deduplicates, promotes facts. |

---

## Agent Tools (MCP)

These tools are used by the LLM agent automatically. You don't call them directly.

### Context Management

| Tool | Purpose | Parameters |
|------|---------|------------|
| `ctx_reduce(drop)` | Mark content for removal to shed context weight. Drops are queued, not applied immediately. | `drop`: comma-separated tag ranges, e.g. `"3-5,12"` or `"1,2,9-15"` |
| `ctx_expand(start, end)` | Expand a compressed history range back to raw messages for recall. Returns `U:`/`A:` transcript format, capped at ~15K tokens. | `start`, `end`: message ordinal numbers |

### Memory & Knowledge

| Tool | Purpose |
|------|---------|
| `ctx_memory(action, ...)` | Cross-session memory CRUD. Actions: `list`, `write`, `dismiss`, `update`. Categories: `USER_DIRECTIVES`, `USER_PREFERENCES`, `NAMING`, `CONFIG_DEFAULTS`, `CONSTRAINTS`, `ARCHITECTURE_DECISIONS`, `ENVIRONMENT`, `WORKFLOW_RULES`, `KNOWN_ISSUES`. |
| `ctx_knowledge(action, ...)` | Project knowledge management (facts, patterns, decisions). |
| `ctx_search(query)` | Search across memories, git commits, and message history. Sources: `memory`, `git_commit`, `message`. |
| `ctx_note(action, ...)` | Durable session notes that survive context compression. Actions: `write`, `read`, `dismiss`, `update`. |

---

## TUI Sidebar

Magic Context adds a live sidebar showing real-time context breakdown:

```
┌─ Context Window ──────────────────┐
│ System:        8.2K  ████░░░░░ 18%│
│ Compartments: 12.4K ██████░░░░ 27%│
│ Facts:         3.1K  ██░░░░░░░░  7%│
│ Memories:     2.8K  ██░░░░░░░░  6%│
│ Conversation: 18.7K ██████████ 42% │
│ Reduce Queue:  3 ops                │
│ Historian:    idle                │
│ Dreamer:     4h ago              │
└───────────────────────────────────┘
```

**What it shows:**
- Token usage by category
- Pending reduction operations
- Historian activity status
- Time since last dreamer run

---

## Current Configuration

**File:** `~/.config/opencode/magic-context.jsonc`

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/cortexkit/magic-context/master/assets/magic-context.schema.json",
  "enabled": true,

  "memory": {
    "enabled": true,
    "injection_budget_tokens": 4000,
    "auto_promote": true
  },

  "embedding": {
    "provider": "local"
  },

  "ctx_reduce_enabled": true,
  "execute_threshold_percentage": 60,
  "auto_drop_tool_age": 50,
  "nudge_interval_tokens": 5000,

  "historian": {
    "model": "github-copilot/gpt-5.4",
    "fallback_models": [
      "nvidia/openai/gpt-oss-120b",
      "nvidia/meta/llama-4-scout-17b-16e-instruct",
      "nvidia/stepfun-ai/step-3.5-flash",
      "mistral/mistral-small-latest"
    ]
  },

  "dreamer": {
    "enabled": true,
    "model": "github-copilot/gpt-5.4",
    "fallback_models": [
      "nvidia/openai/gpt-oss-120b",
      "mistral/devstral-latest",
      "mistral/codestral-latest"
    ],
    "schedule": "02:00-06:00",
    "tasks": ["consolidate", "verify", "archive-stale", "improve"]
  },

  "sidekick": {
    "enabled": false
  }
}
```

### Model Selection

- **historian**: High-quality model for background compression. Prefer request-based pricing (GitHub Copilot) since it runs frequently.
- **dreamer**: Runs during idle time (overnight). Can be smaller/cheaper. Even local models like `ollama/*` work well.
- Models must support tool calling.

### When historian fires

| Trigger | Condition |
|---------|-----------|
| **Context pressure** | `execute_threshold_percentage` (60%) reached |
| **Commit cluster** | 3+ commit clusters in unsummarized tail (even with low context) |
| **Tail size** | Unsummarized tail hits `trigger_budget` |
| **`/ctx-recomp`** | Manual trigger |

### Dreamer tasks

| Task | What it does |
|------|-------------|
| `consolidate` | Merge semantically duplicate memories into one canonical fact |
| `verify` | Check CONFIG_DEFAULTS, ARCHITECTURE_DECISIONS, ENVIRONMENT against actual code |
| `archive-stale` | Archive memories referencing removed features, old paths |
| `improve` | Rewrite verbose/narrative memories into terse operational statements |

---

## Memory Management

| Action | How |
|--------|-----|
| **List memories** | `ctx_memory(action="list")` via agent (natural language: "me mostre as memórias") |
| **Save explicit rule** | "Salva como memória: sempre fazer X quando Y" (agente faz `ctx_memory(write)`) |
| **Delete wrong memory** | "Apague a memória com ID 42" (agente faz `ctx_memory(dismiss)`) |
| **Edit memory** | "Atualiza a memória 42 com novo conteúdo" (agente faz `ctx_memory(update)`) |
| **Browse/edit offline** | Desktop App → Memory Browser → search/edit/delete |
| **Nightly curation** | Dreamer runs during `02:00-06:00` |

### Priority hierarchy

```
identity.txt (suas instruções explícitas)  →  PRIORIDADE MÁXIMA
ctx_memory(write) (regras que você ditou)   →  PRIORIDADE ALTA
<project-memory> (observações do historian) →  PRIORIDADE BAIXA
```

---

## Cross-harvesting (OpenCode + Pi)

Memories are stored in a shared SQLite database at `~/.local/share/cortexkit/magic-context/context.db`:

- `harness` column scopes **session data** (tags, compartments) per-harness
- `project_path` scopes **memories, embeddings, and dreamer runs** cross-harness
- Write a memory in OpenCode → same memories available in Pi for the same project

---

## How It Works

1. **Tagging:** Every message, tool output, and file attachment gets a `§N§` tag (monotonic counter).
2. **Compartments:** Related tags are grouped into compartments (conversation turns, tasks).
3. **Historian:** A background model compresses old compartments into summaries, preserving core information. Extracts session facts and promotes recurring patterns to project memories.
4. **Cache-aware:** Operations are deferred to avoid wasting prompt cache. Reductions happen when cache expires or context pressure is high.
5. **Dreamer:** Runs overnight (or on `/ctx-dream`) to consolidate scattered memories, deduplicate, verify against code, and archive stale entries.
6. **Sidekick (optional):** Can auto-augment prompts with relevant project memories via `/ctx-aug`.
7. **Memory injection:** At each turn, `<project-memory>` block injects relevant memories (by semantic search or utility tier). Budget: 4000 tokens default.

---

## Integration with lean-ctx

- **lean-ctx** compresses **before** content enters the chat (shell outputs, file reads).
- **Magic Context** compresses **after** messages are exchanged (chat history, tool results).
- They are complementary and do not conflict.

---

## Common Workflows

### After a large tool output

The agent will automatically call `ctx_reduce(drop="...")` to mark old tool outputs for removal. This is transparent.

### Need to recall something from earlier?

The agent may call `ctx_expand(start, end)` to temporarily decompress a history range. You can also invoke this manually by asking the agent: "Expand the conversation from 10 minutes ago."

### Context window getting full?

- Magic Context auto-compresses in background.
- You can manually trigger: `/ctx-flush`
- Or force dreamer: `/ctx-dream`

### Want to verify everything is working?

Run: `/ctx-status`

### Before ending a session / handoff

Run `/ctx-recomp` to force extraction of any facts the historian hasn't processed yet.

### Save an explicit rule

"Salva como memória: quando fizer commit nesse projeto, usa Conventional Commits" — o agente chama `ctx_memory(write)`.

---

## Troubleshooting

### Historian not running?

Check sidebar status. If stuck, try `/ctx-dream` to manually trigger. Verify `execute_threshold_percentage` isn't set too high for your session length.

### No memories being created?

Check `memory.enabled: true` and `dreamer.enabled: true` in config. For short sessions (< 60% context), historian may never fire — use `/ctx-recomp` before handoff.

### State seems corrupted?

Rebuild from raw history: `/ctx-recomp` or `/ctx-recomp 1-11322` for partial rebuild.

### High token usage despite compression?

Verify `compaction.auto: false` in `opencode.json` (Magic Context manages its own compaction).

---

## Desktop App (Optional)

A companion desktop app provides Memory Browser, Session History, Cache Diagnostics, and Dreamer Management outside OpenCode. Available for macOS, Windows, Linux from the [GitHub releases page](https://github.com/cortexkit/magic-context/releases).

### Desktop App features
- **Memory Browser** — view all project memories, search, edit, delete
- **Session History** — browse past sessions per project
- **Cache Diagnostics** — inspect cache state, pending ops
- **Dreamer Management** — trigger and monitor dreamer runs
- **Log Viewer** — streaming logs for debugging
- **System tray** — background status indicator
- **Config Editor** — edit `magic-context.jsonc` visually

---

## See Also

- [Lean-ctx Guide](lean-ctx.md) — For shell/file compression
- [Memory Migration Plan](../memory-migration-plan.md) — Transitioning from mempalace to magic-context
