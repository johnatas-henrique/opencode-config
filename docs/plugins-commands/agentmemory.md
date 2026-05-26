# Agentmemory Commands & Tools

**Status:** ⏳ Pending Installation
**Purpose:** Persistent cross-session memory via 22 OpenCode hooks + 53 MCP tools. Auto-captures decisions, patterns, bugs, and facts.
**Repository:** https://github.com/rohitg00/agentmemory
**Documentation:** https://github.com/rohitg00/agentmemory/blob/main/plugin/opencode/README.md

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|---|---|---|
| `/recall <query>` | Slash | Search past observations and lessons |
| `/remember <text>` | Slash | Save an insight to long-term memory |
| `memory_save(...)` | MCP | Save an insight/decision/fact to long-term memory |
| `memory_recall(...)` | MCP | Search past observations by keywords |
| `memory_smart_search(...)` | MCP | Hybrid semantic + keyword search with progressive disclosure |
| `memory_sessions(...)` | MCP | List recent sessions with status and observation counts |
| `memory_file_history(...)` | MCP | Get past observations about specific files |
| `memory_lesson_save(...)` / `memory_lesson_recall(...)` | MCP | Save and search lessons learned |
| `memory_patterns(...)` | MCP | Detect recurring patterns across sessions |
| `memory_consolidate(...)` | MCP | Run the 4-tier memory consolidation pipeline |
| `memory_governance_delete(...)` | MCP | Delete specific memories (requires confirmation) |

---

## Slash Commands

| Command | Description |
|---------|-------------|
| `/recall <query>` | **Search memory.** Calls `memory_smart_search` (BM25 + vector + graph, limit 10) + `memory_lesson_recall` (limit 5). Groups by session, shows type/title/narrative, highlights importance ≥ 7. Suggests alternative terms if empty. |
| `/remember <text>` | **Save memory.** Extracts core insight, 2-5 specific concepts, and file paths. Calls `memory_save` with `content`, `concepts`, `files`, and `type` (pattern/preference/architecture/bug/workflow/fact). Confirms with tagged concepts. |

---

## Agent Tools (MCP)

These tools are exposed via the agentmemory MCP server and used by the LLM agent automatically or on demand. All tools use the `agentmemory_memory_` prefix.

| Tool | Purpose |
|------|---------|
| `memory_save(content, concepts, type, files)` | Save an insight, decision, or fact. Use when user says "remember this", after discovering a bug, after an architectural decision. |
| `memory_recall(query)` | Search past observations by keyword. Use when user says "recall", "what did we do", "do you remember". |
| `memory_smart_search(query, limit)` | Hybrid semantic + keyword search with progressive disclosure. Use for fuzzy/conceptual searches. |
| `memory_sessions(limit)` | List recent sessions with status and observation counts. Use when user asks about past sessions. |
| `memory_file_history(filePath)` | Get past observations about specific files across all sessions. Use before editing a file. |
| `memory_lesson_save(content, concepts)` | Save a lesson learned (what worked, what to avoid). |
| `memory_lesson_recall(query)` | Search lessons sorted by confidence. Use before making a decision. |
| `memory_patterns(concept)` | Detect recurring patterns across sessions. Use for project-level trends. |
| `memory_consolidate(tier, force)` | Run the 4-tier memory consolidation pipeline to compress and organize observations. |
| `memory_governance_delete(memoryId)` | Delete specific memories. Requires explicit user confirmation. |

---

## System Prompt Injection

The plugin uses `experimental.chat.system.transform` to inject context automatically:

**First call each session:**
1. Agentmemory tool usage instructions (`agentmemory_memory_*`)
2. Memory context: project profile, recent session summaries, important observations

**Every file-touching call:**
3. File-enriched context: past observations about the files being edited

```
System prompt = [OpenCode instructions] + [agentmemory instructions] + [memory context] + [file enrichment] + [user message]
                      ^                           ^                        ^                    ^
                  always                     1x per session          1x per session     every file-touching turn
```

---

## Captured Events (22 Hooks)

| Event | Hook | What it captures |
|---|---|---|
| Session start | `session.created` | ID, title, version, project |
| Idle status | `session.status` | Summarization trigger |
| Compaction | `session.compacted` | Summarize + observe |
| Session end | `session.deleted` | End session, run consolidation |
| Session error | `session.error` | Error to memory |
| User prompt | `chat.message` | Text, attached files |
| Assistant response | `message.updated` | Model, tokens, cost, error |
| Message removed | `message.removed` | Undo tracking |
| Subagent started | `message.part.updated (subtask)` | ID, agent, prompt |
| Tool completed | `message.part.updated (tool completed)` | Name, input, output, duration |
| Tool error | `message.part.updated (tool error)` | Name, input, error |
| Step finished | `message.part.updated (step-finish)` | Cost, tokens |
| Reasoning | `message.part.updated (reasoning)` | Reasoning text |
| File edited | `file.edited` | File path |
| File in part | `message.part.updated (file)` | Mentioned file |
| Patch applied | `message.part.updated (patch)` | Hash, files |
| Compaction event | `message.part.updated (compaction)` | Auto or manual |
| Agent selected | `message.part.updated (agent)` | Agent name |
| API retry | `message.part.updated (retry)` | Attempt, error |
| Permission | `permission.updated / permission.replied` | Type, response |
| Task tracking | `todo.updated` | Completed and active tasks |
| Command executed | `command.executed` | Name, arguments |
| Model params | `chat.params` | Model, temperature, topP, limits |
| Config loaded | `config` | Theme, model, agents, MCPs, providers |

---

## Architecture

```
OpenCode ──22 hooks──▶ agentmemory-capture.ts ──POST──▶ agentmemory server (localhost:3111)
                                                            │
                                                        SQLite local
                                                   (data/state_store.db)
```

- **Server:** `npx @agentmemory/agentmemory` — port 3111, SQLite persistence
- **MCP:** `npx @agentmemory/mcp` — 53 tools for the agent to query
- **Plugin:** `agentmemory-capture.ts` — 22 native OpenCode hooks
- **Embeddings:** Local (no external API key)

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AGENTMEMORY_URL` | `http://localhost:3111` | agentmemory server URL |
| `AGENTMEMORY_SECRET` | `""` | Authentication token |
| `OPENCODE_AGENTMEMORY_DEBUG` | (disabled) | `=1` for debug console logs |

---

## Installation

```bash
# 1. Start the server (keep running in background)
npx @agentmemory/agentmemory

# 2. Configure MCP in ~/.config/opencode/opencode.json
#    Add:
#    "mcp": {
#      "agentmemory": {
#        "type": "local",
#        "command": ["npx", "-y", "@agentmemory/mcp"],
#        "enabled": true
#      }
#    }

# 3. Download capture plugin
mkdir -p ~/.config/opencode/plugins
curl -o ~/.config/opencode/plugins/agentmemory-capture.ts \
  https://raw.githubusercontent.com/rohitg00/agentmemory/main/plugin/opencode/agentmemory-capture.ts

# 4. Add plugin in ~/.config/opencode/opencode.json
#    "plugin": ["./plugins/agentmemory-capture.ts"]

# 5. Add slash commands
mkdir -p ~/.config/opencode/commands
curl -o ~/.config/opencode/commands/recall.md \
  https://raw.githubusercontent.com/rohitg00/agentmemory/main/plugin/opencode/commands/recall.md
curl -o ~/.config/opencode/commands/remember.md \
  https://raw.githubusercontent.com/rohitg00/agentmemory/main/plugin/opencode/commands/remember.md
```

---

## Comparison with magic-context

| Feature | agentmemory | magic-context |
|---|---|---|
| Auto-capture | 22 hooks | historian background |
| System prompt injection | ✅ (zero conversation tokens) | ✅ (via context) |
| Cross-session memory | ✅ 95.2% R@5 LongMemEval | ✅ SQLite + embeddings |
| Historian background | ❌ | ✅ |
| Dreamer overnight | ❌ | ✅ |
| Sidekick | ❌ | ✅ |
| ctx-reduce manual | ❌ | ✅ |
| Portable (other agents) | ✅ (MCP universal) | ❌ (OpenCode only) |
| External API key required | ❌ (local embeddings) | ❌ |
| Files in repository | ❌ (all in server) | ⚠️ `.opencode/magic-context/` |
| MCP tools available | 53 | ~10 |

---

## See Also

- [Magic Context Guide](magic-context.md)
- [Simple Memory Guide](simple-memory.md)
- [Lean-ctx Guide](lean-ctx.md)
