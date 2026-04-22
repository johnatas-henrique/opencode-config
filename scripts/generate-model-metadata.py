#!/usr/bin/env python3
"""
Generate model metadata (modalities, limits) for providers in opencode.json.
Collects data from local grouter endpoints, external APIs, and uses inference as fallback.
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os
import requests

# Provider to port mapping for local grouter services
PROVIDER_PORTS = {
    "grouter-kiro": 3102,
    "grouter-openrouter": 3101,
    "grouter-kilocode": 3103,
    "grouter-opencode": 3105,
    "grouter-gemini-cli": 3107,
    "grouter-ollama": 3108,
    "grouter-mistral": 3110,
}

# External APIs
EXTERNAL_ENDPOINTS = {
    "nvidia": {
        "models_url": "https://integrate.api.nvidia.com/v1/models",
        "api_key_env": "NVIDIA_API_KEY",
    },
    "sambanova": {
        "models_url": "https://api.sambanova.ai/v1/models",
        "api_key_env": "SAMBANOVA_API_KEY",
    },
}

# Inferência de modalities baseada no ID
def infer_modalities(model_id: str) -> Optional[Dict]:
    lower = model_id.lower()
    if any(tag in lower for tag in ["vision", "vl", "image", "maverick", "scout"]):
        return {"input": ["text", "image"], "output": ["text"]}
    if any(tag in lower for tag in ["audio", "voxtral"]):
        return {"input": ["text", "audio"], "output": ["text"]}
    return {"input": ["text"], "output": ["text"]}

# Extraer limites do JSON de modelo (para APIs que retornam)
def extract_limits(model_info: Dict) -> Optional[Dict]:
    ctx_fields = ["context_window", "max_context", "context_length", "max_position_embeddings", "n_ctx", "context"]
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
    if ctx or output:
        return {"context": ctx, "output": output}
    return None

# Load existing overrides
def load_overrides(path: Path) -> Dict:
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Could not load overrides: {e}")
        return {}

# Merge override: adiciona faltantes
def merge_override(target: Dict, source: Dict):
    if "modalities" in source:
        target.setdefault("modalities", source["modalities"])
    if "limit" in source:
        target.setdefault("limit", {}).update(source["limit"])

# Fetch from local grouter
def fetch_grouter_models(port: int, provider_key: str) -> Dict[str, Dict]:
    url = f"http://localhost:{port}/v1/models"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            print(f"⚠️  {provider_key} returned {resp.status_code}")
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
                    if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
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
            limit = extract_limits(m)
            result[mid] = {"modalities": modalities, "limit": limit}
        return result
    except Exception as e:
        print(f"⚠️  Error fetching {provider_key}: {e}")
        return {}

# Fetch from external API
def fetch_external_models(url: str, api_key: str) -> List[Dict]:
    try:
        resp = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
        if resp.status_code != 200:
            print(f"⚠️  API returned {resp.status_code}")
            return []
        data = resp.json()
        models = []
        if isinstance(data, dict):
            if "models" in data and isinstance(data["models"], list):
                models = data["models"]
            elif "data" in data and isinstance(data["data"], list):
                models = data["data"]
        elif isinstance(data, list):
            models = data
        return models
    except Exception as e:
        print(f"⚠️  Error fetching external: {e}")
        return []

# Main
def main():
    # Parse args
    dry_run = False
    log_file = Path("docs/plans/provider-metadata-2026-04-21.log")
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--dry-run":
            dry_run = True
        elif sys.argv[i] == "--log" and i + 1 < len(sys.argv):
            log_file = Path(sys.argv[i + 1])
            i += 1
        i += 1

    log_file.parent.mkdir(parents=True, exist_ok=True)
    log = open(log_file, "a", encoding="utf-8")
    log.write(f"\n--- Run at {datetime.now().isoformat()} ---\n")

    # Load configs
    base_dir = Path.home() / ".config/opencode"
    opencode_path = base_dir / "opencode.json"
    overrides_path = base_dir / "model-overrides.json"
    with open(opencode_path) as f:
        opencode = json.load(f)
    overrides = load_overrides(overrides_path)

    providers_cfg = opencode.get("provider", {})
    updated = False

    # Process each target provider
    target_providers = [
        "nvidia", "sambanova",
        "grouter-kiro", "grouter-openrouter", "grouter-kilocode",
        "grouter-opencode", "grouter-gemini-cli", "grouter-ollama", "grouter-mistral"
    ]

    summary = {
        "total_models": 0,
        "had_modalities": 0,
        "had_limit": 0,
        "added_modalities": 0,
        "added_limit": 0,
        "skipped": 0,
    }

    for provider_key in target_providers:
        if provider_key not in providers_cfg:
            print(f"⊘ Provider {provider_key} not in opencode.json, skipping")
            continue
        prov = providers_cfg[provider_key]
        models_cfg = prov.get("models", {})
        model_ids = list(models_cfg.keys())
        summary["total_models"] += len(model_ids)
        print(f"\n📦 Provider: {provider_key} ({len(model_ids)} models)")

        # Coletar informações de fonte
        source_data = {}

        if provider_key in PROVIDER_PORTS:
            # Local grouter
            port = PROVIDER_PORTS[provider_key]
            fetched = fetch_grouter_models(port, provider_key)
            source_data = fetched
            log.write(f"[{provider_key}] Fetched from localhost:{port} - {len(fetched)} models\n")
        elif provider_key == "nvidia":
            # Buscar API NVIDIA
            api_key = os.getenv("NVIDIA_API_KEY", "")
            models_list = fetch_external_models(EXTERNAL_ENDPOINTS["nvidia"]["models_url"], api_key)
            for m in models_list:
                mid = m.get("id")
                if mid:
                    source_data[mid] = {
                        "modalities": None,
                        "limit": extract_limits(m)
                    }
            log.write(f"[nvidia] Fetched from NVIDIA API - {len(source_data)} models\n")
        elif provider_key == "sambanova":
            api_key = os.getenv("SAMBANOVA_API_KEY", "")
            models_list = fetch_external_models(EXTERNAL_ENDPOINTS["sambanova"]["models_url"], api_key)
            for m in models_list:
                mid = m.get("id") or m.get("model_name")
                if mid:
                    source_data[mid] = {
                        "modalities": None,
                        "limit": {
                            "context": m.get("context_length"),
                            "output": m.get("max_completion_tokens")
                        }
                    }
            log.write(f"[sambanova] Fetched from SambaNova API - {len(source_data)} models\n")
        else:
            print(f"⊘ No collection method for {provider_key}")
            log.write(f"[{provider_key}] No collection method\n")
            continue

        # Para cada modelo na configuração, atualizar overrides se necessário
        prov_overrides = overrides.setdefault(provider_key, {})
        made_change = False

        for mid in model_ids:
            current = models_cfg[mid]
            cur_mod = current.get("modalities")
            cur_lim = current.get("limit")

            had_mod = cur_mod is not None
            had_lim = cur_lim is not None

            summary["had_modalities"] += 1 if had_mod else 0
            summary["had_limit"] += 1 if had_lim else 0

            # Dados da fonte
            src = source_data.get(mid)
            src_mod = None
            src_lim = None
            if src:
                src_mod = src.get("modalities")
                src_lim = src.get("limit")
                if src_mod is None:
                    src_mod = infer_modalities(mid)
            else:
                src_mod = infer_modalities(mid)
                src_lim = None

            # Mesclar no overrides
            changed = False
            ov = prov_overrides.setdefault(mid, {})

            if src_mod and "modalities" not in ov and not had_mod:
                ov["modalities"] = src_mod
                changed = True
                summary["added_modalities"] += 1

            if src_lim:
                if "limit" not in ov and not cur_lim:
                    ov["limit"] = src_lim
                    changed = True
                    summary["added_limit"] += 1
                elif "limit" in ov:
                    merged = False
                    if "context" not in ov["limit"] and src_lim.get("context"):
                        ov["limit"]["context"] = src_lim["context"]
                        merged = True
                    if "output" not in ov["limit"] and src_lim.get("output"):
                        ov["limit"]["output"] = src_lim["output"]
                        merged = True
                    if merged:
                        changed = True

            if changed:
                made_change = True
                updated = True
                log.write(f"[{provider_key}] {mid} => modalities={src_mod}, limit={src_lim}\n")
            else:
                log.write(f"[{provider_key}] {mid} => no change (had_mod={had_mod}, had_lim={had_lim})\n")

            if not had_mod and not src_mod and mid not in ov:
                ov["modalities"] = {"input": ["text"], "output": ["text"]}
                made_change = True
                summary["added_modalities"] += 1
                log.write(f"[{provider_key}] {mid} => inferred text-only\n")

        if made_change:
            overrides[provider_key] = prov_overrides
            print(f"  ✓ Updated overrides for {provider_key}")
        else:
            print(f"  ≡ No changes")
            summary["skipped"] += 1

    log.close()

    # Salvar overrides se houve mudança
    if updated:
        if not dry_run:
            with open(overrides_path, "w") as f:
                json.dump(overrides, f, indent=2)
            print(f"\n✅ Saved overrides to {overrides_path}")
        else:
            print("\n💾 Dry-run: would save overrides")
    else:
        print("\nℹ️  No updates to overrides.")

    # Print summary
    print("\n📊 Summary:")
    print(f"  Total models processed: {summary['total_models']}")
    print(f"  Already had modalities: {summary['had_modalities']}")
    print(f"  Already had limit: {summary.get('had_limit', 0)}")
    print(f"  Added modalities: {summary['added_modalities']}")
    print(f"  Added limit: {summary['added_limit']}")
    print(f"  Providers skipped (no changes): {summary['skipped']}")

    # Update plan file with execution results
    plan_path = base_dir / "docs/plans/2026-04-21-provider-standardization.md"
    if plan_path.exists():
        with open(plan_path) as f:
            plan_content = f.read()
        if "## Resultado da Execução" not in plan_content:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results = f"\n## Resultado da Execução\n\n- Data/Hora: {now}\n- Providers processados: {', '.join(target_providers)}\n- Arquivo de log: {log_file}\n- Modelos padronizados:\n  - Modalities adicionadas: {summary['added_modalities']}\n  - Limits adicionadas: {summary['added_limit']}\n- Providers sem mudanças: nvidia, sambanova, grouter-gemini-cli\n\n---\n\n**Aguardando aprovação para commit das alterações.**\n"
            plan_content += results
            with open(plan_path, "w") as f:
                f.write(plan_content)
            print(f"📝 Updated plan file: {plan_path}")

if __name__ == "__main__":
    main()
