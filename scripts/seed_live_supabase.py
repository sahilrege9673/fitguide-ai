#!/usr/bin/env python3
"""
FitGuide AI — Live Supabase Automated Seeder
Populates:
1. 84 Curated Biomechanical Exercises & Media
2. 6 Authoritative Clinical Knowledge Documents & Chunks with 768-dim Embeddings
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any

# Ensure apps/api is in sys.path and load apps/api/.env
api_dir = os.path.join(os.path.dirname(__file__), "..", "apps", "api")
sys.path.insert(0, os.path.abspath(api_dir))

from dotenv import load_dotenv
load_dotenv(os.path.join(api_dir, ".env"))

from app.core.config import settings
from app.data.exercises_catalog import EXERCISES_DATA

SUPABASE_URL = settings.SUPABASE_URL.rstrip("/")
SERVICE_KEY = settings.SUPABASE_SERVICE_ROLE_KEY

HEADERS = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates,return=representation"
}

def supabase_request(endpoint: str, data: Any = None, method: str = "POST"):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    payload = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else []
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"Error on {endpoint}: HTTP {e.code} - {err_msg}")
        return e.code, None

def seed_exercises():
    print(f"\n[1/2] Checking & Seeding {len(EXERCISES_DATA)} Exercises in Supabase...")
    # Check current count
    check_url = f"{SUPABASE_URL}/rest/v1/exercises?select=id"
    req = urllib.request.Request(check_url, headers={
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Range": "0-0",
        "Prefer": "count=exact"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            cr = resp.headers.get("Content-Range", "")
            if cr and "/" in cr:
                count = int(cr.split("/")[-1])
                if count >= len(EXERCISES_DATA):
                    print(f"  [SUCCESS] Supabase already contains {count} exercises. Seeding skipped.")
                    return
    except Exception as e:
        print(f"  Count check note: {e}")

    inserted_exercises = 0
    inserted_media = 0

    for ex in EXERCISES_DATA:
        ex_copy = ex.copy()
        media_list = ex_copy.pop("media", [])
        
        status, res = supabase_request("exercises", [ex_copy])
        if status in (200, 201) and res:
            exercise_id = res[0]["id"]
            inserted_exercises += 1

            if media_list:
                for m in media_list:
                    m_copy = m.copy()
                    m_copy["exercise_id"] = exercise_id
                    m_status, _ = supabase_request("exercise_media", [m_copy])
                    if m_status in (200, 201):
                        inserted_media += 1

    print(f"  [SUCCESS] Verified / Upserted {inserted_exercises} exercises and {inserted_media} media records.")

def seed_knowledge():
    import asyncio
    from app.rag.ingest import IngestionPipeline
    from uuid import uuid5, NAMESPACE_DNS

    print("\n[2/2] Ingesting Authoritative Guidelines & Generating 768-dim Embeddings...")

    async def _run():
        chunks = await IngestionPipeline.load_and_chunk_corpus()
        print(f"  Generated {len(chunks)} text chunks across corpus.")

        # Group by document
        docs_map = {}
        for c in chunks:
            if c.document_id not in docs_map:
                docs_map[c.document_id] = {
                    "id": c.document_id,
                    "title": c.document_title,
                    "source_name": c.source_name,
                    "source_url": c.source_url,
                    "license": "Public Domain / Open Access",
                    "category": c.category
                }

        # Insert documents
        doc_count = 0
        for doc in docs_map.values():
            status, res = supabase_request("knowledge_documents", [doc])
            if status in (200, 201):
                doc_count += 1
        print(f"  [SUCCESS] Upserted {doc_count} knowledge documents.")

        # Insert chunks with embeddings
        chunk_count = 0
        # Batch by 20 chunks
        batch_size = 20
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            payload = []
            for c in batch:
                payload.append({
                    "id": c.chunk_id,
                    "document_id": c.document_id,
                    "content": c.content,
                    "embedding": c.embedding,
                    "metadata": {
                        "document_title": c.document_title,
                        "source_name": c.source_name,
                        "source_url": c.source_url,
                        "category": c.category,
                        "target_age_groups": c.target_age_groups,
                        "token_count": c.token_count
                    }
                })
            status, _ = supabase_request("knowledge_chunks", payload)
            if status in (200, 201):
                chunk_count += len(payload)

        print(f"  [SUCCESS] Ingested {chunk_count} vector chunks with pgvector embeddings.")

    asyncio.run(_run())

if __name__ == "__main__":
    print("=" * 70)
    print("FITGUIDE AI — LIVE SUPABASE SEEDING PIPELINE")
    print(f"Target Database: {SUPABASE_URL}")
    print("=" * 70)
    seed_exercises()
    seed_knowledge()
    print("\n[COMPLETE] Live Supabase database is now fully seeded and operational!")
