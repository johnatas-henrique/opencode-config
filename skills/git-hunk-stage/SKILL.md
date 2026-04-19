---
name: git-hunk-stage
description: "Stage apenas partes específicas de um arquivo para um commit, sem afetar outras mudanças não commitadas no mesmo arquivo. Use quando o usuário quer commitar só parte de um arquivo, stakear um hunk específico, commitar só uma função ou bloco, fazer staging parcial, ou separar mudanças em commits diferentes. Triggers: 'commita só parte', 'stage só este hunk', 'commita só a função X', 'separa em commits', 'staging parcial', 'git add -p'."
license: MIT
compatibility: opencode
---

# Git Hunk Stage — Staging Parcial Não-Interativo

## Protocolo para Agentes (sem interatividade)

### Etapa 1: Mapear todos os hunks do arquivo

```bash
git diff <arquivo>
```

Analise cada bloco `@@` e documente:

- Número do hunk (1, 2, 3...)
- Linhas afetadas (ex: linhas 40-48)
- Conteúdo (bugfix? refactor? debug? feature?)
- Decisão: STAGE | SKIP | DISCARD
  Staging Parcial de Hunks para Agentes · pág. 17
  Apresente a tabela ao usuário e aguarde confirmação antes de prosseguir.

### Etapa 2a: Staging por padrão (se o agente conhece o nome da função)

```bash
# Instalar patchutils se necessário
which grepdiff || sudo apt-get install -y patchutils
# Stage todos os hunks que mencionam o nome da função/variável
git diff <arquivo> \
| grepdiff --output-matching=hunk '<NOME_DA_FUNCAO>' \
| git apply --cached
# Verificar o que foi staged
git diff --staged <arquivo>
```

### Etapa 2b: Staging por patch manual (controle total)

```bash
# 1. Extrair o diff completo
git diff <arquivo> > /tmp/full.patch
# 2. AGENTE: criar patch cirúrgico com APENAS o hunk desejado
# Copiar do full.patch apenas o cabeçalho + o hunk alvo
# Garantir que o @@ count está correto
# 3. Dry-run antes de aplicar
git apply --cached --check /tmp/target-hunk.patch
# 4. Aplicar
git apply --cached /tmp/target-hunk.patch
```

### Etapa 3: Verificação obrigatória

```bash
git diff --staged <arquivo> # confirmar o que está staged
Staging Parcial de Hunks para Agentes · pág. 18
git diff <arquivo> # confirmar o que ficou unstaged
```

Apresente os dois diffs ao usuário. Só prossiga ao commit com aprovação.

### Etapa 4: Commit

```bash
git commit -m '<tipo>: <descrição do que foi staged>'
```

## Regras de Segurança

- NUNCA use `git add <arquivo>` (stages o arquivo inteiro)
- NUNCA commite sem mostrar git diff --staged ao usuário primeiro
- SEMPRE faça dry-run (--check) antes de git apply --cached
- Se em dúvida sobre o patch, pergunte ao usuário

## Descarte de Hunks Indesejados

```bash
# Para APAGAR do working tree (não commitar E não manter):
git diff <arquivo> \
| grepdiff --output-matching=hunk '<PADRAO_DO_HUNK>' \
| git apply --reverse
# Verificar
git diff <arquivo> | grep '<PADRAO_DO_HUNK>'
# → sem output: hunk foi apagado do arquivo
```
