# Plugin Commands Reference

This directory contains reference documentation for the commands and tools provided by installed OpenCode plugins.

## Plugins Index

| Plugin | Purpose | Interface | Main Commands/Tools | Status |
|--------|---------|-----------|---------------------|--------|
| [lean-ctx](lean-ctx.md) | Shell & file compression via MCP | Bash (CLI) + MCP | `ctx_read`, `ctx_shell`, `ctx_search`, `ctx_tree`, CLI: `lean-ctx` | ✅ Active |
| [magic-context](magic-context.md) | Chat compression + memory | TUI + Agent Tools + MCP | `/ctx-status`, `/ctx-flush`, `/ctx-aug`, `/ctx-dream`, `ctx_reduce`, `ctx_expand` | ✅ Active |
| [session-recall](session-recall.md) | Search past sessions | Agent Tools | `session-search`, `session-title-search`, `session-transcript` | ✅ Active |
| [opencode-handoff](opencode-handoff.md) | Create handoff prompts for new sessions | TUI + Agent Tools | `/handoff <goal>`, `read_session` | ✅ Active |
| [agent-identity](agent-identity.md) | Agent self-identity & attribution | Automatic + Agent Tools | (injects identity), `agent_attribution` | ✅ Active |
| [simple-memory](simple-memory.md) | Persistent cross-session memory | Agent Tools | `memory_remember`, `memory_recall`, `memory_update`, `memory_forget`, `memory_list` | ✅ Active |
| [md-table-formatter](md-table-formatter.md) | Auto-format markdown tables | Automatic | (works silently) | ✅ Active |

## Quick Reference

### By Use Case

| Task | Tool/Command | Interface | Plugin |
|------|--------------|-----------|--------|
| Compress shell output | `ctx_shell` (MCP) / `lean-ctx -c` (CLI) | Bash | lean-ctx |
| Read file efficiently | `ctx_read` (MCP) / `lean-ctx read` (CLI) | Bash | lean-ctx |
| Search code | `ctx_search` (MCP) / `lean-ctx grep` (CLI) | Bash | lean-ctx |
| Check token usage | `/ctx-status` | TUI | magic-context |
| Force cleanup | `/ctx-flush` | TUI | magic-context |
| Search past sessions | `/sr-search` or ask AI | TUI / Agent | session-recall |
| Run background maintenance | `/ctx-dream` | TUI | magic-context |
| Create handoff prompt | `/handoff <goal>` | TUI | opencode-handoff |
| View agent attribution | `agent_attribution` (AI calls) | Agent Tool | agent-identity |
| Store memories | `memory_remember` (AI calls) | Agent Tool | simple-memory |
| Recall memories | `memory_recall` (AI calls) | Agent Tool | simple-memory |
| Format markdown tables | Automatic | Automatic | md-table-formatter |

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
| lean-ctx | `~/.lean-ctx/config.toml` | Global |
| magic-context | `magic-context.jsonc` | Global or per-project |
| session-recall | (automatic, no config) | — |
| opencode-handoff | (automatic, no config) | — |
| agent-identity | (automatic, no config) | — |
| simple-memory | `.opencode/memory/` (storage) | Per-project |
| md-table-formatter | (automatic, no config) | — |

## How Plugins Work Together

1. **lean-ctx**: Compresses shell output and file reads **before** they enter the chat. Works via MCP tools and optional shell hooks.
   - Interface: Bash CLI (`lean-ctx -c`) and MCP tools used by AI.

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

7. **md-table-formatter**: Automatically formats markdown tables in AI responses.
   - Interface: Automatic (no user interaction).

All plugins operate at different layers and complement each other without conflict.

## Notes

- **MCP tools**: Used automatically by the agent. You don't need to call them directly.
- **User commands (TUI)**: Starting with `/`, typed in the chat.
- **CLI commands**: Run in terminal (e.g., `lean-ctx gain`, `opencode`).
- **Agent tools**: Called by the AI internally; you don't invoke them directly.
- **Automatic plugins**: Work silently without any user interaction.
- Check plugin-specific documentation for advanced configuration.
