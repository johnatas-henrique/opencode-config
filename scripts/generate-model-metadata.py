#!/usr/bin/env python3
"""
Generate model metadata (modalities, limits) for providers in opencode.json.
Principal fonte: models.dev.api.json (já contém modalities e limits para a maioria).
Para modelos ausentes, tenta fetch de endpoints locais grouter ou inferência.
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict
import os
import requests

PROVIDER_PORTS = {
    "grouter-kiro": 3102,
    "grouter-openrouter": 3101,
    "grouter-kilocode": 3103,
    "grouter-opencode": 3105,
    "grouter-gemini-cli": 3107,
    "grouter-ollama": 3108,
    "grouter-mistral": 3110,
    "grouter-nvidia": 3111,
    "grouter-modal": 3109,
}

BASE_DIR = Path.home() / ".config/opencode"
OPENCODE_PATH = BASE_DIR / "opencode.json"
MODELS_DEV_API_PATH = BASE_DIR / "scripts" / "models.dev.api.json"

def load_models_dev_api() -> Dict:
    if not MODELS_DEV_API_PATH.exists():
        print(f"⚠️  models.dev.api.json não encontrado em {MODELS_DEV_API_PATH}")
        return {}
    with open(MODELS_DEV_API_PATH) as f:
        raw = json.load(f)
    flat = {}
    for provider_entry in raw.values():
        if isinstance(provider_entry, dict) and "models" in provider_entry:
            models_dict = provider_entry["models"]
        elif isinstance(provider_entry, dict):
            models_dict = provider_entry
        else:
            continue
        for model_id, model_data in models_dict.items():
            flat[model_id] = model_data
    return flat

def fetch_grouter_models(port: int) -> Dict[str, Dict]:
    url = f"http://localhost:{port}/v1/models"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        models = []
        if isinstance(data, dict):
            if "models" in data and isinstance(data["models"], list):
                models = data["models"]
            elif "data" in data and isinstance(data["data"], list):
                models = data["data"]
            else:
                for v in data.values():
                    if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v:
                        models = v
                        break
        elif isinstance(data, list):
            models = data
        result = {}
        for m in models:
            mid = m.get("id")
            if not mid:
                continue
            modalities = m.get("modalities")
            ctx = None
            out = None
            for field in ["context_window", "max_context", "context_length", "max_position_embeddings", "n_ctx", "context"]:
                if field in m and isinstance(m[field], (int, float)):
                    ctx = int(m[field])
                    break
            for field in ["max_output_tokens", "max_tokens", "completion_window", "max_completion_tokens", "max_new_tokens"]:
                if field in m and isinstance(m[field], (int, float)):
                    out = int(m[field])
                    break
            limit = {"context": ctx, "output": out} if ctx or out else None
            result[mid] = {"modalities": modalities, "limit": limit}
        return result
    except Exception:
        return {}

def infer_modalities(model_id: str) -> Dict:
    lower = model_id.lower()
    if any(tag in lower for tag in ["vision", "vl", "image", "maverick", "scout"]):
        return {"input": ["text", "image"], "output": ["text"]}
    if any(tag in lower for tag in ["audio", "voxtral"]):
        return {"input": ["text", "audio"], "output": ["text"]}
    return {"input": ["text"], "output": ["text"]}

def main():
    dry_run = False
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--dry-run":
            dry_run = True
        i += 1

    with open(OPENCODE_PATH) as f:
        opencode = json.load(f)

    models_dev_data = load_models_dev_api()

    providers_cfg = opencode.get("provider", {})
    all_providers = list(providers_cfg.keys())

    TARGET_DIRECT_FIELDS = ["modalities", "limit"]
    TARGET_OPTIONS_FIELDS = ["tool_call", "reasoning"]

    all_target_fields = TARGET_DIRECT_FIELDS + TARGET_OPTIONS_FIELDS
    summary = {
        "total_models": 0,
        "models_changed": 0,
        "models_unchanged": 0,
        "fields_added": {f: 0 for f in all_target_fields},
    }

    print("🔍 Gerando metadata para todos os providers...\n")

    for provider_key in all_providers:
        prov = providers_cfg.get(provider_key, {})
        models_cfg = prov.get("models", {})
        model_ids = list(models_cfg.keys())
        total_provider = len(model_ids)
        if total_provider == 0:
            continue

        print(f"📦 {provider_key} ({total_provider} modelos)")
        made_change = False

        for mid in model_ids:
            model_entry = models_cfg[mid]
            summary["total_models"] += 1

            src_data = None
            if mid in models_dev_data:
                src_data = models_dev_data[mid]

            if not src_data and provider_key.startswith("grouter-") and provider_key in PROVIDER_PORTS:
                port = PROVIDER_PORTS[provider_key]
                fetched = fetch_grouter_models(port)
                if mid in fetched:
                    src_data = fetched[mid]

            changed = False
            if src_data:
                for field in TARGET_DIRECT_FIELDS:
                    val = src_data.get(field)
                    if val is not None and field not in model_entry:
                        model_entry[field] = val
                        changed = True
                        summary["fields_added"][field] += 1

                opts = model_entry.get("options")
                if opts is None:
                    opts = {}
                    model_entry["options"] = opts
                for field in TARGET_OPTIONS_FIELDS:
                    val = src_data.get(field)
                    if val is not None and field not in opts:
                        opts[field] = val
                        changed = True
                        summary["fields_added"][field] += 1

            if changed:
                made_change = True

        if made_change:
            print(f"  ✓ Atualizado")
            summary["models_changed"] += 1
        else:
            print(f"  ≡ Sem mudanças")
            summary["models_unchanged"] += 1

    if not dry_run:
        with open(OPENCODE_PATH, "w") as f:
            json.dump(opencode, f, indent=2)
        print(f"\n✅ opencode.json atualizado")
    else:
        print("\n💾 Dry-run: não salvou")

    print("\n📊 Summary:")
    print(f"  Total models processed: {summary['total_models']}")
    print(f"  Models changed: {summary['models_changed']}")
    print(f"  Models unchanged: {summary['models_unchanged']}")
    print("  Fields added:")
    for field, count in summary["fields_added"].items():
        print(f"    {field}: {count}")

if __name__ == "__main__":
    main()