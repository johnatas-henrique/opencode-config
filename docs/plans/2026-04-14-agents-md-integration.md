# Plan: AGENTS.md Integration + skillmaxxing + Enterprise Enhancement

| | Created | Updated |
| -- | -- | -- |
| **Status** | completed | 2026-04-15 |
| **Agent** | plan | - |
| **Priority** | high | - |

## Execution

| Timestamp | Step |
| -- | -- |
| 2026-04-15 15:30 | Plan created |
| 2026-04-15 18:45 | Integrated skillmaxxing, updated AGENTS.md |

## Context

The user works at a bank and wants to raise the quality level of AI-assisted projects. Objectives:

- Avoid "vibe-coding" — quality-less code
- Trust that AI won't create bad code or do stupid things
- Enterprise standards (compliance, audit trail, security)
- Coverage gate mandatory (80%)

## User Requirements

| # | Requirement | Decision |
| -- | -- | -- |
| 1 | Ticket ID mandatory in commits | NO |
| 2 | Coverage gate mandatory (minimum 80%) | YES |
| 3 | Conventional commits | HAS IT ✅ |
| 4 | Code/plans in EN, agent responds in PT | HAS IT ✅ |
| 5 | Use Ask Tool for questions to user | ADD |

## Final AGENTS.md Structure

```markdown
# OpenCode Agent Instructions

## Skill System (PRIMARY)
@.agents/skills/agent-skills-system/SKILL.md

## Core Principles
- English for code/plans, respond in user's language
- FAIL after 2 attempts → stop and report
- ASK when uncertain
- NEVER expose .env, secrets, tokens
- GET web info if unsure

### Decision Hierarchy
Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty

### Goal-First Rule
Define: (1) concrete outcome, (2) success criteria, (3) stopping point

### Think Before Coding
State assumptions, present multiple interpretations, propose simpler approach if exists.

### Simplicity First
Minimum code that solves the problem. Nothing speculative.

### Surgical Changes
Touch only necessary files. Clean own mess only. Never revert changes from other tools.

## Source Control
- Atomic commits: one commit per independent logical change
- NEVER commit without explicit user permission — always ask
- NEVER do git push directly

## Plan Format
- File: docs/plans/YYYY-MM-DD-name.md
- Include Execution table with timestamps
- Update steps to ✅ when done
- All plans in English

## Quality Gates (MANDATORY)
Before commit:
1. lint/format (npm run lint, npm run format)
2. typecheck (npx tsc --noEmit)
3. test (npm test)
4. coverage ≥80%

## Security
- NEVER commit .env, secrets, tokens
- Secret scanning via pre-commit hook

## Communication
- Always use Ask Tool for questions to user
- Respond in user's language
- Code, plans, documentation in English

## Context & Memory
- Use memory_recall() at session start
- Use lean-ctx MCP tools over native equivalents
- Load global memories if none found

## Enterprise Patterns
- Error handling: structured Result types
- Production logging: contextual, JSON
- Observability: metrics + tracing
```

## Notes

- skillmaxxing agent-skills-system cloned to `~/.config/opencode/.agents/skills/agent-skills-system`
- Global memories integrated
- Enterprise layer added (security, coverage gate)