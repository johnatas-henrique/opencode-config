# Plano: Reivindicação Automática de Memória WSL2

**Data:** 2026-05-30
**Objetivo:** Configurar o WSL2 para reivindicar memória automaticamente, evitando o Vmmem a crescer para >12 GB e a precisar de `drop_caches` manual.

---

## Contexto

- PC com **32 GB RAM**
- WSL2 com workload pesado: 2x OpenCode, AFT (codebase indexer), VS Code, agentmemory
- Vmmem crescia para 12+ GB sem reivindicação automática
- O `autoMemoryReclaim` (default) não funcionava porque o CPU raramente fica idle
- O `drop_caches` manual libertava ~3.5 GB, mas tinha de ser executado manualmente

---

## Passo 1: `.wslconfig` — `autoMemoryReclaim=dropCache`

### O que faz
Força o WSL a escrever para `/proc/sys/vm/drop_caches` (liberta page cache + dentry + inode cache) quando o CPU fica idle. É o mecanismo padrão, mas estava implícito — tornámo-lo explícito.

### Fonte
- [Microsoft Docs — WSL Config](https://learn.microsoft.com/en-us/windows/wsl/wsl-config): `autoMemoryReclaim` — "If the value is `dropCache` or an unknown value, cached memory will be reclaimed immediately."
- [GitHub Discussion #10487](https://github.com/microsoft/WSL/discussions/10487): Features in `.wslconfig`

### Execução
```powershell
# Abrir PowerShell como Administrator
notepad "$env:USERPROFILE\.wslconfig"
```

Adicionar no final:
```ini
[experimental]
autoMemoryReclaim=dropCache
```

Aplicar:
```powershell
wsl --shutdown
# Depois reabrir o WSL
```

Verificar (dentro do WSL):
```bash
dmesg | grep -i "memory compaction\|dropCache" | tail -5
```

### Como desligar
Remover as 2 linhas adicionadas de `%USERPROFILE%\.wslconfig` e correr `wsl --shutdown`.

---

## Passo 2: `vfs_cache_pressure=200` — Slab mais agressivo

### O que faz
Diz ao kernel Linux para reivindicar dentry/inode cache (Slab) com o **dobro** da agressividade. O Slab era ~1 GB no nosso teste. Com 200, é reivindicado mais rápido, mesmo com CPU ocupado.

### Fonte
- [Linux Kernel Docs — sysctl/vm](https://docs.kernel.org/6.11/admin-guide/sysctl/vm.html): "vfs_cache_pressure — controls the tendency of the kernel to reclaim memory used for caching of directory and inode objects... Increasing vfs_cache_pressure beyond 100 causes the kernel to prefer to reclaim dentries and inodes."

### Execução
```bash
# Dentro do WSL
echo 'vm.vfs_cache_pressure = 200' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
cat /proc/sys/vm/vfs_cache_pressure  # Deve retornar: 200
```

### Como desligar
Remover a linha `vm.vfs_cache_pressure = 200` de `/etc/sysctl.conf` e correr:
```bash
sudo sysctl -p  # Volta ao default (100)
```

---

## Passo 3: Cron `compact_memory` a cada 15 min

### O que faz
Executa `echo 1 > /proc/sys/vm/compact_memory` a cada 15 minutos. Isto reorganiza a memória, juntando blocos livres em blocos contíguos. O **page reporting** do WSL2 só consegue devolver blocos contíguos ao Hyper-V. Sem compactação, blocos fragmentados não são reportados.

### Fonte
- [Microsoft DevBlog — Memory Reclaim in WSL2](https://devblogs.microsoft.com/commandline/memory-reclaim-in-the-windows-subsystem-for-linux-2/): "periodically compact memory to ensure free memory is available in contiguous blocks. This only runs when your CPU is idle."
- [Linux Kernel Docs — compact_memory](https://docs.kernel.org/6.11/admin-guide/sysctl/vm.html): "compact_memory — When 1 is written, all zones are compacted such that free memory is available in contiguous blocks where possible."

### Execução
```bash
# Criar script
sudo tee /usr/local/bin/wsl-memory-compact << 'EOF'
#!/bin/sh
echo 1 > /proc/sys/vm/compact_memory
EOF
sudo chmod +x /usr/local/bin/wsl-memory-compact

# Criar cron job (a cada 15 min)
echo '*/15 * * * * root /usr/local/bin/wsl-memory-compact' | sudo tee /etc/cron.d/wsl-memory-compact
sudo chmod 644 /etc/cron.d/wsl-memory-compact

# Ativar serviço cron
sudo systemctl enable --now cron
```

Verificar:
```bash
cat /etc/cron.d/wsl-memory-compact
systemctl status cron
```

### Como desligar
Remover o arquivo do cron:
```bash
sudo rm /etc/cron.d/wsl-memory-compact
```

O script `/usr/local/bin/wsl-memory-compact` pode ficar no sistema (pesa poucos bytes).

---

## Passo 4: Cron `drop_caches` a cada 1h (FÚCULTATIVO)

### O que faz
Executa `echo 3 > /proc/sys/vm/drop_caches` a cada hora. Liberta **todo o cache** (page cache + dentries + inodes). É mais agressivo que `compact_memory` — perde cache mas devolve mais memória ao Windows.

### Nota
Este passo é **opcional**. Só ativa se, após os Passos 1-3, o Vmmem continuar a crescer para >12 GB.

### Fonte
- [Microsoft DevBlog](https://devblogs.microsoft.com/commandline/memory-reclaim-in-the-windows-subsystem-for-linux-2/): "If you wish to drop the contents manually you can run `echo 1 > /proc/sys/vm/drop_caches` as the root user to do so."

### Execução
```bash
# Criar script
sudo tee /usr/local/bin/wsl-memory-drop << 'EOF'
#!/bin/sh
echo 3 > /proc/sys/vm/drop_caches
EOF
sudo chmod +x /usr/local/bin/wsl-memory-drop

# Criar cron job (a cada 1h)
echo '0 * * * * root /usr/local/bin/wsl-memory-drop' | sudo tee /etc/cron.d/wsl-memory-drop
sudo chmod 644 /etc/cron.d/wsl-memory-drop
```

Verificar:
```bash
cat /etc/cron.d/wsl-memory-drop
```

### Como desligar
Remover o arquivo do cron:
```bash
sudo rm /etc/cron.d/wsl-memory-drop
```

---

## Resumo: como desligar cada ponto

| Passo  | Arquivo                 | Como desligar                                |
| ------ | ----------------------- | -------------------------------------------- |
| 1      | `%USERPROFILE%\.wslconfig` | Remover `[experimental]` + `autoMemoryReclaim` e `wsl --shutdown` |
| 2      | `/etc/sysctl.conf`        | Remover `vm.vfs_cache_pressure = 200` e `sudo sysctl -p`        |
| 3      | `/etc/cron.d/wsl-memory-compact` | `sudo rm /etc/cron.d/wsl-memory-compact`             |
| 4      | `/etc/cron.d/wsl-memory-drop`    | `sudo rm /etc/cron.d/wsl-memory-drop`                  |

---

## Verificação após execução

| Métrica                              | Antes     | Esperado depois                       |
| ------------------------------------ | --------- | ------------------------------------- |
| Vmmem (Task Manager)                 | 12.5 GB   | 6-8 GB (dependendo do workload)       |
| Cached (Linux)                       | 3 GB      | <1 GB (reivindicado)                  |
| Slab (Linux)                         | 1 GB      | <600 MB (vfs_cache_pressure=200)      |
| `dmesg \| grep "memory compaction"`  | Vazio     | Mensagens periódicas                  |
| `cat /proc/sys/vm/vfs_cache_pressure`| 100       | 200                                   |
