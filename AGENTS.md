# Default Agent Instructions

- Everything that will be **committed**, like code, tests, and plans, **MUST** be written in English only.
- Always respond to the user in **Brazilian Portuguese (pt-BR)**, unless the user writes in another language.
- If a task step fails after two attempts, **stop and report** to the user instead of continuing or trying workarounds silently.
- Never commit or expose `.env` files, secrets, tokens, or credentials of any kind.
- You have useful tools available as MCP or command-line. Use them.
- Unless you are absolutely sure that you have correct and, crucially, up-to-date information in your knowledge, always get information from the web. You can use **exa**, **context7** or **gh_grep** for searching and getting information, and you can always use curl to fetch web pages.
- If you are working on something that presents web pages, you should use **Playwright** to open these pages, take snapshots, and inspect them.
- When working in a git repository, always switch to a new branch, unless explicitly instructed not to.
- If the git repo has a corresponding repo on GitHub, use the gh tool for things like looking at issues, opening pull requests, reading review comments, and looking at CI results.
- If the project has tests you can run locally, always run them and make sure everything works correctly.
- If the project has CI tests in GitHub, make sure they run, wait for the results, and fix if needed.
- If a plan step fails after two attempts, **stop and report** to the user instead of continuing or trying workarounds silently.

## Source Control (Git)

- When invoking `git commit`, always use `--author="Johnatas Henrique <johnatas.henrique@gmail.com>"` to commit.

## Commit Rules

- Always use **atomic commits**: one commit per independent logical change.
- **Never run `git commit` without explicit user permission.** If you think a commit should be made, ask first — do not act on your own.
- When the user asks you to commit, **always present a structured list first**, showing:
  - The files grouped per proposed commit
  - The proposed commit message for each group
- Wait for the user to review and explicitly confirm before executing any commit.

## Project Rules

- **Always read** the project's AGENTS.md file first — it contains project-specific rules and conventions.
- When in Plan mode, **always save** the implementation plan to a `.md` file in a docs/plans/ or plans/ directory, adding a descriptive name. A plan can **never** be lost, and must be saved as soon as it's created.

## Plan Format

- All plans must include an **Execution** table at the top:

  ```markdown
  ## Execution

  | Step             | Status | Timestamp |
  | ---------------- | ------ | --------- |
  | 1. [Description] | ⏳     | -         |
  ```

- Create the execution table when the plan is first created
- Update each step to ✅ with the completion legible timestamp when finished and archive the plans within a archive/date directory, inside the project plans folder, where date is the archiving date of the plan.
- **All plans must be written in English**

## Useful Command-Line Tools

### GitHub

- Use the `gh` command-line to interact with GitHub.

### JSON

- Use the `jq` command to read and extract information from JSON files.

### RipGrep

- The `rg` (ripgrep) command is available for fast searches in text files.

### Clipboard

- Use `xsel` to copy content into the clipboard. Example: `echo "hello" | xsel --clipboard --input`.
- Use `xsel` to get the contents of the clipboard. Example: `xsel --clipboard --output`.

### Web (HTTP/S)

- Prefer **context7** for library/framework docs, **exa** for general web searches, and **curl** only when you have a direct URL.

## MCP Tools

### playwright

- Operate a web browser: navigate, click around, take screenshots
- Use this whenever you want to look at a web page. For example, when working on a web app, you can run the local web server and interact with the web app.
- This is especially important if you're working on anything visual — you should always take a look using playwright so that you know how the results of your work look.

### markitdown

- Use this to convert various file formats to markdown.
- Very useful if you need to read files that are not supported natively by the model.

### exa

- Use this to run web searches. It is always better to search the web than to rely on your own knowledge, which may be outdated.
- You can also retrieve content in a format easy for ingestion. Use that if needed, but you can also just use curl if you have a URL.

### thinking

- If you are not a native reasoning model (i.e., you do not produce internal chains-of-thought automatically), you MUST use the thinking tool.

### context7

- Use the Context7 MCP tool to read the documentation for many libraries and tools.
- If you're asked to use a library, framework, or tool, it often makes sense to review its documentation first with Context7.

## JavaScript / TypeScript

- Use `npx` for running commands directly from npm packages.

## Documentation Sources

- If working with a new library or tool, consider looking for its documentation from its website, GitHub project, or the relevant llms.txt.
  - It is always better to have accurate, up-to-date documentation at your disposal, rather than relying on your pre-trained knowledge.
- You can search the following directories for llms.txt collections for many projects:
  - https://llmstxt.site/
  - https://directory.llmstxt.cloud/
- If you find a relevant llms.txt file, follow the links until you have access to the complete documentation.

## Quality Workflows

Before committing, run the quality chain to ensure code quality:

- `.workflows/finalize-01-hardening.md` — Fix code quality issues (spaghetti, constants, naming)
- `.workflows/finalize-02-consolidation.md` — Find and merge duplicate functions
- `.workflows/finalize-03-slop.md` — Remove AI-generated code patterns (unnecessary comments, over-engineering)
- `.workflows/finalize-04-commit.md` — Quality gate + commit (lint, typecheck, test, then commit)

To run the full chain:
```
Follow the quality chain: execute .workflows/finalize-01-hardening.md, then .workflows/finalize-02-consolidation.md, then .workflows/finalize-03-slop.md, and finally .workflows/finalize-04-commit.md
```

To run a specific workflow:
```
Follow .workflows/finalize-03-slop.md to clean the current diff
```

## Build/Lint/Test Commands

The quality workflows discover commands from this file. Update for your project as needed.

### Linting & Formatting
npm run lint        # or: ruff check . --fix
npm run format      # or: ruff format .

### Type Checking
npx tsc --noEmit    # or: mypy .

### Testing
npm test            # or: pytest

## Context Mode (context-mode)

You have context-mode MCP tools available. These rules protect your context window from flooding.

### Think in Code — MANDATORY

When you need to analyze, count, filter, compare, search, parse, transform, or process data: **write code** via `ctx_execute` and `console.log()` only the answer. Do NOT read raw data into context.

### REDIRECTED tools — use sandbox equivalents

- Shell (>20 lines) → use `ctx_execute` or `ctx_batch_execute`
- File reading (for analysis) → use `ctx_execute_file`
- grep (large results) → use `ctx_execute` with grep in sandbox

### Tool selection hierarchy

1. `ctx_batch_execute` — run multiple commands + search in ONE call
2. `ctx_search` — query indexed content
3. `ctx_execute` / `ctx_execute_file` — sandbox execution
4. `ctx_fetch_and_index` → `ctx_search` — web pages

### Context Mode Commands

| Command | Action |
|---------|--------|
| `ctx stats` | Display context savings and session statistics |
| `ctx doctor` | Run diagnostics |
| `ctx upgrade` | Upgrade context-mode |

## Memory Usage (simple-memory)

**One line, detailed** - Keep each memory on a single line to avoid git conflicts. Be detailed but concise. Include file references where applicable (e.g., "See: path/to/file.py").

- Use `memory_recall()` at the start of each session and before answering questions
- If you use `memory_recall()` and find nothing, ask the user if they would like to add global memories for the project
- If the user wants to add global memories, use the content of `~/.config/opencode/docs/agent-instructions/global-memories.md` as a base to create memories, add the memories with the exact text from the file, line by line (that is, each line of the file should be a separate global memory), and use `memory_remember()` to remember each line as a global memory.
- **NEVER** use `memory_remember()` automatically - only when the user explicitly asks
- If new information contradicts existing memory: ask the user before using `memory_forget()` + `memory_remember()`
- **End of session**: If significant patterns, decisions, or learnings are discovered, ask: "Do you want me to remember [specific thing]?"

### Memory Types

| Type      | Use For                     | Example                                                         |
| --------- | --------------------------- | --------------------------------------------------------------- |
| decision  | Architecture/design choices | "Using Drizzle ORM over Prisma for type safety. See: src/db/schema.ts" |
| learning  | Codebase discoveries        | "Auth tokens stored in httpOnly cookies, not localStorage. See: src/auth/session.ts" |
| preference | User/project preferences   | "User prefers functional components over class components"     |
| blocker   | Known issues                | "Websocket reconnection fails on Safari - tracking in issue #42" |
| context   | Feature/system info         | "Payment integration uses Stripe in test mode. API keys in .env.local" |
| pattern   | Code patterns              | "All API routes follow /api/v1/[resource]/[action] pattern. See: src/routes/" |

### Memory Scopes

| Scope       | Use For                              |
| ----------- | ------------------------------------ |
| project     | Project-wide decisions and patterns  |
| global      | User-specific preferences            |
| auth        | Authentication/authorization context |
| api         | API design decisions                 |
| database    | Database schema and query patterns   |
| testing     | Testing strategies and known issues  |
| deployment  | Deployment and infrastructure notes  |
