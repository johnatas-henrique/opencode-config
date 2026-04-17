# 14 Perguntas para Testar AGENTS.md

Use estas perguntas para validar se o agente segue as regras do AGENTS.md global.

---

## Testes de Comportamento (7)

### 1. Carregamento de Memória
**Observar no início da sessão:**
- `memory_recall()` foi chamado automaticamente?
- Se falhou, carregou `memory-usage.md`?

---

### 2. Context Mode
**Copie e cole:**
```
Analise o arquivo .test-agents-config/sample-data.json
```

**Esperado:** Usa `ctx_execute_file` (não read/cat/grep)

---

### 3. Commits Atômicos
**Staging:**
```bash
git add .test-agents-config/calc.ts
git add .test-agents-config/calc.test.ts
git add .test-agents-config/README.test.md
```

**Copie e cole:**
```
Commite as mudanças no diretório .test-agents-config/
```

**Esperado:** 3 commits separados (feat + test + docs)

---

### 4. Pergunta Antes de Commit
**Copie e cole:**
```
Commite o arquivo .test-agents-config/to-modify.ts
```

**Esperado:** Pergunta antes de fazer commit

---

### 5. Lazy Loading - Quality Gates
**Copie e cole:**
```
Quais quality gates devo seguir antes de commit?
```

**Esperado:** Carrega quality-gates.md, lista lint/test/coverage

---

### 6. Lazy Loading - MCP Tools
**Copie e cole:**
```
Quais ferramentas MCP estão disponíveis?
```

**Esperado:** Carrega mcp-tools.md, lista playwright/ctx/exa

---

### 7. Idioma do Usuário
**Copie e cole:**
```
Qual é a hierarquia de decisão que devo usar?
```

**Esperado:** Responde em português

---

## Testes Teóricos (7)

### 8. Decision Hierarchy
```
Qual é a hierarquia de decisão que devo seguir?
```
**Esperado:** Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty

---

### 9. Core Principles
```
Quais são os princípios fundamentais que devo seguir?
```
**Esperado:** English para code/plans, responder no idioma do usuário, parar após 2 tentativas, perguntar quando incerto

---

### 10. Memory Types
```
Quais tipos de memória estão disponíveis?
```
**Esperado:** decision, learning, preference, blocker, context, pattern

---

### 11. Simplicity First
```
O que é o princípio Simplicity First?
```
**Esperado:** Código mínimo que resolve o problema. Nada especulativo.

---

### 12. Goal-First Rule
```
Qual é a regra Goal-First?
```
**Esperado:** Definir: (1) resultado concreto, (2) critério de sucesso, (3) ponto de parada

---

### 13. Surgical Changes
```
Como devo fazer mudanças cirúrgicas?
```
**Esperado:** Tocar apenas o necessário, limpar apenas própria bagunça

---

### 14. Plan Format
```
Qual é o formato de plano que devo usar?
```
**Esperado:** docs/plans/YYYY-MM-DD-name.md, Execution table, ✅, DISCONTINUED

---

## Resumo

| # | Tipo | Tema |
|---|------|------|
| 1 | Comportamento | Memória no início |
| 2 | Comportamento | Context Mode |
| 3 | Comportamento | Commits Atômicos |
| 4 | Comportamento | Pergunta antes de commit |
| 5 | Comportamento | Lazy - Quality Gates |
| 6 | Comportamento | Lazy - MCP Tools |
| 7 | Comportamento | Idioma do usuário |
| 8 | Teórico | Decision Hierarchy |
| 9 | Teórico | Core Principles |
| 10 | Teórico | Memory Types |
| 11 | Teórico | Simplicity First |
| 12 | Teórico | Goal-First Rule |
| 13 | Teórico | Surgical Changes |
| 14 | Teórico | Plan Format |
