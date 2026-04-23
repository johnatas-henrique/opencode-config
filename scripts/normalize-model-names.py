#!/usr/bin/env python3
"""
Normalize model names in opencode.json with format:
{name} | SWE[-L/V]: X% | {ctx}K/{out}K | [MODALITIES...]

Usage:
    python3 scripts/normalize-model-names.py --dry-run    # Show changes without saving
    python3 scripts/normalize-model-names.py --apply      # Save to opencode.json
    python3 scripts/normalize-model-names.py --output <file>  # Save to different file
"""
import argparse
import json
from pathlib import Path


def build_dev_api_index(dev_api_path: Path) -> dict:
    """Build index of model names from models.dev.api.json
    
    Prioritizes names with proper formatting (spaces > dashes).
    """
    if not dev_api_path.exists():
        print(f"  ⚠️  {dev_api_path} not found, using original names")
        return {}
    
    with open(dev_api_path) as f:
        data = json.load(f)
    
    index = {}
    for provider, provider_data in data.items():
        models = provider_data.get('models', {})
        for model_id, model_info in models.items():
            model_name = model_info.get('name', model_id)
            key = model_id.lower()
            
            if key in index:
                existing = index[key]
                if ' ' in model_name and ' ' not in existing:
                    index[key] = model_name
            else:
                index[key] = model_name
    
    print(f"  📦 Loaded {len(index)} model names from {dev_api_path.name}")
    return index


def load_scores_cache(cache_path: Path) -> dict:
    """Load SWE scores from cache"""
    if not cache_path.exists():
        print(f"  ⚠️  {cache_path} not found, SWE scores will be -")
        return {"models": {}}
    
    with open(cache_path) as f:
        data = json.load(f)
    
    return data


def format_number(n: int) -> str:
    """Format number to K or M"""
    if n >= 1000000:
        return f"{n/1000000:.1f}M".replace('.0M', 'M')
    return f"{n//1000}K"


def format_modalities(modalities: dict) -> str:
    """Format modalities to CAPS string in fixed order: IMAGE/AUDIO/PDF/VIDEO"""
    input_mods = modalities.get('input', ['text'])
    output_mods = modalities.get('output', ['text'])
    all_mods = set(input_mods + output_mods)
    
    non_text = [m.upper() for m in all_mods if m != 'text']
    
    preferred_order = ['IMAGE', 'AUDIO', 'PDF', 'VIDEO']
    
    ordered_mods = [mod for mod in preferred_order if mod in non_text]
    
    other_mods = sorted([mod for mod in non_text if mod not in preferred_order])
    ordered_mods.extend(other_mods)
    
    if ordered_mods:
        return f" | [{'/'.join(ordered_mods)}]"
    return ""


def get_swe_string(cache_entry: dict) -> str:
    """Get SWE score string (prefer Lite, fallback to Verified)"""
    swe_lite = cache_entry.get('swe_lite')
    swe_verified = cache_entry.get('swe_verified')
    
    if swe_lite is not None:
        return f"SWE-L: {swe_lite:.1f}%"
    elif swe_verified is not None:
        return f"SWE-V: {swe_verified:.1f}%"
    return "SWE: -"


def should_use_dev_api_name(current_name: str, model_id: str, dev_name: str) -> bool:
    """Decide whether to use dev API name or keep current name"""
    if '(' in current_name:
        return False
    
    simple_id = model_id.split('/')[-1].lower()
    generic_names = {'auto', 'latest', 'default', 'standard', 'basic', 'premium', 'free'}
    if simple_id in generic_names:
        return False
    
    current_lower = current_name.lower().replace(' ', '-').replace('_', '-')
    if current_lower == simple_id and dev_name.lower() != simple_id:
        return True
    
    return False


def format_model_name(
    current_name: str,
    model_id: str,
    dev_api_index: dict,
    cache_entry: dict,
    limit: dict,
    modalities: dict
) -> str:
    """Format model name with all information, avoiding duplication"""
    
    simple_id = model_id.split('/')[-1].lower()
    dev_name = dev_api_index.get(simple_id, current_name)
    
    if should_use_dev_api_name(current_name, model_id, dev_name):
        official_name = dev_name
    else:
        if ' | ' in current_name:
            official_name = current_name.split(' | ')[0].strip()
        else:
            official_name = current_name
    
    swe_str = get_swe_string(cache_entry)
    
    ctx = limit.get('context', 0) if limit else 0
    out = limit.get('output', 0) if limit else 0
    ctx_str = format_number(ctx)
    out_str = format_number(out)
    
    mod_str = format_modalities(modalities) if modalities else ""
    
    suffix = f"{swe_str} | {ctx_str}/{out_str}{mod_str}"
    
    if ' | ' in current_name:
        existing_parts = current_name.split(' | ', 1)[1] if ' | ' in current_name else ''
        if existing_parts.strip() != suffix.strip():
            return f"{official_name} | {suffix}"
        else:
            return current_name
    else:
        return f"{official_name} | {suffix}"


def process_config(config: dict, dev_api_index: dict, cache: dict) -> dict:
    """Process all models in config and return updated config"""
    changes = []
    
    for provider_name, provider_config in config.get('provider', {}).items():
        models = provider_config.get('models', {})
        
        for model_id, model_config in models.items():
            current_name = model_config.get('name', model_id)
            
            cache_key = f"{provider_name}/{model_id}"
            cache_entry = cache.get('models', {}).get(cache_key, {})
            
            limit = model_config.get('limit', {})
            modalities = model_config.get('modalities', {})
            
            new_name = format_model_name(
                current_name=current_name,
                model_id=model_id,
                dev_api_index=dev_api_index,
                cache_entry=cache_entry,
                limit=limit,
                modalities=modalities
            )
            
            if new_name != current_name:
                changes.append({
                    'provider': provider_name,
                    'model_id': model_id,
                    'old_name': current_name,
                    'new_name': new_name
                })
            
            model_config['name'] = new_name
    
    return config, changes


def main():
    parser = argparse.ArgumentParser(description="Normalize model names in opencode.json")
    parser.add_argument('--dry-run', action='store_true', help='Show changes without saving')
    parser.add_argument('--apply', action='store_true', help='Save to opencode.json')
    parser.add_argument('--output', type=str, help='Save to specified file')
    args = parser.parse_args()
    
    base_path = Path.home() / ".config" / "opencode"
    config_path = base_path / "opencode.json"
    dev_api_path = base_path / "scripts" / "models.dev.api.json"
    cache_path = base_path / "docs" / "model-benchmarks" / ".scores-cache.json"
    
    print("🔍 Loading configuration files...")
    
    with open(config_path) as f:
        config = json.load(f)
    
    print("📦 Building dev API index...")
    dev_api_index = build_dev_api_index(dev_api_path)
    
    print("📊 Loading SWE scores cache...")
    cache = load_scores_cache(cache_path)
    
    print("✏️  Processing models...")
    updated_config, changes = process_config(config, dev_api_index, cache)
    
    print(f"\n📋 Found {len(changes)} changes:\n")
    for change in changes:
        print(f"  {change['provider']}/{change['model_id']}:")
        print(f"    OLD: {change['old_name']}")
        print(f"    NEW: {change['new_name']}")
        print()
    
    if args.dry_run:
        print("💡 --dry-run: No files were modified.")
    elif args.output:
        output_path = base_path / args.output
        with open(output_path, 'w') as f:
            json.dump(updated_config, f, indent=2)
        print(f"✅ Saved to {output_path}")
    elif args.apply:
        with open(config_path, 'w') as f:
            json.dump(updated_config, f, indent=2)
        print(f"✅ Updated {config_path}")
    else:
        print("💡 Use --dry-run, --apply, or --output <file>")


if __name__ == "__main__":
    main()