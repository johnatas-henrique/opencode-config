# OpenCode Stack Cleanup Plan

**Date:** 2026-05-28
**Status:** Draft - pending review

---

## Context

Review of the OpenCode setup revealed several inconsistencies, redundant tools, and underutilized features. This plan addresses them in priority order.

---

## Phase 1: Quick Wins (no risk, immediate benefit)

### 1.0 Remove safety-git.md and merge important rules

**Why:** safety-git.md has 17 lines, most redundant with AGENTS.md or generic advice. Only 2 rules are unique and important (no force-push, no --no-verify).

**Analysis:**
- Line 5 (propagate failures) — redundant with AGENTS.md line 26
- Lines 6-9 (safety/infrastructure) — generic, rarely relevant
- Lines 12-14 (git/PRs) — generic, could be in constraints.md
- Lines 15-16 (no force-push, no --no-verify) — important, must keep

**Files to modify:**
- `docs/agent-instructions/safety-git.md` — remove file
- `opencode.jsonc` — remove from instructions array
- `docs/agent-instructions/constraints.md` — add Git safety rules

**Rules to migrate:**
```markdown
## Git Safety
- Do not force-push to main/master.
- Do not use `--no-verify` or `--no-gpg-sign`.
```

**Impact:** -1 instruction file, -10 lines of redundant/generic instructions, important rules preserved.

### 1.1 Remove gitnexus MCP + skills

**Why:** AFT already covers call graph, impact analysis, code exploration, refactoring, and search. GitNexus skills are redundant.

**Files to modify:**
- `opencode.jsonc` — remove `gitnexus` from `mcp` (disabled entry)
- `~/.config/opencode/skills/` — remove directories: `gitnexus-cli`, `gitnexus-debugging`, `gitnexus-exploring`, `gitnexus-guide`, `gitnexus-impact-analysis`, `gitnexus-pr-review`, `gitnexus-refactoring`
- `docs/agent-instructions/gitnexus.md` — remove file

**Impact:** 7 skill directories + 1 instruction file + 1 MCP config entry removed.

### 1.2 Remove playwright MCP

**Why:** Playwriter is preferred (uses user's own browser, handles logins/captchas). Playwright MCP is redundant.

**Files to modify:**
- `opencode.jsonc` — remove `playwright` from `mcp`

**Impact:** 1 MCP config entry removed.

### 1.3 Enable Python LSP in AFT

**Why:** User uses Python sometimes. Python LSP is currently disabled in AFT config.

**Files to modify:**
- `aft.jsonc` — remove `"python"` from `lsp.disabled`

**Impact:** Python files get LSP diagnostics after edits.

### 1.4 Clean up disabled MCPs

**Why:** Remove `fff` and `markitdown` from config since they're not actively used. markitdown can be re-enabled via CTRL+P toggle when needed.

**Files to modify:**
- `opencode.jsonc` — remove `fff` and `markitdown` from `mcp`

**Impact:** Cleaner config, no functional change.

### 1.5 Fix permission config (remove dead config)

**Why:** Research revealed that `permission.external_directory` does **not exist** in OpenCode's permission system. The entire block is being silently ignored. The bash permission patterns (`"*/dev/null*": "allow"`) are also ignored because the system only supports exact tool names, not glob patterns.

**How OpenCode permissions actually work:**
- Only `permissions.allowed_tools` is recognized (array of tool names like `["bash"]`)
- Bash tool has a built-in safe-command list (`echo`, `ls`, `git status`, etc.) that auto-approves
- Commands not in the safe list trigger a permission prompt
- There is no file-level or directory-level permission granularity

**Options:**
1. **Allow all bash** — `"permissions": { "allowed_tools": ["bash"] }` — simplest, no prompts, but least safe
2. **Keep current behavior** — accept permission prompts for non-safe bash commands
3. **Use `--yolo` flag** — skips all permission prompts entirely

**Recommendation:** Option 2 (keep current). The prompts are a safety net. The `2>/dev/null` annoyance is minor compared to the risk of allowing all bash commands.

**Files to modify:**
- `opencode.jsonc` — remove `permission.external_directory` block (dead config), remove bash glob patterns (ignored), keep only valid config

**Current:**
```json
"permission": {
  "external_directory": {
    "*": "ask",
    "/tmp": "allow",
    "/tmp/*": "allow"
  },
  "bash": {
    "*": "allow",
    "*/dev/null*": "allow",
    ...
  }
}
```

**Target:**
```json
"permission": {
  "bash": {
    "*": "allow"
  }
}
```

**Impact:** Cleaner config. Removes false sense of security from dead config blocks. Permission prompts still appear for non-safe bash commands (including `2>/dev/null`).

---

## Phase 2: AFT Tool Usage Analysis (needs investigation)

### 2.1 Problem

agentmemory logs show errors like:
- `"Invalid tool call: af_search"` — agente errou o nome (deveria ser `aft_search`)
- `"Invalid tool call: 'outline'"` — agente usou nome genérico (deveria ser `aft_outline`)

Isso indica que o agente não está usando as ferramentas AFT corretamente.

### 2.2 AFT tools disponíveis vs uso real

| Tool               | Função                          | Uso esperado                | Status           |
| ------------------ | ------------------------------- | --------------------------- | ---------------- |
| `aft_zoom`             | Inspecionar símbolos            | Antes de editar função      | Desconhecido     |
| `aft_outline`          | Estrutura de arquivos           | Explorar código             | Erros registrados|
| `aft_navigate`         | Call graph, impact analysis     | Antes de mudar assinatura   | Desconhecido     |
| `aft_search`           | Busca híbrida semantic/lexical  | Encontrar código            | Erros registrados|
| `aft_refactor`         | Move/extract/inline             | Refatoração                 | Desconhecido     |
| `aft_import`           | Gerenciar imports               | Após mover funções          | Desconhecido     |
| `aft_safety`           | Undo/checkpoints               | Antes de edição arriscada   | Desconhecido     |
| `aft_transform`        | Add members/derives/decorators  | Modificações estruturais    | Desconhecido     |
| `aft_conflicts`        | Ver conflitos git              | Durante merge               | Desconhecido     |
| `edit` (AFT-hoisted)   | Find/replace, symbol replace   | Edições de código           | Parece funcionar |
| `read` (AFT-hoisted)   | Leitura de arquivos            | Leitura básica              | Parece funcionar |
| `grep` (AFT-hoisted)   | Busca indexed                  | Busca literal               | Parece funcionar |
| `glob` (AFT-hoisted)   | Busca por padrão               | Encontrar arquivos          | Parece funcionar |

### 2.3 Ações

1. **Medir uso real** — consultar agentmemory para contagem de tool calls AFT vs tools nativas (read, edit, grep, glob) nas últimas sessões
2. **Verificar se o problema é instrução** — o `mcp-tools.md` instrui "AFT is the primary code tool" mas pode não ser específico o suficiente
3. **Corrigir documentação** — garantir que os nomes das tools estão corretos nas instruções

### 2.4 Resultado

- **Teste:** Todas as ferramentas AFT dedicadas funcionam (aft_search, aft_outline, aft_navigate, aft_zoom)
- **Causa do não-uso:** Comportamental — agente erra nomes ou prefere ferramentas nativas
- **Ação tomada:** Instruções em mcp-tools.md fortalecidas com regras MANDATORY e FALLBACK ONLY
- **Decisão:** Manter ferramentas AFT, aceitar que agente usa nativas como fallback

---

## Phase 3: Token Analysis (needs measurement)

### 3.1 Analyze startup token cost

**Current state:** Session starts at ~30k tokens (OpenCode system prompt ~10-12k + instructions + plugins).

**Action:** Measure token cost of each component:
- OpenCode base system prompt (fixed, ~10-12k)
- AGENTS.md content
- Each of the 11 agent-instruction files
- Plugin injections (agentmemory-capture, magic-context, AFT)
- Skill definitions loaded at startup

**Tool:** Use `ctx_search` or manual token counting to estimate each component.

**Decision point:** If total exceeds 20k tokens from instructions/plugins alone, consider converting some to on-demand skills.

### 3.2 Identify instructions that could be on-demand skills

**Candidates for conversion to skills (loaded only when needed):**
- `testing.md` — only relevant when writing tests
- `output.md` — could be merged into `writing-style.md`
- `cross-session-memory.md` — only relevant when using agentmemory actively

**Keep as always-loaded (core behavior):**
- `global-identity.md` — mandatory startup actions
- `process.md` — decision-making framework
- `workflow.md` — execution patterns
- `mcp-tools.md` — tool selection rules
- `constraints.md` — change scope rules
- `safety-git.md` — security boundaries
- `writing-style.md` — response format

---

## Phase 4: agentmemory Usage Fix (→ moved to memory-system-cleanup.md)

**Status:** MOVED — This phase has been moved to a dedicated plan file: `docs/plans/memory-system-cleanup.md`

**Summary:** Investigation revealed that agentmemory captures data but doesn't inject context automatically. The agent doesn't search memory proactively. The plan now covers replacing agentmemory with claude-mem (or opencode-mem) for auto-save + auto-inject via hooks, with a separate opencode-hook for global-identity.md injection.

---

## Phase 5: magic-context → DCP (config changed — awaiting test)

**Status:** Configs updated, DCP installed — not yet tested in a session.

### Why magic-context was replaced

Magic-context had 2 plugin entries (opencode.jsonc + tui.json), causing duplicates.
Even with `memory/dreamer/historian disabled`, it still tried to run them (noise).
DCP is a single plugin focused only on context pruning — no memory, no agents, no duplicate TUI entry.

### What was done

| File | Action |
|------|--------|
| `opencode.jsonc` | Replaced `@cortexkit/opencode-magic-context` with `@tarquinen/opencode-dcp` |
| `tui.json` | Removed `@cortexkit/opencode-magic-context` (no replacement needed — DCP doesn't have TUI) |
| `dcp.jsonc` | Created with config below |
| `magic-context.md` | Rewritten as rollback reference |
| `dcp.md` | Created as new documentation |

### DCP config (`dcp.jsonc`)

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
    "showCompression": false,
    "summaryBuffer": true,
    "maxContextLimit": "60%",
    "minContextLimit": "50%",
    "modelMaxLimits": {
      "opencode-go/deepseek-v4-pro": "15%",
      "opencode-go/deepseek-v4-flash": "15%",
      "opencode-go/qwen3.7-max": "15%",
      "opencode-go/mimo-v2-pro": "15%",
      "opencode-go/mimo-v2.5-pro": "15%",
      "opencode-go/mimo-v2.5": "15%"
    },
    "nudgeFrequency": 5,
    "iterationNudgeThreshold": 15,
    "nudgeForce": "soft"
  },
  "strategies": {
    "deduplication": { "enabled": true },
    "purgeErrors": { "enabled": true, "turns": 4 }
  }
}
```

### Rollback (if needed)

1. Remove `@tarquinen/opencode-dcp` from `opencode.jsonc` plugin array
2. Re-add `@cortexkit/opencode-magic-context` to both `opencode.jsonc` and `tui.json`
3. Delete or revert `dcp.jsonc`
4. See `docs/plugins-commands/magic-context.md` for original config

---

## Phase 6: Instruction Files Cleanup

### 6.1 Current state

10 instruction files, ~4.251 tokens total. Several duplications and overlaps identified.

| Arquivo                 | Tokens | Decisão     |
| ----------------------- | ------ | ----------- |
| AGENTS.md               | ~407   | Manter      |
| global-identity.md      | ~547   | Editar      |
| process.md              | ~330   | Manter      |
| workflow.md             | ~374   | Editar      |
| mcp-tools.md            | ~862   | Manter      |
| testing.md              | ~144   | Manter      |
| constraints.md          | ~127   | Manter      |
| output.md               | ~149   | Remover     |
| writing-style.md        | ~436   | Editar      |
| cross-session-memory.md | ~495   | Remover     |

### 6.2 Duplications resolved

#### "Perguntar antes de agir"

| Arquivo            | Linha | Ação                           |
| ------------------ | ----- | ------------------------------ |
| AGENTS.md          | —     | Adicionar regra "always ask"   |
| global-identity.md | 13    | Remover (movido para AGENTS)   |
| process.md         | 5-8   | Manter (detalhamento)          |

**Decisão:** Regra "always ask when in doubt" vai em AGENTS.md (maior prioridade). process.md mantém o detalhamento.

#### "Sem filler / Direto"

| Arquivo          | Ação                    |
| ---------------- | ----------------------- |
| AGENTS.md        | Manter (regra geral)    |
| output.md        | Remover                 |
| writing-style.md | Adicionar regras de output |

**Decisão:** Mesclar output.md em writing-style.md. Regras de "completion" voltam para process.md.

#### "Memória / Lessons"

| Arquivo                 | Ação    |
| ----------------------- | ------- |
| global-identity.md      | Remover linha 5 (agentmemory) |
| workflow.md             | Remover seção "Memory and lessons" |
| cross-session-memory.md | Remover arquivo |

**Decisão:** Tudo removido com agentmemory.

### 6.3 Conflicts resolved

#### Proatividade

| Arquivo            | Linha | Conflito                                    | Resolução                    |
| ------------------ | ----- | ------------------------------------------- | ---------------------------- |
| global-identity.md | 12    | "Do not be proactive in actions that modify" | Manter                       |
| workflow.md        | 20    | "After discovery, actively save it"          | Remover (é agentmemory)      |

**Decisão:** Conflito resolvido com remoção do agentmemory.

### 6.4 Files to modify

#### AGENTS.md — adicionar regra de pergunta

Adicionar na seção "Boundaries":
```markdown
- Always ask when in doubt — prefer one targeted question over assumptions.
```

#### global-identity.md — remover agentmemory

- Remover linha 5: "Call `agentmemory_memory_smart_search`..."
- Remover linha 7: referência a cross-session-memory.md

#### workflow.md — remover seção de memória

- Remover linhas 18-24: "Memory and lessons" (é sobre agentmemory)

#### output.md — remover arquivo

- Regras de estilo → writing-style.md
- Regras de completion → process.md

#### writing-style.md — adicionar regras de output

Adicionar:
```markdown
## Completion

Before declaring completion, confirm the change solves the stated problem, relevant validation ran or gaps are stated, no known unintended side effects were introduced, and no secrets were added or exposed.

## Response Format

Be concise and specific by default. No filler, intros, or restated requirements.

Answer direct questions directly when possible. Example: `npm test`, not `The command to run tests is npm test.`

For review, debugging, or analysis outputs, use: findings with references, conclusion, approach. Mention caveats and unverified risks.
```

#### cross-session-memory.md — remover arquivo

Removido completamente com agentmemory.

### 6.5 Resultado

| Métrica             | Antes    | Depois   | Economia |
| ------------------- | -------- | -------- | -------- |
| Arquivos            | 10       | 8        | -2       |
| Tokens              | ~4.251   | ~3.427   | ~824     |
| Economia            | —        | —        | 19%      |

**Arquivos removidos:**
- output.md (mesclado em writing-style.md)
- cross-session-memory.md (removido com agentmemory)

**Arquivos editados:**
- AGENTS.md (adicionada regra "always ask")
- global-identity.md (removido agentmemory)
- workflow.md (removida seção de memória)
- writing-style.md (adicionadas regras de output)

---

## Phase 7: Writing Style Optimization (no action needed)

### 7.1 Analysis

writing-style.md has 12 lines, ~436 tokens. The question was whether to split into core rules (always loaded) vs detailed rules (on-demand).

### 7.2 Decision

**No split.** writing-style.md is core behavior — the agent should always write with these rules. Splitting would give incomplete instructions. The 236 token savings isn't worth the complexity.

### 7.3 Testing.md as on-demand skill (rejected)

Converting testing.md (~144 tokens) to a skill was considered but rejected. User wants it always loaded since all test projects are in TS.

---

## Investigation: agentmemory Consolidation

### Findings

**Persistence:** State IS persisted to disk. `iii-config.yaml` uses `store_method: file_based` with `file_path: ./data/state_store.db` and `save_interval_ms: 5000`. Verified — files are being written every ~5 seconds.

**Data loss (23-28 May):** Two possible causes:
1. Bug documented in PR #304 — API silently buffered in RAM, returned `success: true`, state evaporated on container restart. Fixed in v0.9.22.
2. Upgrade to v0.9.24 may have changed the working directory.

**Consolidation:** `memory_consolidate` tool exists but was never called. Dashboard shows 0 semantic facts. After manual test call: 12 semantic facts extracted, 76% token savings.

**iii-cron:** Worker is listed in `iii-config.yaml` (line 26-29) but no triggers registered. Worker exists but does nothing.

**iii-database:** NOT needed — state already persists via `file_based` adapter.

### iii Worker Analysis

| Worker         | Recommendation | Reason                                          |
| -------------- | -------------- | ----------------------------------------------- |
| iii-cron       | **Install**        | Register nightly trigger for consolidation      |
| iii-database   | Skip           | State already persists via `file_based` adapter |
| iii-queue      | Skip           | NVIDIA NIM timeouts resolved                    |
| iii-pubsub     | Skip           | Single-instance, not needed                     |
| iii-observability | Skip       | Viewer already covers metrics                   |
| iii-sandbox    | Skip           | No code recall execution                        |

### Consolidation Command

`memory_consolidate({})` WITHOUT project parameter consolidates ALL projects. Confirmed by code (line 5612: `data.project ? sessions.filter(...) : sessions`) and test (12→28 semantic facts).

### iii-cron Configuration

**Frequency:** Once daily at 2am is sufficient.

- Consolidation uses LLM — running 6x/day wastes tokens
- Decay is 30 days — no benefit to frequent runs
- Documentation recommends "nightly" schedule

**Problem:** `iii worker add iii-cron` FAILS with "Release asset not found" because agentmemory pins iii-engine to v0.11.2, but iii-cron requires v0.11.6+.

**Solution:** Linux crontab instead of iii-cron:

```bash
# crontab -e
0 2 * * * curl -s -X POST http://localhost:3111/tools/memory_consolidate -H "Content-Type: application/json" -d '{}' > /dev/null 2>&1
```

No project list needed — `memory_consolidate({})` handles all projects automatically.

---

## Future Improvement: Auto-create Actions and Lessons

### Problem

The agentmemory plugin captures observations and consolidates them into semantic facts, but **never creates actions or lessons automatically**. This leaves the dashboard with 0 actions and 0 lessons, even with 1918 observations and 45 semantic facts.

The pipeline is stuck:

```
0 actions → 0 crystals → 0 lessons → 0 reflections → 0 insights
```

### Root cause

The plugin (`agentmemory-capture.ts`) is purely an observation capture layer. It has zero calls to `memory_action_create` or `memory_lesson_save`. The server-side consolidation pipeline creates insights and procedural knowledge, but not actions or lessons.

### Proposed solution (for plugin maintainer)

Add auto-detection logic in the plugin's `PostToolUse` hook:

1. **Detect recurring patterns** — if the same error or task appears 3+ times across observations
2. **Auto-create action** — call `memory_action_create` with detected pattern as title
3. **Auto-mark done** — when the pattern stops appearing, mark action as done
4. **Let auto-crystallize work** — server extracts lessons from completed actions automatically

### Benefits

- Populates actions and lessons without agent intervention
- Enables the full memory pipeline (actions → crystals → lessons → insights)
- Makes the dashboard more useful

### MCP tools involved

| Tool                    | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| `memory_action_create`    | Create action from detected pattern      |
| `memory_action_update`    | Mark action as done when pattern resolves |
| `memory_crystallize`      | Extract lessons from completed actions   |
| `memory_lesson_save`      | Direct lesson save (alternative)         |

---

## Execution Order

1. **Phase 1** — Quick wins ✅ (gitnexus, playwright, Python LSP, MCP cleanup)
2. **Phase 2** — AFT tool usage ✅ (analysis + mcp-tools.md updated)
3. **Phase 3** — Token analysis ✅ (instruction files analyzed)
4. **Phase 4** — agentmemory → memory-system-cleanup.md (separate plan)
5. **Phase 5** — magic-context → DCP (config changed 2026-05-31, awaits test session)
6. **Phase 6** — Instruction files cleanup ✅ (implemented)
7. **Phase 7** — Writing style optimization ✅ (no action needed)
8. **Consolidation cron** — Linux crontab: `0 2 * * * curl ...` (pending user setup)

---

## Success Criteria

- [x] gitnexus removed (MCP + 7 skills + instruction file)
- [x] playwright MCP removed
- [x] Python LSP enabled in AFT
- [x] Unused MCPs cleaned from config
- [x] AFT tool usage measured and documented
- [x] Instruction files analyzed (duplications, conflicts, merges identified)
- [x] mcp-tools.md updated (gh_grep, exa, webfetch rules)
- [x] /dev/null investigation completed (permission system limitation documented)
- [x] AGENTS.md updated (removed /dev/null prohibition, fixed broken references)
- [x] Phase 7: Writing style optimization (no split needed, core behavior)
- [x] Phase 6: Instruction files cleanup (implemented)
- [x] Consolidation command verified: `memory_consolidate({})` consolidates all projects
- [ ] Phase 5: DCP replacement (config changed, needs testing)
- [x] Consolidation cron: Linux crontab created in /etc/cron.d/agentmemory-consolidate
