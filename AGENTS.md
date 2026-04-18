# OpenCode Agent Instructions — MANDATORY RULES

<!-- [MEMORY] MANDATORY -->
Every session MUST start with `memory_recall()`.
Each memory MUST have a type (decision, learning, preference, blocker, context, pattern) and a scope (global, project, session).
Read `~/.config/opencode/docs/agent-instructions/memory-usage.md` and compare with your own memory list.
If global memories are missing, load them using `memory_remember(MEMORY_HERE, <TYPE>, "global")`.
Call `memory_recall()` again.
<!-- [/MEMORY] -->

<!-- [GIT] MANDATORY -->
NEVER: Mix feat+test, feat+docs, code+config in same commit.
ACTION: Always ask. Always separate.
AUTHOR: Johnatas Henrique <johnatas.henrique@gmail.com>
<!-- [/GIT] -->

---

## Core Principles

- COMMIT, TEST, PLAN files: English only
- RESPOND in user's language (user uses Portuguese → respond in Portuguese)
- FAIL after 2 attempts → stop and report
- ASK when uncertain
- NEVER expose .env, secrets, tokens
- GET web info if unsure

### Decision Hierarchy

```
Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty
```

### Before Implementing

1. Define: concrete outcome, success criteria, stopping point
2. State assumptions explicitly
3. Present multiple interpretations if ambiguous
4. Propose simpler approach if exists

### Implementation Rules

- Minimum code for the problem. Nothing speculative.
- Touch only necessary files. Clean own mess only.
- Never revert changes from other tools (package.json, generated files)

---

## Plan Format

- File: `docs/plans/YYYY-MM-DD-name.md`
- Include Execution table with timestamps
- Update steps to ✅ when done
- Mark superseded plans as "DISCONTINUED"
- All plans in English

---

<!-- [LAZY-LOAD] WHEN-RELEVANT -->
| Trigger | Load |
|---------|------|
| "commit" | @docs/agent-instructions/quality-gates.md |
| MCP tools | @docs/agent-instructions/mcp-tools.md |
| Banking | @docs/agent-instructions/enterprise-patterns.md |
<!-- [/LAZY-LOAD] -->

<!-- lean-ctx MANDATORY-->
## lean-ctx

Prefer lean-ctx MCP tools over native equivalents for token savings.
Full rules: @docs/agent-instructions/lean-ctx.md
<!-- /lean-ctx -->
