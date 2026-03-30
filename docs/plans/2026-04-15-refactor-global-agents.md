# Plan: Refactor Global AGENTS.md with Hybrid Loading

**Created:** 2026-04-15  
**Context:** Reduce AGENTS.md using progressive disclosure + hybrid loading strategy

---

## Loading Strategy

| When to Load      | File                                  | Method          |
| ----------------- | -------------------------------------- | -----------------|
| **Session start** | AGENTS.md (Core + Source Control)       | instructions    |
| **Session start** | memory-usage.md                       | instructions    |
| **Session start**| context-mode.md                       | instructions    |
| **On commit**    | quality-gates.md                     | lazy (@reference)|
| **When needed**  | mcp-tools.md                         | lazy (@reference)|
| **When needed**  | enterprise-patterns.md               | lazy (@reference)|

---

## Execution

| Step | Description                                                           | Status |
| ---- | ---------------------------------------------------------------------- | ------ |
| 1    | Analyze AGENTS.md for contradictions                                     | ✅     |
| 2    | Extract to root AGENTS.md (~80 lines, essentials only)                 | ⏳     |
| 3    | Create memory-usage.md                                               | ⏳     |
| 4    | Create context-mode.md                                              | ⏳     |
| 5    | Create quality-gates.md (lazy)                                      | ⏳     |
| 6    | Create mcp-tools.md (lazy)                                           | ⏳     |
| 7    | Create enterprise-patterns.md (lazy)                                     | ⏳     |
| 8    | Update opencode.json with instructions array                              | ⏳     |
| 9    | Verify: root < 80 lines, links work                                | ⏳     |

---

## File Contents

### AGENTS.md (root - ~80 lines)
Core principles, source control, project rules, plan format + lazy references

### docs/agent-instructions/memory-usage.md
Memory types, scopes, simple-memory plugin rules

### docs/agent-instructions/context-mode.md
Think in Code, ctx tools, tool hierarchy

### docs/agent-instructions/quality-gates.md
Lint, typecheck, test, coverage rules (lazy)

### docs/agent-instructions/mcp-tools.md
playwright, exa, context7, markitdown (lazy)

### docs/agent-instructions/enterprise-patterns.md
Error handling, logging, observability (lazy)

---

## opencode.json

```json
{
  "instructions": [
    "~/.config/opencode/AGENTS.md",
    "~/.config/opencode/docs/agent-instructions/memory-usage.md",
    "~/.config/opencode/docs/agent-instructions/context-mode.md"
  ]
}
```

---

## Verification

- [ ] AGENTS.md ~80 lines
- [ ] memory-usage.md loaded at session start
- [ ] context-mode.md loaded at session start
- [ ] quality-gates.md lazy on commit
- [ ] All lazy links work (@reference format)