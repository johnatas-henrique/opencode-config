# opencode-config

Minhas configurações pessoais para o opencode CLI.

## Conteúdo

- `AGENTS.md` — Instruções globais do agente
- `agents/` — Agentes especializados
- `commands/` — Comandos personalizados
- `rules/` — Regras de lint/format
- `skills/` — Skills personalizadas
- `opencode.json` — Configurações do opencode

## Instalação

```bash
# Clone o repo na pasta desejada
git clone https://github.com/johnatas-henrique/opencode-config.git /tmp/opencode-config

# Execute o script de sincronização
cd /tmp/opencode-config
./sync.sh

# O script irá copiar os arquivos para ~/.config/opencode/
```

## Sincronização

Após fazer alterações nas suas configurações:

```bash
cd ~/.config/opencode
git add .
git commit -m "Descrição das alterações"
git push
```
