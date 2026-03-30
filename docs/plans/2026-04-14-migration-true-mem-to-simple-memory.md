# Plan: Migration from true-mem to simple-memory

| | Created | Updated |
| -- | -- | -- |
| **Status** | completed | 2026-04-14 |
| **Agent** | plan | - |
| **Priority** | high | - |

## Execution

| Timestamp | Step |
| -- | -- |
| 2026-04-14 13:01 | Remove true-mem plugin from opencode.json |
| 2026-04-14 13:01 | Add simple-memory plugin to opencode.json |
| 2026-04-14 13:03 | Restart OpenCode |
| 2026-04-14 13:05 | Create 7 global memories (scope=user) |
| 2026-04-14 13:07 | Verify plugin installation and memory loading |

## Reason

The user wants a simpler memory system. true-mem extracts memories automatically which causes noise. simple-memory requires explicit memory creation, giving the user full control.

## Memories Created (scope=user, type=preference)

| # | Memory |
| -- | -- |
| 1 | "NUNCA fazer commits sem autorização prévia" |
| 2 | "NUNCA fazer git push direto" |
| 3 | "Conventional commits obrigatório" |
| 4 | "Remover comentários do código - código deve se auto-explicar, é anti-pattern" |
| 5 | "Planos com data e hora REIAS, nunca inventar datas ou horários" |
| 6 | "Ao fazer step, adicionar horário REAL do computador para TODOS OS PROJETOS" |
| 7 | "Código mínimo e mais tipado possível (strict: true), para evitar erros e confusões" |

## Verification

After restart, verify:
```bash
ls ~/.opencode/memory/
# Should show logfmt files with memories
```

The plugin provides tools: memory_remember, memory_recall, memory_update, memory_forget, memory_list

## Notes

- simple-memory uses logfmt files in `.opencode/memory/`
- Memories are automatically injected in new sessions
- No daemon or extra dependencies needed