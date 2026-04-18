# OpenCode Handoff Plugin

**Status:** ✅ Active
**Purpose:** Create focused handoff prompts for continuing work in new sessions.
**Plugin:** `opencode-handoff`

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| `/handoff <goal>` | TUI | Creates a handoff prompt, analyzes conversation, extracts relevant files, and opens a new session with an editable draft. |
| `read_session(sessionId)` | Agent Tool | Retrieves full conversation transcript from a previous session (used by the AI during handoff). |

---

## Overview

The Handoff plugin solves the "file archaeology" problem: when starting a fresh session, the AI spends time grepping and reading files to rediscover context. `/handoff` generates a continuation prompt that includes all the relevant files and decisions so the next session can start productive immediately.

---

## `/handoff <goal>` Command

### Usage

Type in the chat:

```
/handoff implement the user authentication feature we discussed
```

### What it does

1. **Analyzes the conversation** to extract:
   - Decisions made
   - Constraints identified
   - Files that should be loaded (8-15 recommended)
   - The goal for continuation

2. **Generates a focused prompt** structured with:
   - Context summary
   - Relevant file references (using `@file` syntax)
   - Clear goal description

3. **Opens a new session** with the prompt as an editable draft. You can review/edit before sending.

### Session Continuity

The generated prompt includes a line:

```
Continuing work from session sess_01jxyz123. When you lack specific information you can use read_session to get it.
```

This gives the AI access to the `read_session` tool, allowing it to fetch details from the source session if needed.

---

## `read_session` Tool (Agent Tool)

The AI can call this to retrieve full transcripts from previous sessions.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sessionId` | string | yes | The session ID (e.g., `ses_abc123`). |

### Returns

Full conversation transcript including:
- Session metadata (title, slug, directory, project info)
- All messages with roles (user/assistant) and content
- Tool invocations (if any)

### Use Cases

- The AI asks: "What were the specific error messages we saw earlier?"
- The handoff prompt included a session reference; the AI can call `read_session` to fetch details.
- Useful when the handoff summary omitted details that are now needed.

---

## Installation & Configuration

Already installed via global plugin list:

```json
{
  "plugin": ["opencode-handoff"]
}
```

No additional configuration required.

---

## Example Workflow

1. You're working on a feature in Session A.
2. You decide to start fresh to reduce context size.
3. Type: `/handoff continue implementing auth middleware`
4. New session opens with a draft prompt pre-loaded with relevant files and context.
5. Review/edit the draft, then send.
6. The AI in Session B starts work immediately without needing to rediscover files.

---

## Notes

- Requires OpenCode v1.2.15 or later.
- The plugin automatically includes file references using `@file` syntax, which loads those files into the new session's context.
- Handoff prompts are designed to be concise yet comprehensive—the goal is to avoid "file archaeology" in the new session.

---

## Related

- [Magic Context](magic-context.md) — Cross-session memory and chat compression
- [Session Recall](session-recall.md) — Search past sessions by content
