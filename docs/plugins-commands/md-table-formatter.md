# Markdown Table Formatter Plugin

**Status:** ✅ Active
**Purpose:** Automatically format markdown tables after AI completion with concealment mode support.
**Plugin:** `@franlol/opencode-md-table-formatter`

---

## Quick Command Reference

| Command/Tool | Interface | Description |
|--------------|-----------|-------------|
| (automatic) | Automatic | Formats markdown tables in AI responses silently |

---

## Overview

When the AI generates markdown tables, they are often misaligned due to markdown formatting symbols (bold, italic) affecting width calculations. This plugin automatically reformats tables to ensure proper column alignment, even when OpenCode's **concealment mode** is enabled (which hides `**`, `*`, `~`, etc.).

### Example

**Before:**
```markdown
| Name    | Age | Description          |
| ------- | --- | -------------------- |
| Alice   | 30  | **Senior** dev       |
| Bob     | 25  | Junior *designer*    |
```

**After:**
```markdown
| Name  | Age | Description      |
| ----- | --- | ---------------- |
| Alice | 30  | Senior dev       |
| Bob   | 25  | Junior designer  |
```

---

## Features

- **Automatic formatting**: Every AI response containing markdown tables is reformatted invisibly.
- **Concealment mode compatible**: Correctly calculates column widths when markdown symbols are hidden by the TUI.
- **Alignment support**: Respects left (`:---`), center (`:---:`), and right (`---:`) text alignment.
- **Nested markdown handling**: Strips bold, italic, strikethrough with multi-pass algorithm.
- **Code block preservation**: Keeps markdown symbols inside inline code (e.g., `` `**bold**` ``) intact.
- **Edge case handling**: Emojis, unicode characters, empty cells, long content.
- **Silent operation**: No console logs; errors don't interrupt workflow.

---

## How It Works

1. The plugin uses OpenCode's `experimental.text.complete` hook.
2. After the AI finishes generating text, the hook fires and scans for markdown tables.
3. For each table, it:
   - Identifies the table structure (headers, separators, rows).
   - Strips markdown formatting symbols (**bold**, *italic*, ~~strikethrough~~) **except** inside inline code blocks.
   - Calculates proper column widths based on stripped content.
   - Reconstructs the table with correct alignment and padding.
4. The formatted table replaces the original in the final output.

This ensures tables render correctly in the TUI with concealment mode on.

---

## Configuration

No configuration needed. The plugin is always active when loaded.

Add to your OpenCode config (already done):

```json
{
  "plugin": ["@franlol/opencode-md-table-formatter@latest"]
}
```

---

## Requirements

- OpenCode >= 1.0.137
- `@opencode-ai/plugin` >= 0.13.7

---

## Troubleshooting

**Tables not formatting?**
- Ensure the plugin is listed in your `opencode.json` or `.opencode/opencode.jsonc`.
- Restart OpenCode after adding the plugin.
- Verify your OpenCode version meets requirements.

**Formatting looks wrong?**
The plugin is designed for standard markdown tables. If your table uses non-standard syntax or complex nested structures, it might not be recognized. Check the GitHub issues for known edge cases.

---

## Notes

- This plugin only affects **assistant** messages, not user input.
- It runs silently; you won't see any logs unless something fails.
- Works seamlessly with concealment mode (the default in OpenCode).

---

## Related

- [Magic Context](magic-context.md) — Context management and compression
- [Lean-ctx](lean-ctx.md) — Shell and file compression

---

## License

MIT © franlol
