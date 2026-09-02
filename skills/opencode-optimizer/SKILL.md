---
name: opencode-optimizer
description: Optimize OpenCode project settings based on project-visible files, project config, and OpenCode CLI-resolved state. Detect the MCP/skill/provider/permission state loaded for the current project and provide evidence-based project config masking and optimization suggestions. Never read or modify the global main config file `~/.config/opencode/opencode.jsonc`; rescan every run, do not cache, and do not write automatically.
metadata:
  short-description: OpenCode project optimizer
---

# OpenCode Project Optimizer

## Goal

On every run, scan only **the current project's visible files and project OpenCode config**, supplemented by safe read-only `opencode` CLI resolution results, and produce an **interactive optimization report**. This skill is a **static / visible project config optimizer**: it only uses project-visible data and CLI-resolved state for the current project to produce project-level patch suggestions. It does not read the global main config file `~/.config/opencode/opencode.jsonc`, and it does not analyze runtime session history or tool-output flow. The report covers these core checks:

1. **Actual MCP loading check** — Use `opencode mcp list` to check MCP servers that are actually loaded / disabled / connected / in error for the current project.
2. **Relevance scoring and masking suggestions** — Grade CLI-visible MCPs and project-visible skills from A to D, then suggest project config `enabled: false` masks for this project.
3. **Low-risk path permission suggestions** — Add common low-risk temporary paths, such as `/tmp/`, to `permission.external_directory`.
4. **Provider / model optimization** — Suggest disabling unnecessary providers and setting appropriate models.
5. **Feature toggle suggestions** — Suggest enabling or disabling formatter / LSP / snapshot and related features based on project type.
6. **Resource usage optimization** — Suggest `watcher.ignore` entries for large directories and compaction settings.
7. **Command safety check** — Check whether dangerous commands such as `rm -rf` are denied and whether `.env` reads are protected.
8. **Agent settings audit** — Check required fields and permission consistency for custom agents.
9. **AGENTS.md health check** — Detect context-consuming but low-value content such as changelogs, embedded TODOs, common-knowledge commands, long tutorials, and machine-specific absolute paths.
10. **Custom command suggestions** — Suggest missing shortcuts such as `/branch`, `/pr`, `/test`, and `/release` based on project tools and workflows, while avoiding duplicate suggestions for existing project commands.
11. **Visible instructions load check** — Only check the number and rough size of statically visible files referenced by `instructions`.

By default, this skill **only produces a patch summary**. It does not automatically write project config and does not output a full `opencode.jsonc` unless explicitly requested. After giving suggestions, ask the user whether they want to generate or apply a full project config. Only after explicit user approval may you generate the project `opencode.jsonc`.

## Core Principles

- **Rescan every time**: Ignore previous results. Start from scratch on every run.
- **Global main config is strictly off-limits**: Do not read, search, grep, cat, write, or modify `~/.config/opencode/opencode.jsonc`. This file often contains MCP commands, API keys, provider settings, and local private paths, so treat it as high risk.
- **Only project config may be changed**: First provide a patch summary. If the user confirms, only generate or apply `opencode.json` / `opencode.jsonc` under the current project. Never modify any global setting.
- **Patch-first output**: Unless the user explicitly asks for it, do not output a full `opencode.jsonc`. This prevents the report itself from wasting context.
- **AGENTS.md is high-signal but must be denoised**: AGENTS.md / CLAUDE.md is important evidence, but changelog, TODO, example, and deprecated sections must not increase tool relevance.
- **Prioritize flow**: Never suggest setting core tools such as `edit`, `bash`, or `write` to `ask`, because that causes frequent interruptions.
- **Evidence-based**: Every mask, keep, and permission suggestion must include traceable evidence and confidence.
- **CLI validation first**: If the `opencode` CLI is available, use safe read-only CLI commands first to verify how the current project is actually resolved. `opencode mcp list` is the primary source for MCP analysis and replaces reading MCP config from the global main config file.
- **Config health first**: If basic health checks such as config parse, schema, duplicate keys, or secret placement fail, report those problems first and do not produce potentially wrong patches.

## Critical Safety Boundary: Global Config Is Off-limits

Always treat `~/.config/opencode/opencode.jsonc` as high risk because it commonly contains provider credentials, MCP API keys, tokens, secrets, local private paths, and command arguments. Other global OpenCode files are not covered by this exact ban, but sensitive content should still not be printed.

This skill must never:

- Read `~/.config/opencode/opencode.jsonc`.
- Grep, cat, find, or otherwise search the contents of `~/.config/opencode/opencode.jsonc`.
- Modify, format, or delete `~/.config/opencode/opencode.jsonc`.
- Extract MCP command, provider, permission, agent, command, or skill settings from `~/.config/opencode/opencode.jsonc`.
- Output contents from `~/.config/opencode/opencode.jsonc` in the report or patch.

This skill may only modify or generate project config under the current project. To disable MCPs shown by CLI, always generate a project-level `enabled: false` mask. Do not touch the global main config file.

## Scope Boundary

This skill only handles **visible project configuration** and **statically observable data**:

- Project OpenCode config: `opencode.json` / `opencode.jsonc` in the current project root.
- Project-local skills and `SKILL.md` frontmatter, if present.
- MCP server status only from `opencode mcp list`; do not read `~/.config/opencode/opencode.jsonc`.
- AGENTS.md / CLAUDE.md / files referenced by `instructions`.
- Project structure and common tool configuration files.
- Custom commands.
- watcher / permission / provider / model / MCP / skill enabled state.
- MCP server state resolved for the current project by `opencode mcp list`: enabled / disabled / connected / error.
- Currently available agents from `opencode agent list`.
- Read-only provider / model validation from `opencode auth list` and `opencode models`.
- Read-only OAuth MCP auth summary from `opencode mcp auth list`.
- `opencode --version` and relevant environment variables as supporting signals for version / config-source behavior.

This skill may run OpenCode CLI commands to read **resolved configuration state for the current project**, but it does not analyze runtime context flow, session history, true usage frequency, or tool output pruning.

If a problem belongs to runtime context management, only mark it as: “Requires a dedicated context-management skill.” Do not expand on runtime pruning, session compression, or memory retrieval in this report.

## Output Concision Rules

Only report items that have findings, need changes, or need confirmation. If a section has no problems, write one line: `No changes needed`. Avoid restating scoring tables, fixed rules, or this skill's internal logic.

By default, output only a patch summary, not a full project `opencode.jsonc`. Only output full JSONC when the user explicitly asks to “generate the full config” or “apply it”.

## Evidence Requirement

Every suggestion must include an evidence type:

| Evidence | Source |
|----------|--------|
| `config` | Project OpenCode config only; never from `~/.config/opencode/opencode.jsonc` |
| `agents` | AGENTS.md / CLAUDE.md |
| `structure` | Directory and file structure |
| `manifest` | package.json / pyproject.toml / composer.json / Cargo.toml, etc. |
| `absence` | Inference from missing corresponding files or settings |
| `cli` | CLI-resolved state from `opencode --version`, `opencode mcp list`, `opencode agent list`, `opencode auth list`, `opencode models`, etc. |
| `heuristic` | General rule of thumb with lower confidence |

If the only evidence is `absence` or `heuristic`, do not make a strong recommendation. Put it under “Consider”.

## Recommendation Confidence

Every suggestion must include confidence:

| Confidence | Condition |
|------------|-----------|
| High | Clear project config plus project structure / manifest evidence |
| Medium | One strong signal or several weak signals |
| Low | Mainly absence / heuristic |

Only High and Medium confidence suggestions may appear in the patch section. Low confidence suggestions must appear only under “Consider”.

## Global Config Safety Boundary

The global main config file `~/.config/opencode/opencode.jsonc` is high risk because it may contain MCP commands, API keys, provider auth, environment variables, and local paths. This skill **must not read, search, modify, or output this file**. This restriction applies only to this file. It does not ban reading other clearly safe and necessary global OpenCode resources.

For MCP state, the primary observation method is:

- `opencode mcp list`: get MCP server names, status, and redacted commands resolved for the current project.

Other safe read-only validation may be used, but never read `~/.config/opencode/opencode.jsonc` or print sensitive values:

- `opencode agent list`: get agent names visible to the CLI.
- `opencode auth list`: get a provider login summary only; do not read auth files.
- `opencode models [provider]`: validate model names.
- `opencode --version`: record version.

If an inherited or otherwise CLI-visible MCP should be disabled, do not read the global main config. Generate a project config mask directly:

```jsonc
{
  "mcp": {
    "<server-name-from-opencode-mcp-list>": {
      "enabled": false
    }
  }
}
```

In reports, say “mask inherited / CLI-visible MCP in this project”. Do not say “modify global main config” or “delete global item”.

## Project Type Detection Guardrail

Do not determine project type from a single file.

Examples:

- `package.json` does not always mean frontend; it may only be tooling.
- `Dockerfile` does not always mean deployment workflow.
- `db/schema.sql` does not always mean a database MCP is needed.
- A technology mentioned in README does not always mean it is currently used.

When classifying the project type, list the main evidence. If evidence is insufficient, use `Unknown / Mixed` instead of forcing a classification.

## Config File Health Check

Before relevance analysis and patch generation, check only the project config's basic health. Do not inspect or read `~/.config/opencode/opencode.jsonc`.

Check:

- Whether `opencode.json` / `opencode.jsonc` can be parsed. JSONC comments are fine; broken structure is not.
- Whether both `opencode.json` and `opencode.jsonc` exist in the project root, making the actual loaded source ambiguous.
- Whether `$schema` is missing. Suggest `"https://opencode.ai/config.json"`.
- Whether duplicate keys exist. If your tooling cannot reliably detect them, mark it as requiring manual confirmation.
- Whether suspicious or unknown top-level keys exist.
- Whether deprecated and new keys are mixed, such as legacy `tools` with `permission`.

Recommendations:

- If config parsing fails, do not generate patches. Report the config health issue only.
- If `$schema` is missing, it may be a Low / Medium confidence patch depending on whether the project config is confirmed.
- If both `opencode.json` and `opencode.jsonc` exist, do not guess precedence. Report “needs confirmation”.
- If unknown keys are found, call them “possible typo” unless schema or CLI error evidence is clear.

## MCP Secret Placement Check

Check whether MCP commands directly contain API keys, tokens, passwords, secrets, or similar sensitive values.

Detection:

- Scan project `mcp.<name>.command`, `args`, and the command shown by `opencode mcp list`. Never read `~/.config/opencode/opencode.jsonc`.
- Match common patterns such as `api-key`, `apikey`, `token`, `secret`, `password`, `bearer`, `ctx7sk-`, and `sk-`.
- Always redact values in the report and patch. Never print the original value.

Recommendations:

- Suggest using `environment` or external environment variables for secrets.
- Never generate a patch containing the original secret value.
- If the only source is CLI output and the config source is not visible, list it as “suggested improvement” only. Do not directly modify config.
- If the secret is already referenced by environment variable name, keep it and do not output the value.

## Provider Credential Source Check

If config specifies a provider but `opencode auth list` does not show it as logged in, do not immediately conclude that the provider is unusable.

Check:

- Whether `.env`, `.env.local`, or `.env.*` exists in the project.
- Only check file existence and key-name patterns. Do not read secret values.
- Whether `.env*` read deny rules already exist.

Recommendations:

- If credentials may come from `.env`, mark it as “needs confirmation”.
- Confirm `.env*` is denied for read, or at least do not read its content in the report.
- Do not log in providers automatically. Do not run mutating auth commands.

## Custom Tools Config Check

If config defines custom tools, treat them as high-impact project-level settings.

Check:

- Whether the tool runs arbitrary shell / node / python code.
- Whether it reads `.env`, credentials, the home directory, or paths outside the project.
- Whether it writes outside the project.
- Whether it duplicates MCP or custom command functionality.
- Whether it lacks a clear purpose description.

Recommendations:

- Do not suggest auto-allow for high-risk custom tools.
- Suggest disabling, removing, or converting low-relevance or duplicate custom tools into commands / MCPs, but only as advice. Do not delete automatically.
- If a custom tool writes outside the project, combine the finding with `permission.external_directory` checks.
- If a custom tool is required by the project workflow, keep it and cite evidence.

## Model Name Shape Check

Check whether `model` / `small_model` follows the `<providerId>/<modelId>` form.

Recommendations:

- If the format does not look like `<provider>/<model>`, mark it as a model shape issue.
- Use `opencode models [provider]` to validate candidate names. Do not invent model names.
- If the provider is not logged in but `.env` may provide the key, mark it as “needs confirmation” instead of invalid.
- `model` and `small_model` should not both point to expensive large models unless the project has clear evidence requiring it.

## Minimal Workflow

### Phase 1: Scan

If `scripts/analyze.py` exists, run it first to obtain structured data. If it does not exist, this is not an error; use Read / Glob / Grep instead. Never stop just because `scripts/analyze.py` is missing.

| Check | Command / Method |
|-------|------------------|
| Global main config | **Do not read** `~/.config/opencode/opencode.jsonc`; do not `cat`, `grep`, `find`, or modify this file. Other global OpenCode resources may be read only when clearly safe and necessary, and sensitive content must not be printed. |
| CLI-visible MCP state | Only use `opencode mcp list` to get MCP server names and status resolved for the current project. Redact before reporting. |
| Global skills | You may scan global skills' `SKILL.md` frontmatter (`name` / `description`) to judge relevance, but must not read `~/.config/opencode/opencode.jsonc`. If content is long, take only a summary. |
| Project structure | Run `ls -la` in the root and check `package.json`, `composer.json`, `Cargo.toml`, `pyproject.toml`, etc. |
| Project AGENTS.md | Read `AGENTS.md` or `CLAUDE.md` if present and parse project domain / requirements. |
| Project OpenCode config | Read project-root `opencode.json` or `opencode.jsonc` if present. |
| Project config health | Only check project `opencode.json` / `opencode.jsonc` parse state, `$schema`, duplicate files, duplicate keys, unknown keys, deprecated `tools` mixed with `permission`, etc. If parse fails, do not generate patches. |
| MCP secret placement | Scan MCP command / args / CLI output for API keys, tokens, or secrets. Reports must be redacted. Suggest `environment`. |
| Custom tools | If config has custom tools, inspect purpose, external paths, secret reads, and overlap with commands/MCPs. |
| CLI basic info | If `opencode` is available, run `opencode --version`. Record the version. Only check whether environment variables such as `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, `OPENCODE_CONFIG_CONTENT`, and `OPENCODE_PERMISSION` exist. Do not read their target files or print sensitive content. |
| Actual MCP loading state | If `opencode` is available, run `opencode mcp list`. Parse server name, enabled/disabled state, connected/error state, and command. If it fails, record CLI unavailable and continue. |
| MCP OAuth state | If OAuth MCPs exist, run `opencode mcp auth list` or `opencode mcp auth ls` to get an auth summary. Use it only to hint “login required / token expired / config abnormal”. Do not log in or out automatically. |
| Actual agent list | Run `opencode agent list`. Compare config / markdown definitions with CLI-visible agents. If a project-defined agent is not listed, mark it as config health issue. |
| Provider / auth state | Run `opencode auth list` to confirm authenticated providers. Do not print API keys or credential file contents. |
| Model availability | For providers or models set in config, run `opencode models [provider]` when needed to validate model names. Do not use `--refresh` by default. |
| Project language / framework | Scan key config files and directory structure, and list main evidence. If evidence is insufficient, mark `Unknown / Mixed`. |

### Phase 2: Analyze

#### a. Relevance Scoring

Use the following scoring rules for MCPs and skills:

| Grade | Label | Condition | Suggested Action |
|-------|-------|-----------|------------------|
| A | Highly relevant | Domain directly matches project type | Keep |
| B | Medium relevance | General development utility | Keep |
| C | Low relevance | Indirectly useful but lacks clear project evidence | Suggest masking by default; if evidence is weak, list as Consider |
| D | Irrelevant | Domain is unrelated | Suggest masking |

**AGENTS.md denoising override**: If AGENTS.md / CLAUDE.md clearly mentions frontend, database, or similar needs in current architecture, required tools, development workflow, testing workflow, or deployment workflow, related skills may be raised to B and kept. Technology names found only in changelog / history / progress / TODO / roadmap / examples / templates / deprecated / removed / legacy sections must not raise relevance.

#### b. Provider / Model Optimization

| Check | Recommendation Logic |
|-------|----------------------|
| `disabled_providers` is unset while 3+ providers are enabled | Suggest disabling unnecessary providers only when there is clear project model preference or too many providers create noise. |
| `model` is unset | Suggest setting a fixed model to avoid session-to-session inconsistency. If possible, validate candidate model names with `opencode models [provider]`. |
| `model` / `small_model` does not look like `<providerId>/<modelId>` | Mark as model shape issue. Validate with `opencode models [provider]`. Do not guess names. |
| `model` / `small_model` is set but not found by `opencode models [provider]` | Mark as model availability issue and suggest a valid `provider/model` name shown by CLI. |
| `small_model` is unset | Suggest setting one to reduce cost for lightweight tasks. |
| `default_agent` is unset | Suggest setting it to ensure expected behavior. If possible, validate the agent name with `opencode agent list`. |
| Config uses an unauthenticated provider | If `opencode auth list` does not list the provider, first check whether `.env*` may provide the key. If no evidence exists, mark auth readiness issue. Do not log in automatically. |

#### c. Feature Toggle Suggestions

| Feature | When the project has corresponding tooling | When the project lacks corresponding tooling |
|---------|-------------------------------------------|---------------------------------------------|
| `formatter` | Suggest enabling (`true`) | Suggest leaving disabled |
| `lsp` | Suggest enabling (`true`) | Suggest leaving disabled |
| `snapshot` | Default `true`; suggest keeping it | For very large projects (>2000 files), consider disabling |
| `autoupdate` | Suggest `true` or `notify` | Suggest `false` only in CI |
| `share` | Default `manual`; no change needed | For security-sensitive projects, consider `disabled` |

#### d. Resource Usage Optimization

| Check | Recommendation Logic |
|-------|----------------------|
| `watcher.ignore` lacks noisy-directory exclusions | Suggest entries based on project type, such as `.git/**`, `node_modules/**`, `dist/**`, `build/**`, `.next/**`, `.nuxt/**`, `.turbo/**`, `coverage/**`, `.venv/**`, `__pycache__/**`, `.pytest_cache/**`, `target/**`, `vendor/**`, `.gradle/**`. |
| CLI shows more than 5 connected MCPs, or config inference shows more than 5 enabled MCPs | Warn that too many MCPs can consume tokens. Prefer using actual `opencode mcp list` connected state to suggest disabling unnecessary MCPs. |
| `compaction.auto` is not `true` | Suggest enabling automatic compaction. |

#### e. Command Safety Check (without hurting flow)

| Check | Recommendation | Flow Impact |
|-------|----------------|-------------|
| Destructive `rm` lacks deny | Add deny for `rm -rf /`, `rm -rf /*`, `rm -rf ~`, `rm -rf .`, `rm -rf ..`, `rm -rf *`, and `rm *`. | No impact; these are not normal daily commands. |
| Force push lacks ask | Add ask only for `git push --force*`, `git push * --force*`, and `git push -f*`. Do not make normal `git push` ask. | Occasional prompt only. |
| `.env` is not denied under `read` | Confirm default protection is effective. | No impact. |
| `external_directory` is set to `"*": "allow"` | Suggest narrowing to concrete paths. | No impact. |
| `edit` is currently `"allow"` | Keep it. Do not suggest changing it. | Keeps flow smooth. |
| `bash: "ask"` but low-risk daily commands are not allowed | Suggest allowing `pwd`, `ls *`, `rg *`, `grep *`, `find *`, `git status`, `git diff *`, `git log *`, `npm test`, `npm run lint`, `pnpm test`, `pnpm lint`, `python -m pytest *`. Suggest `cat *` only if `.env*` read deny is active. | Reduces unnecessary prompts. |

#### f. Agent Settings Audit

| Check | Recommendation |
|-------|----------------|
| Custom agent missing `description` | Required; suggest adding it. |
| Custom agent has `disable: true` | Respect it. Do not ignore it. |
| Custom agent has contradictory `permission`, such as `edit: deny` with `mode: primary` | Suggest adjusting. |
| Custom agent `prompt: "{file:...}"` points to a file above roughly 2000 tokens | Suggest trimming the prompt file to avoid loading too much irrelevant content every session. |

#### g. AGENTS.md Health Check

Scan `AGENTS.md` or `CLAUDE.md` for content that consumes context but is not useful during development. **Do not interfere with formatting or number of sections.**

| # | Type | Detection | Recommendation |
|---|------|-----------|----------------|
| 1 | `## Changelog` / `## History` / `## What's New` | Match section title | Retrospective records are usually not useful during development; suggest removing. |
| 2 | `## Progress` / `## Status` / completed-work sections | Match section title | Dynamic content is stale at session start; suggest moving to a separate file. |
| 3 | `## TODO` / `## Known Issues` / `## Open Questions` embedded directly in the main file | Match title and check whether a separate file exists | Dynamic content should move to a separate file such as `AGENTS_TODO.md`. |
| 4 | Common-knowledge commands such as `npm install`, `npm run build`, `npm test`, `pip install`, `cargo build`, `go build`, `python -m pytest` without special parameters | Compare against known convention list | The AI already knows standard commands; keep only special flags, custom script names, or non-obvious restrictions. |
| 5 | `## File Structure` / `## Directory Tree` or long path lists | Match title and path patterns | Usually unnecessary; keep only important entry points. |
| 6 | More than 50 consecutive lines of prose, not bullets or code blocks | Count paragraph lines | Long tutorials should move to reference docs or a skill. |
| 7 | Leftover `TODO:` / `FIXME:` / `HACK:` comments | Regex match | Suggest cleaning or moving to a tracking file. |
| 8 | Machine-specific absolute paths starting with `/home/` or `/Users/` | Regex match | Suggest using relative paths or removing. |

#### h. Custom Command Suggestions and Command Creation Guardrail

Suggest missing shortcut commands based on project tools and workflows mentioned in AGENTS.md, comparing only against existing **project commands**. **Do not read global commands from `~/.config/opencode/opencode.jsonc`. You may read independent global command markdown frontmatter / summaries if clearly safe. Do not suggest duplicate project commands.**

Official reference: `https://opencode.ai/docs/commands/`

If the user asks to **add**, **create**, **write**, or **modify** an OpenCode command, you must first read the official Commands documentation above and follow the documented command format. Do not guess the command shape from memory.

Command creation rules:

- Prefer project-local markdown commands under `.opencode/commands/<name>.md` unless the user explicitly requests JSON config.
- For markdown commands, the file name becomes the slash command name; for example `.opencode/commands/test.md` becomes `/test`.
- Markdown command files may use frontmatter such as `description`, `agent`, and `model`; the markdown body becomes the command template.
- For JSON config commands, use the project config `command` block. The command needs a `template`; `description`, `agent`, `subtask`, and `model` are optional.
- Support documented placeholders only, such as `$ARGUMENTS`, `$1`, `$2`, shell output with `!\`command\``, and file references with `@path`.
- Be careful with shell-output injection because command output becomes part of the prompt. Avoid long, secret-bearing, or destructive shell commands.
- Check for collisions with existing project commands and built-in commands. Custom commands can override built-in commands; warn before suggesting or creating an override.
- Do not create or edit global commands unless the user explicitly asks. This skill's default behavior is project-local only.
- If the user only asks for optimization suggestions, suggest commands but do not create files. Create command files only when the user explicitly asks to add/create them.

Sources:

| Command Source | Scan Location |
|----------------|---------------|
| Project JSON definitions | `command` block in project-root `opencode.json` / `opencode.jsonc` |
| Project Markdown definitions | `.opencode/commands/*.md`, if present |

Suggestion logic:

| Tool / Situation | Detection | Suggested Command | Template Summary |
|------------------|-----------|-------------------|------------------|
| Git + remote (GitHub/GitLab) | `.git/config` contains `remote "origin"` URL | `/pr` | Get `git log` from base branch to HEAD and generate PR description + body. |
| Git with or without remote | `.git/` exists | `/branch` | Show existing branches, suggest a name, create or switch. |
| Git + SVN coexist | `.git/` + `.svn/` or `which svn` | `/sync` | `git add/commit`, then `svn add/commit`; similar to `/commit` but for dual-submit workflows. |
| npm / yarn / pnpm | `package.json` exists | `/clean` | Remove `node_modules` plus `dist` / `build`, then reinstall. |
| Test framework exists | `package.json` test script / `pytest.ini` / `Cargo.toml` dev dependencies | `/test` | Run the matching test command, analyze failures, suggest fixes. |
| Linter config exists | `.eslintrc*` / `.ruff.toml` / `.golangci.yml` / `tsconfig.json`, etc. | `/lint` | Run linter, apply auto-fixes, list remaining issues. |
| AGENTS.md mentions release/deploy/publish | Match `release`, `deploy`, `publish`, `發佈`, `部署` | `/release` | Follow documented flow: bump version, build, tag, deploy. |
| AGENTS.md mentions review / code review | Match `review`, `code review`, `審查` | `/review` | Review `git diff` item by item and suggest improvements. |
| Project is an Agent Skills repository with multiple SKILL.md files | `classify_project` returns `Agent Skills Repository` | `/skill-check` | Scan all SKILL.md frontmatter for required `name` / `description`. |

#### i. Visible Instructions Load Check

The `instructions` setting determines which extra files are loaded into each agent session. This skill only checks statically visible file count, file size, and low-value content. It does not analyze runtime context flow. If too many files or very large files are matched, they may waste context.

| Check | Recommendation |
|-------|----------------|
| `instructions` omitted or unset | No recommendation. |
| Total loaded instruction files > 5 | Suggest merging or trimming to reduce context waste. |
| Rough total instruction tokens > 2000 | Suggest keeping only required rules and moving the rest to `.agents/rules/` or reference files for on-demand use. |

#### j. Config / Tools Health Check

| Check | Recommendation Logic |
|-------|----------------------|
| Config parse fails | Stop patch generation and report config health issue only. |
| Missing `$schema` | Suggest adding `"https://opencode.ai/config.json"`. |
| Both `opencode.json` and `opencode.jsonc` exist | Mark as needing confirmation; avoid assuming which file is loaded. |
| MCP command contains a secret | Report after redaction and suggest using `environment`; never output original value. |
| Custom tools exist | Check sensitive path reads/writes, overlap with MCP/commands, and missing purpose descriptions. |
| Model shape is abnormal | Validate with `opencode models [provider]`; do not invent replacement models. |

### Phase 3: Produce the Report

Use the fixed template below.

## MCP Masking Rules

Do not compare against `~/.config/opencode/opencode.jsonc`. MCP checks are based on project config and `opencode mcp list`:

- If CLI shows `connected` and project evidence shows low relevance, suggest adding `mcp.<name>.enabled = false` to project config.
- If CLI shows `disabled`, treat it as already masked or disabled for the current project. Do not repeat the mask suggestion.
- If project config already has `{ "enabled": false }`, treat it as a project mask.
- If project config contains a full MCP definition with `type` + `command` or URL-style settings, only check secret placement, relevance, and necessity. Do not infer duplication with definitions inside `~/.config/opencode/opencode.jsonc`.

## MCP CLI Validation Rules

If `opencode` CLI is available, run this command in the current project root:

```bash
opencode mcp list
```

Purpose: verify MCP server state actually resolved for the current project, replacing any need to read `~/.config/opencode/opencode.jsonc`.

Parse:

| Field | Description |
|-------|-------------|
| server name | e.g. `context7`, `brave-search` |
| status | `disabled` / `connected` / `error` / other CLI-displayed status |
| command | MCP startup command; redact API keys, tokens, and secrets before reporting |
| source inference | Only label as `project-defined` / `project-masked` / `cli-visible`; never read `~/.config/opencode/opencode.jsonc` to determine source |

Recommendation logic:

- CLI shows `connected` but project evidence shows low relevance: raise masking priority because it is actually loaded in the current project.
- CLI shows `disabled`: treat as already masked or disabled. Do not repeat mask suggestion except for config-shape issues.
- CLI shows `error`: report as config health issue, but do not automatically suggest deletion. First determine whether this project needs the MCP.
- CLI command unavailable or unsupported: mark `CLI unavailable`, fall back to project config and project structure analysis, and do not read `~/.config/opencode/opencode.jsonc`.

Safety handling:

- Never output raw `--api-key`, `token`, `secret`, `password`, or similar sensitive values.
- If command contains a secret, replace it with `<redacted>`, for example `--api-key <redacted>`.
- CLI result is evidence type `cli`, which can combine with project `config`, `structure`, and `manifest` to increase confidence.

## Other CLI Validation Rules

The following CLI commands are read-only validation only. They should not modify settings or start interactive flows:

| Command | Purpose | Recommendation Logic |
|---------|---------|----------------------|
| `opencode --version` | Record version to help interpret config schema / CLI behavior differences | Show version in report. If CLI is old or lacks a command, downgrade to static analysis. |
| `opencode agent list` | Validate agents actually available in the current project | If `default_agent` or a project custom agent is not listed, mark config health issue. |
| `opencode auth list` / `opencode auth ls` | Validate logged-in providers | If config specifies a provider but it is not logged in, mark auth readiness. Never output credentials. |
| `opencode models [provider]` | Validate config `model` / `small_model` is a valid `provider/model` name | Only query providers used by config or candidates; avoid listing all models indiscriminately. |
| `opencode mcp auth list` / `opencode mcp auth ls` | Validate OAuth MCP authorization | If an MCP is relevant but unauthorized, mark “login required” instead of masking directly. |

Do not automatically run these commands in this skill:

| Command | Reason |
|---------|--------|
| `opencode mcp add` / `opencode mcp auth` / `opencode mcp logout` | Mutates settings or credential state; requires explicit user request. |
| `opencode agent create` | Creates agent files; requires explicit user request. |
| `opencode plugin` / `opencode plug` | Installs plugins and updates config; requires explicit user request. |
| `opencode run` | Creates sessions and may consume model quota; not a default validation command. |
| `opencode models --refresh` | Triggers remote refresh; only suggest when the user asks or model availability is clearly abnormal. |
| `opencode session list` / `opencode stats` / `opencode export` | Session / usage layer; outside this static config skill unless user asks. |
| `opencode uninstall` / `opencode upgrade` | Destructive or environment-changing commands; never run automatically. |

## CLI Safety and Output Handling

- Redact all CLI output before reporting: hide `api-key`, `token`, `secret`, `password`, credential paths, full auth JSON paths, and similar sensitive values.
- CLI validation failure must not stop the report. Mark `CLI unavailable` or `CLI command unsupported` and fall back to static analysis.
- CLI results may increase or decrease confidence, but must not replace project config / structure / manifest evidence.
- If CLI state conflicts with config inference, mark it as “needs confirmation” instead of generating high-risk patches.

## Low-Risk Path Guidelines

The following paths may be suggested as low-risk `permission.external_directory` allows. Only output them when project context and evidence support the suggestion; do not add all of them unconditionally.

| Path | Reason | Risk |
|------|--------|------|
| `/tmp/**` | General temporary directory with no persistent project data | Very low |
| `/private/tmp/**` | macOS temporary path | Very low |
| `/var/tmp/**` | Persistent temporary directory | Low |
| `/dev/null` | Output sink | None |
| `**/.opencode/**` | Avoid treating project-root `.opencode` as external when launching from a monorepo subdirectory | Low |

Avoid suggesting `"*": "allow"` unless the user explicitly asks for maximum flow and accepts the risk.

## Output Template

```text
╔═══════════════════════════════════════════╗
║ opencode-optimizer report                 ║
╚═══════════════════════════════════════════╝

[Project type] <classification>
[AGENTS.md needs] <if present, brief domain needs>
[CLI validation] <opencode version / CLI available / CLI unavailable>

========================================
0. Config Health
========================================
<config parse / schema / duplicate file / unknown key / MCP secret placement / custom tools / model shape>

========================================
1. MCP Masking / Loading Check
========================================
<currently loaded / already masked / masking suggestions summary>

========================================
2. Actual MCP Loading State (CLI)
========================================
<summary of opencode mcp list; connected / disabled / error; sensitive values must be redacted>

========================================
3. MCP Relevance
========================================
<name> │ <A/B/C/D> │ <keep/project mask suggestion> │ confidence │ evidence: <cli/project-config/structure/...>

========================================
4. Skills Relevance
========================================
<name> │ <A/B/C/D> │ <keep/project mask suggestion>

========================================
5. Low-Risk Path Suggestions
========================================
<path> → allow

========================================
6. Provider / Model / Auth Validation
========================================
<model / small_model / auth list / models CLI validation suggestions>

========================================
7. Feature Toggle Suggestions
========================================
<formatter / lsp / snapshot / autoupdate / share suggestions>

========================================
8. Resource Usage Optimization
========================================
<watcher.ignore / MCP count / compaction suggestions>

========================================
9. Command Safety Check
========================================
<rm / git push / .env / external_directory checks>

========================================
10. AGENTS.md Health
========================================
<content type + token estimate → suggestion>

========================================
11. Agent Availability Validation
========================================
<comparison between opencode agent list and default_agent / project custom agents>

========================================
12. Custom Command Suggestions
========================================
<command name> → <reason + compact template>

========================================
13. Patch Summary
========================================
Add:
- <key> = <value> │ confidence: <High/Medium> │ evidence: <config/agents/structure/manifest>

Modify:
- <key>: <old> → <new> │ confidence: <High/Medium> │ evidence: <...>

Project masks for inherited / CLI-visible items:
- <mcp/skill/provider>.enabled = false │ relevance: <C/D> │ confidence: <High/Medium> │ evidence: <cli/structure/manifest/...>

Consider but do not include in patch:
- <Low confidence / heuristic-only suggestion>

========================================
14. Full project opencode.jsonc
========================================
<Only output this when the user explicitly asks to generate the full config. Otherwise write: “Not generated; waiting for user confirmation.”>
```

## Quality Checks

- Every check has a reason, evidence, and confidence traceable to project facts.
- If `opencode` CLI is available, safe read-only validation has been run: `--version`, `mcp list`, and, when needed, `agent list`, `auth list`, `models [provider]`, `mcp auth list`; sensitive values are redacted.
- Config parse / schema / duplicate file / MCP secret placement / custom tools / model shape has been checked first. Do not generate high-risk patches when basic health is broken.
- Do not suggest setting `edit` / `bash` / `write` to `ask`.
- AGENTS.md / CLAUDE.md has been read and denoised.
- If adding or modifying OpenCode commands, `https://opencode.ai/docs/commands/` has been read first and the command is created using the documented project-local markdown or config format.
- C/D masking suggestions must clearly state that they mask inherited or CLI-visible items in project config. They must not imply reading, deleting, or modifying the global main config.
- Low confidence suggestions must not appear in the patch section. Put them under “Consider”.
- If no changes are needed, honestly report: `No optimization needed right now`.

## Non-Goals

- Do not read, search, write, or modify `~/.config/opencode/opencode.jsonc`.
- Do not automatically generate full project config unless the user explicitly asks.
- Do not analyze runtime context flow, session history, tool output pruning, or true usage frequency.
- Do not skip AGENTS.md / CLAUDE.md analysis and denoising.
- Do not cache previous results. Rescan every time.