# Agent Identity Plugin

**Status:** ✅ Active
**Purpose:** Provide agent self-identity awareness and per-message attribution in multi-agent sessions.
**Plugin:** `@gotgenes/opencode-agent-identity`

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `agent_attribution` | MCP (Agent) | Returns which agent produced each assistant response and which model was used |

*Note:* Identity injection into system prompts happens automatically (no command needed).

---

## Overview

When switching between agents mid-session (e.g., Plan → Build → Plan), the AI often loses track of which agent is currently active. This plugin addresses that by:

1. **Injecting identity into system prompt:** Each turn, a one-liner is added: `You are currently operating as the "build" agent.`
2. **Providing attribution tool:** Agents can call `agent_attribution` to see a numbered list of every message and which agent/model produced it.

---

## Automatic Identity Injection

You don't need to do anything. The plugin uses hooks to:

- Detect the current agent from the user message's `info.agent` field.
- Append to the system prompt each turn:

```
You are currently operating as the "build" agent.
Your configuration file: .opencode/agent/build.md
Your mode: primary
Previous agent in session: plan (switched at 2026-04-18 22:30:00)
```

This gives agents awareness of:
- Who they are
- Agent switching history
- Workspace topology (other agents present)

---

## `agent_attribution` Tool

### Purpose

Retrieve per-message attribution for the entire session. Useful for:
- Multi-agent retrospectives
- Auditing which agent produced which response
- Debugging agent coordination issues

### Parameters

None.

### Returns

A numbered list of every message in the session:
- User messages show role only
- Assistant messages show agent name and model used

Example output:

```
1. [user] What's the token usage?
2. [assistant (build, model: openrouter/elephant-alpha)] The current usage is...
3. [assistant (plan, model: gemini-2.5-flash)] Here's the analysis...
```

---

## Usage

You can ask any agent:

```
Which agent wrote this code?
```

Or:

```
Show me the attribution for this session.
```

The agent can call `agent_attribution` and summarize the results.

For a dedicated retrospective, you could use a custom agent with a system prompt like:

```
## Multi-agent attribution
This session may involve multiple agents. To determine which agent produced each response, call the `agent_attribution` tool. It returns a numbered list of every message in the session.
```

---

## Installation

Already installed via global plugin list:

```json
{
  "plugin": ["@gotgenes/opencode-agent-identity"]
}
```

---

## How It Works

1. **`experimental.chat.messages.transform`** hook: Reads the current agent from the last user message's `info.agent` and stores it in session-scoped state.
2. **`experimental.chat.system.transform`** hook: Appends the identity statement to the system prompt using the stored state.
3. **`agent_attribution` tool**: Queries the OpenCode SDK for message metadata and formats it.

The state is keyed by session ID, so concurrent sessions don't interfere.

---

## When to Use This Plugin

- You frequently switch between Plan/Build/Review agents mid-session
- You use multiple custom agents and need to track who said what
- You're debugging multi-agent coordination issues
- You want agents to be aware of their own identity and previous agent switches

---

## Limitations

- Identity tracking requires that agent switches happen via messages with proper `info.agent` metadata (standard OpenCode behavior).
- The one-liner injection may get lost in very long system prompts; consider also referencing config files directly if needed.

---

## Related

- [Magic Context](magic-context.md) — Manages session memory and compression
- [Simple Memory](simple-memory.md) — Persistent memories for agents
