# Error Recovery

Load this file when any error, unexpected git state, or user complaint occurs during the commit flow. Each entry has the exact recovery action — do not improvise.

| Situation | Detect | Action |
|-----------|--------|--------|
| **Tree already clean** | `git status --short` is empty | Say so. Do nothing. |
| **Not a git repo** | `git rev-parse HEAD` fails | Report and abort. |
| **Merge conflict** | `git status` shows `UU` or both modified | Read conflicted files, fix markers, `git add <resolved>`, `git commit`. Do NOT run split flow. |
| **Detached HEAD** | `git branch --show-current` empty | `git checkout -b fix/<description>` before any staging. Ask user for name if unsure. |
| **Interactive rebase in progress** | `git status` shows "interactive rebase in progress" | Ask: abort (`git rebase --abort`) or continue (`git rebase --continue`)? Do NOT commit. |
| **Cherry-pick in progress** | `git status` shows "cherry-pick in progress" | Resolve conflicts if any, then `git cherry-pick --continue` or `--abort`. |
| **Revert in progress** | `git status` shows "revert in progress" | Resolve conflicts if any, then `git revert --continue` or `--abort`. |
| **Bisect in progress** | `git status` shows "bisect in progress" | Do NOT commit. Run `git bisect reset` first. Then normal flow. |
| **Pre-commit hook fails** | `git commit` exits non-zero | Read error → fix the specific issue → `git add <fixed-files>` → retry same message. Never `--no-verify` without explicit user permission. |
| **Wrong file staged** | You notice extra or wrong files in `git diff --cached --stat` | `git reset HEAD <file>` → restage only the correct files. |
| **Wrong commit made** | Message wrong or files don't match plan | `git reset --soft HEAD~1` → restage → recommit. |
| **Push rejected (non-fast-forward)** | `git push` fails with rejected error | `git pull --rebase` → resolve conflicts → `git push` again. |
| **Push to protected branch** | `git push` fails due to branch protection | Cannot push directly. Create a PR instead: `gh pr create`. Do not force-push. |
| **Push to main/master** | Branch is main or master | Create branch first (Phase 3). Do not push main. |
| **Large file (>100 MB)** | `git push` fails with file size error | Use `git lfs track <pattern>` or split the file. If LFS is not set up, tell the user. |
| **Commit message too long** | Editor opens and agent can't drive it | Kill editor, retry with shorter `-m "..."`. If editor persists, use `git commit -m "msg" -m "body"` format. |
| **User says "replan"** | User rejects the plan | Discard current plan. Rerun Phase 1. |
| **gh not installed** | `gh pr create` fails | Skip PR creation. Report to user. |
| **`git add -p` unavailable** | TTY not available for interactive staging | Use fallback: `git diff` → assess → stage clean hunks explicitly with `git add <path>`. |
| **Binary file found** | During staging, file is binary | Skip `git add -p`. Use `git add <path>` directly. |
| **Stash pop conflicts** | `git stash pop` has merge conflicts | Resolve conflicts manually (same as merge conflict), `git add <resolved>`, then `git stash drop` if clean. |
| **Wrong branch created** | Branch name has typo or wrong prefix | `git branch -m <correct-name>` to rename. |
