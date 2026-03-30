# Plan: Install opencode-session-recall

| | Created | Updated |
| ----------- | --------- | ---------
| **Status** | IN PROGRESS | -
| **Agent** | plan | -
| **Priority** | high | -

## Execution

| Timestamp | Step |
| --------- | -----
| 2026-04-15 22:30 | Created plan |

---

## Context

User wants to install opencode-session-recall plugin. This plugin enables searching through past OpenCode sessions that were lost to compaction.

**Current plugins:** ctx-mode, DCP, squeez, opencode-models-usage-plugin

---

## What session-recall does

- Searches past sessions that were compacted
- Cross-project and cross-session search
- Provides 5 tools to the agent: `recall`, `recall_sessions`, `search`, etc.
- Zero setup — no embeddings, no extra storage
- Works by reading OpenCode's internal database

---

## Installation Steps

### Step 1: Install the plugin

```bash
cd ~/.config/opencode && npm install opencode-session-recall
```

Or:

```bash
opencode plugin opencode-session-recall
```

### Step 2: Add to opencode.json

Edit `~/.config/opencode/opencode.json`:

```json
{
  "plugin": [
    "opencode-session-recall"
  ]
}
```

### Step 3: Restart OpenCode

Close and reopen OpenCode to load the plugin.

### Step 4: Verify

Run `ctx status` to confirm ctx-mode still working, then test the plugin by asking the agent to recall something from a past session.

---

## Configuration (Optional)

To disable cross-project search:

```json
{
  "plugin": [["opencode-session-recall", { "global": false }]]
}
```

---

## Decision Required

| Question | Answer |
| -------- | -------
| Install session-recall? | Pending user approval |

---

## Next Steps

- [ ] User approval to install
- [ ] Run installation commands
- [ ] Restart OpenCode
- [ ] Test by searching past sessions