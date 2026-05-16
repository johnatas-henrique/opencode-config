# Plan: Refatorar AGENTS.md Global com Progressive Disclosure

**Data:** 2026-05-04
**Status:** Em progresso

---

## Objetivo

Reduzir o AGENTS.md root de 181 → ~80 linhas, movendo seções específicas para arquivos linked em `docs/agent-instructions/`.

---

## Decisões do Usuário

- Remover Codebase Knowledge Graph (não usa mais)
- Repository Context não carrega globalmente (sem mecanismo), então **remover completamente**
- MCP Tools são gerais, carregar em todos os projetos
- Writing Style mover para linked (já que é detalhado)

---

## Execução

### 1. Editar `AGENTS.md` (root)

**Remover:**
- Linhas 66-76: Repository Context → removido completamente (sem mecanismo para carregar só neste repo)
- Linhas 82-103: Codebase Knowledge Graph → removido (não usa mais)
- Linhas 170-181: Writing Style → mover para linked

**Manter:**
- Header + override note
- Priorities
- Boundaries
- Uncertainty
- Evidence
- Workflow
- MCP Tools (mantém no root, não detalhado)
- Testing
- Change Constraints
- Safety
- Git & PRs
- Completion
- Response Format

---

### 2. Criar `docs/agent-instructions/writing-style.md`

Mover conteúdo das linhas 170-181.

---

### 3. Atualizar `opencode.json`

Adicionar:
```json
{
  "instructions": [
    "~/.config/opencode/AGENTS.md",
    "~/.config/opencode/docs/agent-instructions/writing-style.md"
  ]
}
```

---

## Verificação

- [ ] AGENTS.md root ~80 linhas
- [ ] writing-style.md existe
- [ ] opencode.json atualizado