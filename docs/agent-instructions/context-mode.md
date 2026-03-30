# Context Mode — MANDATORY

<!-- [CTX-MODE] MANDATORY -->
MANDATORY: Use ctx tools for data operations.
NEVER: Use read/cat/grep for analysis.
<!-- [/CTX-MODE] -->

---

## Tool Substitution

| Instead of... | Use... |
|--------------|--------|
| read file | ctx_execute_file |
| cat file | ctx_execute_file |
| grep | ctx_execute with grep |
| ls -la | ctx_execute |
| find | ctx_execute with glob |
| wc -l | ctx_execute_file + processing |
| jq | ctx_execute with jq |

## Tools

| Tool | Use For |
|------|---------|
| ctx_batch_execute | Multiple commands + search |
| ctx_execute_file | Analyze file in sandbox |
| ctx_execute | Run commands |
| ctx_search | Query indexed content |

---

## Decision

1. Reading/searching files? → ctx_execute
2. Analyzing data? → ctx_execute_file + code
3. Searching content? → ctx_execute with grep

If yes: USE ctx tools, not read/cat/grep.

---

## Correct Pattern

```
Analysis → ctx_execute_file + code → console.log(answer only)
Search → ctx_execute with grep → console.log(matches only)
Processing → ctx_execute with code → console.log(result only)
```
