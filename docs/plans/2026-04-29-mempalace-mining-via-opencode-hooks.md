# Plano: Mineração MemPalace via opencode-hooks

## Objetivo

Resolver o problema de auto-mineração de conversas do MemPalace no OpenCode usando o plugin opencode-hooks (em vez do plugin `@devtheops/opencode-plugin-mempalace` que está quebrado).

## Problema Atual

O plugin `@devtheops/opencode-plugin-mempalace` tem um bug na função `exportSessionTranscript()` que usa a API `client.session.messages()`. O erro é:

```
error=messages.map is not a function
```

Isso acontece porque a API do OpenCode mudou o formato de resposta.

## Solução

Usar o **opencode-hooks** para rodar scripts shell que chamam a **CLI do MemPalace** diretamente, contornando a API problemática.

## Como Funciona o MemPalace

### Auto-Inicialização

O MemPalace **NÃO se auto-inicializa automaticamente** em novos diretórios. Você precisa rodar manualmente:

```bash
# Primeira vez em um projeto
mempalace init ~/caminho/do/projeto

# Depois mine os arquivos
mempalace mine ~/caminho/do/projeto
```

Para o seu caso (`~/.config/opencode`):
- ✅ `mempalace init` já foi rodado (arquivo `mempalace.yaml` existe)
- ✅ `mempalace mine` já foi rodado (1510 drawers no palace)

### Comandos úteis:

| Comando | Descrição |
|---------|-----------|
| `mempalace init <dir>` | Cria `mempalace.yaml` com rooms detectadas |
| `mempalace mine <dir>` | Mine arquivos do projeto |
| `mempalace mine <dir> --mode convos` | Mine conversas |
| `mempalace wake-up` | Output L0 + L1 para injeção no system |
| `mempalace wake-up --wing <nome>` | Wake-up para wing específica |
| `mempalace status` | Mostra drawers/rooms/wings |

## Arquitetura da Solução

**Local dos scripts:** `~/.config/opencode/.opencode/plugins/scripts/`

```
~/.config/opencode/
└── .opencode/
    └── plugins/
        ├── scripts/
        │   ├── mempalace-wake.sh    → Injeta L0/L1 no system prompt
        │   └── mempalace-mine.sh   → Incrementa contador + mining
        └── config/
            └── settings.ts          → Configuração de eventos
```

### Eventos do OpenCode usados:

| Evento | Script | Ação |
|--------|--------|------|
| `SESSION_CREATED` | `mempalace-wake.sh` | Injeta L0 na inicialização |
| `SESSION_IDLE` | `mempalace-mine.sh` | Mine conversas quando idle |
| `EXPERIMENTAL_SESSION_COMPACTING` | `mempale-cmine.sh` | Mine antes da compactação |

## Passos de Implementação

### Passo 1: Criar Scripts

Criar em `~/.config/opencode/.opencode/plugins/scripts/`:

#### `mempalace-wake.sh`
```bash
#!/bin/bash
# Injeta L0 + L1 via wake-up
# Usado em SESSION_CREATED

WING="opencode"  # ou inferir do diretório

OUTPUT=$(mempalace wake-up --wing "$WING" 2>/dev/null)

if [ -n "$OUTPUT" ]; then
  echo "=== MEMPALACE L0 ===" 
  echo "$OUTPUT"
  echo "===================="
fi
```

### Script: `mempalace-mine.sh` (contador + mining)

Como o `messageID` não é incremental (é um hash), usamos um arquivo contador que persiste entre as mensagens.

**Local:** `~/.config/opencode/.opencode/plugins/scripts/mempalace-mine.sh`

```bash
#!/bin/bash
# Mineração automática a cada X mensagens
# Evento: chat.message (disparado a cada mensagem)

MINE_EVERY=5              # mining a cada 5 mensagens
WING="opencode"           # wing do MemPalace
SESSION_DIR="$HOME/.local/share/opencode/sessions"

# Session ID vem do argumento ($1) ou usa 'default'
SESSION_ID="${1:-default}"
COUNTER_FILE="/tmp/mempalace_count_$SESSION_ID"

# Incrementa contador
COUNT=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

echo "[MemPalace] Message $COUNT of session $SESSION_ID"

# Verifica threshold (múltiplo de MINE_EVERY)
if [ $((COUNT % MINE_EVERY)) -eq 0 ]; then
  echo "=== MINING (every $MINE_EVERY messages) ==="
  
  # Mine conversas da sessão
  if [ -d "$SESSION_DIR" ]; then
    mempalace mine "$SESSION_DIR" --mode convos --wing "$WING" 2>/dev/null
  else
    echo "Sessions directory not found: $SESSION_DIR"
  fi
  
  echo "============================================="
fi
```

**Como funciona:**
1. Recebe `sessionID` como argumento ($1)
2. Incrementa contador em arquivo `/tmp/mempalace_count_<SESSION_ID>`
3. Quando `COUNT % MINE_EVERY == 0`, faz mining

### Script: `mempalace-wake.sh` (opcional - L0 injection)

**Local:** `~/.config/opencode/.opencode/plugins/scripts/mempalace-wake.sh`

```bash
#!/bin/bash
# Injeta L0 + L1 via wake-up
# Evento: session.created (disparado ao iniciar sessão)

WING="opencode"

OUTPUT=$(mempalace wake-up --wing "$WING" 2>/dev/null)

if [ -n "$OUTPUT" ]; then
  echo "=== MEMPALACE L0 ===" 
  echo "$OUTPUT"
  echo "===================="
fi
```

### Passo 2: Configurar opencode-hooks

Editar `~/.config/opencode/.opencode/plugins/config/settings.ts`:

```typescript
events: {
  [EventType.SESSION_CREATED]: {
    toast: true,
    runScripts: true,
    runOnlyOnce: true,
    appendToSession: true,
    scripts: ['mempalace-wake.sh']  // Opcional: L0 injection
  },
  [EventType.CHAT_MESSAGE]: {
    enabled: true,
    runScripts: true,
    scripts: ['mempalace-mine.sh']  // Contador + mining a cada X mensagens
  },
}
```

**Nota:** O evento `CHAT_MESSAGE` precisa ser habilitado (por padrão está `enabled: false`).

### Passo 3: Testar

1. Reiniciar OpenCode
2. Enviar 5 mensagens → verificar se mining dispara
3. Verificar logs para confirmar

## Transcript: Como obter as mensagens

O script precisa de acesso ao transcript das mensagens. Opções:

1. **Arquivo de transcript**: OpenCode pode salvar transcript da sessão
2. **API session.messages()**: Tem o mesmo bug dos plugins (precisa contorno)
3. **Arquivo JSON de sessão**: Em `~/.local/share/opencode/sessions/`

O MemPalace pode minerar de:
- `~/.local/share/opencode/sessions/` via `--mode convos`
- Arquivo de transcript exportado

## Alternativas Considered

1. **Usar plugin option-K** - Provavelmente mesmo bug (usa mesma API)
2. **Usar plugin nguyentamdat** - Mesmo problema async + mining
3. **Usar rvboris** - Não carrega L0 no início
4. **Corrigir bug do plugin DEVtheops** - Requer mudança no plugin (que você não quer)

## Próximos Passos Após Este Plano

1. Criar scripts shell
2. Configurar opencode-hooks
3. Testar em diferentes cenários
4. Ajustar conforme necessário

## Referências

- opencode-hooks: `~/projects/opencode-hooks/`
- MemPalace CLI: `mempalace --help`
- Eventos OpenCode: ver `events-catalog.md` no opencode-hooks