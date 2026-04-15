# Context Mode — STRICT RULES

## MANDATORY FOR DATA OPERATIONS

When you need to analyze, count, filter, compare, search, parse, or process data: **USE ctx_execute**. Reading raw data into context is **WRONG**.

## Rules — FOLLOW OR YOU WILL BE WRONG

### Think in Code — MANDATORY

```javascript
// WRONG - uses too much context
cat large-file.log

// CORRECT - processes in sandbox, returns only the answer
const lines = FILE_CONTENT.split('\n');
const errors = lines.filter(l => l.includes('ERROR'));
console.log(errors.length);
```

### Tool Substitution — DO THIS AUTOMATICALLY

Replace these tools when processing data:

| Instead of...           | Use THIS...                      |
| ---------------------- | -------------------------------|
| Shell >20 lines       | `ctx_execute`                    |
| File reading (analysis)| `ctx_execute_file`               |
| grep (large results)   | `ctx_execute` with grep         |
| cat > analysis       | `ctx_execute_file` + processing |

### Tool Selection Hierarchy

1. **ctx_batch_execute** — run multiple commands + search in ONE call
2. **ctx_execute** / **ctx_execute_file** — sandbox execution
3. **ctx_search** — query indexed content
4. **ctx_fetch_and_index** → **ctx_search** — web pages

### Context Mode Commands

| Command | Action |
|---------|--------|
| `ctx stats` | Display context savings |
| `ctx doctor` | Run diagnostics |

## Verification

If you used `cat`, `read`, or `bash` without processing in sandbox, **STOP NOW** and rewrite using ctx_execute.

## Summary

- Want to process data? Use **ctx_execute**
- Want to analyze file? Use **ctx_execute_file**
- Only use **console.log()** for the answer
- Never dump raw data into context