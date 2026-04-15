---
description: Detect and remove AI-generated code patterns from changed files
chain: finalize
order: 3
next: finalize-04-commit
---

## 1. Determine the diff

Pick the right diff command based on current state:
- If on a feature branch: `git diff main...HEAD` combined with `git diff` for uncommitted changes
- If all changes are uncommitted: `git diff`
- Focus exclusively on added or modified lines

## 2. Scan for AI-generated slop

For each changed file, compare the new/modified code against the surrounding unchanged code in the same file. Flag anything that breaks the local style or adds unnecessary weight:

### Unnecessary comments
- Comments restating what the code does (`# increment counter` above `counter += 1`)
- Comments inconsistent with the commenting density of the surrounding unchanged code — if the rest of the file has zero inline comments, new code shouldn't suddenly be heavily commented
- Docstrings that restate the function name and parameter types verbatim without adding insight

### Defensive over-engineering
- try/except blocks catching exceptions the called code doesn't actually raise
- None checks or fallback values not needed given the function's contract and callers — read the callers to verify
- Redundant `isinstance` checks when the type is already guaranteed by the function signature or upstream logic
- Overly broad exception handling (`except Exception`) where a specific exception type is appropriate

### Type assertion hacks
- `cast(Any, ...)` to silence type errors instead of fixing them
- `# type: ignore` without a justification comment
- Unnecessary `isinstance` checks papering over type issues rather than solving them

### Gratuitous abstraction
- New base classes, interfaces, protocols, or factories introduced for a single concrete implementation
- Wrapper functions that add no logic — just forward all arguments to another function
- Premature generalization (accepting `*args, **kwargs` when the function always receives the same specific arguments)

### Inconsistent style
- Naming conventions that don't match the rest of the file
- Quote style, import ordering, or formatting that diverges from surrounding code
- Error handling patterns that differ from the established codebase approach

### Dead code
- Commented-out code blocks
- Unused imports
- Unreachable branches (e.g., `if False:`, dead `else` after early return)
- Functions defined but never called

### Leftover debugging
- `print()` statements (unless the project uses print as its output mechanism)
- `breakpoint()`, `debugger`, `console.log()` left from debugging
- Unresolved TODO/FIXME/HACK comments that were added in this change

### Over-parameterization
- Boolean flag parameters like `do_logging=True, validate=True` that should be separate functions or removed
- Functions with more than 5-6 parameters that could accept a config object or be split

## 3. Scan for secrets

Scan all changed lines for accidentally committed sensitive data:
- API keys, tokens, or bearer credentials (strings matching common key patterns: `sk-`, `ghp_`, `AKIA`, etc.)
- Connection strings with embedded passwords
- Private keys (`BEGIN RSA PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, etc.)
- Hardcoded URLs with authentication parameters (`?token=`, `?api_key=`)
- `.env` file contents copy-pasted into source code

If any are found, **remove them immediately** and alert the user — this is not a checkpoint item, it's an emergency fix.

## 4. Checkpoint — present findings

**Stop and present to the user:**
- Slop items found, grouped by category
- For each item: the file, the offending lines, and what you'd change
- Secret scan results (should already be fixed if found)

**Wait for user approval before removing slop.**

Most slop removal is safe (removing comments, dead code, etc.) but some items may be judgment calls (e.g., "is this try/except actually unnecessary?"). Let the user decide.

## 5. Remove approved slop

Remove the approved items. After all removals in a file, verify the code still works:
- Run the project's test suite to confirm nothing broke
- If removals involved deleting code (not just comments), pay extra attention to test results

## 6. Summarize

Provide:
- Slop removed, by category and count
- Items the user declined to remove
- Any patterns worth noting (e.g., "the model consistently over-comments in this file — consider adding a note to AGENTS.md")

Next: run the commit workflow to lint, typecheck, test, and commit.
