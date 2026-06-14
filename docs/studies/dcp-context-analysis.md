# DCP Context Analysis

## Como DCP calcula cada categoria

Baseado no código fonte em `dist/index.js`:

### System
```
System = firstAssistant.input_tokens - countTokens2(first_user_text)
```
Onde `firstAssistant` é a **primeira resposta do assistente** na sessão. O `input_tokens` inclui TODO o prompt enviado (system + user + tools). Subtrai só o texto da primeira mensagem do usuário.

### User
```
User = countTokens2(todas_as_partes_de_texto_do_usuário)
```
Recontado do texto bruto, **não** da API.

### Tools
```
Tools = countTokens2(tool_inputs) + countTokens2(tool_outputs)
```
Também recontado do texto, não da API.

### Total
```
Total = sum(apiInput + apiOutput + apiReasoning + apiCacheRead + apiCacheWrite) da última resposta
```

## O problema do double-count

System usa **tokens da API** (primeira chamada). User e Tools usam **recontagem de texto bruto**.

Isso faz os percentuais somarem >100% porque são métodos de medição diferentes:
- System = 89.3K (de uma única chamada API)
- User = 61.1K (texto bruto recontado — inclui outputs de tools como arquivos lidos)
- Tools = 9.6K (inputs/outputs de ferramentas)

Assistent fica 0 porque `total - system - user - tools` deu negativo.

## Breakdown real da sessão atual (DB)

### Sessão: ses_147d0441fffe78e9H5iqxBkVZv

**Primeira chamada API:**
```json
{
  "input": 90541,
  "output": 75,
  "reasoning": 64,
  "cache": { "write": 0, "read": 0 }
}
```

**Partes no DB (124 total):**
| Tipo | Parts | Chars | ~Tokens |
|------|-------|-------|---------|
| text (synthetic) | 14 | 174,666 | 43,666 |
| reasoning | 24 | 26,062 | 6,515 |
| text (user) | 7 | 6,834 | 1,708 |
| tool | 32 | 0 | 0 |
| step-start | 24 | 0 | 0 |
| step-finish | 23 | 0 | 0 |

**Textos sintéticos** são os maiores contribuintes: plugin-studies.js (106K chars), orchestration-study.html (53K chars). Estes são outputs de `read` que o DCP trata como "User".

## Onde estão os 90K de system prompt?

Não ficam no DB — são montados em runtime pelo servidor OpenCode e enviados ao LLM. Só temos o `input_tokens` da API como evidência.

### Componentes estimados:

| Componente | ~Tokens | Fonte |
|-----------|---------|-------|
| AGENTS.md + 5 docs | 2,500 | medido (9.2K chars) |
| MCP tools (4) schemas | 2,200 | ~8K chars |
| AFT tool descriptions (~15) | 5,600 | ~20K chars |
| Built-in tool descriptions (~10) | 4,200 | ~15K chars |
| Available skills (44) descriptions | 15,000-20,000 | estimado (maior contribuidor) |
| Plugin descriptions (6) | 850 | ~3K chars |
| Plan/Build mode reminders | 850 | ~3K chars |
| DCP + plugins boilerplate | 850 | ~3K chars |
| **mnemory core memories** (19 pin) | 1,500-3,000 | injetado via system.transform |
| **mnemory search results** (per-turn) | 1,000-2,000 | injetado a cada turno |
| OpenCode system prompt boilerplate | 5,000-10,000 | server runtime |
| **Total estimado** | **~39K-52K** | vs 89.3K medido |

**Gap de ~37K-50K** — não identificado. Provavelmente:
- Tool schemas completos (JSON Schema com tipos, descrições, exemplos) são muito maiores que estimei
- Skills descriptions no XML podem incluir seções completas dos SKILL.md
- OpenCode server pode adicionar boilerplate significativo (agent routing, mode instructions, etc.)

## Ações possíveis

1. **Reduzir skills desnecessárias** — 44 skills listadas, cada uma com descrição + location. Remover skills não usadas reduz o system prompt.
2. **Verificar mnemory** — quantas memórias pinned e search_results por turno
3. **Desligar plugins não usados** — cada plugin adiciona ao system prompt
4. **Testar com `protectUserMessages: true`** no DCP — muda como DCP conta (e talvez comprima)

## Observação importante do log

```
"Injecting context (instructions=true, core_memories=true, search_results=X, turn=N, ...)"
```

mnemory injeta **a cada turno**:
- `instructions=true` → AGENTS.md + docs
- `core_memories=true` → memórias pinned (19 itens)
- `search_results=X` → resultados de busca da sessão atual
