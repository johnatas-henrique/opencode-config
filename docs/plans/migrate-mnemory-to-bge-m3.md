# Plano de migração: nemotron-embed-1b-v2 → baai/bge-m3

## Motivação

O modelo atual (`nvidia/llama-nemotron-embed-1b-v2`) é **assimétrico** — requer `input_type` diferente para queries vs passages. O monkey-patch no `mnemory-nim.sh` força `input_type: 'passage'` em todas as chamadas, incluindo queries de busca, o que degrada o recall. O `baai/bge-m3` é **simétrico** (mesma função para query e passage), multilíngue (100+ idiomas), e não precisa de patch.

## Arquivo alvo

`~/.config/opencode/scripts/mnemory-nim.sh`

## Mudanças

### 1. Variáveis de ambiente (linhas 11-12)

```diff
- export EMBED_MODEL="nvidia/llama-nemotron-embed-1b-v2"
- export EMBED_DIMS=1536
+ export EMBED_MODEL="baai/bge-m3"
+ export EMBED_DIMS=1024
```

### 2. Remover Patch 1 (linhas 24-26)

```diff
- # Patch 1: inject input_type for NIM asymmetric models
- orig = e.Embeddings.create
- e.Embeddings.create = lambda self, **kw: orig(self, **kw, extra_body={**kw.get('extra_body', {}), 'input_type': 'passage'})
```

### 3. Patches 2-4 (MANDATORY INSTRUCTIONS, CORE_TOP_MEMORIES=0)

Inalterados. Não têm relação com embedding.

## Re-embedding

Após restart com o novo modelo, os vetores existentes no Qdrant (1536d, nemotron) são incompatíveis com o novo espaço (1024d, bge-m3). O mnemory detecta a mudança e re-embed automaticamente:

1. **Sweep automático**: o mnemory verifica a cada 15min se o modelo de embedding mudou. Quando detecta, itera sobre todas as memórias, gera novo embedding 1024d para cada, e substitui no Qdrant.
2. **Janela sem recall**: entre o restart e o sweep completo (~1-45min), o recall retorna 0 resultados porque os vetores têm dimensionalidade incompatível.
3. **Forçar aceleração**: gerar activity normal (conversar com o agente) aciona recalls que fazem o sweep detectar a mudança mais rapidamente.

### Verificar progresso do re-embed

No dashboard, aba **Search** → buscar qualquer termo. Se retornar resultados, o re-embed já completou.

Ou via servidor:
```bash
journalctl --user -u mnemory --since "5 min ago" | grep -i "re-embed\|reembed\|sweep\|embed.*model"
```

## Riscos e mitigação

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Perda de memórias | Zero — conteúdo no SQLite, só vetores no Qdrant | N/A |
| Recall = 0 entre restart e re-embed | Temporário (até 45min) | Sweep automático; conversar acelera |
| bge-m3 indisponível no NIM | Migração falha | Confirmado disponível via `GET /v1/models` |

## Rollback

```bash
cp ~/.config/opencode/scripts/mnemory-nim.sh.bak ~/.config/opencode/scripts/mnemory-nim.sh
# Opcional: deletar índice Qdrant para forçar re-embed completo
rm -rf ~/.local/share/mnemory/qdrant/
systemctl --user restart mnemory
```

## Verificação

- Embedding calls no log: `journalctl --user -u mnemory | grep embed`
- Recall > 0 nas próximas mensagens: `grep search_results ~/.local/share/opencode/log/opencode.log`
- Nenhum erro: `journalctl --user -u mnemory | grep -i "error\|fail\|exception"`
