# OpenCode Agent Instructions — MANDATORY RULES

## Repository Context

This is the **OpenCode global configuration repository** (`~/.config/opencode`). It contains:
- `opencode.json` — Provider configs, MCP servers, plugins, permissions
- `AGENTS.md` — This file (global agent instructions)
- `docs/agent-instructions/` — Lazy-loaded instruction modules
- `docs/plugins-commands/` — Plugin documentation with Quick Command Reference tables
- `docs/plans/` — Execution plans (YYYY-MM-DD-name.md format)
- `skills/` — Custom agent skills (SKILL.md format)
- `scripts/` — Helper scripts (e.g., verify-provider.py)
- `agents/`, `commands/`, `rules/` — Specialized agents, custom commands, lint rules

## Plan Format

- File: `docs/plans/YYYY-MM-DD-name.md`
- All plans in English

## Codebase Knowledge Graph (codebase-memory-mcp)

This project uses codebase-memory-mcp to maintain a knowledge graph of the codebase.
ALWAYS prefer MCP graph tools over grep/glob/file-search for code discovery.

### Priority Order
1. `search_graph` — find functions, classes, routes, variables by pattern
2. `trace_path` — trace who calls a function or what it calls
3. `get_code_snippet` — read specific function/class source code
4. `query_graph` — run Cypher queries for complex patterns
5. `get_architecture` — high-level project summary

### When to fall back to grep/glob
- Searching for string literals, error messages, config values
- Searching non-code files (Dockerfiles, shell scripts, configs)
- When MCP tools return insufficient results

### Examples
- Find a handler: `search_graph(name_pattern=".*OrderHandler.*")`
- Who calls it: `trace_path(function_name="OrderHandler", direction="inbound")`
- Read source: `get_code_snippet(qualified_name="pkg/orders.OrderHandler")`

## MCP Tools
MANDATORY: Use playwright for web interaction
MANDATORY: Use context7 for library/framework docs
MANDATORY: Use exa for web searches
MANDATORY: Use thinking tool if not native reasoning model

### Tool Selection
| Task | Tool |
|------|------|
| Browser interaction | playwright |
| URL fetch | exa or curl |
| Library docs | context7 |
| Web search | exa |
| Chain-of-thought | thinking |

### Rules
NEVER: Use playwright for simple URL fetch
NEVER: Use context7 for general web search
