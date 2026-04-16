# OpenCode Agent Instructions — MANDATORY RULES

## ⚠️ CRITICAL — READ FIRST — MANDATORY AT SESSION START

These rules are **NOT optional**. Follow them or you will be wrong.

### FIRST THING: Memory Recall (MANDATORY)

Call this NOW at session start:
```
memory_recall()
```

If you didn't call `memory_recall()` at the start of this session, you have already made a mistake. Fix it now.

### Context Mode (MANDATORY) — ALWAYS USE FROM SESSION START

When processing data: use **ctx_execute**. Reading raw data into context is **WRONG**.
**IMPORTANT**: Use ctx tools for EVERY user question that requires reading, searching, or analyzing files. Do NOT wait for the user to specifically ask for it.

| User question... | You must use... |
|-----------------|-----------------|
| "What's in file X?" | ctx_execute_file |
| "List files in Y" | ctx_execute with glob |
| "What does function Z do?" | ctx_execute_file + search |
| "Show me the status" | ctx_execute with processing |
| "Count lines in X" | ctx_execute_file + processing |
| "Find pattern in X" | ctx_execute with grep |

| Instead of... | Use... |
|--------------|---------|
| read entire file | ctx_execute_file |
| cat file | ctx_execute_file |
| grep pattern | ctx_execute with grep |
| ls -la | ctx_execute |
| find files | ctx_execute with glob |
| wc -l | ctx_execute_file + processing |
| jq query | ctx_execute with processing |

**This is NOT optional** — apply this rule from the very first user question, not just when explicitly requested.

---

## Core Principles

- Everything that will be **committed**, like code, tests, and plans, **MUST** be written in English only.
- Always respond in the **language the user is using** in conversation. If user writes in Portuguese, respond in Portuguese.
- If a task step fails after two attempts, **stop and report** to the user instead of continuing silently.
- **ALWAYS use Ask Tool** when you have questions for the user.
- Never commit or expose `.env` files, secrets, tokens, or credentials of any kind.
- Unless you are absolutely sure that you have correct and up-to-date information in your knowledge, always get information from the web.

### Decision Hierarchy

When conflicts arise, use this priority order:

```
Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty
```

### Goal-First Rule

Before implementing, always define: (1) concrete outcome, (2) success signal/criteria, (3) stopping point.

### Think Before Coding

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.

### Simplicity First

- Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code.

### Surgical Changes

- Touch only what you must. Clean up only your own mess.
- Don't "improve" adjacent code, comments, or formatting.
- When your changes create orphans: remove unused imports/variables/functions.

### External Changes

Never delete or revert modifications made by tools other than yourself (e.g., package.json, generated files). Ask the user or ignore.

## Source Control (Git)

- Always use `--author="Johnatas Henrique <johnatas.henrique@gmail.com>"` for commits.
- Use **atomic commits**: one commit per independent logical change.
- **Never run `git commit` without explicit user permission.** Ask first.
- When user asks to commit, **present structured list first** with files grouped and commit message.
- **Never run `git push` directly.**

### Commits Atômicos (OBRIGATÓRIO)

**SEMPRE separe por tipo. Nunca misture em um commit:**
- `feat:` + `test:` → commits separados
- `feat:` + `docs:` → commits separados
- Code + Config → commits separados

**Faça automaticamente. Não pergunte. Separe e commite.****

## Plan Format

- File name: `docs/plans/YYYY-MM-DD-name.md`
- Include **Execution** table at top with timestamps
- Update steps to ✅ when finished
- Mark superseded plans as "DISCONTINUED" in archive
- **All plans in English**

## ⚠️ LAZY LOAD — WHEN RELEVANT

| When... | Load this file... |
|---------|-------------------|
| User says "commit" | @docs/agent-instructions/quality-gates.md |
| Working with MCP tools | @docs/agent-instructions/mcp-tools.md |
| Banking/enterprise | @docs/agent-instructions/enterprise-patterns.md |
