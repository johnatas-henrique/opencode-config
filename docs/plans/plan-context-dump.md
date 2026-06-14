# Plano anti-fabricação (5 etapas)

Baseado no [criterium/opencode-lab](https://github.com/criterium/opencode-lab)

## Etapa 1 — Context Dump (baseline)

Rodar numa **sessão nova e limpa** em sequência:

1. `prompt_1_dump.md` — extrai system prompt, tools, messages
   https://raw.githubusercontent.com/criterium/opencode-lab/main/research/context-dump/prompts/prompt_1_dump.md

2. `prompt_2_analysis.md` — analisa o dump gerado
   https://raw.githubusercontent.com/criterium/opencode-lab/main/research/context-dump/prompts/prompt_2_analysis.md

**Procedimento:**
- Abrir sessão nova
- Colar o conteúdo do `prompt_1_dump.md` como primeira mensagem
- Após gerar o dump, colar `prompt_2_analysis.md` como segunda mensagem
- O dump será salvo em `dump.{model}.{YYYYMMDD}/01_context.dump.md`
- A análise em `dump.{model}.{YYYYMMDD}/02_context.analysis.md`

## Etapa 2 — opencode-tools-override (plugin)

Instalar plugin que substitui descrições de tools. Tool descriptions têm
**mais alta autoridade** que system prompt — regras lá são mais seguidas.

Repo: https://github.com/criterium/opencode-lab/tree/main/plugins/opencode-tools-override

## Etapa 3 — Custom prompt com `[C]/[I]/[S]`

Adotar o `default.md` do shared prompts que já inclui marcadores de certeza:
- `[C]` verified from source
- `[I]` inferred with reasoning
- `[S]` assumption requiring validation

Prompt: https://raw.githubusercontent.com/criterium/opencode-lab/main/prompt/shared/default.md

## Etapa 4 — Neutralizar skill leak

Adicionar `OPENCODE_DISABLE_EXTERNAL_SKILLS=true` no profile do shell.
Remove descrições de skills do `available_skills` no system prompt.
Skills continuam carregáveis via `read ~/.agents/skills/<name>/SKILL.md`.

## Etapa 5 — Revisar AGENTS.md e docs

Mover regras estáveis pro custom prompt. AGENTS.md global (`~/.config/opencode/AGENTS.md`)
é sempre carregado e nenhuma flag bloqueia.

---

**Status atual do AGENTS.md (~/.config/opencode/AGENTS.md):** 34 linhas, enxuto.
Referencia 4 docs em `docs/agent-instructions/`.

**Ordem:** Etapa 1 → entender baseline → decidir próximas etapas.
