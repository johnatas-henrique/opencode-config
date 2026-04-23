#!/usr/bin/env python3
"""
Fetch benchmark scores for models in opencode.json.
Fetches SWE-bench Lite/Verified scores from online sources (swe-bench.github.io).
Generates a Markdown table with all scores.
"""
import json
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

STATIC_FALLBACK = {
    "swe_lite": {
        "claude-4.5-opus": 76.80,
        "gemini-3-flash": 75.80,
        "minimax-m2.5": 75.80,
        "claude-opus-4.6": 75.60,
        "gpt-5-2-codex": 72.80,
        "glm-5": 72.80,
        "gpt-5.2": 72.80,
        "claude-4.5-sonnet": 71.40,
        "kimi-k2.5": 70.80,
        "deepseek-v3.2": 70.00,
        "gemini-3-pro": 69.60,
        "claude-4.5-haiku": 66.60,
        "gpt-5-mini": 56.20,
        "gemini-2.5-pro-preview": 53.6,
        "gemini-2.5-flash-preview": 46.7,
        "gpt-4.1": 23.94,
        "gpt-4o": 21.62,
        "llama-4-maverick": 21.04,
        "llama-4-scout": 9.06,
        "qwen3-coder-next": 40.0,
        "devstral-2-123b": 37.5,
        "deepseek-r1": 41.4,
        "deepseek-v3.1": 38.8,
    },
    "swe_verified": {
        "claude-opus-4.7": 87.6,
        "claude-opus-4.6": 80.8,
        "claude-opus-4.5": 80.9,
        "claude-opus-4": 72.5,
        "claude-sonnet-4.6": 79.6,
        "claude-sonnet-4.5": 77.2,
        "claude-sonnet-4": 72.7,
        "claude-haiku-4.5": 73.3,
        "claude-3.7-sonnet": 70.3,
        "claude-3.5-sonnet": 51.6,
        "claude-3.5-haiku": 40.6,
        "gpt-5.3-codex": 85.0,
        "gpt-5.2": 80.0,
        "gpt-5.1": 74.9,
        "gpt-5": 74.9,
        "gpt-5-codex": 74.5,
        "gpt-4.1": 54.6,
        "gpt-oss-120b": 62.4,
        "o3": 49.8,
        "o4-mini": 68.1,
        "o1": 61.7,
        "o3-mini": 53.8,
        "gemini-3.1-pro": 80.6,
        "gemini-3.1-flash": 78.0,
        "gemini-3-flash": 78.0,
        "gemini-3-pro": 76.2,
        "gemini-2.5-pro": 63.8,
        "gemini-2.5-flash": 55.1,
        "gemini-2.0-flash": 13.5,
        "deepseek-v3.2": 73.0,
        "deepseek-v3.1": 73.0,
        "deepseek-r1": 71.4,
        "deepseek-r1-0528": 71.4,
        "deepseek-r1-distill-qwen-32b": 62.1,
        "deepseek-r1-distill-llama-70b": 47.0,
        "deepseek-r1-distill-qwen-14b": 42.0,
        "deepseek-v3": 38.8,
        "qwen3.6-plus": 78.8,
        "qwen3.5-397b": 76.4,
        "qwen3.5-122b": 72.0,
        "qwen3.5-27b": 72.4,
        "qwen3.5-35b": 69.2,
        "qwen3-235b": 73.1,
        "qwen3-80b": 69.6,
        "qwen3-coder-480b": 69.6,
        "qwen3-coder-next": 70.6,
        "qwen3.6-35b": 73.4,
        "qwen3-max": 69.6,
        "qwen3-32b": 40.0,
        "qwen3-next-80b": 69.6,
        "qwen3.5-flash": 74.0,
        "qwq-32b": 42.0,
        "qwen2.5-coder-32b": 9.0,
        "devstral-2": 72.2,
        "devstral-2-123b": 72.2,
        "devstral-small-2": 68.0,
        "devstral-small-24b": 68.0,
        "devstral-small": 53.6,
        "devstral-medium": 61.6,
        "minimax-m2.5": 80.2,
        "minimax-m2.7": 80.2,
        "minimax-m2.1": 69.4,
        "minimax-m2": 69.4,
        "minimax-m2.6": 80.2,
        "kimi-k2.6": 80.2,
        "kimi-k2.5": 76.8,
        "kimi-k2-thinking": 71.3,
        "kimi-k2": 59.1,
        "glm-5": 77.8,
        "glm-4.7": 73.8,
        "glm-4.6": 68.0,
        "mistral-large-3": 33.3,
        "mistral-small-4": 46.8,
        "mistral-medium-3": 40.0,
        "mistral-magistral-small": 42.0,
        "mistral-ministral-14b": 38.0,
        "mistral-ministral-8b": 35.0,
        "mistral-ministral-3b": 30.0,
        "mixtral-8x22b": 36.0,
        "muse-spark": 77.4,
        "llama-4-maverick": 70.7,
        "llama-4-scout": 44.0,
        "llama-3.3-70b": 48.0,
        "llama-3.1-405b": 47.0,
        "llama-3.1-8b": 23.0,
        "mimo-v2-pro": 78.0,
        "mimo-v2-omni": 74.8,
        "mimo-v2-flash": 73.4,
        "seed-2.0-pro": 76.5,
        "seed-2.0-lite": 73.5,
        "seed-oss-36b": 26.0,
        "step-3.5-flash": 74.4,
        "longcat-flash-thinking": 70.0,
        "longcat-flash": 70.0,
        "grok-4": 73.5,
        "grok-code-fast-1": 57.6,
        "grok-3-beta": 53.3,
        "grok-3-mini-beta": 49.3,
        "optimus-alpha": 52.9,
        "quasar-alpha": 54.7,
        "cogito-2.1": 35.0,
        "rnj-1-8b": 18.0,
        "stockmark-100b": 28.0,
        "colosseum-355b": 27.0,
        "granite-34b": 32.0,
        "ibm-granite-34b": 32.0,
        "gpt-oss-20b": 22.0,
    },
}

SWE_BENCH_URL = "https://raw.githubusercontent.com/SWE-bench/swe-bench.github.io/master/data/leaderboards.json"

def fetch_swe_bench_scores() -> tuple[dict, dict]:
    """Fetch SWE-bench scores from online leaderboard JSON.
    
    Returns:
        Tuple of (swe_lite_scores dict, swe_verified_scores dict)
    """
    if requests is None:
        raise ImportError("requests library not installed")
    
    print("🌐 Fetching SWE-bench leaderboard data...")
    response = requests.get(SWE_BENCH_URL, timeout=60)
    response.raise_for_status()
    
    data = response.json()
    
    swe_lite = {}
    swe_verified = {}
    
    for leaderboard in data.get("leaderboards", []):
        name = leaderboard.get("name", "").lower()
        results = leaderboard.get("results", [])
        
        target_dict = None
        if "lite" in name:
            target_dict = swe_lite
        elif "verified" in name:
            target_dict = swe_verified
        
        if target_dict is not None:
            for entry in results:
                model_name = entry.get("name", "")
                resolved = entry.get("resolved")
                if model_name and resolved is not None:
                    normalized = normalize_model_name(model_name)
                    target_dict[normalized] = resolved
    
    print(f"  Found {len(swe_lite)} models in Lite, {len(swe_verified)} models in Verified")
    return swe_lite, swe_verified

SWE_VERIFIED_SCORES = {
    "claude-opus-4.7": 87.6,
    "claude-opus-4.6": 80.8,
    "claude-opus-4.5": 80.9,
    "claude-opus-4": 72.5,
    "claude-sonnet-4.6": 79.6,
    "claude-sonnet-4.5": 77.2,
    "claude-sonnet-4": 72.7,
    "claude-haiku-4.5": 73.3,
    "claude-3.7-sonnet": 70.3,
    "claude-3.5-sonnet": 51.6,
    "claude-3.5-haiku": 40.6,

    "gpt-5.3-codex": 85.0,
    "gpt-5.2": 80.0,
    "gpt-5.1": 74.9,
    "gpt-5": 74.9,
    "gpt-5-codex": 74.5,
    "gpt-4.1": 54.6,
    "gpt-oss-120b": 62.4,
    "o3": 49.8,
    "o4-mini": 68.1,
    "o1": 61.7,
    "o3-mini": 53.8,

    "gemini-3.1-pro": 80.6,
    "gemini-3.1-flash": 78.0,
    "gemini-3-flash": 78.0,
    "gemini-3-pro": 76.2,
    "gemini-2.5-pro": 63.8,
    "gemini-2.5-flash": 55.1,
    "gemini-2.0-flash": 13.5,

    "deepseek-v3.2": 73.0,
    "deepseek-v3.1": 73.0,
    "deepseek-r1": 71.4,
    "deepseek-r1-0528": 71.4,
    "deepseek-r1-distill-qwen-32b": 62.1,
    "deepseek-r1-distill-llama-70b": 47.0,
    "deepseek-r1-distill-qwen-14b": 42.0,
    "deepseek-v3": 38.8,

    "qwen3.6-plus": 78.8,
    "qwen3.5-397b": 76.4,
    "qwen3.5-122b": 72.0,
    "qwen3.5-27b": 72.4,
    "qwen3.5-35b": 69.2,
    "qwen3-235b": 73.1,
    "qwen3-80b": 69.6,
    "qwen3-coder-480b": 69.6,
    "qwen3-coder-next": 70.6,
    "qwen3.6-35b": 73.4,
    "qwen3-max": 69.6,
    "qwen3-32b": 40.0,
    "qwen3-next-80b": 69.6,
    "qwen3.5-flash": 74.0,
    "qwq-32b": 42.0,
    "qwen2.5-coder-32b": 9.0,

    "devstral-2": 72.2,
    "devstral-2-123b": 72.2,
    "devstral-small-2": 68.0,
    "devstral-small-24b": 68.0,
    "devstral-small": 53.6,
    "devstral-medium": 61.6,

    "minimax-m2.5": 80.2,
    "minimax-m2.7": 80.2,
    "minimax-m2.1": 69.4,
    "minimax-m2": 69.4,
    "minimax-m2.6": 80.2,

    "kimi-k2.6": 80.2,
    "kimi-k2.5": 76.8,
    "kimi-k2-thinking": 71.3,
    "kimi-k2": 59.1,

    "glm-5": 77.8,
    "glm-4.7": 73.8,
    "glm-4.6": 68.0,

    "mistral-large-3": 33.3,
    "mistral-small-4": 46.8,
    "mistral-medium-3": 40.0,
    "mistral-magistral-small": 42.0,
    "mistral-ministral-14b": 38.0,
    "mistral-ministral-8b": 35.0,
    "mistral-ministral-3b": 30.0,
    "mixtral-8x22b": 36.0,

    "muse-spark": 77.4,
    "llama-4-maverick": 70.7,
    "llama-4-scout": 44.0,
    "llama-3.3-70b": 48.0,
    "llama-3.1-405b": 47.0,
    "llama-3.1-8b": 23.0,

    "mimo-v2-pro": 78.0,
    "mimo-v2-omni": 74.8,
    "mimo-v2-flash": 73.4,

    "seed-2.0-pro": 76.5,
    "seed-2.0-lite": 73.5,
    "seed-oss-36b": 26.0,

    "step-3.5-flash": 74.4,

    "longcat-flash-thinking": 70.0,
    "longcat-flash": 70.0,

    "grok-4": 73.5,
    "grok-code-fast-1": 57.6,
    "grok-3-beta": 53.3,
    "grok-3-mini-beta": 49.3,

    "optimus-alpha": 52.9,
    "quasar-alpha": 54.7,
    "cogito-2.1": 35.0,
    "rnj-1-8b": 18.0,
    "stockmark-100b": 28.0,
    "colosseum-355b": 27.0,
    "granite-34b": 32.0,
    "ibm-granite-34b": 32.0,
    "gpt-oss-20b": 22.0,
}


def normalize_model_name(name: str) -> str:
    """Normalize model name for lookup."""
    normalized = name.lower()
    normalized = re.sub(r'\s*\(.*?\)', '', normalized)
    normalized = re.sub(r'\s*(?:instruct|chat|preview|exp|202[0-9]+).*$', '', normalized, flags=re.I)
    normalized = normalized.strip()
    normalized = re.sub(r'\s+', '-', normalized)  # spaces to hyphens
    normalized = re.sub(r'[^a-z0-9\-.]', '', normalized)  # keep alphanumeric, hyphens, dots
    replacements = {
        "deepseek-v3.1-terminus": "deepseek-v3.1",
        "deepseek-v3-0324": "deepseek-v3",
        "qwen3-coder-flash": "qwen3-coder",
        "qwen3-coder-plus": "qwen3-coder",
        "qwen3-coder-next": "qwen3-coder-next",
        "qwen3-vl": "qwen3",
        "claude-sonnet-4-5": "claude-sonnet-4.5",  # handle 4-5 vs 4.5
        "claude-opus-4-5": "claude-opus-4.5",
        "claude-3-5-sonnet": "claude-3.5-sonnet",
        "gemini-2.5-pro-preview": "gemini-2.5-pro",
        "gemini-2.5-flash-preview": "gemini-2.5-flash",
        "mistral-large-3-675b": "mistral-large-3",
        "mistral-small-4-119b": "mistral-small-4",
        "gpt-5-2": "gpt-5.2",
        "gpt-5-2-codex": "gpt-5.2-codex",
    }
    for old, new in replacements.items():
        if old in normalized:
            normalized = normalized.replace(old, new)
    return normalized

def get_score(model_name: str, model_id: str, provider: str, scores_dict: dict) -> float | None:
    """Get score for a model using model_id as primary key."""
    candidates = [
        f"{provider}/{model_id}".lower(),
        model_id.lower(),
        normalize_model_name(model_id),
        normalize_model_name(model_name),
    ]
    
    for candidate in candidates:
        if candidate in scores_dict:
            return scores_dict[candidate]
    
    normalized_id = normalize_model_name(model_id)
    for key, score in scores_dict.items():
        if key in normalized_id or normalized_id in key:
            return score
    
    return None

def extract_models_from_opencode(config_path: Path) -> list[dict]:
    """Extract all models from opencode.json."""
    with open(config_path) as f:
        config = json.load(f)
    
    models = []
    for provider_name, provider_config in config.get('provider', {}).items():
        for model_id, model_config in provider_config.get('models', {}).items():
            model_name = model_config.get('name', model_id)
            models.append({
                'provider': provider_name,
                'id': model_id,
                'name': model_name,
            })
    return models

def load_or_create_cache(cache_path: Path) -> dict:
    """Load existing cache or create new one."""
    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)
    return {"models": {}, "last_updated": datetime.now().isoformat()}

def save_cache(cache_path: Path, cache: dict):
    """Save cache to file."""
    cache["last_updated"] = datetime.now().isoformat()
    with open(cache_path, 'w') as f:
        json.dump(cache, f, indent=2)

def migrate_cache_entry(old_entry) -> dict:
    """Migrate old cache format (single 'score' or primitive) to new multi-score dict."""
    if isinstance(old_entry, dict) and ("swe_lite" in old_entry or "swe_verified" in old_entry):
        return old_entry

    old_score = None
    if isinstance(old_entry, (int, float)):
        old_score = float(old_entry)
    elif isinstance(old_entry, dict):
        old_score = old_entry.get("score")

    return {
        "swe_lite": None,
        "swe_verified": old_score,
    }

def generate_markdown_table(models: list[dict], cache: dict, online_scores: dict = None) -> str:
    """Generate Markdown table with all scores."""
    table_rows = []

    header = "| Model | Provider | SWE-Lite | SWE-Verified |"
    separator = "|-------|----------|----------|--------------|"
    table_rows = [header, separator]

    if online_scores is None:
        online_scores = {"swe_lite": {}, "swe_verified": {}}

    for model in models:
        name = model['name']
        provider = model['provider']
        model_key = f"{provider}/{model['id']}"

        if model_key in cache["models"]:
            cached = cache["models"][model_key]
            scores = migrate_cache_entry(cached)
            
            if scores.get("swe_lite") is None or scores.get("swe_verified") is None:
                norm_id = normalize_model_name(model['id'])
                norm_name = normalize_model_name(name)
                
                if scores.get("swe_lite") is None:
                    scores["swe_lite"] = (
                        online_scores["swe_lite"].get(norm_id) or 
                        online_scores["swe_lite"].get(norm_name) or
                        get_score(name, model['id'], provider, STATIC_FALLBACK.get("swe_lite", {}))
                    )
                if scores.get("swe_verified") is None:
                    scores["swe_verified"] = (
                        online_scores["swe_verified"].get(norm_id) or 
                        online_scores["swe_verified"].get(norm_name) or
                        get_score(name, model['id'], provider, STATIC_FALLBACK.get("swe_verified", {}))
                    )
                
                cache["models"][model_key] = scores
        else:
            norm_id = normalize_model_name(model['id'])
            norm_name = normalize_model_name(name)
            
            swe_lite = (
                online_scores["swe_lite"].get(norm_id) or 
                online_scores["swe_lite"].get(norm_name) or
                get_score(name, model['id'], provider, STATIC_FALLBACK.get("swe_lite", {}))
            )
            swe_verified = (
                online_scores["swe_verified"].get(norm_id) or 
                online_scores["swe_verified"].get(norm_name) or
                get_score(name, model['id'], provider, STATIC_FALLBACK.get("swe_verified", {}))
            )
            
            scores = {
                "swe_lite": swe_lite,
                "swe_verified": swe_verified,
            }
            cache["models"][model_key] = scores

        swe_lite_str = f"{scores['swe_lite']:.1f}%" if scores['swe_lite'] is not None else "-"
        swe_verified_str = f"{scores['swe_verified']:.1f}%" if scores['swe_verified'] is not None else "-"

        row = f"| {name} | {provider} | {swe_lite_str} | {swe_verified_str} |"
        table_rows.append(row)

    return "\n".join(table_rows)


def generate_filtered_table(models: list[dict], cache: dict, score_type: str, title: str) -> str:
    """Generate a filtered table showing only models with a specific score."""
    table_rows = []
    
    header = f"| Model | Provider | {score_type} |"
    separator = "|-------|----------|-------------|"
    table_rows = [header, separator]
    
    scored_models = []
    for model in models:
        model_key = f"{model['provider']}/{model['id']}"
        scores = cache["models"].get(model_key)
        if isinstance(scores, dict):
            score_val = scores.get(score_type)
            if score_val is not None:
                scored_models.append({
                    "name": model['name'],
                    "provider": model['provider'],
                    "score": score_val
                })
    
    scored_models.sort(key=lambda x: x['score'], reverse=True)
    
    for m in scored_models:
        row = f"| {m['name']} | {m['provider']} | {m['score']:.1f}% |"
        table_rows.append(row)
    
    table = "\n".join(table_rows)
    
    doc = f"""# {title}

**Models with {score_type} scores**  
Total: {len(scored_models)} models  
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{table}


- **SWE-Lite**: mini-swe-agent v2 protocol (comparable across models)
- **SWE-Verified**: Vendor-optimized scaffolds (not directly comparable)
"""
    return doc, len(scored_models)

def main():
    parser = argparse.ArgumentParser(description="Fetch SWE-bench benchmark scores")
    parser.add_argument("--force", action="store_true", help="Force refresh all scores from online sources")
    args = parser.parse_args()
    
    base_path = Path.home() / ".config" / "opencode"
    config_path = base_path / "opencode.json"
    cache_path = base_path / "docs" / "model-benchmarks" / ".scores-cache.json"
    output_path = base_path / "docs" / "model-benchmarks" / "scores.md"
    lite_path = base_path / "docs" / "model-benchmarks" / "scores-lite.md"
    verified_path = base_path / "docs" / "model-benchmarks" / "scores-verified.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("🔍 Extracting models from opencode.json...")
    models = extract_models_from_opencode(config_path)
    print(f" Found {len(models)} models across {len(set(m['provider'] for m in models))} providers")

    print("💾 Loading cache...")
    cache = load_or_create_cache(cache_path)
    print(f" Cache has {len(cache['models'])} existing model entries")

    print("🔄 Migrating cache entries to new format...")
    migrated = 0
    for model_key, entry in list(cache["models"].items()):
        new_entry = migrate_cache_entry(entry)
        if new_entry != entry:
            cache["models"][model_key] = new_entry
            migrated += 1
    print(f" Migrated {migrated} entries")

    online_scores = {"swe_lite": {}, "swe_verified": {}}
    online_fetched = False
    
    try:
        online_scores["swe_lite"], online_scores["swe_verified"] = fetch_swe_bench_scores()
        online_fetched = True
    except Exception as e:
        print(f"⚠️ Could not fetch online scores: {e}")
        print("  Using static fallback data")
    
    print(f"📊 Generating Markdown tables...")

    combined_table = generate_markdown_table(models, cache, online_scores)

    lite_doc, lite_count = generate_filtered_table(models, cache, "swe_lite", "SWE-bench Lite Scores")

    verified_doc, verified_count = generate_filtered_table(models, cache, "swe_verified", "SWE-bench Verified Scores")

    combined_doc = f"""# Model Benchmark Scores

> **Note**: SWE-Lite uses mini-swe-agent v2 (comparable across models). SWE-Verified uses vendor-optimized scaffolds (not directly comparable).

**Total models tracked**: {len(models)}
**Cache updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Online data**: {"Yes" if online_fetched else "Using static fallback"}


{combined_table}


- **SWE-Lite**: SWE-bench Lite scores using mini-swe-agent v2 (300 issues). Lower cost, standardized protocol. Best for comparing models directly.
- **SWE-Verified**: SWE-bench Verified scores (500 issues). Each vendor may use custom scaffold — scores not comparable across providers but indicate maximum potential.


- SWE-bench: https://www.swebench.com/


Run `python3 scripts/fetch-benchmark-scores.py` to refresh scores. The script only adds new models; existing scores are preserved in cache.
Run with `--force` to refresh all scores from online sources.

"""

    with open(output_path, 'w') as f:
        f.write(combined_doc)

    with open(lite_path, 'w') as f:
        f.write(lite_doc)

    with open(verified_path, 'w') as f:
        f.write(verified_doc)

    save_cache(cache_path, cache)

    print(f"\n✅ Tables generated:")
    print(f" Combined: {output_path}")
    print(f" SWE-Lite only: {lite_path}")
    print(f" SWE-Verified only: {verified_path}")
    
    print(f"💾 Cache saved: {cache_path}")
    print(f"\n📈 Statistics (current opencode.json models):")
    current_lite = 0
    current_verified = 0
    for model in models:
        model_key = f"{model['provider']}/{model['id']}"
        scores = cache["models"].get(model_key)
        if scores:
            if scores.get("swe_lite") is not None:
                current_lite += 1
            if scores.get("swe_verified") is not None:
                current_verified += 1
    print(f" Models with SWE-Lite: {current_lite}")
    print(f" Models with SWE-Verified: {current_verified}")
    print(f" Total cached entries: {len(cache['models'])}")

if __name__ == "__main__":
    main()
