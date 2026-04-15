# Migration: true-mem to simple-memory

**Date:** 2026-04-14 13:01  
**Status:** in_progress

## Reason

The user wants a simpler memory system. true-mem extracts memories automatically which causes noise. simple-memory requires explicit memory creation, giving the user full control.

## Execution

| Step                                         | Status | Timestamp        |
| -------------------------------------------- | ------ | ---------------- |
| 1. Remove true-mem from opencode.json        | ✅     | 2026-04-14 13:01 |
| 2. Add simple-memory plugin to opencode.json | ✅     | 2026-04-14 13:01 |
| 3. Restart OpenCode                          | ✅     | 2026-04-14 13:03 |
| 4. Create 7 global memories (scope=user)     | ⏳     | -                |
| 5. Verify plugin is working                  | ⏳     | -                |

## Memories to Create

All 7 memories will be stored with:

- **scope:** user (global - works for all projects)
- **type:** preference

| #   | Memory                                                                               | Type       |
| --- | ------------------------------------------------------------------------------------ | ---------- |
| 1   | "NUNCA fazer commits sem autorização prévia"                                         | preference |
| 2   | "NUNCA fazer git push direto"                                                        | preference |
| 3   | "Conventional commits obrigatório"                                                   | preference |
| 4   | "Remover comentários do código - código deve se auto-explicar, é anti-pattern"       | preference |
| 5   | "Planos com data e hora REAIS, nunca inventar datas ou horários"                     | preference |
| 6   | "Ao fazer step, adicionar horário REAL do computador para TODOS OS PROJETOS"         | preference |
| 7   | "Código mínimo e mais tipado possível (strict: true), para evitar erros e confusões" | preference |

## Notes

- simple-memory uses logfmt files in `.opencode/memory/`
- Memories are automatically injected in new sessions
- The plugin provides tools: memory_remember, memory_recall, memory_update, memory_forget, memory_list
- No daemon or extra dependencies needed
