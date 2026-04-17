---
name: test-agent
description: Framework to validate if AGENTS.md global configuration is working correctly. Use when user wants to test agent behavior against global rules.
---

# Test Agent Configuration

Validates if the agent follows AGENTS.md rules in any project.

## Setup

Run the config script in the project you want to test:

```bash
~/.config/opencode/skills/test-agent/scripts/test-agents-config.sh
```

This creates:
- `.test-agents-config/` directory with test files
- `.test-agents-report.md` with 14 test questions

## Run Tests

1. Open a new OpenCode session in the same project
2. Follow the questions in `.test-agents-report.md`
3. Mark ✅ or ❌ for each test

## Test Categories

### Behavioral Tests (7)
These require observing agent actions:
- Session start (memory_recall)
- Context mode (ctx tools usage)
- Atomic commits
- Ask before commit
- Lazy loading (quality gates, MCP tools)
- User language response

### Theoretical Tests (7)
These are knowledge questions:
- Memory types and scopes
- Decision hierarchy
- Core principles
- Simplicity first
- Think before coding
- Goal-first rule
- Surgical changes

## Reference

See: `references/14-perguntas.md`

## Cleanup

After testing, run:

```bash
~/.config/opencode/skills/test-agent/scripts/cleanup-test-agents.sh
```
