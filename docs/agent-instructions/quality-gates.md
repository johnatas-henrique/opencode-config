# Quality Gates

<!-- [QUALITY] MANDATORY - BEFORE COMMIT -->
FAIL: If any gate fails, STOP and report
MINIMUM: 80% coverage required
<!-- [/QUALITY] -->

---

## Gates

| Gate | Command |
|------|---------|
| Lint | `npm run lint` or `ruff check . --fix` |
| Format | `npm run format` or `ruff format .` |
| Types | `npx tsc --noEmit` or `mypy .` |
| Tests | `npm test` or `pytest` |
| Coverage | 80% minimum |

---

## Workflow

1. Run all gates
2. If any fail → STOP → report to user
3. If all pass → proceed to commit

---

## Chain (optional)

```
Follow: workflows/finalize-01-hardening.md → 02-consolidation.md → 03-slop.md → 04-commit.md
```
