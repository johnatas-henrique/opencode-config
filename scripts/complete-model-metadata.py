#!/usr/bin/env python3
"""
Complete model-overrides.json by ensuring every model from target providers
has both 'modalities' and 'limit' defined, using opencode.json as source for limits.
"""
import json
import sys
from pathlib import Path

BASE_DIR = Path.home() / ".config/opencode"
OPENCODE_PATH = BASE_DIR / "opencode.json"
OVERRIDES_PATH = BASE_DIR / "model-overrides.json"

TARGET_PROVIDERS = [
    "nvidia", "sambanova",
    "grouter-kiro", "grouter-openrouter", "grouter-kilocode",
    "grouter-opencode", "grouter-gemini-cli", "grouter-ollama", "grouter-mistral"
]

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    opencode = load_json(OPENCODE_PATH)
    overrides = load_json(OVERRIDES_PATH)

    providers_cfg = opencode.get("provider", {})
    
    total_models = 0
    added_modalities = 0
    added_limit = 0
    cleaned_entries = 0

    for provider_key in TARGET_PROVIDERS:
        if provider_key not in providers_cfg:
            continue
        prov_models = providers_cfg[provider_key].get("models", {})
        ov_provider = overrides.setdefault(provider_key, {})
        
        for model_id, model_cfg in prov_models.items():
            total_models += 1
            ov_model = ov_provider.setdefault(model_id, {})
            
            if "modalities" not in ov_model:
                lower = model_id.lower()
                if any(tag in lower for tag in ["vision", "vl", "image", "maverick", "scout"]):
                    ov_model["modalities"] = {"input": ["text", "image"], "output": ["text"]}
                elif any(tag in lower for tag in ["audio", "voxtral"]):
                    ov_model["modalities"] = {"input": ["text", "audio"], "output": ["text"]}
                else:
                    ov_model["modalities"] = {"input": ["text"], "output": ["text"]}
                added_modalities += 1
            
            if "limit" not in ov_model:
                limit_from_cfg = model_cfg.get("limit")
                if limit_from_cfg:
                    ov_model["limit"] = limit_from_cfg
                    added_limit += 1
                else:
                    ov_model["limit"] = {"context": 131072, "output": 8192}
                    added_limit += 1

        to_remove = []
        for mid, mdata in ov_provider.items():
            if not mdata or ("modalities" not in mdata and "limit" not in mdata):
                to_remove.append(mid)
        for mid in to_remove:
            del ov_provider[mid]
            cleaned_entries += 1

    save_json(overrides, OVERRIDES_PATH)

    print(f"✅ Completion finished:")
    print(f"   Total models processed: {total_models}")
    print(f"   Added modalities: {added_modalities}")
    print(f"   Added limit: {added_limit}")
    print(f"   Cleaned empty entries: {cleaned_entries}")
    print(f"   Saved: {OVERRIDES_PATH}")

if __name__ == "__main__":
    main()
