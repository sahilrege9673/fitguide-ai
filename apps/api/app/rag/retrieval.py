import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.rag.ingest import DocumentChunk, IngestionPipeline
from app.rag.embeddings import embedding_service, cosine_similarity

logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD = 0.65

class RetrievalResult(BaseModel):
    chunk: DocumentChunk
    similarity_score: float

class RAGService:
    """
    Semantic vector retrieval and grounded context synthesis engine.
    Integrates 768-dimensional cosine vector search with demographic metadata filters
    and weak-retrieval threshold guards.
    """
    _INDEXED_CHUNKS: Optional[List[DocumentChunk]] = None

    @classmethod
    async def initialize_store(cls, force_reload: bool = False) -> List[DocumentChunk]:
        """Loads and embeds knowledge corpus chunks into vector index."""
        if cls._INDEXED_CHUNKS is None or force_reload:
            logger.info("Initializing RAG vector knowledge base...")
            cls._INDEXED_CHUNKS = await IngestionPipeline.load_and_chunk_corpus()
            logger.info(f"RAG store initialized with {len(cls._INDEXED_CHUNKS)} indexed knowledge chunks.")
        return cls._INDEXED_CHUNKS

    @classmethod
    async def retrieve(
        cls,
        query: str,
        age_group: Optional[str] = None,
        top_k: int = 3,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[RetrievalResult]:
        """
        Retrieves top-k relevant knowledge chunks using cosine similarity
        with optional age-group metadata filtering.
        """
        chunks = await cls.initialize_store()
        if not chunks or not query.strip():
            return []

        # Generate 768-dimensional embedding for query
        query_vec = await embedding_service.embed_text(query)

        scored_results: List[RetrievalResult] = []
        for chunk in chunks:
            # Metadata Filtering: Age group compatibility
            if age_group and chunk.target_age_groups:
                if age_group not in chunk.target_age_groups:
                    continue

            if not chunk.embedding:
                continue

            score = cosine_similarity(query_vec, chunk.embedding)
            scored_results.append(RetrievalResult(chunk=chunk, similarity_score=round(score, 4)))

        # Sort descending by similarity score
        scored_results.sort(key=lambda r: r.similarity_score, reverse=True)

        # Return top-k candidates
        return scored_results[:top_k]

    @classmethod
    def format_grounded_context(cls, results: List[RetrievalResult]) -> tuple[str, List[Dict[str, str]]]:
        """
        Formats retrieved knowledge chunks into structured citation context
        for prompt grounding and client citation cards.
        """
        if not results:
            return "", []

        lines = ["### RETRIEVED SCIENTIFIC GUIDELINES (GROUNDED EVIDENCE)"]
        citations = []

        for idx, res in enumerate(results, 1):
            chunk = res.chunk
            lines.append(f"\n[Source {idx}: {chunk.document_title} - {chunk.source_name}]")
            lines.append(f"Source URL: {chunk.source_url}")
            lines.append(f"Relevance Score: {res.similarity_score}")
            lines.append(f"Content Excerpt:\n{chunk.content}")

            citations.append({
                "source_number": str(idx),
                "title": chunk.document_title,
                "source_name": chunk.source_name,
                "url": chunk.source_url,
                "relevance_score": str(res.similarity_score)
            })

        lines.append("\n[DIRECTIVE: Ground your response strictly on the evidence above. Cite sources inline using [Source X] where applicable.]\n")
        return "\n".join(lines), citations

    @classmethod
    def is_weak_retrieval(cls, results: List[RetrievalResult], threshold: float = SIMILARITY_THRESHOLD) -> bool:
        """Determines if the top retrieved result falls below the confidence threshold."""
        if not results:
            return True
        return results[0].similarity_score < threshold

    @classmethod
    def get_fallback_insufficient_info_message(cls) -> str:
        """Standard non-hallucinatory message when retrieval confidence is inadequate."""
        return (
            "### Knowledge Base Advisory: Insufficient Grounded Evidence\n\n"
            "I do not have enough verified evidence in my fitness knowledge base to give a definitive, "
            "scientifically validated answer to this specific question. To prevent misinformation or "
            "unsupported claims, I cannot make definitive recommendations for this query.\n\n"
            "*Recommendation*: For specialized physical protocols or conditions outside standard public "
            "exercise guidelines, consult a certified strength and conditioning specialist (CSCS) or licensed sports physician."
        )

# Global singleton
rag_service = RAGService()
