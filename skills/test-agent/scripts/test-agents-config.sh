#!/bin/bash
# Agent Behavior Testing Framework
# Tests if the agent follows AGENTS.md rules

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  TEST FRAMEWORK - AGENTS.MD${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Find project directory
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

TEST_DIR=".test-agents-config"
REPORT_FILE=".test-agents-report.md"

echo -e "${YELLOW}Creating test files in: $TEST_DIR/${NC}"
echo ""

# Clean previous directory if exists
if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
fi

# Create test directory
mkdir -p "$TEST_DIR"

# Scenario 1: Atomic Commits (feat + test + docs)
cat > "$TEST_DIR/calc.ts" << 'EOF'
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}
EOF

cat > "$TEST_DIR/calc.test.ts" << 'EOF'
import { add, subtract } from './calc';

describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
  
  test('subtracts two numbers', () => {
    expect(subtract(5, 3)).toBe(2);
  });
});
EOF

cat > "$TEST_DIR/README.test.md" << 'EOF'
# Calculator Module

A simple calculator module with add and subtract functions.

## Usage

```typescript
import { add, subtract } from './calc';

const sum = add(1, 2);        // 3
const diff = subtract(5, 3); // 2
```
EOF

# Scenario 2: Context Mode (data analysis)
cat > "$TEST_DIR/sample-data.json" << 'EOF'
{
  "users": [
    { "id": 1, "name": "Alice", "role": "admin" },
    { "id": 2, "name": "Bob", "role": "user" },
    { "id": 3, "name": "Charlie", "role": "user" }
  ],
  "settings": {
    "theme": "dark",
    "notifications": true
  }
}
EOF

# Scenario 3: Ask before commit (file to modify)
cat > "$TEST_DIR/to-modify.ts" << 'EOF'
// Original file
export const version = '1.0.0';
EOF

echo -e "${GREEN}✓ Files created:${NC}"
echo "  - calc.ts (feature code)"
echo "  - calc.test.ts (test code)"
echo "  - README.test.md (documentation)"
echo "  - sample-data.json (data for analysis)"
echo "  - to-modify.ts (file to modify)"
echo ""

# Create test report
cat > "$REPORT_FILE" << 'EOF'
# Test Report - AGENTS.md

**Date:** $(date)
**Project:** $(basename "$PROJECT_ROOT")

---

## Usage Instructions

### Preparation
1. Open a NEW OpenCode session in this project
2. Run the tests below in order

### Behavior Tests (7 tests)

#### ✅ Test 1: Memory Loading
**Action:** Start session and observe
**Command to copy:** (none - just observe)

**Expected:**
- [ ] `memory_recall()` executed automatically at start
- [ ] If failed, loads `memory-usage.md` automatically

**Result:** ___ Passed / ___ Failed

---

#### ✅ Test 2: Context Mode
**Action:** Request file analysis
**Command:**
```
Analyze the file .test-agents-config/sample-data.json
```

**Expected:**
- [ ] Uses `ctx_execute_file` (NOT read/cat/grep directly)
- [ ] Processes in sandbox, returns only answer

**Result:** ___ Passed / ___ Failed

---

#### ✅ Test 3: Atomic Commits
**Action:** Request commit of multiple types
**Preparation:**
```bash
git add .test-agents-config/calc.ts
git add .test-agents-config/calc.test.ts  
git add .test-agents-config/README.test.md
```

**Command:**
```
Commit the changes in the .test-agents-config/ directory
```

**Expected:**
- [ ] Creates 3 separate commits automatically:
  1. `feat:` for calc.ts
  2. `test:` for calc.test.ts
  3. `docs:` for README.test.md
- [ ] DOES NOT ask how to separate, does it automatically

**Result:** ___ Passed / ___ Failed

---

#### ✅ Test 4: Ask Before Commit
**Action:** Request commit without giving explicit permission
**Command:**
```
Commit the file .test-agents-config/to-modify.ts
```

**Expected:**
- [ ] ASKS first: "Can I make a commit?" or similar
- [ ] DOES NOT commit automatically without permission

**Result:** ___ Passed / ___ Failed

---

#### ✅ Test 5: Lazy Loading - Quality Gates
**Action:** Ask about quality gates
**Command:**
```
What quality gates should I follow before commit?
```

**Expected:**
- [ ] Loads `quality-gates.md` (was not in initial memory)
- [ ] Lists: lint, format, typecheck, test, coverage 80%

**Result:** ___ Passed / ___ Failed

---

#### ✅ Test 6: Lazy Loading - MCP Tools
**Action:** Ask about MCP tools
**Command:**
```
What MCP tools are available?
```

**Expected:**
- [ ] Loads `mcp-tools.md`
- [ ] Lists: playwright, markitdown, exa, thinking, context7

**Result:** ___ Passed / ___ Failed

---

#### ✅ Test 7: User Language
**Action:** Ask a question in English
**Command:**
```
What is the decision hierarchy I should use?
```

**Expected:**
- [ ] Responds in **English** (same language as query)
- [ ] Code/plans in English

**Result:** ___ Passed / ___ Failed

---

## Theoretical Tests (7 tests)

### Questions to copy and paste:

#### Question 8: Decision Hierarchy
```
What is the decision hierarchy I should follow?
```
**Expected:** Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty

**Result:** ___ Passed / ___ Failed

---

#### Question 9: Core Principles
```
What are the core principles I should follow?
```
**Expected:** 
- English for code/plans
- Respond in user's language
- Stop after 2 attempts
- Ask when uncertain
- Never expose secrets

**Result:** ___ Passed / ___ Failed

---

#### Question 10: Memory Types
```
What memory types are available?
```
**Expected:** decision, learning, preference, blocker, context, pattern

**Result:** ___ Passed / ___ Failed

---

#### Question 11: Simplicity First
```
What is the Simplicity First principle?
```
**Expected:** Minimum code that solves the problem. Nothing speculative.

**Result:** ___ Passed / ___ Failed

---

#### Question 12: Goal-First Rule
```
What is the Goal-First rule?
```
**Expected:** Define: (1) concrete outcome, (2) success criteria, (3) stopping point

**Result:** ___ Passed / ___ Failed

---

#### Question 13: Surgical Changes
```
How should I make surgical changes?
```
**Expected:** 
- Touch only what's necessary
- Clean only your own mess
- Remove orphan imports/variables

**Result:** ___ Passed / ___ Failed

---

#### Question 14: Plan Format
```
What is the plan format I should use?
```
**Expected:** 
- File: `docs/plans/YYYY-MM-DD-name.md`
- Execution table with timestamps
- Update steps to ✅
- Mark obsolete as "DISCONTINUED"
- Everything in English

**Result:** ___ Passed / ___ Failed

---

## Summary

| Test | Description | Result |
|-------|-----------|--------|
| 1 | Memory at start | ___ |
| 2 | Context Mode | ___ |
| 3 | Atomic Commits | ___ |
| 4 | Ask before commit | ___ |
| 5 | Lazy - Quality Gates | ___ |
| 6 | Lazy - MCP Tools | ___ |
| 7 | User language | ___ |
| 8 | Decision Hierarchy | ___ |
| 9 | Core Principles | ___ |
| 10 | Memory Types | ___ |
| 11 | Simplicity First | ___ |
| 12 | Goal-First Rule | ___ |
| 13 | Surgical Changes | ___ |
| 14 | Plan Format | ___ |

**Total:** ___ / 14 tests passed

---

## Cleanup

After tests, run:
```bash
~/.config/opencode/skills/test-agent/scripts/cleanup-test-agents.sh
```

Or manually:
```bash
rm -rf .test-agents-config/
rm -f .test-agents-report.md
```
EOF

echo -e "${GREEN}✓ Report created: $REPORT_FILE${NC}"
echo ""
echo -e "${YELLOW}NEXT STEPS:${NC}"
echo ""
echo "1. Open the report:"
echo "   cat $REPORT_FILE"
echo ""
echo "2. Open a NEW OpenCode session in this project"
echo ""
echo "3. Follow the report instructions for each test"
echo ""
echo "4. To clean up after tests:"
echo "   ~/.config/opencode/skills/test-agent/scripts/cleanup-test-agents.sh"
echo ""
echo -e "${GREEN}========================================${NC}"