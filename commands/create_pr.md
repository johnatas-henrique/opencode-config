---
description: "Creates a PR with the specified changes. Use this command to submit your code changes for review and integration into the main codebase. Provide a clear title and description for the PR to facilitate the review process."
agent: build
model: "opencode/big-pickle"
subtask: true
---

Create a GitHub Pull Request (PR) with the specified commands and rules.

**Instructions**

1. Inspect with a git diff everything that has changed on this branch in comparison with the main branch.

2. Create a new pull request with the following details:

- **head** the current branch name. `git branch --show-current`
- **title** short and appropriate title based on the changes. Use the format: "feat: add new feature" or "fix: resolve bug in module".
- **body** changes in short bullet points listed. Nothing else

3. Follow extra instructions passed by the user EVEN if they override previous instructions. If the user has not provided any extra instructions, just follow the above steps.

**extra-user-instructions**: $ARGUMENTS

**CLI command syntax**

```
gh pr create \
  --head <FILL_IN_ACCORDINGLY> \
  --title <FILL_IN_ACCORDINGLY> \
  --body FILL_IN_ACCORDINGLY
```
  