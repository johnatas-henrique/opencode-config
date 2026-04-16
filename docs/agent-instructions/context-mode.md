# Context Mode — MANDATORY RULES

## ⚠️ CRITICAL — READ THIS FIRST

When processing data: **use ctx tools**. Reading raw data into context is **WRONG**.

This is NOT optional. If you use read/cat/grep to analyze data, you are **wrong**.

---

## Tool Substitution — AUTOMATIC

| Instead of... | Use... | Example |
|--------------|--------|---------|
| read entire file | ctx_execute_file | Analyze file content in sandbox |
| cat file | ctx_execute_file | Get summary, not full content |
| grep pattern | ctx_execute with grep | Find matches in sandbox |
| ls -la | ctx_execute | List with processing |
| find files | ctx_execute with glob | Find files in sandbox |
| wc -l | ctx_execute_file + processing | Count lines in sandbox |
| jq query | ctx_execute with jq | Process JSON in sandbox |

---

## Tool Selection

| Tool | Use For |
|------|---------|
| **ctx_batch_execute** | Multiple commands + search in ONE call |
| **ctx_execute_file** | Analyze file content in sandbox |
| **ctx_execute** | Run commands, process data in sandbox |
| **ctx_search** | Query indexed content |

---

## BEFORE any data operation: CHECK THIS

1. Does this question require reading/searching files? → Use ctx_execute
2. Does this question require analyzing data? → Use ctx_execute_file + processing
3. Does this question require searching content? → Use ctx_execute with grep

If YES to any: **USE ctx tools**, not read/cat/grep.

---

## Examples

### ❌ WRONG — floods context
```
read filePath: /path/to/large-file.txt
```
**Problem**: Reads entire file into context. Wasteful.

### ✅ CORRECT — processes in sandbox
```javascript
const lines = FILE_CONTENT.split('\n');
console.log('Total lines:', lines.length);
```
**Use**: ctx_execute_file + write code that processes and returns only the answer.

### ❌ WRONG — floods context
```
bash command: cat package.json
```
**Problem**: Raw JSON in context.

### ✅ CORRECT — sandbox processing
```javascript
const pkg = JSON.parse(FILE_CONTENT);
console.log(Object.keys(pkg.dependencies).join('\n'));
```
**Use**: ctx_execute_file + process JSON, return only keys.

---

## Verification Checklist

BEFORE using any tool, ask:

- [ ] Am I reading/analyzing data? → Use ctx_execute_file
- [ ] Am I searching for patterns? → Use ctx_execute with grep
- [ ] Am I processing output? → Use ctx_execute with code

If you used read/cat/grep for analysis, **STOP** and rewrite using ctx tools.

---

## Rule Summary

```
Analysis → ctx_execute_file + code → console.log(answer only)
Search → ctx_execute with grep → console.log(matches only)
Processing → ctx_execute with code → console.log(result only)
```