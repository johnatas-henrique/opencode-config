# Model Benchmark Scores

> **Note**: SWE-Lite uses mini-swe-agent v2 (comparable across models). SWE-Verified uses vendor-optimized scaffolds (not directly comparable).

**Total models tracked**: 240
**Cache updated**: 2026-04-23 19:09:56
**Online data**: Yes

## Quick Reference

| Model | Provider | SWE-Lite | SWE-Verified |
|-------|----------|----------|--------------|
| Google: Gemini 2.5 Flash | SWE-V: 55.1% | 1M/65K | [IMAGE/AUDIO/VIDEO/PDF] | grouter-kilocode | - | 55.1% |
| Google: Gemini 2.5 Pro | SWE-V: 63.8% | 1M/65K | [IMAGE/AUDIO/VIDEO/PDF] | grouter-kilocode | - | 63.8% |
| OpenAI: GPT-4.1 | SWE-L: 23.9% | 1M/32K | [IMAGE/PDF] | grouter-kilocode | 23.9% | 54.6% |
| OpenAI: o3 | SWE-V: 49.8% | 200K/100K | [IMAGE/PDF] | grouter-kilocode | - | 49.8% |
| Gemini 3.1 Flash Lite Preview | SWE-V: 78.0% | 1M/65K | [IMAGE/AUDIO/VIDEO/PDF] | grouter-gemini-cli | - | 78.0% |
| Gemini 2.5 Flash | SWE-L: 46.7% | 1M/65K | [IMAGE/AUDIO/VIDEO/PDF] | grouter-gemini-cli | 46.7% | 55.1% |
| cogito-2.1:671b | SWE-V: 35.0% | 163K/32K | grouter-ollama | - | 35.0% |
| deepseek-v3.1:671b | SWE-L: 38.8% | 163K/163K | grouter-ollama | 38.8% | 73.0% |
| DeepSeek V3.2 | SWE-L: 70.0% | 163K/65K | grouter-ollama | 70.0% | 73.0% |
| devstral-2:123b | SWE-L: 37.5% | 262K/262K | grouter-ollama | 37.5% | 72.2% |
| devstral-small-2:24b | SWE-V: 68.0% | 262K/262K | [IMAGE] | grouter-ollama | - | 68.0% |
| Gemini 3 Flash Preview | SWE-L: 75.8% | 1M/65K | [IMAGE] | grouter-ollama | 75.8% | 78.0% |
| gemma3:12b | SWE: - | 131K/131K | [IMAGE] | grouter-ollama | - | - |
| gemma3:27b | SWE: - | 131K/131K | [IMAGE] | grouter-ollama | - | - |
| gemma3:4b | SWE: - | 131K/131K | [IMAGE] | grouter-ollama | - | - |
| gemma4:31b | SWE: - | 262K/8K | [IMAGE] | grouter-ollama | - | - |
| Zai GLM-4.6 | SWE-V: 68.0% | 202K/131K | grouter-ollama | - | 68.0% |
| GLM 5 | SWE-L: 72.8% | 202K/131K | grouter-ollama | 72.8% | 77.8% |
| gpt-oss:120b | SWE-V: 62.4% | 131K/32K | grouter-ollama | - | 62.4% |
| gpt-oss:20b | SWE-V: 22.0% | 131K/32K | grouter-ollama | - | 22.0% |
| Kimi K2 Thinking | SWE-V: 71.3% | 262K/262K | grouter-ollama | - | 71.3% |
| Kimi K2.5 | SWE-L: 70.8% | 262K/262K | [IMAGE] | grouter-ollama | 70.8% | 76.8% |
| Kimi K2.6 (3x limits) | SWE-V: 80.2% | 256K/8K | [IMAGE] | grouter-ollama | - | 80.2% |
| MiniMax M2 | SWE-L: 75.8% | 204K/128K | grouter-ollama | 75.8% | 69.4% |
| MiniMax M2.1 | SWE-V: 69.4% | 204K/131K | grouter-ollama | - | 69.4% |
| MiniMax M2.5 | SWE-L: 75.8% | 204K/131K | grouter-ollama | 75.8% | 80.2% |
| MiniMax M2.7 | SWE-V: 80.2% | 204K/131K | grouter-ollama | - | 80.2% |
| ministral-3:14b | SWE: - | 262K/128K | [IMAGE] | grouter-ollama | - | - |
| ministral-3:3b | SWE: - | 262K/128K | [IMAGE] | grouter-ollama | - | - |
| ministral-3:8b | SWE: - | 262K/128K | [IMAGE] | grouter-ollama | - | - |
| mistral-large-3:675b | SWE-V: 33.3% | 262K/262K | [IMAGE] | grouter-ollama | - | 33.3% |
| nemotron-3-nano:30b | SWE-V: 49.8% | 1M/131K | grouter-ollama | - | 49.8% |
| nemotron-3-super | SWE: - | 262K/65K | grouter-ollama | - | - |
| Qwen3 Coder Next | SWE-L: 40.0% | 262K/65K | grouter-ollama | 40.0% | 70.6% |
| qwen3-coder:480b | SWE-V: 69.6% | 262K/65K | grouter-ollama | - | 69.6% |
| qwen3-next:80b | SWE-V: 69.6% | 262K/32K | grouter-ollama | - | 69.6% |
| qwen3-vl:235b | SWE-V: 73.1% | 262K/32K | [IMAGE] | grouter-ollama | - | 73.1% |
| qwen3-vl:235b-instruct | SWE-V: 73.1% | 262K/131K | [IMAGE] | grouter-ollama | - | 73.1% |
| qwen3.5:397b | SWE-V: 76.4% | 262K/81K | [IMAGE] | grouter-ollama | - | 76.4% |
| rnj-1:8b | SWE-V: 18.0% | 32K/4K | grouter-ollama | - | 18.0% |
| deepseek-v3.1-terminus | grouter-nvidia | 38.8% | 73.0% |
| devstral-2-123b-instruct-2512 | grouter-nvidia | 37.5% | 72.2% |
| dracarys-llama-3.1-70b-instruct | grouter-nvidia | - | - |
| gemma-2-2b-it | grouter-nvidia | - | - |
| gemma-3-27b-it | grouter-nvidia | - | - |
| gemma-3-4b-it | grouter-nvidia | - | - |
| gemma-3n-e2b-it | grouter-nvidia | - | - |
| gemma-3n-e4b-it | grouter-nvidia | - | - |
| glm-5.1 | grouter-nvidia | 72.8% | 77.8% |
| glm4.7 | grouter-nvidia | - | - |
| gpt-oss-120b | grouter-nvidia | - | 62.4% |
| gpt-oss-20b | grouter-nvidia | - | 22.0% |
| kimi-k2-instruct | grouter-nvidia | - | 59.1% |
| kimi-k2-instruct-0905 | grouter-nvidia | - | 59.1% |
| kimi-k2-thinking | grouter-nvidia | - | 71.3% |
| llama-3.1-405b-instruct | grouter-nvidia | - | 47.0% |
| llama-3.2-11b-vision-instruct | grouter-nvidia | - | - |
| llama-3.2-1b-instruct | grouter-nvidia | - | - |
| llama-3.2-3b-instruct | grouter-nvidia | - | - |
| llama-3.2-90b-vision-instruct | grouter-nvidia | - | - |
| llama-4-maverick-17b-128e-instruct | grouter-nvidia | 21.0% | 70.7% |
| llama-guard-4-12b | grouter-nvidia | - | - |
| magistral-small-2506 | grouter-nvidia | - | - |
| minimax-m2.5 | grouter-nvidia | 75.8% | 80.2% |
| minimax-m2.7 | grouter-nvidia | - | 80.2% |
| ministral-14b-instruct-2512 | grouter-nvidia | - | - |
| mistral-large-3-675b-instruct-2512 | grouter-nvidia | - | 33.3% |
| mistral-nemotron | grouter-nvidia | - | - |
| mistral-small-4-119b-2603 | grouter-nvidia | - | 46.8% |
| mixtral-8x22b-instruct-v0.1 | grouter-nvidia | - | 36.0% |
| mixtral-8x7b-instruct-v0.1 | grouter-nvidia | - | - |
| phi-4-mini-instruct | grouter-nvidia | - | - |
| phi-4-multimodal-instruct | grouter-nvidia | - | - |
| qwen2.5-coder-32b-instruct | grouter-nvidia | - | 9.0% |
| qwen3-coder-480b-a35b-instruct | grouter-nvidia | - | 69.6% |
| qwen3-next-80b-a3b-instruct | grouter-nvidia | - | 69.6% |
| qwen3-next-80b-a3b-thinking | grouter-nvidia | - | 69.6% |
| qwen3.5-122b-a10b | grouter-nvidia | - | 72.0% |
| qwen3.5-397b-a17b | grouter-nvidia | - | 76.4% |
| sarvam-m | grouter-nvidia | - | - |
| seed-oss-36b-instruct | grouter-nvidia | - | 26.0% |
| solar-10.7b-instruct | grouter-nvidia | - | - |
| step-3.5-flash | grouter-nvidia | - | 74.4% |
| stockmark-2-100b-instruct | grouter-nvidia | - | - |
| arctic-embed-l | grouter-nvidia | - | - |
| bge-m3 | grouter-nvidia | - | - |
| codegemma-1.1-7b | grouter-nvidia | - | - |
| codegemma-7b | grouter-nvidia | - | - |
| codellama-70b | grouter-nvidia | - | - |
| codestral-22b-instruct-v0.1 | grouter-nvidia | - | - |
| cosmos-reason2-8b | grouter-nvidia | - | - |
| dbrx-instruct | grouter-nvidia | - | - |
| deepseek-coder-6.7b-instruct | grouter-nvidia | - | - |
| deepseek-v3.2 | grouter-nvidia | 70.0% | 73.0% |
| deplot | grouter-nvidia | - | - |
| embed-qa-4 | grouter-nvidia | - | - |
| fuyu-8b | grouter-nvidia | - | - |
| gemma-2b | grouter-nvidia | - | - |
| gemma-3-12b-it | grouter-nvidia | - | - |
| gemma-4-31b-it | grouter-nvidia | - | - |
| gliner-pii | grouter-nvidia | - | - |
| glm5 | grouter-nvidia | - | - |
| granite-3.0-3b-a800m-instruct | grouter-nvidia | - | - |
| granite-3.0-8b-instruct | grouter-nvidia | - | - |
| granite-34b-code-instruct | grouter-nvidia | - | 32.0% |
| granite-8b-code-instruct | grouter-nvidia | - | - |
| ising-calibration-1-35b-a3b | grouter-nvidia | - | - |
| jamba-1.5-large-instruct | grouter-nvidia | - | - |
| kimi-k2.5 | grouter-nvidia | 70.8% | 76.8% |
| kosmos-2 | grouter-nvidia | - | - |
| llama-3.1-70b-instruct | grouter-nvidia | - | - |
| llama-3.1-8b-instruct | grouter-nvidia | - | 23.0% |
| llama-3.1-nemoguard-8b-content-safety | grouter-nvidia | - | - |
| llama-3.1-nemoguard-8b-topic-control | grouter-nvidia | - | - |
| llama-3.1-nemotron-51b-instruct | grouter-nvidia | - | - |
| llama-3.1-nemotron-70b-instruct | grouter-nvidia | - | - |
| llama-3.1-nemotron-nano-8b-v1 | grouter-nvidia | - | - |
| llama-3.1-nemotron-nano-vl-8b-v1 | grouter-nvidia | - | - |
| llama-3.1-nemotron-safety-guard-8b-v3 | grouter-nvidia | - | - |
| llama-3.1-nemotron-ultra-253b-v1 | grouter-nvidia | - | - |
| llama-3.2-nemoretriever-1b-vlm-embed-v1 | grouter-nvidia | - | - |
| llama-3.2-nemoretriever-300m-embed-v1 | grouter-nvidia | - | - |
| llama-3.2-nv-embedqa-1b-v1 | grouter-nvidia | - | - |
| llama-3.2-nv-embedqa-1b-v2 | grouter-nvidia | - | - |
| llama-3.3-70b-instruct | grouter-nvidia | - | 48.0% |
| llama-3.3-nemotron-super-49b-v1 | grouter-nvidia | - | - |
| llama-3.3-nemotron-super-49b-v1.5 | grouter-nvidia | - | - |
| llama-nemotron-embed-1b-v2 | grouter-nvidia | - | - |
| llama-nemotron-embed-vl-1b-v2 | grouter-nvidia | - | - |
| llama2-70b | grouter-nvidia | - | - |
| llama3-chatqa-1.5-70b | grouter-nvidia | - | - |
| mistral-7b-instruct-v0.3 | grouter-nvidia | - | - |
| mistral-large | grouter-nvidia | - | - |
| mistral-large-2-instruct | grouter-nvidia | - | - |
| mistral-medium-3-instruct | grouter-nvidia | - | 40.0% |
| mistral-nemo-12b-instruct | grouter-nvidia | - | - |
| mistral-nemo-minitron-8b-8k-instruct | grouter-nvidia | - | - |
| mixtral-8x22b-v0.1 | grouter-nvidia | - | 36.0% |
| nemoretriever-parse | grouter-nvidia | - | - |
| nemotron-3-content-safety | grouter-nvidia | - | - |
| nemotron-3-nano-30b-a3b | grouter-nvidia | - | - |
| nemotron-3-super-120b-a12b | grouter-nvidia | - | - |
| nemotron-4-340b-instruct | grouter-nvidia | - | - |
| nemotron-4-340b-reward | grouter-nvidia | - | - |
| nemotron-content-safety-reasoning-4b | grouter-nvidia | - | - |
| nemotron-mini-4b-instruct | grouter-nvidia | - | - |
| nemotron-nano-12b-v2-vl | grouter-nvidia | - | - |
| nemotron-nano-3-30b-a3b | grouter-nvidia | - | - |
| nemotron-parse | grouter-nvidia | - | - |
| neva-22b | grouter-nvidia | - | - |
| nv-embed-v1 | grouter-nvidia | - | - |
| nv-embedcode-7b-v1 | grouter-nvidia | - | - |
| nv-embedqa-e5-v5 | grouter-nvidia | - | - |
| nv-embedqa-mistral-7b-v2 | grouter-nvidia | - | - |
| nvclip | grouter-nvidia | - | - |
| nvidia-nemotron-nano-9b-v2 | grouter-nvidia | - | - |
| palmyra-creative-122b | grouter-nvidia | - | - |
| palmyra-fin-70b-32k | grouter-nvidia | - | - |
| palmyra-med-70b | grouter-nvidia | - | - |
| palmyra-med-70b-32k | grouter-nvidia | - | - |
| phi-3-vision-128k-instruct | grouter-nvidia | - | - |
| phi-3.5-moe-instruct | grouter-nvidia | - | - |
| recurrentgemma-2b | grouter-nvidia | - | - |
| riva-translate-4b-instruct | grouter-nvidia | - | - |
| riva-translate-4b-instruct-v1.1 | grouter-nvidia | - | - |
| sea-lion-7b-instruct | grouter-nvidia | - | - |
| starcoder2-15b | grouter-nvidia | - | - |
| vila | grouter-nvidia | - | - |
| yi-large | grouter-nvidia | - | - |
| zamba2-7b-instruct | grouter-nvidia | - | - |
| Codestral | SWE: - | 262K/8K | grouter-mistral | - | - |
| Codestral (latest) | SWE: - | 256K/4K | grouter-mistral | - | - |
| Devstral 2 | SWE-V: 72.2% | 262K/262K | grouter-mistral | - | 72.2% |
| devstral-latest | SWE: - | 262K/8K | grouter-mistral | - | - |
| Devstral 2 (latest) | SWE-V: 61.6% | 262K/262K | grouter-mistral | - | 61.6% |
| Devstral Medium | SWE-V: 61.6% | 128K/128K | grouter-mistral | - | 61.6% |
| Devstral Small | SWE-V: 68.0% | 128K/128K | grouter-mistral | - | 68.0% |
| labs-mistral-small-creative | SWE: - | 131K/8K | grouter-mistral | - | - |
| magistral-medium-2509 | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| Magistral Medium (latest) | SWE: - | 128K/16K | grouter-mistral | - | - |
| magistral-small-2509 | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| magistral-small-latest | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| Ministral 14B | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| ministral-14b-latest | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| Ministral 3B | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| Ministral 3B (latest) | SWE: - | 128K/128K | grouter-mistral | - | - |
| Ministral 8B | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| Ministral 8B (latest) | SWE: - | 128K/128K | grouter-mistral | - | - |
| Mistral Large 2.1 | SWE: - | 131K/16K | grouter-mistral | - | - |
| Mistral Large 3 | SWE-V: 33.3% | 262K/262K | [IMAGE] | grouter-mistral | - | 33.3% |
| Mistral Large (latest) | SWE: - | 262K/262K | [IMAGE] | grouter-mistral | - | - |
| Mistral Medium 3 | SWE-V: 40.0% | 131K/131K | [IMAGE] | grouter-mistral | - | 40.0% |
| mistral-medium | SWE-V: 40.0% | 131K/8K | grouter-mistral | - | 40.0% |
| Mistral Medium 3.1 | SWE: - | 262K/262K | [IMAGE] | grouter-mistral | - | - |
| Mistral Medium (latest) | SWE: - | 128K/16K | [IMAGE] | grouter-mistral | - | - |
| mistral-vibe-cli-with-tools | SWE: - | 131K/8K | grouter-mistral | - | - |
| mistral-medium-2604 | SWE: - | 131K/8K | grouter-mistral | - | - |
| mistral-medium-3 | SWE-V: 40.0% | 131K/8K | grouter-mistral | - | 40.0% |
| mistral-medium-3-5 | SWE-V: 40.0% | 131K/8K | grouter-mistral | - | 40.0% |
| mistral-medium-3.5 | SWE-V: 40.0% | 131K/8K | grouter-mistral | - | 40.0% |
| mistral-medium-c21211-r0-75 | SWE: - | 131K/8K | grouter-mistral | - | - |
| Mistral Small 3.2 | SWE: - | 128K/16K | [IMAGE] | grouter-mistral | - | - |
| Mistral Small 4 | SWE-V: 46.8% | 256K/256K | [IMAGE] | grouter-mistral | - | 46.8% |
| Mistral Small (latest) | SWE: - | 256K/256K | [IMAGE] | grouter-mistral | - | - |
| mistral-vibe-cli-fast | SWE: - | 131K/8K | grouter-mistral | - | - |
| mistral-vibe-cli-latest | SWE: - | 131K/8K | grouter-mistral | - | - |
| mistral-tiny-2407 | SWE: - | 131K/8K | grouter-mistral | - | - |
| mistral-tiny-latest | SWE: - | 131K/8K | grouter-mistral | - | - |
| open-mistral-nemo | SWE: - | 131K/8K | grouter-mistral | - | - |
| open-mistral-nemo-2407 | SWE: - | 131K/8K | grouter-mistral | - | - |
| mistral-large-pixtral-2411 | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| pixtral-large-2411 | SWE: - | 131K/8K | [IMAGE] | grouter-mistral | - | - |
| Pixtral Large (latest) | SWE: - | 128K/128K | [IMAGE] | grouter-mistral | - | - |
| voxtral-mini-latest | SWE: - | 131K/8K | [AUDIO] | grouter-mistral | - | - |
| voxtral-mini-2507 | SWE: - | 131K/8K | [AUDIO] | grouter-mistral | - | - |
| voxtral-small-2507 | SWE: - | 131K/8K | [AUDIO] | grouter-mistral | - | - |
| voxtral-small-latest | SWE: - | 32K/8K | [AUDIO] | grouter-mistral | - | - |
| codestral-embed | SWE: - | 0K/0K | grouter-mistral | - | - |
| codestral-embed-2505 | SWE: - | 0K/0K | grouter-mistral | - | - |
| labs-leanstral-2603 | SWE: - | 0K/0K | grouter-mistral | - | - |
| Mistral Embed | SWE: - | 8K/3K | grouter-mistral | - | - |
| mistral-embed-2312 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-embed-dim128-2510 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-embed-dim256-2510 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-moderation-2411 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-moderation-latest | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-moderation-2603 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-ocr-2505 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-ocr-2512 | SWE: - | 0K/0K | grouter-mistral | - | - |
| mistral-ocr-latest | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-2602 | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-transcribe-2507 | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-realtime-2602 | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-realtime-latest | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-transcribe-realtime-2602 | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-tts-2603 | SWE: - | 0K/0K | grouter-mistral | - | - |
| voxtral-mini-tts-latest | SWE: - | 0K/0K | grouter-mistral | - | - |
| GLM-5-FP8 | grouter-modal | 72.8% | 77.8% |
| GLM-5-FP8-2 | grouter-modal | 72.8% | 77.8% |
| GLM-5.1-FP8 | grouter-modal | 72.8% | 77.8% |

## Legend

- **SWE-Lite**: SWE-bench Lite scores using mini-swe-agent v2 (300 issues). Lower cost, standardized protocol. Best for comparing models directly.
- **SWE-Verified**: SWE-bench Verified scores (500 issues). Each vendor may use custom scaffold — scores not comparable across providers but indicate maximum potential.

## Sources

- SWE-bench: https://www.swebench.com/

## Updating

Run `python3 scripts/fetch-benchmark-scores.py` to refresh scores. The script only adds new models; existing scores are preserved in cache.
Run with `--force` to refresh all scores from online sources.

