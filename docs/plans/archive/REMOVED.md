# Removed Plans

Full content recoverable via `git log --all -- docs/plans/`.

## Plans with Extracted Information

### open-stack-cleanup.md

Cleanup comprehensive do stack OpenCode. Decisões chave:

- **External directory permissions**: recurso não existe no OpenCode (config morta)
- **Análise de instruction files**: 10 arquivos, medição de tokens por arquivo, decisões de merge
- **Substituição magic-context → DCP**: DCP reinstalado com config atual
- **Cron de consolidação agentmemory**: configurado para limpeza periódica
- **Permissões bash**: `rm -f *`, `rm -rf *`, `git reset/restore/clean/push` como "ask"

### global-memories-migration.md

Define 12 memórias globais para agentmemory (9 pinned + 3 lessons):

- **Pinned slots**: correctness_over_speed, scope_and_questions, answer_questions_only, honesty, verify_before_asserting, no_code_comments, question_when_uncertain, no_proactive_scope, mandatory_instructions_header
- **Lessons**: never_commit_without_asking, atomic_commits_conventional_commits, never_git_push
- Único documento que lista e define cada slot do agentmemory

### agentmemory-verification-plan.md

QA do sistema de memória. 8 testes planejados, 6 concluídos:

- Pain points: pinned slots injection, observations capture, proactive search, mandatory rules enforcement, consolidation, stability
- 2 pendentes: dependem de sessão nova para validar

### agentmemory-fix-2026-05-30.md

Sessão de ~6h diagnosticando agentmemory. Lições:

- **ctx.worktree retornar "/"**: causou perda de dados — verificar diretório do projeto sempre
- **console.error invisível no TUI do OpenCode**: usar debug file para logs
- **Benchmark de 12 modelos NVIDIA NIM**: tabela comparativa de performance/qualidade
- **Config final do .env do agentmemory**: documentação da configuração NVIDIA NIM

### aft-only-migration.md

Direção atual: simplificar de 3 sistemas concorrentes (AFT + fff + GitNexus) para AFT + ferramentas nativas.

- **Ações**: criar hook block-stderr-suppression, desativar fff/gitnexus, adicionar global-identity.md, limpar referências conflitantes no AGENTS.md, simplificar mcp-tools.md
- **Status**: plano mais recente sobre estratégia de ferramentas — direção ativa

### memory-system-cleanup.md

Plano de substituição agentmemory → claude-mem (CANCELLED).

- **Comparação claude-mem vs opencode-mem**: critérios de shared state, community, setup complexity
- **Útil se**: no futuro precisar reavaliar provedores de memória

### 2026-04-19-install-magic-context.md

Instalação do Magic Context (compressão de chat + TUI sidebar + dreamer diário).

- **Arquitetura**: historian (resumo), dreamer (relatório diário), sidekick (análise reativa)
- **Modelos free no OpenRouter**: elephant-alpha, nemotron, gemma — configuração e custos
- **Por que foi substituído**: DCP provou ser mais eficiente para compressão de contexto

---

## Procedural Plans (no extracted content)

| Plan | Data | Plugin/Tool References |
|------|------|----------------------|
| 2026-04-14-add-simple-memory-rules | Adicionar regras simple-memory ao AGENTS.md | simple-memory (plugin, never installed) |
| 2026-04-14-agents-md-integration | Integrar skillmaxxing + padroes enterprise | skillmaxxing, conventional commits config |
| 2026-04-14-karpathy-integration | Adicionar principios Karpathy ao AGENTS.md | Nenhum plugin específico |
| 2026-04-14-migration-true-mem-to-simple-memory | Migrar true-mem → simple-memory | true-mem (removed), simple-memory (never installed) |
| 2026-04-15-ctx-mode-vs-dcp-comparison | Comparar ctx-mode + DCP + squeez | ctx-mode (removed), DCP, squeez (removed) |
| 2026-04-15-install-session-recall | Instalar opencode-session-recall | session-recall (never installed) |
| 2026-04-15-refactor-global-agents | Refatorar AGENTS.md progressive disclosure | 6 linked instruction files proposal |
| 2026-04-17-migration-to-lean-ctx | Substituir ctx-mode + DCP + tokenscope | lean-ctx (removed), DCP, tokenscope |
| 2026-04-18-reactivate-dcp | Reativar DCP para compressao | DCP |
| 2026-04-20-codebase-memory-mcp-install | Instalar codebase-memory-mcp | codebase-memory-mcp (MCP, removed) |
| 2026-04-20-direct-migration-lean-ctx-to-rtk | Migrar lean-ctx → RTK | RTK (deprecated, replaced by AFT bash rewrite) |
| 2026-04-20-install-caveman-skill | Instalar caveman skill | caveman skill (still active) |
| 2026-04-21-magic-context-model-selection | Selecao de modelos para Magic Context | OpenRouter free models, NVIDIA NIM |
| 2026-04-21-provider-standardization | Padronizar 163+ modelos | Nenhum plugin, configuracao de modelos |
| 2026-04-27-fix-mempalace-segfault | Recuperar segfault MemPalace | MemPalace (MCP, inactive) |
| 2026-04-29-mempalace-mining-via-opencode-hooks | Automatizar mineracao MemPalace | opencode-hooks, MemPalace (inactive) |
| 2026-05-04-refactor-global-agents | Refatorar AGENTS.md (181→80 linhas) | writing-style.md como linked file |
| 2026-05-12-install-fff-gitnexus | Instalar fff + GitNexus | fff (disabled), GitNexus (removed) |
