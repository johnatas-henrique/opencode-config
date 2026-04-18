# Plan: Add simple-memory rules to global AGENTS.md

| | Created | Updated |
| -- | -- | -- |
| **Status** | completed | 2026-04-14 |
| **Agent** | plan | - |
| **Priority** | high | - |

## Execution

| Timestamp | Step |
| -- | -- |
| 2026-04-14 13:07 | Add Memory Usage section to global AGENTS.md |

## Reason

The user wants to add the 4 memory rules from simple-memory plugin (EXAMPLE_AGENTS.md) to the global AGENTS.md to ensure proper memory usage discipline.

## Rules Added

```markdown
## Memory Usage (simple-memory)

- `memory_recall()` no início de cada sessão e antes de responder perguntas
- **NUNCA** usar `memory_remember()` automaticamente - apenas quando o usuário pedir explicitamente
- Se nova informação contradiz memória existente: perguntar ao usuário antes de usar `memory_forget()` + `memory_remember()`
- **Fim de sessão**: Se padrões, decisões ou aprendizados significativos foram descobertos, perguntar: "Quer que eu lembre [coisa específica]?"
```

## Notes

- These rules ensure the AI uses memory tools correctly
- `memory_recall()` should be called at session start
- `memory_remember()` should only be called when explicitly requested by the user
- The rules were taken from the simple-memory plugin EXAMPLE_AGENTS.md