#!/bin/bash
# Limpa arquivos de teste criados pelo framework

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Limpando arquivos de teste...${NC}"

# Encontrar o diretório do projeto
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

# Remove diretório de teste
if [ -d ".test-agents-config" ]; then
    rm -rf ".test-agents-config"
    echo -e "${GREEN}✓ Removido: .test-agents-config/${NC}"
fi

# Remove relatório
if [ -f ".test-agents-report.md" ]; then
    rm -f ".test-agents-report.md"
    echo -e "${GREEN}✓ Removido: .test-agents-report.md${NC}"
fi

echo ""
echo -e "${GREEN}Limpeza concluída!${NC}"
