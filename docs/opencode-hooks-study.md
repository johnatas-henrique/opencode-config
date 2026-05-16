# OpenCode Hooks — Análise Completa do Projeto

**Data:** 2026-05-15
**Autor:** Análise automatizada do ecossistema OpenCode
**Propósito:** Documentar arquitetura, capacidades e integração do plugin `@johnatas-henrique/opencode-hooks`

---

## 1. Visão Geral

**OpenCode Hooks** é um sistema de plugins TypeScript para [OpenCode AI](https://opencode.ai) que fornece hooks orientados a eventos. Atua como uma camada de middleware entre o sistema interno de eventos do OpenCode e scripts shell definidos pelo usuário, notificações toast e auditoria.

| Campo           | Valor                                                   |
| --------------- | ------------------------------------------------------- |
| **Pacote npm**      | `@johnatas-henrique/opencode-hooks`                     |
| **Versão**          | 0.6.0                                                   |
| **Licença**         | MIT                                                     |
| **Entry Point**     | `./dist/index.mjs`                                      |
| **Types**           | `./dist/index.d.mts`                                    |
| **Autor**           | Johnatas Henrique (`johnatas.henrique@gmail.com`)      |
| **Repositório**     | `github.com/johnatas-henrique/opencode-hooks`           |
| **Build**           | `tsup` → ESM + `.d.mts`                                |
| **Testes**          | Vitest + `@vitest/coverage-v8` (99%+ cobertura)           |
| **CI/CD**           | GitHub Actions (lint, format, test, build) + Release Please |
| **npm publish**     | `prepublishOnly` → tsup build. Pacote escopo público         |

---

## 2. Estrutura de Arquivos

```
.opencode/plugins/
├── opencode-hooks.ts              # ENTRY POINT — exporta OpencodeHooks Plugin
├── config/
│   ├── defaults.ts                # Config padrão (todos eventos desabilitados)
│   ├── jsonc-loader.ts            # Carrega + mescla opencode-hooks.jsonc
│   └── runtime.ts                 # Singleton runtime (userConfig)
├── core/
│   ├── constants.ts               # DEFAULTS (toast timings, script dir, audit)
│   └── toast-queue.ts             # Singleton global de fila de toasts
├── types/
│   ├── core.ts                    # Enum OpenCodeEvents (100+ eventos)
│   ├── config.ts                  # UserEventsConfig, EventOverride, ResolvedEventConfig
│   ├── events.ts                  # Interfaces do config resolver
│   ├── executor.ts                # Tipos de dependências do executor
│   ├── messages.ts                # Tipos de formatação de mensagens
│   ├── scripts.ts                 # Tipos de execução de scripts
│   ├── toast.ts                   # Tipos de toast
│   └── audit.ts                   # Sistema de auditoria completo
└── features/
    ├── adapters/
    │   └── claude-settings.ts     # Carrega hooks do Claude Code (~/.claude/hooks/)
    ├── audit/
    │   ├── audit-logger.ts        # Escrita + arquivamento de auditoria
    │   ├── event-recorder.ts      # Log de eventos
    │   ├── script-recorder.ts     # Log de execução de scripts
    │   ├── error-recorder.ts      # Log de erros
    │   ├── security-recorder.ts   # Log de eventos de segurança
    │   ├── debug-recorder.ts      # Log de debug
    │   └── plugin-integration.ts  # Getters singleton para recorders
    ├── core/
    │   └── toast-director.ts      # ToastDirectorImpl — fila escalonada de toasts
    ├── events/
    │   ├── events.ts              # resolveEventConfig / resolveToolConfig
    │   ├── context.ts             # ConfigResolverContext factory
    │   └── resolvers/             # Resolvedores EventConfig + ToolConfig
    ├── handlers/
    │   ├── index.ts               # Registro central de handlers
    │   ├── create-handler.ts      # Handler factory
    │   ├── session-handlers.ts    # session.created, .compacted, .deleted, .error, .idle, .status, .updated, .unknown + session.next.*
    │   ├── message-handlers.ts    # message.part.*, message.removed, message.updated
    │   ├── tool-handlers.ts       # tool.execute.before/after, subagent variants, file.edited, file.watcher.updated, permission.*
    │   ├── tool-before-handlers.ts # Handlers before por ferramenta
    │   ├── tool-after-handlers.ts  # Handlers after por ferramenta
    │   └── misc-handlers.ts       # chat, command, server, shell, todo, tui, lsp, experimental
    ├── hooks/
    │   └── hook-executor.ts       # Classe HookExecutor — orquestra execução
    ├── message-formatter/
    │   ├── build-keys-message.ts  # Constrói mensagens toast a partir de campos de evento
    │   ├── formatters.ts          # Utilitários de formatação
    │   └── get-value-by-path.ts   # Acesso profundo a chaves (ex: "info.id")
    ├── messages/
    │   ├── append-to-session.ts   # Anexa texto à sessão OpenCode ativa
    │   ├── show-startup-toast.ts  # Notificação de inicialização
    │   └── plugin-status.ts       # Status do plugin
    └── scripts/
        ├── executor.ts            # ScriptExecution — spawn, stdin, parseHookOutput
        ├── run-script.ts          # Runner de baixo nível
        ├── run-script-handler.ts  # Runner de médio nível: execução + auditoria
        ├── script-executor.ts     # Wiring de dependências do executor
        ├── adapters.ts            # Construtores de stdin (Claude vs nativo)
        └── utils.ts               # Utilitários de script
```

---

## 3. Sistema de Eventos

O enum `OpenCodeEvents` em `types/core.ts` define **mais de 100 constantes de evento**:

| Categoria         | Qtd  | Exemplos                                                                                          |
| ----------------- | ---- | ------------------------------------------------------------------------------------------------- |
| **Session**           | 31   | `session.created`, `.compacted`, `.deleted`, `.error`, `.idle`, `.status`, `.updated`, `.diff` + 22 `session.next.*` |
| **Tool**              | 4    | `tool.execute.before`, `.after`, `.before.subagent`, `.after.subagent`                             |
| **Message**           | 5    | `message.part.removed`, `.part.updated`, `.part.delta`, `.removed`, `.updated`                     |
| **File**              | 2    | `file.edited`, `file.watcher.updated`                                                              |
| **Permission**        | 3    | `permission.asked`, `.ask`, `.updated`, `.replied`                                                   |
| **Server**            | 2    | `server.connected`, `server.instance.disposed`                                                     |
| **Chat**              | 3    | `chat.message`, `.params`, `.headers`                                                              |
| **Command**           | 2    | `command.executed`, `command.execute.before`                                                       |
| **LSP**               | 2    | `lsp.client.diagnostics`, `lsp.updated`                                                            |
| **Installation**      | 2    | `installation.updated`, `.update-available`                                                        |
| **TODO**              | 1    | `todo.updated`                                                                                    |
| **Shell**             | 1    | `shell.env`                                                                                       |
| **TUI**               | 3    | `tui.prompt.append`, `.command.execute`, `.toast.show`                                              |
| **PTY**               | 4    | `pty.created`, `.updated`, `.exited`, `.deleted`                                                   |
| **Experimental**      | 4    | `experimental.session.compacting`, `.chat.messages.transform`, `.chat.system.transform`, `.text.complete` |
| **Outros**            | 9    | `tool.definition`, `question.asked/replied/rejected`, `mcp.*`, `workspace.*`, `worktree.*`          |
| **session.next.* (detalhado)** | 22 | agent.switched, model.switched, prompted, synthetic, shell.started/ended, step.started/ended/failed, text.started/delta/ended, reasoning.started/delta/ended, tool.input.started/delta/ended, tool.called/progress/success/failed, retried, compaction.started/delta/ended |

---

## 4. Hooks OpenCode Suportados

O plugin implementa a interface `Plugin` do `@opencode-ai/plugin` e registra handlers para:

| Hook                               | Descrição                                                          | Uso Principal                                |
| ---------------------------------- | ------------------------------------------------------------------ | -------------------------------------------- |
| `event`                            | Handler genérico — recebe TODOS os eventos do OpenCode             | Disparar scripts/configurações por evento     |
| `tool.execute.before`              | Pré-execução de ferramenta                                         | Bloquear/modificar comandos antes de rodar   |
| `tool.execute.after`               | Pós-execução de ferramenta                                         | Auditar resultados, extrair informações       |
| `shell.env`                        | Hook de ambiente shell                                             | Injetar variáveis de ambiente                 |
| `chat.message` / `.params` / `.headers` | Hooks de chat                                                   | Interceptar mensagens do chat                 |
| `permission.ask`                   | Pedido de permissão                                                | Automação de approvals                        |
| `command.execute.before`           | Pré-execução de comando TUI                                        | Validar/modificar comandos                    |
| `experimental.*`                   | 4 hooks experimentais (transform, compacting, text.complete)      | Modificar prompt do sistema, mensagens, saída |
| `tool.definition`                  | Definição de ferramenta                                            | Estender tools disponíveis                    |

---

## 5. Funcionalidades Únicas

### 5.1 Execução de Scripts Shell
- Scripts arbitrários por evento/ferramenta
- Modos: síncrono (blocking), async (fire-and-forget com `spawn.unref()`)
- Blocking via exit code 2 ou resposta JSON
- Scripts recebem stdin estruturado com dados do evento

### 5.2 Notificações Toast
- Fila gerenciada com escalonamento (300ms entre toasts)
- Máximo configurável (default 50)
- Título/mensagem/variante/duração configuráveis por evento

### 5.3 Sistema de Auditoria
- 5 arquivos JSON de log: eventos, scripts, erros, segurança, debug
- Arquivamento automático por tamanho/idade
- Sanitização de campos (senhas, tokens, secrets)
- Truncamento de campos grandes

### 5.4 Compatibilidade com Claude Code
- Carrega scripts `.claude/hooks/` transparentemente
- Mapeia eventos OpenCode para nomes de hook Claude
- Suporta formato stdin Claude e formato nativo

### 5.5 Configuração Dual
- Arquivos `opencode-hooks.jsonc` (projeto + global)
- Deep merge com defaults (tudo desabilitado por padrão)
- Configuração por evento e por ferramenta

### 5.6 Detecção de Subagentes
- Sessões com `parentID` são rastreadas como subagentes
- Scripts marcados `runOnlyOnce` pulam subagentes

### 5.7 Injeção em Sessão
- `appendToSession` alimenta saída de script de volta na conversa ativa
- Útil para relatórios automáticos, resumos, checkpoints

---

## 6. Comparação com Plugins OpenCode Comuns

| Característica                | opencode-hooks                         | Plugin OpenCode Típico          |
| ----------------------------- | -------------------------------------- | ------------------------------- |
| **Arquitetura**                   | Engine de execução de scripts configurável | Callbacks diretos em event handler |
| **Configuração**                  | JSONC dual (projeto + global) + deep merge  | Inline only                     |
| **Notificações**                  | Fila gerenciada com escalonamento      | `client.tui.showToast()` manual   |
| **Scripts shell**                 | Suporte nativo com blocking/async      | Não tem                         |
| **Claude Code compat**            | Sim (carrega `.claude/hooks/`)           | Não                             |
| **Auditoria**                     | 5 logs JSON + arquivamento + sanitização  | Nada comparável                  |
| **Config por ferramenta**         | Sim (bash vs write vs read vs task)     | Config única por evento         |
| **Subagentes**                    | Detecção automática + `runOnlyOnce`       | Tracking manual                  |
| **Injeção em sessão**             | `appendToSession`                        | Não disponível                   |
| **Bloqueio de execução**          | Exit code 2 ou JSON response             | Sem mecanismo de bloqueio       |
| **Cobertura de testes**           | 99%+                                    | Variável                         |

---

## 7. Documentação Incluída

| Arquivo                    | Conteúdo                                                     |
| -------------------------- | ------------------------------------------------------------ |
| `README.md`                  | Visão geral, features, quick start, links                    |
| `CONFIGURATION.md`           | Referência completa de config — campos, tipos, eventos        |
| `EVENTS.md`                  | Catálogo de eventos com chaves disponíveis e campos de toast  |
| `SCRIPTS.md`                 | Guia de escrita de scripts — stdin, exit codes, blocking      |
| `CLAUDE-COMPATIBILITY.md`    | Comparação de campos stdin Claude, mapeamento de eventos      |
| `AUDIT_SYSTEM.md`            | Sistema de auditoria — tipos de arquivo, arquivamento         |
| `SECURITY.md`                | Modelo de segurança — blocking, exit codes, JSON responses    |
| `TROUBLESHOOTING.md`         | Guia de resolução de erros                                    |
| `adr/`                       | Architecture Decision Records                                 |
| `agent-instructions/`        | Diretrizes para agente IA (code style, git, testing)          |

---

## 8. Pipeline CI/CD

- **GitHub Actions:**
  - Push/PR na main: lint → format check → test (com coverage) → build
  - Release Please: push na main → auto-changelog, bump, GitHub release
- **npm publish:** automático via Release Please + `prepublishOnly` build
- **Ferramentas:** ESLint + Prettier + Husky + commitlint + lint-staged + Fallow audit

---

## 9. Casos de Uso Principais

1. **Notificações desktop:** Disparar toasts quando sessão inicia/termina/erro
2. **Auditoria de sessão:** Registrar toda atividade em logs JSON estruturados
3. **Scripts automáticos:** Rodar scripts shell em resposta a eventos (ex: `file.edited` → linter)
4. **Integração com Claude Code:** Migrar hooks existentes do `.claude/hooks/` sem reescrita
5. **Bloqueio de ferramentas:** Impedir execução de comandos perigosos baseado em regras
6. **Pipeline de memória:** Capturar decisões de sessão e armazenar em MCP (mempalace)

---

## 10. Considerações Técnicas

- **Performance:** Spawn com `unref()` para scripts async — não bloqueia o evento loop
- **Segurança:** Sanitização automática de secrets nos logs de auditoria
- **Resiliência:** Erros em scripts não quebram o fluxo do OpenCode (try/catch em toda execução)
- **Config hot-reload:** Arquivos JSONC lidos na inicialização do plugin; requer restart para alterações
- **Dependências:** Apenas `@opencode-ai/plugin` como peer dependency
