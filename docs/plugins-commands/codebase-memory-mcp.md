# Codebase Memory MCP Commands & Tools

**Status:** ⏳ Pending installation
**Purpose:** Knowledge graph of codebase via AST (tree-sitter) — 99% token reduction on code queries
**Documentation:** https://deusdata.github.io/codebase-memory-mcp/
**Repository:** https://github.com/DeusData/codebase-memory-mcp

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `codebase-memory-mcp` | CLI | Main binary — index, query, config, UI |
| `/mcp` | TUI | Check if MCP server is loaded (should list 14 tools) |

---

## MCP Tools (14 tools)

Once installed, the agent automatically uses these tools via OpenCode's MCP integration:

| Tool | Description |
|------|-------------|
| `index_repository` | Index a repository into the knowledge graph (creates SQLite DB) |
| `list_projects` | List all indexed projects with node/edge counts |
| `delete_project` | Remove a project and all its graph data |
| `index_status` | Check indexing status of a project |
| `search_graph` | Structured search by label, name pattern, file pattern, degree filters |
| `trace_call_path` | BFS traversal — who calls a function and what it calls (depth 1-5) |
| `detect_changes` | Map git diff to affected symbols + risk classification |
| `query_graph` | Execute Cypher-like graph queries (read-only) |
| `get_graph_schema` | Get node/edge counts, relationship patterns, property definitions |
| `get_code_snippet` | Read source code for a function by qualified name |
| `get_architecture` | Codebase overview: languages, packages, routes, hotspots, clusters, ADRs |
| `search_code` | Grep-like text search within indexed project files |
| `manage_adr` | CRUD for Architecture Decision Records |
| `ingest_traces` | Ingest runtime traces to validate HTTP_CALLS edges |

---

## CLI Mode

Every MCP tool can be invoked from the command line:

```bash
# Index a repository
codebase-memory-mcp cli index_repository '{"repo_path": "/absolute/path/to/repo"}'

# Search for functions matching pattern
codebase-memory-mcp cli search_graph '{"name_pattern": ".*Handler.*", "label": "Function"}'

# Trace call path
codebase-memory-mcp cli trace_call_path '{"function_name": "Search", "direction": "both"}'

# Get architecture overview
codebase-memory-mcp cli get_architecture '{}'

# List indexed projects
codebase-memory-mcp cli list_projects
```

---

## User Commands (TUI)

No special TUI commands — the MCP tools are used automatically by the agent. Just ask naturally:

- "What's the architecture of this codebase?"
- "Trace the call path for function X"
- "Show me affected symbols from recent changes"
- "Search for database models"

---

## Configuration

### Install-time auto-config

The `install.sh` or `install.ps1` script automatically:
- Downloads the binary to `~/.local/bin/`
- Adds MCP server entry to `opencode.json`
- Creates/updates `AGENTS.md` with instructions
- Installs advisory hooks (remind agent to use graph tools before grep/read)

### Manual config

```bash
# View current config
codebase-memory-mcp config list

# Set auto-index on session start
codebase-memory-mcp config set auto_index true

# Set file limit for auto-index (default 50000)
codebase-memory-mcp config set auto_index_limit 50000

# Reset a config key
codebase-memory-mcp config reset auto_index
```

**Config file location:**
- Linux/macOS: `~/.config/codebase-memory-mcp/config.json`
- Windows: `%USERPROFILE%\.config\codebase-memory-mcp\config.json`
- Override: `CBM_CONFIG_PATH` environment variable

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CBM_CACHE_DIR` | `~/.cache/codebase-memory-mcp/` | Override database storage directory |
| `CBM_DIAGNOSTICS` | `false` | Enable periodic diagnostics (`1` or `true`) |
| `CBM_DOWNLOAD_URL` | GitHub releases | Override download URL for updates |

---

## Installation

### One-line install (recommended)

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 | iex
```

### With graph visualization UI

Add `--ui` flag:

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash -s -- --ui
```

**Windows:**
```powershell
.\install.ps1 --ui
```

Then run:
```bash
codebase-memory-mcp --ui=true --port=9749
# Open http://localhost:9749 in browser
```

---

## Validation Checklist

After installation:

- [ ] `codebase-memory-mcp` binary exists (`which codebase-memory-mcp` or `where codebase-memory-mcp`)
- [ ] `/mcp` in OpenCode shows `codebase-memory-mcp` with 14 tools
- [ ] First project index completes (`index_status` shows `complete`)
- [ ] `get_architecture()` returns structured data when asked
- [ ] `trace_call_path(function_name="main")` returns call graph
- [ ] Advisory hooks appear in `~/.config/opencode/AGENTS.md` (optional)
- [ ] RTK and Magic Context still work (no regression)

---

## Performance

| Operation | Time (typical) | Notes |
|-----------|----------------|-------|
| Full index (medium project) | ~5-30s | Django (~6s), medium repo |
| Full index (large project) | ~1-5 min | 50k+ files |
| Query (search_graph, trace) | <10ms | Sub-millisecond |
| Query (get_architecture) | ~50ms | Still instant |
| Auto-sync (git change) | ~1-3s | Incremental |

**Storage:** ~50-500 MB per project (SQLite WAL mode)

---

## Security & Trust

- **Single static binary** — zero dependencies
- **SLSA Level 3** — cryptographic build provenance
- **VirusTotal** — 0/72 detections on all releases
- **Sigstore cosign** — keyless signatures on artifacts
- **Local-only processing** — code never leaves your machine
- **Open source** — full source available, reproducible builds

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `/mcp` doesn't list cbm | Restart OpenCode after install; check `opencode.json` has MCP entry |
| `index_repository` fails | Use absolute path; ensure Git repo; check write permissions in cache dir |
| Tools return empty results | Verify `index_status` is `complete`; try `search_graph` with broad pattern first |
| Binary not found after install | Add `~/.local/bin` to PATH (`export PATH="$HOME/.local/bin:$PATH"`) |
| UI not loading | Use `--ui` variant; check `http://localhost:9749`; ensure port free |
| Slow indexing | Normal for large repos; use `--ui` to see progress; set `auto_index_limit` if needed |

**Logs:**
- OpenCode logs: `~/.local/share/opencode/log/`
- codebase-memory-mcp diagnostics: set `CBM_DIAGNOSTICS=1` (writes to `/tmp/cbm-diagnostics-*.json`)

**Reset:**
```bash
rm -rf ~/.cache/codebase-memory-mcp/
# Re-index projects
```

---

## References

- **Repository:** https://github.com/DeusData/codebase-memory-mcp
- **Documentation:** https://deusdata.github.io/codebase-memory-mcp/
- **Paper:** https://arxiv.org/abs/2603.27277
- **Benchmarks:** 99% token reduction, sub-ms queries, 66 languages
- **OpenCode integration:** Automatic via `install` script (adds MCP server + hooks)

---

## How It Works (Brief)

1. **Indexing:** Tree-sitter parses all source files → AST → extracts nodes (functions, classes, etc.) and edges (calls, imports, definitions)
2. **Storage:** SQLite database with FTS5 for text search + vector embeddings (optional) for semantic search
3. **Query:** Agent calls MCP tools → graph traversal (BFS, Cypher) returns structured results in ~300-800 tokens vs ~10k-20k by manual file reading
4. **Sync:** Git-based change detection automatically re-indexes affected files incrementally

---

## Migration from Graphify / Other Tools

If you were using Graphify or similar code graph tools:
- `codebase-memory-mcp` **replaces** the need for manual graph generation
- No need to generate `graph.json` or Obsidian notes
- Direct MCP access means the agent queries the live graph, not static files
- You can keep Graphify if you want notes, but not required

---

## Uninstall

```bash
# Remove MCP config from OpenCode
codebase-memory-mcp uninstall

# Remove binary (optional)
rm -f ~/.local/bin/codebase-memory-mcp

# Remove cache (optional, deletes all indexed projects)
rm -rf ~/.cache/codebase-memory-mcp/
```

The `uninstall` command removes MCP server entries, AGENTS.md instructions, and hooks. Does not touch your projects.
