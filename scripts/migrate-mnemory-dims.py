#!/usr/bin/env python3
"""Migrate mnemory Qdrant collection: 1536d (nemotron) → 1024d (bge-m3).

Preserves all payload (text, metadata) and BM25 sparse vectors.
Uses temp collection as safety buffer — original only deleted after
verification. Safe to re-run if interrupted (resumes from temp).
"""

import os, sys, time
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    Modifier,
    PointStruct,
    SparseVectorParams,
    VectorParams,
)
from openai import OpenAI

# ── Config ──────────────────────────────────────────────────────────

QDRANT_PATH = os.path.expanduser("~/.mnemory/qdrant")
COLLECTION = "mnemory"
TEMP_COLLECTION = "_mnemory_migrate_1024"
NEW_DIMS = 1024
EMBED_MODEL = "baai/bge-m3"
EMBED_BASE_URL = "https://integrate.api.nvidia.com/v1"
EMBED_API_KEY = os.environ.get("NIM_API_KEY", "")
BATCH_SIZE = 20  # NIM rate limits are generous, but keep reasonable

# ── Connect ─────────────────────────────────────────────────────────

client = QdrantClient(path=QDRANT_PATH)
embed_client = OpenAI(api_key=EMBED_API_KEY, base_url=EMBED_BASE_URL)

# ── Phase 1: Read all existing points ───────────────────────────────

print("Phase 1: Reading all points from collection...")
points, _ = client.scroll(
    collection_name=COLLECTION,
    limit=9999,
    with_payload=True,
    with_vectors=True,
)
print(f"  Found {len(points)} points")

info = client.get_collection(COLLECTION)
total = info.points_count or 0
print(f"  Collection reports {total} points")

if len(points) != total:
    print(f"  ERROR: scroll returned {len(points)} but collection has {total}")
    sys.exit(1)

# Extract dense vector size to confirm
vc = info.config.params.vectors
dims = vc.size if hasattr(vc, 'size') else None
print(f"  Current dims: {dims}")

# ── Phase 2: Create temp collection ─────────────────────────────────

print(f"\nPhase 2: Creating temp collection '{TEMP_COLLECTION}' ({NEW_DIMS}d)...")
existing = [c.name for c in client.get_collections().collections]

if TEMP_COLLECTION in existing:
    print(f"  Temp collection already exists — reusing (resume mode)")
else:
    client.create_collection(
        collection_name=TEMP_COLLECTION,
        vectors_config=VectorParams(size=NEW_DIMS, distance=Distance.COSINE),
        sparse_vectors_config={
            "bm25": SparseVectorParams(modifier=Modifier.IDF),
        },
    )
    print(f"  Created")

# ── Phase 3: Verify what's already in temp to skip if complete ──────

temp_info = client.get_collection(TEMP_COLLECTION)
temp_count = temp_info.points_count or 0
print(f"\nPhase 3: Temp collection has {temp_count}/{total} points")

if temp_count >= total:
    print(f"  Temp already complete ({temp_count} points) — using temp count as target")
    total = temp_count  # Trust the temp count over the original (may be partial after resume)
else:
    # Determine resume offset — find IDs already in temp
    processed = temp_count
    if processed > 0:
        temp_all, _ = client.scroll(
            collection_name=TEMP_COLLECTION,
            limit=9999,
            with_payload=False,
            with_vectors=False,
        )
        temp_ids = {p.id for p in temp_all}
        remaining = [p for p in points if p.id not in temp_ids]
        print(f"  Resuming: {len(remaining)} points remaining ({processed} already done)")
        points_to_process = remaining
    else:
        points_to_process = points

    # ── Phase 4: Re-embed and write to temp ─────────────────────────

    print(f"\nPhase 4: Re-embedding {len(points_to_process)} points with {EMBED_MODEL}...")
    start_time = time.monotonic()
    local_processed = 0

    for batch_start in range(0, len(points_to_process), BATCH_SIZE):
        batch = points_to_process[batch_start:batch_start + BATCH_SIZE]
        texts = [p.payload.get("data", "") if p.payload else "" for p in batch]

        resp = embed_client.embeddings.create(
            input=[t.replace("\n", " ") for t in texts],
            model=EMBED_MODEL,
        )
        sorted_data = sorted(resp.data, key=lambda d: d.index)
        new_vectors = [d.embedding for d in sorted_data]

        new_points = []
        for i, p in enumerate(batch):
            vectors = {"": new_vectors[i]}
            if isinstance(p.vector, dict) and "bm25" in p.vector:
                vectors["bm25"] = p.vector["bm25"]
            new_points.append(PointStruct(
                id=p.id,
                vector=vectors,
                payload=dict(p.payload or {}),
            ))

        client.upsert(collection_name=TEMP_COLLECTION, points=new_points)

        local_processed += len(batch)
        elapsed = time.monotonic() - start_time
        overall = processed + local_processed
        print(f"  [{overall}/{total}] batch of {len(batch)} done ({elapsed:.1f}s)", flush=True)

    elapsed = time.monotonic() - start_time
    print(f"\n  Re-embedding complete in {elapsed:.1f}s")

    # ── Phase 5: Verify temp collection ─────────────────────────────

    print(f"\nPhase 5: Verifying temp collection...")
    temp_info = client.get_collection(TEMP_COLLECTION)
    temp_count = temp_info.points_count or 0
    print(f"  Temp has {temp_count} points")

    if temp_count < total:
        print(f"  ERROR: temp has {temp_count}, expected {total}")
        print(f"  Original collection is intact. Temp collection preserved for recovery.")
        sys.exit(1)

    print(f"  Verified OK")

# ── Phase 6: Swap collections ───────────────────────────────────────

print(f"\nPhase 6: Swapping collections...")

# Delete original
print(f"  Deleting original collection '{COLLECTION}'...")
client.delete_collection(COLLECTION)

# Recreate with 1024d
print(f"  Recreating '{COLLECTION}' with {NEW_DIMS}d...")
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=NEW_DIMS, distance=Distance.COSINE),
    sparse_vectors_config={
        "bm25": SparseVectorParams(modifier=Modifier.IDF),
    },
)

# Copy back from temp — read all at once (only 337 points)
print(f"  Copying all points from temp in one scroll...")
all_temp, _ = client.scroll(
    collection_name=TEMP_COLLECTION,
    limit=9999,
    with_payload=True,
    with_vectors=True,
)
print(f"    read {len(all_temp)} points from temp")

new_points = []
for p in all_temp:
    vectors = {}
    if isinstance(p.vector, dict):
        for k, v in p.vector.items():
            vectors[k] = v
    else:
        vectors[""] = p.vector

    new_points.append(PointStruct(
        id=p.id,
        vector=vectors,
        payload=dict(p.payload or {}),
    ))

client.upsert(collection_name=COLLECTION, points=new_points)
print(f"    wrote {len(new_points)} points to '{COLLECTION}'")

# Verify
final_info = client.get_collection(COLLECTION)
final_count = final_info.points_count or 0
print(f"\n  Final collection has {final_count} points")

if final_count != total:
    print(f"  ERROR: final count {final_count} != expected {total}")
    print(f"  Temp collection '{TEMP_COLLECTION}' preserved for recovery.")
    sys.exit(1)

# Clean up temp
print(f"  Deleting temp collection...")
client.delete_collection(TEMP_COLLECTION)

print(f"\n✅ Migration complete! {total} points migrated to {NEW_DIMS}d ({EMBED_MODEL})")
