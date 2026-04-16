# Plan: ctx-mode + DCP + squeez Integration

| | Created | Updated |
| ----------- | --------- | ---------
| **Status** | IN PROGRESS | 2026-04-15 22:10
| **Agent** | plan | -
| **Priority** | high | -

## Execution

| Timestamp | Step |
| --------- | -----
| 2026-04-15 22:00 | Created comparison plan
| 2026-04-15 22:10 | Added integration details

---

## Context

User wants to understand how the three systems work together:
1. **ctx-mode** - Already installed and active
2. **DCP** - Not installed
3. **squeez** - Already installed (0.3.1)

---

## How Each System Works

### 1. ctx-mode (Data Layer)

| Aspect | Details |
|--------|---------|
| **What it does** | Processes read/search/analyze in sandbox, only summary enters context |
| **When** | On any file read, grep, ls, search operations |
| **How** | Hook intercepts tools, runs code in subprocess, returns only answer |
| **You can force** | Use ctx_execute, ctx_execute_file, ctx_search instead of read/cat/grep |
| **Current performance** | 67.7% reduction in this session |

**Tools to use:**
- `ctx_execute` - Run commands + process data
- `ctx_execute_file` - Read file + analyze in sandbox
- `ctx_search` - Search indexed content
- `ctx_fetch_and_index` - Fetch URL + index for search
- `ctx_batch_execute` - Multiple commands + queries

### 2. DCP (Conversation Layer)

| Aspect | Details |
|--------|---------|
| **What it does** | Prunes conversation history before sending to LLM |
| **When** | Before each LLM request |
| **How** | Uses 3 automatic strategies + LLM tools (discard, extract) |
| **Requires** | Plugin in opencode.jsonc |

**Strategies (zero LLM cost):**
- **deduplication** - Remove identical tool calls (keeps latest)
- **supersedeWrites** - Remove write when same file is later read
- **purgeErrors** - Remove old error inputs after X turns

### 3. squeez (LLM Output Layer)

| Aspect | Details |
|--------|---------|
| **What it does** | Compresses LLM output to reduce context |
| **When** | Can be used as filter or benchmark |
| **How** | CLI tool for text compression |
| **Current version** | 0.3.1 |

**Usage:**
- `squeez filter <hint>` - Compress stdin
- `squeez benchmark` - Test compression quality
- `squeez wrap <command>` - Wrap command output

---

## How They Work Together

```
┌─────────────────────────────────────────────────────────┐
│                    USER REQUEST                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 1. ctx-mode (Data Layer)                                │
│    - read/grep/ls → sandbox → summary only              │
│    - REDUCES: Tool outputs that flood context           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 2. DCP (Conversation Layer)                             │
│    - deduplication, supersedeWrites, purgeErrors        │
│    - REDUCES: Chat history (message history)            │
│    - Tools: discard, extract for LLM to manage context  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 3. LLM receives optimized context                      │
└─────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 4. squeez (Output Layer - optional)                     │
│    - Can wrap commands to compress output               │
│    - REDUCES: Command output                            │
└─────────────────────────────────────────────────────────┘
```

**Token savings estimate:**
- ctx-mode: ~60-70% on data operations
- DCP: ~30-50% on conversation history
- squeez: ~60-70% on command output

**Combined potential:** Up to 80-90% reduction in total token usage

---

## Installation Plan

### Step 1: Install DCP Plugin

Add to `~/.config/opencode/opencode.jsonc`:

```jsonc
{
    "plugin": ["@tarquinen/opencode-dcp@latest"]
}
```

**Location:** Check if file exists at `~/.config/opencode/opencode.jsonc`

### Step 2: Configure DCP (Optional)

Create `~/.config/opencode/dcp.jsonc`:

```jsonc
{
    "enabled": true,
    "strategies": {
        "deduplication": { "enabled": true },
        "supersedeWrites": { "enabled": false },
        "purgeErrors": { "enabled": true, "turns": 4 }
    }
}
```

### Step 3: Restart OpenCode

### Step 4: Monitor with `ctx status`

---

## Decision Required

| Question | Answer |
| -------- | -------
| Install DCP? | Pending user approval |
| Which strategies enable? | Default recommended |
| Use squeez with which commands? | TBD |

---

## Next Steps

- [ ] Decision: Install DCP?
- [ ] Check opencode.jsonc location
- [ ] Install DCP if approved
- [ ] Configure DCP (optional)
- [ ] Restart OpenCode
- [ ] Benchmark combined performance