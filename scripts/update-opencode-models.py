#!/usr/bin/env python3
"""
Update OpenCode provider models with data from models.dev API.
Uses provider-mapping.json to map OpenCode providers to models.dev sources.
Saves backup before modifying.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Config paths
CONFIG_DIR = Path.home() / ".config" / "opencode"
OPENCODE_JSON_PATH = CONFIG_DIR / "opencode.json"
MAPPING_JSON_PATH = CONFIG_DIR / "provider-mapping.json"
BACKUP_PATH = CONFIG_DIR / "opencode.json.bak"

def load_json(path: Path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data: dict, path: Path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def ensure_backup():
    if not BACKUP_PATH.exists():
        shutil.copy2(OPENCODE_JSON_PATH, BACKUP_PATH)
        print(f"✅ Backup created: {BACKUP_PATH}")
    else:
        print(f"⚠️  Backup already exists: {BACKUP_PATH}")

def extract_prefix(model_id: str) -> str:
    """Extract prefix before '/' from model ID, or return empty."""
    if '/' in model_id:
        return model_id.split('/', 1)[0] + '/'
    return ''

def map_prefix_to_provider(prefix: str) -> str | None:
    """Map prefix to models.dev provider using dynamic_prefix_mapping."""
    if not prefix:
        return None
    # Load mapping
    mapping = load_json(MAPPING_JSON_PATH)
    prefix_map = mapping.get("dynamic_prefix_mapping", {})
    return prefix_map.get(prefix)

def normalize_id(s: str) -> str:
    """Normalize model ID for fuzzy matching: lowercase, replace separators."""
    return s.lower().replace('-', '').replace('_', '').replace(' ', '')

def get_source_provider_for_model(provider_name: str, model_id: str, mapping: dict, models_dev_data: dict) -> str | None:
    """
    Determine which models.dev provider provides this model.
    Order of resolution:
    1. manual_overrides (exact model_id match)
    2. direct mapping
    3. dynamic prefix extraction
    4. fuzzy ID search across likely providers
    """
    provider_cfg = mapping["providers"].get(provider_name)
    if not provider_cfg:
        return None

    if provider_cfg.get("ignore"):
        return None

    # 1. Manual overrides per provider
    manual_overrides = mapping.get("manual_overrides", {}).get(provider_name, {})
    if model_id in manual_overrides:
        return manual_overrides[model_id]

    # 2. Direct mapping
    if provider_cfg["source_type"] == "direct":
        return provider_cfg["source_provider"]

    # 3. Dynamic prefix extraction
    if provider_cfg["source_type"] == "dynamic" and provider_cfg["strategy"] == "extract_prefix":
        prefix = extract_prefix(model_id)
        if prefix:
            source = map_prefix_to_provider(prefix)
            if source:
                return source

    # 4. Fuzzy search: try to find model by normalized ID across all providers
    # Only for known problematic providers to avoid expensive scans
    if provider_name in ("grouter-kiro", "sambanova"):
        norm_target = normalize_id(model_id)
        # Try across all providers in models.dev
        for p_key, p_val in models_dev_data.items():
            p_models = p_val.get("models", {})
            for m_key, m_val in p_models.items():
                # Compare normalized keys and ids
                if normalize_id(m_key) == norm_target or normalize_id(m_val.get("id", "")) == norm_target:
                    return p_key

    return None

def build_model_entry(models_dev_provider: str, model_data: dict, model_id_in_opencode: str) -> dict:
    """
    Build OpenCode model entry from models.dev data.
    OpenCode model entry should have:
      id (optional), name, limit (context, output), modalities (input/output),
      options (tool_call, reasoning)
    """
    entry = {}

    # id: use the id from models.dev if available, else the key used
    entry["id"] = model_data.get("id", model_id_in_opencode)

    # name: use name from models.dev or fallback
    entry["name"] = model_data.get("name", model_id_in_opencode)

    # limit: context and output (if output missing, omit)
    if "limit" in model_data:
        limit = model_data["limit"]
        entry["limit"] = {}
        if "context" in limit:
            entry["limit"]["context"] = limit["context"]
        if "output" in limit:
            entry["limit"]["output"] = limit["output"]
        # If no output, set to default 8192? User said don't alter unless we have data
        # We'll leave as-is; OpenCode may have defaults

    # modalities: copy if present
    if "modalities" in model_data:
        entry["modalities"] = model_data["modalities"]

    # options: always include tool_call and reasoning (boolean) and any other
    options = {}
    options["tool_call"] = bool(model_data.get("tool_call", False))
    options["reasoning"] = bool(model_data.get("reasoning", False))
    # Also include attachment? Not in original spec but might be useful
    # options["attachment"] = bool(model_data.get("attachment", False))

    entry["options"] = options

    return entry

def main():
    print("🔧 Starting OpenCode model update...")

    # Load files
    opencode = load_json(OPENCODE_JSON_PATH)
    mapping = load_json(MAPPING_JSON_PATH)

    # Ensure backup (only if not already backed up)
    BACKUP_PATH = CONFIG_DIR / "opencode.json.bak"
    if not BACKUP_PATH.exists():
        import shutil
        shutil.copy2(OPENCODE_JSON_PATH, BACKUP_PATH)
        print(f"✅ Backup created: {BACKUP_PATH}")
    else:
        print(f"⚠️  Backup exists: {BACKUP_PATH}")

    # Track changes
    total_updates = 0
    not_found_models = []

    # Load models.dev data once
    models_dev_data = load_json(CONFIG_DIR / "models.dev.api.json")

    providers_section = opencode.get("provider", {})

    for oc_provider_name, provider_obj in providers_section.items():
        if oc_provider_name not in mapping["providers"]:
            print(f"⚠️  Provider '{oc_provider_name}' not in mapping, skipping")
            continue

        provider_mapping = mapping["providers"][oc_provider_name]
        if provider_mapping.get("ignore"):
            print(f"⏭️  Skipping ignored provider: {oc_provider_name}")
            continue

        models_section = provider_obj.get("models", {})

        print(f"\n📦 Processing provider: {oc_provider_name}")
        updates_this_provider = 0

        for model_key in list(models_section.keys()):
            # Find source provider in models.dev
            source_provider = get_source_provider_for_model(oc_provider_name, model_key, mapping, models_dev_data)

            if not source_provider or source_provider not in models_dev_data:
                # Model not found; cannot update
                not_found_models.append((oc_provider_name, model_key))
                continue

            # Look for model in source provider
            source_models = models_dev_data[source_provider].get("models", {})
            model_data = None

            # Try exact match on model_key first
            if model_key in source_models:
                model_data = source_models[model_key]
            else:
                # Try alternative: maybe model_key is different but id matches
                for alt_key, alt_data in source_models.items():
                    if alt_data.get("id") == model_key:
                        model_data = alt_data
                        break

            if not model_data:
                not_found_models.append((oc_provider_name, model_key))
                continue

            # Build new entry
            new_entry = build_model_entry(source_provider, model_data, model_key)

            # Compare with existing? Always replace
            provider_obj["models"][model_key] = new_entry
            updates_this_provider += 1
            total_updates += 1

        print(f"   Updated {updates_this_provider}/{len(models_section)} models")

    # Save updated opencode.json
    save_json(opencode, OPENCODE_JSON_PATH)
    print(f"\n✅ OpenCode updated: {OPENCODE_JSON_PATH}")
    print(f"   Total model entries updated: {total_updates}")

    if not_found_models:
        print(f"\n⚠️  Models not found in models.dev ({len(not_found_models)}):")
        for provider, model in not_found_models[:10]:
            print(f"   - {provider}/{model}")
        if len(not_found_models) > 10:
            print(f"   ... and {len(not_found_models) - 10} more")

    print("\n📋 Recommendations:")
    print("   1. Review the changes in opencode.json")
    print("   2. Test with a few providers to ensure mappings are correct")
    print("   3. If issues, edit provider-mapping.json and re-run")

if __name__ == "__main__":
    import shutil
    main()
