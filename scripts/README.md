# Scripts de Benchmark e Gerenciamento de Modelos

Scripts para gerenciar scores de benchmarks e configurar providers no OpenCode.

## 📜 Scripts Disponíveis

### `fetch-benchmark-scores.py`

Busca scores de benchmarks (SWE-bench Lite, SWE-bench Verified, LiveCodeBench, Aider) para todos os modelos configurados no `opencode.json`.

#### Como usar:

```bash
# Primeira vez (ou após adicionar novos modelos no opencode.json)
python3 scripts/fetch-benchmark-scores.py

# Depois, rode novamente a qualquer momento para atualizar
# O script só buscará modelos novos (cache incremental)
```

#### O que gera:

- `docs/model-benchmarks/scores.md` - Tabela combinada com todos os modelos e scores
- `docs/model-benchmarks/scores-lite.md` - Apenas SWE-bench Lite (mini-swe-agent v2) - **comparável entre modelos**
- `docs/model-benchmarks/scores-verified.md` - Apenas SWE-bench Verified
- `docs/model-benchmarks/.scores-cache.json` - Cache incremental

#### Como adicionar scores manualmente:

Edite `scripts/fetch-benchmark-scores.py` e adicione entradas nos dicionários `SWE_LITE_SCORES` e `SWE_VERIFIED_SCORES`. Use IDs normalizados (sem espaços, lowercase).

---

### `verify-provider.py`

Testa um provider grouter em uma porta específica, verificando quais modelos estão funcionando.

#### Como usar:

```bash
# Teste o provider na porta 3109
python3 scripts/verify-provider.py 3109 --api-key grouter

# Com prompt customizado
python3 scripts/verify-provider.py 3102 --api-key grouter --prompt "Write Python hello world"

# Especificando diretório de saída
python3 scripts/verify-provider.py 3109 --output-dir ./test-results
```

#### Detecção automática de nome:

O script lê o endpoint `/v1/models` e extrai o campo `owned_by` do primeiro modelo para nomear os arquivos de saída. Por exemplo, se `owned_by = "modal"`, os arquivos serão `modal-ok.json`, `modal-fail.json`.

Se não conseguir detectar, usa `localhost{port}` como fallback.

#### O que gera:

- `{provider-name}-ok.json` - modelos que responderam com sucesso
- `{provider-name}-fail.json` - modelos que falharam
- `{provider-name}-ok.txt` - versão legível
- `{provider-name}-fail.txt` - versão legível

#### Funcionalidades:

- Testa `/v1/models` para listar modelos disponíveis
- Testa cada modelo com POST `/v1/chat/completions` usando prompt simples
- **Retry até 3x** para modelos que falham na primeira tentativa
- Usa `max_tokens=10` para respostas curtas e rápidas
- **Detecta automaticamente** o nome do provider via `owned_by`

---

### `generate-provider-config.py`

Gera a configuração do provider para o `opencode.json` a partir dos resultados do `verify-provider.py`.

#### Como usar:

```bash
# Gere a config a partir dos resultados de verificação
python3 scripts/generate-provider-config.py "GRouter OpenRouter-ok.json"

# Com arquivo de overrides para preencher modalities/limit
python3 scripts/generate-provider-config.py "GRouter OpenRouter-ok.json" --overrides model-overrides.json

# Especificando diretório de saída
python3 scripts/generate-provider-config.py "GRouter-OpenRouter-ok.json" --output-dir ./configs
```

#### O que gera:

- `provider-{provider}-config.json` - objeto JSON pronto para colar em `opencode.json` under `"provider"`

#### Arquivo de Overrides (`model-overrides.json`):

Como o endpoint `/v1/models` do grouter não retorna `modalities` nem `limit`, você pode fornecer esses dados manualmente:

```json
{
  "zai-org/glm-5-fp8-2": {
    "modalities": {
      "input": ["text"],
      "output": ["text"]
    },
    "limit": {
      "context": 131072,
      "output": 8192
    }
  }
}
```

- As chaves são model IDs (case-insensitive)
- Os valores são mesclados com a config gerada
- Execute o script e depois adicione novos overrides conforme necessário

#### Funcionalidades:

- Agrupa modelos por `owned_by` (cada owner vira uma provider separada: `grouter-{owner}`)
- Aplica overrides de `modalities` e `limit` automaticamente
- Inclui **todos os modelos** (trabalhando e falhando) — você decide depois quais manter

---

## 📊 Interpretação dos Scores de Benchmark

### SWE-bench Lite (Recomendado para comparação)

- **Protocolo**: mini-swe-agent v2 (mesmo código para todos)
- **Dataset**: 300 issues reais do GitHub
- **Comparabilidade**: ✅ **Excelente** - scores diretamente comparáveis entre modelos
- **Exemplo**: Claude Opus 4.5 tem 76.8%, GPT-5.2 Codex tem 72.8%

### SWE-bench Verified

- **Protocolo**: Cada vendor pode otimizar scaffold próprio
- **Dataset**: 500 issues reais
- **Comparabilidade**: ❌ **Ruim** - scores otimizados não são justos para comparação
- **Uso**: Ver máximo potencial que um modelo ALCANÇA (mas não comparar)

### LiveCodeBench

- Problemas de competição (LeetCode/Codeforces)
- Mede raciocínio lógico, não coding agentic real
- Correlaciona-se mal com SWE-bench

### Aider

- Edição de arquivos únicos em múltiplas linguagens
- Mede capacidade de seguir instruções de refatoração
- Não testa debugging multi-file

---

## 🔄 Workflow Completo

### 1. Adicione um novo provider grouter

```bash
# Teste a porta do provider
python3 scripts/verify-provider.py 3109 --api-key grouter --name "OpenRouter"

# Gere a configuração (com overrides se necessário)
python3 scripts/generate-provider-config.py "GRouter OpenRouter-ok.json" --overrides model-overrides.json

# Copie o conteúdo de provider-*.json para opencode.json na seção "provider"
```

### 2. Atualize scores de benchmarks

```bash
# Após adicionar modelos no opencode.json
python3 scripts/fetch-benchmark-scores.py

# Os arquivos markdown são atualizados automaticamente
```

---

## 🐛 Troubleshooting

### `generate-provider-config` não preenche modalities/limit

O endpoint `/v1/models` do provider pode não retornar essas informações. Use `--overrides model-overrides.json` para adicionar manualmente. Veja exemplo acima.

### Modelo aparece duas vezes na config gerada

Isso pode acontecer se houver múltiplas entradas no results JSON. O script agrupa por `owned_by`, mas se o mesmo `owned_by` aparecer com nomes diferentes (ex: "Modal" vs "modal"), serão providers separados. Normalize o `--name` ao rodar `verify-provider.py`.

### Scores não aparecem na tabela after adicionar modelos

Verifique se o `model_id` no `opencode.json` corresponde a uma chave nos dicionários de scores. O script usa normalização (lowercase, remove sufixos). Adicione entradas manuais em `SWE_LITE_SCORES`/`SWE_VERIFIED_SCORES` se necessário.

---

## 📁 Estrutura de Arquivos

```
~/.config/opencode/
├── opencode.json                    # Config principal
├── scripts/
│   ├── fetch-benchmark-scores.py
│   ├── verify-provider.py
│   ├── generate-provider-config.py
│   ├── README.md                    # Este arquivo
│   └── model-overrides.json         # Overrides manuais (crie se precisar)
├── docs/
│   └── model-benchmarks/
│       ├── scores.md
│       ├── scores-lite.md
│       ├── scores-verified.md
│       └── .scores-cache.json
└── provider-*-config.json           # Gerado pelo generate-provider-config.py
```

---

## 🎯 Notas Importantes

- Os scripts **não acessam APIs externas** (exceto durante verificação de provider). Scores são dados locais.
- `fetch-benchmark-scores.py` usa cache incremental para não perder dados ao adicionar modelos
- `verify-provider.py` testa cada modelo até 3x antes de marcar como falha
- Para questions sobre benchmarks, consulte as fontes oficiais (SWE-bench, LiveCodeBench, Aider)

---

**Última atualização:** 2026-04-21
