# Memória Cross-Session no OpenCode — Análise e Diagnóstico

**Data:** 2026-05-15
**Propósito:** Mapear o estado atual da memória entre sessões, avaliar abordagens existentes e recomendar caminhos de melhoria

---

## Sumário

- [Estado Atual](#1-estado-atual)
- [Problema Central](#2-problema-central)
- [Abordagens Avaliadas](#3-abordagens-avaliadas)
- [Comparação](#4-comparação)
- [Recomendação](#5-recomendação)
- [Dúvida sobre Mempalace](#6-dúvida-sobre-mempalace)

---

## 1. Estado Atual

### O Que Já Está Funcionando

| Componente      | Status       | Função                                                    |
| --------------- | ------------ | --------------------------------------------------------- |
| **magic-context**  | ✅ Ativo     | Compressão de chat + histórico (memory.enabled: false)    |
| **RTK**           | ✅ Ativo     | Compressão de output bash (plugin local)                  |
| **AFT**           | ✅ Ativo     | Edição/navegação/refatoração AST-aware                    |
| **mempalace**     | ✅ Ativo     | MCP server de memória persistente (grafo)                 |
| **opencode-hooks** | 🚀 Publicando | Backbone de eventos — intercepta 100+ eventos OpenCode    |

### O Que Está Instalado Mas Não Carregado

| Componente        | Localização       | Status              |
| ----------------- | ----------------- | ------------------- |
| session-recall    | `package.json`    | ⏳ npm instalado, não carregado |
| telegram-bot      | npm global        | ⏳ Instalado, não configurado   |

### O Que Nunca Funcionou

| Abordagem Anterior | Problema                                  |
| ------------------ | ----------------------------------------- |
| context-mode       | Substituído por magic-context             |
| DCP                | Substituído por RTK (compressão melhor)   |
| lean-ctx/tokenscope | Substituído por RTK                      |
| simple-memory      | Nunca chegou a ser integrado              |
| mempalace plugin   | Plugin OpenCode quebrado (bug exportSessionTranscript) |

---

## 2. Problema Central

**Não há captura automática de informações úteis entre sessões.**

O que existe hoje:

```
Sessão A                     Sessão B
   │                            │
   │ magic-context               │ magic-context
   │ comprime histórico          │ comprime histórico
   │ (só pra caber no ctx)       │ (só pra caber no ctx)
   │                            │
   └─── mempalace ──────────────┘
        manual (só se o usuário pedir)
```

O ideal:

```
Sessão A                     Sessão B
   │                            │
   │ hook: session.next.*        │ hook: session.created
   │ → extrai decisões           │ → busca memórias relevantes
   │ → armazena em mempalace     │ → injeta no system prompt
   │                            │
   └─── mempalace ──────────────┘
        pipeline automático
```

**Gaps identificados:**

1. **Extração:** Nada captura decisões, arquivos alterados, blockers, ou descobertas durante a sessão
2. **Sumarização:** Output bruto de ferramentas não é destilado em informação útil
3. **Indexação:** Memórias existem no mempalace mas sem embeddings ou busca semântica
4. **Recuperação:** Nada carrega contexto relevante no início da sessão
5. **Ciclo de vida:** Memórias nunca expiram, nunca são consolidadas, nunca viram "documento"

---

## 3. Abordagens Avaliadas

### 3.1 Memory Bank MCP

MCP server que mantém arquivos markdown estruturados no diretório do projeto.

**Arquivos padrão:**
- `projectbrief.md` — objetivos, escopo, visão
- `productContext.md` — por que o projeto existe
- `systemPatterns.md` — arquitetura, padrões de design
- `techContext.md` — stack, setup, constraints
- `activeContext.md` — foco atual, mudanças recentes, próximos passos
- `progress.md` — o que funciona, milestones

**Prós:**
- Simplicidade máxima. Arquivos no git. Zero infraestrutura
- Complementa mempalace: mempalace guarda o grafo, memory bank guarda documentos
- Versionado — cada commit é um checkpoint da memória do projeto

**Contras:**
- Manual — depende do agente lembrar de ler/escrever
- Sem busca semântica — leitura de arquivo exato
- Sem compressão — arquivos crescem linearmente

**Integração com OpenCode:** Adicionar ao `mcp` no `opencode.jsonc`. Pode ser invocado por regra no AGENTS.md.

---

### 3.2 open-mem

(`github.com/clopca/open-mem`) Plugin nativo OpenCode com pipeline completo de memória.

**Arquitetura:**
1. **Captura:** Lifecycle hooks do OpenCode capturam cada sessão automaticamente
2. **Compressão:** LLM destila output bruto em observações tipadas (decisão, bugfix, feature, refactor)
3. **Armazenamento:** SQLite com 3 índices paralelos:
   - FTS5 full-text search
   - sqlite-vec vector search (embeddings)
   - Grafo de conhecimento local (entidades e relações)
4. **Recuperação:** Progressive disclosure — índice comprimido (~96%) é injetado no system prompt; agente vê o que existe e decide o que buscar
5. **Dashboard web:** Timeline, busca, estatísticas

**Prós:**
- Automático — zero intervenção manual
- Híbrido — 3 modalidades de busca (texto, vetor, grafo)
- Offline — tudo local, sem dependência cloud
- Progressive disclosure — eficiência de tokens (~96% compressão)
- Imutabilidade — observações têm lineage revision (nunca perde dados)

**Contras:**
- Custo de embedding (OpenAI/Voyage) por chunk
- Outro plugin externo na pilha
- open-mem tem seu próprio grafo — concorre com mempalace

**Integração:** `bunx open-mem install` — registro automático de hooks + MCP tools.

---

### 3.3 Mem0

(`mem0ai/mem0`) Camada de memória para LLMs com SDKs Python/TypeScript + MCP server.

**Pipeline:**
1. **ADD-only extraction:** Uma chamada LLM extrai memórias da conversa — nada é sobrescrito
2. **Entity linking:** Entidades (nomes próprios, termos compostos) são extraídas e linkadas
3. **Multi-signal retrieval:** 3 sinais em paralelo:
   - Semântico (vector similarity)
   - BM25 keyword matching
   - Entity matching (graph boost)
4. **Fusão por RRF** (Reciprocal Rank Fusion)

**Prós:**
- Melhor acurácia em benchmarks (92.5% LoCoMo)
- Suporte a 30 vector stores, 4 graph stores, 15 embedding models
- MCP server + plugins para Claude Code, Cursor, Codex
- SOC 2, HIPAA compliance

**Contras:**
- Poder total (graph memory) é cloud-only: $249/mês
- Self-hosted requer vector DB + graph DB
- SDK open-source recentemente removeu suporte a graph store
- Overkill para uso pessoal

**Integração:** Adicionar MCP server `mcp.mem0.ai` ao `opencode.jsonc`.

---

### 3.4 codexfi

Plugin nativo OpenCode com memória tipada e refresh semântico a cada turno.

**Características:**
- 13 categorias de memória (project brief, architecture, tech context, etc.)
- Refresh semântico a cada turno — a seção "relevante para tarefa atual" é re-buscada a cada chamada LLM
- Cross-scope: memórias do projeto + do usuário, mescladas em ranking único
- Embeddings Voyage `voyage-code-3` (1024-dim), otimizado para código
- Desduplicação inteligente (cosine similarity) e versionamento relacional
- Memória injetada no system prompt — sobrevive a truncamento

**Prós:**
- Nativo OpenCode
- Refresh a cada turno = contexto sempre fresco
- Estrutura tipada facilita busca precisa

**Contras:**
- Requer API key Voyage (embedding) + LLM de extração = custo contínuo
- Outra dependência externa
- Custo de tokens por refresh (a cada turno)

**Integração:** `bunx codexfi install` — setup automático.

---

### 3.5 opencode-hooks como Plataforma de Memória

Usar o próprio opencode-hooks como backbone de eventos para alimentar mempalace.

**Pipeline proposto:**

```
evento OpenCode → hook opencode-hooks → script TS → mempalace MCP

Exemplos:
- session.next.text.ended → extrair decisões do turno → armazenar no mempalace
- file.edited → registrar diff resumido no grafo
- tool.execute.after (write) → registrar arquivo criado/modificado
- session.created → carregar memórias relevantes do mempalace → injetar no prompt
- session.idle → comprimir observações do turno, arquivar
```

**Hooks do opencode-hooks que seriam usados:**

| Evento OpenCode                          | Uso na Memória                                      |
| ---------------------------------------- | --------------------------------------------------- |
| `session.created`                        | Carregar contexto relevante de sessões anteriores   |
| `session.next.text.ended`                | Extrair decisões, descobertas, blockers              |
| `session.next.tool.called`               | Registrar ferramentas usadas e resultados            |
| `tool.execute.after` (bash/write/read)   | Capturar outputs e arquivos alterados               |
| `file.edited`                            | Registrar arquivos modificados                      |
| `session.idle` / `session.next.retried`  | Consolidar estado, comprimir observações            |
| `experimental.chat.system.transform`     | Injetar memórias relevantes no system prompt        |
| `experimental.session.compacting`        | Extrair últimas informações antes da compactação    |

**Prós:**
- **Código próprio** — zero dependência externa
- Já intercepta todos os eventos do OpenCode (100+)
- opencode-hooks + mempalace = já tem tudo que precisa
- Pipeline completo sem novos plugins
- Escalável — começa com um hook e vai refinando

**Contras:**
- Precisa construir a lógica de extração e sumarização
- Precisa escrever scripts TS para cada tipo de extração
- Integração MCP (mempalace) via chamadas tool — latência potencial

---

## 4. Comparação

| Critério              | Memory Bank | open-mem | Mem0  | codexfi | hooks + mempalace |
| --------------------- | ----------- | -------- | ----- | ------- | ----------------- |
| **Setup**                 | 5 min       | 5 min    | 30 min | 5 min  | Já tem           |
| **Automático**            | ❌          | ✅      | ✅    | ✅     | ⚠️ (precisa construir) |
| **Offline**               | ✅          | ✅      | Parcial | ✅   | ✅               |
| **Busca semântica**       | ❌          | ✅      | ✅    | ✅     | ⚠️ (depende do mempalace) |
| **Custo contínuo**        | Zero        | API emb  | $$     | $$     | Zero             |
| **Código próprio**        | ❌          | ❌      | ❌    | ❌     | ✅               |
| **Dependências novas**    | MCP server  | Plugin   | MCP    | Plugin  | Nenhuma          |
| **Git-friendly**          | ✅          | ❌      | ❌    | ❌     | ❌               |
| **Controle fino**         | Baixo       | Médio   | Médio  | Médio  | Total            |

---

## 5. Recomendação

### Abordagem por Camadas

Considerando que você já tem opencode-hooks (publicando hoje) e mempalace (já rodando), a recomendação é uma **estratégia em 3 camadas** sem adicionar dependências:

```
Camada 1 — Fundação (já existe)
├── opencode-hooks → backbone de eventos
├── mempalace      → storage persistente
└── magic-context  → compressão de histórico

Camada 2 — Pipeline de Captura (construir)
├── hook session.next.text.ended
│   → extrair decisões/descobertas
│   → armazenar no mempalace
├── hook file.edited
│   → registrar diff no grafo
└── hook tool.execute.after
    → registrar outputs relevantes

Camada 3 — Recuperação (construir)
├── hook session.created
│   → buscar memórias relevantes no mempalace
│   → injetar no system prompt
└── hook experimental.chat.system.transform
    → enriquecer prompt com contexto histórico
```

### Por que essa abordagem

1. **Zero novas dependências** — tudo roda sobre o que já existe
2. **Código próprio** — se algo falha, você conserta (vs. esperar autor de plugin)
3. **Mempalace já funciona** — só precisa ser alimentado automaticamente
4. **Escalável** — começa pequeno e refina
5. **Portável** — se amanhã aparecer uma lib melhor, você conecta via MCP sem mudar arquitetura

### Se preferir第三条 via com plugin externo

**open-mem** é o que chega mais perto do ideal:
- Automático de verdade (captura sem intervenção)
- Híbrido vector + FTS5 + grafo
- Progressive disclosure (~96% compressão)
- Offline, sem dependência cloud
- Único custo é embedding API

Mas adiciona outro grafo que concorre com mempalace.

---

## 6. Dúvida sobre Mempalace

Sua intuição sobre o mempalace ser o ponto fraco faz sentido pelos seguintes motivos:

### O que o mempalace FAZ BEM

- Armazenamento persistente via MCP (funciona)
- Grafo de conhecimento com entidades e relações
- Busca semântica via embeddings
- Túneis entre projetos

### O que o mempalace NÃO FAZ

| Funcionalidade                     | Aberto no seu setup              | Por que é crítico                 |
| ---------------------------------- | -------------------------------- | --------------------------------- |
| **Captura automática**                 | Nada captura                     | Memória só existe se alguém pedir |
| **Extração de decisões**               | Nenhum processo                  | Output bruto não vira insight     |
| **Sumarização**                        | Nenhum processo                  | Informação não é destilada        |
| **Injeção no prompt**                  | Nenhum processo                  | Agente não vê o passado           |
| **Ciclo de vida (expurgo/consolidação)** | Nenhum processo                  | Memória acumula sem qualidade     |
| **Progressive disclosure**             | Nenhum processo                  | Toda memória é jogada de uma vez  |
| **Integração com eventos OpenCode**    | Nenhuma — é só MCP server        | Não reage ao que acontece         |

### A causa raiz

O mempalace é uma **ferramenta de armazenamento**, não um **sistema de memória**. Ele guarda o que você joga nele e recupera quando você pede — mas não há:

1. **Quem colete** → falta o opencode-hooks alimentando eventos
2. **Quem extraia** → falta um processo de destilação (LLM comprimindo raw data → observação)
3. **Quem entregue** → falta injeção automática no início da sessão

**Sem essas 3 peças, o mempalace é uma biblioteca vazia.**

### O que fazer

A boa notícia: opencode-hooks tem os hooks certos pra construir essas 3 peças. O mempalace como storage é adequado — o que falta é o pipeline em volta dele. 

**Diagnóstico final:** Mempalace não é o problema. O problema é que não há pipeline de eventos conectado a ele.
