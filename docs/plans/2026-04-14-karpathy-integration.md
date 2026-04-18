# Plan: AGENTS.md Global + karpathy-skills Integration

| | Created | Updated |
| -- | -- | -- |
| **Status** | completed | 2026-04-15 |
| **Agent** | plan | - |
| **Priority** | high | - |

## Execution

| Timestamp | Step |
| -- | -- |
| 2026-04-15 16:00 | Plan created |
| 2026-04-15 18:30 | Updated global AGENTS.md with karpathy principles |

## Pre-Analysis: Redundant Rules

### Rules that EXIST in Global (should be REMOVED from project):

| Project Rule | Global Location | Global Line |
| -- | -- | -- |
| Ask before commit | Source Control > Commit Rules | 63-64 |
| Real timestamps | Plan Format | 88 |
| Never bypass validation | Quality Gates | 114 |
| Plan Mode (4 rules) | Project Rules + Plan Format | 72-73, 77-89 |

### Rules that DON'T exist in Global (should be ADDED):

| Project Rule | Description |
| -- | -- |
| External changes | Never delete/revert external modifications |

## karpathy Principles Added

### Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- If you write 200 lines and it could be 50, rewrite it.

### Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### External Changes Rule

Never delete or revert modifications made by tools other than yourself (e.g., package.json, package-lock.json, generated files). Either ask the user what to do or ignore them.

## Plan Format Updated

```markdown
## Plan Format

- All plans must include an **Execution** table at the top
- Save to `docs/plans/YYYY-MM-DD-name.md` format
- Create execution table when plan is first created
- Update each step to ✅ with real timestamp when finished
- Archive old plans in `archive/YYYY-MM-DD/` directory
- **All plans must be written in English**
```

## Expected Result

Global AGENTS.md consolidates:
- ✅ Decision Hierarchy (unique)
- ✅ Goal-First Rule (yours, complete)
- ✅ Think Before Coding (karpathy)
- ✅ Simplicity First (karpathy)
- ✅ Surgical Changes (karpathy)
- ✅ External Changes (from project)
- ✅ Plan Format updated to docs/plans/YYYY-MM-DD-name.md
- ✅ Quality Gates (80%)
- ✅ Enterprise Patterns
- ✅ Memory usage rules

Project AGENTS.md keeps only project-specific commands, files, guidelines.