# OpenCode Agent Instructions — MANDATORY RULES

## ⚠️ CRITICAL — READ FIRST

These rules are **NOT optional**. Follow them or you will be wrong.

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

## Project Rules

- **Always read** the project's AGENTS.md file first.
- When in Plan mode, **always save** implementation plan to `docs/plans/YYYY-MM-DD-name.md`.

## Plan Format

- File name: `docs/plans/YYYY-MM-DD-name.md`
- Include **Execution** table at top with timestamps
- Update steps to ✅ when finished
- Mark superseded plans as "DISCONTINUED" in archive
- **All plans in English**

## ⚠️ MANDATORY AT SESSION START

### Memory Usage
```
memory_recall()
```
This is mandatory. Call it at the start of EVERY session.

### Context Mode
- When processing data: **USE ctx_execute**
- When analyzing files: **USE ctx_execute_file**
- Never dump raw data into context with cat/read

## ⚠️ MANDATORY FILES — LAZY LOAD

These files contain rules you **MUST** follow when relevant:

| When... | Load this file... |
| -------- | ----------------- |
| User says "commit" | @docs/agent-instructions/quality-gates.md |
| Working with MCP tools | @docs/agent-instructions/mcp-tools.md |
| Banking/enterprise code | @docs/agent-instructions/enterprise-patterns.md |

These are NOT optional. When the trigger condition applies, you **MUST** load and follow these rules.