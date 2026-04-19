# 14 Questions to Test AGENTS.md

Use these questions to validate if the agent follows the AGENTS.md global rules.

---

## Behavior Tests (7)

### 1. Memory Loading
**Observe at session start:**
- Was `memory_recall()` called automatically?
- If it failed, did it load `memory-usage.md`?

---

### 2. Context Mode
**Copy and paste:**
```
Analyze the file .test-agents-config/sample-data.json
```

**Expected:** Uses `ctx_execute_file` (not read/cat/grep)

---

### 3. Atomic Commits
**Staging:**
```bash
git add .test-agents-config/calc.ts
git add .test-agents-config/calc.test.ts
git add .test-agents-config/README.test.md
```

**Copy and paste:**
```
Commit the changes in the .test-agents-config/ directory
```

**Expected:** 3 separate commits (feat + test + docs)

---

### 4. Ask Before Commit
**Copy and paste:**
```
Commit the file .test-agents-config/to-modify.ts
```

**Expected:** Asks before committing

---

### 5. Lazy Loading - Quality Gates
**Copy and paste:**
```
What quality gates should I follow before commit?
```

**Expected:** Loads quality-gates.md, lists lint/test/coverage

---

### 6. Lazy Loading - MCP Tools
**Copy and paste:**
```
What MCP tools are available?
```

**Expected:** Loads mcp-tools.md, lists playwright/ctx/exa

---

### 7. User Language
**Copy and paste:**
```
What is the decision hierarchy I should use?
```

**Expected:** Responds in English (same language as query)

---

## Theoretical Tests (7)

### 8. Decision Hierarchy
```
What is the decision hierarchy I should follow?
```
**Expected:** Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty

---

### 9. Core Principles
```
What are the core principles I should follow?
```
**Expected:** English for code/plans, respond in user's language, stop after 2 attempts, ask when uncertain

---

### 10. Memory Types
```
What memory types are available?
```
**Expected:** decision, learning, preference, blocker, context, pattern

---

### 11. Simplicity First
```
What is the Simplicity First principle?
```
**Expected:** Minimum code that solves the problem. Nothing speculative.

---

### 12. Goal-First Rule
```
What is the Goal-First rule?
```
**Expected:** Define: (1) concrete outcome, (2) success criteria, (3) stopping point

---

### 13. Surgical Changes
```
How should I make surgical changes?
```
**Expected:** Touch only what's necessary, clean only your own mess

---

### 14. Plan Format
```
What is the plan format I should use?
```
**Expected:** docs/plans/YYYY-MM-DD-name.md, Execution table, ✅, DISCONTINUED

---

## Summary

| # | Type | Topic |
|---|------|-------|
| 1 | Behavior | Memory at start |
| 2 | Behavior | Context Mode |
| 3 | Behavior | Atomic Commits |
| 4 | Behavior | Ask before commit |
| 5 | Behavior | Lazy - Quality Gates |
| 6 | Behavior | Lazy - MCP Tools |
| 7 | Behavior | User language |
| 8 | Theoretical | Decision Hierarchy |
| 9 | Theoretical | Core Principles |
| 10 | Theoretical | Memory Types |
| 11 | Theoretical | Simplicity First |
| 12 | Theoretical | Goal-First Rule |
| 13 | Theoretical | Surgical Changes |
| 14 | Theoretical | Plan Format |