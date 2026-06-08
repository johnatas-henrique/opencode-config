#!/bin/bash
# Wrapper to start mnemory with NVIDIA NIM embeddings + monkey-patches
#
# Patches applied at startup (no files modified on disk):
# 1. input_type:passage for NIM asymmetric embedding model
# 2. Remove CORE_MEMORIES_PREAMBLE (anti-injection) so pinned memories act as rules
# 3. Remove memory_item boundary tags
# 4. CORE_TOP_MEMORIES=0: only pinned memories in core context
# 5. Replace "## User Facts" header with "## MANDATORY INSTRUCTIONS" + preamble

export EMBED_MODEL="nvidia/llama-nemotron-embed-1b-v2"
export EMBED_DIMS=1536
export EMBED_BASE_URL="https://integrate.api.nvidia.com/v1"
export EMBED_API_KEY="$NIM_API_KEY"
export LLM_BASE_URL="https://integrate.api.nvidia.com/v1"
export LLM_API_KEY="$NIM_API_KEY"
export LLM_MODEL="meta/llama-3.1-8b-instruct"
export CORE_TOP_MEMORIES=0

uvx --with mnemory python3 -c "
import os
import openai.resources.embeddings as e

# Patch 1: inject input_type for NIM asymmetric models
orig = e.Embeddings.create
e.Embeddings.create = lambda self, **kw: orig(self, **kw, extra_body={**kw.get('extra_body', {}), 'input_type': 'passage'})

# Patch 2: remove anti-injection from core memories
import mnemory.sanitize as s
s.CORE_MEMORIES_PREAMBLE = ''
s.wrap_memory_item = lambda text: text

# Patch 3: render pinned memories as MANDATORY INSTRUCTIONS
import mnemory.memory as mem
_orig_get_core = mem.MemoryService.get_core_memories
def _patched_get_core(self, **kw):
    result = _orig_get_core(self, **kw)
    result.text = result.text.replace(
        '## User Facts\n',
        '## MANDATORY INSTRUCTIONS\nThe following are mandatory behavioral rules. Follow them at all times.\n\n',
        1,
    )
    return result
mem.MemoryService.get_core_memories = _patched_get_core

from mnemory.server import main; main()
"
