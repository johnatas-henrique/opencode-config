# Plan: Fix MemPalace Segfault Error

## Problem
MemPalace 3.3.3 crashes with segmentation fault when running `mempalace status` or `mempalace repair`. The crash occurs in `chromadb_rust_bindings.abi3.so` (ChromaDB Rust bindings).

**Error from dmesg:**
```
segfault at 0 ip 000073210f8d2877 sp 00007320aeff4500 error 4 in chromadb_rust_bindings.abi3.so
```

## Root Cause
The ChromaDB Rust bindings (v1.5.8) have a null pointer dereference issue, likely triggered by database corruption or incompatible binary.

## Recovery Plan

### Step 1: Backup Current Data (CRITICAL)
```bash
cp -r ~/.mempalace ~/.mempalace.backup.$(date +%Y%m%d_%H%M%S)
cp -r ~/.config/opencode ~/.config/opencode.backup.$(date +%Y%m%d_%H%M%S)
```

### Step 2: Fix venv and Reinstall ChromaDB
The venv is missing pip. Fix the venv first:

```bash
# Bootstrap pip into the existing venv
curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
~/.local/share/mempalace-venv/bin/python3 /tmp/get-pip.py

# Then upgrade ChromaDB
~/.local/share/mempalace-venv/bin/python3 -m pip install --force-reinstall --no-cache-dir "chromadb>=1.5.20"
```

If that fails, recreate the venv:
```bash
rm -rf ~/.local/share/mempalace-venv
python3 -m venv ~/.local/share/mempalace-venv
~/.local/share/mempalace-venv/bin/python3 -m ensurepip --upgrade
~/.local/share/mempalace-venv/bin/pip install mempalace
```

### Step 3: Reset WAL Files (If Step 2 Fails)
WAL (Write-Ahead Log) corruption can cause segfaults:

```bash
rm -rf ~/.mempalace/wal/*
rm -rf ~/.mempalace/locks/*
```

### Step 4: Try Running Membrane with Fresh DB
Test if the binary works with a clean database:

```bash
mv ~/.mempalace/palace ~/.mempalace/palace.broken
mkdir ~/.mempalace/palace
~/.local/share/mempalace-venv/bin/mempalace status
```

If this works, the issue is corrupted data.

### Step 5: Recover Data from Broken Palace
If Step 4 works, attempt to recover data:

1. Use the MCP tool `mempalace_mempalace_reconnect` after fixing
2. Or manually export from SQLite:
   ```bash
   # Check if SQLite is accessible
   ~/.local/share/mempalace-venv/bin/python -c "import sqlite3; conn = sqlite3.connect('~/.mempalace/palace/chroma.sqlite3'); print(conn.execute('SELECT COUNT(*) FROM embeddings').fetchone())"
   ```

### Step 6: Nuclear Option - Full Reinstall
If all else fails:

```bash
# Remove and recreate venv
rm -rf ~/.local/share/mempalace-venv
python3 -m venv ~/.local/share/mempalace-venv
~/.local/share/mempalace-venv/bin/pip install mempalace

# Restore from backup or start fresh
rm -rf ~/.mempalace
```

## Verification
After each step, test with:
```bash
~/.local/share/mempalace-venv/bin/mempalace status
```

## Data Recovery Priority
1. The `knowledge_graph.sqlite3` in `~/.mempalace/` is separate from ChromaDB - likely intact
2. Palace data in `~/.mempalace/palace/chroma.sqlite3` may be recoverable
3. Consider using `mempalace_mempalace_diary_read` MCP tool to check if MCP interface still works

## Risk Assessment
- **Low risk**: Steps 1-3 (backup + reinstall + WAL reset)
- **Medium risk**: Step 4 (moving palace data)
- **High risk**: Step 6 (full reinstall - data loss possible)

## Recommended Approach
Start with Step 1 (backup), then try Step 2 (reinstall ChromaDB). Only proceed to later steps if necessary.
