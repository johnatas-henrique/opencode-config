# MCP Tools

MANDATORY: Use playwright for web interaction
MANDATORY: Use context7 for library/framework docs
MANDATORY: Use exa for web searches
MANDATORY: Use thinking tool if not native reasoning model

## Tool Selection

| Task | Tool |
|------|------|
| Browser interaction | playwright |
| URL fetch | exa or curl |
| Library docs | context7 |
| Web search | exa |
| File/content search | fff |
| Code architecture/impact | gitnexus |
| Chain-of-thought | thinking |

## Rules

NEVER: Use playwright for simple URL fetch
NEVER: Use context7 for general web search

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
