## Tool Use Contract

### 1. Bundle Read-Only Calls

Independent reads/searches/outlines/zooms/callgraphs/greps → emit in **one message**. Sequence only when a later call depends on an earlier result.

### 2. AFT-first, fallback-safe

| Prefer                                                          | When to fallback                                     |
| --------------------------------------------------------------- | ---------------------------------------------------- |
| `aft_*` for nav, read, edit, search, refactor, shell, diagnostics | AFT `success: false`                                   |
|                                                                 | AFT `complete: false` + gap is material                |
|                                                                 | Target unindexed or non-code (config, binary, prose) |
|                                                                 | Need exact raw shell behavior                        |

**Honesty contract**: inspect `success` + `complete` before trusting. `complete:false` = partial — resolve `skipped_files`, `unchecked_files`, `walk_truncated` before acting.

### 3. Exploration — Structure before text

`aft_outline` → `aft_zoom` / focused `read` → full `read` only if needed.
- Exact strings → `grep`
- Concepts → `aft_search`
- Structure → `ast_grep_search`

### 4. Investigation Loop

```
FRAME → PROJECT (next 2-4 rounds?) → FAN-OUT (map: files, tests, configs, contracts)
→ DRILL-IN (confirm: symbols, errors, call paths) → FIRE (all independent calls in one wave)
→ CLASSIFY (KEEP / MAYBE / DISCARD) → PRUNE noise → SYNTHESIZE (confirmed + open)
→ PLAN NEXT (another wave?)
```

Do **not** begin edits while important OPEN items remain.

### 5. 2-4 Round Projection

Before any exploratory call:
- If this succeeds, what next?
- If this fails, what alternate names/tools?
- What fan-out map, exact evidence, tests, configs, callers needed?
- **Bundle all independent calls from that projection now.**

### 6. Fan-out vs Drill-in

| Dimension | Tools                                                            | Answers                 |
| --------- | ---------------------------------------------------------------- | ----------------------- |
| Fan-out   | `aft_outline`, `glob`, `grep` broad, `aft_search`, `aft_inspect`           | "What's near this?"     |
| Drill-in  | `aft_zoom`, `read` range, `grep` exact, `ast_grep_search`, `aft_callgraph` | "What exactly happens?" |

### 7. Tool routing

| Intent               | Use first                                 | Fallback                   |
| -------------------- | ----------------------------------------- | -------------------------- |
| List files           | `aft_outline <dir> files:true` / `glob`       | `read dir` / `find`            |
| File structure       | `aft_outline <file>`                        | `grep defs`                  |
| Inspect symbol       | `aft_zoom <file> <symbol>`                  | `read` range                 |
| Find by concept      | `aft_search <concept>`                      | `grep` synonyms              |
| Find exact text      | `grep <literal/regex>`                      | `rg` via bash                |
| AST search/replace   | `ast_grep_search` / `ast_grep_replace dryRun` | manual edit                |
| Callers/callees      | `aft_callgraph callers/call_tree`           | `grep` symbol refs           |
| Impact               | `aft_callgraph impact`                      | grep + tests               |
| Merge conflicts      | `aft_conflicts`                             | `git status` + grep          |
| Imports              | `aft_import add/remove/organize`            | manual edit                |
| Replace symbol body  | `edit symbol:...`                           | manual patch               |
| Add member/decorator | `aft_transform`                             | manual edit                |
| Move/extract/inline  | `aft_refactor`                              | manual refactor            |
| Move/rename file     | `aft_move`                                  | `mv` + fix imports           |
| Delete files         | `aft_delete`                                | `rm` only with safety review |
| Undo/checkpoint      | `aft_safety`                                | `git diff/restore`           |
| Diagnostics          | `lsp_diagnostics`                           | project typecheck          |
| Health snapshot      | `aft_inspect`                               | manual review              |
| Shell/test/build     | `bash`                                      | native shell               |

### 8. Safe vs Unsafe bundling

**Safe (bundle freely):** all read/search/exploration — outline, zoom, search, inspect, conflicts, callgraph (read-only), grep, glob, read, ast_grep_search, diagnostics, git status/diff/log, web search.

**Never in parallel (sequence one-by-one):** write, edit, apply_patch, ast_grep_replace (applying), aft_import, aft_transform, aft_refactor, aft_move, aft_delete, aft_safety restore/undo, dep installs, commits, pushes, destructive shell, parallel edits to related files.

Investigation = parallel. Patching = sequential.

### 9. Editing workflow

**Before:**
1. Confirm target with `aft_zoom`/`read`/`grep`/`ast_grep_search`
2. Multi-file/load-bearing change → `aft_callgraph impact`
3. Broad/risky → `aft_safety checkpoint`
4. Locate tests via `glob`/`grep`

**During (prefer in order):**
- `edit symbol:` for full symbol replacement
- `aft_import` for imports
- `aft_transform` for structural additions
- `aft_refactor` for move/extract/inline
- `apply_patch` for multi-file text AFT can't model
- `ast_grep_replace dryRun` first

**After:**
1. `lsp_diagnostics` on touched files
2. Smallest meaningful test/typecheck/lint via `bash`
3. `git diff` — verify intended-only changes
4. Don't claim full verification if AFT reports skipped/unchecked

### 10. Load-bearing files

Defines: shared infra, public API, auth/security, routing, persistence, build harness, config loading, widely imported types, many callers.

**Before editing:**
1. `aft_outline`
2. `aft_zoom` affected symbols / read ranges
3. `aft_callgraph impact`
4. `grep` imports/call sites
5. Read tests
6. `aft_safety checkpoint` if broad/risky

### 11. Wave shapes by task

**Debug unknown failure:**
Wave 1: grep error/stack → aft_search behavior → aft_outline area → glob tests → callgraph suspect symbol → read candidate
Wave 2: zoom source → read tests/config → grep alternate errors → diagnostics

**Implement feature:**
Wave 1: aft_outline area → aft_search behavior → grep keywords → glob tests → aft_inspect
Wave 2: zoom extension points → read contracts/configs → callgraph insertion point
Wave 3: callgraph impact → checkpoint

**Refactor:**
Wave 1: outline → zoom symbols → callgraph callers/impact → grep refs → glob tests → inspect metrics
Wave 2: read high-impact callers → aft_search related → ast_grep duplicates → checkpoint

**Review (3 axes):**
Wave 1: outline → inspect → callgraph impact → grep validation/auth/error → ast_grep risky patterns → glob tests

Review axes: **correctness** (invalid states, broken invariants), **security** (missing auth, unsafe trust, secret exposure), **maintainability** (duplicated logic, hidden coupling, poor testability). Tie every finding to source evidence.

### 12. Query construction

- Fan-out: broad but bounded to source area
- Drill-in: exact symbols, error strings, config keys, line ranges
- Bundle variants/synonyms in one grep
- Pair conceptual `aft_search` with exact `grep` for important behavior
- Exclude: deps, generated output, build artifacts, coverage, minified bundles, snapshots, vendor
- Search tests separately and explicitly when behavior is unclear
- Use `ast_grep_search` for syntactic structures grep can't model

### 13. Classification

After every wave: classify each result

```
KEEP    — direct evidence
MAYBE   — plausible but unconfirmed
DISCARD — empty, noise, generated, vendored, stale, irrelevant
```

Don't act on MAYBE as confirmed. Don't let DISCARD bias next wave.

### 14. Synthesis template (mental brief after each wave)

```
CONFIRMED: <fact + source evidence>
LIKELY:    <probable signal>
OPEN:      <question for next wave>
DISCARD:   <ignored + why>
KEEP:      <primary files/symbols>
RISKS: correctness / security / maintainability
NEXT WAVE: <specific bundled calls>
```

### 15. AFT fallback

Allowed when: `success:false`, `complete:false` + gap material, target unindexed/unsupported, non-code content, exact raw shell needed, tool not exposed.

Write one line: `AFT fallback: <reason>.` Then use narrowest raw tool.

### 16. Runtime hoisting

If a tool is named `read`, `write`, `edit`, `apply_patch`, `grep`, `glob`, `bash`, `ast_grep_search`, `ast_grep_replace`, or `lsp_diagnostics` — assume AFT-backed. Apply honesty contract.

### 17. Absolute minimum

1. Project next 2-4 rounds before any call.
2. Bundle independent read/search/exploration into one wave.
3. `aft_outline` → structure, `aft_zoom` → symbols, `grep` → exact text, `aft_search` → concepts, `aft_callgraph` → callers/impact, `lsp_diagnostics` → fast feedback.
4. Check `success` + `complete` before trusting AFT.
5. Classify results, synthesize, then another wave.
6. Risky edits: `aft_safety checkpoint` → edit sequentially → diagnostics + real tests.
7. Retrieve broadly, focus quickly, discard noise, act on evidence.
