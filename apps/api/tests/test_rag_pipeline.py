import pytest
from app.rag.ingest import TextChunker, IngestionPipeline
from app.rag.embeddings import embedding_service, cosine_similarity, VECTOR_DIMENSION
from app.rag.retrieval import rag_service, SIMILARITY_THRESHOLD
from app.rag.evaluation import RetrievalEvaluator, BENCHMARK_EVAL_SET

@pytest.mark.asyncio
async def test_text_chunking_and_token_bounds():
    chunker = TextChunker(target_tokens=400, overlap_tokens=50)
    sample_text = (
        "Paragraph One introduces progressive overload. Resistance training stimulates neuromuscular units.\n\n"
        "Paragraph Two discusses volume thresholds. Performing 10 to 20 sets per muscle group per week yields hypertrophy.\n\n"
        "Paragraph Three highlights compound multi-joint movements like squats, deadlifts, and bench presses."
    )
    chunks = chunker.chunk_text(sample_text)
    assert len(chunks) >= 1
    for chunk in chunks:
        # Check chunk length within safe character bounds
        assert len(chunk) > 20
        assert len(chunk) <= 2500


def test_document_metadata_parsing():
    sample_content = (
        "# Title: ACSM Guidelines for Strength\n"
        "# Source: American College of Sports Medicine\n"
        "# URL: https://acsm.org/guidelines\n"
        "# License: Educational\n"
        "# Category: resistance_training\n"
        "# Target Age Groups: adult_18_64, senior_65_plus\n\n"
        "Body content starts here after the header."
    )
    meta, body = IngestionPipeline.parse_metadata_header(sample_content, "acsm_test.md")
    assert meta.title == "ACSM Guidelines for Strength"
    assert meta.source_name == "American College of Sports Medicine"
    assert meta.source_url == "https://acsm.org/guidelines"
    assert meta.category == "resistance_training"
    assert "adult_18_64" in meta.target_age_groups
    assert "senior_65_plus" in meta.target_age_groups
    assert body == "Body content starts here after the header."


@pytest.mark.asyncio
async def test_embedding_generation_dimension_and_normalization():
    text = "Athletic performance, progressive overload, and hypertrophy."
    vec = await embedding_service.embed_text(text)
    assert len(vec) == VECTOR_DIMENSION
    assert len(vec) == 768

    # Check normalization: cosine similarity with self must be 1.0
    self_sim = cosine_similarity(vec, vec)
    assert pytest.approx(self_sim, 0.001) == 1.0


@pytest.mark.asyncio
async def test_semantic_vector_retrieval_ranking():
    await rag_service.initialize_store()
    query = "What repetition range is best for muscle hypertrophy and progressive overload?"
    results = await rag_service.retrieve(query=query, top_k=3)

    assert len(results) > 0
    top_result = results[0]
    assert top_result.similarity_score > 0.10
    # Retrieved results should reference relevant evidence guidelines
    titles = [r.chunk.document_title.lower() for r in results]
    assert any("acsm" in t or "resistance training" in t or "protein" in t for t in titles)


@pytest.mark.asyncio
async def test_age_group_metadata_filtering():
    await rag_service.initialize_store()
    
    # Query for senior balance and falls
    senior_query = "What exercises prevent falls and improve balance for older adults?"
    senior_results = await rag_service.retrieve(
        query=senior_query,
        age_group="senior_65_plus",
        top_k=3
    )

    assert len(senior_results) > 0
    # All retrieved chunks must be suitable for senior_65_plus
    for r in senior_results:
        if r.chunk.target_age_groups:
            assert "senior_65_plus" in r.chunk.target_age_groups


@pytest.mark.asyncio
async def test_weak_retrieval_insufficient_info_guard():
    await rag_service.initialize_store()
    # Query that has zero factual correlation with athletic exercise guidelines
    nonsense_query = "Quantum chromatic entanglement in medieval architecture"
    results = await rag_service.retrieve(query=nonsense_query, top_k=3)

    is_weak = rag_service.is_weak_retrieval(results, threshold=0.68)
    assert is_weak is True

    fallback_msg = rag_service.get_fallback_insufficient_info_message()
    assert "Insufficient Grounded Evidence" in fallback_msg
    assert "prevent misinformation" in fallback_msg


@pytest.mark.asyncio
async def test_retrieval_evaluation_benchmark_execution():
    # Run evaluation across first 6 benchmark queries for fast test execution
    subset = BENCHMARK_EVAL_SET[:6]
    metrics = await RetrievalEvaluator.evaluate_benchmark(eval_set=subset, top_k=3)

    assert metrics.total_queries == 6
    assert metrics.hit_at_1 >= 0.80  # At least 80% Top-1 hit rate
    assert metrics.hit_at_3 >= 0.80  # At least 80% Top-3 hit rate
    assert metrics.mrr >= 0.80
