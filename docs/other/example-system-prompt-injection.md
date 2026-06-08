# DCP System Prompt Injection via Manual Mode

Descoberto em 2026-06-07 durante sessão de análise de plugins.

## O Mecanismo

O DCP plugin (`@tarquinen/opencode-dcp`) pode injetar instruções no **system prompt do agente** a cada requisição. Isso acontece no `createSystemTransformHandler()` no `dist/index.js` do plugin.

**Fluxo:**

1. `manualMode` é ativado (`/dcp manual on` ou via config)
2. A cada request do agente, DCP chama `createSystemTransformHandler()` (linha ~7398)
3. Dentro dele, `renderSystemPrompt()` (linha 6329) monta o texto de extensão
4. Se `manualMode` está ativo, inclui `MANUAL_MODE_SYSTEM_EXTENSION` (linha 5012)
5. O texto é **anexado ao system prompt** do modelo via `output.system[output.system.length - 1] += "\n\n" + newPrompt` (linha 7423)
6. O agente recebe essas instruções como se fossem do sistema e obedece

## O Texto Injetado (Manual Mode)

```
Manual mode is enabled. Do NOT use compress unless the user has explicitly triggered it through a manual marker.

Only use the compress tool after seeing `<compress triggered manually>` in the current user instruction context.

Issue exactly ONE compress tool per manual trigger. Do NOT launch multiple compress tools in parallel.

After completing a manually triggered context-management action, STOP IMMEDIATELY. Do NOT continue with any task execution.
```

## Implicações

**Plugins podem controlar o comportamento do agente** injetando instruções no system prompt. O DCP usa isso para limitar compressão manual, mas o mesmo mecanismo pode ser usado para:

- Forçar o agente a seguir um workflow específico (spec-first, TDD, review gates)
- Definir regras de segurança (bloquear bash deletes, forçar approval gates)
- Modificar o estilo de código ou documentação
- Injetar conhecimento de domínio (frameworks, APIs, arquitetura)
- Fornecer contexto de projeto persistente entre sessões

**NÃO** é um exploit ou bug — é um pattern legítimo. O DCP documenta isso como "injected into the model system prompt on every request" (linha 5049). O renderSystemPrompt recebe prompts customizáveis via `dcp.jsonc` `compress.prompts` que podem sobrescrever as extensões padrão.

## Como Diferencia Agentes Internos

DCP verifica `INTERNAL_AGENT_SIGNATURES` (linha 7406) para pular injeção em subagentes do OpenCode. A injeção só acontece no agente principal.

## Custom Prompts

O DCP permite sobrescrever os prompts injetados via `dcp.jsonc`:
```jsonc
{
  "experimental": {
    "customPrompts": {
      "system.md": "Seu texto aqui",
      "manual-extension.md": "Instruções para modo manual",
      "subagent-extension.md": "Instruções para subagentes"
    }
  }
}
```

Isso significa que **qualquer plugin** com acesso ao hook de system transform pode fazer o mesmo — injetar instruções personalizadas no agente a cada request.

## Conexão com opencode-hooks

Seu plugin `opencode-hooks` já tem acesso a 28 eventos OpenCode via hooks (`tool.execute.before`, `session.*`, `file.*`, etc.). Para implementar injeção de system prompt, precisaria de:

1. Um hook de **transform de sistema** (como `createSystemTransformHandler` do DCP) — que modifica o system prompt antes de cada request
2. Um mecanismo para definir as regras (config file, comandos slash, etc.)
3. O texto a ser injetado (pode ser um arquivo `.md` referenciado na config)

## Aplicações Práticas

O mesmo pattern do manual mode do DCP pode ser usado para:

- **Workflow enforcement**: forçar spec-first, TDD, review gates antes de merge
- **Regras de segurança**: bloquear `rm -rf`, `git push --force`, `> file` sem aprovação
- **Estilo de código**: injetar convenções, preferências de arquitetura, padrões de nomeação
- **Contexto de projeto**: regras de domínio, decisões arquiteturais, constraints conhecidas
- **Controle de qualidade**: forçar verificação de coverage, lint, typecheck antes de editar
- **Integração com templates**: conectar agent-md, settings-opencode, ou grojeda como regras injetadas

## Diferença entre Abordagens

| Abordagem | Exemplo | Força |
|-----------|---------|-------|
| **Prompt no AGENTS.md** | "Sempre faça review antes de merge" | O agente pode ignorar |
| **Pergunta de aprovação** | `[y/N/edit]` | O agente pergunta, usuário decide |
| **Injeção via plugin (DCP)** | Regra no system prompt a cada request | O agente recebe como instrução nativa |
| **Permission deny** | `write: false` pra certos agentes | O agente **não consegue** desobedecer |

A injeção de system prompt via plugin é mais forte que AGENTS.md (porque renova a cada request) mas menos forte que permissões negadas (que são mecânicas). É o meio-termo ideal para regras que o agente **deve** seguir mas que não precisam de bloqueio mecânico.

