# Plano: Instalar e Configurar fff + GitNexus

## Objetivo

Instalar fff (file search ultra-rápido) e GitNexus (grafo de código), configurar os MCP
servers no OpenCode, e instruir o agente a usá-los automaticamente via AGENTS.md.

---

## Fase 1 — fff

### 1.1 Instalar binário + MCP server

```bash
curl -L https://dmtrkovalenko.dev/install-fff-mcp.sh | bash
```

O script baixa o binário e imprime as instruções de configuração (caminho do executável).

### 1.2 Configurar no opencode.jsonc

Adicionar no bloco `mcp` em `~/.config/opencode/opencode.jsonc`:

```jsonc
"fff": {
  "enabled": true,
  "type": "local",
  "command": ["<caminho-que-o-script-mostrar>", "mcp"]
}
```

### 1.3 Teste

```bash
# verificar se o binário funciona
fff --help

# testar num projeto
cd ~/projects/fake-ai-racer && fffind "game loop"
ffgrep "requestAnimationFrame"
```

---

## Fase 2 — GitNexus

### 2.1 Instalar globalmente

```bash
npm install -g gitnexus
gitnexus setup          # tenta configurar MCP automaticamente
```

### 2.2 Se setup não detectar OpenCode, adicionar manualmente no opencode.jsonc

```jsonc
"gitnexus": {
  "enabled": true,
  "type": "local",
  "command": ["gitnexus", "mcp"]
}
```

### 2.3 Indexar projetos

```bash
cd ~/projects/opencode-hooks && gitnexus analyze
cd ~/projects/overdrive     && gitnexus analyze
cd ~/projects/pay2free/     && gitnexus analyze
cd ~/projects/fake-ai-racer && gitnexus analyze --skip-embeddings
```

Flags úteis:
- `--skip-embeddings` — mais rápido, sem busca semântica
- `--force` — reindexar do zero
- `--skills` — gerar skills por módulo

### 2.4 Verificar

```bash
gitnexus list
# deve listar todos os projetos indexados
```

---

## Fase 3 — AGENTS.md

Adicionar no final do bloco de instruções MCP em
`~/.config/opencode/AGENTS.md` (após a seção `## MCP Tools` existente):

```markdown
## fff (File Search)
MANDATORY: Use fff MCP tools (`ffgrep`, `fffind`, `fff-multi-grep`) for ALL
file and content searches in git-indexed projects. Fall back to grep/glob
only when the query involves non-indexed directories or shell pipes.

Priority:
1. `fffind` — find files by path/name pattern (frecency-ranked)
2. `ffgrep` — search file contents (auto-detects regex/fuzzy)
3. `fff-multi-grep` — multi-pattern OR search
4. native `grep`/`glob` — only if above return insufficient or tool is unavailable

### Rules
NEVER: Use grep/glob when fff MCP tools are available for the search
NEVER: Call fff with wildcard-only patterns (e.g. `.*`) — it rejects them

## GitNexus (Code Intelligence)
Use GitNexus MCP tools for architectural understanding, impact analysis,
and complex code discovery. Prefer BEFORE grep-based approaches when
exploring unfamiliar code or before making changes.

### When to use
| Tool | When |
|------|------|
| `list_repos` | First — discover which repos are indexed |
| `context` | Understand a symbol: who calls it, what it depends on |
| `impact` | Blast radius analysis BEFORE editing any symbol |
| `query` | Hybrid search when you don't know where something is |
| `cypher` | Complex graph queries across modules |

### When to fall back to grep/glob
- Searching string literals, error messages, config values
- The current repo is not indexed (run `gitnexus analyze` first)
- GitNexus returns insufficient results

MANDATORY: Run `context` or `impact` before editing symbols in unfamiliar
code. This prevents breaking hidden dependencies.
```

---

## Cronograma Estimado

| Fase | Duração |
|------|---------|
| Fase 1 (fff) | ~5 min |
| Fase 2 (GitNexus) | ~15-20 min (5 min instalação + ~2-5 min por projeto indexado) |
| Fase 3 (AGENTS.md) | ~2 min |
| **Total** | **~25 min** |

---

## Observações

- fff: a primeira busca pode ser mais lenta que as subsequentes (frecency esquenta com uso)
- GitNexus em projetos pequenos (fake-ai-racer): usar `--skip-embeddings` pra não gastar tempo
- GitNexus `impact` é a ferramenta mais valiosa — usar **antes** de editar símbolos em código que não conhece bem
- Nenhum conflito entre as tools: namespaces diferentes (`ffgrep`/`fffind` vs `context`/`impact`/`query`)
