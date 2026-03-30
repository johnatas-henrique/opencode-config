---
name: commit-list
description: ALWAYS use this skill when committing code changes — never commit directly without it. Creates commits following Conventional Commits with proper conventional commit format and issue references. Trigger on any commit, git commit, save changes, or commit message task.
---

## Prerequisites

Before committing, always check the current branch:

```bash
git branch --show-current
```

**If you're on `main` or `master`, you MUST create a feature branch first** — unless the user explicitly asked to commit to main. Do not ask the user whether to create a branch; just proceed with branch creation. Put a name that makes sense for the change you're making, e.g., `feat/audit-logging` or `fix/config-resolution`.

After you complete the branch creation, verify the current branch has changed before proceeding:

```bash
git branch --show-current
```

If still on `main` or `master` (e.g., the user aborted branch creation), stop — do not commit.

Create a list of GitHub commits with the specified rules.

## Critical Rule

**EVEN IF YOU THINK A COMMIT SHOULD BE MADE, YOU MUST NOT COMMIT WITHOUT EXPLICIT USER PERMISSION.**

This skill is the ONLY acceptable workflow for committing. There are no exceptions.

## Guidelines

- Always use **atomic commits**: one commit per independent logical change.
- **Never run `git commit` without explicit user permission.** If you think a commit should be made, ask first — do not act on your own.
- **Never** make a commit who is different than the list that the user validated, this is **unnaceptable**.

## Instructions

1. Run `git diff` and `git status` to see if there are other files who aren't known by the agent.
2. Update the plans and archive them if completed
3. Always **present list first, in Markdown Tables format**, showing:
   - The files grouped per proposed commit
   - The proposed commit message for each group
4. Wait for the user to review and explicitly confirm before executing any commit.
5. If the user makes questions answer all questions **before commiting**.
6. You can only commit after you answered all questions and the user says **explicitly** to you that you can commit.
7. If a commit includes plan files, update the plans first. If they are complete, archive them before committing.
8. After you've made all the commits, make a second list in Markdown Tables format **showing what you've done** in the same style as the first one.
