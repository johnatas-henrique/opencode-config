---
description: Run mechanical quality checks (lint, typecheck, test), then stage and commit
chain: finalize
order: 4
next: null
---

## 1. Discover available commands

Read `AGENTS.md` (or equivalent project instructions file) for the project's lint, format, type-check, and test commands.

Only run commands that are actually documented. Do NOT assume any tool or command exists. If a project has no type checker, skip that step.

## 2. Lint and format

Run the project's lint and format commands. Fix any errors that auto-fix doesn't resolve.

## 3. Type check

If the project has a type checker configured, run it. Fix any type errors.

## 4. Run the full test suite

Run the project's test command. Fix any failures.

## 5. Re-check if changes were made

If steps 2-4 required code fixes:
- Re-run lint and format
- Re-run tests
- Maximum 3 cycles. If still failing after 3 cycles, report remaining failures to the user and stop — do not attempt further fixes.

## 6. Review what's ready to commit

- Run `git status` to see staged, unstaged, and untracked files
- Run `git diff HEAD` to review the content of all changes
- Run `git log -5 --oneline` to understand the existing commit message style

## 7. Stage files

- Stage files individually with `git add <file>` — only files that are part of the intentional change
- Do NOT use `git add -A` or `git add .`
- Do NOT stage files that may contain secrets:
  `.env*`, `credentials.*`, `*.pem`, `*.key`, `*.secret`, `*.pfx`, `*_rsa`
- Do NOT stage generated or runtime output:
  `dist/`, `build/`, `out/`, `coverage/`, `node_modules/`, `__pycache__/`,
  `.venv/`, `*.pyc`, `*.class`, `*.egg-info/`, `htmlcov/`
- If untracked files exist that aren't part of the change, leave them unstaged and mention them to the user

## 8. Draft the commit message

- Use imperative mood ("add feature" not "added feature")
- Match the style from `git log` — if the repo uses conventional commits (`feat:`, `fix:`, `chore:`), follow that; if plain descriptions, follow that
- Focus on WHY the change was made, not WHAT files were touched
- 1-2 sentences unless the change warrants a body paragraph
- If the changes span multiple unrelated concerns, suggest splitting into multiple commits

## 9. Commit

- Create the commit with the drafted message
- Run `git status` after to verify success

## 10. Push (only if requested)

- Do NOT push unless the user explicitly asks
- If pushing, check for divergence first: `git fetch && git log HEAD..@{upstream}` — if the remote has commits the local branch doesn't, alert the user before pushing
- If pushing: `git push` (or `git push -u origin <branch>` if no upstream is set)
- Confirm success
