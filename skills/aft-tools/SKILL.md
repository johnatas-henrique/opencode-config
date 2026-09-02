---
name: aft-tools
description: >
  Fast reminder for using the cortexkit/aft OpenCode plugin tools. Use when AFT
  is installed, when choosing between read/grep/bash and aft_* tools, when
  checking ~/.config/cortexkit/aft.jsonc, or when updating this skill after a new
  cortexkit/aft release.
---

*Written for AFT v0.42. If a newer release exists, validate tool names and config keys.*

## 0. Check local config first

Global config: `~/.config/cortexkit/aft.jsonc`
Project config: `<project>/.cortexkit/aft.jsonc`
*(Auto-migrated from legacy `~/.config/opencode/aft.jsonc` / `~/.pi/agent/aft.jsonc` in v0.40)*

Read the config to confirm available surface. If no file exists, defaults apply.

Key config effects:
- `tool_surface`: `minimal`, `recommended`, or `all` — controls which aft_* tools exist
- `disabled_tools`: tools removed after surface filtering
- `hoist_builtin_tools: true` → `read`/`write`/`edit`/`grep`/`bash` may be AFT-backed
- `search_index: true` → indexed `grep`/`glob`
- `semantic_search: true` → enables `aft_search` hybrid/semantic
- `inspect.enabled: true` → enables `aft_inspect`
- `bash.rewrite/compress/background`: AFT-managed shell calls
- `semantic.max_files` (default 20000): max files for semantic search indexing in large repos
- `bash.foreground_wait_window_ms` (default 15000): auto-promote to background after ms
- `backup.enabled / .max_depth / .max_file_size` (v0.42): safety backup settings
- `bridge.request_timeout_ms` (default 30000): raise on slow filesystems
- `bridge.hang_threshold` (default 2): raise when many sessions share one bridge
- `lsp.max_callgraph_files` (default 5000): cap for dead-code analysis on large repos
- `callgraph_chunk_size` (default 100): batch size for cold-build call graphs
- `.aftignore`: skip indexed paths that can't go in `.gitignore`

Defaults (no config file): `tool_surface: all`, `hoist_builtin_tools: true`,
`search_index: true`, `semantic_search: true`, `inspect.enabled: true`,
`format_on_edit: false` (was `true` pre-v0.40), `validate_on_edit: syntax`,
bash rewrite/compress/background enabled.

### 1. Bundle Read-Only Calls

Independent reads/searches/outlines/zooms/callgraphs/greps → emit in **one message**. Sequence only when a later call depends on an earlier result.

### 2. AFT-first, fallback-safe

| Prefer | When to fallback |
| ------ | ---------------- |
| `aft_*` for nav, read, edit, search, refactor, shell, diagnostics | AFT `success: false` |
| | AFT `complete: false` + gap is material |
| | Target unindexed or non-code (config, binary, prose) |
| | Need exact raw shell behavior |

**Honesty contract**: inspect `success` + `complete` before trusting. `complete:false` = partial — resolve `skipped_files`, `unchecked_files`, `walk_truncated` before acting.

### 3. Exploration — Structure before text

`aft_outline` → `aft_zoom` / focused `read` → full `read` only if needed.
- Exact strings → `grep`
- Concepts → `aft_search`
- Structure → `ast_grep_search` (YAML/`.yaml`/`.yml` surfaces as rich symbols in AFT tools)

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

| Dimension | Tools | Answers |
| --------- | ----- | ------- |
| Fan-out | `aft_outline`, `glob`, `grep` broad, `aft_search`, `aft_inspect` | "What's near this?" |
| Drill-in | `aft_zoom`, `read` range, `grep` exact, `ast_grep_search`, `aft_callgraph` | "What exactly happens?" |

### 7. Tool routing

| Intent | Use first | Fallback |
| ------ | --------- | -------- |
| List files | `aft_outline <dir> files:true` / `glob` | `read dir` / `find` |
| File structure | `aft_outline <file>` | `grep defs` |
| Inspect symbol | `aft_zoom <file> <symbol>` | `read` range |
| Find by concept | `aft_search <concept>` | `grep` synonyms |
| Find exact text | `grep <literal/regex>` | `rg` via bash |
| AST search/replace | `ast_grep_search` / `ast_grep_replace dryRun` | manual edit |
| Callers/callees | `aft_callgraph callers/call_tree` | `grep` symbol refs |
| Impact | `aft_callgraph impact` | grep + tests |
| Merge conflicts | `aft_conflicts` | `git status` + grep |
| Imports | `aft_import add/remove/organize` | manual edit |
| Replace symbol body | `edit symbol:...` | manual patch |
| Add member/decorator | `edit symbol:` or `edit oldString/newString` | manual patch |
| Move/extract/inline | `aft_refactor` | manual refactor |
| Move/rename file | `aft_move` | `mv` + fix imports |
| Delete files | `aft_delete` | `rm` only with safety review |
| Undo/checkpoint | `aft_safety` | `git diff/restore` |
| Diagnostics | `lsp_diagnostics` | project typecheck |
| Health snapshot | `aft_inspect` | manual review |
| Shell/test/build | `bash` | native shell |

### 8. Tool surface list

**Hoisted built-ins** (when `hoist_builtin_tools: true`):
- `read`: file read, directory listing, image/PDF metadata
- `write`: write with dirs, backup, format, optional diagnostics
- `edit`: fuzzy replace, symbol replace, batch/transaction edits
- `apply_patch`: multi-file patch format
- `bash`: rewritten/compressed/background/PTY shell
- `grep` / `glob`: indexed search when `search_index` enabled
- `ast_grep_search` / `ast_grep_replace`: structural search/replace
- `lsp_diagnostics`: focused LSP diagnostics when registered

**Recommended `aft_*` tools** (surface: recommended or all):
- `aft_outline`, `aft_zoom`, `aft_search`, `aft_inspect`, `aft_import`, `aft_conflicts`, `aft_safety`

**`tool_surface: all` extras** (only if registered):
- `aft_callgraph`: callers, call_tree, impact, trace_to_symbol, trace_data
- `aft_refactor`: move, extract, inline
- `aft_delete`, `aft_move`

*Note: `aft_transform` was removed in v0.37.0 — use `edit symbol:` or find/replace instead.*

### 9. AFT health bar (status line)

Tool results may end with a health bar like `[AFT E<errors> W<warnings> | D<dead> U<unused> C<clones> | T<todos>]`.
- `E`/`W` = live LSP diagnostics for files touched this session
- `~` before `D` means Tier-2 counts predate latest edit — run `aft_inspect` for current numbers
- When `E>0`, investigate before moving on

### 10. Tool output changes (v0.34→v0.42)

- **`aft_search`**: top result renders full symbol (capped 250 lines); test files hidden by default (`includeTests: true` to show)
- **`aft_zoom`**: call-graph annotations are opt-in (`callgraph: true`). Default is symbol source only. Large containers (>~150 lines) return a member menu. Ambiguous names return candidate signatures
- **`aft_inspect`**: compact text summary (not raw JSON). Diagnostics detail always included (message + file:line, capped by topK)
- **`aft_callgraph`**: standard-library noise collapsed into one summary line per caller. Returns readable text (not raw JSON)
- **`edit`**: compact one-line output (`Edited (+3/-1).`). `replaceAll` refuses overlapping matches. Surfaces formatter reflows
- **`apply_patch`**: partial application reports "Partially applied (N of M)"
- **`bash`** (when background disabled): `bash_status`/`bash_kill`/`bash_watch` not registered; `background`/`pty` params removed; piped commands run verbatim (no rewrite)

### 11. Language support (since v0.34)

New languages added since v0.34:
- **Outline/zoom/AST**: YAML/Kubernetes symbols, SCSS, Pascal (`.pas`/`.pp`/`.dpr`), R (`.R`/`.r`), Quarto (`.qmd`), R-Markdown (`.Rmd`)
- **`aft_import`** extended to: Solidity, Java, C#, PHP, Kotlin, Scala, Swift, Ruby, Lua, Perl, C/C++, Vue
- **Semantic search**: Java, Kotlin, Ruby, Swift, Scala, Lua, Perl, R (v0.41)

### 12. .aftignore

`.aftignore` files are honored (hierarchical, layered on `.gitignore`). Excludes paths from trigram index, semantic index, call graph, `aft_inspect`, and ripgrep fallback. Editing `.aftignore` refreshes indexes. Naming a single file in `grep` searches it even if ignored.

### 13. Safe vs Unsafe bundling

**Safe (bundle freely):** all read/search/exploration — outline, zoom, search, inspect, conflicts, callgraph (read-only), grep, glob, read, ast_grep_search, diagnostics, git status/diff/log, web search.

**Never in parallel (sequence one-by-one):** write, edit, apply_patch, ast_grep_replace (applying), aft_import, aft_refactor, aft_move, aft_delete, aft_safety restore/undo, dep installs, commits, pushes, destructive shell, parallel edits to related files.

Investigation = parallel. Patching = sequential.

### 14. Editing workflow

**Before:**
1. Confirm target with `aft_zoom`/`read`/`grep`/`ast_grep_search`
2. Multi-file/load-bearing change → `aft_callgraph impact`
3. Broad/risky → `aft_safety checkpoint`
4. Locate tests via `glob`/`grep`

**During (prefer in order):**
- `edit symbol:` for full symbol replacement (covers structural additions; `aft_transform` removed in v0.37)
- `aft_import` for imports
- `aft_refactor` for move/extract/inline
- `apply_patch` for multi-file text AFT can't model
- `ast_grep_replace dryRun` first

**After:**
1. `lsp_diagnostics` on touched files
2. Smallest meaningful test/typecheck/lint via `bash`
3. `git diff` — verify intended-only changes
4. Don't claim full verification if AFT reports skipped/unchecked

### 15. Load-bearing files

Defines: shared infra, public API, auth/security, routing, persistence, build harness, config loading, widely imported types, many callers.

**Before editing:**
1. `aft_outline`
2. `aft_zoom` affected symbols / read ranges
3. `aft_callgraph impact`
4. `grep` imports/call sites
5. Read tests
6. `aft_safety checkpoint` if broad/risky

### 16. Wave shapes by task

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

### 17. Query construction

- Fan-out: broad but bounded to source area
- Drill-in: exact symbols, error strings, config keys, line ranges
- Bundle variants/synonyms in one grep
- Pair conceptual `aft_search` with exact `grep` for important behavior
- Exclude: deps, generated output, build artifacts, coverage, minified bundles, snapshots, vendor
- Search tests separately and explicitly when behavior is unclear
- Explicit single-file `grep` inspects ignored files (ripgrep behavior — intentional, for targeted checks)
- Use `ast_grep_search` for syntactic structures grep can't model

### 18. Classification

After every wave: classify each result

```
KEEP    — direct evidence
MAYBE   — plausible but unconfirmed
DISCARD — empty, noise, generated, vendored, stale, irrelevant
```

Don't act on MAYBE as confirmed. Don't let DISCARD bias next wave.

### 19. Synthesis template (mental brief after each wave)

```
CONFIRMED: <fact + source evidence>
LIKELY:    <probable signal>
OPEN:      <question for next wave>
DISCARD:   <ignored + why>
KEEP:      <primary files/symbols>
RISKS: correctness / security / maintainability
NEXT WAVE: <specific bundled calls>
```

### 20. AFT fallback

Allowed when: `success:false`, `complete:false` + gap material, target unindexed/unsupported, non-code content, exact raw shell needed, tool not exposed.

Write one line: `AFT fallback: <reason>.` Then use narrowest raw tool.

### 21. Runtime hoisting

If a tool is named `read`, `write`, `edit`, `apply_patch`, `grep`, `glob`, `bash`, `ast_grep_search`, `ast_grep_replace`, or `lsp_diagnostics` — assume AFT-backed. Apply honesty contract.

### 22. Absolute minimum

1. Project next 2-4 rounds before any call.
2. Bundle independent read/search/exploration into one wave.
3. `aft_outline` → structure, `aft_zoom` → symbols, `grep` → exact text, `aft_search` → concepts, `aft_callgraph` → callers/impact, `lsp_diagnostics` → fast feedback.
4. Check `success` + `complete` before trusting AFT.
5. Classify results, synthesize, then another wave.
6. Risky edits: `aft_safety checkpoint` → edit sequentially → diagnostics + real tests.
7. Retrieve broadly, focus quickly, discard noise, act on evidence.
