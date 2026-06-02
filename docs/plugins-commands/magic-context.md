# Magic Context — Rollback Reference

**Status:** ❌ Removed (2026-05-31) — replaced by [DCP](dcp.md)
**Purpose:** This file exists only for rollback. Do not reference for active use.

---

## To restore magic-context

### 1. Update `~/.config/opencode/opencode.jsonc`

Replace DCP entry with magic-context in the `plugin` array:

```diff
-    "@tarquinen/opencode-dcp@latest",
+    "@cortexkit/opencode-magic-context@latest",
```

### 2. Update `~/.config/opencode/tui.json`

Add magic-context back:

```diff
+    "@cortexkit/opencode-magic-context@latest",
```

### 3. Delete or disable DCP config

```bash
rm ~/.config/opencode/dcp.jsonc
```

### 4. Previous config (for reference)

**`magic-context.jsonc`** — file still present but inactive:

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/cortexkit/magic-context/master/assets/magic-context.schema.json",
  "enabled": true,
  "memory": {
    "enabled": false,
    "injection_budget_tokens": 4000,
    "auto_promote": true
  },
  "embedding": {
    "provider": "local"
  },
  "ctx_reduce_enabled": true,
  "execute_threshold_percentage": 60,
  "execute_threshold_tokens": {
    "opencode-go/deepseek-v4-pro": 150000,
    "opencode-go/deepseek-v4-flash": 150000,
    "opencode-go/qwen3.7-max": 150000,
    "opencode-go/mimo-v2-pro": 150000,
    "opencode-go/mimo-v2.5-pro": 150000,
    "opencode-go/mimo-v2.5": 150000
  },
  "auto_drop_tool_age": 25,
  "nudge_interval_tokens": 10000,
  "commit_cluster_trigger": {
    "enabled": true,
    "min_clusters": 1
  },
  "historian": { "disable": true },
  "dreamer": { "disable": true },
  "sidekick": { "disable": true }
}
```

### 5. Why it was replaced

- Two plugin entries (opencode.jsonc + tui.json) — duplicate loading
- Dreamer/historian kept trying to run despite `disable: true`
- Memory injection was inconsistent
- DCP is lighter and single-plugin
