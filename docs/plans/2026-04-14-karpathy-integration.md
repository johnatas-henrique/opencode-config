# Plan: AGENTS.md Global + karpathy-skills Integration

**Created:** 2026-04-15  
**Context:** Organize global AGENTS.md, integrate karpathy-skills, and consolidate project rules

---

## Pre-Analysis: Redundant Rules

### Rules that EXIST in Global (should be REMOVED from project):

| Project Rule         | Global Location                      | Global Line |
| -------------------- | ----------------------------------- | ------------ |
| Ask before commit    | Source Control > Commit Rules       | 63-64        |
| Real timestamps     | Plan Format                        | 88           |
| Never bypass validation | Quality Gates                    | 114          |
| Plan Mode (4 rules) | Project Rules + Plan Format          | 72-73, 77-89 |

### Rules that DON'T exist in Global (should be ADDED):

| Project Rule    | Description                              |
| --------------- | ---------------------------------------- |
| External changes | Never delete/revert external modifications |

---

## Execution

| Step | Description                                                            | Status |
| ---- | ---------------------------------------------------------------------- | ------ |
| 1    | Remove line 4 (invalid @.agents/skills reference)                        | ⏳     |
| 2    | Add Think Before Coding (karpathy)                                       | ⏳     |
| 3    | Add Simplicity First (karpathy)                                      | ⏳     |
| 4    | Add Surgical Changes (karpathy)                                      | ⏳     |
| 5    | Add "External changes" rule (from project)                              | ⏳     |
| 6    | Update Plan Format to docs/plans/YYYY-MM-DD-name.md                 | ⏳     |
| 7    | Clean redundant rules from project                                     | ⏳     |
| 8    | Verify and clean other invalid references                              | ⏳     |

---

## Step Details

### Step 1: Remove Invalid Reference

Remove line 4:
```
@.agents/skills/agent-skills-system/SKILL.md
```

### Step 2-4: Add karpathy-skills (3 principles)

```markdown
### Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
```

```markdown
### Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- If you write 200 lines and it could be 50, rewrite it.
```

```markdown
### Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.
```

### Step 5: Add "External Changes" Rule

Add to Core Principles:

```markdown
### External Changes

Never delete or revert modifications made by tools other than yourself (e.g., package.json, package-lock.json, generated files). Either ask the user what to do or ignore them.
```

### Step 6: Update Plan Format

Update to specific format:

```markdown
## Plan Format

- All plans must include an **Execution** table at the top
- Save to `docs/plans/YYYY-MM-DD-name.md` format
- Create execution table when plan is first created
- Update each step to ✅ with real timestamp when finished
- Archive old plans in `archive/YYYY-MM-DD/` directory
- **All plans must be written in English**
```

### Step 7: Clean Redundant Rules from Project

Remove from project AGENTS.md (`/home/johnatas/projects/opencode-hooks/AGENTS.md`):

Lines to remove:
- Line 43: "Ask before commit" (exists in global)
- Line 44: "Real timestamps" (exists in global)
- Line 45: "Never bypass validation" (exists in global)
- Lines 34-40: "Plan Mode" (exists in global, but with different format)

### Step 8: Verify References

Verify other invalid references.

---

## Expected Result

### Global AGENTS.md will have:
- ✅ Decision Hierarchy (unique)
- ✅ Goal-First Rule (yours, complete)
- ✅ Think Before Coding (NEW - karpathy)
- ✅ Simplicity First (NEW - karpathy)
- ✅ Surgical Changes (NEW - karpathy)
- ✅ External Changes (NEW - from project)
- ✅ Plan Format updated to docs/plans/YYYY-MM-DD-name.md
- ✅ Quality Gates (80%)
- ✅ Enterprise Patterns
- ✅ Your existing rules

### Project AGENTS.md will have:
- ✅ Commands (npm run build, etc)
- ✅ Important Files (specific files)
- ✅ Guidelines (links to docs)
- ✅ Release (Release Please)
- ✅ Reference to global (@~/.config/opencode/AGENTS.md)

---

## History

| Date       | Description                         |
| ---------- | ----------------------------------- |
| 2026-04-15 | Plan created/updated                |