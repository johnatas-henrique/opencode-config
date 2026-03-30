---
description: Harden code quality — fix structural issues one category at a time
chain: finalize
order: 1
next: finalize-02-consolidation
---

## 1. Determine the diff

Pick the right diff command based on current state:
- If on a feature branch: `git diff main...HEAD` combined with `git diff` for uncommitted changes
- If all changes are uncommitted: `git diff`
- The goal is to see everything that's changed relative to the last clean baseline

## 2. Discover project conventions

- Read `AGENTS.md` (or equivalent project instructions file) for project conventions, file structure, and coding standards
- Identify where the project keeps constants, configuration, and shared utilities
- Do NOT assume any paths, directory names, or conventions — derive them from the project

## 3. Assess scope

- Run `git diff --stat` to see the breadth of changes
- If changes span multiple unrelated concerns (e.g., a bug fix AND a refactor AND a new feature), flag this to the user and suggest splitting before continuing
- Proceed with the review regardless, but note scope issues in the checkpoint

## 4. Review each changed source file

For every changed source file (excluding generated output and files listed in `.gitignore`):

### Hardcoded values
- Flag magic numbers, strings, or repeated literals that should be constants
- Check if a matching constant already exists in the project's constants/config that could be reused
- Watch for repeated format strings or template patterns — these indicate a formatting helper is needed

### Abstraction placement
- Is this logic in the right module?
- Are functions doing too many things? (>40 lines is a smell, not a rule)
- Could a conditional chain be replaced with a lookup or function map?
- Is business logic leaking into UI components or vice versa?

### Spaghetti indicators
- Functions reaching into another module's internals instead of using its public API
- Circular dependency risk
- Mixed concerns in a single function (parsing AND formatting AND state mutation)
- Changes spanning unrelated files without a unifying purpose

### Maintainability
- Is the code self-documenting through naming?
- Are interfaces between components clear?
- Is error handling consistent with the rest of the codebase?
- Do new patterns match existing patterns?

### Breaking changes
- Has a public function's signature changed (parameters added/removed/reordered)?
- Has a return type changed?
- Has a default value changed that callers might depend on?
- If so, flag these — they may be intentional but should be noted

### Test coverage (flag only)
- Note any changed or added functions that have no corresponding tests
- Do NOT write tests — just flag the gaps in the checkpoint report

## 5. Checkpoint — present findings

**Stop and present to the user:**
- A categorized list of issues found, grouped by file
- Which issues you recommend fixing and which are judgment calls
- Any scope concerns from step 3
- Any breaking changes detected
- Any test coverage gaps noticed

**Wait for user approval before proceeding to fixes.**

If the user says to skip fixes, jump to step 7.

## 6. Apply corrections

For each approved fix:
- Move hardcoded values to the project's constants/config location
- Extract shared logic into utility functions in the appropriate module
- Split large functions into focused helpers
- Improve naming where intent is unclear
- Remove dead code left behind during refactoring

After applying fixes to a group of related files, run the project's test suite to verify nothing broke before continuing to the next group.

## 7. Summarize

Provide:
- Issues found and how each was addressed (or why it was skipped)
- Any remaining concerns that need human review
- Do NOT run full lint/format/typecheck here — that's workflow 04's job

Next: run the consolidation workflow to check for near-duplicate functions.
