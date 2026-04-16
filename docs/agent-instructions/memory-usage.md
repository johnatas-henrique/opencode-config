# Memory Usage (simple-memory) — MANDATORY

<!-- [MEMORY] MANDATORY -->
memory_recall()
MANDATORY: Call at session start. Before any tool.
NEVER: Use any tool before memory_recall().
<!-- [/MEMORY] -->

---

## Actions

| Action | When | Command |
|--------|------|---------|
| recall | SESSION START | `memory_recall()` |
| remember | USER ASKS | `memory_remember(content, type, scope)` |
| forget | USER CONFIRMS | `memory_forget(scope, type, reason)` |
| list | ANYTIME | `memory_list()` |

---

## Creating Memories

NEVER: Call memory_remember() automatically
ONLY: When user explicitly says "Remember that..."

Example:
- User: "Remember I prefer conventional commits"
- Action: `memory_remember("User prefers conventional commits", "preference", "global")`

---

## Memory Types

- decision: Architecture choices (include file reference)
- learning: Codebase findings
- preference: User preferences
- blocker: Known issues
- context: System info
- pattern: Code patterns

## Scopes

- project: Project-wide
- global: User preferences

---

## End of Session

If useful: Ask "Do you want me to remember [specific thing]?"

---

## Format

One line, detailed: "Using Drizzle ORM. See: src/db/schema.ts"
