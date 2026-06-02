# AgentMemory Plugin Fix & NVIDIA NIM Integration

**Date:** 2026-05-29/30  
**Session ID:** ses_18c037886ffeuc4c1m74Tjtsvo  
**Duration:** ~6 hours  

---

## Summary

This session involved diagnosing and fixing the agentmemory plugin for OpenCode, including:
1. Fixing project path detection bug
2. Adding debug logging to file
3. Upgrading agentmemory to v0.9.24
4. Recovering lost observations
5. Testing and configuring NVIDIA NIM as LLM provider

---

## Phase 1: Problem Identification

### Initial Issue
- Agentmemory plugin was not injecting context into the agent's system prompt
- The `experimental.chat.system.transform` hook was not firing correctly

### Root Cause Discovery
1. **Project path bug:** `ctx.worktree` was returning `/` instead of `undefined` when no git worktree existed
2. **Debug visibility:** Plugin used `console.error` which was invisible in OpenCode's TUI
3. **Outdated version:** Agentmemory v0.9.21 lacked auto-context injection fix

---

## Phase 2: Plugin Fixes

### Fix 1: Project Path Detection
**File:** `~/.config/opencode/plugins/agentmemory-capture.ts`

**Before (line 171):**
```ts
projectPath = ctx.worktree || ctx.project?.id || process.cwd();
```

**After (line 180):**
```ts
const hasWorktree = ctx.worktree && ctx.worktree !== "/";
projectPath = hasWorktree ? ctx.worktree : ctx.directory || process.cwd();
```

**Why:** `ctx.worktree` returns `/` when no worktree exists, which is truthy in JavaScript, causing incorrect project path.

### Fix 2: Debug to File
**Added imports (lines 1-3):**
```ts
import * as fs from "node:fs";
import * as path from "node:path";
```

**Added debug function (lines 12-18):**
```ts
const DEBUG_FILE = path.join(process.cwd(), ".agentmemory-debug.log");

function debug(...args: unknown[]) {
  if (!DEBUG) return;
  const msg = `[${new Date().toISOString()}] ${args.map(String).join(" ")}\n`;
  try { fs.appendFileSync(DEBUG_FILE, msg); } catch {}
}
```

**Replaced all `console.error` calls with `debug()`:**
- Line 35: HTTP POST failures
- Line 49: HTTP POST failures
- Line 181: Project path info
- Line 278: Session deletion

### Fix 3: Provider Info Logging
**Added function (lines 20-32):**
```ts
function logProviderInfo() {
  if (!DEBUG) return;
  const hasOpenAI = !!process.env.OPENAI_API_KEY;
  const hasGemini = !!process.env.GEMINI_API_KEY;
  const hasAnthropic = !!process.env.ANTHROPIC_API_KEY;
  const hasOpenRouter = !!process.env.OPENROUTER_API_KEY;
  const provider = hasOpenAI ? `openai (${process.env.OPENAI_MODEL || "default"})` :
                   hasGemini ? "gemini" :
                   hasAnthropic ? "anthropic" :
                   hasOpenRouter ? "openrouter" : "noop";
  const baseUrl = process.env.OPENAI_BASE_URL || "(default)";
  debug("provider:", provider, "| baseUrl:", baseUrl);
}
```

**Called at plugin initialization (line 196):**
```ts
logProviderInfo();
```

---

## Phase 3: Agentmemory Upgrade

### Upgrade to v0.9.24
```bash
npm i -g @agentmemory/agentmemory@0.9.24
```

**Key fixes in v0.9.24:**
- OpenCode plugin zero-config auto-context injection (PR #648, closes #431)
- OpenCode plugin implicit-creates session on first observation (closes #638)
- Full 51-tool MCP surface by default (closes #553)

### Service Restart
```bash
systemctl --user restart agm
```

---

## Phase 4: Data Recovery & Cleanup

### Problem
- Old observations (May 23-29) were stored under `project: "/"` instead of correct path
- After upgrade, `state_store.db/` directory contained 67 orphaned `.bin` files

### Recovery Steps
1. Exported all data via `GET /agentmemory/export`
2. Edited JSON to fix project paths from `/` to `/home/johnatas/projects`
3. Imported with `strategy: "replace"` via `POST /agentmemory/import`

### Final Cleanup
- Deleted all sessions via `POST /agentmemory/session/end`
- Deleted all memories via `POST /agentmemory/forget`
- Cleared `stream_store/` directory (17.83 MB)

---

## Phase 5: Observation Recreation

### Script Created
**File:** `/home/johnatas/projects/recreate_observations.py`

**Function:** Recreates observations from session history via `POST /agentmemory/observe`

**Results:**
- 132 observations created via API
- 76 unique observations after engine processing
- 1369 compress calls triggered

---

## Phase 6: NVIDIA NIM Integration

### Why Switch from Gemini
- Gemini API averaging 10.7s response time
- Frequent timeouts (5% failure rate)
- Close to 15s `CALL_TIMEOUT_MS` limit

### Model Testing
Tested 12 models on NVIDIA NIM endpoint:

| Model | Time (s) | Quality | Status |
|-------|----------|---------|--------|
| meta/llama-3.1-8b-instruct | 0.82 | ✅ Good | Fastest |
| meta/llama-3.2-3b-instruct | 0.95 | ✅ Good | Fast |
| openai/gpt-oss-20b | 1.06 | ❌ Error | Failed |
| openai/gpt-oss-120b | 1.42 | ✅ Very Good | **Selected** |
| mistralai/mistral-7b-instruct-v0.3 | 1.49 | ✅ Good | Fast |
| nvidia/nemotron-3-super-120b-a12b | 1.84 | ⚠️ OK | Verbose |
| stepfun-ai/step-3.5-flash | 3.12 | ❌ Error | Failed |
| qwen/qwen3-coder-480b-a35b-instruct | 3.45 | ✅ Very Good | Slow |
| qwen/qwen3-next-80b-a3b-instruct | 5.38 | ✅ Good | Slow |
| meta/llama-3.3-70b-instruct | 7.11 | ✅ Good | Slow |
| deepseek-ai/deepseek-v4-flash | 15.13 | ✅ Good | Very Slow |
| nvidia/llama-3.1-nemotron-nano-8b-v1 | 17.72 | ✅ Good | Very Slow |
| nvidia/llama-3.1-nemotron-ultra-253b-v1 | 0.41 | ❌ Error | Failed |

### Selected Model
**openai/gpt-oss-120b**
- 1.42s response time (7.5x faster than Gemini)
- 100% quality score
- Good balance of speed and quality

### Configuration
**File:** `~/.agentmemory/.env`

**Changes:**
```bash
# Added
OPENAI_API_KEY=<nvidia-nim-key>
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
OPENAI_MODEL=openai/gpt-oss-120b
AGENTMEMORY_LLM_TIMEOUT_MS=120000

# Kept for embeddings
GEMINI_API_KEY=AIzaSy...
```

---

## Phase 7: Verification

### Debug Log Output
After fixes, debug log shows:
```
[2026-05-30T...] provider: openai (openai/gpt-oss-120b) | baseUrl: https://integrate.api.nvidia.com/v1
[2026-05-30T...] projectPath= /home/johnatas/projects directory= /home/johnatas/projects worktree= /
[2026-05-30T...] session.created: startResult context_len= 1770
[2026-05-30T...] system.transform called sid=... activeSessionId=...
[2026-05-30T...] system.transform: pushed AGENTMEMORY_INSTRUCTIONS
[2026-05-30T...] system.transform: using cached context ctx_len=1770
[2026-05-30T...] system.transform: pushed context to output.system
```

### Context Injection Test
- Created memory: "Meu pokémon preferido é o Squirtle"
- Opened new session, asked "Qual é o meu pokémon preferido?"
- Agent responded: "Squirtle. 🐢"
- **Context injection working!**

### Summarize Test
```bash
curl -X POST http://localhost:3111/agentmemory/summarize \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"ses_18c037886ffeuc4c1m74Tjtsvo"}'
```
Result: `qualityScore: 100, success: true`

---

## Files Modified

| File | Changes |
|------|---------|
| `~/.config/opencode/plugins/agentmemory-capture.ts` | Project path fix, debug to file, provider logging |
| `~/.agentmemory/.env` | NVIDIA NIM config, timeout increase |
| `~/.agentmemory/.env.bak` | Backup of original .env |
| `~/projects/.agentmemory-debug.log` | Debug output file |
| `~/projects/recreate_observations.py` | Observation recreation script |

---

## Commands Reference

### Debug Mode
```bash
OPENCODE_AGENTMEMORY_DEBUG=1 opencode
cat ~/projects/.agentmemory-debug.log
```

### Service Management
```bash
systemctl --user status agm
systemctl --user restart agm
journalctl --user -u agm --since "5 min ago"
```

### API Tests
```bash
# Health check
curl -s http://localhost:3111/agentmemory/health

# Context injection
curl -X POST http://localhost:3111/agentmemory/context \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"current","project":"/home/johnatas/projects"}'

# Summarize
curl -X POST http://localhost:3111/agentmemory/summarize \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"ses_18c037886ffeuc4c1m74Tjtsvo"}'
```

---

## Lessons Learned

1. **`ctx.worktree` returns `/` when no worktree exists** — always check for this
2. **OpenCode TUI hides console.error** — use file-based debug logging
3. **GEMINI_API_KEY is required for embeddings** — can't remove it when switching LLM provider
4. **Agentmemory v0.9.22+ has auto-context injection fix** — upgrade was necessary
5. **NVIDIA NIM models vary widely in performance** — test before selecting
6. **step-3.7-flash is a reasoning model** — only outputs `reasoning_content`, not `content`
7. **Data in `stream_store/` persists independently** — cleanup requires explicit deletion

---

## Next Steps

1. Test plugin with new debug logging after OpenCode restart
2. Monitor summarize performance with gpt-oss-120b
3. Verify context injection continues working in new sessions
4. Consider adding more observations for better context injection
