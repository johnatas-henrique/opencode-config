#!/bin/bash
# Cleanup test files created by the framework

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Cleaning test files...${NC}"

# Find project directory
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

# Remove test directory
if [ -d ".test-agents-config" ]; then
    rm -rf ".test-agents-config"
    echo -e "${GREEN}✓ Removed: .test-agents-config/${NC}"
fi

# Remove report
if [ -f ".test-agents-report.md" ]; then
    rm -f ".test-agents-report.md"
    echo -e "${GREEN}✓ Removed: .test-agents-report.md${NC}"
fi

echo ""
echo -e "${GREEN}Cleanup complete!${NC}"
