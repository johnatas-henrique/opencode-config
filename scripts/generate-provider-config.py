#!/usr/bin/env python3
"""
Generate provider configuration for opencode.json from verification results.
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


def test_chat_completion(base_url: str, model_id: str, api_key: str, prompt: str, timeout: int) -> Tuple[bool, float, str]:
    """Single test of chat completion."""
    import time
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 10
    }
    
    start = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        latency = time.time() - start
        
        if resp.status_code in (200, 201):
            data = resp.json()
            if "choices" in data and len(data["choices"]) > 0:
                return True, latency, ""
            return False, latency, "Malformed response"
        return False, latency, f"HTTP {resp.status_code}"
    except requests.exceptions.Timeout:
        return False, timeout, "Timeout"
    except Exception as e:
        return False, time.time() - start, str(e)[:50]


def fetch_models_list(base_url: str, api_key: str) -> Tuple[bool, List[Dict]]:
    """Fetch full models list from /v1/models."""
    url = f"{base_url.rstrip('/')}/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return False, []
        
        data = resp.json()
        models = []
        
        if isinstance(data, dict):
            if "models" in data and isinstance(data["models"], list):
                models = data["models"]
            elif "data" in data and isinstance(data["data"], list):
                models = data["data"]
            else:
                for key, value in data.items():
                    if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0]:
                        models = value
                        break
        elif isinstance(data, list):
            models = data
        
        return True, models
    except Exception:
        return False, []


def extract_owned_by(model_info: Dict, default: str) -> str:
    """Extract provider/owner from model info."""
    for field in ["owned_by", "provider", "organization", "org", "vendor", "creator"]:
        value = model_info.get(field)
        if value and isinstance(value, str):
            return value.lower().replace(" ", "-").replace("/", "-")
    
    model_id = model_info.get("id", "")
    if "/" in model_id:
        return model_id.split("/")[0].lower()
    
    return default


def extract_context_limits(model_info: Dict) -> Tuple[Optional[int], Optional[int]]:
    """Extract context window and max output tokens from model info."""
    ctx_fields = ["context_window", "max_context", "context_length", "max_position_embeddings", "n_ctx"]
    output_fields = ["max_output_tokens", "max_tokens", "completion_window", "max_completion_tokens", "max_new_tokens"]
    
    ctx = None
    output = None
    
    for field in ctx_fields:
        if field in model_info and isinstance(model_info[field], (int, float)):
            ctx = int(model_info[field])
            break
    
    for field in output_fields:
        if field in model_info and isinstance(model_info[field], (int, float)):
            output = int(model_info[field])
            break
    
    return ctx, output


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-provider-config.py <results_json> [--output-dir DIR]")
        print("Example: python3 generate-provider-config.py GRouter-OpenRouter-ok.json --output-dir ./configs")
        sys.exit(1)
    
    results_file = Path(sys.argv[1])
    if not results_file.exists():
        print(f"❌ File not found: {results_file}")
        sys.exit(1)
    
    output_dir = Path.cwd()
    
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = Path(args[i + 1])
            output_dir.mkdir(parents=True, exist_ok=True)
            i += 2
        else:
            i += 1
    
    print(f"📖 Reading results: {results_file}")
    
    with open(results_file) as f:
        data = json.load(f)
    
    summary = data.get("summary", {})
    provider_name = summary.get("provider", "unknown")
    base_url = summary.get("url", "")
    ok_models = summary.get("ok_models", [])
    fail_models = summary.get("fail_models", [])
    
    all_model_ids = [m["model"] for m in ok_models] + [m["model"] for m in fail_models]
    working_set = set(m["model"] for m in ok_models)
    
    if not all_model_ids:
        print("❌ No models found in results")
        sys.exit(1)
    
    print(f"\n🔍 Fetching model details for {len(all_model_ids)} models...\n")
    
    api_key = "grouter"
    models_data = []
    
    for i, model_id in enumerate(all_model_ids, 1):
        is_working = model_id in working_set
        status = "✅" if is_working else "❌"
        print(f"[{i}/{len(all_model_ids)}] {status} Fetching: {model_id}...", end=" ", flush=True)
        
        success, models_list = fetch_models_list(base_url, api_key)
        model_info = {}
        owned_by = provider_name
        
        if success:
            found = next((mm for mm in models_list if mm.get("id") == model_id), None)
            if found:
                owned_by = extract_owned_by(found, provider_name)
                model_info = found
                print(f"✅ {owned_by}")
            else:
                print("⚠️  Not in model list")
        else:
            print("⚠️  Could not fetch list")
        
        models_data.append({
            "model_id": model_id,
            "owned_by": owned_by,
            "details": model_info,
            "working": is_working
        })
    
    by_owned_by: Dict[str, List[Dict]] = {}
    for m in models_data:
        owner = m["owned_by"]
        by_owned_by.setdefault(owner, []).append(m)
    
    print(f"\n📦 Detected {len(by_owned_by)} provider(s):")
    for owner, models in by_owned_by.items():
        working_count = sum(1 for m in models if m["working"])
        print(f"   - {owner}: {working_count}/{len(models)} working")
    
    providers_output = {}
    for owner, models in by_owned_by.items():
        provider_key = f"grouter-{owner}"
        provider_obj = {
            "npm": "@ai-sdk/openai-compatible",
            "name": f"{owner.title()} via GRouter",
            "options": {
                "baseURL": base_url,
                "apiKey": api_key
            },
            "models": {}
        }
        
        for m in models:
            model_id = m["model_id"]
            model_info = m.get("details", {})
            
            model_obj = {
                "name": model_id.split("/")[-1] if "/" in model_id else model_id,
                "id": model_id,
            }
            
            if "modalities" in model_info:
                model_obj["modalities"] = model_info["modalities"]
            
            ctx, output = extract_context_limits(model_info)
            if ctx or output:
                model_obj["limit"] = {}
                if ctx:
                    model_obj["limit"]["context"] = ctx
                if output:
                    model_obj["limit"]["output"] = output
            
            provider_obj["models"][model_id] = model_obj
        
        providers_output[provider_key] = provider_obj
    
    output_file = output_dir / f"provider-{provider_name.replace(' ', '-').lower()}-config.json"
    
    with open(output_file, 'w') as f:
        json.dump(providers_output, f, indent=None)
    
    print(f"\n✅ Generated provider configuration:")
    print(f"   File: {output_file}")
    print(f"\n📋 Summary:")
    for pkey, pobj in providers_output.items():
        print(f"\n   Provider: {pkey}")
        print(f"   Name: {pobj['name']}")
        print(f"   URL: {pobj['options']['baseURL']}")
        print(f"   Total models: {len(pobj['models'])}")
        working_count = sum(1 for m in models_data if m["owned_by"] == pkey.replace("grouter-", "") and m["working"])
        print(f"   Working: {working_count}")
        
        for mid, minfo in pobj['models'].items():
            extras = []
            if "modalities" in minfo:
                extras.append("modalities")
            if "limit" in minfo:
                extras.append("limit")
            extra_str = f" [{', '.join(extras)}]" if extras else ""
            print(f"     - {mid}{extra_str}")
    
    print(f"\n📝 Next steps:")
    print(f"   1. Review the generated JSON")
    print(f"   2. Copy the entire content (the providers object) into opencode.json under 'provider'")
    print(f"   3. Run: python3 scripts/generate-model-metadata.py to add modalities/limit")
    print(f"   4. Run: python3 scripts/normalize-model-names.py --apply")
    print(f"   5. Run: python3 scripts/fetch-benchmark-scores.py")


if __name__ == "__main__":
    main()
