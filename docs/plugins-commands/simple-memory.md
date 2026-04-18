# Simple Memory Plugin

**Status:** ✅ Active
**Purpose:** Persistent memory across sessions using structured memories (decision, learning, preference, blocker, context, pattern).
**Plugin:** `@knikolov/opencode-plugin-simple-memory`

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `memory_remember(type, scope, content)` | MCP (Agent) | Store a new memory (only when user explicitly asks) |
| `memory_recall(scope, type, query)` | MCP (Agent) | Retrieve memories by scope, type, or search query (call at session start) |
| `memory_update(type, scope, content)` | MCP (Agent) | Update an existing memory (with audit trail) |
| `memory_forget(type, scope, reason)` | MCP (Agent) | Delete a memory (with audit logging) |
| `memory_list()` | MCP (Agent) | List all scopes and types for discovery |

---

## Memory System

Memories are structured records with:
- **type**: category (decision, learning, preference, blocker, context, pattern)
- **scope**: organizational boundary (project, user, auth, api, database, testing, deployment, or custom)
- **content**: detailed single-line description (include file references when relevant)

Stored as daily logfmt files in `.opencode/memory/`.

---

## Memory Types

| Type | Use For | Example |
|------|---------|---------|
| `decision` | Architectural/design decisions | `Using Drizzle ORM over Prisma for type safety. See: src/db/schema.ts` |
| `learning` | Things learned about the codebase | `Auth tokens stored in httpOnly cookies, not localStorage. See: src/middleware/auth.ts` |
| `preference` | User or project preferences | `User prefers functional components over class components` |
| `blocker` | Current blockers or issues | `Websocket reconnection fails on Safari - tracking in issue #42` |
| `context` | Feature/system info | `Payment integration uses Stripe in test mode. API keys in .env.local` |
| `pattern` | Recurring code patterns | `All API routes follow /api/v1/[resource]/[action] pattern. See: src/routes/` |

---

## Memory Scopes

Use scopes to organize memories logically:

| Scope | Use For |
|-------|---------|
| `project` | Project-wide decisions and patterns |
| `user` | User-specific preferences |
| `auth` | Authentication/authorization context |
| `api` | API design decisions |
| `database` | Database schema and query patterns |
| `testing` | Testing strategies and known issues |
| `deployment` | Deployment and infrastructure notes |
| Custom (any) | Tailor to your domain |

---

## Tools Details

### `memory_remember(type, scope, content)`

Store a memory. **Only call when user explicitly asks to remember something.**

Parameters:
- `type`: one of the 6 memory types
- `scope`: string (e.g., `"project"`, `"user"`, `"api"`)
- `content`: detailed single-line description (include file references)

Example:
```json
{
  "type": "preference",
  "scope": "user",
  "content": "User prefers pnpm over npm for package management"
}
```

---

### `memory_recall(scope, type, query)`

Retrieve memories. **Should be called at session start** (mandatory per AGENTS.md) and before answering questions.

Parameters (all optional, but at least one should be provided):
- `scope`: filter by scope
- `type`: filter by type
- `query`: search text (matches against content)

Example:
```json
{
  "scope": "user",
  "type": "preference"
}
```

Returns matching memories with timestamps.

---

### `memory_update(type, scope, content)`

Update an existing memory. When new information contradicts an old memory, prefer this over creating a new one.

Parameters: same as `memory_remember` plus you should reference the memory being updated (the tool handles this internally based on match).

---

### `memory_forget(type, scope, reason)`

Delete a memory with audit logging.

Parameters:
- `type`: memory type
- `scope`: memory scope
- `reason`: explanation for deletion (required)

---

### `memory_list()`

List all scopes and types currently in use. Useful for discovery.

---

## Usage Guidelines (AGENTS.md Pattern)

From your own AGENTS.md, the standard rules:

1. **MANDATORY:** Call `memory_recall()` at session start and before answering questions.
2. **NEVER** use `memory_remember()` automatically — only when user explicitly says "Remember that..." or similar.
3. When user asks to remember something: store as decision, learning, preference, blocker, context, or pattern.
4. If new info contradicts existing memory: ask user before using `memory_forget()` + `memory_remember()`.
5. **End of session:** If significant patterns, decisions, or learnings were discovered, ask user: "Would you like me to store this in memory?"

---

## Storage Format

Memories are stored in `.opencode/memory/YYYY-MM-DD.logfmt` as logfmt lines:

```
ts=2025-12-15T03:29:22.830Z type=learning scope=auth content="Token expiry uses JWT exp claim from Cognito, see src/middleware/auth.ts"
```

This format is:
- Human-readable
- Git-friendly (one line per memory)
- Easy to append

---

## Example Interaction

```
User: Remember that my name is Kris
AI: [calls memory_remember]
I've stored that your name is Kris.

User: My preferred programming language is Erlang
AI: [calls memory_remember]
Got it! I've noted your preference.

User: What do you know about me?
AI: [calls memory_recall(scope="user")]
Here's what I know about you:
- Your name is Kris
- Preferred programming language: Erlang
```

---

## Installation

Already installed globally in your OpenCode config:

```json
{
  "plugin": ["@knikolov/opencode-plugin-simple-memory"]
}
```

No additional setup required. Memories are stored per-project in `.opencode/memory/`.

---

## Notes

- **One line per memory:** Keep content concise to avoid git conflicts.
- **Include file references:** Use `See: path/to/file` when applicable.
- **Be detailed:** Include enough context to be useful later.
- **No automatic storage:** The AI should never call `memory_remember` without explicit user permission.

---

## Troubleshooting

**Memories not persisting?**
- Check `.opencode/memory/` directory exists and is writable.
- Verify plugin is in `opencode.json` plugin list.

**Want to disable?**
Remove from plugin list and restart OpenCode. Memories remain on disk but won't be accessible.

---

## Related

- [Magic Context](magic-context.md) — Higher-level context management with compartments
- [Agent Identity](agent-identity.md) — Agent self-awareness in multi-agent sessions
