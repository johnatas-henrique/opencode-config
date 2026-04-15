---
description: Identify and consolidate near-duplicate functions across the codebase
chain: finalize
order: 2
next: finalize-03-slop
---

## 1. Determine the scope

Pick the right diff command based on current state:
- If on a feature branch: `git diff main...HEAD` combined with `git diff` for uncommitted changes
- If all changes are uncommitted: `git diff`
- The consolidation analysis focuses on changed or added functions and their relationship to the broader codebase.

## 2. Identify near-duplicates

For each changed or added function:

### Search strategies
- Search for functions with **similar names** — focus on the verb and noun (e.g., `get_user_name` vs `fetch_user_name`, `format_output` vs `render_output`)
- Search for the function's **key operations** — if it calls `.split()` then `.join()`, grep for that pattern elsewhere
- Search for functions with **similar parameter signatures** and return types
- Check other modules that **import from the same file** — they often contain related or overlapping logic

### Compare implementations
When you find functions that appear similar:
- Read both implementations in full
- Identify what they have in common
- Identify what differs: parameters, return values, side effects, error handling, edge cases

## 3. Evaluate consolidation potential

For each pair of near-duplicate functions:

### Can they be unified?
- Is one a subset of the other's functionality?
- Could a single function accept a parameter to handle both cases?
- Are the differences incidental (naming, minor formatting) or meaningful (different business logic)?

### What would change?
- Would the consolidated function produce identical results for all callers?
- If not identical, which callers would get different behavior?
- Is that different behavior acceptable or a breaking change?

### What simplifications would enable consolidation?
Sometimes functions diverge because of unnecessary complexity:
- A flag parameter that could be removed
- A special case that's no longer needed
- A parameter that's always passed the same value

## 4. Checkpoint — present candidates

**Stop and present to the user:**

Organize findings into three tiers:
1. **Exact duplicates** — identical or near-identical logic. Recommend consolidating without hesitation.
2. **Near-duplicates** — could be consolidated with a simplification. Explain what would change and which callers are affected.
3. **Look-alikes** — similar structure but meaningfully different. Note them but do not recommend consolidating.

**Wait for user approval on which consolidations to perform.**

If the user says to skip, jump to step 6.

## 5. Consolidate

For each approved consolidation:
1. Identify the canonical implementation (prefer the more general one)
2. Modify it to handle all cases if needed
3. Update all callers to use the consolidated function
4. Remove the now-redundant function(s)
5. Update any tests that referenced the old function names
6. Run the project's test suite to verify nothing broke

## 6. Summarize

Provide:
- Consolidations performed, with before/after summary
- Near-duplicates the user declined to consolidate (and why)
- Any remaining look-alikes worth monitoring

Next: run the slop workflow to detect AI-generated code patterns.