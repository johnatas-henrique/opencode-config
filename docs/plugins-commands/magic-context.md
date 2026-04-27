# Magic Context Commands & Tools

**Status:** ✅ Active
**Purpose:** Infinite context via cache-aware chat compression, cross-session memory, and background historian.
**Documentation:** https://github.com/cortexkit/opencode-magic-context

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `/ctx-status` | TUI | Debug view: tags, drops, cache TTL, historian progress, compartment coverage |
| `/ctx-flush` | TUI | Force all queued reduction operations immediately |
| `/ctx-recomp` | TUI | Rebuild compartments and facts from raw history |
| `/ctx-aug` | TUI | Run sidekick augmentation (retrieve relevant memories) |
| `/ctx-dream` | TUI | Run dreamer maintenance now (instead of waiting for schedule) |
| `ctx_reduce(drop)` | MCP (Agent) | Mark content for removal to shed context weight |
| `ctx_expand(start, end)` | MCP (Agent) | Expand compressed history range back to raw messages |
| `ctx_memory(...)` | MCP (Agent) | Cross-session memory CRUD (automatic) |
| `ctx_knowledge(...)` | MCP (Agent) | Project knowledge management (automatic) |

---

## User Commands (TUI)

Type these in the chat to interact with Magic Context:

| Command | Description |
|---------|-------------|
| `/ctx-status` | **Debug view.** Shows: §N§ tags, pending drops, cache TTL, nudge state, historian progress, compartment coverage, history compression budget. |
| `/ctx-flush` | **Force cleanup.** Immediately executes all queued reduction operations, bypassing cache TTL. Use when context is bloated. |
| `/ctx-recomp` | **Rebuild state.** Reconstructs compartments and facts from raw history. Use if stored state seems corrupted or inconsistent. |
| `/ctx-aug` | **Sidekick augmentation.** Runs the sidekick model to retrieve relevant memories and inject them into your current prompt. Enhances context with project history. |
| `/ctx-dream` | **Manual dreamer.** Triggers the dreamer maintenance immediately (instead of waiting for scheduled 5 AM run). Consolidates memories, deduplicates, promotes facts. |

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
| `ctx_memory(action, ...)` | Cross-session memory CRUD (internal use via automatic injections). |
| `ctx_knowledge(action, ...)` | Project knowledge management (facts, patterns, decisions). |

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

## Configuration

**File:** `magic-context.jsonc` (global: `~/.config/opencode/magic-context.jsonc` or per-project)

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/cortexkit/opencode-magic-context/master/assets/magic-context.schema.json",
  "enabled": true,

  "historian": {
    "model": "openrouter/elephant-alpha",
    "fallback_models": [
      "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
      "openrouter/google/gemma-4-31b-it:free"
    ]
  },

  "dreamer": {
    "enabled": true,
    "model": "openrouter/google/gemma-4-31b-it:free",
    "schedule": "0 5 * * *"  // Cron: daily at 5:00 AM
  },

  "sidekick": {
    "enabled": false  // Set true to auto-augment prompts
  }
}
```

### Model Selection

- **historian**: Should be high-quality (we use `elephant-alpha`, 256k context, free on OpenRouter).
- **dreamer**: Can be smaller/cheaper (we use `gemma-4-31b-it:free`).
- Models must support tool calling.

---

## How It Works

1. **Tagging:** Every message, tool output, and file attachment gets a `§N§` tag (monotonic counter).
2. **Compartments:** Related tags are grouped into compartments (conversation turns, tasks).
3. **Historian:** A background model compresses old compartments into summaries, preserving core information. Original messages are kept but marked as compressible.
4. **Cache-aware:** Operations are deferred to avoid wasting prompt cache. Reductions happen when cache expires or context pressure is high.
5. **Dreamer:** Runs overnight to consolidate scattered memories, deduplicate, and promote recurring patterns to "facts".
6. **Sidekick (optional):** Can auto-augment prompts with relevant project memories.

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

---

## Troubleshooting

### Historian not running?

Check sidebar status. If stuck, try `/ctx-dream` to manually trigger.

### State seems corrupted?

Rebuild from raw history: `/ctx-recomp`

### High token usage despite compression?

Verify `compaction.auto: false` in `opencode.json` (Magic Context manages its own compaction).

---

## Desktop App (Optional)

A companion desktop app provides Memory Browser, Session History, Cache Diagnostics, and Dreamer Management outside OpenCode. Available for macOS, Windows, Linux from the GitHub releases page.

---

## See Also

- [Lean-ctx Guide](lean-ctx.md) — For shell/file compression
- [Session Recall](session-recall.md) — For searching past sessions
