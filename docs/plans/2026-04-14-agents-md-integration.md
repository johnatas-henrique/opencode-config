# Plan: AGENTS.md Integration + skillmaxxing + Enterprise Enhancement

**Created:** 2026-04-15 15:30 BRT  
**Context:** Improve OpenCode setup for enterprise use at user's bank

---

## Context

The user works at a bank and wants to raise the quality level of AI-assisted projects. Objectives:

- Avoid "vibe-coding" — quality-less code
- Trust that AI won't create bad code or do stupid things
- Enterprise standards (compliance, audit trail, security)
- Doesn't want mandatory coverage gate (Step 2 — user answered "yes, mandatory")

---

## Pre-Analysis

### Coverage Comparison

| Principle                    | AGENTS.md Current | skillmaxxing | Enterprise | Result     |
| ---------------------------- | :----------------: | :----------: | :--------: | ---------- |
| Atomic commits               |       ✅         |      ❌      |     ❌     | **KEEP**  |
| Mode routing                 |       ❌         |      ✅      |     ❌     | **ADD**   |
| Decision hierarchy           |       ⚠️         |      ✅      |     ❌     | **MERGE** |
| Goal-first                   |       ❌         |      ✅      |     ❌     | **MERGE** |
| Success criteria             |       ⚠️         |      ✅      |     ❌     | **MERGE** |
| Enforcement (lint/type/test) |       ✅         |      ❌      |     ✅     | **ENFORCE** |
| Security compliance          |       ⚠️         |      ❌      |     ✅     | **ADD**   |
| Memory usage                 |       ✅         |      ❌      |     ❌     | **KEEP** |
| Plan format                  |       ✅         |      ❌      |     ❌     | **KEEP** |
| Portuguese response          |       ✅         |      ❌      |     ❌     | **KEEP** |
| Coverage gate (80%)          |       ❌         |      ❌      |     ✅     | **ADD**   |

---

## User Requirements (Captured)

| #   | Requirement                                              | Decision        |
| --- | -------------------------------------------------------- | ---------------|
| 1   | Ticket ID mandatory in commits                             | **NO**         |
| 2   | Coverage gate mandatory (minimum 80%)                     | **YES**        |
| 3   | Conventional commits                                      | **HAS IT** ✅   |
| 4   | Code/plans in EN, agent responds in user's language         | **HAS IT** ✅   |
| 5   | Use Ask Tool for questions to user                     | **ADD**        |

---

## Proposed Structure

```markdown
# OpenCode Agent Instructions

## Skill System (PRIMARY)
@.agents/skills/agent-skills-system/SKILL.md

## Core Principles (Merge - Yours + skillmaxxing)
[Keeps your principles + adds Goal-First + Decision Hierarchy]

## Source Control (Yours - keep)
- Atomic commits
- Conventional commits (current standard)
- Ask before commit
- NEVER push

## Plan Format (Yours - keep)
- Execution table with timestamps
- Explicit success criteria
- File in English

## Quality Gates (MANDATORY)
- lint + typecheck + test BEFORE commit
- Coverage minimum 80%
- Quality chain (hardening → consolidation → slop → commit)

## Security (Enhancement)
- NEVER commit .env, secrets, tokens
- Secret scanning via pre-commit hook

## Communication
- Always use Ask Tool for questions to user
- Respond in user's language
- Code, plans, and documentation in English unless user specifies otherwise

## Context & Memory
[...keep from current...]

## Enterprise Patterns (NEW)
- Error handling structured
- Production logging
- Observability
```

---

## Execution

| Step | Description                                                                        | Timestamp |
| ---- | -------------------------------------------------------------------------------- | --------- |
| 1    | Clone skillmaxxing to `/tmp/skillmaxxing`                                           | -         |
| 2    | Copy `agent-skills-system` to `~/.config/opencode/.agents/skills/agent-skills-system` | -         |
| 3    | Backup current AGENTS.md (`AGENTS.md.backup-YYYYMMDD`)                           | -         |
| 4    | Rewrite AGENTS.md with integrated structure                                        | -         |
| 5    | Add enterprise layer (security, coverage gate)                                     | -         |
| 6    | Validate new setup                                                               | -         |

---

### Step 1: Clone skillmaxxing

```bash
git clone https://github.com/johnvouros/skillmaxxing.git /tmp/skillmaxxing
```

**Verification:**
- directory `/tmp/skillmaxxing` exists
- contains `agent-skills-system/SKILL.md`

---

### Step 2: Copy skill to global config

```bash
cp -R /tmp/skillmaxxing/agent-skills-system ~/.config/opencode/.agents/skills/agent-skills-system
```

**Verification:**
- file `~/.config/opencode/.agents/skills/agent-skills-system/SKILL.md` exists

---

### Step 3: Backup current AGENTS.md

```bash
cp ~/.config/opencode/AGENTS.md ~/.config/opencode/AGENTS.md.backup-$(date +%Y%m%d)
```

**Verification:**
- backup file created with current date

---

### Step 4-5: Rewrite AGENTS.md + Enterprise Patterns

See detailed structure in plan sections above.

---

### Step 6: Validate Setup

```bash
# Verify skillmaxxing installed
ls -la ~/.config/opencode/.agents/skills/agent-skills-system/

# Verify AGENTS.md exists
cat ~/.config/opencode/AGENTS.md | head -20
```

---

## Risks and Mitigations

| Risk                                   | Mitigation                         |
| --------------------------------------- | ---------------------------------- |
| skillmaxxing conflicts with existing rules | Decision hierarchy resolves conflicts |
| Coverage 80% too high for some projects | Allow override via project AGENTS.md |
| Adding too much complexity               | Keep simplicity where possible     |

---

## Final Validation

After implementation, the agent should:

1. ✅ Choose mode (karpathy/rauch/levels/swyx/theo/amjad) at start of each task
2. ✅ Declare "success criteria" before implementing
3. ✅ Use decision hierarchy when conflict arises
4. ✅ Run lint + typecheck + test + coverage BEFORE asking to commit
5. ✅ Ask using Ask Tool
6. ✅ NEVER commit secrets
7. ✅ Keep minimum and typed code

---

## History

| Date       | Description                         |
| ---------- | -----------------------------------|
| 2026-04-15 | Plan created                        |