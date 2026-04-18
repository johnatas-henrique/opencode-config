# Manifest Build Integration

## Visão geral
O **Manifest Build** (`https://app.manifest.build/`) é um roteador de LLM que escolhe dinamicamente o modelo mais barato que consegue atender à tarefa.  Ele funciona como um provedor **OpenAI‑compatible**, portanto pode ser usado como qualquer outro modelo configurado em `opencode.json`.

## Configuração necessária
1. **Variável de ambiente**
   ```bash
   export MANIFEST_API_KEY=mnfst_SEU_TOKEN_AQUI
   ```
   A variável deve estar disponível no ambiente onde o OpenCode é executado.

2. **Provider em `opencode.json`**
   ```json
   "manifest": {
     "npm": "@ai-sdk/openai-compatible",
     "name": "Manifest Build",
     "options": {
       "baseURL": "https://app.manifest.build/v1",
       "apiKey": "{env:MANIFEST_API_KEY}"
     },
     "models": {
       "auto": {
         "id": "auto",
         "name": "Manifest Auto (Roteado)",
         "limit": {
           "context": 2000000,
           "output": 120000
         }
       }
     }
   }
   ```
   O limite de **contexto** foi definido para **2 000 000** tokens, permitindo que o Manifest roteie para qualquer modelo, inclusive aqueles com janelas de contexto de 1 M+ tokens.

## Como usar
- Defina o modelo padrão do agente para o Manifest:
  ```bash
  openclaw config set agents.defaults.model.primary manifest/auto
  ```
- O Manifest escolherá o modelo apropriado por tier (simple, standard, complex, reasoning) e por especialidade (coding, web‑browsing, etc.).
- Cada resposta inclui cabeçalhos úteis:
  - `X-Manifest-Model` – modelo real que atendeu à requisição
  - `X-Manifest-Tier` – tier de complexidade atribuído
  - `X-Manifest-Specificity` – categoria detectada (coding, data‑analysis…)

## Fallbacks e segurança de contexto
O Manifest **não** verifica o tamanho do prompt antes de rotear. Caso um modelo com janela menor receba um prompt que exceda seu limite, ele retornará erro **"context window exceeded"** e o Manifest tentará o próximo fallback configurado para o tier.

**Recomendações**
1. No dashboard do Manifest, configure *fallbacks* para cada tier com modelos que tenham janelas de contexto adequadas ao seu uso típico.
2. Monitore os cabeçalhos `X-Manifest-Model` nas respostas para validar se o fallback está sendo acionado.
3. Caso observe muitos erros de excesso de contexto, reduza o limite em `opencode.json` (ex.: 500 000) ou ajuste os fallbacks.

## Referências
- Documentação oficial: https://manifest.build/docs
- Discussão sobre limites de contexto: https://github.com/mnfst/manifest/discussions/1450

---
*Esta página foi criada automaticamente por OpenCode ao integrar o Manifest Build.*
