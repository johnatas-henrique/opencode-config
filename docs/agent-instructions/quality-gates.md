# Quality Gates (MANDATORY)

## Overview

Before any commit, you MUST ensure all quality gates pass. This is mandatory - do not skip any step.

## Quality Gates

### 1. Linting & Formatting

Fix all lint/format errors:

```bash
npm run lint        # or: ruff check . --fix
npm run format      # or: ruff format .
```

### 2. Type Checking

Ensure type safety:

```bash
npx tsc --noEmit    # or: mypy .
```

### 3. Tests

All tests must pass:

```bash
npm test            # or: pytest
```

### 4. Coverage

Minimum 80% coverage required. If coverage is below 80%, do not proceed to commit.

If any gate fails, **STOP** and report to user.

## Quality Chain (workflows)

Before committing, run the quality chain to ensure code quality:

### Workflows

- `workflows/finalize-01-hardening.md` — Fix code quality issues (spaghetti, constants, naming)
- `workflows/finalize-02-consolidation.md` — Find and merge duplicate functions
- `workflows/finalize-03-slop.md` — Remove AI-generated code patterns (unnecessary comments, over-engineering)
- `workflows/finalize-04-commit.md` — Quality gate + commit (lint, typecheck, test, then commit)

### Running the Chain

**Full chain:**
```
Follow the quality chain: execute workflows/finalize-01-hardening.md, then workflows/finalize-02-consolidation.md, then workflows/finalize-03-slop.md, and finally workflows/finalize-04-commit.md
```

**Single workflow:**
```
Follow workflows/finalize-03-slop.md to clean the current diff
```

## Notes

- These rules apply to ALL commits
- No exceptions - even small changes must pass quality gates
- If tests are failing, fix before proceeding
- Coverage is a hard requirement - cannot be bypassed