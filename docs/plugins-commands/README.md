# Plugin Commands Reference

This directory contains reference documentation for the commands and tools provided by installed OpenCode plugins.

## Plugins Index

| Plugin | Purpose | Interface | Main Commands/Tools | Status |
|--------|---------|-----------|---------------------|--------|
| [rtk](rtk.md) | Token savings via command output compression | Plugin (auto-rewrite) | `rtk` CLI (plugin: auto-rewrites bash commands) | ✅ Active |
| [magic-context](magic-context.md) | Chat compression + memory | TUI + Agent Tools + MCP | `/ctx-status`, `/ctx-flush`, `/ctx-aug`, `/ctx-dream`, `ctx_reduce`, `ctx_expand` | ✅ Active |
| [session-recall](session-recall.md) | Search past sessions | Agent Tools | `session-search`, `session-title-search`, `session-transcript` | ✅ Active |
| [opencode-handoff](opencode-handoff.md) | Create handoff prompts for new sessions | TUI + Agent Tools | `/handoff <goal>`, `read_session` | ✅ Active |
| [agent-identity](agent-identity.md) | Agent self-identity & attribution | Automatic + Agent Tools | (injects identity), `agent_attribution` | ✅ Active |
| [simple-memory](simple-memory.md) | Persistent cross-session memory | Agent Tools | `memory_remember`, `memory_recall`, `memory_update`, `memory_forget`, `memory_list` | ✅ Active |
| [md-table-formatter](md-table-formatter.md) | Auto-format markdown tables | Automatic | (works silently) | ✅ Active |
| [codebase-memory-mcp](codebase-memory-mcp.md) | Knowledge graph of codebase (AST) — ~99% token reduction on code queries | MCP Server + CLI | 14 MCP tools: `search_graph`, `trace_call_path`, `get_architecture`, etc. | ⏳ Pending installation |

## Quick Reference

#### By Use Case

| Task | Tool/Command | Interface | Plugin |
|------|--------------|-----------|--------|
| Compress bash output | `rtk <command>` (auto-rewrite by plugin) | Bash | rtk |
| Check RTK savings | `rtk gain`, `rtk gain --daily` | CLI | rtk |
| Check token usage | `/ctx-status` | TUI | magic-context |
| Force cleanup | `/ctx-flush` | TUI | magic-context |
| Search past sessions | `/sr-search` or ask AI | TUI / Agent | session-recall |
| Run background maintenance | `/ctx-dream` | TUI | magic-context |
| Create handoff prompt | `/handoff <goal>` | TUI | opencode-handoff |
| View agent attribution | `agent_attribution` (AI calls) | Agent Tool | agent-identity |
| Store memories | `memory_remember` (AI calls) | Agent Tool | simple-memory |
| Recall memories | `memory_recall` (AI calls) | Agent Tool | simple-memory |
| Format markdown tables | Automatic | Automatic | md-table-formatter |
| Index codebase for fast queries | "Index this project" or auto-index | Agent → MCP | codebase-memory-mcp |
| Get architecture overview | "What's the architecture?" | Agent → MCP | codebase-memory-mcp |
| Trace call paths | "Trace calls for function X" | Agent → MCP | codebase-memory-mcp |
| List indexed projects | `codebase-memory-mcp list_projects` | CLI | codebase-memory-mcp |

### User Commands (TUI)

Type these in the chat:

| Command | Description | Plugin |
|---------|-------------|--------|
| `/ctx-status` | Debug view: tags, drops, cache TTL, historian progress | magic-context |
| `/ctx-flush` | Force all queued operations immediately | magic-context |
| `/ctx-recomp` | Rebuild compartments and facts from raw history | magic-context |
| `/ctx-aug` | Run sidekick augmentation (retrieve relevant memories) | magic-context |
| `/ctx-dream` | Run dreamer maintenance now | magic-context |
| `/handoff <goal>` | Create handoff prompt and open new session | opencode-handoff |
| `/sr-search <query>` | Search past sessions (session-recall) | session-recall |

## Configuration Files

| Plugin | Config File / Location | Type |
|--------|-----------------------|------|
| rtk | `~/.config/rtk/config.toml` | Global |
| magic-context | `magic-context.jsonc` | Global or per-project |
| session-recall | (automatic, no config) | — |
| opencode-handoff | (automatic, no config) | — |
| agent-identity | (automatic, no config) | — |
| simple-memory | `.opencode/memory/` (storage) | Per-project |
| md-table-formatter | (automatic, no config) | — |
| codebase-memory-mcp | `~/.config/codebase-memory-mcp/config.json` | Global |

## How Plugins Work Together

1. **rtk**: Compresses bash command output **before** it enters the chat. Uses built-in filters for git, npm, cargo, docker, etc.
   - Interface: Auto-rewrite via plugin hook (transparent), CLI `rtk` for manual runs.

2. **magic-context**: Manages chat history compression **after** messages are exchanged. Provides TUI sidebar and cross-session memory.
   - Interface: TUI commands (`/ctx-*`) and background historian.

3. **session-recall**: Adds ability to search through past compressed sessions that would otherwise be lost.
   - Interface: Agent tools (`session-search`, etc.).

4. **opencode-handoff**: Generates focused continuation prompts when starting a new session.
   - Interface: TUI command (`/handoff`) and agent tool (`read_session`).

5. **agent-identity**: Injects agent self-awareness into system prompts and provides attribution tool.
   - Interface: Automatic injection + agent tool (`agent_attribution`).

6. **simple-memory**: Structured persistent memories (decision, learning, preference, blocker, context, pattern).
   - Interface: Agent tools (`memory_remember`, `memory_recall`, etc.).

8. **codebase-memory-mcp**: Builds a knowledge graph of the codebase using tree-sitter AST. Provides 14 MCP tools for instant architecture queries, call tracing, and change impact analysis.
   - Interface: MCP server (used automatically by agent) + CLI for management.
   - Storage: SQLite in `~/.cache/codebase-memory-mcp/`.
   - Indexes automatically on first use if `auto_index=true`, or when explicitly requested.

All plugins operate at different layers and complement each other without conflict.

## Notes

- **MCP tools**: Used automatically by the agent. You don't need to call them directly.
- **User commands (TUI)**: Starting with `/`, typed in the chat.
- **CLI commands**: Run in terminal (e.g., `rtk gain`, `opencode`).
- **Agent tools**: Called by the AI internally; you don't invoke them directly.
- **Automatic plugins**: Work silently without any user interaction.
- Check plugin-specific documentation for advanced configuration.
