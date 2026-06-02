# Plano: Memória Permanente para Agentmemory

## Problema

O agentmemory perdia dados após `wsl --shutdown` ou falhas de energia. O iii-engine v0.11.2 usa `file_based` KV com `save_interval_ms` default (5000ms), mas o flush nem sempre acontece antes do kill do processo.

## 4 intervenções feitas

### 1. `save_interval_ms: 100` → `5000`

**O que:** Reduziu a frequência de flush do iii-engine de 10/s para 0.2/s.

**Porquê:** `save_interval_ms: 100` causava I/O excessivo (180.000 writes em 30 min), que acumulava page cache e contribuía para crescimento do Vmmem.

**Onde:** `~/.agentmemory/iii-config.yaml` (linhas 11 e 23)

```yaml
config:
  store_method: file_based
  file_path: ./data/state_store.db
  save_interval_ms: 5000  # era 100
```

**Para desligar/reverter:**
```bash
# Editar ~/.agentmemory/iii-config.yaml
# Trocar save_interval_ms: 5000 para 100 (ou remover a linha para default)
systemctl --user restart agm
```

---

### 2. `TimeoutStopSec=30` no systemd

**O que:** Aumentou o timeout de graceful shutdown de 5s para 30s.

**Porquê:** Com 5s, o systemd matava o processo com SIGKILL antes do `IndexPersistence.save()` terminar. Vetores e BM25 index ficavam só em memória e eram perdidos.

**Onde:** `~/.config/systemd/user/agm.service` (linha 10)

```ini
[Service]
TimeoutStopSec=30  # era 5 (implicit default)
```

**Para desligar/reverter:**
```bash
# Editar ~/.config/systemd/user/agm.service
# Trocar TimeoutStopSec=30 para 5 (ou remover a linha para default)
systemctl --user daemon-reload
systemctl --user restart agm
```

---

### 3. `AGENTMEMORY_DROP_STALE_INDEX=true`

**O que:** Força descarte do vector index antigo (768 dims Gemini) a cada startup, permitindo reconstrução com o novo provider (4096 dims NVIDIA NIM).

**Porquê:** O vector index tinha 114 vetores de 768 dims (Gemini). O novo provider (NVIDIA NIM) usa 4096 dims. Sem esta flag, o engine recusa a iniciar.

**Onde:** `~/.agentmemory/.env`

```
AGENTMEMORY_DROP_STALE_INDEX=true
```

**Para desligar:**
```bash
# Editar ~/.agentmemory/.env
# Comentar: # AGENTMEMORY_DROP_STALE_INDEX=true
systemctl --user restart agm
```

**Nota:** Uma vez que o vector index seja reconstruído com 4096 dims, esta flag pode ser removida sem efeito. Mas se o provider mudar de novo (ex: voltar para Gemini), a flag será necessária.

---

### 4. `.env` — mudanças de embedding e slots

**O que:** Corrigiu o provider de embeddings (Gemini → NVIDIA NIM) e ativou memory slots.

**Mudanças aplicadas:**

| Variável                     | Antes                    | Depois                          |
| ---------------------------- | ------------------------ | ------------------------------- |
| `EMBEDDING_PROVIDER`           | `gemini` (via systemd)     | `openai`                          |
| `OPENAI_EMBEDDING_MODEL`       | Não existia              | `nvidia/nv-embed-v1`              |
| `OPENAI_EMBEDDING_DIMENSIONS`  | Não existia              | `4096`                            |
| `AGENTMEMORY_SLOTS`            | Não existia              | `true`                            |
| `GEMINI_API_KEY`               | Ativo                    | Comentado                       |
| `GEMINI_MODEL`                 | Ativo                    | Comentado                       |
| `EMBEDDING_MODEL` (errado)     | `nvidia/nv-embed-v1`       | **Renomeado** para `OPENAI_EMBEDDING_MODEL` |
| `AGENTMEMORY_DROP_STALE_INDEX` | Não existia              | `true`                            |
| `SNAPSHOT_INTERVAL`            | `300` (duplicado)           | `3600`                            |
| `SNAPSHOT_DIR`                 | `~/.agentmemory/snapshots` | Path absoluto                   |

**Arquivo:** `~/.agentmemory/.env`

**Para desligar individualmente:**

| Feature                    | Comando                                        |
| -------------------------- | ---------------------------------------------- |
| Embedding NVIDIA NIM       | Trocar `OPENAI_EMBEDDING_MODEL` para `text-embedding-3-small` e usar chave OpenAI |
| Memory Slots               | `# AGENTMEMORY_SLOTS=true`                        |
| Snapshot                   | `# SNAPSHOT_ENABLED=true`                         |
| Embedding provider (voltar Gemini) | Trocar `EMBEDDING_PROVIDER=gemini` e descomentar `GEMINI_API_KEY` |

---

## Estado atual do sistema

| Componente                    | Estado  |
| ----------------------------- | ------- |
| Serviço agm                   | ✅ Saudável |
| LLM provider                  | NVIDIA NIM (gpt-oss-120b) |
| Embedding provider            | NVIDIA NIM (nv-embed-v1, 4096 dims) |
| Vector index                  | ✅ 3 vetores, Triple-stream active |
| BM25 index                    | ✅ 1261 docs |
| save_interval_ms              | 5000 |
| TimeoutStopSec                | 30s |
| SNAPSHOT_ENABLED              | true (1h interval) |
| AGENTMEMORY_SLOTS             | true |
| AGENTMEMORY_DROP_STALE_INDEX  | true |
| AGENTMEMORY_INJECT_CONTEXT    | true |
| AGENTMEMORY_AUTO_COMPRESS     | true |
| CONSOLIDATION_ENABLED         | true |
| GRAPH_EXTRACTION_ENABLED      | true |
| AGENTMEMORY_REFLECT           | true |

## Notas conhecidas

1. **`mode: "compact"` é hardcoded** — o `mem::smart-search` sempre retorna `mode: "compact"` mesmo quando vector search está ativo. Não é um bug, é limitação do código.

2. **`PassEnvironment=GEMINI_API_KEY` no systemd** — o shell pode ter `GEMINI_API_KEY` set (do `.bashrc`/`.profile`). O systemd passa para o processo. Isto pode causar confusão se o Gemini voltar a ser necessário.

3. **`~/.agentmemory/iii-config.yaml`** — pode ser sobrescrito em updates npm. Manter cópia de backup.

4. **Arquivo `.agentmemory-debug.log`** — cresce ~1.3MB por linha se debug estiver ativo. Remover o `OPENCODE_AGENTMEMORY_DEBUG=1` do ambiente.
