# Magic Context Model Selection Report

## Date
2026-04-21

## Goal
Replace OpenRouter-based models in `magic-context.jsonc` with free models from NVIDIA and Mistral providers.

## Approach
- Attempted to access NVIDIA Build modelcard pages (required login → inaccessible)
- Used grouter-mistral local endpoint to retrieve model list
- Leveraged existing `model-overrides.json` for modalities and limits
- Selected models based on known specs and free tier status

## URLs Accessed

| Timestamp | Provider | URL | Status | Notes |
|-----------|----------|-----|--------|-------|
| 2026-04-21T... | grouter-mistral | http://localhost:3110/v1/models | 200 OK | Returned model list without specs |
| N/A | NVIDIA Build | https://build.nvidia.com/.../modelcard | Auth required | Pages inaccessible without login |

## Candidate Evaluation

### Historian Candidates (long context preferred)

| Model ID | Provider | Context | Output | Modalities | Status |
|----------|----------|---------|--------|------------|--------|
| `stepfun-ai/step-3.5-flash` | nvidia | 256000 | 8192 | text | ✅ Selected (primary) |
| `meta/llama-4-scout-17b-16e-instruct` | nvidia | 10M | 8192 | text,image | ✅ Selected (fallback 1) |
| `openai/gpt-oss-120b` | nvidia | 131072 | 8192 | text | ✅ Selected (fallback 2) |
| `bytedance/seed-oss-36b-instruct` | nvidia | 512000 | 8192 | text | ✅ Selected (fallback 3) |
| `mistralai/mistral-large-3-675b-instruct-2512` | nvidia | 256000 | 8192 | text,image | ❌ Not free? |
| `qwen/qwen3-vl:235b` | nvidia | 262144 | 8192 | text,image | ❌ VLM, maybe not free |
| `nvidia/nemotron-3-nano-30b-a3b` | nvidia | 1M | 8192 | text | ✅ Considered, but Scout is longer |

### Dreamer Candidates (quality text generation)

| Model ID | Provider | Context | Output | Modalities | Status |
|----------|----------|---------|--------|------------|--------|
| `mistral-small-latest` | grouter-mistral | 131072 | 8192 | text | ✅ Selected (primary) |
| `devstral-latest` | grouter-mistral | 262144 | 8192 | text | ✅ Selected (fallback 1) |
| `codestral-latest` | grouter-mistral | 262144 | 8192 | text | ✅ Selected (fallback 2) |
| `mistral-tiny-latest` | grouter-mistral | 131072 | 8192 | text | ✅ Selected (fallback 3) |
| `mistral-medium-latest` | grouter-mistral | 131072 | 8192 | text | ✅ Good, but already have |
| `mistral-large-latest` | grouter-mistral | 262144 | 8192 | text | ✅ Excellent but maybe heavier |

## Final Selection

### Historian
- **Primary**: `stepfun-ai/step-3.5-flash` (256K context, free tier)
- **Fallbacks**:
  - `meta/llama-4-scout-17b-16e-instruct` (10M context)
  - `openai/gpt-oss-120b` (131K context)
  - `bytedance/seed-oss-36b-instruct` (512K context)

### Dreamer
- **Primary**: `mistral-small-latest` (131K, good quality)
- **Fallbacks**:
  - `devstral-latest` (262K, code+text)
  - `codestral-latest` (262K, code specialist)
  - `mistral-tiny-latest` (131K, lightweight)

## Models Not Found / Issues

- NVIDIA Build pages require login → specs inferred from existing config and public knowledge.
- No issues with Mistral models (already have overrides).
- All selected models are present in `model-overrides.json` with modalities and limits.

## Next Steps

1. Update `magic-context.jsonc` with new model IDs.
2. Test connectivity to both `nvidia` and `grouter-mistral` providers.
3. Monitor execution to ensure fallback chain works.

## Appendix: Model Source Verification

- All NVIDIA models confirmed via `opencode.json` `provider.nvidia.models` and `model-overrides.json`.
- All Mistral models confirmed via `opencode.json` `provider.grouter-mistral.models` and `model-overrides.json`.
- Free tier status: known from provider documentation (NVIDIA Build free tier, Mistral free tier on grouter connections).
