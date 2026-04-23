# Model Benchmark and Management Scripts

Scripts for managing benchmark scores, configuring providers, and updating models in OpenCode.

## Available Scripts

### `verify-provider.py`

Tests a grouter provider on a specific port to identify which models are working.

#### Usage:

```bash
# Test provider on port 3109
python3 scripts/verify-provider.py 3109 --api-key grouter

# Custom prompt
python3 scripts/verify-provider.py 3102 --api-key grouter --prompt "Write Python hello world"

# Specify output directory
python3 scripts/verify-provider.py 3109 --output-dir ./test-results
```

#### Auto-detection of name:

The script reads `/v1/models` endpoint and extracts `owned_by` field from the first model to name output files. For example, if `owned_by = "modal"`, files will be `modal-ok.json`, `modal-fail.json`.

If detection fails, uses `localhost{port}` as fallback.

#### Output Files:

- `{provider-name}-ok.json` - successfully tested models
- `{provider-name}-fail.json` - failed models
- `{provider-name}-ok.txt` - human-readable version
- `{provider-name}-fail.txt` - human-readable version

#### Features:

- Tests `/v1/models` to list available models
- Tests each model with POST `/v1/chat/completions` using simple prompt
- **Retry up to 3x** for models that fail on first attempt
- Uses `max_tokens=10` for short, fast responses
- **Auto-detects** provider name via `owned_by`

---

### `generate-provider-config.py`

Generates provider configuration for `opencode.json` from `verify-provider.py` results. Creates a provider object with basic model entries. Metadata (modalities, limit, tool_call, reasoning) will be added later by `generate-model-metadata.py`.

#### Usage:

```bash
# Generate config from verification results
python3 scripts/generate-provider-config.py "GRouter OpenRouter-ok.json"

# Specify output directory
python3 scripts/generate-provider-config.py "GRouter-OpenRouter-ok.json" --output-dir ./configs
```

#### Output:

- `provider-{provider}-config.json` - JSON object ready to paste into `opencode.json` under `"provider"` section

#### Features:

- Groups models by `owned_by` (each owner becomes separate provider: `grouter-{owner}`)
- Includes **all models** (working and failing) — you decide which to keep
- Extracts basic info (model ID, name, context limits) from the provider's `/v1/models` endpoint

#### Next Steps:

After generating the provider config:
1. Copy the provider object into `opencode.json` under `"provider"`
2. Run `python3 scripts/generate-model-metadata.py` to populate `modalities`, `limit`, `tool_call`, `reasoning` for all models using `models.dev.api.json`
3. Run `python3 scripts/normalize-model-names.py --apply` to format model names consistently
4. Run `python3 scripts/fetch-benchmark-scores.py` to update benchmark scores


---

### `generate-provider-mapping.py`

Generates `provider-mapping.json` that maps OpenCode providers to sources in `models.dev.api.json`.

#### Usage:

```bash
python3 scripts/generate-provider-mapping.py
```

#### Output:

- `provider-mapping.json` - mapping between OpenCode providers and models.dev sources

#### Features:

- Direct mapping for providers like `grouter-openrouter` → `openrouter`
- Dynamic strategies by model ID prefix (e.g., `anthropic/` → `anthropic`)
- Skips special providers like `manifest` (internal models)
- Saves mapping for use by `update-opencode-models.py`

---

### `update-opencode-models.py`

Updates models in `opencode.json` with fresh data from `models.dev.api.json` using `provider-mapping.json` for routing.

#### Usage:

```bash
python3 scripts/update-opencode-models.py
```

#### Behavior:

- For each provider in `opencode.json`
- Queries `provider-mapping.json` to find source in `models.dev.api.json`
- Updates `name`, `modalities`, `limit` of models
- Adds new missing models
- **Creates backup** of `opencode.json` before modifying
- **Preserves** existing fields like `blacklist`, `options`, `npm`

#### Features:

- Mapping by direct provider or by model ID prefix
- Supports multiple sources per provider via dynamic mapping
- Incremental: only adds/updates, never removes
- Automatic backup to `opencode.json.bak`

---

### `generate-model-metadata.py`

Generates metadata (`modalities`, `limit`, `tool_call`, `reasoning`) for provider models by querying local grouter endpoints, external APIs, and using inference.

#### Usage:

```bash
# Dry run to preview changes
python3 scripts/generate-model-metadata.py --dry-run

# Apply changes to opencode.json
python3 scripts/generate-model-metadata.py
```

#### What it does:

- Iterates over all providers defined in `opencode.json`
- Queries `models.dev.api.json` as primary source
- For models not found, queries local grouter endpoints if available
- Infers modalities when not available (based on keywords: "vision", "audio", "image")
- Extracts `context` and `max_tokens` from responses
- Updates `opencode.json` directly

#### Fields Added:

- `modalities` (input/output arrays)
- `limit` (context/output)
- `options.tool_call` (boolean)
- `options.reasoning` (boolean)

#### Features:

- Processes all providers automatically (not hardcoded list)
- Primary source: `models.dev.api.json` (flattened across all providers)
- Secondary: local grouter endpoints for `grouter-*` providers
- Inference fallback for modalities only
- Does not overwrite existing fields

---

### `normalize-model-names.py`

Normalizes model names in `opencode.json`, enriching them with scores and standardized metadata.

#### Usage:

```bash
# Preview changes without saving
python3 scripts/normalize-model-names.py --dry-run

# Apply to opencode.json
python3 scripts/normalize-model-names.py --apply
```

#### What it does:

- Loads official names from `models.dev.api.json`
- Uses scores cache (`.scores-cache.json`)
- Decides whether to use official name (better formatted) or keep current
- Reformats name to standard pattern:
  ```
  {Official Name} | SWE-L/X% | {ctx}K/{out}K | [MODALITIES...]
  ```
- Example: `DeepSeek V3.2 | SWE-L: 70.0% | 163K/65K`

#### Decision Logic:

- Replaces if current name is simple kebab-case and official name has spaces
- Does not replace if name contains parentheses (provider info)
- Does not replace generic IDs (auto, latest, etc.)

#### Modality Order:

Modalities are sorted in fixed priority: `IMAGE`, `AUDIO`, `PDF`, `VIDEO`, then any others alphabetically.

---

### `fetch-benchmark-scores.py`

Fetches benchmark scores (SWE-bench Lite, SWE-bench Verified, LiveCodeBench, Aider) for all configured models in `opencode.json`.

#### Usage:

```bash
# First time (or after adding new models)
python3 scripts/fetch-benchmark-scores.py

# Run again anytime to update (incremental cache)
python3 scripts/fetch-benchmark-scores.py

# Force refresh all scores
python3 scripts/fetch-benchmark-scores.py --force
```

#### Output:

- `docs/model-benchmarks/scores.md` - combined table with all models and scores
- `docs/model-benchmarks/scores-lite.md` - SWE-bench Lite only (comparable)
- `docs/model-benchmarks/scores-verified.md` - SWE-bench Verified only
- `docs/model-benchmarks/.scores-cache.json` - incremental cache

#### Adding scores manually:

Edit `scripts/fetch-benchmark-scores.py` and add entries to `STATIC_FALLBACK["swe_lite"]` and `STATIC_FALLBACK["swe_verified"]`. Use normalized IDs (lowercase, no suffixes).

#### Sources:

- Online: `https://swe-bench.github.io/leaderboards.json`
- Internal static fallback when online fails

---

## 📊 Benchmark Scores Interpretation

### SWE-bench Lite (Recommended for comparison)

- **Protocol**: mini-swe-agent v2 (same code for all)
- **Dataset**: 300 real GitHub issues
- **Comparability**: ✅ **Excellent** - scores directly comparable across models
- **Example**: Claude Opus 4.5 has 76.8%, GPT-5.2 Codex has 72.8%

### SWE-bench Verified

- **Protocol**: Each vendor can optimize their own scaffold
- **Dataset**: 500 real issues
- **Comparability**: ❌ **Poor** - optimized scores are not fair to compare
- **Use**: See maximum potential a model CAN ACHIEVE (but do not compare)

### LiveCodeBench

- Competition problems (LeetCode/Codeforces)
- Measures logical reasoning, not real coding agent capability
- Poor correlation with SWE-bench

### Aider

- Single-file editing across multiple languages
- Measures ability to follow refactoring instructions
- Does not test multi-file debugging

---

## 🔄 Complete Workflow

### 1. Add a new grouter provider

```bash
# Test the provider port
python3 scripts/verify-provider.py 3109 --api-key grouter --name "OpenRouter"

# Generate provider config
python3 scripts/generate-provider-config.py "GRouter OpenRouter-ok.json"

# Copy the provider object from provider-*.json into opencode.json under "provider"

# Add metadata (modalities, limits, tool_call, reasoning)
python3 scripts/generate-model-metadata.py

# Normalize model names
python3 scripts/normalize-model-names.py --apply

# Update benchmark scores
python3 scripts/fetch-benchmark-scores.py
```

### 2. Update benchmark scores (optional incremental)

```bash
# After adding models to opencode.json
python3 scripts/fetch-benchmark-scores.py

# Markdown files are updated automatically
```

---

## 🐛 Troubleshooting

### Model appears twice in generated config

This can happen if there are multiple entries in results JSON. The script groups by `owned_by`, but if same `owned_by` appears with different names (e.g., "Modal" vs "modal"), separate providers are created. Normalize `--name` when running `verify-provider.py`.

### Scores do not appear in table after adding models

Check that `model_id` in `opencode.json` matches a key in scores dictionaries. The script uses normalization (lowercase, remove suffixes). Add manual entries to `SWE_LITE_SCORES`/`SWE_VERIFIED_SCORES` if needed.

---

## 📁 File Structure

```
~/.config/opencode/
├── opencode.json                    # Main config
├── scripts/
│   ├── fetch-benchmark-scores.py
│   ├── verify-provider.py
│   ├── generate-provider-config.py
│   ├── generate-model-metadata.py
│   ├── normalize-model-names.py
│   ├── generate-provider-mapping.py
│   ├── update-opencode-models.py
│   ├── README.md                    # This file
│   └── models.dev.api.json          # Model metadata source (place here)
├── docs/
│   └── model-benchmarks/
│       ├── scores.md
│       ├── scores-lite.md
│       ├── scores-verified.md
│       └── .scores-cache.json
└── provider-*-config.json           # Generated by generate-provider-config.py
```

---

## 🎯 Important Notes

- Scripts **do not access external APIs** (except during provider verification). Scores are local data.
- `fetch-benchmark-scores.py` uses incremental cache to avoid data loss when adding models
- `verify-provider.py` tests each model up to 3x before marking as failure
- For questions about benchmarks, consult official sources (SWE-bench, LiveCodeBench, Aider)

---

**Last updated:** 2026-04-21
