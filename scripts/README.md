# Scripts

## `verify-provider.py`

Tests a grouter provider on a specific port to identify working models.

```bash
# Test provider on port 3109
python3 scripts/verify-provider.py 3109 --api-key grouter

# Custom prompt
python3 scripts/verify-provider.py 3102 --api-key grouter --prompt "Write Python hello world"

# Specify output directory
python3 scripts/verify-provider.py 3109 --output-dir ./test-results
```

## `mnemory-nim.sh`

Systemd service wrapper for mnemory with NVIDIA NIM embeddings + monkey-patches.
Started via `~/.config/systemd/user/mnemory.service`.

## `mnemory.env`

Environment file for `mnemory-nim.sh` — contains `NIM_API_KEY`.
Gitignored to avoid leaking secrets.

---

## Removed Scripts

The complete model pipeline (verify → generate → normalize → fetch scores) was
removed. The config is now `opencode.jsonc` and the pipeline scripts referenced
`opencode.json`. The static score data (`models.dev.api.json`, 1.8MB) was also
removed. Full content recoverable via git.

**Last updated:** 2026-06-06
