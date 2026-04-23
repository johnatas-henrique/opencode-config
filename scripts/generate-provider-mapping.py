#!/usr/bin/env python3
"""
Provider mapping generator for OpenCode model updates.
Fetches or uses cached models.dev API JSON to map OpenCode providers to models.dev sources.
"""

import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "opencode"
API_JSON_PATH = CONFIG_DIR / "scripts" / "models.dev.api.json"
MAPPING_JSON_PATH = CONFIG_DIR / "provider-mapping.json"
OPENCODE_JSON_PATH = CONFIG_DIR / "opencode.json"

PROVIDER_MAPPING_RULES = {
    "grouter-ollama": {"source_provider": "ollama-cloud", "source_type": "direct"},
    "grouter-openrouter": {"source_provider": "openrouter", "source_type": "direct"},
    "grouter-mistral": {"source_provider": "mistral", "source_type": "direct"},
    "grouter-kilocode": {"source_provider": "kilo", "source_type": "direct"},
    "grouter-gemini-cli": {"source_provider": "google", "source_type": "direct"},
    "grouter-gemini-cli": {"source_provider": "google", "source_type": "direct"},
    "grouter-kiro": {"source_type": "dynamic", "strategy": "extract_prefix"},
    "grouter-opencode": {"source_type": "dynamic", "strategy": "extract_prefix"},
    "omniroute": {"source_type": "dynamic", "strategy": "extract_prefix"},
    "regolo": {"source_type": "dynamic", "strategy": "extract_prefix"},
    "sambanova": {"source_type": "dynamic", "strategy": "extract_prefix"},
    "manifest": {"ignore": True, "reason": "Manifest provider uses internal models"},
}

PREFIX_MAPPING = {
    "anthropic/": "anthropic",
    "google/": "google",
    "moonshotai/": "moonshotai",
    "openrouter/": "openrouter",
    "mistralai/": "mistral",
    "deepseek-ai/": "deepseek",
    "minimaxai/": "minimax",
    "qwen/": "alibaba",
    "meta/": "meta",
    "nvidia/": "nvidia",
    "microsoft/": "microsoft",
    "bytedance/": "bytedance",
    "ibm/": "ibm",
    "stepfun-ai/": "stepfun",
    "alibaba/": "alibaba",
    "302ai/": "302ai",
    "groq/": "groq",
    "cohere/": "cohere",
    "fireworks-ai/": "fireworks-ai",
    "cerebras/": "cerebras",
    "together/": "togetherai",
    "perplexity/": "perplexity",
    "ai21/": "ai21",
    "databricks/": "databricks",
    "langchain/": "langchain",
    "hf-inference/": "huggingface",
}

def load_models_dev_api(api_path: Path) -> dict:
    """Load models.dev API JSON, skip non-JSON lines."""
    if not api_path.exists():
        print(f"ERROR: models.dev API JSON not found at {api_path}")
        print("Please fetch it first with: curl -s https://models.dev/api.json > ~/.config/opencode/models.dev.api.json")
        sys.exit(1)

    with open(api_path, 'r') as f:
        content = f.read().strip()

    start = content.find('{')
    end = content.rfind('}') + 1
    if start == -1 or end == 0:
        print("ERROR: Invalid JSON in models.dev API file")
        sys.exit(1)

    json_str = content[start:end]
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decode error: {e}")
        sys.exit(1)

    return data

def build_provider_mapping(opencode_json: dict, models_dev_data: dict) -> dict:
    """Build mapping from OpenCode providers to models.dev sources."""
    mapping = {
        "generated_at": "2025-12-19T00:00:00Z",
        "strategies": {
            "direct": "Provider name maps directly to models.dev provider key",
            "dynamic": "Provider is a router; extract prefix from model ID"
        },
        "providers": {},
        "dynamic_prefix_mapping": PREFIX_MAPPING,
        "notes": []
    }

    providers_section = opencode_json.get("provider", {})

    for oc_provider_name in providers_section:
        if oc_provider_name == "manifest":
            mapping["providers"][oc_provider_name] = {
                "ignore": True,
                "reason": "Manifest provider uses internal model definitions"
            }
            continue

        rule = PROVIDER_MAPPING_RULES.get(oc_provider_name)
        if rule:
            if rule.get("ignore"):
                mapping["providers"][oc_provider_name] = rule
            elif rule["source_type"] == "direct":
                provider_key = rule["source_provider"]
                if provider_key in models_dev_data:
                    mapping["providers"][oc_provider_name] = {
                        "source_provider": provider_key,
                        "source_type": "direct",
                        "available": True
                    }
                else:
                    mapping["providers"][oc_provider_name] = {
                        "source_provider": provider_key,
                        "source_type": "direct",
                        "available": False,
                        "error": f"Provider '{provider_key}' not found in models.dev"
                    }
            elif rule["source_type"] == "dynamic" and rule["strategy"] == "extract_prefix":
                mapping["providers"][oc_provider_name] = {
                    "source_type": "dynamic",
                    "strategy": "extract_prefix",
                    "note": "Will extract prefix from each model ID at runtime"
                }
        else:
            inferred = oc_provider_name.replace("grouter-", "").replace("openrouter-", "")
            if inferred in models_dev_data:
                mapping["providers"][oc_provider_name] = {
                    "source_provider": inferred,
                    "source_type": "direct",
                    "inferred": True
                }
            else:
                mapping["providers"][oc_provider_name] = {
                    "source_type": "dynamic",
                    "strategy": "extract_prefix",
                    "inferred": True,
                    "note": "No direct match; treating as router with prefixed model IDs"
                }

    return mapping

def main():
    try:
        with open(OPENCODE_JSON_PATH, 'r') as f:
            opencode_json = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: opencode.json not found at {OPENCODE_JSON_PATH}")
        sys.exit(1)

    models_dev_data = load_models_dev_api(API_JSON_PATH)

    mapping = build_provider_mapping(opencode_json, models_dev_data)

    with open(MAPPING_JSON_PATH, 'w') as f:
        json.dump(mapping, f, indent=2)

    print(f"✅ Provider mapping generated: {MAPPING_JSON_PATH}")

    total = len(mapping["providers"])
    direct = sum(1 for v in mapping["providers"].values() if v.get("source_type") == "direct")
    dynamic = sum(1 for v in mapping["providers"].values() if v.get("source_type") == "dynamic")
    ignored = sum(1 for v in mapping["providers"].values() if v.get("ignore"))

    print(f"   Total providers: {total}")
    print(f"   Direct mappings: {direct}")
    print(f"   Dynamic (router): {dynamic}")
    print(f"   Ignored: {ignored}")

    print("\n⚠️  Review this file before running the update script.")
    print("   Check the 'providers' section and adjust any 'source_provider' or 'source_type' values.")

if __name__ == "__main__":
    main()
