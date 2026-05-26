# Understand-Anything Commands & Tools

**Status:** ✅ Active
**Purpose:** Interactive knowledge graph for codebase understanding — guided tours, semantic search, business domain mapping, and persona-adaptive dashboard.
**Repository:** https://github.com/Lum1104/Understand-Anything
**Documentation:** https://understand-anything.com

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|---|---|---|
| `/understand` | TUI | Run multi-agent pipeline — scans project, extracts functions/classes/deps, builds knowledge graph |
| `/understand-dashboard` | TUI (Browser) | Open interactive web dashboard with force-directed graph, search, tours |
| `/understand-chat` | TUI | Ask questions about the codebase in natural language |
| `/understand-explain <path>` | TUI | Plain-English explanation of a specific file or function |
| `/understand-onboard` | TUI | Generate onboarding guide ordered by dependency (new hires) |
| `/understand-domain` | TUI | Extract business domains, flows, and process steps from code |
| `/understand-diff` | TUI | Analyze ripple effects of uncommitted changes across the graph |
| `/understand-knowledge <path>` | TUI | Analyze a Karpathy-pattern LLM wiki (wikilinks, categories, entities) |

---

## User Commands (TUI)

Type these in the chat:

| Command | Description |
|---|---|
| `/understand` | **Main analysis.** Orchestrates 5 agents: project-scanner, file-analyzer (parallel, up to 5 concurrent), architecture-analyzer, tour-builder, graph-reviewer. Saves to `.understand-anything/knowledge-graph.json`. |
| `/understand --language <code>` | Localized output. Supported: `en` (default), `zh`, `zh-TW`, `ja`, `ko`, `ru`. Affects node summaries, dashboard UI labels, and tour explanations. |
| `/understand --review` | Full LLM graph review pass (slower, higher quality). Default is inline validation only. |
| `/understand --auto-update` | Enable post-commit hook to incrementally patch the graph. |
| `/understand-dashboard` | Opens local web dashboard in browser. Graph is color-coded by architectural layer, clickable, searchable (fuzzy + semantic). Features: hierarchical drill-down, community clustering, dependency path finder, persona-adaptive UI (junior dev → power user), export to PNG/SVG/JSON. |
| `/understand-chat How does the payment flow work?` | Ask anything about the codebase. Uses the knowledge graph as context. |
| `/understand-explain src/auth/login.ts` | Deep-dive into a specific file or function with plain-English summary. |
| `/understand-onboard` | Generates a walkthrough ordered by dependency — learn the codebase in the right sequence. |
| `/understand-domain` | Runs a 6th agent (domain-analyzer) to extract business domains, flows, and process steps. |
| `/understand-diff` | Compares working tree changes against the graph and shows affected nodes. |
| `/understand-knowledge ~/path/to/wiki` | Analyzes an LLM wiki (Karpathy pattern: `index.md` with wikilinks). Deterministic parser extracts links and categories; LLM agents discover implicit relationships, entities, and claims. |

---

## How It Works

### Multi-Agent Pipeline (`/understand`)

| Agent | Role |
|---|---|
| `project-scanner` | Discover files, detect languages and frameworks |
| `file-analyzer` | Extract functions, classes, imports; produce graph nodes and edges (parallel, 5 concurrent) |
| `architecture-analyzer` | Identify architectural layers (API, Service, Data, UI, Utility) |
| `tour-builder` | Generate guided learning tours ordered by dependency |
| `graph-reviewer` | Validate graph completeness and integrity (inline by default, full pass with `--review`) |
| `domain-analyzer` | Extract business domains, flows, steps (used by `/understand-domain`) |

### Dashboard Features

- **Force-directed graph** — pan, zoom, click, search
- **Color-coded layers** — API, Service, Data, UI, Utility with legend
- **Persona-adaptive UI** — detail level adjusts based on role (junior, PM, power user)
- **Fuzzy + semantic search** — "which parts handle auth?" returns relevant nodes
- **Guided tours** — auto-generated walkthroughs in dependency order
- **Domain view** — switch from structural graph to business process graph
- **Diff impact** — visual overlay of what your changes affect
- **Export** — PNG, SVG, filtered JSON
- **Dependency path finder** — shortest path between any two components

---

## Installation

For OpenCode, add to `~/.config/opencode/config.json` (global) or project `opencode.json`:

```json
{
  "plugin": ["understand-anything@git+https://github.com/Lum1104/Understand-Anything.git"]
}
```

Restart OpenCode. Verify with `List available skills` — you should see `understand`, `understand-chat`, `understand-dashboard`, etc.

---

## Sharing the Graph

The graph is JSON — commit `.understand-anything/` (excluding `intermediate/` and `diff-overlay.json`) so teammates skip the 5-agent pipeline. For large graphs (10 MB+), use git-lfs.

```gitignore
.understand-anything/intermediate/
.understand-anything/diff-overlay.json
```

---

## Typical Workflow

```bash
# 1. First run — builds the graph (takes a few minutes)
/understand

# 2. Explore visually
/understand-dashboard

# 3. Ask specific questions
/understand-chat como funciona o fluxo de autenticação?

# 4. Before a handoff or PR, check impact
/understand-diff

# 5. Generate onboarding for new team members
/understand-onboard

# 6. For business logic understanding
/understand-domain
```

---

## See Also

- [Magic Context](magic-context.md) — Chat compression and cross-session memory
- [Codebase Memory MCP](codebase-memory-mcp.md) — AST-level code graph for the agent
