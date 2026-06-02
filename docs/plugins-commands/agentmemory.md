# Agentmemory Commands & Tools

**Status:** ✅ Installed — MCP, plugin, e server estão configurados e rodando

**Purpose:** Persistent cross-session memory via 22 OpenCode hooks + 53 MCP tools. Auto-captures decisions, patterns, bugs, and facts.
**Repository:** https://github.com/rohitg00/agentmemory
**Documentation:** https://github.com/rohitg00/agentmemory/blob/main/plugin/opencode/README.md

---

## Dashboard Tabs (12 abas confirmadas via Playwriter)

| # | Tab | O que mostra |
|---|-----|-------------|
| 1 | **DASHBOARD** | Métricas gerais: compress, summarize, tokens saved, system resources, recent sessions |
| 2 | **GRAPH** | Knowledge graph visual de conceitos e relações |
| 3 | **MEMORIES** | Facts salvos via `memory_save` — title, type, strength, version |
| 4 | **TIMELINE** | Observações de uma sessão específica, filtradas por importância |
| 5 | **SESSIONS** | Lista de sessões com project, status, obs count |
| 6 | **LESSONS** | Heuristics portáteis (always/never/prefer/avoid) com confidence scores |
| 7 | **ACTIONS** | Tarefas pendentes: pending → active → done/blocked |
| 8 | **CRYSTALS** | Snapshots comprimidos de trabalho completado |
| 9 | **AUDIT** | Operações de governance (delete, evolve, consolidate) |
| 10 | **ACTIVITY** | Atividade recente do sistema |
| 11 | **PROFILE** | Perfil auto-gerado: top concepts, files, conventions, project stats |
| 12 | **REPLAY** | Import JSONL de sessões passadas |

---

## Curadoria: Onde salvar cada tipo de memória

### O que entra automaticamente no system prompt

| Tipo | Tool | Como injeta |
|------|------|-------------|
| **Pinned Slots** | `memory_slot_create(scope="global")` | Sempre presente em todas as sessões |
| **Project Profile** | Auto-gerado | Análise automática de observations |
| **Lessons** | `memory_lesson_save` (sem project) | Injetadas em todos os projetos |
| **Session Summaries** | Auto-gerado | Últimas 10 sessões do projeto |

### O que só é recuperável via busca

| Tipo | Tool | Recuperável via |
|------|------|-----------------|
| **Memories** | `memory_save` | `memory_smart_search` / `memory_recall` |
| **Actions** | `memory_action_create` | Busca manual |
| **Crystals** | `memory_crystallize` | Busca manual |
| **Observations** | Capturadas por hooks | Busca manual |

### Mapa de curadoria

| Quer controlar                  | Onde curar no dashboard        | Tool                               |
| -------------------------------- | ------------------------------ | ---------------------------------- |
| O que **SEMPRE** aparece no prompt  | Criar **SLOT**                     | `memory_slot_create(scope="global")` |
| Lições que aparecem no prompt   | Criar **LESSON**                   | `memory_lesson_save` (sem project)   |
| Memórias recuperáveis via busca | Criar **MEMORY**                   | `memory_save`                        |
| Perfil do projeto               | Auto-gerado (aba PROFILE)     | —                                |
| Ações pendentes                 | Criar **ACTION**                   | `memory_action_create`               |
| Snapshots de sessão             | Criar **CRYSTAL**                  | `memory_crystallize`                 |

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
| `memory_slot_create(...)` | MCP | Create editable memory slot (scope: project/global) |
| `memory_slot_replace(...)` | MCP | Replace slot content |
| `memory_slot_list(...)` | MCP | List all slots (pinned + project + global) |
| `memory_action_create(...)` | MCP | Create a tracked action item |
| `memory_action_update(...)` | MCP | Update action status/priority |
| `memory_crystallize(...)` | MCP | Compress completed actions into crystal digest |

---

## Slash Commands

| Command | Description |
|---------|-------------|
| `/recall <query>` | **Search memory.** Calls `memory_smart_search` (BM25 + vector + graph, limit 10) + `memory_lesson_recall` (limit 5). Groups by session, shows type/title/narrative, highlights importance ≥ 7. Suggests alternative terms if empty. |
| `/remember <text>` | **Save memory.** Extracts core insight, 2-5 specific concepts, and file paths. Calls `memory_save` with `content`, `concepts`, `files`, and `type` (pattern/preference/architecture/bug/workflow/fact). Confirms with tagged concepts. |

---

## Agent Tools (MCP)

These tools are exposed via the agentmemory MCP server and used by the LLM agent automatically or on demand. All tools use the `agentmemory_memory_` prefix.

### Core Memory Tools

| Tool | Purpose |
|------|---------|
| `memory_save(content, concepts, type, files)` | Save an insight, decision, or fact. **NOT injected automatically** — only retrievable via search. |
| `memory_recall(query)` | Search past observations by keyword. Use when user says "recall", "what did we do", "do you remember". |
| `memory_smart_search(query, limit)` | Hybrid semantic + keyword search with progressive disclosure. Use for fuzzy/conceptual searches. |
| `memory_sessions(limit)` | List recent sessions with status and observation counts. Use when user asks about past sessions. |
| `memory_file_history(filePath)` | Get past observations about specific files across all sessions. Use before editing a file. |

### Lessons

| Tool | Purpose |
|------|---------|
| `memory_lesson_save(content, context, confidence, project, tags)` | Save a lesson learned. **Always include `context`** (where/when it applies) — the dashboard shows it inline and reinforces when to use it. **Omit `project` for global lessons**. |
| `memory_lesson_recall(query)` | Search lessons sorted by confidence. Use before making a decision. |

### Slots (Memory Injection)

| Tool | Purpose |
|------|---------|
| `memory_slot_create(label, content, scope, pinned)` | Create editable memory slot. **Use `scope: "global"` for always-present memories.** |
| `memory_slot_replace(label, content)` | Replace slot content in place. |
| `memory_slot_list()` | List all slots (pinned + project + global). |

### Actions & Crystals

| Tool | Purpose |
|------|---------|
| `memory_action_create(title, description, priority, project)` | Create a tracked action item. |
| `memory_action_update(actionId, status, result)` | Update action status (pending/active/done/blocked/cancelled). |
| `memory_crystallize(actionIds, project, sessionId)` | Compress completed actions into crystal digest. |

### Consolidation & Governance

| Tool | Purpose |
|------|---------|
| `memory_consolidate(tier, force)` | Run the 4-tier memory consolidation pipeline to compress and organize observations. |
| `memory_governance_delete(memoryId)` | Delete specific memories. Requires explicit user confirmation. |
| `memory_patterns(concept)` | Detect recurring patterns across sessions. Use for project-level trends. |

---

## System Prompt Injection

The plugin uses `experimental.chat.system.transform` to inject context automatically:

**First call each session (via `/session/start` → `mem::context`):**
1. **Pinned Slots** — slots with `pinned="true"` (global + project)
2. **Project Profile** — top concepts, key files, conventions (auto-generated from observations)
3. **Lessons** — global lessons (no project) + project-specific lessons
4. **Session Summaries** — resumos das últimas 10 sessões

**Injected via `system.transform` hook:**
5. Agentmemory tool usage instructions (`agentmemory_memory_*`)

**Every file-touching call:**
6. File-enriched context: past observations about the files being edited

```
System prompt = [OpenCode instructions] + [agentmemory instructions] + [pinned slots] + [profile] + [lessons] + [session summaries] + [file enrichment] + [user message]
                       ^                           ^                      ^                ^           ^                ^                    ^                ^
                   always                     1x per session          1x per session   1x per session  1x per session    1x per session     every file-touching turn
```

### ⚠️ Importante: `memory_save` NÃO é injetado automaticamente

Memórias salvas via `memory_save` ficam armazenadas mas **não aparecem no system prompt**. Só são recuperadas quando o agent busca explicitamente via `memory_smart_search` ou `memory_recall`.

Para ter memórias **sempre presentes**, use:
- `memory_slot_create(scope="global")` — para memórias editáveis
- `memory_lesson_save` (sem project) — para lições globais

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
- **Viewer:** http://localhost:3113 — dashboard with 12 tabs

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AGENTMEMORY_URL` | `http://localhost:3111` | agentmemory server URL |
| `AGENTMEMORY_SECRET` | `""` | Authentication token |
| `OPENCODE_AGENTMEMORY_DEBUG` | (disabled) | `=1` for debug console logs |
| `CONSOLIDATION_ENABLED` | `true` | Auto-crystallization at session end |
| `AGENTMEMORY_REFLECT` | `true` | Auto-reflection (clusters of lessons) |

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

## See Also

- [Magic Context Guide](magic-context.md)
- [Simple Memory Guide](simple-memory.md)
- [Lean-ctx Guide](lean-ctx.md)
