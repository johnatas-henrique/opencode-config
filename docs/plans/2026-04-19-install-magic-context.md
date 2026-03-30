# Plan: Install Magic Context

| | Created | Updated |
| -- | -- | -- |
| **Status** | pending | - |
| **Agent** | build | - |
| **Priority** | high | - |

## Context

Magic Context (cortexkit/opencode-magic-context) é um plugin OpenCode que combina:
- Chat context compression (historian background)
- Tool output management (ctx_reduce)
- Cross-session memory (ctx_memory)
- Live TUI sidebar com breakdown de tokens
- Daily dreamer maintenance (5h da manhã)

Este plugin complementa lean-ctx (shell/file compression), não substitui.

## Current Setup (manter)

| Plugin  | Status | Função                              |
| -------- | -------- | ------------------------------------ |
| lean-ctx | ✅ Ativo | Shell output + file read compression |

## What Will Be Added

| Plugin               | Status   | Função                                |
| --------------------- | -------- | -------------------------------------- |
| magic-context        | Novo     | Chat compression + TUI sidebar        |
| DCP (opencode-dcp)   | Mantém   | Como backup (não instalar agora)      |
| tokenscope           | Removido | Não precisa (TUI substitui)           |

## Status

| | |
| -- | -- |
| **Status** | ✅ completed |

| Timestamp | Step |
| -- | -- |
| 2026-04-18 22:00 | Install Magic Context plugin |
| 2026-04-18 22:01 | Update opencode.json (disable compaction) |
| 2026-04-18 22:02 | Create magic-context.jsonc with elephant-alpha model |
| 2026-04-18 22:03 | Test TUI sidebar |
| 2026-04-18 22:04 | Verify dreamer schedule |

## Installation Options

### Option 1: Script (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/cortexkit/opencode-magic-context/master/scripts/install.sh | bash
```

### Option 2: Manual

```bash
opencode plugin @cortexkit/opencode-magic-context --global
```

## Free Models Analysis

### Best Options (OpenRouter, Free Tier)

| Model | Context | Size | Provider | Status |
|-------|---------|------|----------|--------|
| **openrouter/elephant-alpha** | 256k | 100B | OpenRouter | ✅ Recommended |
| nvidia/nemotron-3-super-120b-a12b:free | 256k | 120B MoE | OpenRouter | Backup |
| google/gemma-4-31b-it:free | 256k | 31B MoE | OpenRouter | Backup |

### Why elephant-alpha?
- 256k context window
- 100B parameters (high quality)
- Completely free on OpenRouter
- Best cost/performance ratio

---

## Configuration

### opencode.json

Add OpenRouter provider and disable built-in compaction (Magic Context manages it):

```json
{
  "plugin": ["@cortexkit/opencode-magic-context", ...existing plugins...],
  "provider": [
    {
      "name": "openrouter",
      "api_key": "$OPENROUTER_API_KEY",
      "base_url": "https://openrouter.ai/api/v1"
    }
  ],
  "compaction": {
    "auto": false,
    "prune": false
  }
}
```

### magic-context.jsonc (global or per-project)

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/cortexkit/opencode-magic-context/master/assets/magic-context.schema.json",
  "enabled": true,

  "historian": {
    "model": "openrouter/elephant-alpha",
    "fallback_models": ["openrouter/nvidia/nemotron-3-super-120b-a12b:free"]
  },

  "dreamer": {
    "enabled": true,
    "model": "openrouter/google/gemma-4-31b-it:free",
    "schedule": "0 5 * * *"
  },

  "sidekick": {
    "enabled": false
  }
}
```

### Config locations (merged, project overrides global)

1. `<project-root>/magic-context.jsonc`
2. `<project-root>/.opencode/magic-context.jsonc`
3. `~/.config/opencode/magic-context.jsonc`

## Important Notes

### Dreamer Schedule

- **Runs daily at 5:00 AM** (config: `"0 5 * * *"`)
- **Duration varies:** 5-60 min depending on project size/memories
- **RAM only during execution:** ~6GB when running, 0 otherwise
- **Can run manually:** `/ctx-dream` in OpenCode

### Historian

- **Runs on-demand** (not always running)
- **Triggers:** cache expiry (5min), threshold (65%), or when agent calls historian
- **Uses cloud model** (if configured) — faster than local

### TUI Sidebar

Shows live:
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

### lean-ctx Compatibility

Magic Context and lean-ctx work together:
- lean-ctx: compress shell output + file reads before sending to LLM
- Magic Context: compress chat history + provides TUI sidebar

They don't conflict.

### Ollama Setup (OPTIONAL - not needed with OpenRouter)

Only needed if you prefer local models instead of cloud:

1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull model: `ollama pull llama3:8b`
3. Config uses `ollama/llama3:8b` as model name

**Recommended:** Use OpenRouter instead (free, no local setup needed)

## Rollback Plan

If issues occur:

1. Remove plugin from opencode.json:
   ```json
   "plugin": [ ... without magic-context ... ]
   ```
2. Restore compaction:
   ```json
   "compaction": { "auto": true, "prune": true }
   ```
3. Uninstall: `npm uninstall -g @cortexkit/opencode-magic-context`

## Related Plans

- **DCP:** docs/plans/2026-04-18-reactivate-dcp.md (backup if Magic Context doesn't work)
- **lean-ctx:** Already installed (keep it)

## Summary Checklist

- [ ] Install Magic Context (script or opencode plugin)
- [ ] Add OpenRouter provider to opencode.json
- [ ] Update magic-context.jsonc with elephant-alpha model
- [ ] Set OPENROUTER_API_KEY environment variable
- [ ] Restart OpenCode
- [ ] Verify TUI sidebar
- [ ] Test `/ctx-status` command
- [ ] Schedule test: `/ctx-dream` (manual trigger)