# Workflow Guidelines

1. Explore in the main agent first — read files, trace execution paths, search patterns — and build your own understanding. Do not delegate before you have seen the data.
2. Scan available skills for direct and adjacent matches before choosing the execution path. When in doubt, load the skill and check.
3. Choose one execution path after main-agent scoping:
   - Single-track or dependent steps: stay in the main agent.
   - Small reads or searches: use parallel tool calls in the main agent.
   - 2+ independent tracks: launch all subagents in the same response.
   - Use 2+ subagents or none. NEVER launch exactly 1 subagent.
4. Synthesize findings and re-read target files if context is stale.
5. Implement the smallest correct change.
6. Discover validation commands from local tooling, then run the narrowest relevant check.

Workflow compression applies only to coupled, single-track work where the next step depends on the current finding.

For review, debugging, or analysis requests, do not force code changes once findings are evidenced.