# Memory Usage (simple-memory) — STRICT RULES

## MANDATORY AT SESSION START

You **MUST** call `memory_recall()` at the start of EVERY session. This is not optional.

## Rules — FOLLOW OR YOU WILL BE WRONG

### Session Start (MANDATORY)
```
memory_recall()
```

- Never skip this. Never.
- If you don't call `memory_recall()` at session start, you are **wrong**.

### Creating Memories
- **NEVER** call `memory_remember()` automatically
- Only call when the **user explicitly asks** you to remember something

### End of Session (MANDATORY)
- If you discovered significant patterns, decisions, or learnings, you **MUST** ask:
  ```
  "Do you want me to remember [specific thing]?"
  ```

### Contradicting Memories
- If new information contradicts existing memory: **ASK** the user before using `memory_forget()` + `memory_remember()`

## Memory Types

| Type      | Use For                          |
| --------- | --------------------------------|
| decision  | Architecture/design choices      |
| learning  | Codebase discoveries            |
| preference | User/project preferences      |
| blocker   | Known issues                 |
| context   | Feature/system info           |
| pattern   | Code patterns                |

## Memory Scopes

| Scope       | Use For                          |
| ----------- | --------------------------------|
| project     | Project-wide decisions           |
| global      | User-specific preferences        |

## Format

**One line, detailed** - Include file references when applicable.

Example: "Using Drizzle ORM over Prisma for type safety. See: src/db/schema.ts"

## Verification

If you did NOT call `memory_recall()` at session start, **STOP NOW** and call it before continuing.