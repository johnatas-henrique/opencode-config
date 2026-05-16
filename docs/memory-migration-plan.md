# Memory Architecture Migration Plan

## Diagnóstico: gargalos atuais

| Componente            | Latência | Problema                                                         |
| --------------------- | -------- | ---------------------------------------------------------------- |
| `mempalace wake-up`     | 1.252s   | Lê identity.txt (1863 bytes) via Python. `cat` faz em 0.002s     |
| `mempalace mine`        | 2.5s     | `opencode export` + ChromaDB embedding. Roda a cada 5 mensagens  |
| `mempalace exit`        | 2.5s     | Mesmo custo do mine, roda no fim da sessão                       |

**Causa raiz:** mempalace usa ChromaDB (Python) + modelo de embedding no hot path. Para session memory, é desnecessariamente pesado.

## Solução: magic-context (já instalado) + identity.txt puro

### Troca: mempalace mine → magic-context memory

| Funcionalidade         | Antes (mempalace)                | Depois (magic-context)          |
| ---------------------- | -------------------------------- | ------------------------------- |
| Project memory capture | `mempalace mine` a cada 5 msg       | Historian automático em background |
| Storage                | ChromaDB (56MB, vetores)         | SQLite in-process (FTS5 + vec)  |
| Cura                   | Manual (`mempalace_delete_drawer`)  | Dreamer noturno + Desktop App   |
| Latência               | 2.5s no hot path                 | 0.02ms por turno                |
| Injeção                | Manual (wake-up script)          | `<project-memory>` automático     |

### Troca: mempalace wake-up → cat identity.txt

| Funcionalidade    | Antes (mempalace wake-up) | Depois (cat)             |
| ----------------- | ------------------------- | ------------------------ |
| Ler identity.txt  | 1.252s (via Python)       | 0.002s                  |
| Ler project wing  | Sim (L1 do mempalace)     | Não (magic-context faz) |

## Config analysis by key

### 🟥 Must change (memory doesn't work without)

| Key | Current | New | Reason |
|-----|---------|-----|--------|
| `memory.enabled` | `false` | `true` | Without this, `ctx_memory` is hidden, no `<project-memory>` injection |
| `embedding.provider` | `"off"` | `"local"` | "off" = keyword search only. No semantic ranking for memory injection |
| `dreamer.enabled` | `false` | `true` | Without dreamer, historian observations accumulate but are never promoted to stable memories |

### 🟡 Recommended (aligned with short-session workflow)

| Key | Current | Recommended | Reason |
|-----|---------|-------------|--------|
| `memory.injection_budget_tokens` | _missing_ | `4000` | Budget for memory injection in system prompt. Default | |
| `memory.auto_promote` | _missing_ | `true` | Auto-promote session facts to project memories after historian runs |
| `dreamer.tasks` | _missing_ | `["consolidate","verify","archive-stale","improve"]` | Official default. Without tasks, dreamer doesn't know what to do |
| `commit_cluster_trigger.min_clusters` | _missing_ | `1` (default 3) | Historian fires after each commit batch instead of waiting for 3 clusters |
| `nudge_interval_tokens` | `5000` | `10000` (default) | 5000 fires nudges too frequently |

### 🔵 Optional (consider later)

| Key | What it does | When to enable |
|-----|-------------|----------------|
| `git_commit_indexing.enabled: true` | Indexes HEAD commits for semantic search via `ctx_search` | Now — zero latency cost |
| `auto_search.enabled: true` | Background memory scan on each user message, adds hint | Later, if you feel recall is missing |
| `dreamer.user_memories.enabled: true` | Historian observes your behavior, dreamer promotes patterns | Later, can create noise initially |
| `sidekick.enabled: true` | `/ctx-aug` command to fetch memories and inject briefing | Not needed — you use natural language |

### ⚪ Keep as-is

| Key | Value | Why |
|-----|-------|-----|
| `ctx_reduce_enabled` | `true` | Agent auto-drops old tool outputs |
| `execute_threshold_percentage` | `60` | Your choice, good middle ground |
| `auto_drop_tool_age` | `50` | Standard threshold |
| Historian/dreamer models | current | Already configured |

## O que muda na configuração

### 1. `magic-context.jsonc` (~/.config/opencode/)

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/cortexkit/magic-context/master/assets/magic-context.schema.json",
  "enabled": true,
  "memory": {
    "enabled": true,
    "injection_budget_tokens": 4000,
    "auto_promote": true
  },
  "embedding": {
    "provider": "local"
  },
  "dreamer": {
    "enabled": true,
    "tasks": [
      "consolidate",
      "verify",
      "archive-stale",
      "improve"
    ]
  },
  "execute_threshold_percentage": 60
}
```

### 2. Identity.txt (mover para config global)

```
~/.mempalace/identity.txt  →  ~/.config/opencode/identity.txt
```

Conteúdo permanece o mesmo.

### 3. Scripts do opencode-hooks

| Script                    | Ação     | Novo comportamento             |
| ------------------------- | -------- | ------------------------------ |
| `session-created.sh`        | MANTER   | Contexto de projeto (branch, sprint, bugs) |
| `session-stop.sh`           | MANTER   | Log de sessão pra audit trail  |
| `mempalace-wake.sh`         | ADAPTAR  | Substituir `mempalace wake-up` por `cat ~/.config/opencode/identity.txt` |
| `mempalace-mine.sh`         | REMOVER  | Redundante (magic-context memory substitui) |
| `mempalace-exit.sh`         | REMOVER  | Redundante                     |
| `mempalace-pre-compact-hook.sh` | REMOVER | Redundante                  |

Wake-up adaptado:

```bash
GLOBAL_IDENTITY=$(cat ~/.config/opencode/identity.txt 2>/dev/null)
echo "=== GLOBAL INSTRUCTIONS ==="
echo "$GLOBAL_IDENTITY"
echo "==========================="
```

### 4. Remover scripts dos hooks (não deletar arquivos)

Editar `opencode-hooks.jsonc`:

| Evento | Remover script |
|--------|---------------|
| `server.instance.disposed` | `mempalace-exit.sh` |
| `session.created` | `mempalace-wake.sh` (substituir por wake novo) |
| `session.deleted` | `mempalace-exit.sh` |
| `experimental.session.compacting` | `mempalace-wake.sh` |
| `chat.message` | `mempalace-mine.sh` |

Os arquivos `.sh` continuam no disco. Só param de ser chamados.

### 5. Dados antigos do mempalace

- ChromaDB (`~/.mempalace/palace/`) permanece no disco
- `mempalace search "termo"` continua funcionando para consultas históricas
- Novas memórias vão para o SQLite do magic-context
- `/ctx-recomp` **não lê mempalace** — ele reprocessa o raw history do OpenCode, não dados externos
- Migração manual possível: agente lê mempalace drawers via MCP (`mempalace_search`, `mempalace_list_drawers`) e escreve como `ctx_memory(write)`

## Fluxo de trabalho recomendado

```
SESSÃO LONGA (uma por projeto, semanas)
  │
  ├── INÍCIO
  │   ├── opencode-hooks session.created → contexto do projeto
  │   └── cat identity.txt → regras globais (0.002s)
  │
  ├── DURANTE
  │   ├── Historian extrai memórias (background, automático)
  │   ├── <project-memory> injetado a cada turno
  │   ├── ctx_memory(action="write") para regras explícitas em PT-BR
  │   └── /ctx-dream para consolidar na hora (opcional)
  │
  ├── ANTES DE HANDOFF
  │   └── /ctx-recomp (opcional, se quiser 100% de cobertura)
  │
  └── PRÓXIMA SESSÃO
      └── <project-memory> já carregado automaticamente
```

## Gestão de memórias

| Ação                    | Como fazer                                                     |
| ----------------------- | -------------------------------------------------------------- |
| **Listar memórias**     | `ctx_memory(action="list")` (via agente)                       |
| **Apagar memória ruim** | "Apague a memória com ID Y" (agente faz `delete`)              |
| **Salvar regra explícita** | "Salva como memória: sempre fazer X quando Y" (agente faz `write`) |
| **Curar automaticamente**   | Dreamer noturno (consolida, verifica, arquiva)                 |
| **Curar manualmente**       | Desktop App → Memory Browser → search/edit/delete              |
| **Inspecionar memórias**    | Desktop App ou `/ctx-status`                                    |

## Prioridade de regras

```
identity.txt (suas instruções explícitas)  →  PRIORIDADE MÁXIMA
ctx_memory(write) (regras que você ditou)   →  PRIORIDADE ALTA
<project-memory> (observações do historian) →  PRIORIDADE BAIXA
```

## Por que não usar outras abordagens

| Abordagem         | Motivo da rejeição                          |
| ----------------- | ------------------------------------------- |
| ECC (session-end.sh) | Só captura no fim, sem busca semântica   |
| fmflurry instinct | Só salva observação, sem injeção automática |
| chroma-local      | Mesmo problema do mempalace (Python lento)  |
| mem0 cloud        | Dependência de cloud, não roda local        |
