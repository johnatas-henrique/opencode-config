# Plan: Reactivate DCP (Dynamic Context Pruning)

| | Created | Updated |
| -- | -- | -- |
| **Status** | pending | - |
| **Agent** | plan | - |
| **Priority** | high | - |

## Context

User wants to reactivate DCP to manage context window (chat history, tool outputs). This complements lean-ctx which handles shell/file output compression.

## Why DCP

- Lean-ctx compresses **tool outputs** (shell, file reads)
- DCP compresses **chat context** (conversation history)
- They work together without conflict

## Configuration (percentage-based)

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/Opencode-DCP/opencode-dynamic-context-pruning/master/dcp.schema.json",
  "enabled": true,
  "pruneNotification": "detailed",
  "pruneNotificationType": "chat",
  "compress": {
    "mode": "range",
    "permission": "allow",
    "showCompression": false,
    "summaryBuffer": true,
    "maxContextLimit": "80%",
    "minContextLimit": "40%",
    "nudgeFrequency": 5,
    "nudgeForce": "soft"
  },
  "strategies": {
    "deduplication": { "enabled": true },
    "purgeErrors": { "enabled": true, "turns": 4 }
  }
}
```

### Why 80%/40%

- 80% max: aggressive enough to keep context low
- 40% min: starts nudges to compress
- Works for any model (128k, 200k, 1M, etc.)

## Execution

| Timestamp | Step |
| -- | -- |
| - | Install DCP: `opencode plugin @tarquinen/opencode-dcp@latest --global` |
| - | Update dcp.jsonc with config above |
| - | Restart OpenCode |
| - | Test: `/dcp context` to see token breakdown |

## DCP Commands

| Command | Purpose |
| -- | -- |
| `/dcp context` | Show token usage by category |
| `/dcp stats` | Cumulative pruning statistics |
| `/dcp sweep [n]` | Prune last N tools |
| `/dcp compress [focus]` | Trigger compression |
| `/dcp manual on/off` | Toggle manual mode |

## What DCP Does

1. **Compress tool** — Replaces old messages with summaries
2. **Deduplication** — Removes duplicate tool calls
3. **Purge errors** — Removes errored tool inputs after 4 turns
4. **Nudges** — Reminds model to compress when near limit

## Lean-ctx + DCP Together

| Feature | lean-ctx | DCP |
| -- | -- | -- |
| Shell compression | ✅ | ❌ |
| File read compression | ✅ | ❌ |
| Chat context compression | ❌ | ✅ |
| Auto-dedupe | ✅ (file re-reads) | ✅ (tool calls) |
| Slash commands | ❌ | ✅ (/dcp) |

## Trade-offs

### Prompt Caching

DCP modifies messages → may invalidate prompt cache.
- Cache hit: ~85-90% without DCP → ~85% with DCP
- Trade-off: less tokens vs fewer cache hits

Usually worth it for long sessions.

## Notes

- Default protected tools: `task`, `skill`, `todowrite`, `todoread`, `compress`, `batch`, `plan_enter`, `plan_exit`, `write`, `edit`
- `protectUserMessages: false` (default) means your messages can be compressed
- Set to `true` if you want to preserve all your messages

## Summary Checklist

- [ ] Install DCP: `opencode plugin @tarquinen/opencode-dcp@latest --global`
- [ ] Update ~/.config/opencode/dcp.jsonc
- [ ] Restart OpenCode
- [ ] Test with `/dcp context`