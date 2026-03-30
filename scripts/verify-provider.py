#!/usr/bin/env python3
"""
Provider verification script for grouter/external providers.

Tests:
1. GET /v1/models - list available models
2. For each model: POST /v1/chat/completions with simple prompt

Outputs:
- ok.json - models that responded successfully
- fail.json - models that failed or timed out
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import requests


def test_models_endpoint(base_url: str, api_key: str = "grouter") -> Tuple[bool, List[str]]:
    """Test /v1/models endpoint and return list of model IDs."""
    url = f"{base_url.rstrip('/')}/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"❌ Models endpoint returned {resp.status_code}: {resp.text[:200]}")
            return False, []
        
        data = resp.json()
        
        # Debug: show what we got
        print(f"ℹ️  Response type: {type(data)}")
        if isinstance(data, dict):
            print(f"   Keys: {list(data.keys())}")
            if "models" in data and isinstance(data["models"], list):
                models = [m.get("id") for m in data["models"] if m.get("id")]
            elif "data" in data and isinstance(data["data"], list):
                models = [m.get("id") for m in data["data"] if m.get("id")]
            else:
                # Try to find any list field that might contain models
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict) and "id" in value[0]:
                        models = [m.get("id") for m in value if m.get("id")]
                        print(f"   Found models in field '{key}'")
                        break
                else:
                    print(f"❌ Could not find models list in response")
                    return False, []
        elif isinstance(data, list):
            models = [m.get("id") for m in data if m.get("id")]
        else:
            print(f"❌ Unexpected response: {type(data)}")
            return False, []
        
        print(f"✅ Found {len(models)} models")
        return True, models
    except Exception as e:
        print(f"❌ Error fetching models: {e}")
        return False, []


def test_chat_completion(base_url: str, model_id: str, api_key: str, prompt: str = "Hello", timeout: int = 15) -> Tuple[bool, float, str]:
    """Test chat completion for a specific model. Returns (success, latency_seconds, error)."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 10  # Keep response short
    }
    
    start = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        latency = time.time() - start
        
        if resp.status_code in (200, 201):
            data = resp.json()
            if "choices" in data and len(data["choices"]) > 0:
                return True, latency, ""
            return False, latency, f"Malformed response: {resp.text[:100] if resp.text else 'empty'}"
        return False, latency, f"HTTP {resp.status_code}: {resp.text[:100] if resp.text else 'no body'}"
    except requests.exceptions.Timeout:
        return False, timeout, "Timeout"
    except Exception as e:
        return False, time.time() - start, str(e)[:100]


def fetch_models_list(base_url: str, api_key: str) -> Tuple[bool, List[Dict]]:
    """Fetch full models list from /v1/models (with details)."""
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify-provider.py <port> [--api-key KEY] [--prompt TEXT] [--output-dir DIR]")
        print("Example: python3 verify-provider.py 3109 --api-key grouter")
        sys.exit(1)
    
    # First arg is the port number
    port = sys.argv[1]
    if not port.isdigit():
        print(f"❌ Invalid port: {port}")
        sys.exit(1)
    
    base_url = f"http://localhost:{port}/v1"
    api_key = "grouter"
    prompt = "Hello"
    output_dir = Path.cwd()
    provider_name = None  # Will be detected from models
    
    # Parse optional args
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--api-key" and i + 1 < len(args):
            api_key = args[i + 1]
            i += 2
        elif args[i] == "--prompt" and i + 1 < len(args):
            prompt = args[i + 1]
            i += 2
        elif args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = Path(args[i + 1])
            output_dir.mkdir(parents=True, exist_ok=True)
            i += 2
        else:
            i += 1
    
    print(f"🌐 URL: {base_url}")
    print(f"🔑 Using API key: {api_key}")
    print(f"💬 Test prompt: '{prompt}'")
    print()
    
    # Step 1: Get models list
    success, model_ids = test_models_endpoint(base_url, api_key)
    if not success or not model_ids:
        print("❌ Failed to retrieve models. Aborting.")
        sys.exit(1)
    
    # Try to detect provider name from owned_by of first model
    if provider_name is None:
        success, models_list = fetch_models_list(base_url, api_key)
        if success and models_list:
            first_model = models_list[0]
            owned_by = extract_owned_by(first_model, f"localhost{port}")
            provider_name = owned_by
        else:
            provider_name = f"localhost{port}"
    
    print(f"🔍 Detected provider: {provider_name}")
    
    # Try to detect provider name from owned_by of first model
    if provider_name is None:
        # Fetch models list again to get owned_by
        success, models_list = fetch_models_list(base_url, api_key)
        if success and models_list:
            first_model = models_list[0]
            owned_by = extract_owned_by(first_model, f"localhost{port}")
            provider_name = owned_by
        else:
            provider_name = f"localhost{port}"
    
    print(f"🔍 Detected provider: {provider_name}")
    
    print(f"\n🧪 Testing {len(model_ids)} models with chat completion...\n")
    
    # Step 2: Test each model
    ok_models = []
    fail_models = []
    
    for i, model_id in enumerate(model_ids, 1):
        print(f"[{i}/{len(model_ids)}] Testing: {model_id}...", end=" ", flush=True)
        success, latency, error = test_chat_completion(base_url, model_id, api_key, prompt, timeout=15)
        
        if success:
            ok_models.append({"model": model_id, "latency": round(latency, 3)})
            print(f"✅ OK ({latency:.2f}s)")
        else:
            fail_models.append({"model": model_id, "error": error, "latency": round(latency, 3)})
            print(f"❌ FAILED: {error}")
    
    # Step 3: Write outputs
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {
        "provider": provider_name,
        "url": base_url,
        "tested_at": timestamp,
        "total_models": len(model_ids),
        "working": len(ok_models),
        "failed": len(fail_models),
        "ok_models": ok_models,
        "fail_models": fail_models
    }
    
    # Use provider name for file naming
    safe_name = provider_name.replace(':', '-').replace('/', '-')
    ok_path = output_dir / f"{safe_name}-ok.json"
    fail_path = output_dir / f"{safe_name}-fail.json"
    
    with open(ok_path, 'w') as f:
        json.dump({"summary": summary, "models": ok_models}, f, indent=2)
    
    with open(fail_path, 'w') as f:
        json.dump({"summary": summary, "models": fail_models}, f, indent=2)
    
    # Also create simple txt versions for quick reading
    ok_txt = output_dir / f"{safe_name}-ok.txt"
    fail_txt = output_dir / f"{safe_name}-fail.txt"
    
    with open(ok_txt, 'w') as f:
        f.write(f"# Provider: {provider_name}\n")
        f.write(f"# URL: {base_url}\n")
        f.write(f"# Tested: {timestamp}\n")
        f.write(f"# Working: {len(ok_models)}/{len(model_ids)}\n\n")
        for m in ok_models:
            f.write(f"{m['model']}: OK (latency: {m['latency']}s)\n")
    
    with open(fail_txt, 'w') as f:
        f.write(f"# Provider: {provider_name}\n")
        f.write(f"# URL: {base_url}\n")
        f.write(f"# Tested: {timestamp}\n")
        f.write(f"# Failed: {len(fail_models)}/{len(model_ids)}\n\n")
        for m in fail_models:
            f.write(f"{m['model']}: {m['error']}\n")
    
    print(f"\n📊 Results:")
    print(f"   ✅ Working: {len(ok_models)}")
    print(f"   ❌ Failed: {len(fail_models)}")
    print(f"\n💾 Saved:")
    print(f"   - {ok_path}")
    print(f"   - {fail_path}")
    print(f"   - {ok_txt}")
    print(f"   - {fail_txt}")


if __name__ == "__main__":
    main()
