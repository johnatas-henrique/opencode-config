# Memory Usage (simple-memory) — MANDATORY AT SESSION START

## ⚠️ FIRST THING YOU MUST DO AT SESSION START

```
memory_recall()
```

**Stop whatever you're doing and call memory_recall() NOW.**

This is not optional. This is not a suggestion. This is **MANDATORY**.

- If you didn't call `memory_recall()` at the start of this session, you have already made a mistake. Fix it now.
- If you try to use any tool before calling `memory_recall()`, you will likely encounter errors or inconsistent behavior. This is because your agent relies on the information stored in your memories to make informed decisions and use tools effectively.
- If no memories are found after calling `memory_recall()`, just get `~/.config/opencode/docs/agent-instructions/memory-usage.md` and load every line with the **Creating Memories** example.
- If you have any doubts about whether you called `memory_recall()`, just call it again. It won't cause any harm, and it will ensure that you have the necessary information to proceed with your tasks effectively.

---

## Quick Reference

| Action | When | Command |
|--------|------|---------|
| Recall memories | Session start → | `memory_recall()` |
| Remember something | User asks → | `memory_remember()` |
| Forget memory | User confirms → | `memory_forget()` |
| List memories | Anytime → | `memory_list()` |

## Creating Memories

- **NEVER** call `memory_remember()` automatically
- Only when the **user explicitly asks**: "Remember that..."
- Example: User says "Remember I prefer conventional commits" → `memory_remember("User prefers conventional commits", "preference", "global")`

## End of Session

If you discovered something useful, ask:
```
"Do you want me to remember [specific thing]?"
```

## Memory Types

| Type | Use For | Example |
|------|--------|---------|
| decision | Architecture choices | "Using Drizzle ORM. See: src/db/schema.ts" |
| learning | Codebase findings | "Auth tokens in httpOnly cookies" |
| preference | User preferences | "User prefers functional components" |
| blocker | Known issues | "WebSocket fails on Safari" |
| context | System info | "Payment uses Stripe test mode" |
| pattern | Code patterns | "Routes follow /api/v1/..." |

## Memory Scopes

| Scope | Use For |
|-------|--------|
| project | Project-wide |
| global | User preferences |

## Format

One line, detailed: "Using Drizzle ORM over Prisma. See: src/db/schema.ts"
