---
description: "Show a list of commits, with files and messages for each commit that will be made"
---

Create a list of GitHub commits with the specified rules.

## Guidelines

- Always use **atomic commits**: one commit per independent logical change.
- **Never** include unrelated files in the same commit. Each commit should be focused on a single change or feature.
- **Never** use `git add .` or `git add -A` to stage all changes. Always review and stage files individually to ensure only relevant changes are included in each commit.
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
