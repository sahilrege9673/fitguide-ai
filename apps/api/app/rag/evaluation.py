import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.rag.retrieval import rag_service, RetrievalResult

class EvaluationQuery(BaseModel):
    query_id: str
    query: str
    expected_doc_substring: str
    target_age_group: Optional[str] = None
    expected_topic: str

# 24 Ground-Truth Benchmark Evaluation Pairs
BENCHMARK_EVAL_SET: List[EvaluationQuery] = [
    # 1-4: ACSM Resistance Training
    EvaluationQuery(
        query_id="q01",
        query="What is progressive overload and how do I apply it to prevent plateaus?",
        expected_doc_substring="acsm_resistance_training",
        expected_topic="Progressive overload principles"
    ),
    EvaluationQuery(
        query_id="q02",
        query="What repetition range and rest periods are recommended for muscular hypertrophy?",
        expected_doc_substring="acsm_resistance_training",
        expected_topic="Hypertrophy rep ranges"
    ),
    EvaluationQuery(
        query_id="q03",
        query="How many working sets per muscle group per week should I do according to ACSM?",
        expected_doc_substring="acsm_resistance_training",
        expected_topic="Weekly volume thresholds"
    ),
    EvaluationQuery(
        query_id="q04",
        query="Why should compound multi-joint movements form the foundation of my training?",
        expected_doc_substring="acsm_resistance_training",
        expected_topic="Compound multi-joint movements"
    ),

    # 5-8: WHO Guidelines
    EvaluationQuery(
        query_id="q05",
        query="How many minutes of moderate-intensity aerobic exercise are recommended each week by WHO?",
        expected_doc_substring="who_physical_activity",
        expected_topic="Adult aerobic exercise duration"
    ),
    EvaluationQuery(
        query_id="q06",
        query="What are the physical activity recommendations for children and adolescents under 18?",
        expected_doc_substring="who_physical_activity",
        target_age_group="minor_under_18",
        expected_topic="Youth 60-min daily exercise"
    ),
    EvaluationQuery(
        query_id="q07",
        query="How frequently should adults perform muscle-strengthening activities each week?",
        expected_doc_substring="who_physical_activity",
        expected_topic="Adult muscle strengthening 2+ days"
    ),
    EvaluationQuery(
        query_id="q08",
        query="What are the health risks associated with high levels of sedentary behaviour?",
        expected_doc_substring="who_physical_activity",
        expected_topic="Sedentary behaviour health risks"
    ),

    # 9-12: NSCA Youth Athletics
    EvaluationQuery(
        query_id="q09",
        query="Does lifting weights damage growth plates or stunt growth in young athletes?",
        expected_doc_substring="nsca_youth_athletics",
        target_age_group="minor_under_18",
        expected_topic="Growth plate safety in youth lifting"
    ),
    EvaluationQuery(
        query_id="q10",
        query="Why is maximal 1RM testing prohibited for adolescent novice lifters?",
        expected_doc_substring="nsca_youth_athletics",
        target_age_group="minor_under_18",
        expected_topic="1RM prohibition for minors"
    ),
    EvaluationQuery(
        query_id="q11",
        query="What fundamental movement skills should youth athletic conditioning prioritize?",
        expected_doc_substring="nsca_youth_athletics",
        target_age_group="minor_under_18",
        expected_topic="Fundamental movement patterns"
    ),
    EvaluationQuery(
        query_id="q12",
        query="Why is severe caloric restriction hazardous for adolescent athletes?",
        expected_doc_substring="nsca_youth_athletics",
        target_age_group="minor_under_18",
        expected_topic="Prohibition of calorie deficits in youth"
    ),

    # 13-16: NIA Senior Guidelines
    EvaluationQuery(
        query_id="q13",
        query="What exercises prevent falls and improve balance for older adults?",
        expected_doc_substring="nia_older_adults_mobility",
        target_age_group="senior_65_plus",
        expected_topic="Balance drills and fall prevention"
    ),
    EvaluationQuery(
        query_id="q14",
        query="How can older adults mitigate age-related muscle loss and sarcopenia?",
        expected_doc_substring="nia_older_adults_mobility",
        target_age_group="senior_65_plus",
        expected_topic="Sarcopenia reversal through resistance training"
    ),
    EvaluationQuery(
        query_id="q15",
        query="What stretching guidelines maintain joint flexibility and mobility in seniors?",
        expected_doc_substring="nia_older_adults_mobility",
        target_age_group="senior_65_plus",
        expected_topic="Senior joint flexibility"
    ),
    EvaluationQuery(
        query_id="q16",
        query="Which low-impact aerobic modalities are recommended for arthritic joints?",
        expected_doc_substring="nia_older_adults_mobility",
        target_age_group="senior_65_plus",
        expected_topic="Low-impact cardio for older adults"
    ),

    # 17-20: ISSN Nutrition & Hydration
    EvaluationQuery(
        query_id="q17",
        query="How much total daily protein per kilogram of body weight is optimal for muscle building?",
        expected_doc_substring="issn_protein_hydration",
        expected_topic="Daily protein intake 1.4-2.0 g/kg"
    ),
    EvaluationQuery(
        query_id="q18",
        query="How much protein and leucine should be consumed per meal to trigger muscle protein synthesis?",
        expected_doc_substring="issn_protein_hydration",
        expected_topic="Leucine threshold and mTOR activation"
    ),
    EvaluationQuery(
        query_id="q19",
        query="Is there a strict 30-minute post-workout anabolic window for nutrient intake?",
        expected_doc_substring="issn_protein_hydration",
        expected_topic="Anabolic window timing reality"
    ),
    EvaluationQuery(
        query_id="q20",
        query="At what percentage of dehydration does athletic endurance and power start degrading?",
        expected_doc_substring="issn_protein_hydration",
        expected_topic="Dehydration threshold 2% body mass"
    ),

    # 21-24: CDC Cardiorespiratory Health
    EvaluationQuery(
        query_id="q21",
        query="How do I estimate my maximum heart rate using my age?",
        expected_doc_substring="cdc_cardiorespiratory_health",
        expected_topic="220 minus age formula"
    ),
    EvaluationQuery(
        query_id="q22",
        query="What is Zone 2 aerobic training and what heart rate percentage defines it?",
        expected_doc_substring="cdc_cardiorespiratory_health",
        expected_topic="Zone 2 50-70% MHR fat oxidation"
    ),
    EvaluationQuery(
        query_id="q23",
        query="How does the talk test differ between moderate and vigorous aerobic intensity?",
        expected_doc_substring="cdc_cardiorespiratory_health",
        expected_topic="Talk test guidelines"
    ),
    EvaluationQuery(
        query_id="q24",
        query="Why should beginners establish a baseline of Zone 2 cardio before high intensity interval training?",
        expected_doc_substring="cdc_cardiorespiratory_health",
        expected_topic="Aerobic base before HIIT"
    ),
]

class EvaluationMetrics(BaseModel):
    total_queries: int
    hit_at_1: float
    hit_at_3: float
    hit_at_5: float
    mrr: float
    details: List[Dict[str, Any]]

class RetrievalEvaluator:
    @classmethod
    async def evaluate_benchmark(
        cls, eval_set: List[EvaluationQuery] = BENCHMARK_EVAL_SET, top_k: int = 5
    ) -> EvaluationMetrics:
        await rag_service.initialize_store()

        hit_1_count = 0
        hit_3_count = 0
        hit_5_count = 0
        reciprocal_ranks = []
        details = []

        for item in eval_set:
            results = await rag_service.retrieve(
                query=item.query,
                age_group=item.target_age_group,
                top_k=top_k,
                threshold=0.0  # Measure raw retrieval ranking
            )

            # Check positions of expected document
            found_rank: Optional[int] = None
            for rank, r in enumerate(results, 1):
                chunk_file = getattr(r.chunk, 'filename', '').lower()
                doc_title = r.chunk.document_title.lower()
                expected = item.expected_doc_substring.lower()

                if expected in chunk_file or expected in doc_title or expected.replace("_", " ") in doc_title:
                    found_rank = rank
                    break

            if found_rank == 1:
                hit_1_count += 1
            if found_rank and found_rank <= 3:
                hit_3_count += 1
            if found_rank and found_rank <= 5:
                hit_5_count += 1

            rr = 1.0 / found_rank if found_rank else 0.0
            reciprocal_ranks.append(rr)

            details.append({
                "query_id": item.query_id,
                "query": item.query,
                "expected": item.expected_doc_substring,
                "found_rank": found_rank,
                "reciprocal_rank": round(rr, 4),
                "top_retrieved_title": results[0].chunk.document_title if results else "None",
                "top_similarity_score": results[0].similarity_score if results else 0.0
            })

        total = len(eval_set)
        return EvaluationMetrics(
            total_queries=total,
            hit_at_1=round(hit_1_count / total, 4),
            hit_at_3=round(hit_3_count / total, 4),
            hit_at_5=round(hit_5_count / total, 4),
            mrr=round(sum(reciprocal_ranks) / total, 4),
            details=details
        )

if __name__ == "__main__":
    async def main():
        print("Running RAG Retrieval Evaluation Benchmark (24 Queries)...")
        metrics = await RetrievalEvaluator.evaluate_benchmark()
        print("\n--- BENCHMARK RESULTS ---")
        print(f"Total Queries Evaluated: {metrics.total_queries}")
        print(f"Hit Rate @ 1: {metrics.hit_at_1 * 100:.1f}%")
        print(f"Hit Rate @ 3: {metrics.hit_at_3 * 100:.1f}%")
        print(f"Hit Rate @ 5: {metrics.hit_at_5 * 100:.1f}%")
        print(f"Mean Reciprocal Rank (MRR): {metrics.mrr:.4f}")

    asyncio.run(main())
