# Workflow

## Process (mindset)

- **Uncertainty** — Ask before choices that change behavior, API/UX, naming, persistence, auth, dependencies, config, or compatibility. Proceed without asking only when ambiguity is low-risk and repo conventions make the choice clear. State the assumption briefly.
- **Evidence** — Gather evidence proportional to risk. Trivial edits: inspect target file and adjacent context. Behavioral, API, dependency, or infrastructure change: trace execution path, call sites, constraints, and regression surface. Check local code, imports, config, types, tests, and patterns. Prefer external verification over self-review. State uncertainty when something cannot be confirmed.
- **Threshold** — Before launching an explore agent: if you can answer with grep + read in <1min (≤3 files), do it directly. Subagents are for multi-directory traversals or unknown codebases.

### Investigation

- Bundle independent reads/searches/outlines in one wave.
- Prefer `aft_outline` → structure, `aft_search` → concepts, `aft_callgraph` → callers/impact.
- Use `aft_outline`/`aft_zoom` over `webfetch` for URLs — AFT handles structured docs and GitHub better, with no navigation noise.
- Reserve `grep` for exact text, `read` for confirmation after `aft_zoom`.
- Check AFT `success` + `complete` before trusting result.
- Classify findings: KEEP / MAYBE / DISCARD. Don't act on MAYBE.

## Execution flow

1. Explore in the main agent first — read files, trace execution paths, search patterns. Do not delegate before you have seen the data.
2. Scan available skills for direct and adjacent matches. When in doubt, load the skill and check.
3. Choose execution path:
   - Single-track or dependent steps: stay in the main agent.
   - Small reads or searches: use parallel tool calls in the main agent.
   - 2+ independent tracks: launch all subagents in the same response.
   - Use 2+ subagents or none. NEVER launch exactly 1 subagent.
   - **Cascade depth = 1.** Subagents MUST NOT launch further subagents. They use direct tools only (grep, read, aft_search) — never task().
4. Synthesize findings and re-read target files if context is stale.
5. Implement the smallest correct change.
6. Discover validation commands from local tooling, then run the narrowest relevant check.

Workflow compression applies only to coupled, single-track work where the next step depends on the current finding.

For review, debugging, or analysis requests, do not force code changes once findings are evidenced.
