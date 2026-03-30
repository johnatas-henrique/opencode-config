# Install Caveman Skill (JuliusBrussee/caveman)

**Date:** 2026-04-20  
**Status:** In Progress (installed, awaiting test)  
**Scope:** Install caveman skill for agent response compression (~65-75%) and configure auto-activation

---

## 1. Objective

Integrate **caveman** (JuliusBrussee/caveman skill) into OpenCode to compress agent responses automatically, complementing RTK (bash output) and magic-context (chat compression).

---

## 2. Current Context

| Component   | Status       | Notes                                           |
|-------------|--------------|------------------------------------------------|
| RTK         | ✅ Active     | Compresses bash commands                        |
| magic-context| ✅ Active   | Compresses chat history                         |
| caveman     | ✅ Installed  | Skill at `~/.config/opencode/skills/caveman/`   |
| AGENTS.md   | ✅ Updated    | Caveman rules added (full mode)                |
| OpenCode    | ⏳ Restart?   | Needs restart to load skill?                    |

---

## 3. Decisions Made

| Decision                     | Choice                 | Justification                                          |
|-----------------------------|------------------------|--------------------------------------------------------|
| Installation method          | `npx skills add -g` or manual clone | OpenCode skills use `~/.config/opencode/skills/` dir |
| Default intensity           | **full**               | Aggressive compression (65-75%) — user requested      |
| Activation                  | Always On              | Rules in AGENTS.md active on all responses            |
| caveman-commit commands     | ❌ Not using           | User does not want commit automation                  |
| Languages                   | English (default)      | Skill rules are universal — works in PT too           |

---

## 4. Installation Performed

### Steps executed:

1. ✅ **Install caveman skill**:
   ```bash
   # Recommended (via npx)
   npx skills add -g JuliusBrussee/caveman

   # Or manual (git clone)
   mkdir -p ~/.config/opencode/skills/caveman
   git clone https://github.com/JuliusBrussee/caveman.git ~/.config/opencode/skills/caveman
   ```

2. ✅ **Add rules to AGENTS.md**:
   - Section "Caveman Compression (Always On)"
   - Configured: `Default: full`, `Persistence: ACTIVE EVERY RESPONSE`
   - Full rules: drop articles, filler, pleasantries; fragments OK; pattern `[thing] [action] [reason]`
   - Intensity levels (lite/full/ultra/wenyan-*)
   - Auto-Clarity (exceptions for warnings, destructive ops)
   - Boundaries (code/commits/PRs normal; off: "stop caveman")

3. ✅ **Verify installation** (pending):
   - Restart OpenCode
   - Test `/caveman` command
   - Observe response style

---

## 5. AGENTS.md Configuration (added)

```markdown
## Caveman Compression (Always On)

**Persistence:** ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift. Still active if unsure. Off only: "stop caveman" / "normal mode".

**Default:** **full**. Switch: `/caveman lite|full|ultra`.

### Rules
Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Short synonyms (big not extensive, fix not "implement a solution for"). Technical terms exact. Code blocks unchanged. Errors quoted exact.

Pattern: `[thing] [action] [reason]. [next step].`

### Intensity
| Level | What change |
|-------|------------|
| lite | No filler/hedging. Keep articles + full sentences. |
| full | Drop articles, fragments OK, short synonyms. |
| ultra | Abbreviate, strip conjunctions, arrows (X → Y). |
| wenyan-lite/full/ultra | Classical Chinese variants |

### Auto-Clarity
Drop caveman for: security warnings, irreversible action confirmations, multi-step sequences where fragment order risks misread, user asks to clarify.

### Boundaries
Code/commits/PRs: write normal. "stop caveman": revert. Level persist until session end.
```

---

## 6. Validation (to perform)

| Test | Command/Action | Expected |
|------|----------------|----------|
| 1 | `/caveman` in chat | Response indicating caveman active (full mode) |
| 2 | Simple question | Response in caveman style (no articles, direct) |
| 3 | Request long explanation | Output ~60% smaller than normal |
| 4 | Code blocks | Code unchanged (no compression) |
| 5 | RTK still works | `rtk gain` shows bash command compression |
| 6 | magic-context intact | `/ctx-status` normal |

---

## 7. Useful Caveman Commands

| Command | Purpose |
|---------|---------|
| `/caveman` | Show status or toggle on/off |
| `/caveman lite` | Lighter mode (less aggressive) |
| `/caveman full` | Default mode (aggressive) |
| `/caveman ultra` | Maximum (telegraphic) |
| `stop caveman` | Disable for current session |
| `normal mode` | Return to normal mode |

---

## 8. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Responses too short lose nuances | Medium | Use `/caveman lite` if full too aggressive |
| Conflict with other AGENTS.md rules | Low | Test and adjust section order if needed |
| Skill fails to load automatically | Medium | Restart OpenCode; check `~/.config/opencode/skills/` |

---

## 9. Rollback

```bash
# Remove skill
rm -rf ~/.config/opencode/skills/caveman

# Remove AGENTS.md section (revert edit)

# Restart OpenCode
```

---

## 10. Timeline

| Step | Time | Dependencies |
|------|------|--------------|
| Install skill | 5 min | git, internet |
| Edit AGENTS.md | 5 min | — |
| Restart OpenCode | 2 min | — |
| Initial tests | 15 min | OpenCode running |
| **Total** | **~30 min** | — |

---

## 11. Expected Artifacts

- ✅ `~/.config/opencode/skills/caveman/` (installed skill)
- ✅ `~/.config/opencode/AGENTS.md` (rules added)
- ✅ `docs/plans/2026-04-21-install-caveman-skill.md` (this plan)

---

## 12. Next Steps (after approval)

1. Perform installation (if not already done)
2. Restart OpenCode completely
3. Open new session and test `/caveman`
4. Check compression on a long response
5. Adjust intensity if needed (`lite` vs `full`)

---

**Current status:** Caveman skill cloned to `~/.config/opencode/skills/caveman/` and AGENTS.md updated with **full** rules. Awaiting OpenCode restart and tests in new session.
