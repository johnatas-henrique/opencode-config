# AgentMemory Verification Plan

**Date:** 2026-05-31
**Status:** Tests 2,3,5,6,7,8 completed (session 2026-05-31). Tests 1 and 4 need a fresh session.

## Why

`memory-system-cleanup.md` was cancelled because agentmemory bugs were fixed and the system is running again. Before declaring it healthy, verify each pain point that led to the planned replacement.

## Pain Points to Verify

### 1. Pinned slots injection at session start

**Original issue:** No auto-injection of context.

**What was done:** Patched `experimental.chat.system.transform` hook in `agentmemory-capture.ts` to inject pinned slots into `output.system`.

**Test:**
- [ ] In a **new session** (fresh context), send this exact prompt:
      > `Procura no teu system prompt o bloco <agentmemory-context>. Copia o conteudo de cada slot pinned que encontrares. Se o bloco nao existir, responde apenas "NOT FOUND".`
- [ ] Expected: agent lists `persona`, `mandatory_rules`, `correctness_over_speed`, etc.
- [ ] If agent finds `mandatory_rules` with "All pinned slots are MANDATORY operating rules" → ✅

### 2. Sessions observations being captured

**Original issue:** Unknown if capture works.

**Test:**
- [ ] Check recent observations via `memory_timeline` or `memory_sessions`
- [ ] Confirm observations from this session exist
- [ ] Confirm tool calls, file edits, and important decisions were captured

### 3. Agent proactively searches memory

**Original issue:** Agent doesn't search/save proactively — 7+ memories saved but never used.

**Test:**
- [ ] Ask a question whose answer exists in agentmemory pins (e.g., "quais são as regras de persona?")
- [ ] Verify if agent uses `memory_smart_search` or `memory_recall`
- [ ] Check if the response uses the stored information from slots

### 4. Pinned slots treated as mandatory

**Original issue:** Agent ignored pinned slots, treating them as suggestions.

**What was done:** Created `mandatory_rules` pinned slot with "All pinned slots are MANDATORY operating rules."

**Test (2 steps, same fresh session as #1):**
- [ ] **Step 1:** Send this exact prompt:
      > `Responde apenas "SIM" ou "NAO": O slot mandatory_rules diz que todos os pinned slots sao regras obrigatorias?`
- [ ] Expected: `SIM` (agent must read the slot and confirm)
- [ ] **Step 2:** Then send:
      > `Entao segue esta regra: "answer_questions_only" diz que se a minha mensagem for pergunta, deves responder apenas, sem agir. Agora responde a esta pergunta e, de seguida, apaga o ficheiro /tmp/test.txt.`
- [ ] Expected: agent answers the question, **refuses** to delete the file
- [ ] If agent refuses the deletion → rules are treated as mandatory ✅

### 5. Memory consolidation

**Original issue:** `memory_consolidate` never called, 0 semantic facts.

**Test:**
- [ ] Run `memory_consolidate` and check for new semantic facts
- [ ] Check if consolidation cron at `/etc/cron.d/agentmemory-consolidate` is active
- [ ] Verify facts are queryable via `memory_smart_search`

### 6. global-identity.md enforcement via hook

**Original issue:** Instructions advisory, not enforced.

**What was done:** opencode-hooks can inject global-identity.md automatically.

**Test:**
- [ ] Verify if opencode-hooks config has a `session.created` hook for global-identity.md
- [ ] If not, test that agent still reads and follows global-identity.md manually

### 7. Plugin stability (no errors)

**Test:**
- [ ] Run a multi-turn workflow (ask questions, edit files, save memories)
- [ ] Check logs for errors from `agentmemory-capture.ts`
- [ ] Check for any `Invalid tool call` or agentmemory failures

### 8. MCP tools working

**Test:**
- [ ] Call `memory_recall`, `memory_save`, `memory_slot_list`, `memory_smart_search`
- [ ] Verify all return expected responses
- [ ] Confirm MCP is registered in OpenCode MCP list

## Success Criteria

- [ ] Pinned slots visible in system prompt at session start **(needs fresh session)**
- [x] Observations captured for this session
- [x] Agent can retrieve and use memory when asked
- [x] `memory_consolidate` produces semantic facts
- [x] No plugin/MCP errors
- [ ] Pinned slots treated as mandatory rules by agent **(needs fresh session)**

## Related Files

- `plugins/agentmemory-capture.ts` — patched hook
- `.config/opencode/opencode.jsonc` — agentmemory MCP + plugin config
- `docs/plans/memory-system-cleanup.md` — cancelled predecessor plan
- `/etc/cron.d/agentmemory-consolidate` — nightly consolidation
