# Test Questions for AGENTS.md Global

Use these questions to verify if the global AGENTS.md is loading correctly in any project.

---

## Testing Strategy

### Session Start (loaded via instructions array)
- AGENTS.md (84 lines - root)
- memory-usage.md (simple-memory rules)
- context-mode.md (ctx_execute, sandbox rules)

### Lazy Loading (@reference)
- quality-gates.md (on commit)
- mcp-tools.md (when using tools)
- enterprise-patterns.md (when banking)

---

## Questions

```
1. What is loaded at session start?

2. List my global memories

3. What are the memory types and scopes available?

4. What are the quality gates mandatory before commit?

5. What is the decision hierarchy we should use?

6. What are the core principles I should follow?

7. What is the Simplicity First principle?

8. What is the "Think Before Coding" approach?

9. What tools should I use for data analysis in context-mode?

10. How do I use playwright, exa, and context7?

11. What enterprise patterns should I use for banking code?

12. How do I handle errors in production systems?

13. What is the goal-first rule?

14. How do I do surgical changes?
```

---

## Expected Answers

| #   | Expected Answer                                                            |
| --- | -------------------------------------------------------------------------- |
| 1   | AGENTS.md, memory-usage.md, context-mode.md (loaded at session start)    |
| 2   | User's global memories (preferences, decisions, patterns)                  |
| 3   | decision, learning, preference, blocker, context, pattern                  |
| 4   | lint + format → typecheck → test → coverage 80%                           |
| 5   | Constraints > Correctness > Goal Fit > Reversibility > Simplicity >...    |
| 6   | English for code/plans, respond in user's language, Ask Tool for questions |
| 7   | Minimum code that solves the problem, nothing speculative                  |
| 8   | State assumptions, ask if uncertain, present tradeoffs                     |
| 9   | ctx_execute, ctx_batch_execute, ctx_execute_file, ctx_search              |
| 10  | playwright for browser, exa for web search, context7 for docs             |
| 11  | typed errors, audit trail, structured logs, correlation IDs, observability |
| 12  | Use typed errors, never any, add audit trail for financial/auth           |
| 13  | Define: (1) concrete outcome, (2) success criteria, (3) stopping point    |
| 14  | Touch only what you must, remove only orphans from YOUR changes           |

---

## Configuration

The global AGENTS.md is configured to load automatically via `opencode.json`:

```json
{
  "instructions": [
    "~/.config/opencode/AGENTS.md",
    "~/.config/opencode/docs/agent-instructions/memory-usage.md",
    "~/.config/opencode/docs/agent-instructions/context-mode.md"
  ]
}
```

Location: `~/.config/opencode/opencode.json`

---

## File Structure

```
~/.config/opencode/
├── AGENTS.md                              (84 lines - root)
└── docs/agent-instructions/
    ├── memory-usage.md                   (session start)
    ├── context-mode.md                   (session start)
    ├── quality-gates.md                  (lazy - on commit)
    ├── mcp-tools.md                      (lazy - when needed)
    └── enterprise-patterns.md            (lazy - banking)
```

---

## How to Test

1. Start a new OpenCode session in any project
2. Ask question #1 - should show 3 files loaded
3. Ask question #2 - should list global memories
4. Ask question #4 - should show lazy loading works (file not in memory yet)
5. Ask question about "commit" - should trigger quality-gates.md
6. Verify context-mode rules are being followed (ctx_execute usage)