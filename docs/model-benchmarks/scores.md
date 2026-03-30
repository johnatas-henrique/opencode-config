# Model Benchmark Scores

> **Note**: Scores are from multiple sources. SWE-Lite uses mini-swe-agent v2 (comparable). SWE-Verified uses vendor-optimized scaffolds (not directly comparable).

**Total models tracked**: 199  
**Cache updated**: 2026-04-21 21:37:35

## Quick Reference

| Model | Provider | SWE-Lite | SWE-Verified | LiveCodeBench | Aider |
|-------|----------|----------|--------------|---------------|-------|
| Manifest Auto (Routed 1M context) | manifest | - | - | - | - |
| Claude Haiku 4.5 (Kiro AI - Gratis) | omniroute | - | 73.3% | - | - |
| Claude Sonnet 4.5 (Kiro AI - Gratis) | omniroute | - | 77.2% | - | - |
| Llama 3.3 70B (Cloudflare AI - Gratis) | omniroute | - | 48.0% | - | - |
| Qwen2.5 Coder 15B (Cloudflare AI - Gratis) | omniroute | - | - | - | - |
| Gemini 2.5 Flash (180K/mes - Gratis) | omniroute | 46.7% | 55.1% | - | - |
| Kimi K2 Thinking (OmniRoute) | omniroute | - | 71.3% | - | - |
| LongCat Flash Lite (50M tokens/dia - Gratis) | omniroute | - | 70.0% | - | - |
| Llama 3.3 70B (NVIDIA NIM - Gratis) | omniroute | - | 48.0% | - | - |
| Claude 3.5 Sonnet (OpenRouter) | omniroute | - | 51.6% | - | - |
| DeepSeek R1 (OpenRouter) | omniroute | 41.4% | 71.4% | - | - |
| GPT-4o (OpenRouter) | omniroute | 21.6% | - | - | 21.6% |
| Llama 3.3 70B (OpenRouter) | omniroute | - | 48.0% | - | - |
| Qwen3 Coder Flash (Qwen Code - Gratis) | omniroute | 40.0% | 69.6% | - | - |
| Qwen3 Coder Next (Qwen Code - Gratis) | omniroute | 40.0% | 70.6% | - | - |
| Qwen3 Coder Plus (Qwen Code - Gratis) | omniroute | - | - | - | - |
| gpt-oss-120b | regolo | - | 62.4% | - | - |
| minimax-m2.5 | regolo | 75.8% | 80.2% | 78.8% | - |
| mistral-small-4-119b | regolo | - | 46.8% | - | - |
| qwen3-coder-next | regolo | 40.0% | 70.6% | - | - |
| qwen3.5-122b | regolo | - | 72.0% | - | - |
| DeepSeek V3.2 128K | nvidia | 70.0% | 73.0% | - | - |
| Kimi K2.5 256K | nvidia | 70.8% | 76.8% | - | - |
| GLM 5 204K | nvidia | - | - | - | - |
| GLM 4.7 131K | nvidia | - | - | - | - |
| Kimi K2 Thinking 256K | nvidia | - | 71.3% | - | - |
| MiniMax M2.1 196K | nvidia | - | 69.4% | - | - |
| MiniMax M2.5 204K | nvidia | 75.8% | 80.2% | 78.8% | - |
| Step 3.5 Flash 256K | nvidia | - | 74.4% | - | - |
| Qwen3 Coder 480B 262K | nvidia | - | 69.6% | - | - |
| Qwen3 235B 262K | nvidia | - | 73.1% | - | - |
| Devstral 2 123B 256K | nvidia | 37.5% | 72.2% | - | - |
| DeepSeek V3.1 Terminus 128K | nvidia | 38.8% | 73.0% | - | - |
| Kimi K2 Instruct 0905 256K | nvidia | - | 59.1% | - | - |
| Kimi K2 Instruct 256K | nvidia | - | 59.1% | - | - |
| MiniMax M2 196K | nvidia | - | 69.4% | - | - |
| Qwen3 80B Thinking 262K | nvidia | - | 69.6% | - | - |
| Qwen3 80B Instruct 262K | nvidia | - | 69.6% | - | - |
| Qwen3.5 400B VLM 262K | nvidia | - | 76.4% | - | - |
| GPT OSS 120B 131K | nvidia | - | 62.4% | - | - |
| Llama 4 Maverick 1M | nvidia | 21.0% | 70.7% | - | - |
| DeepSeek V3.1 128K | nvidia | 38.8% | 73.0% | - | - |
| Nemotron Ultra 253B 128K | nvidia | - | - | - | - |
| Mistral Large 675B 256K | nvidia | - | 33.3% | - | - |
| QwQ 32B 131K | nvidia | - | 42.0% | - | - |
| Colosseum 355B 16K | nvidia | - | - | - | - |
| Mistral Medium 3 32K | nvidia | - | 40.0% | - | - |
| Mistral Magistral Small 128K | nvidia | - | - | - | - |
| Nemotron Super 49B 128K | nvidia | - | - | - | - |
| Llama 4 Scout 10M | nvidia | 9.1% | 44.0% | - | - |
| Nemotron Nano 30B 1M | nvidia | - | - | - | - |
| DeepSeek R1 Distill 32B 128K | nvidia | 41.4% | 71.4% | - | - |
| GPT OSS 20B 128K | nvidia | - | 22.0% | - | - |
| Qwen2.5 Coder 32B 128K | nvidia | - | 9.0% | - | - |
| Llama 3.1 405B 128K | nvidia | - | 47.0% | - | - |
| Llama 3.3 70B 128K | nvidia | - | 48.0% | - | - |
| DeepSeek R1 Distill 14B 128K | nvidia | 41.4% | 71.4% | - | - |
| Seed OSS 36B 512K | nvidia | - | 26.0% | - | - |
| Stockmark 100B 128K | nvidia | - | - | - | - |
| Mixtral 8x22B 64K | nvidia | - | 36.0% | - | - |
| Ministral 14B 128K | nvidia | - | - | - | - |
| Granite 34B Code 8K | nvidia | - | 32.0% | - | - |
| DeepSeek R1 Distill 8B 128K | nvidia | 41.4% | 71.4% | - | - |
| DeepSeek R1 Distill 7B 128K | nvidia | 41.4% | 71.4% | - | - |
| Gemma 2 9B 4K | nvidia | - | - | - | - |
| Phi 3.5 Mini 128K | nvidia | - | - | - | - |
| Phi 4 Mini 128K | nvidia | - | - | - | - |
| MiniMax M2.5 | sambanova | 75.8% | 80.2% | 78.8% | - |
| DeepSeek R1 0528 | sambanova | 41.4% | 71.4% | - | - |
| DeepSeek V3.1 | sambanova | 38.8% | 73.0% | - | - |
| DeepSeek V3 0324 | sambanova | 70.0% | 38.8% | - | - |
| DeepSeek V3.2 | sambanova | 70.0% | 73.0% | - | - |
| Llama 4 Maverick | sambanova | 21.0% | 70.7% | - | - |
| GPT OSS 120B | sambanova | - | 62.4% | - | - |
| DeepSeek V3.1 Term | sambanova | 38.8% | 73.0% | - | - |
| Qwen3 32B | sambanova | - | 40.0% | - | - |
| Qwen3 235B Instruct 2507 | sambanova | - | 73.1% | - | - |
| R1 Distill 70B | sambanova | 41.4% | 47.0% | - | - |
| Llama 3.3 70B | sambanova | - | 48.0% | - | - |
| Llama 3.1 8B | sambanova | - | 23.0% | - | - |
| Claude Sonnet 4.5 | grouter-kiro | - | 77.2% | - | - |
| Claude Haiku 4.5 | grouter-kiro | - | 73.3% | - | - |
| DeepSeek 3.2 | grouter-kiro | - | - | - | - |
| DeepSeek 3.1 | grouter-kiro | - | - | - | - |
| Qwen3 Coder Next | grouter-kiro | 40.0% | 70.6% | - | - |
| Claude Opus 4.5 | grouter-openrouter | - | 80.9% | - | - |
| Claude Sonnet 4.5 | grouter-openrouter | - | 77.2% | - | - |
| GPT-4o | grouter-openrouter | 21.6% | - | - | 21.6% |
| Gemini 2.5 Pro | grouter-openrouter | - | 63.8% | - | - |
| DeepSeek R1 | grouter-openrouter | 41.4% | 71.4% | - | - |
| Llama 3.3 70B | grouter-openrouter | - | 48.0% | - | - |
| Gemini 2.5 Flash | grouter-kilocode | - | 55.1% | - | - |
| Gemini 2.5 Pro | grouter-kilocode | - | 63.8% | - | - |
| GPT-4.1 | grouter-kilocode | 23.9% | 54.6% | - | 52.4% |
| o3 | grouter-kilocode | - | 49.8% | - | 49.8% |
| Nemotron 3 Super | grouter-opencode | - | - | - | - |
| Gemini 3.1 Flash Lite Preview | grouter-gemini-cli | - | 78.0% | - | - |
| Gemini 2.5 Flash | grouter-gemini-cli | 46.7% | 55.1% | - | - |
| Cogito 2.1 671B | grouter-ollama | - | 35.0% | - | - |
| DeepSeek V3.1 671B | grouter-ollama | 38.8% | 73.0% | - | - |
| DeepSeek V3.2 | grouter-ollama | 70.0% | 73.0% | - | - |
| Devstral 2 123B | grouter-ollama | 37.5% | 72.2% | - | - |
| Devstral Small 2 24B | grouter-ollama | - | 68.0% | - | - |
| Gemini 3 Flash Preview | grouter-ollama | 75.8% | 78.0% | - | - |
| Gemma 3 12B | grouter-ollama | - | - | - | - |
| Gemma 3 27B | grouter-ollama | - | - | - | - |
| Gemma 3 4B | grouter-ollama | - | - | - | - |
| Gemma 4 31B | grouter-ollama | - | - | - | - |
| GLM 4.6 | grouter-ollama | - | 68.0% | - | - |
| GLM 5 | grouter-ollama | 72.8% | 77.8% | - | - |
| GPT OSS 120B | grouter-ollama | - | 62.4% | - | - |
| GPT OSS 20B | grouter-ollama | - | 22.0% | - | - |
| Kimi K2 Thinking | grouter-ollama | - | 71.3% | - | - |
| Kimi K2.5 | grouter-ollama | 70.8% | 76.8% | - | - |
| Kimi K2.6 | grouter-ollama | - | 80.2% | - | - |
| MiniMax M2 | grouter-ollama | 75.8% | 69.4% | 78.8% | - |
| MiniMax M2.1 | grouter-ollama | - | 69.4% | - | - |
| MiniMax M2.5 | grouter-ollama | 75.8% | 80.2% | 78.8% | - |
| MiniMax M2.7 | grouter-ollama | - | 80.2% | - | - |
| Ministral 14B | grouter-ollama | - | - | - | - |
| Ministral 3 3B | grouter-ollama | - | - | - | - |
| Ministral 3 8B | grouter-ollama | - | - | - | - |
| Mistral Large 3 675B | grouter-ollama | - | 33.3% | - | - |
| Nemotron Nano 30B | grouter-ollama | - | 49.8% | - | 49.8% |
| Nemotron 3 Super | grouter-ollama | - | - | - | - |
| Qwen3 Coder Next | grouter-ollama | 40.0% | 70.6% | - | - |
| Qwen3 Coder 480B | grouter-ollama | - | 69.6% | - | - |
| Qwen3 80B | grouter-ollama | - | 69.6% | - | - |
| Qwen3 VL 235B | grouter-ollama | - | 73.1% | - | - |
| Qwen3 VL 235B Instruct | grouter-ollama | - | 73.1% | - | - |
| Qwen3.5 397B | grouter-ollama | - | 76.4% | - | - |
| RNJ 1 8B | grouter-ollama | - | 18.0% | - | - |
| codestral-2508 | grouter-mistral | - | - | - | - |
| codestral-latest | grouter-mistral | - | - | - | - |
| devstral-2512 | grouter-mistral | - | 72.2% | - | - |
| devstral-latest | grouter-mistral | - | - | - | - |
| devstral-medium-latest | grouter-mistral | - | 61.6% | - | - |
| devstral-medium-2507 | grouter-mistral | - | 61.6% | - | - |
| devstral-small-2507 | grouter-mistral | - | 68.0% | - | - |
| labs-mistral-small-creative | grouter-mistral | - | - | - | - |
| magistral-medium-2509 | grouter-mistral | - | - | - | - |
| magistral-medium-latest | grouter-mistral | - | - | - | - |
| magistral-small-2509 | grouter-mistral | - | - | - | - |
| magistral-small-latest | grouter-mistral | - | - | - | - |
| ministral-14b-2512 | grouter-mistral | - | - | - | - |
| ministral-14b-latest | grouter-mistral | - | - | - | - |
| ministral-3b-2512 | grouter-mistral | - | - | - | - |
| ministral-3b-latest | grouter-mistral | - | - | - | - |
| ministral-8b-2512 | grouter-mistral | - | - | - | - |
| ministral-8b-latest | grouter-mistral | - | - | - | - |
| mistral-large-2411 | grouter-mistral | - | - | - | - |
| mistral-large-2512 | grouter-mistral | - | - | - | - |
| mistral-large-latest | grouter-mistral | - | - | - | - |
| mistral-medium-2505 | grouter-mistral | - | - | - | - |
| mistral-medium | grouter-mistral | - | 40.0% | - | - |
| mistral-medium-2508 | grouter-mistral | - | - | - | - |
| mistral-medium-latest | grouter-mistral | - | - | - | - |
| mistral-vibe-cli-with-tools | grouter-mistral | - | - | - | - |
| mistral-medium-2604 | grouter-mistral | - | - | - | - |
| mistral-medium-3 | grouter-mistral | - | 40.0% | - | - |
| mistral-medium-3-5 | grouter-mistral | - | 40.0% | - | - |
| mistral-medium-3.5 | grouter-mistral | - | 40.0% | - | - |
| mistral-medium-c21211-r0-75 | grouter-mistral | - | - | - | - |
| mistral-small-2506 | grouter-mistral | - | - | - | - |
| mistral-small-2603 | grouter-mistral | - | - | - | - |
| mistral-small-latest | grouter-mistral | - | - | - | - |
| mistral-vibe-cli-fast | grouter-mistral | - | - | - | - |
| mistral-vibe-cli-latest | grouter-mistral | - | - | - | - |
| mistral-tiny-2407 | grouter-mistral | - | - | - | - |
| mistral-tiny-latest | grouter-mistral | - | - | - | - |
| open-mistral-nemo | grouter-mistral | - | - | - | - |
| open-mistral-nemo-2407 | grouter-mistral | - | - | - | - |
| mistral-large-pixtral-2411 | grouter-mistral | - | - | - | - |
| pixtral-large-2411 | grouter-mistral | - | - | - | - |
| pixtral-large-latest | grouter-mistral | - | - | - | - |
| voxtral-mini-latest | grouter-mistral | - | - | - | - |
| voxtral-mini-2507 | grouter-mistral | - | - | - | - |
| voxtral-small-2507 | grouter-mistral | - | - | - | - |
| voxtral-small-latest | grouter-mistral | - | - | - | - |
| codestral-embed | grouter-mistral | - | - | - | - |
| codestral-embed-2505 | grouter-mistral | - | - | - | - |
| labs-leanstral-2603 | grouter-mistral | - | - | - | - |
| mistral-embed | grouter-mistral | - | - | - | - |
| mistral-embed-2312 | grouter-mistral | - | - | - | - |
| mistral-embed-dim128-2510 | grouter-mistral | - | - | - | - |
| mistral-embed-dim256-2510 | grouter-mistral | - | - | - | - |
| mistral-moderation-2411 | grouter-mistral | - | - | - | - |
| mistral-moderation-latest | grouter-mistral | - | - | - | - |
| mistral-moderation-2603 | grouter-mistral | - | - | - | - |
| mistral-ocr-2505 | grouter-mistral | - | - | - | - |
| mistral-ocr-2512 | grouter-mistral | - | - | - | - |
| mistral-ocr-latest | grouter-mistral | - | - | - | - |
| voxtral-mini-2602 | grouter-mistral | - | - | - | - |
| voxtral-mini-transcribe-2507 | grouter-mistral | - | - | - | - |
| voxtral-mini-realtime-2602 | grouter-mistral | - | - | - | - |
| voxtral-mini-realtime-latest | grouter-mistral | - | - | - | - |
| voxtral-mini-transcribe-realtime-2602 | grouter-mistral | - | - | - | - |
| voxtral-mini-tts-2603 | grouter-mistral | - | - | - | - |
| voxtral-mini-tts-latest | grouter-mistral | - | - | - | - |

## Legend

- **SWE-Lite**: SWE-bench Lite scores using mini-swe-agent v2 (300 issues). Lower cost, standardized protocol. Best for comparing models directly.
- **SWE-Verified**: SWE-bench Verified scores (500 issues). Each vendor may use custom scaffold — scores not comparable across providers but indicate maximum potential.
- **LiveCodeBench**: Competition problems (LeetCode/Codeforces style).
- **Aider**: Code editing benchmark (225 Exercism exercises across multiple languages).

## Sources

- SWE-bench: https://www.swebench.com/
- LiveCodeBench: https://www.livecodebench.org/
- Aider: https://aider.chat/docs/leaderboards/

## Updating

Run `python3 scripts/fetch-benchmark-scores.py` to refresh scores. The script only adds new models; existing scores are preserved in cache.

