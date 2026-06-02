# DCP — Dynamic Context Pruning

**Status:** ✅ Installed
**Purpose:** Context pruning — compress, deduplicate, purge errors. Replaces magic-context.
**Repository:** https://github.com/Tarquinen/opencode-dynamic-context-pruning

---

## Slash Commands

| Command | Description |
|---------|-------------|
| `/dcp` | Show available commands |
| `/dcp context` | Token usage breakdown by category |
| `/dcp stats` | Cumulative pruning statistics |
| `/dcp sweep [N]` | Prune last N tool outputs (default: all) |
| `/dcp manual [on/off]` | Toggle manual mode |
| `/dcp compress [focus]` | Trigger compression manually |
| `/dcp decompress [ID]` | Restore a compression by ID |
| `/dcp recompress [ID]` | Re-apply a decompressed compression |

## Config

**File:** `~/.config/opencode/dcp.jsonc` (auto-created on first run)

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/Opencode-DCP/opencode-dynamic-context-pruning/master/dcp.schema.json",
  "enabled": true,
  "autoUpdate": true,
  "pruneNotification": "minimal",
  "pruneNotificationType": "chat",
  "compress": {
    "mode": "range",
    "permission": "allow",
    "maxContextLimit": "60%",
    "minContextLimit": "50%",
    "summaryBuffer": true,
    "nudgeFrequency": 5,
    "iterationNudgeThreshold": 15,
    "nudgeForce": "soft",
    "modelMaxLimits": {
      "opencode-go/deepseek-v4-pro": "15%",
      "opencode-go/deepseek-v4-flash": "15%",
      "opencode-go/qwen3.7-max": "15%",
      "opencode-go/mimo-v2-pro": "15%",
      "opencode-go/mimo-v2.5-pro": "15%",
      "opencode-go/mimo-v2.5": "15%"
    }
  },
  "strategies": {
    "deduplication": { "enabled": true },
    "purgeErrors": { "enabled": true, "turns": 4 }
  }
}
```

## What DCP does

| Feature | Description |
|---------|-------------|
| Auto-compress | Compresses old conversation spans at 60%+ context |
| Deduplication | Removes duplicate tool outputs automatically |
| Purge errors | Clears errored tool inputs after 4 turns |
| Per-model limits | Different thresholds per model provider |
| Manual mode | Full control via `/dcp` commands |

## What DCP does NOT do

- No memory system (agentmemory handles this)
- No git commit indexing (was magic-context only)
- No background agents/dreamer/historian
- No TUI sidebar (no plugin in tui.json)
- No cross-session memory injection

## Rollback (restore magic-context)

See [magic-context.md](magic-context.md) for instructions.

## See Also

- [Magic Context Guide](magic-context.md) — rollback reference
- [AgentMemory Guide](agentmemory.md) — memory system
