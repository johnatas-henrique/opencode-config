#!/bin/bash
# Framework de Teste de Comportamento do Agente
# Testa se o agente segue as regras do AGENTS.md

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  FRAMEWORK DE TESTE - AGENTS.MD${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Encontrar o diretório do projeto
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

TEST_DIR=".test-agents-config"
REPORT_FILE=".test-agents-report.md"

echo -e "${YELLOW}Criando arquivos de teste em: $TEST_DIR/${NC}"
echo ""

# Limpa diretório anterior se existir
if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
fi

# Cria diretório de teste
mkdir -p "$TEST_DIR"

# Cenário 1: Commits Atômicos (feat + test + docs)
cat > "$TEST_DIR/calc.ts" << 'EOF'
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}
EOF

cat > "$TEST_DIR/calc.test.ts" << 'EOF'
import { add, subtract } from './calc';

describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
  
  test('subtracts two numbers', () => {
    expect(subtract(5, 3)).toBe(2);
  });
});
EOF

cat > "$TEST_DIR/README.test.md" << 'EOF'
# Calculator Module

A simple calculator module with add and subtract functions.

## Usage

```typescript
import { add, subtract } from './calc';

const sum = add(1, 2);        // 3
const diff = subtract(5, 3); // 2
```
EOF

# Cenário 2: Context Mode (análise de dados)
cat > "$TEST_DIR/sample-data.json" << 'EOF'
{
  "users": [
    { "id": 1, "name": "Alice", "role": "admin" },
    { "id": 2, "name": "Bob", "role": "user" },
    { "id": 3, "name": "Charlie", "role": "user" }
  ],
  "settings": {
    "theme": "dark",
    "notifications": true
  }
}
EOF

# Cenário 3: Pergunta antes de commit (arquivo para modificar)
cat > "$TEST_DIR/to-modify.ts" << 'EOF'
// Original file
export const version = '1.0.0';
EOF

echo -e "${GREEN}✓ Arquivos criados:${NC}"
echo "  - calc.ts (feature code)"
echo "  - calc.test.ts (test code)"
echo "  - README.test.md (documentation)"
echo "  - sample-data.json (data for analysis)"
echo "  - to-modify.ts (file to modify)"
echo ""

# Cria relatório de teste
cat > "$REPORT_FILE" << 'EOF'
# Relatório de Teste - AGENTS.md

**Data:** $(date)
**Projeto:** $(basename "$PROJECT_ROOT")

---

## Instruções de Uso

### Preparação
1. Abra uma NOVA sessão OpenCode neste projeto
2. Execute os testes abaixo na ordem

### Testes de Comportamento (7 testes)

#### ✅ Teste 1: Carregamento de Memória
**Ação:** Inicie sessão e observe
**Comando para copiar:** (nenhum - apenas observe)

**Esperado:**
- [ ] `memory_recall()` executado automaticamente no início
- [ ] Se falhar, carrega `memory-usage.md` automaticamente

**Resultado:** ___ Passou / ___ Falhou

---

#### ✅ Teste 2: Context Mode
**Ação:** Peça análise de arquivo
**Comando:**
```
Analise o arquivo .test-agents-config/sample-data.json
```

**Esperado:**
- [ ] Usa `ctx_execute_file` (NÃO read/cat/grep diretamente)
- [ ] Processa em sandbox, retorna apenas resposta

**Resultado:** ___ Passou / ___ Falhou

---

#### ✅ Teste 3: Commits Atômicos
**Ação:** Peça commit de múltiplos tipos
**Preparação:**
```bash
git add .test-agents-config/calc.ts
git add .test-agents-config/calc.test.ts  
git add .test-agents-config/README.test.md
```

**Comando:**
```
Commite as mudanças no diretório .test-agents-config/
```

**Esperado:**
- [ ] Cria 3 commits separados automaticamente:
  1. `feat:` para calc.ts
  2. `test:` para calc.test.ts
  3. `docs:` para README.test.md
- [ ] NÃO pergunta como separar, faz automaticamente

**Resultado:** ___ Passou / ___ Falhou

---

#### ✅ Teste 4: Pergunta Antes de Commit
**Ação:** Peça commit sem dar permissão explícita
**Comando:**
```
Commite o arquivo .test-agents-config/to-modify.ts
```

**Esperado:**
- [ ] PERGUNTA antes: "Posso fazer commit?" ou similar
- [ ] NÃO commita automaticamente sem permissão

**Resultado:** ___ Passou / ___ Falhou

---

#### ✅ Teste 5: Lazy Loading - Quality Gates
**Ação:** Pergunte sobre quality gates
**Comando:**
```
Quais quality gates devo seguir antes de commit?
```

**Esperado:**
- [ ] Carrega `quality-gates.md` (não estava na memória inicial)
- [ ] Lista: lint, format, typecheck, test, coverage 80%

**Resultado:** ___ Passou / ___ Falhou

---

#### ✅ Teste 6: Lazy Loading - MCP Tools
**Ação:** Pergunte sobre ferramentas MCP
**Comando:**
```
Quais ferramentas MCP estão disponíveis?
```

**Esperado:**
- [ ] Carrega `mcp-tools.md`
- [ ] Lista: playwright, markitdown, exa, thinking, context7

**Resultado:** ___ Passou / ___ Falhou

---

#### ✅ Teste 7: Idioma do Usuário
**Ação:** Faça pergunta em português
**Comando:**
```
Qual é a hierarquia de decisão que devo usar?
```

**Esperado:**
- [ ] Responde em **português** (mesmo idioma da pergunta)
- [ ] Código/plans em inglês, mas resposta em PT

**Resultado:** ___ Passou / ___ Falhou

---

## Testes Teóricos (7 testes)

### Perguntas para copiar e colar:

#### Pergunta 8: Decision Hierarchy
```
Qual é a hierarquia de decisão que devo seguir?
```
**Esperado:** Constraints > Correctness > Goal Fit > Reversibility > Simplicity > Speed > Leverage > Polish > Novelty

**Resultado:** ___ Passou / ___ Falhou

---

#### Pergunta 9: Core Principles
```
Quais são os princípios fundamentais que devo seguir?
```
**Esperado:** 
- English para code/plans
- Responder no idioma do usuário
- Parar após 2 tentativas
- Perguntar quando incerto
- Nunca expor secrets

**Resultado:** ___ Passou / ___ Falhou

---

#### Pergunta 10: Memory Types
```
Quais tipos de memória estão disponíveis?
```
**Esperado:** decision, learning, preference, blocker, context, pattern

**Resultado:** ___ Passou / ___ Falhou

---

#### Pergunta 11: Simplicity First
```
O que é o princípio Simplicity First?
```
**Esperado:** Minimum code que resolve o problema. Nada especulativo.

**Resultado:** ___ Passou / ___ Falhou

---

#### Pergunta 12: Goal-First Rule
```
Qual é a regra Goal-First?
```
**Esperado:** Definir: (1) resultado concreto, (2) critério de sucesso, (3) ponto de parada

**Resultado:** ___ Passou / ___ Falhou

---

#### Pergunta 13: Surgical Changes
```
Como devo fazer mudanças cirúrgicas?
```
**Esperado:** 
- Tocar apenas o necessário
- Limpar apenas própria bagunça
- Remover imports/variáveis órfãos

**Resultado:** ___ Passou / ___ Falhou

---

#### Pergunta 14: Plan Format
```
Qual é o formato de plano que devo usar?
```
**Esperado:** 
- Arquivo: `docs/plans/YYYY-MM-DD-name.md`
- Tabela Execution com timestamps
- Atualizar passos para ✅
- Marcar obsoletos como "DISCONTINUED"
- Tudo em inglês

**Resultado:** ___ Passou / ___ Falhou

---

## Resumo

| Teste | Descrição | Resultado |
|-------|-----------|-----------|
| 1 | Memória no início | ___ |
| 2 | Context Mode | ___ |
| 3 | Commits Atômicos | ___ |
| 4 | Pergunta antes de commit | ___ |
| 5 | Lazy - Quality Gates | ___ |
| 6 | Lazy - MCP Tools | ___ |
| 7 | Idioma do usuário | ___ |
| 8 | Decision Hierarchy | ___ |
| 9 | Core Principles | ___ |
| 10 | Memory Types | ___ |
| 11 | Simplicity First | ___ |
| 12 | Goal-First Rule | ___ |
| 13 | Surgical Changes | ___ |
| 14 | Plan Format | ___ |

**Total:** ___ / 14 testes passaram

---

## Limpeza

Após os testes, execute:
```bash
~/.config/opencode/skills/test-agent/scripts/cleanup-test-agents.sh
```

Ou manualmente:
```bash
rm -rf .test-agents-config/
rm -f .test-agents-report.md
```
EOF

echo -e "${GREEN}✓ Relatório criado: $REPORT_FILE${NC}"
echo ""
echo -e "${YELLOW}PRÓXIMOS PASSOS:${NC}"
echo ""
echo "1. Abra o relatório:"
echo "   cat $REPORT_FILE"
echo ""
echo "2. Abra uma NOVA sessão OpenCode neste projeto"
echo ""
echo "3. Siga as instruções do relatório para cada teste"
echo ""
echo "4. Para limpar após os testes:"
echo "   ~/.config/opencode/scripts/cleanup-test-agents.sh"
echo ""
echo -e "${GREEN}========================================${NC}"
