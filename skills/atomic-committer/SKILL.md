---
name: atomic-committer
description: >
  CRITICAL: load this skill for EVERY git commit request. It prevents the
  agent from creating a single mega-commit by splitting changes into atomic
  units using a ceiling formula (ceil(files/4)). Handles branch management,
  selective staging (git add -p), binary file detection, and optional PR
  creation. WITHOUT THIS, default commits bundle unrelated changes and fail
  review. Use when the user asks to commit, save work, make "commits
  atômicos", split changes, or any commit task — NOT for rebase, history
  search, or blame operations.
---

# Atomic Committer

## Scenario Detection — MANDATORY First Step

Before ANY planning, run these to determine the git state:

```
git status --short --untracked-files=all
git diff --stat                    # unstaged changes
git diff --cached --stat           # already staged
git branch --show-current
git rev-parse HEAD                 # confirm git repo; if fails → ABORT
```

| Scenario | Action |
|----------|--------|
| **Tree already clean** (no staged, no unstaged) | Say so. Do not commit. |
| **Merge conflict** (`UU` or both modified) | **STOP.** Resolve conflicts: read each conflicted file, fix markers, `git add <resolved>`, `git commit`. Do NOT run split flow. |
| **Interactive rebase in progress** (`git status` shows "interactive rebase in progress") | Ask user: abort (`git rebase --abort`) or continue (`git rebase --continue`)? Do NOT commit during rebase. |
| **Cherry-pick in progress** (`git status` shows "cherry-pick in progress") | Resolve conflicts if any, then `git cherry-pick --continue` or `--abort`. Do NOT run normal split flow. |
| **Revert in progress** (`git status` shows "revert in progress") | Resolve conflicts if any, then `git revert --continue` or `--abort`. Do NOT run normal split flow. |
| **Bisect in progress** (`git status` shows "bisect in progress") | Do NOT commit. Run `git bisect reset` first. Then normal flow. |
| **Detached HEAD** (branch empty) | Create branch before committing: `git checkout -b fix/<description>`. Ask user for name if unsure. |
| **Stash exists** (`git stash list` shows entries) | Inform user. Ask: pop stash first (`git stash pop`) or commit current changes separately? |
| **User specified exact paths** ("commit only auth/") | Skip grouping. Use exactly those paths. Still apply ceiling formula. |
| **User says "amend"** or "fixup" | Skip full planning. `git commit --amend` or `git commit --fixup=<target>`. |
| **Normal — mixed worktree** | Full flow (Phases 1-6). |
| **Only untracked files** (no modified tracked) | `git add -p` not possible for new files. Use `git add <path>`. |

---

## The Atomic Mindset — Thinking Frameworks

### Before planning, ask yourself:
1. **One-sentence test** — can you describe this commit without "and"?
2. **Revert test** — would reverting it undo exactly one logical change?
3. **Mechanical vs functional** — renames/formatting separate from behavior. Always.
4. **Scope test** — crossing directories? Almost always a grouping error.

### Before staging, verify:
- Does every file here belong to THIS planned commit? If not → **unstage and replan**.
- Binary files in this group? Skip `git add -p` (doesn't work on binaries), use `git add <path>`.

### After each commit, confirm:
- `git log -1 --oneline` matches the planned message?
- `git status --short` shows the expected remaining files?
- Pre-commit hook modified or rejected the commit? Read its output and act.

### Spiral workflow
If during staging or committing you discover the plan no longer fits, **STOP. Restart Phase 1 with what you now know.** This is expected, not a failure.

---

## Rules

### MIN_COMMITS formula (unified — always use this)

```
MIN_COMMITS = ceil(changed_files / 4)
Then enforce minimums:
  3+ files  → at least 2 commits
  5+ files  → at least 3 commits
  10+ files → at least 5 commits
```

Examples: 3 files → 2 min. 8 files → 3 min. 13 files → 4 min. 20 files → 5 min.

If `MIN_COMMITS >= 8`, warn: "This plan requires 8+ commits — consider squashing related groups or confirm with the user."

### Self-check before committing

```
"I am making N commits from M files."
IF N < MIN_COMMITS:
  → WRONG. Go back and split.
  → Write down WHY each file must be together.
  → If you can't justify, SPLIT.
```

### Per-commit file limit

**Max 4 files per commit** (or justified). **Justified** means the files are tightly coupled — type definition + its sole consumer, migration + its rollback, feature flag + all code using it. "Related to the same feature" is NOT justification.

### Split by directory first

**Different directories = Different commits (almost always).**

Within the same directory, split by logical concern:
- **Feature** — source, new modules, behavior changes
- **Fix** — patches, error handling
- **Test** — test files, fixtures, test helpers
- **Docs** — README, inline docs, examples
- **Config** — package.json, lockfiles, CI, tooling
- **Refactor** — renames, moves, extractions (no behavior change)
- **Format** — whitespace, lint fixes (no logic change)

**Heuristics:**
- Keep lockfile with its manifest (package.json + lockfile).
- Keep tests with the source they verify.
- **Always separate** mechanical changes from functional ones.
- Deletions are their own group when they remove a feature or clean obsolete files across directories.
- Renames stay in their own commit or with the exact changes to the renamed file — never with unrelated files.

### Dependency ordering

**MANDATORY — read ENTIRE `references/orderings.md`** (~30 lines) before ordering commits. **Do NOT load** during normal staging or commit flow — only when ordering.

Foundations before dependents. The file contains backend, frontend, and monorepo level tables. Read only the section that matches your project.

---

## NEVER Do This

```
✗ git add . / -A / --all → stages untracked files, build artifacts,
  caches, and secrets you did not intend. Always use explicit paths.

✗ git commit --no-verify without user permission → hides pre-commit
  hook errors (lint, format, tests). Only use if user explicitly says
  "skip hooks" or "force".

✗ Co-Authored-By: <AI name> → pollutes git blame with non-human
  authorship. Never add Claude, Copilot, or any AI tool name.

✗ Rebase or amend during commit flow → rewrites history mid-task,
  makes recovery harder. Finish all commits first, then consider
  cleanup rebase.

✗ git commit from 3+ files as a single commit → you are bundling
  unrelated changes. You cannot describe this commit without "and".
  Split by module.

✗ git add submodule path without verifying its internal diff →
  pins the submodule to HEAD without checking if internal changes
  are intentional. Run `git diff --submodule` first.

✗ Committing files with secrets, API keys, .env, credentials, or
  build artifacts → once pushed, secrets in git history are nearly
  impossible to fully remove. Always review `git diff --cached --stat`
  and verify against .gitignore before each commit.
```

---

## Convention Detection

```
.github/agent-commit-message-instructions.md   # follow if exists
.github/commit-convention.md                    # follow if exists
git log -5 --oneline                            # infer from history
```

Repo instructions always win. Default to conventional commits if unclear. Scope is optional — use it when the commit touches a specific module: `feat(auth): add rate limiting` not `feat: add rate limiting to auth module`.

---

## Phase 1: Commit Planning — BLOCKING

**MANDATORY OUTPUT.** You MUST show the Commit Plan before any staging or execution.

### 1A. Count + Formula

```
changed_files = (git status --short | wc -l)   # or count user-specified paths
MIN_COMMITS = ceil(changed_files / 4)
Apply graduated minimums: 3+→2, 5+→3, 10+→5
```

### 1B. Group files

Split by directory first, then by logical concern. Apply the per-commit file limit.

### 1C. Justify

For each commit with 3+ files, write ONE sentence explaining why they belong together.

| Valid | Invalid |
|-------|---------|
| "type definition + the only file that uses it" | "all related to feature X" (too vague) |
| "implementation + its test" | "part of the same PR" (not technical) |
| "migration + its rollback" | "same developer worked on them" |

### 1D. Order

Order commits by dependency — read `references/orderings.md` for the appropriate table.

### 1E. Commit Plan Block (MANDATORY OUTPUT)

```
COMMIT PLAN
===========
Files changed: N
Minimum commits required: M
Planned commits: K
Status: K >= M (PASS) | K < M (FAIL — must split more)

COMMIT 1: type(scope): subject
  - path/to/file1.ext
  - path/to/file2.ext
  Justification: why these belong together

COMMIT 2: type(scope): subject
  - path/to/file3.ext
  Justification: independent change

Execution order: Commit 1 → Commit 2 → ...
Proceed? (yes/no/replan)
```

**STOP. DO NOT STAGE. DO NOT COMMIT.** Wait for explicit "yes". If "replan", restart Phase 1.

### State tracking (for 3+ commits)

After each commit, output progress:

```
COMMIT PROGRESS: [2/5]
✓ Commit 1: feat(auth): add rate limiting — DONE
→ Commit 2: fix(auth): handle edge case — IN PROGRESS
  Commit 3: test(auth): add rate limit tests — PENDING
Remaining files: src/auth/edge.ts, tests/auth/rate.test.ts, ...
```

If a spiral restart occurs, recalculate from `git status --short` — do not assume the original file list is still valid.

---

## Phase 2: Validation Checklist — BLOCKING

```
[] MIN_COMMITS >= ceil(N/4) with graduated minimums enforced?
[] Each commit with 3+ files has a justification?
[] Different directories → different commits?
[] Tests paired with their implementation?
[] Foundations before dependents?
[] Max 4 files per commit (or justified)?
[] User-specified paths respected (if any)?
[] No commit groups 3+ files from different directories?
```

**HARD STOP:** 1 commit from 3+ files → WRONG. SPLIT.

---

## Phase 3: Branch Decision

`git branch --show-current` (already known from scenario detection).

- **main/master** → propose `type/kebab-description`, run `git branch --list <proposed>` to check exist. Exists? Ask to use it or pick another. Not exists? Ask before creating.
- **Feature branch** → ask "Continue on this branch or create new?".
- **Detached HEAD** → `git checkout -b fix/<description>` before staging.
- Never switch branches with uncommitted changes without stashing first.

---

## Phase 4: Staging

Stage one group at a time, in dependency order.

| Situation | Command |
|-----------|---------|
| Clean single-purpose files | `git add -- path1 path2` |
| Mixed hunks (formatting + logic) | `git add -p -- path/to/file` |
| Binary files (images, PDFs, compiled) | `git add <path>` (NOT `-p`) |
| Renamed files | `git add <new-path>` (git detects rename automatically) |
| Submodule moved | `git diff --submodule <path>` to inspect pointer change, then `git add <path>` if intentional. Stage submodule's own files first. |

### TTY Fallback

If `git add -p` requires a TTY and the agent cannot drive it:

```bash
git diff -- path/to/file              # show the diff
git diff --cached -- path/to/file     # show what's staged
```

Then decide: if the file can stay in one commit despite mixed hunks, stage whole and note the constraint in the commit message. If not, split via explicit `git add <path>` for clean hunks only.

### Pre-commit Verification

```bash
git diff --cached --stat     # verify only intended files
git diff --cached --check    # verify no whitespace errors
```

Check: no secrets, .env, caches, build artifacts, or unrelated changes.

---

## Phase 5: Commit

Format: `<type>(<scope>): <subject>`. Body explains **why**, not what. Subject max 72 chars, imperative, capitalized, no period.

After each commit:

```bash
git status --short                    # check remaining files
git log -1 --oneline --stat          # verify commit matches plan
```

### Pre-commit Hook Failure

1. Read the hook error output.
2. Fix the specific issue (lint, format, test).
3. `git add <fixed-files>` to stage fixes.
4. Retry `git commit` with the same message.
5. If it repeatedly fails for the same reason, ask user for guidance. Do NOT use `--no-verify` without explicit permission.

### Spiral Checkpoint

If during staging or committing the plan no longer fits, **STOP. Restart Phase 1 with what you now know.**

Repeat until tree is clean. Report intentionally uncommitted files.

### User Override

If the user explicitly says "one commit is enough" or overrides the minimum commit count:
1. **Confirm**: "You understand this bundles N files into one commit?"
2. **Document**: add `User-Override: single-commit (<reason>)` to the commit message body.
3. **Proceed** with `git add` and `git commit`. Do not fight the user — the repo owner decides, not the agent.

---

## Phase 6: Push & PR

Tree clean + non-main branch? **"Push? (yes/no)"** → `git push -u origin <branch>`.
After push → **"PR? (yes/no)"** → `gh pr create --title "<type>: <subject>" --body "## Summary\n<bullet points>" --base <default-branch>` (skip if `gh` missing).

---

## Error Recovery

**MANDATORY — read ENTIRE `references/error-recovery.md`** (~30 lines) when an error or unexpected git state occurs. The file covers 22 specific situations with exact recovery commands. **Do NOT load** during normal flow — only when something goes wrong.
