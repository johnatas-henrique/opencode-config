# Session Recall Plugin

**Status:** ✅ Active
**Purpose:** Search and retrieve past OpenCode chat sessions that would otherwise be lost to compaction.
**Plugin:** `opencode-session-recall` (global plugin)

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `session-search(query, limitSessions)` | MCP (Agent) | Search local chat history for sessions containing specific text |
| `session-title-search(query, limitSessions)` | MCP (Agent) | Search for sessions by their title |
| `session-transcript(sessionId, limit, order)` | MCP (Agent) | Reconstruct full transcript of a specific chat session |

---

## Overview

Session Recall adds the ability to search through your complete chat history, even after sessions have been compacted or archived. It provides tools to:

- Search sessions by keyword/content
- Search sessions by title
- Retrieve full transcripts of past conversations
- Find sessions by date, project, or directory

This complements Magic Context's cross-session memory by letting you explicitly fetch and review old conversations.

---

## Agent Tools (MCP)

The agent can use these tools automatically or you can ask it to:

| Tool | Description | Parameters |
|------|-------------|------------|
| `session-search(query, limitSessions)` | Search local chat history for sessions containing specific text. | `query` (string, required): 1-200 chars, non-whitespace<br>`limitSessions` (number, optional): 1-12, default 6 |
| `session-title-search(query, limitSessions)` | Search for sessions by their title. | `query` (string, required)<br>`limitSessions` (number, optional) |
| `session-transcript(sessionId, limit, order)` | Reconstruct the full transcript of a specific chat session. | `sessionId` (string, required): e.g., `ses_abc123`<br>`limit` (number, optional): 1-120, default 80<br>`order` (string, optional): `asc` or `desc`, default `asc` |

---

## Usage Examples

You can ask the agent to:

```
Find sessions where we discussed authentication
```

```
Search for my work on the storage module from last week
```

```
Get the full transcript of session ses_abc123
```

The agent will call the appropriate tools and present results with:
- Session metadata (title, directory, date)
- Snippets showing matches
- Suggestions for opening the full transcript

---

## How It Works

1. **Storage:** Session data is stored locally under `~/.local/share/opencode/session/` (or project-specific `.opencode/session/`).
2. **Indexing:** Content is indexed for fast search. Index format may be keyword, regex, or fuzzy depending on configuration.
3. **Retrieval:** When you search, matching sessions are returned with excerpts and metadata.
4. **Transcript reconstruction:** The `session-transcript` tool can reconstruct full conversations (subject to limit).

---

## Storage Details

Sessions are stored as JSON files:

```
~/.local/share/opencode/session/{projectID}/ses_*.json
```

Each session contains:
- Title
- Directory/workspace
- Project name
- Messages with roles (user/assistant) and content
- Timestamps
- Tool invocations (if any)

---

## Configuration

No special configuration needed. The plugin is enabled by being listed in your `opencode.json` `plugin` array.

```json
{
  "plugin": [
    "opencode-handoff",
    "opencode-session-recall",
    ...
  ]
}
```

---

## Notes

- **Local only:** All data stays on your machine.
- **No extra cost:** No API calls; searches your local history.
- **Works with compaction:** Even if Magic Context compresses sessions, the full raw history is preserved and searchable.
- **Complementary:** Works alongside Magic Context's memory system. Session Recall lets you fetch old conversations; Magic Context extracts and stores decisions as structured memories.

---

## Related Plugins

- [Magic Context](magic-context.md): Provides cross-session memory and chat compression.
- [Lean-ctx](lean-ctx.md): Compresses shell/file output, independent of session storage.

---

## Troubleshooting

**No search results?**
- Verify sessions exist in `~/.local/share/opencode/session/`.
- Check file permissions on the storage directory.

**Want to disable?**
Remove `"opencode-session-recall"` from your `opencode.json` plugin list and restart OpenCode.

---

## CLI Access (Optional)

You can also search from the terminal:

```bash
bunx opencode-session-recall search -- "auth login" --limitSessions 5
```

(Requires the plugin package to be installed globally.)
