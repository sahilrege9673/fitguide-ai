import math
import hashlib
import re
from typing import List
import httpx
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

VECTOR_DIMENSION = 768

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two float vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot / (norm1 * norm2)


class LocalDeterministicEmbedder:
    """
    Offline/Fallback embedding generator producing 768-dimensional normalized vectors.
    Uses n-gram semantic hashing with L2 normalization so semantic overlap
    produces high cosine similarity without external network dependencies.
    """
    def __init__(self, dimension: int = VECTOR_DIMENSION):
        self.dimension = dimension

    def embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dimension
        clean = re.sub(r"[^\w\s]", "", text.lower())
        words = clean.split()
        if not words:
            return [0.0] * self.dimension

        # Single word and bigram hashing
        tokens = words + [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        for token in tokens:
            # Deterministic hash to dimension index
            h = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            sign = 1.0 if (h >> 16) % 2 == 0 else -1.0
            vec[idx] += sign

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec


class EmbeddingService:
    """
    Unified Embedding Service.
    Calls Gemini gemini-embedding-001 (outputDimensionality: 768) when API key is active;
    falls back cleanly to LocalDeterministicEmbedder for offline tests.
    """
    def __init__(self, use_local: bool = False):
        self.use_local = use_local
        self.local_embedder = LocalDeterministicEmbedder(dimension=VECTOR_DIMENSION)
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent"

    async def embed_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * VECTOR_DIMENSION

        if self.use_local or not self.api_key or not self.api_key.strip():
            return self.local_embedder.embed(text)

        url = f"{self.base_url}?key={self.api_key}"
        payload = {
            "content": {"parts": [{"text": text[:2000]}]},
            "outputDimensionality": VECTOR_DIMENSION
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    values = data.get("embedding", {}).get("values", [])
                    if len(values) == VECTOR_DIMENSION:
                        return values
                logger.warning(f"Gemini embedding API returned status {resp.status_code}. Using fallback embedder.")
        except Exception as e:
            logger.warning(f"Gemini embedding error: {e}. Using fallback embedder.")

        return self.local_embedder.embed(text)

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            vec = await self.embed_text(text)
            results.append(vec)
        return results

# Singleton instance
embedding_service = EmbeddingService()
